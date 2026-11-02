import { describe, expect, it } from 'vitest';
import { checkQuestion, MAX_QUESTION_CHARS } from './validate';

describe('checkQuestion', () => {
  it('rỗng hoặc chỉ khoảng trắng → không hợp lệ', () => {
    expect(checkQuestion('').valid).toBe(false);
    expect(checkQuestion('   \n ').valid).toBe(false);
  });

  it('câu hỏi bình thường → hợp lệ, trả về chuỗi đã trim', () => {
    const r = checkQuestion('  Điều khoản thanh toán là gì?  ');
    expect(r.valid).toBe(true);
    expect(r.trimmed).toBe('Điều khoản thanh toán là gì?');
  });

  it('đúng 2000 ký tự → hợp lệ; 2001 → không hợp lệ và báo số ký tự vượt', () => {
    expect(checkQuestion('a'.repeat(MAX_QUESTION_CHARS)).valid).toBe(true);
    const r = checkQuestion('a'.repeat(MAX_QUESTION_CHARS + 1));
    expect(r.valid).toBe(false);
    expect(r.over).toBe(1);
  });
});
