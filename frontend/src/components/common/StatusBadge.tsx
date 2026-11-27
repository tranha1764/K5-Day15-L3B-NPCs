import { getStatusInfo } from "../../constants/status";
import styles from "./StatusBadge.module.css";

/** Nhãn tròn màu theo trạng thái xử lý: xanh / vàng / đỏ / xám. */
export function StatusBadge({ status }: { status: string | null | undefined }) {
  const info = getStatusInfo(status);
  return <span className={`${styles.badge} tone-${info.tone}`}>{info.title}</span>;
}
