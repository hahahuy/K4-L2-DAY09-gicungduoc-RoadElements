
# Annotation guideline — Boundary & Occlusion Edge-cases for Vehicle Hazards

**Version:** v1

## 1. Objective + scope

Mục tiêu của task là gắn nhãn các phương tiện và các phần nhô/mở nguy hiểm làm
tăng vùng chiếm chỗ thực tế của phương tiện trên đường.

Các trường hợp chính trong scope:

- Xe tải chở sắt, thép, gỗ hoặc hàng hóa nhô ra ngoài thân xe.
- Xe máy/xe đạp máy chở hàng cồng kềnh vượt ra ngoài boundary thông thường.
- Ô tô, xe tải hoặc van có cửa đang mở ra ngoài.
- Vật thể được gắn, buộc hoặc chở trên phương tiện và nhô rõ ra ngoài thân xe.
- Các trường hợp bị che khuất hoặc bị cắt bởi mép ảnh nhưng vẫn đủ bằng chứng để
  xác định vehicle/hazard.

Mục tiêu của annotation là:

1. Giữ bounding box `vehicle` phản ánh thân chính của phương tiện.
2. Không làm bbox vehicle bị phình to vì hàng hóa hoặc cửa mở.
3. Biểu diễn riêng phần nguy hiểm bằng label `attached_hazard`.
4. Có cách đánh dấu rõ ràng các trường hợp không chắc chắn để reviewer kiểm tra.

Ngoài scope:

- Người đi bộ.
- Biển báo.
- Vạch đường.
- Vật nằm gần xe nhưng không có bằng chứng là gắn với xe.
- Bóng đổ và phản chiếu.
- Các bộ phận bình thường của phương tiện như gương, cản xe hoặc bánh xe.

---

## 2. Annotation unit

Task sử dụng **ảnh tĩnh**.

Đơn vị annotation là từng instance nhìn thấy trong một ảnh.

Mỗi phương tiện là một instance `vehicle` riêng.

Mỗi phần nhô nguy hiểm độc lập là một instance `attached_hazard` riêng.

Một object được tính là instance mới khi:

- thuộc một phương tiện khác; hoặc
- là một hazard tách biệt rõ ràng về không gian với hazard khác.

Ví dụ:

- Một xe tải chở một cụm thanh thép liên tục nhô ra phía sau:
  → một `vehicle` + một `attached_hazard`.
- Một xe tải có một bó thép nhô phía sau và một vật lớn nhô riêng sang bên trái:
  → một `vehicle` + hai `attached_hazard`.

Không sử dụng tracking và không nối object giữa các ảnh.

---

## 3. Geometry rule

Sử dụng **Rectangle / Bounding Box**.

### 3.1 Vehicle

Bounding box `vehicle` phải:

- ôm sát phần thân chính nhìn thấy của phương tiện;
- không chứa khoảng nền thừa lớn;
- không mở rộng để bao cả hàng hóa nhô ra;
- không mở rộng để bao cửa đang mở;
- không suy đoán phần thân bị che hoàn toàn.

Quy tắc chính:

**Vehicle bbox chỉ biểu diễn thân phương tiện, không bao gồm phần nhô nguy hiểm.**

### 3.2 Attached hazard

Bounding box `attached_hazard` phải:

- ôm sát phần hazard nhìn thấy;
- tập trung vào phần vượt ra ngoài boundary thông thường của thân xe;
- không bao gồm thân vehicle nếu có thể tách boundary rõ ràng;
- kết thúc tại mép ảnh nếu hazard bị cắt bởi frame.

### 3.3 Visible boundary

Task sử dụng **visible bounding box**, không sử dụng amodal bounding box.

Không kéo box qua vùng bị che dựa trên suy đoán.

Nếu object bị che một phần, bbox chỉ dựa trên phần có thể quan sát hợp lý.

### 3.4 Không gộp Vehicle + Hazard

Không được vẽ một bbox `vehicle` lớn bao cả thân xe và phần hazard.

Sai:

    [ vehicle + cargo overhang ]

Đúng:

    [ vehicle ] [ attached_hazard ]

Hai bbox có thể chạm hoặc chồng nhẹ nếu boundary thực tế bị che, nhưng không cố ý
gộp hai object thành một bbox.

---

## 4. Taxonomy

### 4.1 Label: `vehicle`

Geometry: Rectangle

Attribute:

`vehicle_type`

Allowed values:

- `car`
- `truck`
- `bus`
- `motorcycle`
- `other`
- `unknown`

Default:

`unknown`

Chỉ dùng `unknown` khi nhìn thấy chắc chắn đó là một phương tiện nhưng không đủ
thông tin để phân loại loại xe.

### 4.2 Label: `attached_hazard`

Geometry: Rectangle

Attribute:

`hazard_type`

Allowed values:

- `cargo_overhang`
- `oversized_load`
- `open_door`
- `other`
- `unknown`

Giải thích:

- `cargo_overhang`: hàng dài nhô ra ngoài thân xe, ví dụ thép/gỗ.
- `oversized_load`: hàng cồng kềnh làm tăng đáng kể chiều rộng hoặc chiều cao.
- `open_door`: cửa phương tiện đang mở.
- `other`: phần nhô nguy hiểm rõ ràng nhưng không thuộc ba loại trên.
- `unknown`: chắc chắn có hazard nhưng không xác định được loại.

Attribute:

`certainty`

Allowed values:

- `clear`
- `uncertain`

Default:

`clear`

### 4.3 Label: `review_region`

Geometry: Rectangle

Dùng để biểu diễn các candidate mà annotator quyết định IGNORE hoặc ESCALATE,
để quyết định vẫn xuất hiện trong CVAT export.

Attribute:

`decision`

Allowed values:

- `ignore`
- `escalate`

Attribute:

`reason`

Allowed values:

- `not_attached`
- `too_occluded`
- `too_small`
- `ambiguous_parent`
- `ambiguous_boundary`
- `other`

Taxonomy trong file này phải khớp với `03_ontology_and_cvat_setup.md` và
`03_cvat_labels.json`.

---

## 5. Inclusion / exclusion

### INCLUDE — bắt buộc label

Tạo `vehicle` cho phương tiện nhìn thấy đủ để nhận biết.

Tạo `attached_hazard` nếu:

1. Có bằng chứng rõ ràng hazard thuộc/gắn/chở trên phương tiện; và
2. Hazard vượt đáng kể ra ngoài boundary thông thường của thân vehicle.

Bao gồm:

- Thanh sắt/thép/gỗ nhô khỏi xe tải.
- Hàng dài nhô phía sau xe.
- Hàng cồng kềnh rộng hơn thân xe máy.
- Hàng hóa nhô sang một bên.
- Cửa xe mở rõ ràng.
- Hazard bị che một phần nhưng vẫn nhận diện được.

### EXCLUDE — không tạo `attached_hazard`

Không tạo hazard cho:

- Gương chiếu hậu bình thường.
- Cản trước hoặc cản sau bình thường.
- Bánh xe.
- Roof rack trống không tạo phần nhô đáng kể.
- Vật nằm trên mặt đường gần phương tiện.
- Một phương tiện khác đứng sát.
- Bóng đổ.
- Reflection trong kính/gương.
- Vật không có đủ bằng chứng cho thấy đang gắn/chở trên vehicle.

Nếu có một candidate nhưng kết luận phải bỏ qua, dùng `review_region` với
`decision=ignore`.

---

## 6. Visibility / occlusion

### 6.1 Bị che một phần

Nếu vehicle/hazard bị che một phần nhưng vẫn nhận biết được:

→ vẫn label.

Không suy đoán boundary bị che hoàn toàn.

### 6.2 Bị cắt bởi mép ảnh

Nếu object bị cắt bởi mép ảnh nhưng phần nhìn thấy đủ để xác định:

→ vẫn label.

BBox kết thúc tại mép ảnh.

Không kéo bbox ra ngoài ảnh.

### 6.3 Quá nhỏ hoặc quá xa

Nếu vẫn xác định chắc chắn object thuộc class nào:

→ label.

Nếu kích thước quá nhỏ làm annotator không thể phân biệt hazard với nhiễu:

→ tạo `review_region`
→ `decision=ignore`
→ `reason=too_small`.

### 6.4 Reflection

Hazard chỉ xuất hiện qua phản chiếu trong kính/gương:

→ không label `attached_hazard`.

Nếu cần ghi nhận candidate đã được xem xét:

→ `review_region`
→ `decision=ignore`
→ `reason=other`.

### 6.5 Occlusion nặng

Nếu chỉ thấy một phần vật thể nhưng không đủ bằng chứng để xác định nó có thuộc
vehicle hay không:

→ không tự suy đoán.
→ dùng `review_region`.
→ `decision=escalate`.
→ `reason=too_occluded` hoặc `ambiguous_parent`.

---

## 7. Ambiguity / escalation

Annotator sử dụng bốn quyết định sau.

### LABEL

Dùng khi đủ bằng chứng.

Trong CVAT:

- tạo bbox `vehicle`; và/hoặc
- tạo bbox `attached_hazard`.

Ví dụ:

Nhìn rõ bó thép được chở trên xe tải và nhô phía sau.

→ LABEL.

### IGNORE

Dùng khi nhìn thấy candidate nhưng guideline xác định nó không thuộc scope.

Trong CVAT:

- vẽ `review_region` quanh candidate;
- `decision=ignore`;
- chọn `reason` tương ứng.

Ví dụ:

Một thùng hàng nằm trên mặt đường sát xe nhưng không có bằng chứng gắn với xe.

→ IGNORE.

### UNKNOWN

Dùng khi chắc chắn đây là hazard nhưng không xác định được subtype.

Trong CVAT:

- tạo `attached_hazard`;
- `hazard_type=unknown`;
- `certainty=uncertain`.

UNKNOWN không dùng cho trường hợp chưa chắc object có phải hazard hay không.

### ESCALATE

Dùng khi evidence không đủ để quyết định LABEL hoặc IGNORE.

Trong CVAT:

- tạo `review_region`;
- `decision=escalate`;
- chọn `reason`.

Ví dụ:

Một vật dài xuất hiện phía sau xe tải nhưng điểm nối bị che hoàn toàn nên không biết
đó là hàng trên xe hay object phía sau.

→ ESCALATE.

Không giải quyết ambiguity bằng suy đoán.

---

## 8. Temporal rule

**Không áp dụng — task ảnh tĩnh.**

Không sử dụng frame trước hoặc frame sau để suy luận.

Mỗi ảnh phải được quyết định chỉ dựa trên thông tin nhìn thấy trong chính ảnh đó.

Không sử dụng track.

---

## 9. Examples

Lưu ý: thay `<BDDxx>` bằng `sample_id` thật thuộc split `example` hoặc
`calibration`. Không sử dụng ảnh thuộc split `blind`.

| sample_id   | Thấy gì                                                                          | Expected output                                                                                  | Rule áp dụng      |
| ----------- | ---------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------ | ------------------- |
| `<BDDxx>` | Xe tải bình thường, không có hàng nhô                                      | 1 bbox`vehicle`; không có `attached_hazard`                                                | Normal / Inclusion  |
| `<BDDxx>` | Xe tải có bó thép dài nhô rõ phía sau                                      | 1`vehicle` + 1 `attached_hazard`, `hazard_type=cargo_overhang`, `certainty=clear`        | Cargo overhang      |
| `<BDDxx>` | Xe máy chở hàng rộng đáng kể sang hai bên                                  | 1`vehicle` + bbox hazard cho phần hàng vượt khỏi thân xe, `hazard_type=oversized_load` | Oversized load      |
| `<BDDxx>` | Ô tô đang mở cửa ra phía đường                                            | 1`vehicle` + 1 bbox quanh phần cửa mở, `hazard_type=open_door`                            | Open door           |
| `<BDDxx>` | Bó hàng nhô bị một xe khác che một phần nhưng vẫn nhận biết được    | Vẫn tạo`attached_hazard`; bbox theo phần nhìn thấy; không đoán phần bị che           | Occlusion           |
| `<BDDxx>` | Vật dài nhô khỏi xe và tiếp tục ra ngoài mép ảnh                         | `attached_hazard` kết thúc tại mép ảnh; không suy đoán phần ngoài frame              | Truncation          |
| `<BDDxx>` | Một vật dài nằm sát phía sau xe nhưng không thấy điểm gắn              | `review_region`, `decision=escalate`, `reason=ambiguous_parent`                            | Ambiguity           |
| `<BDDxx>` | Một thùng/hộp nằm trên đường cạnh xe nhưng rõ ràng không gắn với xe | `review_region`, `decision=ignore`, `reason=not_attached`; không tạo `attached_hazard` | Exclusion           |
| `<BDDxx>` | Hazard chắc chắn tồn tại nhưng quá mờ để biết là loại hàng nào       | `attached_hazard`, `hazard_type=unknown`, `certainty=uncertain`                            | Unknown             |
| `<BDDxx>` | Hai phần hàng nhô tách biệt rõ ràng khỏi cùng một xe                     | 1`vehicle` + 2 bbox `attached_hazard` riêng                                                 | Instance separation |

---

## 10. Common mistakes

### Mistake 1 — Gộp vehicle và hazard thành một bbox

Sai:

- kéo bbox vehicle bao cả thanh thép/hàng/cửa mở.

Đúng:

- bbox `vehicle` cho thân xe;
- bbox `attached_hazard` riêng.

### Mistake 2 — Vẽ toàn bộ cargo thay vì phần gây protrusion

Nếu cargo nằm một phần trong thân xe và chỉ một phần nhô ra:

- ưu tiên bbox phần hazard nhìn thấy vượt ra ngoài boundary của vehicle;
- không bao toàn bộ vehicle vào bbox hazard.

### Mistake 3 — Coi mọi vật gần xe là attached hazard

Khoảng cách gần không chứng minh quan hệ.

Nếu không đủ bằng chứng:

→ ESCALATE.

### Mistake 4 — Gắn gương/cản/bánh xe thành hazard

Các bộ phận bình thường của vehicle không phải `attached_hazard`.

### Mistake 5 — Bỏ qua cửa xe mở

Cửa mở làm tăng vùng chiếm chỗ bên ngoài thân xe:

→ phải tạo `attached_hazard`, `hazard_type=open_door`.

### Mistake 6 — Đoán phần bị occluded

Không dùng amodal bbox.

Chỉ dựa trên phần nhìn thấy.

### Mistake 7 — Kéo bbox ra ngoài mép ảnh

BBox phải dừng tại boundary của ảnh.

### Mistake 8 — Dùng `unknown` thay cho mọi trường hợp khó

`unknown` chỉ dùng khi chắc chắn object là hazard nhưng không xác định được subtype.

Nếu chưa chắc object có phải hazard hoặc thuộc vehicle nào:

→ ESCALATE.

### Mistake 9 — Gộp hai hazard tách biệt

Hai phần hazard có khoảng cách rõ ràng:

→ hai bbox riêng.

### Mistake 10 — Dùng thông tin từ frame khác

Đây là task ảnh tĩnh.

Không suy luận từ ảnh trước/sau.
