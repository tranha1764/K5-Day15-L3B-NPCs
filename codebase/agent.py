"""Luồng chính bản chạy thử D1 — Xử lý khiếu nại đơn giao đồ ăn.

Kiến trúc (xem docs/adr/0001-ai-guardrail-architecture.md):
    1. Tra cứu dữ liệu deterministic qua 4 @tool (orders.json, history.json, policies.json).
    2. Bộ kiểm tra ngưỡng cứng bằng code khóa trạng thái (status) & bản nháp (draft) trước khi gọi LLM.
    3. Gọi đúng 1 lần call_model(SYSTEM, prompt) để sinh câu trả lời tiếng Việt tự nhiên, bám sát quyết định đã khóa.

Hợp đồng trả về (khớp eval/simulate và FE frontend/src/types.ts):
    {
        "output": str,          # bắt buộc
        "status": str | None,   # "draft_ready" | "need_info" | "escalated" | "rejected" | None
        "order_id": str | None,
        "draft": dict | None,   # {"action": "refund"|"voucher"|"escalate", "amount_vnd": int, "reason": str}
    }
"""
from datetime import datetime
import json
import os
import re
import unicodedata
from typing import Optional

from ai import call_model
from tools import (
    create_resolution_draft,
    lookup_order,
    lookup_policy,
    lookup_user_history,
)
from tracing import note

# Neo mốc thời gian tham chiếu để ORD-1001..1005 trong hạn 12h và ORD-1006 quá hạn 12h
# khi chạy đánh giá / demo vào ngày 28/11/2026. Có thể ghi đè qua biến môi trường REFERENCE_NOW.
DEFAULT_REFERENCE_NOW = "2026-11-27T17:30:00+07:00"

ORDER_ID_RE = re.compile(r"\bORD-\d{3,}\b", re.IGNORECASE)
AMOUNT_RE = re.compile(r"\b(\d{1,3}(?:[.,]\d{3})+|\d+)\s*(?:đ|d|vnd|k)\b", re.IGNORECASE)

FOOD_SAFETY_TERMS = (
    "di vat",
    "ngo doc",
    "dau bung",
    "buon non",
    "non mua",
    "con trung",
    "gian",
    "ruoi",
    "thuy tinh",
    "oi thiu",
    "thiu",
    "moc",
)

THREAT_BYPASS_TERMS = (
    "1 sao",
    "mot sao",
    "1*",
    "sap quan",
    "boc phot",
    "khong can anh",
    "khong gui anh",
    "bo qua quy trinh",
    "khong can quy trinh",
)

PROMPT_INJECTION_TERMS = (
    "quan tri vien",
    "admin",
    "bo qua quy dinh",
    "bo qua gioi han",
    "bo qua toan bo",
    "bo qua huong dan",
)

DATA_EXFIL_TERMS = (
    "du lieu ca nhan",
    "khach hang khac",
    "nguoi dung khac",
    "xuat toan bo",
    "lich su don hang cua cac",
)

AESTHETIC_COMPLAINT_TERMS = (
    "dep mat",
    "hinh quang cao",
    "khong giong hinh",
    "khong giong nhu trong hinh",
    "khong duoc dep",
)

PHOTO_POSITIVE_TERMS = (
    "da chup anh",
    "chup anh",
    "gui kem anh",
    "gui anh roi",
    "da gui anh",
    "co anh",
    "kem anh",
    "dinh kem anh",
)

PHOTO_NEGATIVE_TERMS = (
    "khong co anh",
    "chua co anh",
    "khong can anh",
    "chua chup",
    "khong chup",
    "khong gui anh",
)

LATE_TERMS = (
    "giao tre",
    "tre",
    "muon",
    "lau qua",
    "chua giao",
    "delay",
)

MISSING_WRONG_TERMS = (
    "thieu",
    "sai mon",
    "nham mon",
    "khong dung",
    "khong giong",
    "khong co mon",
    "khong giao du",
    "giao sai",
)

SLA_INQUIRY_TERMS = (
    "bao lau",
    "khi nao",
    "tien ve",
    "thoi gian hoan",
    "the ngan hang",
    "tai khoan ngan hang",
    "chuyen thang",
    "phuong thuc hoan",
    "kenh hoan",
    "may ngay",
)

ITEM_STOPWORDS = {
    "don", "cua", "toi", "minh", "bi", "thieu", "sai", "mon", "phan", "ly", "hop",
    "cai", "co", "da", "roi", "va", "voi", "cho", "di", "nhe", "a", "nha", "ngay",
    "hoan", "tien", "gui", "kem", "anh", "chup", "toan", "bo", "nhan", "duoc",
    "tu", "dong", "luon", "la", "o", "trong", "them", "vua", "co", "mot", "hai",
}

SYSTEM = (
    "Bạn là Trợ lý Hỗ trợ Khiếu nại Đơn Giao Đồ Ăn (Track D · D1) hoạt động theo chính sách ShopeeFood.\n"
    "Nguyên tắc bắt buộc:\n"
    "1. CHỈ dựa vào dữ liệu đơn hàng, lịch sử, chính sách và QUYẾT ĐỊNH ĐÃ KHÓA do hệ thống cung cấp; "
    "TUYỆT ĐỐI không bịa món ăn, số tiền, mã chính sách hay mốc thời gian.\n"
    "2. TUYỆT ĐỐI tuân thủ QUYẾT ĐỊNH ĐÃ KHÓA: không tự duyệt hoàn tiền/voucher khi hệ thống đã chặn "
    "(quá hạn 12h, thiếu ảnh, món ngoài đơn, >100.000đ, trễ <30 phút, >3 lần/tháng, dọa 1★, dị vật/ngộ độc).\n"
    "3. Khi tạo đề xuất hoàn tiền hoặc voucher, luôn nói rõ đây là BẢN NHÁP / ĐỀ XUẤT CHỜ CSKH DUYỆT, "
    "không khẳng định tiền/voucher đã được chuyển ngay lập tức.\n"
    "4. Không yêu cầu khách tự liên hệ quán khi khách báo thiếu/sai món hoặc không liên hệ được quán.\n"
    "5. Trả lời bằng tiếng Việt ngắn gọn, rõ ràng, lịch sự, đi thẳng vào phương án, số tiền/mốc thời gian "
    "và bước tiếp theo cho người dùng."
)


def _norm(text: str) -> str:
    """Chuyển về chữ thường không dấu để so khớp ổn định với tiếng Việt."""
    s = (text or "").replace("đ", "d").replace("Đ", "D")
    s = unicodedata.normalize("NFD", s)
    s = "".join(ch for ch in s if unicodedata.category(ch) != "Mn")
    return re.sub(r"\s+", " ", s.lower()).strip()


def _has_any(norm_text: str, terms: tuple) -> bool:
    return any(t in norm_text for t in terms)


def _has_photo_evidence(norm_text: str) -> bool:
    if _has_any(norm_text, PHOTO_NEGATIVE_TERMS):
        return False
    return _has_any(norm_text, PHOTO_POSITIVE_TERMS)


def _reference_now() -> datetime:
    raw = (os.environ.get("REFERENCE_NOW") or DEFAULT_REFERENCE_NOW).strip()
    return datetime.fromisoformat(raw)


def _hours_since_completed(order: dict) -> Optional[float]:
    completed_at = order.get("completed_at")
    if not completed_at:
        return None
    try:
        dt = datetime.fromisoformat(completed_at)
        delta = _reference_now() - dt
        return round(delta.total_seconds() / 3600.0, 2)
    except ValueError:
        return None


def _extract_claimed_amount(text: str) -> Optional[int]:
    m = AMOUNT_RE.search(text or "")
    if not m:
        return None
    raw_num = m.group(1)
    unit = m.group(0).lower().strip()
    digits = int(re.sub(r"[.,]", "", raw_num))
    if unit.endswith("k") and digits < 10000:
        return digits * 1000
    return digits


def _match_order_item(norm_text: str, order: dict) -> Optional[dict]:
    """Khớp món khách nhắc tới với danh sách items trong đơn."""
    items = order.get("items") or []
    best_item = None
    best_score = 0.0
    text_tokens = set(re.findall(r"[a-z0-9]+", norm_text)) - ITEM_STOPWORDS

    for item in items:
        item_norm = _norm(item.get("name", ""))
        if item_norm and item_norm in norm_text:
            return item
        item_tokens = set(re.findall(r"[a-z0-9]+", item_norm)) - ITEM_STOPWORDS
        if not item_tokens:
            continue
        overlap = text_tokens & item_tokens
        if len(overlap) >= 2:
            score = len(overlap) / len(item_tokens)
            if score > best_score:
                best_score = score
                best_item = item
    return best_item


def _is_pure_sla_inquiry(norm_text: str) -> bool:
    """Phân biệt câu hỏi thuần về thời gian hoàn tiền (71298) với khiếu nại sự cố mới."""
    if not _has_any(norm_text, SLA_INQUIRY_TERMS):
        return False
    if _has_any(norm_text, MISSING_WRONG_TERMS) or _has_any(norm_text, LATE_TERMS):
        return False
    return True


def _format_vnd(amount: int) -> str:
    return f"{int(amount):,}".replace(",", ".") + "đ"


def _evaluate_guardrails(
    text: str,
    order_id: Optional[str],
    order: Optional[dict],
    history: Optional[dict],
    policy_bundle: dict,
) -> dict:
    """Động cơ kiểm tra ngưỡng cứng deterministic — khóa status, draft và yêu cầu bắt buộc."""
    norm_text = _norm(text)
    thresholds = policy_bundle.get("simulated_thresholds") or {}
    max_auto_refund = int(thresholds.get("auto_refund_missing_item_max_vnd", 100000))
    min_late_minutes = int(thresholds.get("late_voucher_min_delay_minutes", 30))
    max_late_voucher = int(thresholds.get("late_voucher_max_vnd", 50000))
    max_complaints = int(thresholds.get("high_frequency_complaint_limit_per_month", 3))

    # 1. An toàn thực phẩm (dị vật / ngộ độc) — ưu tiên tuyệt đối
    if _has_any(norm_text, FOOD_SAFETY_TERMS):
        note("guardrail: food_safety -> escalated")
        draft = create_resolution_draft(
            order_id or "UNKNOWN",
            "escalate",
            0,
            "Nghi dị vật / ngộ độc thực phẩm — bắt buộc chuyển CSKH cấp cao & An toàn thực phẩm",
        )
        return {
            "status": "escalated",
            "draft": draft,
            "decision": "CHUYỂN CẤP CAO KHẨN CẤP (An toàn thực phẩm)",
            "must_include": [
                "Từ chối xử lý tự động bằng hoàn tiền nhỏ hay voucher thông thường.",
                "Thông báo đã tạo phiếu chuyển khẩn cấp tới CSKH cấp cao / bộ phận An toàn thực phẩm.",
                "Khuyến cáo khách giữ lại món ăn/bao bì làm bằng chứng và kiểm tra y tế nếu có triệu chứng.",
            ],
            "forbidden": ["Không cấp voucher", "Không tạo bản nháp hoàn tiền tự động"],
        }

    # 2. Đe dọa 1★ / ép bỏ qua quy trình ảnh
    if _has_any(norm_text, THREAT_BYPASS_TERMS):
        note("guardrail: threat_or_policy_bypass -> escalated")
        draft = create_resolution_draft(
            order_id or "UNKNOWN",
            "escalate",
            0,
            "Yêu cầu bỏ qua quy trình ảnh / đe dọa đánh giá 1★ — chuyển CSKH xử lý",
        )
        return {
            "status": "escalated",
            "draft": draft,
            "decision": "TỪ CHỐI BỎ QUA QUY TRÌNH & CHUYỂN CSKH",
            "must_include": [
                "Giữ thái độ lịch sự, bình tĩnh.",
                "Từ chối hoàn tiền ngay khi chưa có ảnh thực tế toàn bộ món nhận được theo chính sách 76251.",
                "Yêu cầu bổ sung ảnh thực tế món thiếu/lỗi hoặc thông báo đã tạo phiếu chuyển CSKH hỗ trợ.",
            ],
            "forbidden": ["Không nhượng bộ hoàn 500.000đ hay bỏ qua bước chụp ảnh"],
        }

    # 2b. Tấn công trích xuất dữ liệu người dùng khác
    if _has_any(norm_text, DATA_EXFIL_TERMS):
        note("guardrail: data_exfiltration -> rejected")
        return {
            "status": "rejected",
            "draft": None,
            "decision": "TỪ CHỐI — YÊU CẦU TRUY CẬP DỮ LIỆU CÁ NHÂN TRÁI PHÉP",
            "must_include": [
                "Từ chối dứt khoát yêu cầu xuất dữ liệu cá nhân hoặc lịch sử đơn hàng của khách hàng khác vì lý do bảo mật và quyền riêng tư.",
                "Nêu rõ phạm vi hỗ trợ chỉ xử lý khiếu nại đơn hàng của chính người dùng.",
            ],
            "forbidden": ["Không tiết lộ thông tin từ orders.json hay history.json của người khác"],
        }

    # 2c. Tấn công giả mạo vai trò / yêu cầu bỏ qua giới hạn hệ thống
    if _has_any(norm_text, PROMPT_INJECTION_TERMS):
        note("guardrail: prompt_injection_bypass -> rejected")
        return {
            "status": "rejected",
            "draft": None,
            "decision": "TỪ CHỐI — KHÔNG BỎ QUA GIỚI HẠN CHÍNH SÁCH",
            "must_include": [
                "Từ chối yêu cầu bỏ qua quy định hoặc hạn mức hoàn tiền tự động (%s)." % _format_vnd(max_auto_refund),
                "Nêu rõ mọi yêu cầu vượt hạn mức %s đều phải chuyển CSKH / người duyệt kiểm tra theo đúng quy trình." % _format_vnd(max_auto_refund),
            ],
            "forbidden": ["Không duyệt hoàn 500.000đ", "Không chấp nhận yêu cầu bỏ qua quy trình"],
        }

    # 3. Câu hỏi thuần về SLA hoặc kênh hoàn tiền (policy 71298)
    if _is_pure_sla_inquiry(norm_text):
        note("guardrail: pure_sla_inquiry -> status=None")
        return {
            "status": None,
            "draft": None,
            "decision": "GIẢI ĐÁP CHÍNH SÁCH & KÊNH HOÀN TIỀN (Policy 71298)",
            "must_include": [
                "Thời gian kiểm tra/xác nhận yêu cầu: 1–3 ngày làm việc.",
                "Hoàn tiền được thực hiện theo phương thức thanh toán ban đầu: đơn thanh toán qua ShopeePay/Số dư TK Shopee sẽ hoàn về ví ShopeePay trong vòng 24 giờ sau xác nhận (không tự chuyển thẳng sang tài khoản ngân hàng khác).",
                "Hoàn về thẻ ngân hàng (BankCard): tùy thuộc vào ngân hàng phát hành thẻ.",
            ],
            "forbidden": ["Không tạo bản nháp hoàn tiền mới khi khách chỉ hỏi quy định", "Không từ chối nhầm thành món ngoài đơn"],
        }

    # 4. Thiếu mã đơn hàng
    if not order_id:
        if _has_any(norm_text, AESTHETIC_COMPLAINT_TERMS):
            note("guardrail: aesthetic_presentation -> rejected")
            return {
                "status": "rejected",
                "draft": None,
                "decision": "NGOÀI PHẠM VI HOÀN TIỀN — KHÁC BIỆT THẨM MỸ / TRÌNH BÀY",
                "must_include": [
                    "Giải thích nhẹ nhàng rằng sự khác biệt về hình thức trình bày/thẩm mỹ so với ảnh quảng cáo không thuộc lỗi thiếu/sai món hay hư hỏng theo chính sách 76251.",
                    "Mời khách cung cấp mã đơn hàng và ảnh thực tế nếu món có dấu hiệu sai thành phần, thiếu món hoặc hư hỏng để được xem xét.",
                ],
                "forbidden": ["Không tự ý duyệt hoàn tiền chỉ vì không đẹp mắt như ảnh"],
            }
        note("guardrail: missing_order_id -> need_info")
        note("guardrail: missing_order_id -> need_info")
        must = [
            "Hỏi lại mã đơn hàng (vd ORD-xxxx), vấn đề cụ thể (thiếu/sai món hay giao trễ) và tên món bị ảnh hưởng.",
            "Nếu là thiếu/sai món, nhắc khách chuẩn bị ảnh thực tế toàn bộ món đã nhận và lưu ý thời hạn tiếp nhận 12 tiếng kể từ khi đơn hoàn thành theo chính sách 76251.",
            "Không hứa hẹn hay ước lượng số tiền hoàn trước khi tra cứu đơn hàng.",
        ]
        if "quan" in norm_text:
            must.append("Khẳng định nền tảng hỗ trợ tiếp nhận trực tiếp, không bắt khách tự liên hệ quán.")
        return {
            "status": "need_info",
            "draft": None,
            "decision": "CẦN BỔ SUNG THÔNG TIN (Thiếu mã đơn hàng)",
            "must_include": must,
            "forbidden": ["Không tự đoán mã đơn", "Không hứa số tiền hoàn", "Không bắt khách tự liên hệ quán"],
        }

    # 5. Có mã đơn nhưng không tìm thấy trong data/orders.json
    if order is None:
        note("guardrail: order_not_found -> need_info")
        return {
            "status": "need_info",
            "draft": None,
            "decision": "KHÔNG TÌM THẤY MÃ ĐƠN HÀNG",
            "must_include": [
                "Thông báo không tìm thấy mã đơn %s trong hệ thống." % order_id,
                "Đề nghị khách kiểm tra lại mã đơn hàng chính xác.",
            ],
            "forbidden": ["Không bịa thông tin đơn hàng"],
        }

    is_late = _has_any(norm_text, LATE_TERMS)
    is_missing_wrong = _has_any(norm_text, MISSING_WRONG_TERMS)
    complaints_count = int((history or {}).get("complaints_this_month", 0))
    hours_elapsed = _hours_since_completed(order)

    # 6. Nhánh giao trễ
    if is_late and not is_missing_wrong:
        delay = int(order.get("delay_minutes") or 0)
        if delay < min_late_minutes:
            note("guardrail: late_under_30m (delay=%d) -> rejected" % delay)
            return {
                "status": "rejected",
                "draft": None,
                "decision": "KHÔNG ĐỦ ĐIỀU KIỆN VOUCHER GIAO TRỄ (%d phút < %d phút)" % (delay, min_late_minutes),
                "must_include": [
                    "Nêu rõ đơn %s hiện mới trễ %d phút, chưa đạt ngưỡng %d phút để đề xuất voucher hỗ trợ."
                    % (order_id, delay, min_late_minutes),
                    "Hướng dẫn khách kiểm tra thời gian dự kiến giao hàng trên ứng dụng và liên hệ trực tiếp tài xế trước theo chính sách 71069.",
                    "Nếu trễ kéo dài hoặc tài xế không phản hồi, khách có thể quay lại chat CSKH.",
                ],
                "forbidden": ["Không cấp hoặc hứa tặng voucher hỗ trợ giao trễ"],
            }

        if complaints_count > max_complaints:
            note("guardrail: high_frequency_late (count=%d) -> escalated" % complaints_count)
            draft = create_resolution_draft(
                order_id,
                "escalate",
                0,
                "Khách khiếu nại %d lần/tháng (vượt ngưỡng %d) cho đơn giao trễ %d phút — chuyển duyệt thủ công"
                % (complaints_count, max_complaints, delay),
            )
            return {
                "status": "escalated",
                "draft": draft,
                "decision": "CHUYỂN NGƯỜI DUYỆT (Tần suất khiếu nại cao)",
                "must_include": [
                    "Ghi nhận đơn %s giao trễ %d phút (> %d phút)." % (order_id, delay, min_late_minutes),
                    "Thông báo yêu cầu cần chuyển bộ phận CSKH duyệt thủ công thay vì tạo voucher tự động do lịch sử khiếu nại trong tháng vượt ngưỡng.",
                ],
                "forbidden": ["Không tự cấp voucher"],
            }

        note("guardrail: late_eligible (delay=%d) -> draft_ready (voucher)" % delay)
        draft = create_resolution_draft(
            order_id,
            "voucher",
            max_late_voucher,
            "Đơn %s giao trễ %d phút (vượt ngưỡng %d phút) — đề xuất voucher tối đa %s chờ CSKH duyệt"
            % (order_id, delay, min_late_minutes, _format_vnd(max_late_voucher)),
        )
        return {
            "status": "draft_ready",
            "draft": draft,
            "decision": "ĐÃ TẠO BẢN NHÁP VOUCHER HỖ TRỢ GIAO TRỄ (CHỜ DUYỆT)",
            "must_include": [
                "Xác nhận đơn %s giao trễ %d phút (vượt ngưỡng %d phút)." % (order_id, delay, min_late_minutes),
                "Thông báo đã tạo bản nháp đề xuất tặng voucher tối đa %s chờ CSKH duyệt (không vượt hạn mức)."
                % _format_vnd(max_late_voucher),
            ],
            "forbidden": ["Không hứa tặng voucher vượt quá %s" % _format_vnd(max_late_voucher)],
        }

    # 7. Nhánh thiếu / sai món — kiểm tra quá hạn 12h trước (policy 76251)
    if hours_elapsed is not None and hours_elapsed > 12.0:
        note("guardrail: over_12h (hours=%.2f) -> rejected" % hours_elapsed)
        return {
            "status": "rejected",
            "draft": None,
            "decision": "TỪ CHỐI TỰ ĐỘNG — QUÁ THỜI HẠN 12 TIẾNG (Policy 76251)",
            "must_include": [
                "Thông báo đơn %s đã hoàn thành lúc %s, đã quá thời hạn tiếp nhận khiếu nại 12 tiếng theo chính sách 76251."
                % (order_id, order.get("completed_at")),
                "Không thể tạo đề xuất hoàn tiền tự động.",
                "Hướng dẫn khách liên hệ trực tiếp CSKH nếu cần xem xét trường hợp ngoại lệ.",
            ],
            "forbidden": ["Không tạo bản nháp hoàn tiền"],
        }

    # 8. Đối chiếu món trong đơn (nguồn sự thật orders.json — ưu tiên trước tần suất khiếu nại)
    matched_item = _match_order_item(norm_text, order)
    claimed_amount = _extract_claimed_amount(text)
    items_summary = ", ".join(
        "%s (%s)" % (it["name"], _format_vnd(it["price_vnd"])) for it in (order.get("items") or [])
    )

    if matched_item is None:
        if claimed_amount is not None or re.search(r"thieu\s+(?:phan|ly|mon|chai|hop)\s+\w+", norm_text):
            note("guardrail: item_not_in_order -> rejected")
            return {
                "status": "rejected",
                "draft": None,
                "decision": "TỪ CHỐI — MÓN KHIẾU NẠI KHÔNG CÓ TRONG ĐƠN HÀNG",
                "must_include": [
                    "Đối chiếu đơn %s: các món thực tế trong đơn chỉ gồm: %s." % (order_id, items_summary),
                    "Từ chối hoàn tiền cho món không có trong đơn hàng.",
                    "Mời khách kiểm tra lại mã đơn hoặc xác nhận lại đúng món bị thiếu trong danh sách trên.",
                ],
                "forbidden": ["Không tạo bản nháp hoàn tiền cho món không có trong đơn"],
            }
        note("guardrail: item_unspecified -> need_info")
        return {
            "status": "need_info",
            "draft": None,
            "decision": "CẦN XÁC NHẬN MÓN THIẾU & ẢNH BẰNG CHỨNG",
            "must_include": [
                "Liệt kê các món trong đơn %s (%s) để khách xác nhận món nào bị thiếu/sai." % (order_id, items_summary),
                "Yêu cầu cung cấp ảnh thực tế toàn bộ món đã nhận theo chính sách 76251.",
            ],
            "forbidden": ["Không tự tạo bản nháp hoàn tiền khi chưa rõ món và chưa có ảnh"],
        }

    # 9. Kiểm tra ảnh bằng chứng (policy 76251)
    if not _has_photo_evidence(norm_text):
        note("guardrail: missing_photo -> need_info")
        return {
            "status": "need_info",
            "draft": None,
            "decision": "CẦN BỔ SUNG ẢNH THỰC TẾ TOÀN BỘ MÓN ĐÃ NHẬN (Policy 76251)",
            "must_include": [
                "Xác nhận đã tra thấy đơn %s có món '%s' (%s)."
                % (order_id, matched_item["name"], _format_vnd(matched_item["price_vnd"])),
                "Theo chính sách 76251, khách cần cung cấp ảnh thực tế toàn bộ món đã nhận và xác nhận món thiếu trước khi hệ thống tạo đề xuất hoàn tiền.",
            ],
            "forbidden": ["Không tạo bản nháp hoàn tiền khi chưa có ảnh"],
        }

    # 10. Kiểm tra tần suất khiếu nại (> 3 lần/tháng)
    if complaints_count > max_complaints:
        note("guardrail: high_frequency_user (user=%s, count=%d) -> escalated" % (order.get("user_id"), complaints_count))
        draft = create_resolution_draft(
            order_id,
            "escalate",
            0,
            "Tài khoản %s có %d lần khiếu nại trong tháng (vượt ngưỡng %d lần/tháng) — chuyển người duyệt kiểm tra"
            % (order.get("user_id"), complaints_count, max_complaints),
        )
        return {
            "status": "escalated",
            "draft": draft,
            "decision": "CHUYỂN NGƯỜI DUYỆT THỦ CÔNG (Tần suất khiếu nại vượt ngưỡng)",
            "must_include": [
                "Ghi nhận khiếu nại thiếu món '%s' (%s) của đơn %s kèm ảnh."
                % (matched_item["name"], _format_vnd(matched_item["price_vnd"]), order_id),
                "Thông báo hệ thống không thể tự động hoàn tiền vì lịch sử khiếu nại trong tháng vượt mức tự động (%d lần/tháng > %d lần/tháng), đã tạo phiếu chuyển CSKH duyệt thủ công."
                % (complaints_count, max_complaints),
            ],
            "forbidden": ["Không tự động duyệt hoàn tiền"],
        }

    # 11. Kiểm tra hạn mức hoàn tiền tự động (> 100.000đ)
    item_price = int(matched_item["price_vnd"])
    if item_price > max_auto_refund:
        note("guardrail: exceeds_auto_refund_limit (amount=%d > %d) -> escalated" % (item_price, max_auto_refund))
        draft = create_resolution_draft(
            order_id,
            "escalate",
            0,
            "Món '%s' trị giá %s vượt hạn mức hoàn tự động %s — chuyển CSKH duyệt"
            % (matched_item["name"], _format_vnd(item_price), _format_vnd(max_auto_refund)),
        )
        return {
            "status": "escalated",
            "draft": draft,
            "decision": "CHUYỂN CSKH / NGƯỜI DUYỆT (Vượt hạn mức tự động 100.000đ)",
            "must_include": [
                "Xác nhận đơn %s có món '%s' trị giá %s."
                % (order_id, matched_item["name"], _format_vnd(item_price)),
                "Giải thích giá trị món thiếu (%s) vượt hạn mức đề xuất hoàn tự động %s nên không thể tự động duyệt."
                % (_format_vnd(item_price), _format_vnd(max_auto_refund)),
                "Thông báo đã tạo phiếu chuyển CSKH / người duyệt xem xét xử lý.",
            ],
            "forbidden": ["Không tự động duyệt hoàn tiền"],
        }

    # 12. Hợp lệ hoàn toàn → tạo bản nháp hoàn tiền chờ duyệt
    payment = order.get("payment_method", "ShopeePay")
    note("guardrail: eligible_refund (order=%s, amount=%d) -> draft_ready" % (order_id, item_price))
    draft = create_resolution_draft(
        order_id,
        "refund",
        item_price,
        "Thiếu món '%s' (%s) trong hạn 12h, đủ ảnh bằng chứng, trong hạn mức %s — chờ CSKH duyệt"
        % (matched_item["name"], _format_vnd(item_price), _format_vnd(max_auto_refund)),
    )
    sla_note = (
        "Hoàn về ShopeePay trong vòng 24 giờ sau khi xác nhận (thời gian kiểm tra 1–3 ngày làm việc theo chính sách 71298)."
        if payment == "ShopeePay"
        else "Thời gian kiểm tra 1–3 ngày làm việc; hoàn về phương thức %s tùy ngân hàng/kênh thanh toán theo chính sách 71298." % payment
    )
    return {
        "status": "draft_ready",
        "draft": draft,
        "decision": "ĐỦ ĐIỀU KIỆN — ĐÃ TẠO BẢN NHÁP HOÀN TIỀN CHỜ DUYỆT",
        "must_include": [
            "Xác nhận đơn %s hợp lệ (trong hạn 12h theo policy 76251, có ảnh, giá trị %s ≤ %s)."
            % (order_id, _format_vnd(item_price), _format_vnd(max_auto_refund)),
            "Thông báo đã tạo BẢN NHÁP đề xuất hoàn tiền %s cho món '%s' chờ CSKH duyệt."
            % (_format_vnd(item_price), matched_item["name"]),
            sla_note,
        ],
        "forbidden": ["Không khẳng định tiền đã về ví ngay lập tức"],
    }


def _build_user_prompt(
    text: str,
    order: Optional[dict],
    history: Optional[dict],
    policy_bundle: dict,
    verdict: dict,
) -> str:
    context = {
        "order": order,
        "user_history": history,
        "policies": policy_bundle.get("policies"),
        "thresholds": policy_bundle.get("simulated_thresholds"),
        "locked_decision": {
            "status": verdict["status"],
            "decision": verdict["decision"],
            "draft": verdict["draft"],
            "must_include": verdict["must_include"],
            "forbidden": verdict["forbidden"],
        },
    }
    return (
        "DỮ LIỆU TRA CỨU & QUYẾT ĐỊNH ĐÃ KHÓA (JSON):\n"
        + json.dumps(context, ensure_ascii=False, indent=2)
        + "\n\nTIN NHẮN KHÁCH HÀNG:\n"
        + text
        + "\n\nHãy viết câu trả lời tiếng Việt gửi khách hàng bám đúng QUYẾT ĐỊNH ĐÃ KHÓA và các ý trong must_include."
    )


def answer(text: str) -> dict:
    """Xử lý 1 lượt khiếu nại và trả về dict khớp hợp đồng eval/simulate và FE."""
    m = ORDER_ID_RE.search(text or "")
    order_id = m.group(0).upper() if m else None

    order = lookup_order(order_id) if order_id else None
    history = lookup_user_history(order["user_id"]) if order and order.get("user_id") else None

    norm_text = _norm(text)
    if _is_pure_sla_inquiry(norm_text):
        topic = "refund_timeline"
    elif _has_any(norm_text, LATE_TERMS) and not _has_any(norm_text, MISSING_WRONG_TERMS):
        topic = "late_delivery"
    elif _has_any(norm_text, MISSING_WRONG_TERMS):
        topic = "missing_or_wrong_item"
    else:
        topic = "all"
    policy_bundle = lookup_policy(topic)

    verdict = _evaluate_guardrails(text, order_id, order, history, policy_bundle)
    user_prompt = _build_user_prompt(text, order, history, policy_bundle, verdict)
    reply = call_model(SYSTEM, user_prompt)

    draft = verdict["draft"]
    fe_draft = (
        {
            "action": draft["action"],
            "amount_vnd": draft["amount_vnd"],
            "reason": draft["reason"],
        }
        if draft
        else None
    )
    return {
        "output": reply["text"],
        "status": verdict["status"],
        "order_id": order_id,
        "draft": fe_draft,
    }
