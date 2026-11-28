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

const ORDER_ID_RE = /\bORD-\d{3,}\b/i;

/** Trạng thái hội thoại: tự giữ ngữ cảnh khi ca khiếu nại chưa hoàn thành (`need_info`). */
export function useChat(): UseChat {
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [latest, setLatest] = useState<ChatResponse | null>(null);
  const [busy, setBusy] = useState(false);
  const abortRef = useRef<AbortController | null>(null);
  const pendingContextRef = useRef<string>("");

  useEffect(() => () => abortRef.current?.abort(), []);

  const send = useCallback(
    async (raw: string) => {
      const text = raw.trim();
      if (!text || busy) return;
      setMessages((m) => [...m, { id: nextId(), role: "user", text }]);
      setBusy(true);
      const controller = new AbortController();
      abortRef.current = controller;

      // Nếu người dùng nhắc tới mã đơn mới (hoặc bấm ca mẫu khác), bắt đầu ngữ cảnh mới;
      // nếu ca trước vẫn đang `need_info` (chưa hoàn thành), nối tiếp thông tin bổ sung.
      const mentionsOrder = ORDER_ID_RE.test(text);
      const effectiveText =
        !mentionsOrder && pendingContextRef.current
          ? `${pendingContextRef.current}. ${text}`
          : text;

      try {
        const res = await sendChatMessage(effectiveText, controller.signal);
        setLatest(res);
        if (!res.error && res.status === "need_info") {
          pendingContextRef.current = effectiveText;
        } else if (!res.error) {
          pendingContextRef.current = "";
        }
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
    pendingContextRef.current = "";
    setMessages([]);
    setLatest(null);
    setBusy(false);
  }, []);

  return { messages, latest, busy, send, reset };
}
