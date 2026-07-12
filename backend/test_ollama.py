import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3",
        "prompt": "What is cloud computing?",
        "stream": False
    }
)

print(response.json()["response"])