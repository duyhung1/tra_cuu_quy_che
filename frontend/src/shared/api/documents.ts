import { apiFetch } from './client';

export type DocumentStatus = 'queued' | 'processing' | 'ready' | 'failed';

export interface DocumentItem {
  id: string;
  filename: string;
  pages: number | null;
  uploaded_at: string;
  status: DocumentStatus;
  error_code: string | null;
  /** Số hiệu, tên và ngày hiệu lực đọc được từ nội dung văn bản (null nếu không tìm thấy). */
  doc_number: string | null;
  title: string | null;
  effective_date: string | null;
}

export interface DocumentCounts {
  ready: number;
  processing: number;
  failed: number;
  total: number;
}

export interface DocumentsResponse {
  items: DocumentItem[];
  counts: DocumentCounts;
  limit: number;
}

export type UploadItem =
  | { filename: string; document_id: string; status: 'queued' }
  | { filename: string; error_code: string };

export interface UploadResponse {
  items: UploadItem[];
}

export function listDocuments(): Promise<DocumentsResponse> {
  return apiFetch<DocumentsResponse>('/documents');
}

export function uploadDocuments(files: File[]): Promise<UploadResponse> {
  const form = new FormData();
  for (const f of files) form.append('files', f, f.name);
  return apiFetch<UploadResponse>('/documents', { method: 'POST', body: form });
}
