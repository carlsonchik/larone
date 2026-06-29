"""Tests for LangGraph integration helpers."""

from langchain_core.messages import AIMessage

from lar1.langgraph import (
    attach_lar1_message,
    lar1_for_node,
    middleware_tag_node,
    read_lar1_message,
)


def test_attach_and_read():
    msg = AIMessage(content="hi")
    tagged = attach_lar1_message(msg, {"C": "obs", "L": 0.9, "V": "verified_tool"})
    block = read_lar1_message(tagged)
    assert block is not None
    assert block["C"] == "obs"


def test_middleware_tag_node():
    msg = AIMessage(content="research output")
    tagged = middleware_tag_node("researcher", msg)
    block = read_lar1_message(tagged)
    assert block["C"] == "obs"


def test_lar1_for_node_critic():
    fields = lar1_for_node("critic")
    assert fields["C"] == "rev"
