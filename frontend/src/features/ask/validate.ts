export const MAX_QUESTION_CHARS = 2000;

export interface QuestionCheck {
  trimmed: string;
  length: number;
  over: number;
  valid: boolean;
}

/** Hợp lệ khi không rỗng sau trim và không quá 2000 ký tự (độ dài đếm trên chuỗi gốc). */
export function checkQuestion(raw: string): QuestionCheck {
  const trimmed = raw.trim();
  const length = raw.length;
  const over = Math.max(0, length - MAX_QUESTION_CHARS);
  return { trimmed, length, over, valid: trimmed.length > 0 && over === 0 };
}
