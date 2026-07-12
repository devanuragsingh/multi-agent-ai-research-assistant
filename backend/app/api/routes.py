from fastapi import APIRouter, UploadFile, File, HTTPException
from urllib.parse import quote_plus
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET
from email.utils import parsedate_to_datetime

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


def get_latest_news(query: str):
    """Read public Google News RSS results without needing an API key."""
    url = "https://news.google.com/rss/search?q={}&hl=en-US&gl=US&ceid=US:en".format(
        quote_plus(query)
    )
    request = Request(url, headers={"User-Agent": "BrieflyNewsBot/1.0"})
    try:
        with urlopen(request, timeout=10) as response:
            root = ET.fromstring(response.read())
    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail="The live news feed is temporarily unavailable."
        ) from exc

    articles = []
    for item in root.findall("./channel/item")[:6]:
        raw_title = item.findtext("title", "Untitled story")
        title, separator, source_from_title = raw_title.rpartition(" - ")
        source = item.findtext("source", source_from_title if separator else "News")
        published = item.findtext("pubDate", "")
        try:
            published = parsedate_to_datetime(published).strftime("%b %d, %H:%M UTC")
        except (TypeError, ValueError):
            pass
        articles.append({
            "title": title if separator else raw_title,
            "source": source,
            "url": item.findtext("link", ""),
            "published": published,
        })
    return articles


@router.post("/upload-pdf")
async def upload_pdf(
    file: UploadFile = File(...)
):

    pdf_path = await save_pdf(file)

    text = extract_text_from_pdf(
        pdf_path
    )

    chunks = split_text(text)

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


@router.post("/ask")
async def ask(
    request: QueryRequest
):

    intent = analysis_agent.analyze_query(
        request.query
    )

    # Research Workflow
    if research_agent.is_research_query(
        request.query
    ):

        sub_queries = (
            research_agent.break_down_query(
                request.query
            )
        )

        all_documents = []

        for query in sub_queries:

            docs = (
                retriever.get_relevant_documents(
                    query,
                    k=3
                )
            )

            all_documents.extend(
                docs
            )

        documents = all_documents

    else:

        documents = (
            retriever.get_relevant_documents(
                request.query,
                k=5
            )
        )

    # Summary Workflow
    if intent == "summary":

        answer = (
            summarizer.summarize(
                documents
            )
        )

    # Question Workflow
    else:

        context = "\n\n".join(
            documents
        )

        answer = generate_answer(
            request.query,
            context
        )

    sources = (
        citation_agent.extract_citations(
            documents
        )
    )

    return response_agent.combine(
        answer=answer,
        sources=sources,
        intent=intent
    )


@router.post("/news")
async def news(request: QueryRequest):
    """A lightweight, current-news chat endpoint with transparent source links."""
    query = request.query.strip()
    if not query:
        raise HTTPException(status_code=400, detail="Please enter a news question.")
    articles = get_latest_news(query)
    if not articles:
        return {"answer": "I couldn't find fresh reporting for that topic yet. Try a broader search.", "articles": []}
    names = ", ".join(article["source"] for article in articles[:3])
    return {
        "answer": f"Here are the latest headlines about {query}. I found current reporting from {names}. Open any story below for the full context.",
        "articles": articles,
    }
