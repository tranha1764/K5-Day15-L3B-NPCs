import styles from "./TypingIndicator.module.css";

export function TypingIndicator() {
  return (
    <div className={styles.typing} aria-live="polite">
      <span className={styles.dots} aria-hidden="true">
        <i />
        <i />
        <i />
      </span>
      Đang tra đơn và chính sách…
    </div>
  );
}
