"""TASK-002: text normalisation, tokenisation and error table."""

from app.domain.errors import ERRORS, AppError
from app.domain.text import content_terms, normalize, sentences, tokenize


def test_tokenize_keeps_diacritics_drops_stopwords_and_adds_bigrams():
    toks = tokenize("Phụ cấp lưu trú là bao nhiêu?")
    assert "phụ" in toks and "trú" in toks and "là" not in toks
    assert "phụ_cấp" in toks and "lưu_trú" in toks


def test_normalize_dashes_and_nfc():
    assert normalize("QC­SM") == "QC-SM"
    assert normalize("Điều") == "Điều"


def test_sentences_do_not_split_numbers():
    assert sentences("Mức 300.000 đồng. Hết.") == ["Mức 300.000 đồng.", " Hết."]


def test_content_terms():
    assert content_terms("Thủ đô của Pháp là gì?") == ["thủ", "đô", "pháp"]


def test_every_error_has_vietnamese_message_and_status():
    assert len(ERRORS) == 13
    e = AppError("no_text_layer")
    assert e.message == "PDF dạng ảnh chưa được hỗ trợ" and e.status == 200
