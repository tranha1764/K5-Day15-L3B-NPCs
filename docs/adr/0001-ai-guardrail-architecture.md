# ADR 0001: Kiến trúc 1-call LLM + Guardrail cứng bằng code cho xử lý khiếu nại D1

- **Ngày:** 27/11/2026 *(cập nhật v2: 28/11/2026 sau `eval/run-2.csv` 24/24)*
- **Trạng thái:** Accepted
- **Phạm vi:** `codebase/ai.py`, `codebase/tools.py`, `codebase/agent.py` (Task `AI-01` & `AI-02`)

## 1. Bối cảnh (Context)

Hệ thống xử lý khiếu nại đơn giao đồ ăn (Track D · D1) phải đồng thời đáp ứng 3 yêu cầu xung đột:
1. **An toàn tuyệt đối ở các ca biên (100%):** Không bao giờ tự duyệt hoàn tiền/voucher khi vượt 100.000đ, quá hạn 12h (`76251`), thiếu ảnh, giao trễ < 30 phút (`71069`), tần suất khiếu nại > 3 lần/tháng, đòi món không có trong đơn, đe dọa 1★ bỏ qua quy trình, hoặc nghi dị vật/ngộ độc.
2. **Tiết kiệm token và độ trễ:** Phải chạy mượt bộ 20–30 câu `eval` và ≥ 50 phiên `simulate` trên gói API giới hạn lượt gọi, đồng thời giữ chi phí/task thành công thấp cho bài toán `COST-01`.
3. **Tính tái lập của mốc thời gian 12 tiếng:** Các đơn mẫu `ORD-1001..ORD-1005` trong `data/orders.json` có `completed_at` vào trưa 27/11/2026; nếu so với `datetime.now()` vào ngày 28/11 (CP3/CP4), toàn bộ đơn hợp lệ sẽ bị tính nhầm là quá hạn 12h.

## 2. Quyết định (Decision)

### 2.1. Workflow cố định: Code tra cứu & khóa quyết định → 1 lần gọi LLM sinh câu trả lời
Thay vì dùng vòng lặp agent tự do hoặc gọi 2 lần LLM (Extract + Generate), `answer(text)` thực thi luồng cố định 3 bước:
1. **Tra cứu deterministic qua `@tool`:** Trích `order_id` bằng regex, gọi `lookup_order`, `lookup_user_history`, `lookup_policy`.
2. **Động cơ Guardrail bằng code Python:** Đánh giá theo thứ tự ưu tiên cứng để quyết định `status` và (nếu phù hợp) gọi `create_resolution_draft`. Ghi quyết định vào `tracing.note()`.
3. **1 lần gọi `call_model(SYSTEM, prompt)`:** Truyền toàn bộ căn cứ (đơn hàng, lịch sử, chính sách) và **quyết định đã khóa** để LLM diễn đạt câu trả lời tiếng Việt tự nhiên, lịch sự, không thể lật ngược quyết định của code.

### 2.2. Bảng State Machine chuẩn (khớp FE `frontend/src/types.ts`)

| Ưu tiên | Điều kiện kích hoạt | `status` | `draft` (`create_resolution_draft`) |
|---|---|---|---|
| 1 | Dị vật / ngộ độc thực phẩm | `escalated` | `action="escalate"`, `amount_vnd=0` |
| 2 | Đe dọa 1★ / ép bỏ qua quy trình ảnh | `escalated` | `action="escalate"`, `amount_vnd=0` |
| 2b | *(v2)* Tấn công trích xuất dữ liệu khách hàng khác (`DATA_EXFIL_TERMS`) | `rejected` | `None` |
| 2c | *(v2)* Prompt injection / giả mạo admin đòi bỏ qua hạn mức (`PROMPT_INJECTION_TERMS`) | `rejected` | `None` |
| 3 | Hỏi thông tin SLA hoặc kênh hoàn tiền thuần túy (`policy 71298`) | `None` | `None` |
| 4a | *(v2)* Thiếu `order_id` + khiếu nại khác biệt thẩm mỹ / hình quảng cáo (`AESTHETIC_COMPLAINT_TERMS`) | `rejected` | `None` |
| 4 | Thiếu `order_id` hoặc không tìm thấy đơn | `need_info` | `None` |
| 5 | Quá hạn 12h (`policy 76251`) cho khiếu nại thiếu/sai món | `rejected` | `None` |
| 6 | Khiếu nại món không có trong `order.items` | `rejected` | `None` |
| 7 | Thiếu/sai món nhưng chưa có ảnh toàn bộ món nhận được | `need_info` | `None` |
| 8 | Giao trễ < 30 phút | `rejected` | `None` |
| 9 | Lịch sử khiếu nại > 3 lần/tháng (`history.json`) | `escalated` | `action="escalate"`, `amount_vnd=0` |
| 10 | Giá món thiếu > 100.000đ | `escalated` | `action="escalate"`, `amount_vnd=0` |
| 11 | Thiếu/sai món hợp lệ (≤ 100.000đ, có ảnh, ≤ 12h, ≤ 3 lần) | `draft_ready` | `action="refund"`, `amount_vnd=<giá món>` |
| 12 | Giao trễ ≥ 30 phút (≤ 3 lần/tháng) | `draft_ready` | `action="voucher"`, `amount_vnd=50000` |

> **Lưu ý thứ tự ưu tiên 6 trước 9:** Nếu khách tần suất cao (`USR-004`, `ORD-1005`) đòi hoàn món không có trong đơn (`D08`), hệ thống từ chối ngay theo nguồn sự thật (`orders.json`) trước khi xét tần suất khiếu nại (`D09`).

### 2.3. Neo mốc thời gian tham chiếu (`REFERENCE_NOW`)
Mặc định dùng `REFERENCE_NOW = "2026-11-27T17:30:00+07:00"` (cho phép ghi đè qua biến môi trường `REFERENCE_NOW`). Ở mốc này, `ORD-1001..ORD-1005` nằm trong hạn 12 tiếng và `ORD-1006` (hoàn thành 20:35 ngày 26/11) quá hạn ~20.9 tiếng, đảm bảo kết quả `eval` nhất quán xuyên suốt CP3 và CP4.

### 2.4. Đa provider trong `codebase/ai.py`
Hỗ trợ đồng thời `openai` (kèm `BASE_URL` tuỳ chọn cho API tương thích OpenAI), `gemini` (Google AI Studio REST), `anthropic` và `ollama` bằng thư viện chuẩn `urllib` (không thêm dependency ngoài), luôn đọc token thật từ `usage` / `usageMetadata` (gồm cả `thoughtsTokenCount` nếu có).

## 3. Hệ quả (Consequences)
- **Tích cực:** Mỗi lượt chỉ tốn đúng 1 lần gọi model; 100% ca biên/tấn công bị chặn bằng code trước khi gọi LLM; không bị lỗi thời gian 12h khi chạy chấm vào ngày 28/11; đổi model chỉ cần sửa `.env`.
- **Đánh đổi:** Lớp trích xuất heuristic bằng tiếng Việt (nhận diện ảnh, tên món, ý định hỏi SLA) cần được kiểm thử kỹ và tinh chỉnh thêm ở `AI-02` nếu Lượt 1 phát hiện cách diễn đạt mới từ người dùng.
