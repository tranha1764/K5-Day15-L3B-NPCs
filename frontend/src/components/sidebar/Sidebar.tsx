import type { ChatResponse } from "../../types";
import { OrderCard } from "./OrderCard";
import { StatusCard } from "./StatusCard";
import { TraceCard } from "./TraceCard";
import styles from "./Sidebar.module.css";

/** Cột phải: trạng thái xử lý → đơn hàng → trace, đều theo phản hồi gần nhất. */
export function Sidebar({ latest }: { latest: ChatResponse | null }) {
  return (
    <aside className={styles.sidebar}>
      <StatusCard response={latest} />
      <OrderCard response={latest} />
      <TraceCard trace={latest?.trace ?? null} />
    </aside>
  );
}
