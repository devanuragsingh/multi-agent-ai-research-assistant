from app.agents.analysis_agent import (
    AnalysisAgent
)

agent = AnalysisAgent()

print(
    agent.analyze_query(
        "Summarize cloud computing"
    )
)

print(
    agent.analyze_query(
        "What is cloud computing?"
    )
)

print(
    agent.analyze_query(
        "Give sources for cloud computing"
    )
)