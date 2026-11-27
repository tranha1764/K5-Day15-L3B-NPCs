import type { QuickCase } from "../../types";
import styles from "./QuickCaseBar.module.css";

interface QuickCaseBarProps {
  cases: QuickCase[];
  disabled: boolean;
  onPick: (text: string) => void;
}

/** Hàng nút "ca demo nhanh" — bấm một lần là gửi luôn. */
export function QuickCaseBar({ cases, disabled, onPick }: QuickCaseBarProps) {
  return (
    <div className={styles.bar}>
      <b>Ca demo nhanh:</b>
      {cases.map((c) => (
        <button key={c.label} type="button" title={c.text} disabled={disabled} onClick={() => onPick(c.text)}>
          {c.label}
        </button>
      ))}
    </div>
  );
}
