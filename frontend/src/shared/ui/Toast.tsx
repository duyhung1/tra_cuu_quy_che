import { createContext, useCallback, useContext, useMemo, useState, type ReactNode } from 'react';
import { useTranslation } from 'react-i18next';
import { Icon } from './Icon';

interface ToastItem {
  id: number;
  message: string;
  kind: 'info' | 'error';
}

interface ToastApi {
  toast: (message: string, kind?: ToastItem['kind']) => void;
}

const ToastCtx = createContext<ToastApi>({ toast: () => undefined });

export function useToast() {
  return useContext(ToastCtx);
}

export function ToastProvider({ children }: { children: ReactNode }) {
  const { t } = useTranslation();
  const [items, setItems] = useState<ToastItem[]>([]);

  const remove = useCallback((id: number) => setItems((xs) => xs.filter((x) => x.id !== id)), []);

  const toast = useCallback(
    (message: string, kind: ToastItem['kind'] = 'info') => {
      const id = Date.now() + Math.random();
      setItems((xs) => [...xs, { id, message, kind }]);
      if (kind !== 'error') window.setTimeout(() => remove(id), 5000);
    },
    [remove],
  );

  const api = useMemo(() => ({ toast }), [toast]);

  return (
    <ToastCtx.Provider value={api}>
      {children}
      <div className="toasts" role="status" aria-live="polite">
        {items.map((x) => (
          <div key={x.id} className={`toast ${x.kind === 'error' ? 'err' : ''}`.trim()}>
            <span>{x.message}</span>
            <button type="button" aria-label={t('common.close')} onClick={() => remove(x.id)}>
              <Icon name="x" size={16} />
            </button>
          </div>
        ))}
      </div>
    </ToastCtx.Provider>
  );
}
