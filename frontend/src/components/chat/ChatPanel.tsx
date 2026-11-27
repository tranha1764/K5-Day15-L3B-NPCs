import { QUICK_CASES } from "../../constants/quickCases";
import type { ChatMessage } from "../../types";
import { ChatInput } from "./ChatInput";
import { MessageList } from "./MessageList";
import { QuickCaseBar } from "./QuickCaseBar";
import styles from "./ChatPanel.module.css";

interface ChatPanelProps {
  messages: ChatMessage[];
  busy: boolean;
  onSend: (text: string) => void;
}

/** Cột trái: ca demo nhanh → danh sách tin nhắn → ô nhập. */
export function ChatPanel({ messages, busy, onSend }: ChatPanelProps) {
  return (
    <section className={styles.panel}>
      <QuickCaseBar cases={QUICK_CASES} disabled={busy} onPick={onSend} />
      <MessageList messages={messages} busy={busy} />
      <ChatInput disabled={busy} onSend={onSend} />
    </section>
  );
}
