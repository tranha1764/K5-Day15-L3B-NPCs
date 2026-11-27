import type { ReactNode } from "react";
import type { ChatMessage } from "../../types";
import { traceLine } from "../../utils/format";
import { StatusBadge } from "../common/StatusBadge";
import styles from "./MessageBubble.module.css";

// Hỗ trợ URL có cặp ngoặc đơn lồng (vd link bài viết ShopeeFood kết thúc bằng -(%C4%91ang-giao)).
const MD_LINK_RE = /\[([^\]]+)\]\((https?:\/\/(?:[^\s()]+|\([^\s()]*\))+)\)/g;

/** Chuyển cú pháp [nhãn](https://...) trong output thành thẻ <a> an toàn, giữ nguyên văn bản còn lại. */
function renderFormattedText(text: string): ReactNode[] {
  const nodes: ReactNode[] = [];
  let lastIndex = 0;
  for (const match of text.matchAll(MD_LINK_RE)) {
    const idx = match.index ?? 0;
    if (idx > lastIndex) {
      nodes.push(text.slice(lastIndex, idx));
    }
    const [, label, url] = match;
    nodes.push(
      <a
        key={`${idx}-${url}`}
        className={styles.link}
        href={url}
        target="_blank"
        rel="noopener noreferrer"
      >
        {label}
      </a>
    );
    lastIndex = idx + match[0].length;
  }
  if (lastIndex < text.length) {
    nodes.push(text.slice(lastIndex));
  }
  return nodes;
}

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
          <p className={styles.text}>
            {r.output ? renderFormattedText(r.output) : "(answer() trả output rỗng)"}
          </p>
          <span className={styles.meta}>{traceLine(r.trace)}</span>
        </div>
      );
    }
  }
}
