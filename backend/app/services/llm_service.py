import requests


def generate_answer(question, context):

    prompt = f"""
Use the provided context to answer the question.

Context:
{context}

Question:
{question}

Answer:
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

    data = response.json()

    if "response" not in data:
        raise Exception(f"Ollama returned: {data}")

    return data["response"]