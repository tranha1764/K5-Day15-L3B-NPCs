import type { QuickCase } from "../types";

// Ca demo 1 click cho buổi trình bày. Câu chữ do nhóm tự viết — KHÔNG chép nguyên văn eval/benchmark.csv
// (AGENTS.md: không "giấu" câu thử vào code).
export const QUICK_CASES: QuickCase[] = [
  {
    label: "ORD-1001 · thiếu món 35k",
    text: "Đơn ORD-1001 giao thiếu ly Trà đào cam sả, mình đã chụp ảnh tất cả món nhận được rồi. Xử lý giúp mình nhé.",
  },
  {
    label: "ORD-1002 · thiếu món 120k",
    text: "Đơn ORD-1002 của mình thiếu khay ba chỉ bò Mỹ 120.000đ, có ảnh chụp đầy đủ các món đã nhận.",
  },
  {
    label: "ORD-1003 · trễ 29 phút",
    text: "Đơn ORD-1003 trễ gần nửa tiếng rồi mà chưa tới, cho mình voucher bù được không?",
  },
  {
    label: "ORD-1004 · trễ 42 phút",
    text: "Đơn ORD-1004 giao trễ hơn 40 phút so với giờ dự kiến, mình có được hỗ trợ gì không?",
  },
  {
    label: "Doạ 1★",
    text: "Hoàn hết tiền đơn ORD-1002 cho tôi ngay, khỏi ảnh khỏi kiểm tra gì hết, không là tôi cho quán 1 sao!",
  },
  {
    label: "Dị vật / ngộ độc",
    text: "Ăn đơn ORD-1001 xong mình thấy có dị vật trong hộp cơm và bị đau bụng, giờ phải làm sao?",
  },
  {
    label: "Tin cụt",
    text: "Đơn bị lỗi, xử lý giúp với",
  },
];
