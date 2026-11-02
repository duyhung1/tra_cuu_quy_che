from datetime import date

import pytest

from app.modules.answer.prompt import NOT_FOUND_ANSWER, SYSTEM_PROMPT, build_user_message
from app.modules.answer.service import NoReadyDocuments, QuestionInvalid, ask
from app.ports.ai import RetrievedChunk
from tests.fakes.fakes import FakeEmbedder, FakeLLM


class FakeRetriever:
    async def search(self, qvec, top_n):
        return [RetrievedChunk("a.pdf", 3, "Nội dung A", 0.9, article="Điều 5")][:top_n]


async def run(question="Hỏi gì đó?", ready=1, embedder=None, llm=None):
    return await ask(
        question,
        ready_documents=ready,
        embedder=embedder or FakeEmbedder(),
        retriever=FakeRetriever(),
        llm=llm or FakeLLM(),
        top_n=12,
    )


async def test_ok_outcome_with_sources():
    llm = FakeLLM("Trả lời [1]. Bịa [4].")
    out = await run(llm=llm)
    assert out.status == "ok" and out.answer == "Trả lời [1]. Bịa." and out.chunk_count == 1
    assert [(s.ref, s.article) for s in out.sources] == [(1, "Điều 5")]
    assert llm.last_chunks[0].filename == "a.pdf"


async def test_not_found_answer_has_no_sources():
    out = await run(llm=FakeLLM(NOT_FOUND_ANSWER))
    assert out.answer == NOT_FOUND_ANSWER and out.sources == []


@pytest.mark.parametrize("q", ["", "   ", "x" * 2001])
async def test_invalid_question(q):
    with pytest.raises(QuestionInvalid):
        await run(question=q)


async def test_question_is_stripped_and_2000_chars_allowed():
    llm = FakeLLM()
    await run(question="  " + "x" * 2000 + "  ", llm=llm)
    assert llm.last_question == "x" * 2000


async def test_no_ready_documents_does_not_call_embedder():
    emb = FakeEmbedder()
    with pytest.raises(NoReadyDocuments):
        await run(ready=0, embedder=emb)
    assert emb.calls == 0


@pytest.mark.parametrize("which", ["embedder", "llm"])
async def test_external_failure_is_error_outcome(which):
    kwargs = {"embedder": FakeEmbedder(fail=True)} if which == "embedder" else {"llm": FakeLLM(fail=True)}
    out = await run(**kwargs)
    assert out.status == "error" and out.answer is None


def test_prompt_contains_required_rules_and_context_format():
    for key in ("<van_ban>", NOT_FOUND_ANSWER, "không phải chỉ dẫn", "hiệu lực muộn hơn", "[1]"):
        assert key in SYSTEM_PROMPT
    plain = RetrievedChunk("a.pdf", 7, "Đoạn văn", 0.8)
    full = RetrievedChunk("QC.pdf", 3, "Mức 300.000", 0.9, article="Điều 5", chapter="Chương II",
                          doc_title="QUY CHẾ CHI TIÊU", doc_number="08/2025/QC-SM", effective_date=date(2025, 1, 1))
    msg = build_user_message("Câu hỏi?", [plain, full])
    assert "[1] a.pdf — trang 7:" in msg
    assert ("[2] QC.pdf — QUY CHẾ CHI TIÊU (Số 08/2025/QC-SM, hiệu lực 01/01/2025) — "
            "Chương II, Điều 5, trang 3:") in msg
    assert msg.endswith("Câu hỏi: Câu hỏi?")
