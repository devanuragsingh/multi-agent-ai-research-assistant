import requests


def generate_answer(question, context):

    prompt = f"""
You are a professional AI news research assistant.

Answer the user's question using ONLY the provided news context.

USER QUESTION:
{question}

NEWS CONTEXT:
{context}

INSTRUCTIONS:

1. Give a concise but useful answer.
2. Do NOT repeat the user's question.
3. Start with a short 1-2 sentence overview.
4. Organize the answer using Markdown headings.
5. Use bullet points for individual stories.
6. Make important facts and story titles bold.
7. Explain why the most important developments matter.
8. Mention the source naturally when relevant.
9. Do not invent facts that are not present in the context.
10. Do not create a separate "Sources" section because the frontend handles sources.
11. Keep the answer around 250-400 words maximum.
12. Avoid unnecessary repetition.
13. Leave blank lines between sections.
14. Use clean Markdown.

PREFERRED FORMAT:

## Today's Brief

A short overview of the biggest developments.

### 1. **Headline**

2-3 sentences explaining what happened and why it matters.

### 2. **Headline**

2-3 sentences explaining what happened and why it matters.

### 3. **Headline**

2-3 sentences explaining what happened and why it matters.

## Why It Matters

A short conclusion explaining the broader significance.

Now answer the user.
"""

    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3:latest",
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    print("STATUS:", response.status_code)
    print("RAW RESPONSE:")
    print(response.text)

    response.raise_for_status()

    data = response.json()

    if "response" not in data:
        raise Exception(f"Ollama returned: {data}")

    return data["response"].strip()