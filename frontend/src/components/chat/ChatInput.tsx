import { useEffect, useRef, useState, type FormEvent, type KeyboardEvent } from "react";
import styles from "./ChatInput.module.css";

const MAX_CHARS = 2000; // khớp MAX_MESSAGE_CHARS trong codebase/app.py

interface ChatInputProps {
  disabled: boolean;
  onSend: (text: string) => void;
}

/** Ô nhập tin nhắn. Enter để gửi, Shift+Enter để xuống dòng. */
export function ChatInput({ disabled, onSend }: ChatInputProps) {
  const [value, setValue] = useState("");
  const ref = useRef<HTMLTextAreaElement>(null);

  useEffect(() => {
    if (!disabled) ref.current?.focus();
  }, [disabled]);

  const submit = (e?: FormEvent) => {
    e?.preventDefault();
    if (disabled || !value.trim()) return;
    onSend(value);
    setValue("");
  };

  const onKeyDown = (e: KeyboardEvent<HTMLTextAreaElement>) => {
    if (e.key === "Enter" && !e.shiftKey && !e.nativeEvent.isComposing) submit();
    if (e.key === "Enter" && !e.shiftKey) e.preventDefault();
  };

  return (
    <form className={styles.form} onSubmit={submit}>
      <textarea
        ref={ref}
        value={value}
        onChange={(e) => setValue(e.target.value)}
        onKeyDown={onKeyDown}
        disabled={disabled}
        maxLength={MAX_CHARS}
        placeholder="Ví dụ: Đơn ORD-1001 bị thiếu ly trà đào, mình có ảnh chụp đủ món đã nhận…"
        aria-label="Nội dung khiếu nại"
      />
      <button type="submit" disabled={disabled || !value.trim()}>
        Gửi
      </button>
    </form>
  );
}
