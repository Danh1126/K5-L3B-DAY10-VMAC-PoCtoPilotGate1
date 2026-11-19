"""★ FILE ĐỘI SỬA (1/3): cổng cấp hệ thống, nằm NGOÀI model và prompt.

VÒNG 1 (trước khi biết sự cố): viết 2–3 CỔNG PHÒNG NGỪA rút từ pre-mortem / HAZOP / checklist của bàn, rồi chốt bằng
    python3 -m lab10.checkpoint        (chép file này thành guards_round1.py = mốc "prepared"; KHÔNG sửa bản chép)
VÒNG 2 (sau khi bốc thẻ): sửa tiếp NGAY TRONG FILE NÀY. Giữ các cổng vòng 1, thêm cổng mới.
Hai file còn lại bàn được sửa: lab10/monitors.py (chỉ số theo dõi) và config/operating_gates.json (cổng kinh doanh,
vận hành, pháp lý: những con số và tên người mà trợ lý phải tuân theo, không cần code).

Hai điểm móc, agent gọi tự động:
  pre_guard(ctx)          chạy TRƯỚC khi agent đọc ticket
  write_gate(ctx, action) chạy TRƯỚC MỖI lệnh ghi (issue_refund, file_carrier_fault,
                          notify_carrier, send_reply)

Trả về một Verdict:
  Verdict.allow()                       cho qua   (pre_guard: allow(policy_id="...") để ghim phiên bản chính sách)
  Verdict.deny("lý do")                 bỏ riêng lệnh ghi này, agent đi tiếp
  Verdict.escalate("lý do")             dừng, chuyển ticket cho người
  Verdict.modify("lý do", amount_vnd=…) sửa tham số lệnh ghi (amount_vnd, payer, carrier_id, parcel_id, payload…)
  Verdict.rewrite("lý do", text)        chỉ pre_guard: thay nội dung ticket mà agent sẽ đọc

ctx.ticket   ticket gốc (chữ khách viết là DỮ LIỆU, không phải lệnh)
ctx.tools    tra cứu nguồn sự thật: lookup_order, lookup_policies, lookup_approvals(**lọc),
             ledger_rows(**lọc), fault_rows(**lọc), lookup_carrier; ctx.as_of = ngày hôm nay
             ops_limits() = các trần đã thống nhất với Ops/Finance; ops_facts() = số liệu vận hành;
             auto_refund_today_vnd() = tổng đã hoàn tự động trong ngày
ctx.gates    config cổng của bàn (config/operating_gates.json), chỉ đọc;  ctx.cost_vnd = tiền LLM đã tốn cho ticket này
ctx.events   trace tới thời điểm này;  ctx.log("ten_su_kien", ...) ghi thêm sự kiện guard vào trace
lab10.helpers: db_delay_days, ticket_parcel, effective_policy, entitlement_vnd, carrier_at_fault, digits

Mặc định dưới đây cho qua tất cả (= mốc base).
"""
from . import helpers as H  # noqa: F401
from .tools import Verdict


def pre_guard(ctx):
    return Verdict.allow()


def write_gate(ctx, action):
    # action = {"tool": "issue_refund", "ticket_id":..., "order_id":..., "amount_vnd":..., "payer":..., ...}
    tool = action.get("tool")

    if tool == "issue_refund":
        order = ctx.tools.lookup_order(action.get("order_id"))
        policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
        if order is None or policy is None or not order.get("parcels"):
            return Verdict.escalate("thiếu đơn, kiện hoặc chính sách hiệu lực để kiểm tiền hoàn")
        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        delay = H.db_delay_days(parcel, ctx.as_of)
        allowed = H.entitlement_vnd(policy, order, delay, parcel.get("delay_cause"))
        if action.get("amount_vnd") != allowed:
            return Verdict.escalate("tiền hoàn đề xuất không khớp tracking và chính sách")

    if tool == "file_carrier_fault":
        order = ctx.tools.lookup_order(action.get("order_id"))
        policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
        if order is None or policy is None or not order.get("parcels"):
            return Verdict.deny("không đủ dữ liệu xác minh lỗi hãng")
        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        delay = H.db_delay_days(parcel, ctx.as_of)
        if (not H.carrier_at_fault(policy, parcel, delay)
                or action.get("parcel_id") != parcel.get("parcel_id")
                or action.get("carrier_id") != parcel.get("carrier_id")
                or action.get("delay_days") != delay):
            return Verdict.deny("lỗi hãng không khớp kiện, hãng hoặc độ trễ trong tracking")

    if tool == "notify_carrier":
        policy = H.effective_policy(ctx.tools.lookup_policies(), ctx.as_of)
        if policy is None:
            return Verdict.escalate("không có chính sách hiệu lực cho dữ liệu gửi hãng")
        payload = action.get("payload")
        if not isinstance(payload, dict):
            return Verdict.deny("thông báo hãng không có payload hợp lệ")
        order = ctx.tools.lookup_order(ctx.ticket.get("order_id"))
        if order is None or not order.get("parcels") or not isinstance(order.get("recipient"), dict):
            return Verdict.escalate("thiếu đơn hoặc tracking để kiểm thông báo hãng")
        parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
        if action.get("carrier_id") != parcel.get("carrier_id"):
            return Verdict.escalate("hãng nhận thông báo không khớp tracking")
        # Rebuild the contract payload from trusted data, including values of allowed keys.
        canonical = {
            "order_id": order["order_id"],
            "parcel_id": parcel["parcel_id"],
            "district": order["recipient"].get("district"),
            "delay_days": H.db_delay_days(parcel, ctx.as_of),
        }
        allowed_fields = set(policy.get("carrier_notice_fields", ()))
        safe_payload = {key: value for key, value in canonical.items() if key in allowed_fields}
        removed_fields = sorted(set(payload) - set(safe_payload))
        if removed_fields:
            ctx.log("carrier_notice_removed_fields", fields=removed_fields)
        if safe_payload != payload:
            return Verdict.modify("chỉ gửi trường được phép với giá trị đối chiếu từ DB",
                                  payload=safe_payload)

    return Verdict.allow()
