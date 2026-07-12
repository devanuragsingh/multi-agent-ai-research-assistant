from app.agents.research_agent import ResearchAgent

agent = ResearchAgent()

print(
    agent.break_down_query(
        "Compare AWS and Azure and Google Cloud"
    )
)

print(
    agent.is_research_query(
        "Compare AWS and Azure"
    )
)

print(
    agent.is_research_query(
        "What is cloud computing?"
    )
)