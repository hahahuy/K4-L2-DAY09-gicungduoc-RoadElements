# Annotation guideline — Phần nhô nguy hiểm của phương tiện (vehicle + attached_hazard)

**Version:** v2

Peer chỉ nhận file này. Rule không viết ở đây thì không tồn tại. Ảnh ví dụ gọi bằng `sample_id` (`OVH01`, `OVH10`, …).
Schema CVAT dùng đúng tên label và attribute trong file này (`vehicle`, `attached_hazard`, `image_escalate`).

**Rule nhớ nhanh:** (1) Xe có phần nhô đạt ngưỡng mới vẽ `vehicle`. (2) `attached_hazard` chỉ là phần nằm **ngoài**
đường bao chuẩn của xe. (3) Group hazard với đúng xe + tick `has_hazard`. (4) Không chắc → `needs_review` /
`image_escalate`. (5) Trước khi lưu: không còn `__undefined__`.

## 1. Objective + scope

Annotation phục vụ hai downstream:

1. **Detector / ước lượng kích thước xe** cần box `vehicle` đúng **kích thước chuẩn** của thân xe — như khi xe không
   chở gì và mọi cửa đều đóng.
2. **Planner** cần box `attached_hazard` cho **không gian bị chiếm thêm** bởi hàng hoặc cửa nằm ngoài thân xe.

Không bao giờ vẽ một box to bao cả xe lẫn phần nhô.

**Trong scope**

- Phương tiện: ô tô con, xe tải, bus, xe máy, xe đạp, xe ba gác / xe đẩy hàng.
- Phần nhô: hàng / vật liệu thò ra ngoài thân hoặc thùng xe (trước, sau, hai bên); hàng cồng kềnh vượt bề ngang tay
  lái của xe máy / xe ba gác; cửa xe (cửa bên, cốp sau, cửa thùng sau của xe tải) **đang mở ra ngoài** thân xe.

**Ngoài scope — không vẽ**

- Hàng chất cao trên nóc / trong thùng nhưng **không thò ra** khỏi mép trước, sau hoặc hai bên (task không đo chiều cao).
- Hàng nằm gọn trong thùng xe, kể cả khi cửa thùng đang mở (chỉ vẽ cánh cửa, không vẽ hàng bên trong).
- Gương chiếu hậu, bạt phủ ôm sát thùng, người bước xuống xe, người đứng cạnh xe, phản chiếu, xe trong ảnh quảng cáo.
- Xe **không** có phần nhô đạt ngưỡng: không vẽ `vehicle`, kể cả xe to, xe gần camera hay xe đang che một phần hazard
  của xe khác.

## 2. Annotation unit

Một ảnh tĩnh. Mỗi xe có phần nhô = một box `vehicle` + một hoặc nhiều box `attached_hazard`.

- Một xe = một box `vehicle`. Xe máy / xe đạp / xe ba gác: box gồm cả người lái. Đầu kéo + rơ-moóc = một box.
- Một phần nhô liền khối ở **một phía** của xe = một box `attached_hazard`. Nhiều thanh sắt bó chung, nhiều thùng
  hàng chồng liền nhau ở cùng một phía → một box.
- Phần nhô vượt ra ở **hai phía khác nhau** → mỗi phía một box, mỗi box một giá trị `side`. Ví dụ `OVH03`: sọt hàng
  vượt cả bên trái lẫn bên phải xe máy → hai box.
- Mỗi `attached_hazard` thuộc đúng một xe (xem Group ở mục 4).
- Tag `image_escalate` gắn cho cả ảnh, không gắn cho object.

## 3. Geometry rule

Công cụ: **Rectangle**, chế độ **Shape** (ảnh tĩnh, không dùng Track).

**Box `vehicle` = đường bao chuẩn của xe**

- Ô tô / xe tải / bus: ôm thân xe + thùng xe, gồm cả gương chiếu hậu. **Không** gồm hàng thò ra ngoài mép thùng,
  **không** gồm cánh cửa / cánh cốp đang mở ra ngoài thân (vẽ như khi cửa đóng).
- Xe máy / xe đạp / xe ba gác: ôm xe + người lái. Hàng nằm trong bề ngang tay lái và trong chiều dài xe vẫn thuộc box
  `vehicle`.
- Bị che: ôm phần nhìn thấy, không đoán phần bị khuất. Bị mép ảnh cắt: box dừng ở mép ảnh.

**Box `attached_hazard` = chỉ phần nằm ngoài box `vehicle`**

- Bắt đầu từ mép box xe ở phía nhô ra; được chạm hoặc chồng lên box xe **tối đa 5 px**.
- Kéo tới điểm xa nhất của phần nhô nhìn thấy; hai cạnh còn lại ôm sát vật nhô.
- Cửa mở: từ bản lề tới mép ngoài cánh cửa, chỉ lấy phần nằm ngoài đường bao chuẩn của xe.
- Dây buộc, vải phủ lủng lẳng thuộc hàng → tính vào hazard.
- Không bao phần hàng vẫn nằm trong box xe, không bao nền hay khoảng trống.

**Ngưỡng — có vẽ hazard hay không.** Đo phần nhô theo cùng chiều với xe: theo chiều dài xe nếu thò trước / sau, theo
bề ngang xe nếu thò trái / phải. So với kích thước box `vehicle` theo chiều đó.

| Phần nhô | Quyết định |
|---|---|
| ≥ 12% **hoặc** ≥ 15 px (chỉ cần một điều kiện) | LABEL hazard |
| 8–12% **và** < 15 px | LABEL hazard + `needs_review=true` (sát ngưỡng thì nghiêng về vẽ vì bỏ sót nguy hiểm hơn) |
| < 8% **và** < 15 px | IGNORE hazard. Box `vehicle` vẫn không được nuốt phần nhô đó |

**Tolerance:** mỗi cạnh lệch ≤ 3 px so với biên vật là đạt; vật cao < 40 px thì lệch ≤ 10% chiều cao. Box xe bị kéo
phình để bao phần nhô là sai, dù attribute đúng.

## 4. Taxonomy

Mọi dropdown mặc định `__undefined__`. Còn `__undefined__` trong export là chưa gán, tính là lỗi. Checkbox mặc định tắt.

| Label | Attribute | Giá trị | Chọn khi |
|---|---|---|---|
| `vehicle` (rectangle) | `vehicle_type` | `car`, `truck`, `bus`, `motorcycle`, `bicycle`, `cart`, `unknown` | Loại xe. Pickup, SUV, van = `car`. Xe tải thùng, xe ben = `truck`. Xe ba gác, xe đẩy hàng = `cart`. Không nhận ra = `unknown` |
| | `has_hazard` | checkbox | **Luôn tick** — chỉ vẽ `vehicle` cho xe có hazard |
| | `occluded` | checkbox | Xe bị vật khác che > 30% |
| | `truncated` | checkbox | Xe bị mép ảnh cắt |
| `attached_hazard` (rectangle) | `hazard_type` | `protruding_load`, `oversized_cargo`, `open_door`, `other` | `protruding_load`: vật **dài** (ống, sắt, gỗ, thanh nhôm) thò ra khỏi mép xe. `oversized_cargo`: hàng **khối** (thùng, bao, sọt, xe chở trên xe) vượt bề ngang / chiều dài xe. `open_door`: cửa bên, cốp, cửa thùng sau đang mở ra ngoài thân. Thấy rõ phần nhô nhưng không nhận ra loại: `other` + `needs_review` |
| | `side` | `front`, `rear`, `left`, `right` | Phía **của thân xe** mà phần nhô vượt ra — không theo camera. Xe đi cùng chiều, nhìn từ phía sau: bên trái ảnh = `left` của xe. Xe đi ngược chiều (nhìn đầu xe): bên trái ảnh = `right` của xe. Cốp và cửa thùng sau = `rear` |
| | `needs_review` | checkbox | Chỉ bật theo bảng mục 7. Không bật "cho chắc" trên ca đã rõ |
| `image_escalate` (tag) | — | tag cả ảnh | Ảnh quá tối / nhoè / bị che đến mức không kết luận được có phần nhô hay không. Vẫn vẽ những case rõ trong ảnh |

**Liên kết hazard ↔ xe bằng Group của CVAT**

1. Vẽ box `vehicle` và các box `attached_hazard` của xe đó.
2. Bấm **G** (chế độ Group shapes), click box xe rồi từng box hazard của xe đó.
3. Bấm **G** lần nữa để hoàn tất.
4. Kiểm tra: sidebar phải → **Appearance** → **Color by: Group**; xe và hazard của nó phải cùng màu, xe khác màu khác.
5. Tick `has_hazard` trên xe.

Quên Group hoặc quên tick `has_hazard` đều là lỗi. **Ngoại lệ duy nhất:** thấy rõ phần nhô nhưng xe chở nó bị che gần
hết (không vẽ được box xe) → vẫn vẽ `attached_hazard`, không Group, bật `needs_review`.

## 5. Inclusion / exclusion

**Bắt buộc vẽ**

1. Mọi `attached_hazard` đạt ngưỡng mục 3 và có bằng chứng gắn / chở / mở từ xe (dây buộc, giá đỡ, đặt trên xe, bản lề).
2. Một `vehicle` cho mỗi xe có ít nhất một hazard, `has_hazard=true`, đủ `vehicle_type`.
3. Group hazard với đúng xe.

**Không vẽ**

- Hàng chất cao nhưng không thò khỏi mép (ví dụ bồn nước trên thùng pickup ở `OVH03`, `OVH05`: bồn nằm trong bề
  ngang thùng → không vẽ gì cho chiếc pickup).
- Hàng nằm gọn trong thùng, kể cả khi thấy qua cửa thùng đang mở.
- Cửa đóng, bạt phủ ôm sát thùng, gương chiếu hậu.
- Vật đặt trên mặt đất / vỉa hè cạnh xe mà có khoảng hở rõ với xe và không có dây / giá nối với xe (thùng rác, hàng
  bày bán, cây).
- Xe không có hazard.

## 6. Visibility / occlusion

- **Bị che một phần:** vẽ phần nhìn thấy. Không thấy điểm xa nhất của phần nhô → bật `needs_review`. Xe bị che > 30%
  → `occluded=true`.
- **Không thấy xe chở hàng** (bị che gần hết): vẫn vẽ hazard, không Group, `needs_review=true`.
- **Ban đêm / ngược sáng / mưa:** chỉ vẽ khi phân biệt được đường viền vật nhô. Không đoán hình dạng hàng từ đèn xe
  hay bóng đổ. Ví dụ `OVH08`: đêm, bao hàng đen vẫn thấy rõ đường viền vượt bên trái xe máy → vẽ.
- **Đám đông xe máy:** đánh giá từng xe. Hàng che người lái vẫn tính theo phần vượt bề ngang tay lái.
- Không vẽ phản chiếu trên mặt đường ướt hay trên kính.

## 7. Ambiguity / escalation

| Tình huống | Quyết định | Thể hiện trong CVAT |
|---|---|---|
| Phần nhô rõ, ≥ ngưỡng | LABEL | `vehicle` + `attached_hazard` + Group + `has_hazard` |
| Hàng không thò ra khỏi mép | IGNORE | Không vẽ gì cho xe đó |
| Nhô < 8% và < 15 px | IGNORE | Không vẽ gì cho xe đó |
| Nhô 8–12% và < 15 px | ESCALATE object | Vẽ `vehicle` + hazard + Group, hazard `needs_review=true` |
| Thấy rõ phần nhô nhưng không nhận ra loại | UNKNOWN | `hazard_type=other` + `needs_review=true` |
| Cửa hé, không chắc đang mở ra ngoài thân | ESCALATE object | Vẽ `open_door` + `needs_review=true` |
| Vật chạm / đè lên xe nhưng không thấy dây buộc hay giá đỡ (không chắc có gắn với xe) | ESCALATE object | Vẽ hazard `other` + `needs_review=true`, Group với xe đó |
| Vật cạnh xe có khoảng hở rõ, đứng trên mặt đất | IGNORE | Không vẽ |
| Không xác định hazard thuộc xe nào (hai xe chồng lấn) | ESCALATE object | Group với xe gần camera hơn theo chiều sâu + `needs_review=true` |
| Không thấy xe chở hàng | ESCALATE object | Hazard không Group + `needs_review=true` |
| Cả ảnh quá tối / nhoè, không kết luận được | ESCALATE ảnh | Tag `image_escalate`; vẫn vẽ các case rõ |
| Ảnh không có phần nhô nào | IGNORE cả ảnh | Không box, không tag |

**Cấm:** gộp phần nhô vào box xe "cho nhanh"; bỏ qua phần nhô vì "chỉ hé một chút" khi nó ≥ 8%.

## 8. Temporal rule

Không áp dụng. Mỗi ảnh là một quyết định độc lập, dùng **Shape**. Không suy luận cửa "sắp đóng" hay hàng "sắp rơi";
không dùng ảnh khác để quyết định cho ảnh này.

## 9. Examples

| sample_id | Thấy gì | Expected output | Rule |
|---|---|---|---|
| `OVH01` | Xe tải nhỏ phủ bạt, bó ống thép thò ra sau thùng và lệch sang phải | `vehicle truck has_hazard=true` ôm cabin + thùng tới mép sau thùng; `attached_hazard protruding_load side=rear` từ mép sau thùng tới đầu bó ống; cùng Group. Không có xe nào khác được vẽ | §3 hazard chỉ phần ngoài box xe |
| `OVH02` | Xe máy chở nhiều thùng carton + bao hàng, khối hàng vượt bề ngang tay lái sang phải và ra sau | `vehicle motorcycle` (xe + người lái); hazard `oversized_cargo` cho từng phía vượt ngưỡng (`right`, và `rear` nếu phần sau đạt ngưỡng); Group tất cả | §2 mỗi phía một box |
| `OVH03` | Xe máy chở hai sọt tre hai bên; pickup phía trước chở bồn nước trên thùng | Xe máy: `vehicle motorcycle` + hai hazard `oversized_cargo` `left` và `right`, Group cả ba. Pickup: không vẽ gì — bồn nằm trong bề ngang thùng | §2; §5 hàng chất cao không thò ra |
| `OVH04` | SUV phía trước đang mở cốp sau hất lên; xe tải đỗ bên phải mở cửa thùng sau | SUV: `vehicle car` vẽ như cốp đóng; hazard `open_door side=rear` ôm cánh cốp phần nằm ngoài đường bao xe. Xe tải: `vehicle truck` + hazard `open_door side=rear` cho cánh cửa thùng mở ra ngoài; không vẽ hàng bên trong thùng | §3 cửa mở; §5 hàng trong thùng không vẽ |
| `OVH10` | Ô tô đỗ sát lề phải, cửa tài xế mở ra phía lòng đường | `vehicle car` theo thân xe khi cửa đóng; hazard `open_door side=left` (cửa tài xế là bên trái của xe); Group | §4 side theo thân xe |

## 10. Common mistakes

1. Một box to bao cả xe lẫn hàng / cửa mở. Luôn tách hai box.
2. Box hazard bao cả xe, hoặc bao phần hàng vẫn nằm trong thùng.
3. Quên Group hoặc quên tick `has_hazard`.
4. Chọn `side` theo camera thay vì theo thân xe (xe ngược chiều là hay sai nhất).
5. Vẽ hazard cho hàng chất cao không thò khỏi mép; vẽ `vehicle` cho xe không có hazard.
6. Bỏ qua cửa / cốp đang mở vì nghĩ "cửa không phải hàng" — cửa mở là `open_door`, trong scope.
7. Box xe máy không gồm người lái.
8. Để sót `__undefined__`. Quét bằng **Attribute annotation** trước khi lưu.

**Checklist trước khi Save:** có hazard thật không (so ngưỡng 12% / 15 px)? → box xe là đường bao chuẩn, hazard chỉ
phần ngoài? → đủ `vehicle_type`, `hazard_type`, `side`? → Group đúng xe, `has_hazard` đã tick? → case nào cần
`needs_review` / `image_escalate`?
