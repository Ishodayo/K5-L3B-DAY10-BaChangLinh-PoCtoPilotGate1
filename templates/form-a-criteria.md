# Phiếu A · Tiêu chí và cách đo · Khối 1 (phút 15–65)

**Bàn:** ______ · **Người cầm bút chính:** vai Sản phẩm và kinh doanh (câu 1.3: Kỹ sư cổng; câu 1.2, 1.4: Vận hành và pháp lý)

Điền phiếu này **trước khi chạy trợ lý lần nào**. Viết xong thì chép ngưỡng sang `config/acceptance_criteria.json`, ký ở phút 60–65,
rồi mới chạy đánh giá. Khối 1 không sửa code.

**Mục lục**
- [A1 · Mục tiêu (câu 1.1, 1.2) · phút 15–20](#a1)
- [A2 · Thước đo → Dữ liệu → Cách tính (câu 1.3, 1.4) · phút 20–35](#a2)
- [A3 · Đọc một kết quả có khoảng tin cậy (câu 1.5) · phút 35–40](#a3)
- [A4 · Câu tiêu chí thành công và ranh giới đầu ra (câu 1.6) · phút 40–60](#a4)
- [A5 · Ký và đẩy tiêu chí · phút 60–65](#a5)

---

<a id="a1"></a>

## A1 · Mục tiêu (phút 15–20)

### Câu 1.1 · Một mục tiêu cấp hệ thống (khác "model trả lời đúng")

> …

### Câu 1.2 · Mục tiêu nhìn từ hai người

- Chị Oanh, kế toán đối soát (không dùng trợ lý, nhưng phải khớp sổ với hãng và shop mỗi tuần): cuối mỗi tuần, mọi dòng do trợ lý ghi (tiền hoàn trong sổ cái, lỗi ghi cho hãng, khoản trừ shop) đều truy được về một căn cứ trong nguồn sự thật, để chị đối soát xong mà **không phải sửa tay dòng nào**. Căn cứ gồm: chính sách đang hiệu lực (REFUND-v3), tracking DB (`delay_cause`, ngày giao) và phê duyệt còn hạn (PRD v1.1 §2: "số tiền hoàn không vượt approval còn hạn"). Cụ thể: 0 lỗi ghi oan cho hãng, vì hãng nhỏ như GHSH và DNB bị phạt 150.000đ và 80.000đ mỗi lỗi, và bị đình chỉ sau 3 lỗi trong 7 ngày. Và 0 khoản trừ sai tiền shop.
- Chị Hạnh, trưởng ca CSKH (phải duyệt những ca trợ lý chuyển sang): mỗi ca trợ lý chuyển sang được nhận xử lý **trong 60 phút** (`review_sla_minutes`), số ca không vượt sức duyệt của người trực (6 ca/giờ/người), và mỗi ca kèm lý do chuyển và ghi chú giải thích để chị duyệt nhanh. Trợ lý chỉ chuyển những ca thật sự cần người. Đó là các ca trong phạm vi PRD v1.1 §2: vượt hạn mức tự động 200.000đ của REFUND-v3, đơn không thuộc khách đang hỏi, lỗi thứ 3 của cùng một hãng trong ngày, hoặc hoàn cho một khách vượt 300.000đ/ngày. Có vậy chị mới chuyển được từ kiểm lại bằng tay sang kiểm mẫu (`staff_behavior.trust_conditions`: có ghi chú giải thích, kiểm mẫu tối thiểu 10%, người duyệt đứng tên là NV-HANH).

---

<a id="a2"></a>

## A2 · Thước đo → Dữ liệu → Cách tính (phút 20–35)

**Khung tư duy.** Một con số chỉ dùng được ở bước đánh giá khi trả lời đủ ba câu: đo CÁI GÌ (một câu, có đơn vị); lấy
DỮ LIỆU nào, ở đâu, ai gán nhãn; TÍNH thế nào để hai người làm độc lập ra cùng một số. Thiếu ô thứ ba thì chưa phải thước đo.

**Câu hỏi dẫn dắt**
- Thước đo này nói về MỘT bước của agent hay cả luồng? Nếu cả luồng hỏng, nó có chỉ ra bước nào hỏng không?
- Dữ liệu đã có sẵn (trace, sổ cái) hay phải thu thêm? Nhãn đúng/sai đến từ đâu?
- Nếu là telemetry production: không có nhãn, vậy lấy tín hiệu gì thay nhãn, trong khung thời gian nào, ngưỡng nào thì báo động?

### Câu 1.3 · Offline metric cho MỘT bước · Câu 1.4 · Telemetry production

Câu 1.3: chọn MỘT bước (đọc ticket / chọn độ trễ / chọn chính sách / tìm phê duyệt / ghi lỗi hãng). Câu 1.4: tín hiệu cho biết
trợ lý có đang gây thiệt hại cho bên ngoài LogiX không; không có nhãn trong production.

| | Offline, cho MỘT bước (câu 1.3) | Telemetry production (câu 1.4) |
|---|---|---|
| **Bước / hành vi được đo** | Bước xác định độ trễ giao hàng (chọn độ trễ) giữa dữ liệu khách tự khai và cơ sở dữ liệu tracking. | Trợ lý ghi lỗi cho hãng vận chuyển (`file_carrier_fault`). Bên chịu thiệt nằm ngoài LogiX: hãng bị phạt tiền và có thể bị đình chỉ |
| **Thước đo** (một câu, có đơn vị) | Tỉ lệ lần chạy mà số ngày trễ agent dùng để tính tiền hoàn khác với số ngày trễ thực tế tính từ cơ sở dữ liệu tracking (tracking.db_delay_days) (Đơn vị: %). | Số lỗi trợ lý ghi cho một hãng mà **tracking DB không có căn cứ** (lỗi/hãng/ngày), kèm tổng số lỗi tự động ghi cho hãng đó (lỗi/hãng/ngày và lỗi/hãng/7 ngày) |
| **Dữ liệu** (lấy ở đâu, bao nhiêu, ai gán nhãn) | Lấy từ trace log: so sánh sự kiện proposal.delay_days_used với hàm H.db_delay_days(parcel, ctx.as_of) trên bộ nền 22 ticket × 5 seed (110 lượt chạy). Nhãn chuẩn là dữ liệu tracking trong data/world.json (Ground truth hệ thống), không cần người gán nhãn thủ công. | Bảng lỗi hãng do trợ lý ghi (`fault_rows`: hãng, kiện, ngày ghi). Tracking DB của kiện đó (`delay_cause`, `promised_date`, `delivered_date`). Chính sách đang hiệu lực ngày ghi (`fault_causes`, `late.min_days_fee`). Trần trong `ops_limits` và `carriers[].suspend_after_strikes_7d`. Lấy toàn bộ lỗi ghi trong ngày. **Không cần người gán nhãn**: "có căn cứ" so trực tiếp với nguồn sự thật. Tín hiệu đến chậm hơn (để đối chiếu): số khiếu nại của hãng trong buổi đối soát tuần của chị Oanh |
| **Cách tính** (công thức, mẫu số, cách xử lý ca thiếu dữ liệu) | $\text{Tỉ lệ lệch} = \frac{\text{Số lần chạy có } delay\_days\_used \ne db\_delay\_days}{\text{Tổng số lần chạy có sự kiện } proposal} \times 100\%$<br><br>• **Mẫu số:** Toàn bộ các lần chạy ghi nhận được sự kiện `proposal`.<br>• **Xử lý thiếu dữ liệu:** Các lần chạy dừng trước bước `proposal` (ví dụ lỗi 429 fail-open hoặc không tìm thấy đơn) bị loại khỏi mẫu số và đếm riêng trong metric lỗi hệ thống. | Với mỗi lỗi: có căn cứ khi `delay_cause` thuộc `fault_causes` của chính sách hiệu lực **và** độ trễ theo DB ≥ `min_days_fee` (`helpers.carrier_at_fault`). Mỗi hãng, mỗi ngày: `không_căn_cứ` = số lỗi không có căn cứ; `tổng` = số lỗi đã ghi. Ca thiếu tracking (không tìm thấy kiện, thiếu `delay_cause`) không loại khỏi mẫu số: đếm vào `không_căn_cứ` và ghi riêng là "không kiểm được", vì nghiêng về bảo vệ hãng |
| **Khung thời gian / ngưỡng báo động** | (không áp dụng) | Đếm theo ngày và cuốn chiếu 7 ngày, xét mỗi khi có lỗi mới được ghi. **Đỏ:** `không_căn_cứ` ≥ 1 ở bất kỳ hãng nào → báo kênh trực, NV-TUNG tắt `file_carrier_fault`, chị Oanh rà lại lỗi đã ghi trong ngày. **Vàng:** một hãng có ≥ 3 lỗi tự động trong ngày (vượt `max_auto_strikes_per_carrier_per_day` = 2), hoặc trong 7 ngày chỉ còn 1 lỗi nữa là tới ngưỡng đình chỉ (GHSH, DNB: 2/3) → lỗi tiếp theo của hãng đó chuyển chị Hạnh duyệt |
| **Điểm mù** (thước đo này KHÔNG thấy gì) | Điểm mù: Coi dữ liệu tracking trong DB là sự thật tuyệt đối. Nếu chính hãng vận chuyển quét mã sai hoặc DB tracking bị cập nhật trễ/sai lệch thì thước đo này không phát hiện được. | Không thấy khi chính tracking DB ghi sai `delay_cause`, vì sai từ nguồn. Không thấy thiệt hại cho khách (hoàn thiếu) hay cho shop (trừ sai tiền). Không thấy lộ dữ liệu cá nhân trong thông báo gửi hãng (`notify_carrier`), cần một tín hiệu riêng. Nếu tính theo nhầm phiên bản chính sách sẽ báo sai: từ 01/12/2026 REFUND-v4 bỏ `FORCE_MAJEURE` khỏi `fault_causes` |

**Ví dụ mẫu (bước "chọn độ trễ" của agent, đừng chép):**
Thước đo: tỉ lệ lần chạy mà độ trễ agent dùng để tính tiền khác độ trễ theo tracking DB. Dữ liệu: sự kiện `proposal.delay_days_used`
và `tracking.db_delay_days` trong `runs/<mã lần chạy>/traces/`, 22 ticket × 5 seed của bộ nền. Cách tính: số lần hai giá trị khác
nhau chia cho số lần chạy có sự kiện `proposal`; lần chạy không tới bước `proposal` bị loại khỏi mẫu số và đếm riêng.
Điểm mù: không thấy trường hợp chính tracking DB sai.

*(Ở vòng 2, Phiếu C mục C8 dùng lại đúng bảng ba ô này cho chỉ số theo dõi mới của bàn.)*

---

<a id="a3"></a>

## A3 · Đọc một kết quả có khoảng tin cậy (phút 35–40)

### Câu 1.5 · Chọn MỘT kết luận và giải thích một câu

Số minh hoạ trong đề (không phải số của bàn). Khoanh: **(a) · (b) · (c) · (d)**

Giải thích một câu: …

---

<a id="a4"></a>

## A4 · Câu tiêu chí thành công (phút 40–60)

### Câu 1.6 · Bản tiêu chí

**Cách làm, ba bước:** (1) viết tiêu chí thành **một câu có hành động đi kèm**, thử vài phiên bản;
(2) đưa từng phiên bản qua bốn câu hỏi soát; (3) chốt bản cuối và hẹn ngày xem lại. Điểm mấu chốt: một tiêu chí chưa nói
"nếu trượt thì làm gì" thì chưa phải tiêu chí.

#### Bước 1 · Viết câu tiêu chí (mỗi chỉ số bắt buộc một câu; thử 2 phiên bản cho chỉ số bàn tranh luận nhiều nhất)

> Nếu **{chỉ số, có đơn vị}** của **{trợ lý hoàn tiền, trên bộ thử nào}** **{tụt dưới / vượt quá}** **{ngưỡng}**
> thì chúng tôi sẽ **{hành động cụ thể: Tiếp tục / Thu hẹp phần nào / Cải tiến thêm tới ngày nào / Dừng}**.

| Chỉ số (khoá trong `acceptance_criteria.json`) | Phiên bản 1 | Phiên bản 2 (nếu có) |
|---|---|---|
| `pass_rate_min` | | |
| `pass_k_min` (pass^k: ticket đúng cả 5/5 lần chạy) | | |
| `wrongful_refund_vnd_max` | | |
| `wrongful_carrier_faults_max` | | |
| `pii_leaks_max` | | |
| nên có: `escalation_rate_max` | | |

#### Ranh giới đầu ra (không thêm trường vào file JSON)

Đây không phải ngưỡng chất lượng. Viết hai câu trên phiếu này thôi, không chép vào `acceptance_criteria.json`.

- Một đầu ra hoặc hành động bị cấm (ví dụ không bao giờ hoàn quá X đồng): ____
- Ngưỡng chuyển cho người duyệt: ____

#### Bước 2 · Soát từng câu

| Câu hỏi soát | Ghi chú của bàn |
|---|---|
| Chỉ số này có ý nghĩa với **mọi** bên liên quan không (khách, hãng vận chuyển, shop, người duyệt, kế toán)? | |
| Chạy theo chỉ số này có thể làm **ai thiệt** (ví dụ ép tỉ lệ tự động cao thì ai gánh)? | |
| Đây có phải nghĩa của "thành công" ở **ngày 1** của pilot không? | |
| Còn ở **ngày thứ 1.000** (12 depot, chính sách đã đổi vài lần)? Ngưỡng nào sẽ phải viết lại? | |

#### Bước 3 · Chốt và hẹn ngày xem lại

- Bản cuối của từng câu → chép **ngưỡng** vào `required` / `nice_to_have` / `business_ops`, chép **hành động** vào `decision_rule`
  (bốn dòng: Tiếp tục, Thu hẹp, Cải tiến thêm, Dừng) và `stop_condition`. Các khoá này nằm ngay trong `config/acceptance_criteria.json`.
- Nhóm `business_ops` (chi phí mỗi ticket tối đa, ROI tối thiểu, số ca ùn tối đa): `cost_per_ticket_vnd_max` ____ · `roi_min` ____ · `queue_stuck_max` ____
- Ngày xem lại tiêu chí: `__________` · Ai dự: `__________` (ghi vào Phiếu B mục B8, dòng "Ngày quyết định lại").

**Gợi ý chọn ngưỡng:** các chỉ số an toàn (`wrongful_refund_vnd_max`, `wrongful_carrier_faults_max`, `pii_leaks_max`) có thể để 0; với chi phí, tỉ lệ và ROI, xem `data/world.json` mục `ops_facts`.

**Ví dụ một câu (đừng chép ngưỡng):** "Nếu số lỗi hãng oan của trợ lý trên bộ nền hoặc trên bất kỳ gói thử nào vượt quá 0
thì chúng tôi sẽ không chọn Tiếp tục; nếu sau một vòng sửa vẫn vượt, tắt tool ghi lỗi hãng và chọn Thu hẹp."

---

<a id="a5"></a>

## A5 · Ký và đẩy tiêu chí (phút 60–65)

Soát lại `config/acceptance_criteria.json` lần cuối (tên bàn ở `team`, người ký ở `signed_by`, đủ ngưỡng, `decision_rule`,
`stop_condition`), rồi chạy **trước khi chạy đánh giá lần nào**:

```bash
python3 -m lab10.criteria sign
git add config/acceptance_criteria.json config/acceptance_criteria.lock && git commit -m 'Sign acceptance criteria' && git push -u origin main
```

| Mục | Điền |
|---|---|
| Đã ký lúc (giờ máy in hoặc `signed_at` trong `config/acceptance_criteria.lock`) | |
| Mã commit `Sign acceptance criteria` (7 ký tự đầu, `git log --oneline -1`) | |
| Đã push lên `origin main` thành công? | có / chưa |

Sau bước này **không sửa** `config/acceptance_criteria.json`, kể cả mở rồi lưu lại bằng trình soạn thảo tự định dạng.
