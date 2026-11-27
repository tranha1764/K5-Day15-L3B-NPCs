# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | Coding agent (Claude Code / Codex) | Hỗ trợ khung `codebase/agent.py`, `tools.py`, `ai.py` (`AI-01`, `AI-02`), server `codebase/app.py` và giao diện React `frontend/` (`FE-01`) | Thành viên kiểm logic guardrail, rà hợp đồng JSON, sửa hiển thị link trên UI và test tay trực tiếp trên `http://127.0.0.1:8000` | Đoàn Trí Hùng, Nguyễn Đình Nam, Trần Quang Hà |
| Prompt / thiết kế lời gọi mô hình | Coding agent | Soạn và tinh chỉnh `SYSTEM` prompt + `_build_user_prompt` trong `codebase/agent.py` qua 2 lượt (`AI-01` → `AI-02`) | Đối chiếu từng câu trả lời của `gpt-4o-mini` với `eval/run-1.csv` và `run-2.csv` để đảm bảo không tự duyệt hoàn tiền/voucher | Đoàn Trí Hùng, Ngô Minh Cương |
| Đào data (viết script đếm, gợi ý nhãn) | Coding agent (Claude Code / Gemini) | Viết script đọc RSS Apple App Store VN, xuất bảng `evidence/reviews_labeled.csv` (300 review) và `evidence/count_reviews.py` | Định nghĩa nhãn `tre_ghep`, `sai_thieu_mat`, `cskh_hoan_tien`; lọc các ca nhầm ngữ cảnh (vd `R148` "Hình AI" trên Grab, các review 4–5★) và kiểm khớp bảng đếm | Trần Quang Hà |
| Rà câu hỏi phỏng vấn / khảo sát | Claude Code | Soạn nháp 5 câu hỏi khảo sát (`evidence/survey/questions.md`), script tạo Google Form (`create_form.gs`) và tổng hợp đếm số phiếu từ `results.csv` | Nhóm tự chốt câu hỏi, lọc phiếu spam (`S04`), tự gửi thu thập 24 phản hồi từ người thật và kiểm chéo lại toàn bộ số đếm `n=23` | Trần Quang Hà (cả nhóm gửi form) |
| Viết câu thử (benchmark) | Claude Code | Hỗ trợ cấu trúc hóa và mở rộng `eval/benchmark.csv` từ 14 lên 24 câu (`thuong 8`, `kho 12`, `tu_choi 4`) | Kiểm từng `expected` / `pass_criterion` theo policy `76251`, `71069`, `71298`; `10/24` câu lấy từ lời người dùng khảo sát hoặc chính sách thật | Ngô Minh Cương, Trần Quang Hà |
| Sinh data `synthetic` (nếu có) | Claude Code | Dựng `data/orders.json` (6 đơn) và `data/history.json` (5 user) theo schema `mindweave/food-delivery-orders` | Không dùng seed ngẫu nhiên; kiểm tay toàn bộ 6 đơn hàng và 5 user để khớp ca biên trong `benchmark.csv` | Ngô Minh Cương |
| Chấm cột `pass` bằng LLM (nếu có) | Không dùng (chấm tay) | — | Chấm thủ công toàn bộ 24 câu ở `eval/run-1.csv` (`20/24`) và `eval/run-2.csv` (`24/24`) theo `eval/metric_spec.yaml` | Ngô Minh Cương |
| Slide, văn bản | Claude Code / Gemini | Soạn nháp khung `canvas.md`, `spec.md`, `evidence/data-mining.md`, `evidence/summary.md`, `README.md` | Nhóm duyệt ngưỡng giả thuyết, phân công, số liệu khảo sát/review và chuẩn "đạt" (`spec.md` §7) trước khi commit | Trần Quang Hà |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
