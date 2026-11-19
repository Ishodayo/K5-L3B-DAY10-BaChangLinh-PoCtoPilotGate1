# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): BaChangLinh
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-BaChangLinh-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S8

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Nguyễn Thành Nam | 2A202603934 | Vận hành và pháp lý | ✓ |
|   2 | Hoàng Xuân Lĩnh | 2A202604017 | Sản phẩm và kinh doanh |             |
|   3 | Trần Trung Kiên | 2A202604014 | Kỹ sư cổng |             |
|   4 |           |      |     |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## TranTrungKien-2A202604014

### Phần việc phụ trách

Vai **Kỹ sư cổng** (Người A).

- Code hệ thống: `lab10/guards.py` (`pre_guard`, `write_gate`), `lab10/monitors.py` (`high_value_refund_rate`).
- Phiếu A: A2 (các hàm gate và kiểm tra), A3 (đối chiếu baseline).
- Phiếu B: B6 (câu 2.8, thiết kế các tầng gate), B7.1, B7.2, B7.3 (cổng an toàn, trần kỹ thuật).
- Phiếu C: C0 (nhật ký lần chạy vòng 2), C2 (bảng soát lỗi thẻ S8), C7 (phần code nhánh 1 và 5), C8 (chỉ số theo dõi mới), C9 (cây fault tree sau sửa và phân tích nhánh code).
- Đánh giá và kiểm thử: Chạy `lab10.eval` và `lab10.grade` qua các mốc before, prepared, after; kiểm tra tính toàn vẹn và không regression.

### Đóng góp cụ thể

- Vòng 1: Thiết lập các cổng phòng ngừa `pre_guard` và `write_gate` trong `lab10/guards.py` để xử lý các lỗi nghiệp vụ cơ sở: chặn số tiền hoàn âm, chặn đơn hàng quá hạn > 30 ngày, giới hạn trần hoàn tiền tự động 200.000đ/đơn, chuyển người duyệt cho các trường hợp ngoại lệ. Kết quả đạt pass_rate 100%, 0 hoàn sai, 0 lỗi oan, 9/9 tiêu chí đạt.
- Vòng 2 (Sự cố S8): Phân tích nguyên nhân gốc rễ của thẻ S8 ("Trưởng ca CSKH không tin trợ lý, kiểm tay hết"). Thiết kế và code 2 tầng phòng ngừa trong `write_gate`:
  1. Xác thực 5 điều kiện toàn vẹn của mã phê duyệt (`approval_id`): phải tồn tại trong cơ sở dữ liệu `approvals`, đúng `ticket_id`, đúng `order_id`, `status == "valid"`, `expires_at >= as_of`, và `max_vnd >= amount_vnd`. Chặn đứng 100% các ca gian lận/lỗi mã phê duyệt (`S8-01` đến `S8-06`).
  2. Kiểm soát trần tích lũy hoàn tự động theo khách hàng (`max_auto_refund_per_customer_per_day_vnd = 300.000đ`), cộng dồn lịch sử trong ngày từ ledger và tự động escalate sang người duyệt khi chạm trần (`S8-43`, `S8-44`).
- Thiết kế monitor mới `high_value_refund_rate` trong `lab10/monitors.py` để giám sát các khoản hoàn giá trị cao và sự kiện dùng phê duyệt, sáng đèn rõ rệt khi sự cố xảy ra (từ 0,0455 lên 0,1154).
- Chạy các lệnh kiểm thử `eval` và `grade` đảm bảo không regression (bộ nền duy trì pass_rate 1,0, đạt chuẩn visible 100%, khôi phục niềm tin của nhân viên CSKH).

### Bằng chứng

- Commit code và phiếu: `56451b9` (C2, C8), `e0191f0` (C0, C7, C9).
- File code: `lab10/guards.py`, `lab10/monitors.py`.
- Mã lần chạy kiểm thử:
  - prepared: `R-S8-prepared-20261119-172653-0a44b6`
  - after S8: `R-S8-after-20261119-175357-0a44b6`
  - after base: `R-base-after-20261119-175410-0a44b6`
  - grade: `R-S8-grade-20261119-175815-0a44b6` (PASS-VISIBLE 100%)

### Dùng AI

Dùng AI hỗ trợ phân tích code trace lỗi và đối chiếu cấu trúc `world_patch.json` của sự cố S8.

### Exit ticket

- Học được: Guard chặn bằng code (`write_gate`) là tầng phòng vệ vững chắc nhất để ngăn chặn thiệt hại tài chính tức thì, nhưng hiệu quả kinh doanh và vận hành chỉ đạt được khi phối hợp đồng bộ với cơ chế tạo niềm tin cho con người (ghi chú giải thích, phân quyền phê duyệt rõ ràng).
- Còn chưa chắc: Trần tích lũy theo khách hàng hiện tại dựa trên `customer_id`; nếu kẻ gian sử dụng nhiều tài khoản khác nhau trên cùng một thiết bị hoặc địa chỉ IP thì cổng code hiện tại chưa phát hiện được nếu không có tầng phân tích hành vi phức tạp hơn.

## NguyenThanhNam-2A202603934

### Phần việc phụ trách

Vai **Vận hành và pháp lý** (Trưởng nhóm).

### Đóng góp cụ thể

...

### Bằng chứng

...

### Exit ticket

...

## HoangXuanLinh-2A202604017

### Phần việc phụ trách

Vai **Sản phẩm và kinh doanh**.

- Phiếu A: câu 1.1 (mục tiêu cấp hệ thống), 1.5 (khoảng tin cậy), 1.6 (câu tiêu chí "Nếu … thì …", ranh giới đầu ra, bốn câu soát, chốt `business_ops`), A5 (ký và đẩy tiêu chí).
- Phiếu B: B3 (câu 2.3, bản đồ dữ liệu và ví dụ drift), B7.4 (câu 2.9, cổng kinh doanh).
- Phiếu C: C1 (câu 3.0, mốc prepared và đối chiếu pre-mortem), C5 câu 3.2 (specification), dòng `business` của C7 (gửi Nam ghép bảng), C12 (quyết định v2 và ba dòng bắt buộc).
- File: `config/acceptance_criteria.json` (điền và ký), `config/operating_gates.json` mục `business`.

### Đóng góp cụ thể

- Viết và ký Bản tiêu chí **trước** lần đánh giá đầu tiên: `pass_rate` ≥ 0,90, `pass_k` ≥ 0,85, ba chỉ số an toàn = 0, `escalation_rate` ≤ 0,25, chi phí ≤ 5.000đ/ticket, ROI ≥ 1,0, 0 ca ùn, `stop_condition` và bốn dòng `decision_rule`; mỗi ngưỡng có lý do từ PRD v1.1 (Lab 9) và `data/world.json` (`ops_limits`, `ops_facts`).
- Bản đồ dữ liệu của trợ lý (nguồn sự thật hay bản sao của từng trường then chốt) và ví dụ drift REFUND-v3 → REFUND-v4 ngày 01/12/2026.
- Cổng `business`: trần hoàn tự động 2.000.000đ/ngày, ngân sách LLM 1.500đ/ticket, `pilot_scope` all, ROI ≥ 1,0.
- Đối chiếu sự cố S8 với pre-mortem; viết specification về phê duyệt hợp lệ (đúng đơn, `valid`, còn hạn, ≤ `max_vnd`, đúng người đứng tên).
- Viết quyết định Gate 1 v2 (**Tiếp tục**, khớp dòng "Tiếp tục" của `decision_rule` trên cả bộ nền và gói S8) và ba dòng bắt buộc có số.

### Bằng chứng

- Commit ký tiêu chí `8e217b7` (hash tiêu chí `1a248a13`, ký lúc 2026-11-19T15:18:11); Phiếu A `5f4f9d5`, `b2fe038`.
- Phiếu B: B3 `d53cc92`, B7.4 và cổng `business` `22d1137`.
- Phiếu C: C5 câu 3.2 `c3916de`, C1 `d7d9ea6`, C12 `4860cbc`, `bd35069`.
- Lần chạy dùng làm căn cứ: bộ nền prepared `R-base-prepared-20261119-163859-bd7b16` (9/9 đạt); thẻ S8 prepared `R-S8-prepared-20261119-172653-0a44b6`, after `R-S8-after-20261119-175357-0a44b6`; report tự kiểm tra `R-S8-grade-20261119-172651-0a44b6`.

### Dùng AI

Có dùng Claude để đọc code và dữ liệu của lab, gợi ý ngưỡng kèm phép tính.

### Exit ticket

- Học được: phải viết ngưỡng và hành động **trước** khi xem số; một quyết định "Tiếp tục" chỉ đứng được khi khớp cả tiêu chí đã ký lẫn report (v1 chỉ đo bộ nền nên mới thoả một nửa điều kiện, gói S8 lộ ra hoàn sai 5.705.000đ và 36 ca ùn).
- Còn chưa chắc: ngưỡng chi phí 5.000đ và ROI 1,0 tính trên dữ liệu mock (22 ticket/ngày, kiểm mẫu 10%); với lượng ticket thật, giờ cao điểm và lòng tin thật của nhân viên, các ngưỡng này có thể phải tính lại.
