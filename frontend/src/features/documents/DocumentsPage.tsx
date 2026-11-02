import { useEffect, useRef, useState, type ChangeEvent } from 'react';
import { Trans, useTranslation } from 'react-i18next';
import type { DocumentItem, DocumentStatus } from '../../shared/api/documents';
import { messageForCode, messageForError } from '../../shared/api/errors';
import { formatDate } from '../../shared/i18n/format';
import { Badge, Banner, Button, EmptyState, Icon, Table, useToast } from '../../shared/ui';
import { useDocuments } from './useDocuments';
import { useUpload } from './useUpload';
import { MAX_FILES, MAX_MB, validateFiles, type RejectedFile } from './validate';

const STATUS_TONE: Record<DocumentStatus, 'queue' | 'proc' | 'ready' | 'fail'> = {
  queued: 'queue',
  processing: 'proc',
  ready: 'ready',
  failed: 'fail',
};

function StatusBadge({ status }: { status: DocumentStatus }) {
  const { t } = useTranslation();
  const icon =
    status === 'processing' ? (
      <Icon name="spinner" size={14} className="spin" />
    ) : status === 'ready' ? (
      <Icon name="check" size={14} />
    ) : status === 'failed' ? (
      <Icon name="alert" size={14} />
    ) : (
      <Icon name="clock" size={14} />
    );
  return (
    <Badge tone={STATUS_TONE[status]}>
      {icon}
      {t(`documents.status.${status}`)}
    </Badge>
  );
}

export function DocumentsPage() {
  const { t } = useTranslation();
  const { toast } = useToast();
  const docs = useDocuments();
  const upload = useUpload();
  const inputRef = useRef<HTMLInputElement>(null);

  const [tooMany, setTooMany] = useState<number | null>(null);
  const [rejected, setRejected] = useState<RejectedFile[]>([]);
  const [uploadError, setUploadError] = useState<string | null>(null);

  // Phát hiện tài liệu chuyển sang `ready` giữa hai lần poll → toast
  const prevStatus = useRef<Map<string, DocumentStatus>>(new Map());
  useEffect(() => {
    const items = docs.data?.items ?? [];
    const prev = prevStatus.current;
    if (prev.size > 0) {
      for (const d of items) {
        const before = prev.get(d.id);
        if (before && before !== 'ready' && d.status === 'ready') toast(t('documents.readyToast', { name: d.filename }));
      }
    }
    prevStatus.current = new Map(items.map((d) => [d.id, d.status]));
  }, [docs.data, t, toast]);

  const onPick = async (e: ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files ?? []);
    e.target.value = '';
    setTooMany(null);
    setUploadError(null);
    const v = validateFiles(files);
    if (v.tooMany) {
      setTooMany(files.length);
      setRejected([]);
      return;
    }
    setRejected(v.rejected);
    if (v.accepted.length === 0) return;
    try {
      const res = await upload.mutateAsync(v.accepted);
      const serverRejected = res.items.filter((i): i is { filename: string; error_code: string } => 'error_code' in i);
      const okCount = res.items.length - serverRejected.length;
      setRejected((xs) => [...xs, ...serverRejected.map((r) => ({ filename: r.filename, error_code: r.error_code as RejectedFile['error_code'] }))]);
      if (okCount > 0) toast(t('documents.uploadDone', { count: okCount }));
    } catch (err) {
      setUploadError(messageForError(err));
    }
  };

  const items: DocumentItem[] = docs.data?.items ?? [];
  const counts = docs.data?.counts;
  const limit = docs.data?.limit ?? 50;
  const used = counts?.total ?? 0;

  return (
    <div className="page">
      <div className="page-head">
        <div className="grow">
          <h1>{t('documents.title')}</h1>
          <p className="sub">
            <Trans i18nKey="documents.subtitle" components={{ b: <b /> }} />
          </p>
        </div>
        <div className="usage" aria-label={t('documents.usage', { used, limit })}>
          <span className="small">
            <b>{used}</b>/{limit}
          </span>
          <div className="meter" role="progressbar" aria-valuemin={0} aria-valuemax={limit} aria-valuenow={used}>
            <span style={{ width: `${Math.min(100, (used / limit) * 100)}%` }} />
          </div>
        </div>
      </div>

      <section className="upload-box" aria-labelledby="upload-title">
        <div className="art">
          <Icon name="upload" size={28} />
        </div>
        <div className="grow">
          <h3 id="upload-title">{t('documents.uploadTitle')}</h3>
          <p className="muted small">{t('documents.uploadHint', { maxFiles: MAX_FILES, maxMb: MAX_MB })}</p>
        </div>
        <input
          ref={inputRef}
          type="file"
          accept=".pdf,application/pdf"
          multiple
          className="sr-only"
          id="file-input"
          onChange={onPick}
          disabled={upload.isPending}
        />
        <Button variant="primary" onClick={() => inputRef.current?.click()} disabled={upload.isPending} aria-busy={upload.isPending}>
          {upload.isPending ? <Icon name="spinner" size={16} className="spin" /> : <Icon name="upload" />}
          {upload.isPending ? t('documents.uploading') : t('documents.chooseFiles')}
        </Button>
      </section>

      <div className="stack" style={{ marginTop: 12 }} aria-live="polite">
        {tooMany !== null && (
          <Banner tone="danger" role="alert" onClose={() => setTooMany(null)} closeLabel={t('common.close')}>
            {t('documents.tooManyFiles', { maxFiles: MAX_FILES, count: tooMany })}
          </Banner>
        )}
        {uploadError && (
          <Banner tone="danger" role="alert" onClose={() => setUploadError(null)} closeLabel={t('common.close')}>
            {uploadError}
          </Banner>
        )}
        {rejected.length > 0 && (
          <div className="rejects">
            <p className="small muted">{t('documents.rejected')}</p>
            {rejected.map((r, i) => (
              <div key={`${r.filename}-${i}`} className="reject">
                <Icon name="alert" size={16} className="muted" />
                <span className="file-name grow">{r.filename}</span>
                <span className="err-detail">{messageForCode(r.error_code)}</span>
              </div>
            ))}
            <div>
              <Button size="sm" variant="ghost" onClick={() => setRejected([])}>
                {t('common.close')}
              </Button>
            </div>
          </div>
        )}
      </div>

      <section className="card" style={{ marginTop: 24 }}>
        <div className="toolbar">
          <span className="small muted">{counts ? t('documents.usage', { used, limit }) : docs.isLoading ? t('common.loading') : ''}</span>
          <div className="grow" />
          {(counts?.processing ?? 0) > 0 && (
            <span className="poll">
              <Icon name="refresh" size={14} /> {t('documents.autoRefresh')}
            </span>
          )}
        </div>

        {docs.isError && (
          <div style={{ padding: 16 }}>
            <Banner tone="danger" role="alert">
              {t('documents.loadError')}{' '}
              <Button size="sm" onClick={() => docs.refetch()}>
                {t('common.retry')}
              </Button>
            </Banner>
          </div>
        )}

        {!docs.isError && items.length === 0 && !docs.isLoading && (
          <EmptyState icon="file" title={t('documents.emptyTitle')} body={t('documents.emptyBody')} />
        )}

        {items.length > 0 && (
          <Table
            head={
              <tr>
                <th scope="col">{t('documents.columns.filename')}</th>
                <th scope="col" className="hide-sm">
                  {t('documents.columns.docNumber')}
                </th>
                <th scope="col" className="hide-sm">
                  {t('documents.columns.effectiveDate')}
                </th>
                <th scope="col" className="num hide-sm">
                  {t('documents.columns.pages')}
                </th>
                <th scope="col" className="hide-sm">
                  {t('documents.columns.uploadedAt')}
                </th>
                <th scope="col">{t('documents.columns.status')}</th>
              </tr>
            }
          >
            {items.map((d) => (
              <tr key={d.id}>
                <td>
                  <div className="file-cell">
                    <span className="file-ic">
                      <Icon name="file" size={18} />
                    </span>
                    <div>
                      <div className="file-name">{d.title ?? d.filename}</div>
                      {d.title && <div className="small muted">{d.filename}</div>}
                      {d.status === 'failed' && <div className="err-detail">{messageForCode(d.error_code)}</div>}
                    </div>
                  </div>
                </td>
                <td className="hide-sm">{d.doc_number ?? '—'}</td>
                <td className="hide-sm">{d.effective_date ? formatDate(d.effective_date) : '—'}</td>
                <td className="num hide-sm">{d.pages ?? '—'}</td>
                <td className="hide-sm">{formatDate(d.uploaded_at)}</td>
                <td>
                  <StatusBadge status={d.status} />
                </td>
              </tr>
            ))}
          </Table>
        )}
      </section>
    </div>
  );
}
