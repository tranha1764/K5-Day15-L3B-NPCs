import styles from "./Header.module.css";

interface HeaderProps {
  onReset: () => void;
  canReset: boolean;
}

export function Header({ onReset, canReset }: HeaderProps) {
  return (
    <header className={styles.header}>
      <div className={styles.titles}>
        <h1>Trợ lý khiếu nại đơn đồ ăn</h1>
        <span>
          Bản chạy thử · Nhóm NPCs · Track D1 — mọi hoàn tiền / voucher chỉ là <b>bản nháp chờ CSKH duyệt</b>
        </span>
      </div>
      <button type="button" className={styles.reset} onClick={onReset} disabled={!canReset}>
        Làm mới
      </button>
    </header>
  );
}
