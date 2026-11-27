import { useEffect, useRef } from "react";
import type { ChatMessage } from "../../types";
import { MessageBubble } from "./MessageBubble";
import { TypingIndicator } from "./TypingIndicator";
import styles from "./MessageList.module.css";

interface MessageListProps {
  messages: ChatMessage[];
  busy: boolean;
}

/** Vùng cuộn chứa các tin nhắn; tự cuộn xuống cuối khi có tin mới. */
export function MessageList({ messages, busy }: MessageListProps) {
  const endRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth", block: "end" });
  }, [messages.length, busy]);

  return (
    <div className={styles.list}>
      {messages.length === 0 && !busy ? (
        <p className={styles.empty}>
          Gõ khiếu nại (kèm mã đơn, ví dụ <b>ORD-1001</b>) hoặc bấm một ca demo ở trên.
          <br />
          Mỗi tin nhắn được xử lý độc lập.
        </p>
      ) : (
        messages.map((m) => <MessageBubble key={m.id} message={m} />)
      )}
      {busy && <TypingIndicator />}
      <div ref={endRef} />
    </div>
  );
}
