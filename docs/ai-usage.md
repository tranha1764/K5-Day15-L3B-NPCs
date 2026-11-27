# Khai báo dùng AI

README của nhóm có mục "Dùng AI vào việc gì" (2–3 dòng, bắt buộc). Ghi chi tiết vào bảng dưới đây.

> Luật của đề: dùng AI để làm bài thoải mái, nhưng **ai không giải thích được phần có tên mình thì phần đó nhận 0 điểm**. Khai thiếu không bị trừ; giấu mới bị.

| Việc | Công cụ AI | AI làm gì | Người kiểm/sửa gì | Ai phụ trách |
|---|---|---|---|---|
| Code bản chạy thử | *(chưa thực hiện)* | Sẽ dùng coding agent hỗ trợ viết `agent.py`, `tools.py`, `app.py` | Kiểm logic ngưỡng cứng và test tay | Đoàn Trí Hùng, Nguyễn Đình Nam |
| Prompt / thiết kế lời gọi mô hình | *(chưa thực hiện)* | Sẽ thử nghiệm `SYSTEM` prompt ở bước `AI-01` / `AI-02` | Kiểm độ bám chính sách và không tự duyệt | Đoàn Trí Hùng |
| Đào data (viết script đếm, gợi ý nhãn) | Coding agent (Claude Code / Gemini) | Viết script đọc RSS Apple App Store VN, xuất bảng `evidence/reviews_labeled.csv` (300 review) và `evidence/count_reviews.py` | Định nghĩa nhãn `tre_ghep`, `sai_thieu_mat`, `cskh_hoan_tien`; lọc các ca nhầm ngữ cảnh (vd `R148` "Hình AI" trên Grab, các review 4–5★) và kiểm khớp bảng đếm | Trần Quang Hà |
| Rà câu hỏi phỏng vấn / khảo sát | Claude Code | Soạn nháp 5 câu hỏi khảo sát (`evidence/survey/questions.md`), script tạo Google Form (`create_form.gs`) và tổng hợp đếm số phiếu từ `results.csv` | Nhóm tự chốt câu hỏi, lọc phiếu spam (`S04`), tự gửi thu thập 24 phản hồi từ người thật và kiểm chéo lại toàn bộ số đếm `n=23` | Trần Quang Hà (cả nhóm gửi form) |
| Viết câu thử (benchmark) | Claude Code | Hỗ trợ cấu trúc hóa 14 câu thử ban đầu từ chính sách ShopeeFood và các ca biên D1 | Kiểm từng `expected` / `pass_criterion` theo policy `76251`, `71069`, `71298`; 2 câu lấy nguyên văn từ khảo sát (`D13`: S06, `D14`: S03) | Ngô Minh Cương, Trần Quang Hà |
| Sinh data `synthetic` (nếu có) | Claude Code | Dựng `data/orders.json` (6 đơn) và `data/history.json` (5 user) theo schema `mindweave/food-delivery-orders` | Không dùng seed ngẫu nhiên; kiểm tay toàn bộ 6 đơn hàng và 5 user để khớp ca biên trong `benchmark.csv` | Ngô Minh Cương |
| Chấm cột `pass` bằng LLM (nếu có) | Không dùng (chấm tay / code) | — | Chấm thủ công ở lượt `eval/run-1.csv` và `run-2.csv` | Ngô Minh Cương |
| Slide, văn bản | Claude Code / Gemini | Soạn nháp khung `canvas.md`, `spec.md`, `evidence/data-mining.md`, `evidence/summary.md`, `README.md` | Nhóm duyệt ngưỡng giả thuyết, phân công, số liệu khảo sát/review và chuẩn "đạt" (`spec.md` §7) trước khi commit | Trần Quang Hà |

**Không dùng AI để:** tạo người được phỏng vấn, trích dẫn, câu trả lời khảo sát; sửa kết quả các lượt đã chạy (`eval/run-*.csv`, `cost/simulate-*.csv`, `traces/`).
