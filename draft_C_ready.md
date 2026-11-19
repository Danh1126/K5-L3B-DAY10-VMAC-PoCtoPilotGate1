# Nháp phần C · viết trước, chưa có số từ A và B

Phần này chỉ gồm những gì viết được ngay. Các ô để trống đang chờ A hoặc B. Chép vào form sau khi nhóm xác nhận.

## B4 · HAZOP vòng 1 · các dòng ngoài kỹ thuật

Tool được HAZOP: [chờ A và nhóm xác nhận; đề xuất `issue_refund`]

| # | Từ gợi ý | Lệch thế nào | Hậu quả | Người chịu | Kiểm soát (khoá config, số do B điền) |
|---|---|---|---|---|---|
| 1 | THỪA (MORE) | Tổng hoàn tự động cho một khách vượt trần trong ngày, hoặc tổng cả ngày vượt ngân sách Finance | Finance mất tiền ngoài ngân sách | NV-HANH (duyệt vượt hạn mức) | `business.daily_refund_cap_vnd`; cổng `write_gate` của A |
| 2 | KHÁC NGƯỜI (OTHER THAN) | Thông tin cá nhân của khách đi kèm thông báo gửi cho hãng hoặc shop | Lộ dữ liệu cá nhân cho bên thứ ba | NV-OANH (đối soát hãng và shop) | `legal.pii_fields_blocked_to_third_party` (danh sách trường chờ B3); chỉ số `pii_leaks` |
| 3 | MUỘN (LATE) | Ticket chuyển người duyệt không được nhận trong 60 phút | Khách chờ lâu; người duyệt quá tải | NV-HANH | `operations.reviewers_on_shift`; `operations.max_queue_wait_minutes` (khớp `queue_stuck_max` của B) |
| 4 | SAI (AS WELL AS) | Ghi lỗi cho hãng mà không có nguyên nhân được ghi lại | Tài xế bị phạt oan. Ví dụ DNB: 80.000đ mỗi lần, đình chỉ sau 3 lần trong 7 ngày | NV-OANH | `legal.carrier_fault_requires_recorded_cause`; `ops_limits.max_auto_strikes_per_carrier_per_day` = 2 |

## B5 · Checklist, dòng 8 (con người, pháp lý)

- **Mục cần kiểm tra:** bên thứ ba gồm hãng vận chuyển, tài xế, shop, người nhận quà, người đứng tên duyệt; trường cá nhân cấm gửi; ghi nguyên nhân lỗi cho hãng.
- **PIC:** Phạm Kiều Oanh (NV-OANH), đề xuất.
- **Trạng thái:** Chưa.
- **Bằng chứng:** điền sau, khi có config và runbook.

## B5 · Checklist 9 nhóm, lần 1 (đề xuất PIC, trạng thái "Chưa" cho tất cả)

Các dòng 1–6 và 9 không thuộc phần của C. Cột PIC là đề xuất theo vai, nhóm xác nhận tên.

| # | Nhóm việc | PIC đề xuất | Ghi chú |
|---|---|---|---|
| 1 | Chất lượng | Kỹ sư cổng (A) | Chờ báo cáo baseline |
| 2 | Dữ liệu | Sản phẩm và kinh doanh (B) | Chờ bản đồ dữ liệu B3 |
| 3 | Bảo mật | Kỹ sư cổng (A) | HAZOP PERTURBED, do A làm |
| 4 | Quyền hạn | Kỹ sư cổng (A) | `config/switches.json` và `write_gate` |
| 5 | Hiệu năng, hạ tầng | Kỹ sư cổng (A) | Chờ số người duyệt và ca mỗi giờ |
| 6 | Chi phí | Sản phẩm và kinh doanh (B) | Chờ khối kinh doanh của report |
| 7 | Vận hành | Lê Thanh Tùng (NV-TUNG), đề xuất | Runbook và `operations`, do C làm |
| 8 | Con người, pháp lý | Phạm Kiều Oanh (NV-OANH), đề xuất | Bên thứ ba và `legal`, do C làm |
| 9 | Quyết định | Sản phẩm và kinh doanh (B) | Tiêu chí đã ký và quyết định v1 |

## B4 · Dòng kỹ thuật

Chưa viết. Cần tool từ A (đề xuất `issue_refund`) và hành vi lệch của tool đó. Câu 2.4 yêu cầu ít nhất ba dòng trên một tool, trong đó ít nhất hai dòng ngoài kỹ thuật. Bốn dòng ngoài kỹ thuật ở trên đã đáp ứng cả hai điều kiện, nên dòng kỹ thuật không bắt buộc để đủ 2.4; A có thể bổ sung nếu muốn cân bằng HAZOP.

## B7.5 · Bảng vai trò trong runbook (đề xuất, nhóm xác nhận)

| Vai trò | Người đề xuất |
|---|---|
| PIC của trợ lý | [nhóm chốt]; đề xuất Lê Thanh Tùng (NV-TUNG) |
| Người duyệt hoàn tiền vượt hạn mức | Trần Thị Hạnh (NV-HANH) |
| Người giữ công tắc tắt từng thao tác ghi | Lê Thanh Tùng (NV-TUNG) |
| Người nhận khiếu nại của bên thứ ba | Phạm Kiều Oanh (NV-OANH) |

## Chờ, chưa điền

- Tool của B4 (chờ A và nhóm).
- Danh sách trường cá nhân (chờ B3).
- Mọi con số trong config: trần hoàn tiền, `queue_stuck_max`, `cost_per_ticket_vnd_max`, `roi_min` (chờ B ký và điền mục `business`).
- `reviewers_on_shift`, `max_queue_wait_minutes` (chờ báo cáo baseline của A).
- `stop_conditions` (chờ A viết cổng).
- Cột "Trạng thái" và "Bằng chứng" của B5 (chờ báo cáo và runbook).
- Giờ cao điểm (chờ số ticket nền).
