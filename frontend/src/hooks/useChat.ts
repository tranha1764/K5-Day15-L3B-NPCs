import { useCallback, useEffect, useRef, useState } from "react";
import { sendChatMessage } from "../api/chat";
import type { ChatMessage, ChatResponse } from "../types";
import { nextId } from "../utils/format";

export interface UseChat {
  messages: ChatMessage[];
  /** Phản hồi gần nhất từ server (kể cả khi answer() lỗi) — sidebar hiển thị theo cái này. */
  latest: ChatResponse | null;
  busy: boolean;
  send: (text: string) => Promise<void>;
  reset: () => void;
}

/** Trạng thái hội thoại. Mỗi tin nhắn được xử lý độc lập — answer(text) không nhớ lượt trước. */
export function useChat(): UseChat {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [latest, setLatest] = useState<ChatResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const abortRef = useRef<AbortController | null>(null);

  useEffect(() => () => abortRef.current?.abort(), []);

  const send = useCallback(
    async (raw: string) => {
      const text = raw.trim();
      if (!text || busy) return;
      setMessages((m) => [...m, { id: nextId(), role: "user", text }]);
      setBusy(true);
      const controller = new AbortController();
      abortRef.current = controller;
      try {
        const res = await sendChatMessage(text, controller.signal);
        setLatest(res);
        setMessages((m) => [
          ...m,
          res.error
            ? { id: nextId(), role: "error", text: `Lỗi khi chạy answer(): ${res.error}` }
            : { id: nextId(), role: "bot", response: res },
        ]);
      } catch (e) {
        if ((e as Error).name === "AbortError") return;
        setMessages((m) => [...m, { id: nextId(), role: "error", text: (e as Error).message }]);
      } finally {
        if (abortRef.current === controller) abortRef.current = null;
        setBusy(false);
      }
    },
    [busy],
  );

  const reset = useCallback(() => {
    abortRef.current?.abort();
    setMessages([]);
    setLatest(null);
    setBusy(false);
  }, []);

  return { messages, latest, busy, send, reset };
}
