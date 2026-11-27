// Hợp đồng dữ liệu giữa giao diện và server Python (codebase/app.py → POST /api/chat).
// Khớp "Đặc tả kỹ thuật chung" mục 2.2: answer(text) trả output (bắt buộc) + status, order_id, draft (tuỳ chọn).

export type ResolutionStatus = "draft_ready" | "need_info" | "escalated" | "rejected";

export type DraftAction = "refund" | "voucher" | "escalate";

export interface ResolutionDraft {
  action: DraftAction | string;
  amount_vnd?: number;
  reason?: string;
}

export interface OrderItem {
  item_id?: string;
  name: string;
  qty?: number;
  price_vnd?: number;
}

export interface Order {
  order_id: string;
  restaurant_name?: string;
  status?: string;
  delay_minutes?: number;
  payment_method?: string;
  items?: OrderItem[];
  total_vnd?: number;
  completed_at?: string;
}

export interface TraceSummary {
  models: string[];
  model_calls: number;
  tool_calls: number;
  tokens_in: number;
  tokens_out: number;
  latency_s: number;
  errors: string[];
}

export interface ChatResponse {
  output: string;
  /** null khi agent.py chưa trả khoá "status". */
  status: ResolutionStatus | string | null;
  order_id: string | null;
  draft: ResolutionDraft | null;
  /** Thẻ đơn hàng, server đọc data/orders.json để hiển thị. */
  order: Order | null;
  trace: TraceSummary;
  /** Lỗi khi chạy answer() (chưa nối model, hết lượt…); server vẫn trả 200. */
  error: string | null;
}

export type ChatMessage =
  | { id: string; role: "user"; text: string }
  | { id: string; role: "bot"; response: ChatResponse }
  | { id: string; role: "error"; text: string };

export interface QuickCase {
  label: string;
  text: string;
}
