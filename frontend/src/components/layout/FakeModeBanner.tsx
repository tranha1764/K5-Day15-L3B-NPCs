import styles from "./FakeModeBanner.module.css";

/** Hiện khi lượt gần nhất chạy model giả — để lúc quay video CP3 thấy ngay đã gọi AI thật hay chưa. */
export function FakeModeBanner({ visible }: { visible: boolean }) {
  if (!visible) return null;
  return (
    <div className={`${styles.banner} tone-warn`} role="status">
      ⚠️ Đang chạy <b>chế độ giả</b> (model "fake", token 0) — chưa gọi model thật. Nối model:{" "}
      <code>docs/connect-model.md</code>.
    </div>
  );
}
