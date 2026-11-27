# Tổng hợp bằng chứng pain

> Điền ở guide bước 1.2, xong trước **CP3 10:00 Thứ Bảy 28/11**. Chấm ở rubric R1.
> Ba nguồn ngang nhau — tối thiểu **≥1 nguồn đạt ngưỡng**. Mạnh nhất: đào data ra insight → hỏi người dùng để kiểm lại (hoặc ngược lại).

## 1. Nguồn đã dùng

| Nguồn | Đạt ngưỡng? | File |
|---|---|---|
| Đào data (x/N, %, cách đếm chạy lại được, ≥5 ví dụ) | [x] | `evidence/data-mining.md` |
| Phỏng vấn (≥3 người ngoài nhóm, đúng người dùng) | ☐ | `evidence/interviews/P1.md`… |
| Khảo sát (≥20 người ngoài nhóm, đúng người dùng) | [x] | `evidence/survey/` |

## 2. Số chính

- Đào data: **100/300 (33.3%)** review mới nhất trên Apple App Store VN (ShopeeFood `36/100`, Grab `46/100`, Be `18/100`; xem ngày `27/11/2026`, mọi mức sao) đề cập ít nhất 1 vấn đề thuộc 3 nhóm: giao trễ / ghép đơn **`56/300` (18.7%)** (ShopeeFood `28/100`, Grab `24/100`, Be `4/100`), CSKH / bot AI vòng vo / chậm hoàn tiền **`48/300` (16.0%)** (Grab `24/100`, Be `15/100`, ShopeeFood `9/100`), sai / thiếu / mất đơn **`13/300` (4.3%)**. Chi tiết bảng & script đếm: `evidence/data-mining.md`, `evidence/count_reviews.py`.
- Phỏng vấn: chưa thực hiện *(nhóm dùng 2 nguồn chính là Khảo sát n = 23 và Đào review công khai N = 300)*.
- Khảo sát: n = 23 phiếu hợp lệ / 24 phiếu tổng (lọc 1 phiếu nhiễu `S04`; **đạt ngưỡng ≥20 người**). Trong 23 phiếu hợp lệ: **20/23 (87.0%)** từng gặp sự cố khi nhận đơn (giao trễ >30 phút `11/23` — 47.8%, giao thiếu món `10/23` — 43.5%, giao sai món `9/23` — 39.1%, không giống ảnh / giao ít so với mô tả `2/23` — 8.7%). Trong 20 người từng gặp sự cố: **10/20 (50.0%)** chọn *"Bỏ qua không khiếu nại vì thấy rườm rà / mất thời gian"*; `5/20` (25.0%) phải chờ vài tiếng đến hôm sau (tổng **15/20 — 75.0%** bỏ cuộc hoặc chờ lâu); `5/20` (25.0%) được giải quyết trong 5–10 phút. Vướng mắc lớn nhất (n=23): *"Bot trả lời chung chung, vòng vo không đúng vấn đề"* (`5/23` — 21.7%), *"Chờ nhân viên phản hồi / duyệt hoàn tiền quá lâu"* (`5/23` — 21.7%) và *"Phải tìm lại hóa đơn giấy, chụp nhiều ảnh bằng chứng"* (`5/23` — 21.7%); theo sau là *"Không rõ mình có đủ điều kiện được hoàn tiền/voucher hay không"* (`4/23` — 17.4%).

Phỏng vấn nhiều vai thì đếm theo từng vai, không cộng chung.

| | Vai | Gặp pain? | Số lần / 1 tháng qua | Lần gần nhất mất | Đang xoay xở bằng |
|---|---|---|---|---|---|
| P1 | | | | | |
| P2 | | | | | |
| P3 | | | | | |

## 3. ≥5 trích dẫn hoặc ví dụ nguyên văn (có nguồn, bỏ tên)

1. "món không đúng mô tả nhắn không liên hệ được quán." — phiếu khảo sát `S03`
2. "Quán giao sai món và thiếu món nhưng mà quán không xử lý và không được hoàn tiền" — phiếu khảo sát `S06`
3. "Tháng trước mình mở app giao hàng để khiếu nại vì đơn ghi đã giao thành công nhưng trước cửa nhà chẳng có ai. Bot hỗ trợ trả lời tự động lòng vòng suốt 20 phút, cuối cùng phải gửi ảnh camera mới được chuyển sang nhân viên xử lý." — phiếu khảo sát `S14`
4. "Cơm xá xíu nhìn không được đẹp mắt như trong hình" — phiếu khảo sát `S12`
5. "Có lần mình đặt một phần combo gà rán cho nhóm bạn, nhưng khi nhận hàng thì bị thiếu một món ăn kèm và tài xế đã rời đi." — phiếu khảo sát `S21`
6. "Khá khó chịu vì không được hoàn tiền mà chỉ được tặng voucher tương đương giá, mà mỗi lần đặt chỉ đc dùng 1 voucher thì như vậy nghĩa là bị lố tiền ship vì k đc dùng voucher freeship nữa." — phiếu khảo sát `S23`
7. "Nên để thẳng số của quán cần gì thì gọi thẳng luôn, cứ nhắn với con tép r đợi nch với nv hỗ trợ tốn hết cả thgian ai rảnh đâu mà canh." — review App Store ShopeeFood 2★ `23/11/2026` (`R013`)
8. "App phục vụ tệ, sai sót nhắn hỗ trợ toàn là bot AI, không biết giải quyết nên bảo gửi cho admin, admin chờ đọc thông tin rồi lặn luôn." — review App Store Grab 1★ `19/11/2026` (`R194`)

## 4. Các nguồn có khớp nhau không

Data đào 300 review công khai trên App Store nói: **18.7% (56/300)** phàn nàn giao trễ / ghép đơn (ShopeeFood `28%`, Grab `24%`) và **16.0% (48/300)** phàn nàn CSKH / bot AI vòng vo / chậm hoặc không hoàn tiền (Grab `24%`, Be `15%`, ShopeeFood `9%`). Người dùng khảo sát (`n = 23`) nói: **87.0% (20/23)** từng gặp sự cố (nhiều nhất là giao trễ >30p `11/23` = 47.8%, thiếu món `10/23` = 43.5%, sai món `9/23` = 39.1%), **50.0% (10/20)** bỏ qua khiếu nại vì rườm rà, vướng nhiều nhất ở bot trả lời vòng vo (`21.7%`), chờ nhân viên duyệt lâu (`21.7%`) và tìm hóa đơn/chụp ảnh (`21.7%`).
- **Chỗ khớp:** Cả hai nguồn đều xác nhận **2 trục pain giống nhau**: (1) giao trễ / ghép đơn là lỗi hay gặp nhất (`47.8%` trong khảo sát; `18.7%` trong review, riêng ShopeeFood `28%`); (2) chatbot/AI hỗ trợ vòng vo ("con tép", "bot AI") và chờ nhân viên hoàn tiền lâu là nguyên nhân trực tiếp khiến khách bức xúc hoặc bỏ cuộc. Đặc biệt, bức xúc về **ép tặng voucher thay tiền hoàn** xuất hiện ở cả khảo sát (`S23`) lẫn review thật (`R221`).
- **Chỗ lệch & vì sao:** Thiếu / sai món chiếm tỷ lệ rất cao trong khảo sát (`43.5%` và `39.1%`) nhưng chỉ chiếm `4.3% (13/300)` trên review App Store, vì với các món thiếu/sai giá trị nhỏ người dùng thường chọn bỏ qua (`50%` theo khảo sát) thay vì lên App Store đánh giá 1★ — họ chỉ viết review 1★ khi bị mất hẳn đơn/mất tiền hoặc bực bội kéo dài với CSKH. Ngoài ra, mẫu App Store của Grab và Be còn lẫn một phần phản ánh dịch vụ đặt xe bên cạnh giao đồ ăn.

## 5. Kết luận

Giả thuyết ở `evidence/hypothesis.md`: **đúng** — cả khảo sát (`n = 23`: `87.0%` gặp sự cố, `75.0%` bỏ qua hoặc chờ lâu) và đào review công khai (`N = 300`: `33.3%` nêu vấn đề giao nhận/CSKH, riêng nhóm CSKH/bot AI/hoàn tiền `16.0%` ≥ ngưỡng tự đặt `15%`) đều ủng hộ mạnh giả thuyết rằng khâu xử lý khiếu nại qua bot tự động và chờ hoàn tiền hiện tại đang gây mất thời gian, mất tiền và làm giảm niềm tin người dùng. Insight bổ sung từ cả hai nguồn (`S23`, `R221`): không nên tự động ép khách nhận voucher thay hoàn tiền khi chính sách cho phép hoàn về ví, và mọi bước kiểm tra điều kiện cần trả lời thẳng, minh bạch ngay thay vì vòng vo. Điều vẫn chưa biết: mức độ người dùng hài lòng khi dùng luồng mới của nhóm (sẽ kiểm thêm bằng người dùng thử ở `validation/log.md` nếu kịp).

## Lịch hẹn (dùng cho CP2 — chỉ ghi vai và giờ, không tên)

| Vai | Giờ hẹn | Đã xong? |
|---|---|---|
| | | |
