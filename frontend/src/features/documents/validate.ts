export const MAX_FILES = 10;
export const MAX_MB = 20;
export const MAX_BYTES = MAX_MB * 1024 * 1024;

export interface RejectedFile {
  filename: string;
  error_code: 'not_pdf' | 'file_too_large';
}

export interface ValidationResult {
  /** Quá số tệp cho phép → không gửi gì cả. */
  tooMany: boolean;
  accepted: File[];
  rejected: RejectedFile[];
}

function isPdf(f: File): boolean {
  const byName = /\.pdf$/i.test(f.name);
  const byType = !f.type || f.type === 'application/pdf';
  return byName && byType;
}

/** Kiểm tra phía client trước khi gửi: số tệp, phần mở rộng, dung lượng. */
export function validateFiles(files: File[]): ValidationResult {
  if (files.length === 0 || files.length > MAX_FILES) {
    return { tooMany: files.length > MAX_FILES, accepted: [], rejected: [] };
  }
  const accepted: File[] = [];
  const rejected: RejectedFile[] = [];
  for (const f of files) {
    if (!isPdf(f)) rejected.push({ filename: f.name, error_code: 'not_pdf' });
    else if (f.size > MAX_BYTES) rejected.push({ filename: f.name, error_code: 'file_too_large' });
    else accepted.push(f);
  }
  return { tooMany: false, accepted, rejected };
}
