import { postJson } from './client';

/** Một trích đoạn được câu trả lời dẫn bằng [ref]. */
export interface Source {
  ref: number;
  filename: string;
  page: number;
  article: string | null;
  chapter: string | null;
  doc_title: string | null;
  doc_number: string | null;
  effective_date: string | null;
}

export interface AskResponse {
  answer: string;
  latency_ms: number;
  sources: Source[];
}

export function ask(question: string): Promise<AskResponse> {
  return postJson<AskResponse>('/ask', { question });
}
