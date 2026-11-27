# Tóm tắt mô phỏng simulate-1@20261128-012706

Do `python run.py simulate` sinh ra — không sửa tay. Chép bảng sang `cost/cost-estimate.md`.

| Persona | Số phiên mô phỏng | Lượt hỏi / phiên | Token vào / phiên | Token ra / phiên | Gọi model / phiên | Gọi công cụ / phiên |
|---|---:|---:|---:|---:|---:|---:|
| dat_it | 23 | 1 | 1305 | 139 | 1.0 | 2.3 |
| dat_vua | 24 | 2 | 2597 | 248 | 2.0 | 5.8 |
| dat_nhieu | 3 | 2 | 2185 | 228 | 2.0 | 3.7 |

Tỉ lệ đạt dùng để tính: 24/24 (100%) — lượt run-2@20261128-012206

- Tỉ lệ đạt lấy từ lượt nhóm chọn: eval/run-2.csv (--rate-from).

| Model (giá) | Chi phí / phiên | Chi phí / task thành công | Chi phí / câu hỏi đạt | Chi phí / tháng — thấp (500 người) | Chi phí / tháng — cơ sở (1.000 người) | Chi phí / tháng — cao (3.000 người) | Chi phí / người / tháng (cơ sở) |
|---|---:|---:|---:|---:|---:|---:|---:|
| gpt-4o-mini (vào 0.15 · ra 0.6 $/1M) | $0.00041 (≈ 11 ₫) | $0.00041 (≈ 11 ₫) | $0.00027 (≈ 7 ₫) | $0.3978 (≈ 10.105 ₫) | $0.7957 (≈ 20.210 ₫) | $2.39 (≈ 60.630 ₫) | $0.00080 (≈ 20 ₫) |
| gpt-4o (vào 2.5 · ra 10.0 $/1M) | $0.0069 (≈ 176 ₫) | $0.0069 (≈ 176 ₫) | $0.0045 (≈ 114 ₫) | $6.63 (≈ 168.417 ₫) | $13.26 (≈ 336.834 ₫) | $39.78 (≈ 1.010.501 ₫) | $0.0133 (≈ 337 ₫) |

- Chi phí / task thành công = chi phí / phiên ÷ tỉ lệ đạt. Chi phí / câu hỏi đạt = chi phí / phiên ÷ số lượt hỏi trung bình mỗi phiên (1.5) ÷ tỉ lệ đạt — tỉ lệ đạt đo theo từng câu thử.
- Token đo trên model: gpt-4o-mini. Giá tính theo từng model trong bảng — model khác bộ tách token thì số token thật có thể lệch; ghi rõ "đo trên model X, tính giá model Y" trong cost/cost-estimate.md.
- Phiên lỗi (không tính vào trung bình): 0/50.
- Tỷ giá: 1 USD = 25.400 ₫ (Tỷ giá quy đổi tham chiếu 25.400 VND/USD (28/11/2026)).
