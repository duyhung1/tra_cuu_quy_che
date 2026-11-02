import { useCallback, useState } from 'react';
import { ask, type Source } from '../../shared/api/ask';
import { ApiError } from '../../shared/api/client';

export type Turn =
  | { id: number; question: string; state: 'pending' }
  | { id: number; question: string; state: 'done'; answer: string; latencyMs: number; sources: Source[] }
  | { id: number; question: string; state: 'error'; code: string };

/** Lịch sử hỏi–đáp chỉ nằm trong bộ nhớ trang (mất khi tải lại). */
export function useAsk() {
  const [turns, setTurns] = useState<Turn[]>([]);
  const [busy, setBusy] = useState(false);

  const run = useCallback(async (id: number, question: string) => {
    setBusy(true);
    try {
      const res = await ask(question);
      setTurns((xs) => xs.map((t) => (t.id === id ? { id, question, state: 'done', answer: res.answer, latencyMs: res.latency_ms, sources: res.sources ?? [] } : t)));
    } catch (err) {
      const code = err instanceof ApiError ? err.code : 'unknown';
      setTurns((xs) => xs.map((t) => (t.id === id ? { id, question, state: 'error', code } : t)));
    } finally {
      setBusy(false);
    }
  }, []);

  const submit = useCallback(
    (question: string) => {
      const id = Date.now();
      setTurns((xs) => [...xs, { id, question, state: 'pending' }]);
      void run(id, question);
    },
    [run],
  );

  /** Hỏi lại cùng câu hỏi của lượt bị lỗi (thay thế tại chỗ). */
  const retry = useCallback(
    (id: number) => {
      const turn = turns.find((t) => t.id === id);
      if (!turn) return;
      setTurns((xs) => xs.map((t) => (t.id === id ? { id, question: turn.question, state: 'pending' } : t)));
      void run(id, turn.question);
    },
    [run, turns],
  );

  return { turns, busy, submit, retry };
}
