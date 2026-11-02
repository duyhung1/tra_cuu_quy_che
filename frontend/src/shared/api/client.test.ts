import { afterEach, describe, expect, it, vi } from 'vitest';
import { ApiError, apiFetch } from './client';
import { messageForError } from './errors';

function mockFetch(res: Partial<Response> & { json?: () => Promise<unknown> }) {
  vi.stubGlobal('fetch', vi.fn().mockResolvedValue(res));
}

afterEach(() => vi.unstubAllGlobals());

async function capture(p: Promise<unknown>): Promise<ApiError> {
  try {
    await p;
  } catch (e) {
    return e as ApiError;
  }
  throw new Error('expected rejection');
}

describe('apiFetch', () => {
  it('gắn tiền tố /api/v1 và trả JSON khi thành công', async () => {
    mockFetch({ ok: true, status: 200, json: async () => ({ a: 1 }) });
    const data = await apiFetch<{ a: number }>('/documents');
    expect(data).toEqual({ a: 1 });
    expect(fetch).toHaveBeenCalledWith('/api/v1/documents', expect.objectContaining({ credentials: 'same-origin' }));
  });

  it('ném ApiError với code từ problem+json', async () => {
    mockFetch({ ok: false, status: 409, json: async () => ({ code: 'no_documents', title: 'Conflict', status: 409 }) });
    const err = await capture(apiFetch('/ask'));
    expect(err).toBeInstanceOf(ApiError);
    expect(err.code).toBe('no_documents');
    expect(err.status).toBe(409);
    expect(messageForError(err)).toBe('Chưa có văn bản nào Sẵn sàng để trả lời.');
  });

  it('body không phải JSON và status 5xx → internal_error', async () => {
    mockFetch({ ok: false, status: 502, json: async () => { throw new Error('bad json'); } });
    const err = await capture(apiFetch('/ask'));
    expect(err.code).toBe('internal_error');
  });

  it('lỗi mạng → ApiError network, thông điệp tiếng Việt', async () => {
    vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new TypeError('Failed to fetch')));
    const err = await capture(apiFetch('/documents'));
    expect(err.code).toBe('network');
    expect(messageForError(err)).toMatch(/Mất kết nối/);
  });

  it('mã lỗi lạ → thông điệp chung', async () => {
    mockFetch({ ok: false, status: 400, json: async () => ({ code: 'something_new' }) });
    const err = await capture(apiFetch('/documents'));
    expect(messageForError(err)).toBe('Đã xảy ra lỗi. Vui lòng thử lại.');
  });
});
