import type { ChatMessage } from "../../types";
import { traceLine } from "../../utils/format";
import { StatusBadge } from "../common/StatusBadge";
import styles from "./MessageBubble.module.css";

/** Một tin nhắn: của khách, của trợ lý (kèm nhãn trạng thái + dòng trace), hoặc báo lỗi. */
export function MessageBubble({ message }: { message: ChatMessage }) {
  switch (message.role) {
    case "user":
      return <div className={`${styles.bubble} ${styles.user}`}>{message.text}</div>;
    case "error":
      return (
        <div className={`${styles.bubble} ${styles.error} tone-bad`} role="alert">
          {message.text}
        </div>
      );
    case "bot": {
      const r = message.response;
      return (
        <div className={`${styles.bubble} ${styles.bot}`}>
          <StatusBadge status={r.status} />
          <p className={styles.text}>{r.output || "(answer() trả output rỗng)"}</p>
          <span className={styles.meta}>{traceLine(r.trace)}</span>
        </div>
      );
    }
  }
}
