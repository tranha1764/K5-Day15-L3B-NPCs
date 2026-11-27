import type { ReactNode } from "react";
import styles from "./KeyValueList.module.css";

export interface KeyValueRow {
  label: string;
  value: ReactNode;
}

/** Danh sách nhãn – giá trị hai cột (dùng cho đơn hàng, bản nháp, trace). */
export function KeyValueList({ rows }: { rows: KeyValueRow[] }) {
  return (
    <dl className={styles.list}>
      {rows.map((r) => (
        <div className={styles.row} key={r.label}>
          <dt>{r.label}</dt>
          <dd>{r.value}</dd>
        </div>
      ))}
    </dl>
  );
}
