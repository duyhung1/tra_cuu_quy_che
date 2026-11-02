import type { ReactNode } from 'react';
import { Icon } from './Icon';

type Tone = 'info' | 'warn' | 'danger';
const ICON: Record<Tone, string> = { info: 'info', warn: 'alert', danger: 'alert' };

interface Props {
  tone: Tone;
  children: ReactNode;
  role?: 'alert' | 'status';
  className?: string;
  onClose?: () => void;
  closeLabel?: string;
}

export function Banner({ tone, children, role = 'status', className = '', onClose, closeLabel }: Props) {
  return (
    <div className={`banner banner-${tone} ${className}`.trim()} role={role}>
      <Icon name={ICON[tone]} />
      <div className="banner-body">{children}</div>
      {onClose && (
        <button type="button" className="btn btn-ghost btn-sm btn-icon" aria-label={closeLabel} onClick={onClose}>
          <Icon name="x" size={16} />
        </button>
      )}
    </div>
  );
}
