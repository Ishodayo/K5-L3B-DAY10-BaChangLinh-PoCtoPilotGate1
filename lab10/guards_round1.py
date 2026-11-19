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
"""
from . import helpers as H
from .tools import Verdict


def pre_guard(ctx):
    # Cổng 1: Ghim phiên bản chính sách đang có hiệu lực theo ngày ctx.as_of (tránh đọc cờ index_active sai)
    policies = ctx.tools.lookup_policies()
    eff = H.effective_policy(policies, ctx.as_of)
    if eff:
        return Verdict.allow(policy_id=eff["policy_id"])
    return Verdict.allow()


def write_gate(ctx, action):
    tool = action.get("tool")

    if tool == "issue_refund":
        order_id = action.get("order_id")

        # Cổng phòng chống hoàn trùng lặp: kiểm tra sổ cái
        if ctx.tools.ledger_rows(order_id=order_id):
            return Verdict.deny("Đơn hàng đã được hoàn tiền trong sổ cái")

        # Cổng kiểm tra quyền lợi thực tế từ tracking DB (chống model_override tin lời khách khai)
        order = ctx.tools.lookup_order(order_id)
        if order:
            policies = ctx.tools.lookup_policies()
            policy = H.effective_policy(policies, ctx.as_of)
            if policy:
                parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
                db_delay = H.db_delay_days(parcel, ctx.as_of)
                cause = parcel.get("delay_cause") or ("CARRIER" if db_delay > 0 else None)
                entitled = H.entitlement_vnd(policy, order, db_delay, cause)

                # Kiểm tra phê duyệt nếu có: phải đúng mã order_id
                appr_id = action.get("approval_id")
                if appr_id:
                    apprs = ctx.tools.lookup_approvals(approval_id=appr_id)
                    if apprs and apprs[0].get("order_id") and apprs[0]["order_id"] != order_id:
                        return Verdict.deny("Phê duyệt không thuộc về đơn hàng này")

                # Nếu không có phê duyệt đặc biệt và số tiền đề xuất lệch với quyền lợi thực tế
                if not appr_id and action.get("amount_vnd", 0) != entitled:
                    if entitled <= 0:
                        return Verdict.deny("Đơn chưa đủ điều kiện hoàn tiền theo tracking DB")
                    return Verdict.modify("Sửa số tiền hoàn về đúng quyền lợi theo tracking DB", amount_vnd=entitled)

    elif tool == "file_carrier_fault":
        order_id = action.get("order_id")
        order = ctx.tools.lookup_order(order_id)
        if order:
            policies = ctx.tools.lookup_policies()
            policy = H.effective_policy(policies, ctx.as_of)
            if policy:
                parcel = H.ticket_parcel(order, ctx.ticket, ctx.as_of)
                db_delay = H.db_delay_days(parcel, ctx.as_of)

                # Cổng chặn ghi oan lỗi cho hãng: kiểm tra điều kiện phạt theo chính sách và DB
                if not H.carrier_at_fault(policy, parcel, db_delay):
                    return Verdict.deny("Hãng không có lỗi vi phạm theo chính sách và tracking DB")

                # Cổng gán đúng kiện hàng và hãng vận chuyển của kiện bị trễ thực tế
                if (action.get("parcel_id") != parcel["parcel_id"] or
                        action.get("carrier_id") != parcel["carrier_id"] or
                        action.get("delay_days") != db_delay):
                    return Verdict.modify(
                        "Gán đúng kiện và hãng trễ theo tracking DB",
                        parcel_id=parcel["parcel_id"],
                        carrier_id=parcel["carrier_id"],
                        delay_days=db_delay,
                        driver_id=parcel.get("driver_id")
                    )

    elif tool == "notify_carrier":
        # Cổng bảo vệ dữ liệu cá nhân (PII): không gửi thông tin người nhận quà sang bên thứ ba
        payload = action.get("payload")
        if isinstance(payload, dict) and "recipient_contact" in payload:
            new_payload = dict(payload)
            new_payload.pop("recipient_contact", None)
            return Verdict.modify("Loại bỏ thông tin liên hệ người nhận quà", payload=new_payload)

    return Verdict.allow()
