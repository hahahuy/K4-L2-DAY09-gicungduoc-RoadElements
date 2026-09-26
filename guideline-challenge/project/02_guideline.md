# Annotation guideline — Phần nhô nguy hiểm: hàng thò ra, hàng cồng kềnh, cửa xe mở

**Version:** v1

<!--
v1 = bản nháp đầu. Sau calibration đổi thành v2, sau blind handoff đổi thành v3; mỗi lần ghi một dòng vào
08_revision_log.md. Peer chỉ nhận file này: rule nào không có ở đây thì coi như không tồn tại.
-->

## 1. Objective + scope

Dữ liệu dùng cho hai việc: (1) phát hiện xe và ước lượng **kích thước chuẩn** của xe; (2) cho biết **không gian bị
chiếm thêm** bởi phần nhô ra. Vì vậy **không bao giờ vẽ một box to bao cả xe lẫn phần nhô**. Luôn vẽ **2 box riêng
có liên kết**: `vehicle` cho thân xe, `attached_hazard` cho phần nhô.

Trong scope: ô tô, xe tải, bus, xe máy, xe ba gác/xe đẩy hàng, xe đạp; phần nhô = hàng/vật liệu thò ra, hàng cồng
kềnh vượt bề ngang xe, cửa xe đang mở. Không vẽ: gương chiếu hậu, hàng chất cao nhưng không thò ra khỏi mép, người
bước xuống xe, phản chiếu.

## 2. Annotation unit

- Đơn vị là **một ảnh tĩnh**.
- **Một xe = một box `vehicle`.** Xe máy/xe đạp/xe ba gác: box gồm cả người lái. Xe tải kéo rơ-moóc: đầu kéo và
  rơ-moóc là **một** box.
- **Một phần nhô liền khối = một box `attached_hazard`.** Hàng thò ra ở **hai phía khác nhau** (ví dụ thò cả trước và
  sau) là **hai** box hazard. Nhiều thanh sắt bó chung thò ra cùng một phía là **một** box.
- Mỗi box `attached_hazard` gắn với **đúng một** xe.

## 3. Geometry rule

Công cụ: **Rectangle**, chế độ **Shape**.

**Box `vehicle` = đường bao chuẩn của xe** (như lúc xe không chở gì và mọi cửa đóng):
- Ô tô/xe tải/bus: ôm thân xe + thùng xe, **gồm** gương chiếu hậu, **không gồm** hàng thò ra ngoài mép thùng và
  **không gồm** cánh cửa đang mở ra ngoài thân.
- Xe máy/xe đạp/xe ba gác: ôm xe + người lái + phần hàng **nằm trong** bề ngang tay lái và chiều dài xe.
- Bị che: ôm phần nhìn thấy, không đoán phần bị khuất.

**Box `attached_hazard` = chỉ phần nằm NGOÀI box `vehicle`:**
- Bắt đầu từ mép box xe (chạm hoặc chồng ≤ 5 px) và kéo tới **điểm xa nhất** của phần nhô.
- Chiều còn lại ôm sát vật nhô. Ví dụ bó sắt thò sau thùng: box hazard cao đúng bằng bó sắt, không cao bằng cả xe.
- Cửa mở: ôm phần cánh cửa nằm ngoài thân xe, tính từ bản lề tới mép ngoài cửa.
- Dây buộc, tấm vải phủ lủng lẳng thuộc hàng hoá thì tính vào hazard.

**Ngưỡng vẽ hazard** — đo phần nhô theo cùng chiều với xe (chiều dài nếu thò trước/sau, bề ngang nếu thò hai bên):
- Nhô **≥ 12%** kích thước xe **hoặc ≥ 15 px** (chỉ cần đạt một trong hai) → **vẽ** hazard.
- Nhô **8–12%** và < 15 px → **vẽ** hazard + tick `needs_review` (xem §7).
- Nhô **< 8%** và < 15 px → **không vẽ** hazard; box xe vẫn **không** gồm phần đó.

Tolerance: mỗi cạnh lệch ≤ 3 px là đạt; vật cao < 40 px thì lệch ≤ 10% chiều cao là đạt.

## 4. Taxonomy

Class: `vehicle`, `attached_hazard` (rectangle), `image_escalate` (tag). Mọi dropdown mặc định `__undefined__`:
**bắt buộc chọn**, còn `__undefined__` trong export là lỗi.

| Label | Attribute | Giá trị | Chọn khi |
|---|---|---|---|
| `vehicle` | `vehicle_type` | `car`, `truck`, `bus`, `motorcycle`, `bicycle`, `cart` (xe ba gác/xe đẩy), `unknown` | Loại xe |
| | `has_hazard` | checkbox | Luôn tick (vì chỉ vẽ xe có hazard); để trống là lỗi quên liên kết |
| | `occluded` | checkbox | Xe bị vật khác che > 30% |
| | `truncated` | checkbox | Xe bị mép ảnh cắt |
| `attached_hazard` | `hazard_type` | `protruding_load` | Hàng/vật liệu dài (sắt, ống, gỗ, tre) thò ra ngoài thân/thùng |
| | | `oversized_cargo` | Khối hàng to (thùng, bao, tủ, kính) vượt bề ngang/chiều dài xe máy, xe ba gác |
| | | `open_door` | Cửa bên, cốp, cửa sau thùng xe đang mở ra ngoài thân |
| | | `other` | Nhô nguy hiểm nhưng không thuộc 3 loại trên |
| | `side` | `front`, `rear`, `left`, `right` | Phía nhô ra so với **thân xe** (không phải so với camera). Nhô chéo thì chọn phía nhô **xa hơn** |
| | `needs_review` | checkbox | Không chắc có vượt ngưỡng, không chắc thuộc xe nào, hoặc không chắc cửa đang mở |

## 5. Inclusion / exclusion

**Bắt buộc:**
1. Vẽ `vehicle` **chỉ** cho xe có ít nhất một hazard được vẽ theo §3. Xe **không** có hazard thì **không vẽ**, kể cả
   xe to, gần hay che mất một phần hazard.
2. Vẽ `attached_hazard` cho mọi phần nhô ≥ ngưỡng §3.
3. **Liên kết** hazard với xe của nó:
   - Bấm **G** (hoặc nút **Group shapes** ở thanh công cụ trái) để vào chế độ nhóm, click box xe rồi click box
     hazard, bấm **G** lần nữa để hoàn tất → hai box thành một **Group**. Kiểm tra: sidebar phải, mục
     **Appearance → Color by: Group**, hai box phải cùng màu.
   - Tick `has_hazard` trên box xe.
   - Hazard không có Group, hoặc xe có hazard mà `has_hazard=false`, là lỗi.

**Không vẽ hazard:** hàng chất cao nhưng không thò ra khỏi mép trước/sau/bên; hàng nằm gọn trong thùng; gương chiếu
hậu; bạt phủ ôm sát thùng; cửa đóng; người đứng cạnh xe.

## 6. Visibility / occlusion

- Phần nhô bị xe khác che một phần: vẽ phần nhìn thấy, tick `needs_review` nếu không thấy điểm xa nhất.
- Thấy phần nhô nhưng **không thấy xe chở nó** (xe bị che gần hết): vẫn vẽ `attached_hazard`, không có Group, tick
  `needs_review`. Đây là trường hợp duy nhất hazard được phép không có Group.
- Ban đêm/ngược sáng: chỉ vẽ khi phân biệt được đường viền vật nhô.
- Xe máy chở hàng trong đám đông xe máy: đánh giá từng xe; hàng che người lái vẫn tính vào hazard phần vượt bề ngang.

## 7. Ambiguity / escalation

| Tình huống | Quyết định | Thể hiện trong CVAT |
|---|---|---|
| Nhô rõ ràng ≥ ngưỡng | LABEL | `vehicle` + `attached_hazard` + Group + `has_hazard` |
| Hàng không thò ra khỏi mép | IGNORE | Không vẽ gì cho xe này |
| Nhô < 8% và < 15 px | IGNORE | Không vẽ gì cho xe này |
| Nhô 8–12% và < 15 px (sát ngưỡng) | ESCALATE object | **Vẽ** `vehicle` + hazard + Group + `needs_review` (nghiêng về vẽ vì bỏ sót nguy hiểm hơn) |
| Nhô rõ nhưng không nhận ra loại | UNKNOWN | `hazard_type=other` + `needs_review` |
| Cửa hé, không chắc đang mở hay chỉ là khe cửa | ESCALATE object | Vẽ `open_door` + `needs_review` |
| Không xác định được hazard thuộc xe nào | ESCALATE object | Vẽ hazard, Group với xe **gần nhất** theo chiều sâu, tick `needs_review` |
| Cả ảnh quá tối/nhoè | ESCALATE ảnh | Tag `image_escalate`, vẫn vẽ các trường hợp rõ |

## 8. Temporal rule

Không áp dụng — task ảnh tĩnh. Không suy đoán cửa "sắp mở" hay hàng "sắp rơi".

## 9. Examples

| sample_id | Thấy gì | Expected output | Rule áp dụng |
|---|---|---|---|
| OVH01 | Xe tải phía trước chở bó sắt thép thò ra sau thùng | `vehicle truck has_hazard=true` ôm thân + thùng; `attached_hazard protruding_load side=rear` từ mép sau thùng tới đầu bó sắt; hai box cùng Group | §3 box xe chuẩn, §5 liên kết |
| OVH02 | Ô tô đỗ ven đường, cửa tài xế mở về phía lòng đường | `vehicle car has_hazard=true` theo thân xe đóng cửa; `attached_hazard open_door side=left` (hoặc `right` tuỳ phía cửa của xe) ôm cánh cửa ngoài thân; Group | §3 cửa mở, §4 side theo thân xe |
| OVH03 | Xe máy chở thùng hàng rộng hơn tay lái | `vehicle motorcycle has_hazard=true` ôm xe + người + phần hàng trong bề ngang tay lái; hai box `oversized_cargo side=left` và `side=right` cho phần vượt ra mỗi bên; Group cả ba | §2 hai phía = hai box |
| OVH04 | Xe tải chở hàng chất cao nhưng nằm gọn trong thùng | Không vẽ gì cho xe tải này (không `vehicle`, không hazard) | §5 xe không có hazard thì không vẽ |

## 10. Common mistakes

1. Vẽ **một box to** bao cả xe lẫn hàng thò ra → sai kích thước xe. Luôn tách hai box.
2. Box hazard **bao cả xe** hoặc bao cả bó hàng nằm trong thùng → hazard chỉ là phần **nằm ngoài** box xe.
3. Quên **Group** hoặc quên tick `has_hazard` → liên kết không đọc được trong export.
4. Chọn `side` theo hướng camera thay vì theo **thân xe** (xe đi ngược chiều: cửa bên trái của xe nằm bên phải ảnh).
5. Vẽ hazard cho hàng chất cao nhưng không thò ra mép, hoặc vẽ `vehicle` cho xe không có hazard.
6. Box xe máy không gồm người lái.
7. Để sót `__undefined__` → quét lại bằng chế độ **Attribute annotation** trước khi lưu.
