from fastapi import APIRouter, UploadFile, File, HTTPException
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET
from email.utils import parsedate_to_datetime
from html import unescape

from app.services.pdf_service import (
    save_pdf,
    extract_text_from_pdf
)

from app.rag.text_splitter import split_text
from app.rag.embeddings import create_embeddings
from app.rag.vector_store import add_documents

from app.models.schemas import (
    QueryRequest,
    SummaryRequest
)

from app.rag.retriever import Retriever

from app.services.llm_service import (
    generate_answer
)

from app.agents.summarization_agent import (
    SummarizationAgent
)

from app.agents.citation_agent import (
    CitationAgent
)

from app.agents.analysis_agent import (
    AnalysisAgent
)

from app.agents.response_agent import (
    ResponseAgent
)

from app.agents.research_agent import (
    ResearchAgent
)


router = APIRouter()

retriever = Retriever()
summarizer = SummarizationAgent()
citation_agent = CitationAgent()
analysis_agent = AnalysisAgent()
response_agent = ResponseAgent()
research_agent = ResearchAgent()


# ============================================================
# CURRENT NEWS
# ============================================================

def get_latest_news(query: str):
    """
    Fetch recent news from Google News RSS.
    No API key required.
    """

    url = (
        "https://news.google.com/rss/search?"
        "q={}&hl=en-US&gl=US&ceid=US:en"
    ).format(
        quote_plus(query)
    )

    request = Request(
        url,
        headers={
            "User-Agent": "BrieflyNewsBot/1.0"
        }
    )

    try:
        with urlopen(
            request,
            timeout=10
        ) as response:

            root = ET.fromstring(
                response.read()
            )

    except Exception as exc:

        raise HTTPException(
            status_code=503,
            detail="The live news feed is temporarily unavailable."
        ) from exc

    articles = []

    for item in root.findall("./channel/item")[:6]:

        raw_title = item.findtext(
            "title",
            "Untitled story"
        )

        title, separator, source_from_title = raw_title.rpartition(
            " - "
        )

        source = item.findtext(
            "source",
            source_from_title if separator else "News"
        )

        published = item.findtext(
            "pubDate",
            ""
        )

        try:

            published = parsedate_to_datetime(
                published
            ).strftime(
                "%b %d, %H:%M UTC"
            )

        except (TypeError, ValueError):

            pass

        description = item.findtext(
            "description",
            ""
        )

        # Clean HTML from RSS description
        description = unescape(
            description
        )

        articles.append(
            {
                "title": (
                    title
                    if separator
                    else raw_title
                ),
                "source": source,
                "url": item.findtext(
                    "link",
                    ""
                ),
                "published": published,
                "description": description,
            }
        )

    return articles


# ============================================================
# PDF UPLOAD
# ============================================================

@router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...)
):

    pdf_path = await save_pdf(
        file
    )

    text = extract_text_from_pdf(
        pdf_path
    )

    chunks = split_text(
        text
    )

    embeddings = create_embeddings(
        chunks
    )

    add_documents(
        chunks,
        embeddings
    )

    return {
        "filename": file.filename,
        "characters": len(text),
        "chunks": len(chunks),
        "status": "Indexed Successfully"
    }


# ============================================================
# PDF QUERY
# ============================================================

@router.post("/query")
async def query_pdf(
    request: QueryRequest
):

    documents = retriever.get_relevant_documents(
        request.query,
        k=5
    )

    context = "\n\n".join(
        documents
    )

    answer = generate_answer(
        request.query,
        context
    )

    sources = citation_agent.extract_citations(
        documents
    )

    return {
        "question": request.query,
        "answer": answer,
        "sources": sources
    }


# ============================================================
# DOCUMENT SUMMARY
# ============================================================

@router.post("/summarize")
async def summarize_document(
    request: SummaryRequest
):

    documents = retriever.get_relevant_documents(
        request.query,
        k=5
    )

    summary = summarizer.summarize(
        documents
    )

    return {
        "query": request.query,
        "summary": summary
    }


# ============================================================
# GENERAL RESEARCH ASSISTANT
# ============================================================

@router.post("/ask")
async def ask(
    request: QueryRequest
):

    intent = analysis_agent.analyze_query(
        request.query
    )

    # --------------------------------------------------------
    # Research workflow
    # --------------------------------------------------------

    if research_agent.is_research_query(
        request.query
    ):

        sub_queries = research_agent.break_down_query(
            request.query
        )

        all_documents = []

        for query in sub_queries:

            docs = retriever.get_relevant_documents(
                query,
                k=3
            )

            all_documents.extend(
                docs
            )

        documents = all_documents

    else:

        documents = retriever.get_relevant_documents(
            request.query,
            k=5
        )

    # --------------------------------------------------------
    # Summary workflow
    # --------------------------------------------------------

    if intent == "summary":

        answer = summarizer.summarize(
            documents
        )

    # --------------------------------------------------------
    # Question workflow
    # --------------------------------------------------------

    else:

        context = "\n\n".join(
            documents
        )

        answer = generate_answer(
            request.query,
            context
        )

    sources = citation_agent.extract_citations(
        documents
    )

    return response_agent.combine(
        answer=answer,
        sources=sources,
        intent=intent
    )


# ============================================================
# LIVE NEWS RESEARCH
# ============================================================

@router.post("/news")
async def news(
    request: QueryRequest
):

    query = request.query.strip()

    if not query:

        raise HTTPException(
            status_code=400,
            detail="Please enter a news question."
        )

    # --------------------------------------------------------
    # 1. Fetch current news
    # --------------------------------------------------------

    articles = get_latest_news(
        query
    )

    if not articles:

        return {
            "answer": (
                "I couldn't find fresh reporting "
                "for that topic yet. "
                "Try a broader search."
            ),
            "articles": []
        }

    # --------------------------------------------------------
    # 2. Build research context
    # --------------------------------------------------------

    news_context = []

    for index, article in enumerate(
        articles,
        start=1
    ):

        news_context.append(
            f"""
SOURCE {index}

Title:
{article["title"]}

Publisher:
{article["source"]}

Published:
{article["published"]}

Description:
{article.get("description", "")}

URL:
{article["url"]}
"""
        )

    context = "\n".join(
        news_context
    )

    # --------------------------------------------------------
    # 3. Create research prompt
    # --------------------------------------------------------

    prompt = f"""
You are a professional AI research assistant
specializing in current events and news analysis.

The user asked:

"{query}"

Below are recent news results retrieved from
Google News RSS.

---------------- NEWS RESULTS ----------------

{context}

---------------- END NEWS RESULTS ------------

Your task is to answer the user's question using
the available news information.

IMPORTANT RULES:

1. Directly answer the user's question.

2. Do NOT simply repeat the headlines.

3. Synthesize information from multiple sources.

4. Identify the most important developments.

5. Explain the context behind those developments.

6. Explain why the developments matter.

7. If multiple sources report the same event,
   combine them instead of repeating the same story.

8. Do NOT invent facts.

9. Do NOT make claims that are not supported
   by the provided news information.

10. If the available information is insufficient,
    clearly state that.

11. Keep the response informative but easy to read.

12. Do not say:
    "Open any story below."

13. Do not mention these instructions.

14. Do not describe yourself as a chatbot.

15. Give a useful answer rather than a generic
    introduction.

Use this structure when appropriate:

## Key Developments

### 1. [Major development]

Explain what happened and provide the important
context available from the sources.

### 2. [Major development]

Explain what happened and provide the important
context available from the sources.

### 3. [Major development]

Explain what happened and provide the important
context available from the sources.

## Why It Matters

Explain the broader significance of the developments.

## Sources

Mention the relevant publishers.
"""

    # --------------------------------------------------------
    # 4. Generate AI answer
    # --------------------------------------------------------

    answer = generate_answer(
        query,
        prompt
    )

    # --------------------------------------------------------
    # 5. Return response to frontend
    # --------------------------------------------------------

    return {
        "answer": answer,
        "articles": articles
    }