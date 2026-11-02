import { useEffect, useRef, useState, type FormEvent, type KeyboardEvent } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import type { Source } from '../../shared/api/ask';
import { messageForCode } from '../../shared/api/errors';
import { formatDate } from '../../shared/i18n/format';
import { Banner, Button, EmptyState, Icon } from '../../shared/ui';
import { useDocuments } from '../documents/useDocuments';
import { renderMarkdown } from './markdown';
import { useAsk, type Turn } from './useAsk';
import { checkQuestion, MAX_QUESTION_CHARS } from './validate';

/** Danh sách căn cứ: [n] Điều X — Tên văn bản (Số …, hiệu lực …), trang Y. */
function Sources({ sources }: { sources: Source[] }) {
  const { t } = useTranslation();
  if (sources.length === 0) return null;
  return (
    <section className="sources" aria-label={t('ask.sourcesTitle')}>
      <h3 className="sources-title">{t('ask.sourcesTitle')}</h3>
      <ol>
        {sources.map((s) => (
          <li key={s.ref}>
            <span className="ref">[{s.ref}]</span>
            <div>
              <div className="src-main">
                {s.article ? <b>{s.article}</b> : null}
                {s.article ? ' — ' : null}
                {s.doc_title ?? s.filename}
              </div>
              <div className="small muted">
                {[
                  s.doc_number ? t('ask.sourceNumber', { number: s.doc_number }) : null,
                  s.effective_date ? t('ask.sourceEffective', { date: formatDate(s.effective_date) }) : null,
                  t('ask.sourcePage', { page: s.page }),
                  s.doc_title ? s.filename : null,
                ]
                  .filter(Boolean)
                  .join(' · ')}
              </div>
            </div>
          </li>
        ))}
      </ol>
    </section>
  );
}

function AiTurn({ turn, onRetry }: { turn: Turn; onRetry: (id: number) => void }) {
  const { t } = useTranslation();
  return (
    <article className="msg-ai" aria-label={t('ask.ai')}>
      <span className="avatar ai">{t('ask.ai')}</span>
      <div className={`body ${turn.state === 'error' ? 'error' : ''}`.trim()}>
        {turn.state === 'pending' && (
          <div className="thinking" role="status" aria-live="polite">
            <Icon name="spinner" size={18} className="spin" />
            <div>
              <div>{t('ask.thinking')}</div>
              <div className="sub">{t('ask.thinkingSub')}</div>
            </div>
          </div>
        )}
        {turn.state === 'done' && (
          <>
            <div className="answer" dangerouslySetInnerHTML={{ __html: renderMarkdown(turn.answer) }} />
            <Sources sources={turn.sources} />
            <div className="ai-foot">
              <Icon name="sparkle" size={14} />
              <span>{t('ask.aiLabel')}</span>
              <span className="grow" />
              <span>{t('ask.latency', { seconds: (turn.latencyMs / 1000).toFixed(1).replace('.', ',') })}</span>
            </div>
          </>
        )}
        {turn.state === 'error' && (
          <>
            <div className="row" style={{ alignItems: 'flex-start' }}>
              <Icon name="alert" size={18} className="muted" />
              <div>
                <b>{turn.code === 'ai_unavailable' || turn.code === 'network' || turn.code === 'unknown' || turn.code === 'internal_error' ? t('ask.errorTitle') : messageForCode(turn.code)}</b>
                <p className="small muted">{t('ask.errorSub')}</p>
              </div>
            </div>
            <div className="row" style={{ marginTop: 10 }}>
              <Button size="sm" onClick={() => onRetry(turn.id)}>
                <Icon name="refresh" size={14} /> {t('ask.askAgain')}
              </Button>
            </div>
          </>
        )}
      </div>
    </article>
  );
}

export function AskPage() {
  const { t } = useTranslation();
  const { data } = useDocuments();
  const { turns, busy, submit, retry } = useAsk();
  const [draft, setDraft] = useState('');
  const threadRef = useRef<HTMLDivElement>(null);
  const textRef = useRef<HTMLTextAreaElement>(null);

  const ready = data?.counts.ready ?? 0;
  const processing = data?.counts.processing ?? 0;
  const locked = data !== undefined && ready === 0;
  const check = checkQuestion(draft);
  const canSend = check.valid && !busy && !locked;

  // Tự cuộn xuống khi có lượt mới
  useEffect(() => {
    const el = threadRef.current;
    if (el) el.scrollTop = el.scrollHeight;
  }, [turns]);

  // Textarea tự giãn
  useEffect(() => {
    const el = textRef.current;
    if (!el) return;
    el.style.height = 'auto';
    el.style.height = `${Math.min(el.scrollHeight, 200)}px`;
  }, [draft]);

  const onSubmit = (e?: FormEvent) => {
    e?.preventDefault();
    if (!canSend) return;
    submit(check.trimmed);
    setDraft('');
  };

  const onKey = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      onSubmit();
    }
  };

  return (
    <div className="chat-col">
      <header className="chat-head">
        <h1 className="grow">{t('ask.title')}</h1>
        <Link className="src-pill" to="/documents">
          <Icon name="file" size={14} /> <span>{t('ask.sources', { count: ready })}</span>
        </Link>
      </header>

      <div className="thread" ref={threadRef} aria-busy={busy}>
        <div className="thread-inner">
          {locked && (
            <EmptyState
              icon="file"
              title={t('ask.lockedTitle')}
              body={t('ask.lockedBody')}
              action={
                <Link className="btn btn-primary" to="/documents">
                  <Icon name="upload" /> {t('ask.lockedCta')}
                </Link>
              }
            />
          )}
          {!locked && turns.length === 0 && (
            <div className="welcome">
              <div className="empty-art" style={{ margin: '0 auto' }}>
                <Icon name="sparkle" size={32} />
              </div>
              <h2 style={{ marginTop: 16 }}>{t('ask.welcomeTitle')}</h2>
              <p className="lead">{t('ask.welcomeBody')}</p>
            </div>
          )}
          {turns.map((turn) => (
            <div key={turn.id} className="stack" style={{ gap: 24 }}>
              <div className="msg-user" aria-label={t('ask.you')}>
                {turn.question}
              </div>
              <AiTurn turn={turn} onRetry={retry} />
            </div>
          ))}
        </div>
      </div>

      <div className="composer-wrap">
        {processing > 0 && (
          <div className="notice">
            <Banner tone="info" className="small">
              {t('ask.processingNotice', { count: processing })}
            </Banner>
          </div>
        )}
        <form className={`composer ${locked ? 'disabled' : ''}`.trim()} onSubmit={onSubmit}>
          <label htmlFor="question" className="sr-only">
            {t('ask.title')}
          </label>
          <textarea
            id="question"
            ref={textRef}
            rows={1}
            value={draft}
            onChange={(e) => setDraft(e.target.value)}
            onKeyDown={onKey}
            placeholder={locked ? t('ask.placeholderLocked') : t('ask.placeholder')}
            disabled={locked}
            aria-describedby="question-meta"
            aria-invalid={check.over > 0}
          />
          <Button variant="primary" icon type="submit" aria-label={t('ask.send')} disabled={!canSend}>
            {busy ? <Icon name="spinner" size={18} className="spin" /> : <Icon name="send" />}
          </Button>
        </form>
        <div className="composer-meta" id="question-meta">
          <span className="grow">{t('ask.hint')}</span>
          <span className={check.over > 0 ? 'over' : ''} title={check.over > 0 ? t('ask.tooLong', { over: check.over }) : undefined}>
            {t('ask.counter', { count: check.length, max: MAX_QUESTION_CHARS })}
          </span>
        </div>
      </div>
    </div>
  );
}
