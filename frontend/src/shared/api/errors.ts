import i18n from '../i18n';
import { ApiError } from './client';

const KNOWN = new Set([
  'not_pdf', 'file_too_large', 'too_many_files', 'duplicate_name', 'collection_full',
  'encrypted_pdf', 'no_text_layer', 'too_many_pages', 'corrupted', 'transient_exhausted',
  'question_invalid', 'no_documents', 'ai_unavailable', 'storage_error', 'internal_error',
  'network', 'unknown',
]);

/** Thông điệp tiếng Việt cho một mã lỗi; mã lạ → thông điệp chung. */
export function messageForCode(code: string | null | undefined): string {
  const key = code && KNOWN.has(code) ? code : 'unknown';
  return i18n.t(`errors.${key}`);
}

export function messageForError(err: unknown): string {
  if (err instanceof ApiError) return messageForCode(err.code);
  return messageForCode('unknown');
}
