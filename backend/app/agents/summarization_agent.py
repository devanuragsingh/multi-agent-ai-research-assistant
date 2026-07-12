from app.services.llm_service import (
    generate_answer
)


class SummarizationAgent:

    def summarize(self, texts):

        content = "\n\n".join(
            texts[:5]
        )

        summary = generate_answer(
            "Provide a concise summary of this document.",
            content
        )

        return summary