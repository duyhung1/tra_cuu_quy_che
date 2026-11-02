"""T-019: error mapping of the Claude adapter, without network calls."""

from types import SimpleNamespace

import anthropic
import httpx
import pytest

from app.modules.qa.adapters.anthropic_llm import AnthropicLLM
from app.modules.qa.ports import LLMUnavailable, RetrievedChunk
from app.modules.qa.prompts import NOT_FOUND_ANSWER

CHUNKS = [RetrievedChunk("a.pdf", 1, "Nội dung", 0.9)]


def adapter_raising(exc: BaseException | None = None, resp=None) -> AnthropicLLM:
    llm = AnthropicLLM(api_key="test-key", model="claude-opus-5-5", timeout_s=5, max_tokens=256)

    async def create(**_):
        if exc is not None:
            raise exc
        return resp

    llm._client = SimpleNamespace(messages=SimpleNamespace(create=create))  # type: ignore[assignment]
    return llm


def status_error(code: int) -> anthropic.APIStatusError:
    req = httpx.Request("POST", "https://api.anthropic.com/v1/messages")
    return anthropic.APIStatusError("err", response=httpx.Response(code, request=req), body=None)


@pytest.mark.parametrize(
    "exc",
    [
        TypeError('"Could not resolve authentication method. Expected one of api_key, auth_token..."'),
        status_error(500),
        status_error(401),
        anthropic.APIConnectionError(request=httpx.Request("POST", "https://api.anthropic.com")),
    ],
    ids=["no-credentials", "server-error", "unauthorized", "connection"],
)
async def test_failures_map_to_llm_unavailable(exc):
    with pytest.raises(LLMUnavailable):
        await adapter_raising(exc).answer("Hỏi?", CHUNKS)


async def test_unrelated_type_error_is_not_swallowed():
    with pytest.raises(TypeError):
        await adapter_raising(TypeError("bug in our code")).answer("Hỏi?", CHUNKS)


def response(stop_reason: str, text: str = "Trả lời."):
    return SimpleNamespace(
        stop_reason=stop_reason,
        usage=SimpleNamespace(input_tokens=10, output_tokens=5),
        content=[SimpleNamespace(type="thinking", thinking=""), SimpleNamespace(type="text", text=text)],
    )


async def test_text_blocks_are_joined_and_thinking_ignored():
    result = await adapter_raising(resp=response("end_turn", "Tạm ứng 30%.")).answer("Hỏi?", CHUNKS)
    assert (result.text, result.input_tokens, result.output_tokens) == ("Tạm ứng 30%.", 10, 5)


async def test_refusal_returns_not_found_answer():
    result = await adapter_raising(resp=response("refusal", "")).answer("Hỏi?", CHUNKS)
    assert result.text == NOT_FOUND_ANSWER
