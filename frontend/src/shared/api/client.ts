export const API_PREFIX = '/api/v1';

/** Lỗi từ API (application/problem+json) hoặc lỗi mạng. `code` ánh xạ sang `errors.*` trong vi.json. */
export class ApiError extends Error {
  readonly code: string;
  readonly status: number;

  constructor(code: string, status: number, message?: string) {
    super(message ?? code);
    this.name = 'ApiError';
    this.code = code;
    this.status = status;
  }
}

interface Problem {
  code?: string;
  title?: string;
  status?: number;
}

async function toApiError(res: Response): Promise<ApiError> {
  let code = 'unknown';
  let title: string | undefined;
  try {
    const body = (await res.json()) as Problem;
    if (typeof body.code === 'string' && body.code) code = body.code;
    title = body.title;
  } catch {
    // body không phải JSON → giữ code mặc định theo status
    if (res.status >= 500) code = 'internal_error';
  }
  return new ApiError(code, res.status, title);
}

/**
 * fetch có tiền tố /api/v1. Trả JSON đã parse (hoặc undefined với 204).
 * Ném ApiError khi HTTP lỗi; ApiError('network', 0) khi không kết nối được.
 */
export async function apiFetch<T>(path: string, init: RequestInit = {}): Promise<T> {
  let res: Response;
  try {
    res = await fetch(`${API_PREFIX}${path}`, { credentials: 'same-origin', ...init });
  } catch {
    throw new ApiError('network', 0);
  }
  if (!res.ok) throw await toApiError(res);
  if (res.status === 204) return undefined as T;
  return (await res.json()) as T;
}

export function postJson<T>(path: string, body: unknown, init: RequestInit = {}): Promise<T> {
  return apiFetch<T>(path, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', ...(init.headers ?? {}) },
    body: JSON.stringify(body),
    ...init,
  });
}
