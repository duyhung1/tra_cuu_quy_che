from app.worker.chunker import chunk_document, chunk_pages
from app.worker.extract import ExtractedPage


def words(text: str) -> int:  # simple token counter for tests: 1 word = 1 token
    return len(text.split())


def sentence(i: int, n: int = 20) -> str:
    return " ".join(f"w{i}_{j}" for j in range(n - 1)) + " end."


def test_long_page_is_split_within_limits_and_overlaps():
    page = ExtractedPage(1, " ".join(sentence(i) for i in range(150)))  # ~3000 tokens
    chunks = chunk_pages([page], "a.pdf", target=500, max_tokens=800, overlap=75, count=words)
    assert len(chunks) >= 5
    assert all(c.token_count <= 800 for c in chunks)
    assert all(c.page_start == c.page_end == 1 for c in chunks)
    # consecutive chunks share text (overlap)
    assert chunks[0].content.split()[-1] in chunks[1].content
    assert [c.index for c in chunks] == list(range(len(chunks)))


def test_short_pages_are_merged_with_next():
    pages = [ExtractedPage(1, "ngắn " * 30), ExtractedPage(2, "ngắn " * 30), ExtractedPage(3, "dài " * 200)]
    chunks = chunk_pages(pages, "b.pdf", count=words)
    assert len(chunks) == 1
    assert (chunks[0].page_start, chunks[0].page_end) == (1, 3)


def test_chunks_never_span_two_normal_pages():
    pages = [ExtractedPage(1, "một " * 300), ExtractedPage(2, "hai " * 300)]
    chunks = chunk_pages(pages, "c.pdf", count=words)
    assert [(c.page_start, c.page_end) for c in chunks] == [(1, 1), (2, 2)]


def test_empty_pages_skipped_and_embed_text_has_prefix():
    pages = [ExtractedPage(1, ""), ExtractedPage(2, "nội dung " * 100)]
    chunks = chunk_pages(pages, "Quy_che.pdf", count=words)
    assert len(chunks) == 1
    assert chunks[0].embed_text.startswith("Quy_che.pdf — trang 2: ")
    assert not chunks[0].content.startswith("Quy_che.pdf")


# --- chunk_document: article-aware (default chunker of the worker) ---


def clause(i: int, n: int = 40) -> str:
    return f"{i}. " + " ".join(f"k{i}_{j}" for j in range(n - 2)) + " hết."


def test_one_chunk_per_article_with_chapter_and_pages():
    pages = [
        ExtractedPage(1, "QUY CHẾ\nChương II\nCÔNG TÁC PHÍ\nĐiều 5. Phụ cấp\n1. Mức 300.000 đồng."),
        ExtractedPage(2, "2. Trong ngày 150.000 đồng.\nĐiều 6. Phương tiện\nMáy bay."),
    ]
    chunks = chunk_document(pages, "Quy_che.pdf", count=words)
    assert [(c.article, c.page_start, c.page_end) for c in chunks] == [
        (None, 1, 1),
        ("Điều 5", 1, 2),
        ("Điều 6", 2, 2),
    ]
    art5 = chunks[1]
    assert art5.chapter == "Chương II. CÔNG TÁC PHÍ"
    assert art5.content.startswith("Điều 5. Phụ cấp") and "150.000" in art5.content
    assert art5.embed_text.startswith("Quy_che.pdf — Chương II. CÔNG TÁC PHÍ: Điều 5.")


def test_long_article_is_split_on_clauses_and_repeats_heading():
    body = "\n".join(clause(i) for i in range(1, 31))  # 30 clauses x 40 words
    chunks = chunk_document([ExtractedPage(1, f"Điều 3. Định mức\n{body}")], "a.pdf",
                            target=200, max_tokens=300, count=words)
    assert len(chunks) > 1
    assert all(c.article == "Điều 3" and c.token_count <= 300 for c in chunks)
    assert chunks[0].content.startswith("Điều 3. Định mức\n1. ")
    assert all(c.content.startswith("Điều 3. Định mức (tiếp)\n") for c in chunks[1:])
    # clauses are never cut in the middle
    for c in chunks[1:]:
        assert c.content.splitlines()[1].split(" ")[0].endswith(".")


def test_very_long_clause_falls_back_to_sentences():
    long_clause = "1. " + " ".join(sentence(i) for i in range(30))  # ~600 words in one clause
    chunks = chunk_document([ExtractedPage(1, f"Điều 1. Dài\n{long_clause}")], "a.pdf",
                            target=200, max_tokens=300, count=words)
    assert len(chunks) >= 2 and all(c.token_count <= 300 for c in chunks)


def test_document_without_articles_uses_page_chunker():
    pages = [ExtractedPage(1, "một " * 300), ExtractedPage(2, "hai " * 300)]
    chunks = chunk_document(pages, "c.pdf", count=words)
    assert [(c.page_start, c.article) for c in chunks] == [(1, None), (2, None)]
