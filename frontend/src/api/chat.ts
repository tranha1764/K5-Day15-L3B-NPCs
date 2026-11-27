import type { ChatResponse } from "../types";

/** Gọi POST /api/chat. Lỗi HTTP (400, 500…) hoặc mất kết nối → throw Error có thông điệp tiếng Việt. */
export async function sendChatMessage(message: string, signal?: AbortSignal): Promise<ChatResponse> {
  let res: Response;
  try {
    res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
      signal,
    });
  } catch (e) {
    if ((e as Error).name === "AbortError") throw e;
    throw new Error("Không kết nối được server — `python run.py` còn chạy không?");
  }

  let data: unknown;
  try {
    data = await res.json();
  } catch {
    throw new Error(`Server trả dữ liệu không phải JSON (HTTP ${res.status}).`);
  }
  if (!res.ok) {
    const msg = (data as { error?: string })?.error;
    throw new Error(msg || `HTTP ${res.status}`);
  }
  return data as ChatResponse;
}
