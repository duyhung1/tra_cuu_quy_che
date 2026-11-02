"""Error codes and Vietnamese messages — the single source (blueprint §5, NFR-007)."""

ERRORS: dict[str, tuple[int, str]] = {
    "too_many_files": (400, "Mỗi lần chỉ tải tối đa 10 tệp"),
    "not_pdf": (200, "Không phải tệp PDF hợp lệ"),
    "file_too_large": (200, "Tệp vượt quá 20 MB"),
    "too_many_pages": (200, "Văn bản dài hơn 300 trang"),
    "encrypted_pdf": (200, "Tệp có mật khẩu"),
    "no_text_layer": (200, "PDF dạng ảnh chưa được hỗ trợ"),
    "corrupted": (200, "Tệp bị hỏng"),
    "duplicate_name": (200, "Đã có văn bản cùng tên"),
    "collection_full": (200, "Kho đã đủ 50 văn bản"),
    "storage_error": (200, "Không lưu được văn bản, vui lòng thử lại"),
    "question_invalid": (422, "Câu hỏi phải có từ 1 đến 2000 ký tự"),
    "no_documents": (409, "Chưa có văn bản nào Sẵn sàng để trả lời"),
    "ai_unavailable": (503, "Hệ thống đang bận, vui lòng thử lại"),
}


class AppError(Exception):
    def __init__(self, code: str) -> None:
        if code not in ERRORS:
            raise ValueError(f"unknown error code {code}")
        super().__init__(code)
        self.code = code

    @property
    def status(self) -> int:
        return ERRORS[self.code][0]

    @property
    def message(self) -> str:
        return ERRORS[self.code][1]
