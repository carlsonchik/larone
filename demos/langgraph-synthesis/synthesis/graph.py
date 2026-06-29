"""LangGraph wiring for researcher → critic → synthesizer."""

from __future__ import annotations

from typing import Annotated, TypedDict

from langchain_core.messages import AIMessage
from langgraph.graph import END, StateGraph
from langgraph.graph.message import add_messages

from synthesis.agents import critic, researcher, researcher_hypothesis, synthesizer


class State(TypedDict):
    messages: Annotated[list, add_messages]
    topic: str
    use_lar1: bool
    include_hypothesis: bool


def node_researcher(state: State) -> dict:
    msgs = [researcher(state["topic"])]
    if state.get("include_hypothesis"):
        msgs.append(researcher_hypothesis(state["topic"]))
    return {"messages": msgs}


def node_critic(state: State) -> dict:
    return {"messages": [critic(state["topic"])]}


def node_synthesizer(state: State) -> dict:
    agent_msgs = [m for m in state["messages"] if isinstance(m, AIMessage)]
    return {
        "messages": [
            synthesizer(agent_msgs, use_lar1=state.get("use_lar1", False))
        ]
    }


def build_graph() -> StateGraph:
    g = StateGraph(State)
    g.add_node("researcher", node_researcher)
    g.add_node("critic", node_critic)
    g.add_node("synthesizer", node_synthesizer)
    g.set_entry_point("researcher")
    g.add_edge("researcher", "critic")
    g.add_edge("critic", "synthesizer")
    g.add_edge("synthesizer", END)
    return g


def run_pipeline(
    topic: str = "agent protocols",
    *,
    use_lar1: bool = False,
    include_hypothesis: bool = True,
) -> str:
    graph = build_graph().compile()
    result = graph.invoke(
        {
            "messages": [],
            "topic": topic,
            "use_lar1": use_lar1,
            "include_hypothesis": include_hypothesis,
        }
    )
    final = result["messages"][-1]
    return final.content
