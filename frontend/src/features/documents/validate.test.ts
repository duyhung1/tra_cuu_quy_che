import { describe, expect, it } from 'vitest';
import { MAX_BYTES, validateFiles } from './validate';

function file(name: string, size = 1024, type = 'application/pdf'): File {
  const f = new File(['x'], name, { type });
  Object.defineProperty(f, 'size', { value: size });
  return f;
}

describe('validateFiles', () => {
  it('chấp nhận PDF hợp lệ', () => {
    const r = validateFiles([file('a.pdf'), file('b.PDF')]);
    expect(r.tooMany).toBe(false);
    expect(r.accepted.map((f) => f.name)).toEqual(['a.pdf', 'b.PDF']);
    expect(r.rejected).toEqual([]);
  });

  it('> 10 tệp → tooMany, không gửi tệp nào', () => {
    const r = validateFiles(Array.from({ length: 11 }, (_, i) => file(`f${i}.pdf`)));
    expect(r.tooMany).toBe(true);
    expect(r.accepted).toEqual([]);
  });

  it('tệp không phải .pdf → not_pdf; tệp quá 20 MB → file_too_large; tệp hợp lệ vẫn được giữ', () => {
    const r = validateFiles([
      file('note.docx', 1024, 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'),
      file('big.pdf', MAX_BYTES + 1),
      file('ok.pdf'),
    ]);
    expect(r.rejected).toEqual([
      { filename: 'note.docx', error_code: 'not_pdf' },
      { filename: 'big.pdf', error_code: 'file_too_large' },
    ]);
    expect(r.accepted.map((f) => f.name)).toEqual(['ok.pdf']);
  });

  it('đổi đuôi .pdf nhưng MIME khác → not_pdf', () => {
    const r = validateFiles([file('fake.pdf', 1024, 'application/msword')]);
    expect(r.rejected[0]?.error_code).toBe('not_pdf');
  });
});
