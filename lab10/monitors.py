"""★ FILE ĐỘI SỬA (2/3): chỉ số theo dõi (monitor). Thêm ÍT NHẤT MỘT chỉ số bắt được sự cố của bàn.

Mỗi monitor nhận danh sách trial (KHÔNG có nhãn đúng/sai, giống production) và trả về một số.
Một trial = {"ticket_id", "seed", "day", "status", "amount_vnd", "ticket", "events", "ledger", "faults", "outbound",
             "arrive_min", "warehouse", "cost_vnd", "review_kind", "queue_wait_min", "queue_stuck"}
  "day"            một ngày vận hành giả lập: các ticket cùng "day" và cùng "seed" chạy nối nhau trên cùng một sổ cái
  "arrive_min"     phút ticket tới trong ca (0..480)          "warehouse"   kho của đơn
  "cost_vnd"       tiền LLM + nền tảng đã tốn cho ticket      "review_kind" None / "escalated" (trợ lý chuyển người) /
  "queue_wait_min" số phút chờ người duyệt (None nếu không vào hàng chờ)     "recheck" (nhân viên tự kiểm lại)
Chỉ số có thể là kỹ thuật (tỉ lệ model đè số trong ticket lên DB), vận hành (số ca cần người trong giờ đông nhất),
hay kinh doanh (tỉ lệ ticket trợ lý đọc xong vẫn phải chuyển người).

lab10.grade kiểm: monitor chạy không lỗi, và giá trị trên gói sự cố khác giá trị trên bộ nền,
tức là monitor "sáng đèn" khi sự cố xảy ra.
"""


def escalation_rate(trials):
    return sum(t["status"] == "escalated" for t in trials) / max(1, len(trials))

def monitor_carrier_notice_sanitized_rate(trials: list[dict]) -> float:
    """Tỷ lệ lệnh gửi hãng chỉ chứa bốn trường hợp đồng cho phép."""
    total_notices = 0
    sanitized_notices = 0
    allowed = {"order_id", "parcel_id", "district", "delay_days"}
    for t in trials:
        for step in t.get("events", []):
            if step.get("type") == "tool" and step.get("tool") == "notify_carrier":
                total_notices += 1
                payload = step.get("payload")
                if isinstance(payload, dict) and set(payload) == allowed:
                    sanitized_notices += 1
    if total_notices == 0:
        return 1.0
    return round(sanitized_notices / total_notices, 4)


def recipient_contact_block_rate(trials: list[dict]) -> float:
    """Tỷ lệ ticket có nhánh người nhận bị cổng gỡ khỏi bản tin gửi hãng."""
    blocked = sum(
        any(
            event.get("type") == "guard"
            and event.get("kind") == "carrier_notice_removed_fields"
            and "recipient_contact" in event.get("fields", ())
            for event in trial.get("events", ())
        )
        for trial in trials
    )
    return round(blocked / max(1, len(trials)), 4)

MONITORS = {
    "escalation_rate": escalation_rate,     # có sẵn; KHÔNG tính là metric mới của đội
}
STARTER_MONITORS = ("escalation_rate",)
MONITORS["carrier_notice_sanitized_rate"] = monitor_carrier_notice_sanitized_rate
MONITORS["recipient_contact_block_rate"] = recipient_contact_block_rate
