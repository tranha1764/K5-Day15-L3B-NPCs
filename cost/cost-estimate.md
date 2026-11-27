# Chi phí khi dùng thật

> Điền ở guide bước 4.2, nộp ở CP4 14:30 Thứ Bảy 28/11. Chấm ở rubric R6.
> Số lấy từ `python3 run.py simulate --rate-from eval/run-2.csv` (`cost/simulate-1-summary.md`).

## 1. Đầu vào

- **Persona** (`cost/personas.yaml`): 3 kiểu (`dat_it` 0.48 · `dat_vua` 0.39 · `dat_nhieu` 0.13). Nguồn: Khảo sát `n = 23` phiếu hợp lệ (`evidence/survey/results.csv`).
- **Số người dùng thật** 3 kịch bản: thấp `500` · cơ sở `1.000` · cao `3.000`. Nguồn: Tự ước tính quy mô triển khai thử nghiệm (khớp `spec.md` §2).
- **Giá** 2 mức model (https://openai.com/api/pricing/ · xem 28/11/2026): `gpt-4o-mini` ($0.15 vào / $0.60 ra per 1M token) · `gpt-4o` ($2.50 vào / $10.00 ra per 1M token).
- **Tỉ lệ đạt** dùng để tính: `24/24 (100%)` — lượt `run-2@20261128-012206` (`eval/run-2.csv`).
- Đo token trên model `gpt-4o-mini`, tính giá model `gpt-4o-mini` và `gpt-4o` (tỷ giá 1 USD = 25.400 ₫).

## 2. Kết quả mô phỏng

Lượt mô phỏng: `cost/simulate-1.csv` · `50` phiên · `seed 42` · phiên lỗi `0/50`

| Model | Chi phí / phiên | Chi phí / task thành công | / tháng — thấp (500) | / tháng — cơ sở (1.000) | / tháng — cao (3.000) | / người / tháng (cơ sở) |
|---|---|---|---|---|---|---|
| `gpt-4o-mini` | $0.00041 (≈ 11 ₫) | $0.00041 (≈ 11 ₫) | $0.3978 (≈ 10.105 ₫) | $0.7957 (≈ 20.210 ₫) | $2.39 (≈ 60.630 ₫) | $0.00080 (≈ 20 ₫) |
| `gpt-4o` *(đo token trên `gpt-4o-mini`)* | $0.0069 (≈ 176 ₫) | $0.0069 (≈ 176 ₫) | $6.63 (≈ 168.417 ₫) | $13.26 (≈ 336.834 ₫) | $39.78 (≈ 1.010.501 ₫) | $0.0133 (≈ 337 ₫) |

Chi phí / task thành công = chi phí trung bình mỗi phiên ÷ tỉ lệ đạt.

## 3. So với impact

- Impact / người / tháng (`spec.md` §2): Tiết kiệm ~15–30 phút khiếu nại/chờ đợi mỗi tháng và giảm tỷ lệ bỏ qua khiếu nại (`10/20 = 50.0%` trong số người gặp sự cố theo khảo sát `n = 23`) do thiếu rõ ràng điều kiện hoàn tiền/voucher.
- Chi phí / người / tháng (cơ sở, model `gpt-4o-mini`): **$0.00080 (≈ 20 ₫)** (~20.210 ₫/tháng cho 1.000 người dùng).
- **Kết luận một dòng — đáng làm không:** **Rất đáng làm**, vì chỉ tốn ~**20 ₫/người/tháng** (rẻ hơn ~1.700 lần so với một món thiếu 35.000đ) nhưng giúp xử lý ngay lập tức và giảm gần một nửa ca người dùng bỏ cuộc khi khiếu nại.
