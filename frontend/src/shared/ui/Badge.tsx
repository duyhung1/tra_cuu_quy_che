import type { ReactNode } from 'react';

type Tone = 'ready' | 'proc' | 'queue' | 'fail' | 'neutral';

const TONE: Record<Tone, string> = {
  ready: 'b-ready',
  proc: 'b-proc',
  queue: 'b-queue',
  fail: 'b-fail',
  neutral: 'b-neutral',
};

export function Badge({ tone, children }: { tone: Tone; children: ReactNode }) {
  return <span className={`badge ${TONE[tone]}`}>{children}</span>;
}
