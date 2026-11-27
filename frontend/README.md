# Giao diện React — bản chạy thử D1

Chạy bản chạy thử **không cần Node**: `python run.py` ở thư mục gốc phục vụ bản build sẵn trong `codebase/static/`.
Chỉ người **sửa giao diện** mới cần Node 20.19+ (hoặc 22.12+).

## Lệnh

```bash
cd frontend
npm install          # lần đầu
npm run dev          # sửa nóng ở http://localhost:5173 — cần chạy song song `python run.py` (API ở cổng 8000)
npm run build        # kiểm kiểu TypeScript + build ra ../codebase/static/  → nhớ commit cả codebase/static/
```

Sửa xong **phải `npm run build` rồi commit `codebase/static/`**, nếu không `python run.py` vẫn chạy bản cũ.

## Cấu trúc

```
src/
├── main.tsx                     # điểm vào, gắn <App/>
├── App.tsx                      # bố cục: Header · FakeModeBanner · ChatPanel | Sidebar
├── types.ts                     # hợp đồng dữ liệu với POST /api/chat (khớp codebase/app.py)
├── api/chat.ts                  # gọi POST /api/chat, chuẩn hoá lỗi
├── hooks/useChat.ts             # state hội thoại: messages, latest, busy, send, reset
├── constants/
│   ├── quickCases.ts            # 7 ca demo 1 click (câu tự viết, không chép benchmark)
│   └── status.ts                # draft_ready / need_info / escalated / rejected → màu + câu chữ
├── utils/format.ts              # tiền VNĐ, dòng trace, phát hiện chế độ giả
├── styles/global.css            # token màu (sáng / tối) + lớp .tone-*
└── components/
    ├── layout/   Header · FakeModeBanner
    ├── chat/     ChatPanel → QuickCaseBar · MessageList (MessageBubble · TypingIndicator) · ChatInput
    ├── sidebar/  Sidebar → StatusCard (DraftDetails) · OrderCard (OrderItemsTable) · TraceCard
    └── common/   Card · KeyValueList · StatusBadge
```

Mỗi component có file `*.module.css` riêng (CSS Modules), màu lấy từ biến trong `global.css`.

## Hợp đồng với backend (TV2)

`answer(text)` trong `codebase/agent.py` chỉ bắt buộc trả `output`. Muốn thẻ trạng thái đổi màu, trả thêm:

```python
{"output": "...", "status": "draft_ready" | "need_info" | "escalated" | "rejected",
 "order_id": "ORD-1001", "draft": {"action": "refund" | "voucher" | "escalate", "amount_vnd": 35000, "reason": "..."}}
```

Thiếu khoá nào thì giao diện hiện màu xám "Chưa có trạng thái", không vỡ.
