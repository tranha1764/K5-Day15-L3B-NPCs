"""Bản chạy thử — giao diện web chat cho D1 (xử lý khiếu nại đơn giao đồ ăn). Task FE-01.

Chạy bằng: python run.py            → mở giao diện web (http://127.0.0.1:8000, tự mở trình duyệt)
           python codebase/app.py --cli  → bản dòng lệnh cũ của khung (gõ đầu vào, in kết quả)

Chỉ dùng thư viện chuẩn (http.server) — không cần pip install.
Giao diện là React (mã nguồn ở frontend/), đã build sẵn vào codebase/static/ nên máy không có Node vẫn chạy được.
Sửa giao diện: cd frontend && npm install && npm run build   (hoặc npm run dev để sửa nóng, xem frontend/README.md).
Biến môi trường tuỳ chọn: APP_PORT (mặc định 8000) · APP_NO_BROWSER=1 (không tự mở trình duyệt).

Giao diện gọi thẳng answer(text) trong agent.py qua endpoint:
    POST /api/chat   {"message": "..."}
    → {"output", "status", "order_id", "draft", "order", "trace", "error"}
answer() chỉ bắt buộc trả "output"; các khoá phụ (status, order_id, draft) có thì hiển thị, không có thì bỏ qua.
Thẻ "Đơn hàng" đọc thẳng data/orders.json để HIỂN THỊ — không gọi công cụ, nên không làm lệch số lần gọi công cụ trong trace.
"""
import json
import os
import re
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import unquote

for _stream in (sys.stdout, sys.stderr, sys.stdin):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

STATIC_DIR = os.path.join(HERE, "static")  # bản build của frontend/ (React) — npm run build ghi vào đây
CONTENT_TYPES = {
    ".html": "text/html; charset=utf-8", ".js": "text/javascript; charset=utf-8",
    ".css": "text/css; charset=utf-8", ".json": "application/json; charset=utf-8",
    ".svg": "image/svg+xml", ".png": "image/png", ".ico": "image/x-icon", ".woff2": "font/woff2",
}
ORDERS_PATH = os.path.join(ROOT, "data", "orders.json")
ORDER_RE = re.compile(r"\bORD-\d{3,}\b", re.IGNORECASE)
MAX_MESSAGE_CHARS = 2000

# tracing ghi vào một biến toàn cục → mỗi lúc chỉ xử lý MỘT tin nhắn.
_answer_lock = threading.Lock()


def _where(e):
    """File (trong codebase/) gây lỗi khi nạp: SyntaxError có e.filename, lỗi khác lấy khung cuối của traceback."""
    import traceback
    path = getattr(e, "filename", None) or (traceback.extract_tb(e.__traceback__)[-1].filename if e.__traceback__ else "")
    if not path:
        return "codebase/"
    p = os.path.abspath(path)
    return os.path.relpath(p, ROOT).replace(os.sep, "/") if p.startswith(ROOT) else path


def _load_codebase():
    try:
        import tracing
        from agent import answer
    except Exception as e:  # lỗi cú pháp, thiếu thư viện… trong codebase/
        print("Không nạp được codebase/ — lỗi ở %s: %s: %s" % (_where(e), type(e).__name__, e))
        print("Sửa lỗi rồi chạy lại. Cách nối model: docs/connect-model.md")
        return None, None
    return tracing, answer


# ---------------------------------------------------------------- dữ liệu hiển thị

def _find_order(order_id):
    """Đọc data/orders.json để hiện thẻ đơn hàng. Không có file / không thấy đơn → None."""
    if not order_id:
        return None
    try:
        with open(ORDERS_PATH, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, ValueError):
        return None
    orders = data.get("orders", []) if isinstance(data, dict) else data
    for o in orders:
        if str(o.get("order_id", "")).upper() == order_id.upper():
            return {k: o.get(k) for k in ("order_id", "restaurant_name", "status", "delay_minutes",
                                          "payment_method", "items", "total_vnd", "completed_at")}
    return None


def handle_message(tracing, answer, message):
    """Chạy một tin nhắn qua answer(), trả dict JSON cho giao diện."""
    with _answer_lock:
        tracing.begin("app")
        t0 = time.perf_counter()
        error = None
        result = {}
        try:
            result = answer(message)
        except NotImplementedError as e:
            error = "Chưa nối model: %s" % e
        except Exception as e:  # lỗi gọi model / lỗi code — báo lên giao diện, server vẫn chạy
            error = "%s: %s" % (type(e).__name__, e)
        summary, _events = tracing.end()
        latency = round(time.perf_counter() - t0, 2)

    if not isinstance(result, dict):
        result = {"output": str(result)}
    order_id = result.get("order_id")
    if not order_id:  # agent chưa trả order_id → lấy mã đơn trong tin nhắn, chỉ để hiển thị
        m = ORDER_RE.search(message)
        order_id = m.group(0).upper() if m else None
    draft = result.get("draft") if isinstance(result.get("draft"), dict) else None
    return {
        "output": str(result.get("output", "")),
        "status": result.get("status"),
        "order_id": order_id,
        "draft": draft,
        "order": _find_order(order_id),
        "trace": {
            "models": summary["models"],
            "model_calls": summary["model_calls"],
            "tool_calls": summary["tool_calls"],
            "tokens_in": summary["tokens_in"],
            "tokens_out": summary["tokens_out"],
            "latency_s": latency,
            "errors": summary["errors"],
        },
        "error": error,
    }


# ---------------------------------------------------------------- web server

def make_handler(tracing, answer):
    class Handler(BaseHTTPRequestHandler):
        server_version = "NPCsDemo/1.0"

        def log_message(self, fmt, *args):  # gọn log: chỉ in lỗi
            if args and str(args[1]).startswith(("4", "5")):
                sys.stderr.write("[web] %s\n" % (fmt % args))

        def _send(self, code, body, ctype):
            data = body.encode("utf-8") if isinstance(body, str) else body
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def _json(self, code, obj):
            self._send(code, json.dumps(obj, ensure_ascii=False), "application/json; charset=utf-8")

        def do_GET(self):
            path = unquote(self.path.split("?", 1)[0])
            if path == "/api/health":
                self._json(200, {"ok": True})
                return
            if path in ("/", "/index.html"):
                path = "/index.html"
            # Chỉ phục vụ file nằm TRONG codebase/static (chặn ../ thoát ra ngoài).
            full = os.path.realpath(os.path.join(STATIC_DIR, path.lstrip("/")))
            if not full.startswith(os.path.realpath(STATIC_DIR) + os.sep) or not os.path.isfile(full):
                if path == "/index.html":
                    self._send(500, "Thiếu codebase/static/index.html — chạy: cd frontend && npm install && npm run build",
                               "text/plain; charset=utf-8")
                else:
                    self._send(404, "Không có trang này", "text/plain; charset=utf-8")
                return
            ctype = CONTENT_TYPES.get(os.path.splitext(full)[1].lower(), "application/octet-stream")
            with open(full, "rb") as f:
                self._send(200, f.read(), ctype)

        def do_POST(self):
            if self.path.split("?", 1)[0] != "/api/chat":
                self._json(404, {"error": "Không có endpoint này"})
                return
            try:
                length = int(self.headers.get("Content-Length") or 0)
                payload = json.loads(self.rfile.read(length).decode("utf-8") or "{}")
            except (ValueError, UnicodeDecodeError):
                self._json(400, {"error": "Body phải là JSON: {\"message\": \"...\"}"})
                return
            message = str(payload.get("message", "")).strip() if isinstance(payload, dict) else ""
            if not message:
                self._json(400, {"error": "Tin nhắn trống"})
                return
            if len(message) > MAX_MESSAGE_CHARS:
                self._json(400, {"error": "Tin nhắn dài quá %d ký tự" % MAX_MESSAGE_CHARS})
                return
            self._json(200, handle_message(tracing, answer, message))

    return Handler


def _bind(handler, first_port, host="127.0.0.1"):
    """Thử cổng first_port, bận thì thử 9 cổng kế tiếp."""
    last = None
    for port in range(first_port, first_port + 10):
        try:
            return ThreadingHTTPServer((host, port), handler), port
        except OSError as e:
            last = e
    raise OSError("Không mở được cổng %d–%d: %s" % (first_port, first_port + 9, last))


def run_web():
    tracing, answer = _load_codebase()
    if answer is None:
        return 1
    host = os.environ.get("APP_HOST") or "127.0.0.1"
    raw_port = os.environ.get("PORT") or os.environ.get("APP_PORT") or "8000"
    try:
        server, port = _bind(make_handler(tracing, answer), int(raw_port), host=host)
    except (OSError, ValueError) as e:
        print(e)
        return 1
    url = "http://%s:%d" % (host, port)
    print("Bản chạy thử (web) đang chạy: %s" % url, flush=True)
    print("Dừng: Ctrl+C. Bản dòng lệnh: python codebase/app.py --cli", flush=True)
    if not os.environ.get("APP_NO_BROWSER"):
        threading.Timer(0.6, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nĐã dừng.")
    finally:
        server.server_close()
    return 0


# ---------------------------------------------------------------- bản dòng lệnh (giữ từ khung)

def run_cli():
    tracing, answer = _load_codebase()
    if answer is None:
        return 1
    print("Bản chạy thử — gõ đầu vào rồi Enter. Thoát: Ctrl+C (hoặc Enter 2 lần với dòng trống).")
    blank = 0
    while True:
        try:
            text = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print()
            return 0
        if not text:
            blank += 1
            if blank >= 2:
                return 0
            continue
        blank = 0
        r = handle_message(tracing, answer, text)
        if r["error"]:
            print("[lỗi] %s" % r["error"])
            if r["error"].startswith("Chưa nối model"):
                return 1
            continue
        print(r["output"])
        if r["status"]:
            print("   [trạng thái: %s]" % r["status"])
        t = r["trace"]
        print("   (model: %s · gọi model %d lần · công cụ %d lần · token vào %d / ra %d)"
              % (", ".join(t["models"]) or "—", t["model_calls"], t["tool_calls"], t["tokens_in"], t["tokens_out"]))


if __name__ == "__main__":
    sys.exit(run_cli() if "--cli" in sys.argv[1:] else run_web())
