"""Generate PDF fixtures for tests (T-016). Run: python tests/fixtures/make_pdfs.py

Files are small and deterministic; big ones (21 MB, 301 pages) are generated
on the fly inside the tests instead of being committed.
"""

from pathlib import Path

import pymupdf

HERE = Path(__file__).parent / "pdfs"

# Fictional company and documents (no real customer data). Pages are kept short:
# insert_textbox silently drops text that does not fit the box.
SAMPLE_DOCS = {
    "Quy_che_chi_tieu_noi_bo_2025.pdf": [
        "CÔNG TY CỔ PHẦN SAO MAI\nSố: 08/2025/QC-SM\n\nHà Nội, ngày 20 tháng 12 năm 2024\n\n"
        "QUY CHẾ\nCHI TIÊU NỘI BỘ\n\n"
        "Chương I\nQUY ĐỊNH CHUNG\n\n"
        "Điều 1. Phạm vi điều chỉnh\n"
        "Quy chế này quy định các khoản chi công tác phí, tiếp khách và văn phòng phẩm của Công ty.\n\n"
        "Điều 2. Hiệu lực thi hành\n"
        "Quy chế này có hiệu lực từ ngày 01/01/2025.\n\n"
        "Chương II\nCHẾ ĐỘ CÔNG TÁC PHÍ\n\n"
        "Điều 5. Phụ cấp lưu trú\n"
        "1. Người được cử đi công tác được hưởng phụ cấp lưu trú 300.000 đồng/ngày.\n"
        "2. Trường hợp đi công tác trong ngày (đi và về trong ngày) được hưởng 150.000 đồng.",
        "Điều 6. Phương tiện đi lại\n"
        "1. Chặng đi từ 300 km trở lên được mua vé máy bay hạng phổ thông.\n"
        "2. Chặng dưới 300 km đi bằng tàu hỏa, ô tô hoặc xe của Công ty.\n\n"
        "Chương III\nCHI TIẾP KHÁCH\n\n"
        "Điều 8. Mức chi tiếp khách\n"
        "Mức chi tiếp khách tối đa 2.000.000 đồng/lần và phải được Trưởng phòng phê duyệt trước.",
    ],
    "Noi_quy_lao_dong_2025.pdf": [
        "CÔNG TY CỔ PHẦN SAO MAI\nSố: 15/2025/NQ-SM\n\nHà Nội, ngày 10 tháng 3 năm 2025\n\n"
        "NỘI QUY LAO ĐỘNG\n\n"
        "Điều 4. Thời giờ làm việc\n"
        "1. Thời giờ làm việc từ 08 giờ 00 đến 17 giờ 30, từ thứ Hai đến thứ Sáu.\n"
        "2. Thời gian nghỉ trưa từ 12 giờ 00 đến 13 giờ 30.\n\n"
        "Điều 7. Nghỉ phép năm\n"
        "1. Người lao động làm việc đủ 12 tháng được nghỉ 12 ngày phép năm hưởng nguyên lương.\n"
        "2. Cứ đủ 05 năm làm việc thì số ngày nghỉ phép năm được tăng thêm 01 ngày.",
        "Điều 9. Xử lý vi phạm giờ giấc\n"
        "Người lao động đi muộn quá 03 lần trong một tháng bị xử lý kỷ luật bằng hình thức khiển trách.\n\n"
        "Điều 12. Hiệu lực\n"
        "Nội quy này có hiệu lực kể từ ngày ký.",
    ],
    "Quyet_dinh_sua_doi_cong_tac_phi_2026.pdf": [
        "CÔNG TY CỔ PHẦN SAO MAI\nSố: 02/2026/QĐ-SM\n\nHà Nội, ngày 15 tháng 6 năm 2026\n\n"
        "QUYẾT ĐỊNH\nVề việc sửa đổi mức phụ cấp lưu trú\n\n"
        "Điều 1. Sửa đổi Điều 5 Quy chế chi tiêu nội bộ số 08/2025/QC-SM\n"
        "1. Phụ cấp lưu trú khi đi công tác là 450.000 đồng/ngày.\n"
        "2. Đi công tác tại các tỉnh miền núi, hải đảo được hưởng 500.000 đồng/ngày.\n\n"
        "Điều 2. Hiệu lực thi hành\n"
        "Quyết định này có hiệu lực từ ngày 01/07/2026 và thay thế khoản 1 Điều 5 của Quy chế số 08/2025/QC-SM.",
    ],
}


def _find_unicode_font() -> str | None:
    for path in (
        "C:/Windows/Fonts/arial.ttf",
        "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
        "/Library/Fonts/Arial Unicode.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
        "/usr/share/fonts/dejavu/DejaVuSans.ttf",
    ):
        if Path(path).exists():
            return path
    return None


def text_pdf(pages: list[str]) -> bytes:
    """A real text-layer PDF with Vietnamese diacritics."""
    font = _find_unicode_font()
    doc = pymupdf.open()
    for body in pages:
        page = doc.new_page()
        rect = pymupdf.Rect(50, 50, 545, 790)
        if font:
            page.insert_textbox(rect, body, fontsize=11, fontname="vn", fontfile=font)
        else:  # Fallback: built-in font (diacritics may be lost, still a text layer)
            page.insert_textbox(rect, body, fontsize=11)
    if font:
        doc.subset_fonts()  # embed only the glyphs used, otherwise the file is ~23 MB
    data = doc.tobytes(garbage=4, deflate=True)
    doc.close()
    return data


def many_pages_pdf(n: int) -> bytes:
    doc = pymupdf.open()
    for i in range(n):
        doc.new_page().insert_text((72, 72), f"Trang {i + 1} co noi dung van ban de kiem thu.")
    data = doc.tobytes()
    doc.close()
    return data


def encrypted_pdf() -> bytes:
    doc = pymupdf.open(stream=text_pdf(["Tài liệu mật có mật khẩu bảo vệ, nội dung đủ dài để có văn bản."]))
    data = doc.tobytes(encryption=pymupdf.PDF_ENCRYPT_AES_256, user_pw="secret", owner_pw="owner")
    doc.close()
    return data


def scanned_pdf() -> bytes:
    """Pages containing only an image, no text layer."""
    doc = pymupdf.open()
    pix = pymupdf.Pixmap(pymupdf.csRGB, pymupdf.IRect(0, 0, 200, 100), False)
    pix.clear_with(200)
    for _ in range(3):
        page = doc.new_page()
        page.insert_image(pymupdf.Rect(50, 50, 450, 250), pixmap=pix)
    data = doc.tobytes()
    doc.close()
    return data


def corrupted_pdf() -> bytes:
    data = text_pdf(["Nội dung sẽ bị cắt mất phần cuối để làm hỏng tệp PDF này cho kiểm thử."])
    return b"%PDF-1.7\n" + data[9 : len(data) // 3]


def fake_pdf() -> bytes:
    return b"PK\x03\x04 this is a docx (zip) renamed to .pdf"


def write_all() -> None:
    (HERE / "sample").mkdir(parents=True, exist_ok=True)
    for name, pages in SAMPLE_DOCS.items():
        (HERE / "sample" / name).write_bytes(text_pdf(pages))
    (HERE / "encrypted.pdf").write_bytes(encrypted_pdf())
    (HERE / "scanned.pdf").write_bytes(scanned_pdf())
    (HERE / "corrupted.pdf").write_bytes(corrupted_pdf())
    (HERE / "fake.pdf").write_bytes(fake_pdf())


if __name__ == "__main__":
    write_all()
    print("fixtures written to", HERE)
