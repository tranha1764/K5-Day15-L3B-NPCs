import type { TraceSummary } from "../types";

export function formatVnd(n: number | null | undefined): string {
  return typeof n === "number" ? `${n.toLocaleString("vi-VN")}đ` : "—";
}

export function formatModels(models: string[] | undefined): string {
  return models && models.length ? models.join(", ") : "—";
}

/** Chế độ giả: model "fake", hoặc có gọi model mà token = 0 (không lấy được usage). */
export function isFakeMode(trace: TraceSummary | undefined): boolean {
  if (!trace) return false;
  return trace.models.includes("fake") || (trace.model_calls > 0 && trace.tokens_in === 0);
}

export function traceLine(t: TraceSummary): string {
  return (
    `model: ${formatModels(t.models)} · gọi model ${t.model_calls} lần · công cụ ${t.tool_calls} lần` +
    ` · token vào ${t.tokens_in} / ra ${t.tokens_out} · ${t.latency_s}s`
  );
}

let counter = 0;
export function nextId(): string {
  counter += 1;
  return `${Date.now().toString(36)}-${counter}`;
}
