# Đào data — review công khai trên Apple App Store Việt Nam

> Điền ở guide bước 1.2 (mục *Đào review công khai*, track B–F).
> Bảng từng review đã gắn nhãn (bỏ tên người viết, trích tối đa 2 câu): [evidence/reviews_labeled.csv](reviews_labeled.csv) · Script đếm chạy lại được: [evidence/count_reviews.py](count_reviews.py).

## 1. Cách đếm — viết TRƯỚC khi chạy

- **Nguồn dữ liệu & ngày xem:** 100 review mới nhất (2 trang RSS đầu, **mọi mức sao** 1★–5★) của mỗi app tại Việt Nam trên **Apple App Store Customer Reviews RSS**, xem ngày **27/11/2026**:
  - **ShopeeFood - Food Delivery** (`id=1137866760`, 11/11 → 26/11/2026): `https://itunes.apple.com/vn/rss/customerreviews/page=1/id=1137866760/sortby=mostrecent/json` (và `page=2`)
  - **Grab: Food Delivery, Taxi Ride** (`id=647268330`, 19/11 → 26/11/2026): `https://itunes.apple.com/vn/rss/customerreviews/page=1/id=647268330/sortby=mostrecent/json` (và `page=2`)
  - **be - Multi-Service Platform** (`id=1440565902`, 01/11 → 26/11/2026): `https://itunes.apple.com/vn/rss/customerreviews/page=1/id=1440565902/sortby=mostrecent/json` (và `page=2`)
- **Định nghĩa nhãn** *(chỉ gắn nhãn vấn đề với các review 1★–3★; 1 review có thể mang nhiều nhãn)*:
  - `tre_ghep`: phản ánh đơn giao chậm, trễ giờ dự kiến, hoặc bị ghép nhiều đơn khiến chờ lâu / đồ ăn nguội.
  - `sai_thieu_mat`: phản ánh giao sai món, thiếu món, không đúng mô tả/ảnh, hết món, hoặc báo đã giao nhưng chưa nhận được hàng / bị lấy mất hàng.
  - `cskh_hoan_tien`: phản ánh khiếu nại khó, tổng đài / hỗ trợ / **bot AI** trả lời rập khuôn, vòng vo, không phản hồi hoặc chậm/không hoàn tiền (hoặc ép hoàn voucher thay tiền mặt). Nhãn phụ `bot_ai`: nhắc trực tiếp bot / AI / con tép / trả lời rập khuôn.
- **Mẫu số:** `N = 100` review/app (tổng `N = 300` review đã đọc và gắn nhãn, bao gồm cả review khen 5★ và review không liên quan).
- **Script đếm:** `python evidence/count_reviews.py` (đọc trực tiếp `evidence/reviews_labeled.csv`).

## 2. Đọc trước, đếm sau

Đã đọc toàn bộ 300 review đầu (100/app). Các kiểu vấn đề lặp lại trước khi thống kê:
- **ShopeeFood:** khách phàn nàn nhiều nhất về ghép 2–5 đơn khiến giao trễ 45 phút đến >2 tiếng, kèm tình trạng "nhắn con tép" (chatbot) chờ nhân viên lâu, tổng đài trả lời rập khuôn hoặc không xem bằng chứng.
- **Grab:** ngoài ghép đơn giao trễ, nổi bật nhất là nhóm phản ánh **"bot AI" / "AI spam 1 câu" / "không có hotline"** và gửi khiếu nại nhiều ngày không phản hồi / chưa nhận được tiền hoàn.
- **Be:** ít phàn nàn ghép đơn giao đồ ăn trễ hơn, nhưng lặp lại cùng nỗi đau về CSKH **"toàn AI trả lời"**, hoàn tiền đồ ăn chờ nửa tháng, hoặc **không hoàn tiền mà tặng voucher** (khớp phản ánh `S23` trong khảo sát của nhóm).

## 3. Kết quả (`N = 300`, mọi mức sao)

| App | N | Review 1–3★ | Giao trễ / ghép đơn (`tre_ghep`) | Sai / thiếu / mất đơn (`sai_thieu_mat`) | CSKH / bot AI / hoàn tiền (`cskh_hoan_tien`) | Có ≥1 vấn đề trong 3 nhóm |
|---|---:|---:|---:|---:|---:|---:|
| **ShopeeFood** | 100 | 67/100 (67.0%) | **28/100 (28.0%)** | 3/100 (3.0%) | 9/100 (9.0%) *(2 nói thẳng bot/rập khuôn)* | **36/100 (36.0%)** |
| **Grab** | 100 | 85/100 (85.0%) | 24/100 (24.0%) | 6/100 (6.0%) | **24/100 (24.0%)** *(7 chỉ đích danh bot AI)* | **46/100 (46.0%)** |
| **Be** | 100 | 64/100 (64.0%) | 4/100 (4.0%) | 4/100 (4.0%) | **15/100 (15.0%)** *(1 nói thẳng AI + ca ép voucher)* | 18/100 (18.0%) |
| **Tổng 3 app** | **300** | **216/300 (72.0%)** | **56/300 (18.7%)** | **13/300 (4.3%)** | **48/300 (16.0%)** *(10 nói thẳng bot/AI)* | **100/300 (33.3%)** |

*(Lưu ý khi đọc số: tổng `56 + 13 + 48 > 100` vì một số review đề cập đồng thời cả giao trễ/mất đơn và CSKH kém.)*

## 4. ≥5 ví dụ cụ thể (trích ≤ 2 câu, đã bỏ tên người viết)

1. **`R008` · ShopeeFood · 1★ · 24/11/2026 (`sai_thieu_mat`, `cskh_hoan_tien`, `bot_ai`):** *"Chính sách giải quyết không bảo vệ khách hàng, tổng đài trả lời rập khuôn, mất thời gian, đơn chuyển và yêu cầu kh trả thêm ship mới giao không thì tự huỷ không hoàn tiền và cũng không giao hàng. Công ty ra chính sách như chiếm đoạt của kh, để mặt kh giải quyết với người giao"*
2. **`R013` · ShopeeFood · 2★ · 23/11/2026 (`tre_ghep`, `cskh_hoan_tien`, `bot_ai`):** *"Nên để thẳng số của quán cần gì thì gọi thẳng luôn, cứ nhắn với con tép r đợi nch với nv hỗ trợ tốn hết cả thgian ai rảnh đâu mà canh. Mỗi lần cần xử lý là ngồi đợi ngồi canh tốn thgian vch ra"*
3. **`R037` · ShopeeFood · 1★ · 19/11/2026 (`cskh_hoan_tien`):** *"bộ phận chăm sóc khách hàng mà coi khách hàng như rác những bằng chứng đã có gửi lên thì không thèm xem xong tự nhiên mất tiền oan . Nên xem lại cách làm việc của mình đi bảo sao ko cạnh tranh lại các nền tảng giao đồ khác"*
4. **`R149` · Grab · 1★ · 22/11/2026 (`cskh_hoan_tien`, `bot_ai`):** *"Tệ , hỗ trợ KH bằng 1 con AI dốt , không hiểu vấn đề , thái độ tệ"*
5. **`R194` · Grab · 1★ · 19/11/2026 (`tre_ghep`, `sai_thieu_mat`, `cskh_hoan_tien`, `bot_ai`):** *"App phục vụ tệ, sai sót nhắn hỗ trợ toàn là bot AI, không biết giải quyết nên bảo gửi cho admin, admin chờ đọc thông tin rồi lặn luôn. 1 lần đặt món bị hết món, quán kiu đổi món khác giúp mà chỉ 1 option đổi mình ko ăn được, quán bỏ món đó nhưng grab ko hoàn tiền..."*
6. **`R188` · Grab · 1★ · 20/11/2026 (`tre_ghep`, `cskh_hoan_tien`, `bot_ai`):** *"Ngoài con chat AI thì có cách nào complaint dịch vụ được không? Mỗi lần đặt đồ ăn, trả phí dịch vụ nhanh, thì luôn luôn bị giao trễ từ 15p có khí đến cả 60p, nhưng phí thì vẫn giữ nguyên."*
7. **`R221` · Be · 1★ · 20/11/2026 (`cskh_hoan_tien`):** *"Tôi bị tài xế không đón và hoàn thành chuyến mất tiền. Báo cáo tổng đài 1 ngày không làm việc sau 2 ngày email không hoàn tiền mà tặng voucher."*
8. **`R281` · Be · 1★ · 05/11/2026 (`sai_thieu_mat`, `cskh_hoan_tien`, `bot_ai`):** *"Báo cáo tài xế quỵt đồ của khách, nhắn vô CSKH toàn AI trả lời, đến khi khách tức không nhắn được nữa thì thôi"*

## 5. Giới hạn của data

- Người viết review trên App Store thường là người đang gặp trải nghiệm xấu (`72.0%` trong mẫu 300 review mới nhất là 1–3★, dù điểm trung bình toàn app đều `4.68–4.84★`), nên tỷ lệ này không phải tỷ lệ lỗi trên tổng mọi đơn hàng thực tế.
- **ShopeeFood** là app chuyên giao đồ ăn; còn **Grab** và **Be** là siêu ứng dụng nên một phần review thuộc nhãn `tre_ghep` hoặc `cskh_hoan_tien` phản ánh dịch vụ đặt xe / giúp việc chứ không riêng giao đồ ăn.
- → Kiểm lại bằng khảo sát người dùng đặt đồ ăn thật của nhóm (`n = 23` phiếu hợp lệ trong `evidence/survey/results.csv`, tổng hợp ở `evidence/summary.md`).
