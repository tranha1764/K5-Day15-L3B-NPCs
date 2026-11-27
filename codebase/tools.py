"""Công cụ của bài toán D1 (Xử lý khiếu nại đơn giao đồ ăn).

4 công cụ đọc dữ liệu từ data/*.json và tạo bản nháp chờ duyệt:
    1. lookup_order
    2. lookup_user_history
    3. lookup_policy
    4. create_resolution_draft (chỉ tạo bản nháp chờ người duyệt, KHÔNG tác động ra ngoài)
"""
import json
import os
from typing import Optional

from tracing import tool, TOOLS  # noqa: F401

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(ROOT, "data")

VALID_ACTIONS = ("refund", "voucher", "escalate")


def _load_json(filename: str) -> dict:
    path = os.path.join(DATA_DIR, filename)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


@tool
def lookup_order(order_id: str) -> Optional[dict]:
    """lookup_order · Input: order_id (str, vd 'ORD-1001').
    Output: dict thông tin đơn hàng từ data/orders.json hoặc None nếu không tìm thấy.
    Tác động ra ngoài: Không."""
    if not order_id:
        return None
    target = order_id.strip().upper()
    data = _load_json("orders.json")
    for order in data.get("orders", []):
        if str(order.get("order_id", "")).upper() == target:
            return order
    return None


@tool
def lookup_user_history(user_id: str) -> Optional[dict]:
    """lookup_user_history · Input: user_id (str, vd 'USR-001').
    Output: dict lịch sử khiếu nại theo tháng từ data/history.json hoặc None nếu không thấy.
    Tác động ra ngoài: Không."""
    if not user_id:
        return None
    target = user_id.strip().upper()
    data = _load_json("history.json")
    for user in data.get("users", []):
        if str(user.get("user_id", "")).upper() == target:
            return user
    return None


@tool
def lookup_policy(topic: str) -> dict:
    """lookup_policy · Input: topic (str: 'missing_or_wrong_item' | 'late_delivery' | 'refund_timeline' | 'all').
    Output: dict gồm danh sách chính sách khớp và simulated_thresholds từ data/policies.json.
    Tác động ra ngoài: Không."""
    data = _load_json("policies.json")
    policies = data.get("policies", [])
    thresholds = data.get("simulated_thresholds", {})
    key = (topic or "all").strip().lower()
    if key == "all":
        matched = policies
    else:
        matched = [
            p for p in policies
            if p.get("topic", "").lower() == key or str(p.get("id", "")) == key
        ]
        if not matched:
            matched = policies
    return {"policies": matched, "simulated_thresholds": thresholds}


@tool
def create_resolution_draft(
    order_id: str,
    action_type: str,
    amount_vnd: int,
    reason: str,
) -> dict:
    """create_resolution_draft · Input: order_id (str), action_type ('refund'|'voucher'|'escalate'), amount_vnd (int), reason (str).
    Output: dict bản nháp đề xuất chờ CSKH/người duyệt (action, amount_vnd, reason, status='pending_approval').
    Tác động ra ngoài: Không — chỉ tạo bản nháp chờ người duyệt, KHÔNG tự chuyển tiền hay phát hành voucher."""
    action = (action_type or "escalate").strip().lower()
    if action not in VALID_ACTIONS:
        raise ValueError("action_type phải thuộc %s, nhận: %r" % (VALID_ACTIONS, action_type))
    safe_amount = max(0, int(amount_vnd or 0))
    if action == "escalate":
        safe_amount = 0
    clean_order = (order_id or "UNKNOWN").strip().upper()
    return {
        "draft_id": "DRF-%s-%s" % (clean_order, action.upper()),
        "status": "pending_approval",
        "order_id": clean_order,
        "action": action,
        "amount_vnd": safe_amount,
        "reason": (reason or "").strip(),
    }
