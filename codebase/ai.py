"""Nối model — chỗ DUY NHẤT trong bản chạy thử gọi model AI.

Hợp đồng (giữ nguyên để khung đo được token):
    call_model(system: str, user: str) -> dict với 4 khoá
        "text":       str   chữ model trả về
        "model":      str   tên model đã gọi (để tra giá ở bảng giá model)
        "tokens_in":  int   số token vào, lấy từ trường usage trong phản hồi API — KHÔNG ước lượng
        "tokens_out": int   số token ra, gồm cả token suy luận / suy nghĩ nếu API tính riêng

Hỗ trợ đa provider bằng thư viện chuẩn (urllib):
    - fake (mặc định khi chưa cấu hình .env)
    - openai (và các endpoint tương thích OpenAI qua BASE_URL tuỳ chọn)
    - gemini (Google AI Studio REST API)
    - anthropic (Claude Messages API)
    - ollama (chạy cục bộ)
"""
import json
import os
import urllib.error
import urllib.parse
import urllib.request

from tracing import model_call

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SHOW_RAW = False  # đổi thành True để in phản hồi thô khi cần kiểm tra trường usage


def load_env(path=os.path.join(ROOT, ".env")):
    """Đọc file .env (KEY=VALUE mỗi dòng) vào biến môi trường, không ghi đè biến đã có."""
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8-sig") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))


load_env()
MODEL_PROVIDER = (os.environ.get("MODEL_PROVIDER") or "fake").strip().lower()
MODEL_NAME = (os.environ.get("MODEL_NAME") or "").strip()
API_KEY = (os.environ.get("API_KEY") or "").strip()
BASE_URL = (os.environ.get("BASE_URL") or "").strip()

URL_OPENAI = "https://api.openai.com/v1/chat/completions"
URL_CLAUDE = "https://api.anthropic.com/v1/messages"
URL_OLLAMA = "http://localhost:11434/api/chat"


def post_json(url: str, headers: dict, body: dict, timeout: int = 60) -> dict:
    """Gửi POST JSON, trả về JSON phản hồi. Chỉ dùng thư viện chuẩn (urllib)."""
    req = urllib.request.Request(
        url,
        data=json.dumps(body).encode("utf-8"),
        method="POST",
        headers=dict({"Content-Type": "application/json"}, **headers),
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            data = json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detail = e.read().decode("utf-8", "replace")[:300]
        raise RuntimeError("HTTP %d: %s" % (e.code, detail)) from e
    if SHOW_RAW:
        print(json.dumps(data, ensure_ascii=False, indent=2)[:3000])
    return data


def call_openai(system: str, user: str) -> dict:
    """Gọi OpenAI hoặc API tương thích OpenAI (tuỳ chọn BASE_URL trong .env)."""
    url = BASE_URL or URL_OPENAI
    messages = ([{"role": "system", "content": system}] if system else []) + [
        {"role": "user", "content": user}
    ]
    data = post_json(
        url,
        {"Authorization": "Bearer " + API_KEY},
        {"model": MODEL_NAME, "messages": messages, "temperature": 0.2},
    )
    usage = data.get("usage") or {}
    text = (data["choices"][0]["message"].get("content") or "").strip()
    return {
        "text": text,
        "tokens_in": int(usage.get("prompt_tokens", 0)),
        "tokens_out": int(usage.get("completion_tokens", 0)),
    }


def call_gemini(system: str, user: str) -> dict:
    """Gọi Google Gemini API (generateContent), cộng cả thoughtsTokenCount nếu có."""
    model_path = urllib.parse.quote(MODEL_NAME, safe="")
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/%s:generateContent?key=%s"
        % (model_path, urllib.parse.quote(API_KEY, safe=""))
    )
    body = {
        "contents": [{"role": "user", "parts": [{"text": user}]}],
        "generationConfig": {"temperature": 0.2},
    }
    if system:
        body["system_instruction"] = {"parts": [{"text": system}]}
    data = post_json(url, {}, body)
    candidates = data.get("candidates") or []
    parts = (candidates[0].get("content") or {}).get("parts") or [] if candidates else []
    text = "".join(
        p.get("text", "") for p in parts if isinstance(p, dict) and not p.get("thought")
    ).strip()
    usage = data.get("usageMetadata") or {}
    tokens_in = int(usage.get("promptTokenCount", 0))
    tokens_out = int(usage.get("candidatesTokenCount", 0)) + int(
        usage.get("thoughtsTokenCount", 0)
    )
    return {"text": text, "tokens_in": tokens_in, "tokens_out": tokens_out}


def call_claude(system: str, user: str) -> dict:
    """Gọi Anthropic Claude Messages API."""
    body = {
        "model": MODEL_NAME,
        "max_tokens": 1024,
        "messages": [{"role": "user", "content": user}],
    }
    if system:
        body["system"] = system
    data = post_json(
        URL_CLAUDE,
        {"x-api-key": API_KEY, "anthropic-version": "2023-06-01"},
        body,
    )
    text = "".join(
        b.get("text", "") for b in data.get("content", []) if b.get("type") == "text"
    ).strip()
    usage = data.get("usage") or {}
    return {
        "text": text,
        "tokens_in": int(usage.get("input_tokens", 0)),
        "tokens_out": int(usage.get("output_tokens", 0)),
    }


def call_ollama(system: str, user: str) -> dict:
    """Gọi model chạy cục bộ qua Ollama."""
    url = BASE_URL or URL_OLLAMA
    messages = ([{"role": "system", "content": system}] if system else []) + [
        {"role": "user", "content": user}
    ]
    data = post_json(
        url,
        {},
        {"model": MODEL_NAME, "messages": messages, "stream": False},
        timeout=300,
    )
    return {
        "text": (data.get("message") or {}).get("content", "").strip(),
        "tokens_in": int(data.get("prompt_eval_count", 0)),
        "tokens_out": int(data.get("eval_count", 0)),
    }


@model_call
def call_model(system: str, user: str) -> dict:
    if MODEL_PROVIDER == "fake":
        last = (user.strip().splitlines() or [""])[-1]
        return {
            "text": "[câu trả lời giả — chưa nối model] " + last[:80],
            "model": "fake",
            "tokens_in": 0,
            "tokens_out": 0,
        }

    if not MODEL_NAME:
        raise ValueError("Thiếu MODEL_NAME trong .env cho MODEL_PROVIDER=%s" % MODEL_PROVIDER)
    if MODEL_PROVIDER != "ollama" and not API_KEY:
        raise ValueError("Thiếu API_KEY trong .env cho MODEL_PROVIDER=%s" % MODEL_PROVIDER)

    if MODEL_PROVIDER in ("openai", "openai-compatible", "deepseek", "groq", "openrouter"):
        r = call_openai(system, user)
    elif MODEL_PROVIDER in ("gemini", "google"):
        r = call_gemini(system, user)
    elif MODEL_PROVIDER in ("anthropic", "claude"):
        r = call_claude(system, user)
    elif MODEL_PROVIDER == "ollama":
        r = call_ollama(system, user)
    else:
        raise NotImplementedError(
            "Không hỗ trợ MODEL_PROVIDER=%s trong codebase/ai.py — chọn openai, gemini, anthropic hoặc ollama"
            % MODEL_PROVIDER
        )

    return {
        "text": r["text"],
        "model": MODEL_NAME,
        "tokens_in": int(r["tokens_in"]),
        "tokens_out": int(r["tokens_out"]),
    }
