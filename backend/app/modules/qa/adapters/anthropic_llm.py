"""Claude adapter for LLMPort (T-019). Non-streaming in the MVP."""

import anthropic
import structlog

from app.modules.qa.ports import LLMResult, LLMUnavailable, RetrievedChunk
from app.modules.qa.prompts import NOT_FOUND_ANSWER, PROMPT_VERSION, SYSTEM_PROMPT, build_user_message

log = structlog.get_logger("llm")


class AnthropicLLM:
    def __init__(self, api_key: str, model: str, timeout_s: float, max_tokens: int) -> None:
        self._client = anthropic.AsyncAnthropic(api_key=api_key or None, max_retries=2, timeout=timeout_s)
        self._model = model
        self._max_tokens = max_tokens

    async def answer(self, question: str, chunks: list[RetrievedChunk]) -> LLMResult:
        try:
            resp = await self._client.messages.create(
                model=self._model,
                max_tokens=self._max_tokens,
                output_config={"effort": "low"},
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": build_user_message(question, chunks)}],
            )
        except anthropic.RateLimitError as exc:
            raise LLMUnavailable("rate_limited") from exc
        except anthropic.APIStatusError as exc:
            if exc.status_code >= 500:
                raise LLMUnavailable(f"status_{exc.status_code}") from exc
            log.error("llm_request_rejected", status=exc.status_code, model=self._model)
            raise LLMUnavailable(f"status_{exc.status_code}") from exc
        except (anthropic.APIConnectionError, anthropic.APITimeoutError) as exc:
            raise LLMUnavailable("connection") from exc
        except anthropic.AnthropicError as exc:
            log.error("llm_sdk_error", error=type(exc).__name__, model=self._model)
            raise LLMUnavailable("sdk_error") from exc
        except TypeError as exc:
            # The SDK raises TypeError before sending anything when no credentials are configured.
            if "authentication" not in str(exc).lower():
                raise
            log.error("llm_not_configured", hint="set ANTHROPIC_API_KEY", model=self._model)
            raise LLMUnavailable("not_configured") from exc

        usage = resp.usage
        log.info(
            "llm_answer",
            model=self._model,
            prompt_version=PROMPT_VERSION,
            stop_reason=resp.stop_reason,
            input_tokens=usage.input_tokens,
            output_tokens=usage.output_tokens,
            chunk_count=len(chunks),
        )
        if resp.stop_reason == "refusal":
            return LLMResult(NOT_FOUND_ANSWER, usage.input_tokens, usage.output_tokens)
        if resp.stop_reason == "max_tokens":
            log.warning("llm_answer_truncated", model=self._model)

        text = "".join(block.text for block in resp.content if block.type == "text").strip()
        return LLMResult(text or NOT_FOUND_ANSWER, usage.input_tokens, usage.output_tokens)
