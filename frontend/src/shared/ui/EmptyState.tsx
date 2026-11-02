import type { ReactNode } from 'react';
import { Icon } from './Icon';

interface Props {
  icon: string;
  title: string;
  body?: ReactNode;
  action?: ReactNode;
}

export function EmptyState({ icon, title, body, action }: Props) {
  return (
    <div className="empty">
      <div className="empty-art">
        <Icon name={icon} size={28} />
      </div>
      <h3>{title}</h3>
      {body && <p>{body}</p>}
      {action}
    </div>
  );
}
