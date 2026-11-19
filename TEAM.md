# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): BaChangLinh
- Lớp: `L3B`
- Repo của bàn: `K5-L3B-DAY10-BaChangLinh-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8):

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

## HoVaTen-MSSV

### Phần việc phụ trách

Vai trong bàn; câu nào của đề, mục nào của phiếu A/B/C, file nào (`lab10/guards.py`, `config/operating_gates.json`, …).

### Đóng góp cụ thể

...

### Bằng chứng

Mã commit, mã lần chạy (`runs/<mã>`), dòng trong phiếu.

### Exit ticket

Một điều học được, một điều còn chưa chắc.

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
