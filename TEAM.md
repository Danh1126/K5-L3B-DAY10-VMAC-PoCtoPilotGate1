# Team

## Thông tin nhóm

- Tên nhóm (`TenNhom`, không dấu, không khoảng trắng): VMAC
- Lớp: `L3B`
- Repo của bàn: `https://github.com/Danh1126/K5-L3B-DAY10-VMAC-PoCtoPilotGate1`
- Thẻ sự cố đã bốc (S1–S8): S7

## Thành viên

Họ tên đầy đủ và MSSV của **mọi** thành viên; bàn 3 người thì để trống dòng 4. Vai: Kỹ sư cổng · Sản phẩm và kinh doanh · Vận hành và pháp lý (README mục 3, phút 0–15).

| STT | Họ và tên | MSSV | Vai | Trưởng nhóm |
| --: | --------- | ---- | --- | :---------: |
|   1 | Nguyễn Duy Anh | 2A202603796 | Sản phẩm và kinh doanh | X |
|   2 | Lã Thái Minh | 2A202603756 | Kỹ sư cổng |  |
|   3 | Đặng Nhật Huy | 2A202603822 | Vận hành và pháp lý  |  |
|   4 |           |      |     |             |

Ghi `members` trong `submission/submission.json` theo dạng `"HoVaTen-MSSV"`, khớp bảng trên.

## Cá nhân

Mỗi thành viên tự viết một mục bên dưới (chép mẫu, đổi tiêu đề thành họ tên không dấu và MSSV, ví dụ `## NguyenVanAn-20241234`).

## LaThaiMinh-2A202603756

### Phần việc phụ trách

- Vai **Kỹ sư cổng**: đo bộ nền, đọc trace và đối chiếu hành động ghi với dữ liệu đơn hàng, tracking, chính sách.
- Phiếu B: cung cấp bằng chứng kỹ thuật cho B0–B2, triển khai cổng B7.1, kiểm tra tránh học thuộc bộ thử và ticket hiểm ở B7.2–B7.3; bàn giao số liệu cổng vòng 1 cho B8.
- Phiếu C, thẻ S7: phân tích lỗi ở C2, sửa cổng và ghi bảng sửa C7, xây chỉ số theo dõi C8. File phụ trách: [`lab10/guards.py`](lab10/guards.py) và [`lab10/monitors.py`](lab10/monitors.py).

### Đóng góp cụ thể

- Viết các nhánh `write_gate` kiểm tiền hoàn, lỗi ghi cho hãng và dữ liệu gửi hãng theo tracking, chính sách hiệu lực. Cùng bàn chốt bản cổng vòng 1 trước khi nhận thẻ S7.
- Dò các ca `S7-01@11`, `S7-04@11`, `S7-20@11`: phát hiện `customer_note` đưa thông tin cá nhân từ ticket ra hãng và `recipient_contact` lấy tên, SĐT người nhận từ DB dù ticket không chứa thông tin này.
- Sửa nhánh `notify_carrier` trong `write_gate`: xác minh đúng hãng, dựng lại bốn giá trị được phép từ order/tracking, gỡ các trường ngoài hợp đồng và ghi sự kiện các trường đã gỡ.
- Sửa monitor kiểm payload thực gửi để đọc `events`; thêm `recipient_contact_block_rate` đo tỷ lệ ticket mà cổng phải gỡ thông tin liên hệ người nhận. Kiểm lại S7 và bộ nền sau sửa.

### Bằng chứng

- Commit `e20546b` chốt bản cổng vòng 1 và Phiếu B; hash checkpoint `78a12654`. Xem [`lab10/guards_round1.py`](lab10/guards_round1.py) và [`config/round1.lock`](config/round1.lock).
- Bộ nền: `R-base-before-20261119-154520-bde05c` (109/110 trial đạt) và `R-base-prepared-20261119-172718-4676fa` (110/110 trial đạt). Số liệu ghi tại [Phiếu B B0](templates/form-b-evaluation-gates.md#b0) và [B7](templates/form-b-evaluation-gates.md#b7).
- S7 sau sửa: [`R-S7-grade-20261119-210956-4e5132`](runs/R-S7-grade-20261119-210956-4e5132.md) tự kiểm `PASS-VISIBLE`; `pii_leaks` 30 → 0, bộ nền không có ca mới hỏng, monitor `recipient_contact_block_rate` trên nền `0.0` và S7 `0.25`. Chi tiết ở [Phiếu C C2](templates/form-c-incident.md#c2), [C7](templates/form-c-incident.md#c7), [C8](templates/form-c-incident.md#c8). Bản sửa vòng 2 hiện có trong working tree, chưa có commit riêng.

### Exit ticket

- **Học được:** Allowlist tên trường chưa đủ; cổng cần đối chiếu cả giá trị và đích nhận với nguồn dữ liệu đáng tin, đồng thời log lần can thiệp để theo dõi lỗi chìm.
- **Còn chưa chắc:** Kết quả tự kiểm trên gói S7 nhìn thấy chưa chứng minh sẽ qua test ẩn; nếu dữ liệu order/tracking hoặc chính sách nguồn sai, cổng vẫn cần cơ chế phát hiện và xử lý vận hành.
  
## DangNhatHuy-2A202603822

### Phần việc phụ trách

- Vai **Vận hành và pháp lý**: người duyệt, người chịu trách nhiệm, điều kiện dừng, dữ liệu cá nhân gửi bên thứ ba, runbook và bài nộp.
- Phiếu B: câu 2.4 (B4 HAZOP phần ngoài kỹ thuật, B5 checklist 9 nhóm dòng 7–8), B6 dòng lăng kính "Con người và vận hành", câu 2.10 (B7.5 runbook phần 1–3, B7.6 giờ cao điểm).
- Phiếu C, thẻ S7: C2, C3.3, C4 (đối chiếu với bản của đồng đội), C10 risk register, C11 checklist và runbook phần 4–5, C12 phần vận hành.
- File phụ trách: [`config/operating_gates.json`](config/operating_gates.json) (mục `operations` và `legal`) và [`submission/submission.json`](submission/submission.json).

### Đóng góp cụ thể

- Điền mục `operations` (PIC, người duyệt, công suất duyệt, thời gian chờ tối đa, điều kiện dừng, kênh báo tin) và `legal` (`pii_fields_blocked_to_third_party`, `carrier_fault_requires_recorded_cause`); kiểm bằng `lab10.ops.problems()` trả về rỗng.
- Viết runbook phần 1–3 và giờ cao điểm, mọi con số khớp `data/world.json` (`ops_limits`, `ops_facts`): SLA 60 phút, 6 ca mỗi giờ mỗi người duyệt, trần 2.000.000đ mỗi ngày.
- Dò trace thẻ S7 (`S7-01`, `S7-04`, `S7-20`, `S7-21`, đối chứng `S7-05`) để viết bảng soát lỗi, hiệu chỉnh lòng tin và HAZOP của thẻ.
- Viết risk register C10, cập nhật checklist C11, runbook phần 4–5 và phần vận hành của C12 (đề xuất **Cải tiến thêm** cho v2, chờ cả bàn chốt).
- Điền `submission/submission.json` (`team`, `members`, `incident`, `decision_v1`, `decision_v2`, `three_lines`).
- Gộp nhánh: fetch `origin/main`, giải quyết xung đột ở Phiếu C bằng cách giữ phần đồng đội đã viết và chỉ áp lại phần còn trống.

### Bằng chứng

- Commit `9d637dd` (Phiếu C: C10, C11, runbook 4–5, C12; `submission.json`) và merge `b4f4683`.
- Report tự kiểm S7 dùng khi viết C11, C12: `R-S7-grade-20261119-172132-b3dc2e` (integrity, criteria, visible, regression ✅; monitor ❌ lúc đó vì chưa có chỉ số mới).
- Dòng trong phiếu: B4 (bảng ngoài kỹ thuật), B5 dòng 7–8, B7.5, B7.6, C10, C11, C12.
- Dùng AI: Claude hỗ trợ đọc code và trace, soạn nháp các mục trên và xử lý git. Các con số và quyết định đã được nhóm xem lại.

### Exit ticket

- **Học được:** Cổng pháp lý chỉ có tác dụng khi bật trong config và khớp với cổng trong code; con số vận hành phải dẫn về `ops_limits`, `ops_facts` mới giải thích được lúc demo.
- **Còn chưa chắc:** Các ngưỡng vàng, đỏ và 15 phút LLM lỗi là đề xuất chưa đo trên lượng ticket thật; chưa có căn cứ pháp lý do Pháp chế xác nhận.


## NguyenDuyAnh - 2A202603796

### Phần việc phụ trách

- Vai **Kiến trúc sư vận hành & Quản trị rủi ro / Điều phối Gate 1**: thiết kế tiêu chí nghiệm thu, bản đồ dữ liệu nguồn sự thật, phân tích failure mode và điều hành quy trình ra quyết định go/no-go giữa các vòng.
- Phiếu B (Vòng 1): xây dựng tiêu chí pass/fail, bản đồ dữ liệu và phân tích HAZOP vòng 1 (B3–B6); đánh giá chi phí–ROI, đối chiếu trạng thái sẵn sàng pilot và chốt quyết định vòng 1 tại B8 (`Tiếp tục`).
- Phiếu C (Vòng 2 – thẻ S7): tổng hợp kết quả tự kiểm và đối chiếu pre-mortem (C1), hiệu chỉnh lòng tin giữa người đặt và người nhận quà (C3.3), xây dựng HAZOP sự cố (C4), đặc tả specification và giả định môi trường (C5), phân tích cây lỗi fault tree trước và sau sửa (C6–C7), đồng thời thiết kế kịch bản ứng phó vận hành và sổ đăng ký rủi ro (C9–C12). File phụ trách: [`templates/form-b-evaluation-gates.md`](templates/form-b-evaluation-gates.md) và [`templates/form-c-incident.md`](templates/form-c-incident.md).

### Đóng góp cụ thể

- Thiết lập khung tiêu chí nghiệm thu Gate 1 (`pass_rate = 1.0`, `pii_leaks = 0`, kiểm soát chi phí ~4,293 VND và ROI ~1.33) cùng bảng phân quyền nguồn sự thật cho các thực thể đơn hàng, tracking và chính sách hiệu lực.
- Phân tích hiệu chỉnh lòng tin (C3.3) và bản chất lỗi chìm trên sự cố S7: làm rõ sự lệch pha giữa nhận thức của người đặt quà (`customer_note`) và người nhận quà (`orders[].recipient`) với hành vi tự động đẩy dữ liệu ra bên thứ ba (`notify_carrier`), chỉ ra cơ chế lọc danh sách trắng 4 trường (`order_id`, `parcel_id`, `district`, `delay_days`) là biện pháp bảo đảm không lộ thay vì chỉ che mờ ký tự.
- Xây dựng cây lỗi Fault Tree (C6) từ tác hại đỉnh (`pii_leaks = 30` ở gói S7 nền) ngược về 3 nhánh nguyên nhân độc lập ở các tầng đầu vào (`customer_note`), dữ liệu (`orders[].recipient`) và vận hành đối tác; liên kết từng lá với specification bị vi phạm và giả định môi trường sai thực tế.
- Hoàn thiện quy trình ứng phó sự cố (runbook) và sổ đăng ký rủi ro còn lại cho giai đoạn vận hành pilot thực tế (tình huống chính sách nguồn thiếu trường hợp đồng hoặc hãng vận chuyển thay đổi giao thức đối soát).

### Bằng chứng

- Bản chốt vòng 1 tại commit `e20546b` (checkpoint hash `78a12654`, [`config/round1.lock`](config/round1.lock)) và nội dung đầy đủ tại [Phiếu B](templates/form-b-evaluation-gates.md) (B3–B6, B8).
- Kết quả đối chiếu trước và sau sửa trên gói sự cố S7: từ lần chạy nền `pii_leaks = 30` về `pii_leaks = 0` tại [`R-S7-grade-20261119-210956-4e5132`](runs/R-S7-grade-20261119-210956-4e5132.md) (`PASS-VISIBLE`), giữ nguyên độ ổn định bộ nền 110/110 ca đạt (`R-base-prepared-20261119-172718-4676fa`).
- Các phân tích chi tiết được ghi nhận tại [Phiếu C C1](templates/form-c-incident.md#c1), [C3.3](templates/form-c-incident.md#c33), [C4](templates/form-c-incident.md#c4), [C5](templates/form-c-incident.md#c5) và [C6](templates/form-c-incident.md#c6).

### Exit ticket

- **Học được:** Trước đây mình cứ nghĩ AI chạy xong không báo lỗi, trả lời đúng là đạt rồi, nhưng qua bài này mới thấy có những lỗi "chìm" như gửi nhầm SĐT và địa chỉ người nhận quà sang cho hãng vận chuyển — hệ thống vẫn chạy êm ru nhưng ngoài đời lại thành vi phạm quyền riêng tư. Mình cũng hiểu ra là không thể chỉ nhắc khéo model trong prompt được, mà phải chặn cứng bằng luật ở code (chỉ cho phép gửi đúng 4 trường đã thỏa thuận) và kiểm tra lại những điều mình hay mặc định sai về người dùng ngoài đời.
- **Còn chưa chắc:** Vẫn hơi băn khoăn là khi mang ra chạy thật ngoài pilot, nếu bản tin gửi hãng chỉ có mã đơn với tên quận mà thiếu SĐT người nhận thì các bác tài xế giao hàng có gặp khó khăn không. Nếu hãng than phiền khó giao lại, không biết bên vận hành có bị áp lực phải mở thêm trường thông tin hay tìm cách lách cổng hay không.