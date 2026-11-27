# DATA CARD — Đề tài D1: Xử lý khiếu nại đơn giao đồ ăn

## 1. Nguồn chính sách thật (`data/policies.json`)
Tham khảo từ **Trung tâm Trợ giúp ShopeeFood** (kiểm tra ngày **27/11/2026**):
- **Thiếu / Sai món (`76251`):** Tiếp nhận trong vòng **12 tiếng** kể từ khi đơn hoàn thành; yêu cầu ảnh thực tế toàn bộ món đã nhận và mô tả món thiếu/sai; hỗ trợ liên hệ quán hoặc bồi hoàn.  
  Nguồn: https://help.cs.shopeefood.vn/portal/102/article/76251-L%C3%A0m-th%E1%BA%BF-n%C3%A0o-khi-%C4%91%C6%A1n-h%C3%A0ng-b%E1%BB%8B-thi%E1%BA%BFu%2Fsai-m%C3%B3n
- **Tài xế giao trễ (`71069`):** Kiểm tra thời gian dự kiến trên app, liên hệ tài xế trước; nếu trễ quá lâu hoặc tài xế không phản hồi thì chuyển sang Chat với CSKH.  
  Nguồn: https://help.cs.shopeefood.vn/portal/102/article/71069-L%C3%A0m-th%E1%BA%BF-n%C3%A0o-khi-T%C3%A0i-x%E1%BA%BF-giao-tr%E1%BB%85-%C4%91%C6%A1n-h%C3%A0ng-c%E1%BB%A7a-t%C3%B4i-(%C4%91ang-giao)
- **Thời gian hoàn tiền (`71298`):** Thời gian kiểm tra giao dịch **1–3 ngày làm việc**; hoàn về ví ShopeePay/Số dư TK Shopee thường trong **24 giờ** sau khi xác nhận (thẻ ngân hàng tùy ngân hàng phát hành).  
  Nguồn: https://help.cs.shopeefood.vn/portal/102/article/71298-Khi-n%C3%A0o-t%C3%B4i-nh%E1%BA%ADn-%C4%91%C6%B0%E1%BB%A3c-ti%E1%BB%81n-ho%C3%A0n-tr%E1%BA%A3

> **Lưu ý phần giả lập bổ sung:** Các ngưỡng định lượng nội bộ (ví dụ: trễ > 30 phút tặng voucher tối đa 50.000đ, tự động hoàn món thiếu tối đa 100.000đ) được thiết lập giả lập theo đề bài D1 vì sàn không công khai hạn mức tự động.

## 2. Dữ liệu đơn hàng & lịch sử (`data/orders.json`, `data/history.json`)
- **Cấu trúc đơn hàng & thời gian trễ:** Tham khảo cấu trúc từ dataset công khai `mindweave/food-delivery-orders` (Hugging Face), nội địa hóa sang đơn vị VNĐ.
- **Lịch sử khiếu nại người dùng:** Dữ liệu giả lập có kiểm soát (tạo mẫu khách bình thường 0–1 lần/tháng và khách khiếu nại nhiều lần trong tháng).

## 3. Bộ câu thử (`eval/benchmark.csv`)
- Gồm 12 tình huống khiếu nại (≥ 10 ca) tổng hợp từ phản hồi thực tế của người dùng và các ca biên của đề bài D1 (đơn thiếu 1 món trong đơn 500k, trễ 29 phút sát ngưỡng 30 phút, tin nhắn cụt, đòi món ngoài đơn, dọa 1★, nghi dị vật/ngộ độc).

## 4. Quyền riêng tư & An toàn dữ liệu
- Toàn bộ `user_id`, `order_id`, tên người dùng đều được ẩn danh/giả lập, không chứa SĐT, địa chỉ thật hay dữ liệu cá nhân.
- Không coi review 1★ đơn lẻ là đại diện cho toàn bộ người dùng.
