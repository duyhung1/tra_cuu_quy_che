import type { ReactNode, TableHTMLAttributes } from 'react';

interface Props extends TableHTMLAttributes<HTMLTableElement> {
  head: ReactNode;
  children: ReactNode;
}

export function Table({ head, children, ...rest }: Props) {
  return (
    <div className="table-wrap">
      <table className="tbl" {...rest}>
        <thead>{head}</thead>
        <tbody>{children}</tbody>
      </table>
    </div>
  );
}
