# Ontology + CVAT setup

Bảng ontology là **source of truth** cho schema CVAT: `03_cvat_labels.json` phải khớp từng dòng ở đây.

## Ontology table

| Name | Geometry | Type (class / attribute) | Allowed values | Default | Mutable? | Rationale |
|---|---|---|---|---|---|---|
| `vehicle` | rectangle | class | — | — | — | Box thân xe chuẩn cho detector + ước lượng kích thước |
| `vehicle_type` | — | attribute của `vehicle` | `__undefined__`, `car`, `truck`, `bus`, `motorcycle`, `bicycle`, `cart`, `unknown` | `__undefined__` | không | Cùng rule vẽ cho mọi loại xe nên để attribute; `cart` cho xe ba gác/xe đẩy phổ biến ở VN |
| `has_hazard` | — | attribute (checkbox) của `vehicle` | `false` / `true` | `false` | không | Bản sao liên kết nằm trên xe, đọc được bằng `lab9.py calib/score` (tool không đọc Group) |
| `occluded` | — | attribute (checkbox) | `false` / `true` | `false` | không | QA lọc xe bị che để kiểm geometry |
| `truncated` | — | attribute (checkbox) | `false` / `true` | `false` | không | Tách bị mép ảnh cắt khỏi bị che |
| `attached_hazard` | rectangle | class | — | — | — | Không gian bị chiếm thêm; tách class để box xe không bị phình |
| `hazard_type` | — | attribute của `attached_hazard` | `__undefined__`, `protruding_load`, `oversized_cargo`, `open_door`, `other` | `__undefined__` | không | Planner xử lý khác nhau (cửa có thể đóng lại, hàng thì không) |
| `side` | — | attribute của `attached_hazard` | `__undefined__`, `front`, `rear`, `left`, `right` | `__undefined__` | không | Cho biết phía nào của xe bị mở rộng |
| `needs_review` | — | attribute (checkbox) của `attached_hazard` | `false` / `true` | `false` | không | Kênh ESCALATE ở mức object |
| `image_escalate` | tag | class (tag cả ảnh) | — | — | — | ESCALATE cả ảnh |
| *(liên kết)* | Group của CVAT | — | `group_id` trong export XML | — | — | Nối hazard với đúng xe; mỗi hazard thuộc một Group có đúng một `vehicle` |

## Class hay attribute

- `vehicle` và `attached_hazard` là **class** riêng vì downstream dùng khác nhau: box xe dùng cho kích thước chuẩn,
  box hazard dùng cho không gian bị chiếm. Nếu để hazard thành attribute của xe thì không có hình học riêng → buộc
  phải phình box xe, đúng thứ bài này cần tránh.
- `hazard_type`, `side` là **attribute** của hazard vì cùng rule vẽ.
- **Liên kết:** dùng **Group** (phím G) vì export CVAT for images 1.1 ghi `group_id` giống nhau cho các box cùng nhóm.
  Vì `lab9.py` không đọc `group_id`, nhóm thêm checkbox `has_hazard` trên xe để calibration/score vẫn so được.
- **Default gây bias:** `hazard_type` và `side` mặc định `__undefined__` để annotator không để sót giá trị mặc định;
  `has_hazard` mặc định `false` nên QA đối chiếu: ảnh có hazard mà không xe nào `has_hazard=true` là lỗi.

## CVAT

- **Phiên bản CVAT** (`python lab9.py cvat`): TODO — điền bản in ra, ví dụ v2.74.1
- **Tên task calibration** (có version guideline): TODO — ví dụ `teamXX-calib-v1-<tên>`
- **Guide của task đã dán `02_guideline.md`?** TODO (có / chưa)
- **Nhóm dùng Track hay Shape, vì sao:** Shape. Ảnh tĩnh; Group hoạt động với Shape; export CVAT for images 1.1.

## Setup test

Một thành viên **chưa tham gia setup** mở task và trả lời: label gì, dùng tool nào, gán attribute nào, cách Group,
khi nào escalate. Ghi lại ai test và chỗ họ vấp:

TODO — ví dụ: "<tên> vẽ đúng hai box nhưng không biết bấm G để group → đã thêm các bước bấm phím vào §5."
