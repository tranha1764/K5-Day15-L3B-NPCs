export type Tone = "ok" | "warn" | "bad" | "neutral";

export interface StatusInfo {
  tone: Tone;
  title: string;
  hint: string;
}

const STATUS_INFO: Record<string, StatusInfo> = {
  draft_ready: {
    tone: "ok",
    title: "Đã tạo bản nháp chờ CSKH duyệt",
    hint: "Tiền / voucher CHƯA được chuyển — nhân viên duyệt mới thực hiện.",
  },
  need_info: {
    tone: "warn",
    title: "Cần bổ sung thông tin / ảnh",
    hint: "Khách bổ sung mã đơn, món bị lỗi hoặc ảnh thực tế rồi gửi lại.",
  },
  escalated: {
    tone: "bad",
    title: "Chuyển CSKH cấp cao",
    hint: "Ca vượt ngưỡng hoặc có rủi ro — người xử lý trực tiếp.",
  },
  rejected: {
    tone: "bad",
    title: "Từ chối theo chính sách",
    hint: "Không đủ điều kiện theo chính sách đã tra.",
  },
};

/** Trạng thái lạ hoặc thiếu (agent.py chưa trả "status") → thẻ xám, không vỡ giao diện. */
export function getStatusInfo(status: string | null | undefined): StatusInfo {
  if (status && STATUS_INFO[status]) return STATUS_INFO[status];
  return {
    tone: "neutral",
    title: status ? `Trạng thái: ${status}` : "Chưa có trạng thái",
    hint: status ? "Trạng thái chưa có trong danh sách hiển thị." : 'answer() chưa trả khoá "status".',
  };
}

export const ACTION_LABEL: Record<string, string> = {
  refund: "Hoàn tiền",
  voucher: "Voucher",
  escalate: "Chuyển CSKH",
};
