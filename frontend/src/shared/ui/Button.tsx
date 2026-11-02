import type { ButtonHTMLAttributes } from 'react';

type Variant = 'default' | 'primary' | 'ghost';

interface Props extends ButtonHTMLAttributes<HTMLButtonElement> {
  variant?: Variant;
  size?: 'md' | 'sm';
  icon?: boolean;
}

const VARIANT: Record<Variant, string> = { default: '', primary: 'btn-primary', ghost: 'btn-ghost' };

export function Button({ variant = 'default', size = 'md', icon = false, className = '', type = 'button', ...rest }: Props) {
  const cls = ['btn', VARIANT[variant], size === 'sm' ? 'btn-sm' : '', icon ? 'btn-icon' : '', className]
    .filter(Boolean)
    .join(' ');
  return <button type={type} className={cls} {...rest} />;
}
