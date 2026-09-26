
# Annotation guideline — Boundary & Occlusion Edge-cases for Vehicle Hazards

**Version:** v0

> DRAFT — Bản này dùng để nhóm thống nhất cách gắn nhãn trước khi tạo guideline v1.
> Các rule về boundary, taxonomy và uncertainty chưa được freeze.
> Sau khi nhóm review và thống nhất, đổi Version thành v1.

---

## 1. Objective + scope

### Mục tiêu

Task tập trung vào các phương tiện có phần nhô hoặc phần mở ra ngoài thân xe,
có thể làm tăng vùng chiếm chỗ thực tế của phương tiện.

Các trường hợp nhóm muốn nghiên cứu:

- Xe tải chở sắt/thép/gỗ hoặc hàng hóa nhô ra phía trước, phía sau hoặc hai bên.
- Xe máy chở hàng cồng kềnh.
- Ô tô/van/truck có cửa đang mở.
- Phần hàng hóa hoặc vật thể gắn với xe bị che khuất một phần.
- Vật thể nằm gần xe nhưng không rõ có thực sự thuộc về xe hay không.

### Câu hỏi chính của guideline

Khi vehicle có phần nhô nguy hiểm, annotator nên:

- vẽ 1 bounding box lớn bao cả vehicle và phần nhô,

hay

- vẽ riêng bbox `vehicle` và bbox `attached_hazard`?

### Hướng dự kiến của nhóm ở v0

Nhóm đang nghiêng về phương án:

- `vehicle`: bbox riêng cho thân phương tiện;
- `attached_hazard`: bbox riêng cho phần nhô nguy hiểm.

Lý do cần kiểm chứng qua calibration:
nếu gộp hazard vào bbox vehicle, kích thước bbox của vehicle có thể bị thay đổi lớn.

### Ngoài scope dự kiến

- Người đi bộ.
- Biển báo.
- Vạch đường.
- Vật thể không liên quan nằm gần xe.
- Bóng đổ.
- Reflection.
- Các bộ phận bình thường của xe không tạo ra phần nhô bất thường.

---

## 2. Annotation unit

Task sử dụng ảnh tĩnh.

Đơn vị annotation dự kiến là từng object instance trong mỗi ảnh.

Hai loại instance đang được xem xét:

1. `vehicle`
2. `attached_hazard`

Một phương tiện được tính là một instance `vehicle`.

Một phần nhô nguy hiểm được tính là một instance `attached_hazard`
nếu có đủ bằng chứng cho thấy nó liên quan trực tiếp tới vehicle.

### Câu hỏi cần chốt trước v1

- Một cụm nhiều thanh thép nhô cùng hướng sẽ là một hazard hay nhiều hazard?
- Hai phần hàng nhô tách biệt có cần hai bbox riêng không?
- Cửa xe mở có được coi là `attached_hazard` giống hàng hóa hay cần class riêng?

---

## 3. Geometry rule

Geometry dự kiến:

**Rectangle / Bounding Box**

### Vehicle

Bbox dự kiến ôm phần thân chính của phương tiện.

Ở v0, nhóm chưa freeze việc bbox sẽ:

- chỉ theo phần nhìn thấy;
- hay suy đoán phần bị che.

Hướng ưu tiên hiện tại:

**visible bounding box** — không đoán phần bị che hoàn toàn.

### Attached hazard

Bbox dự kiến ôm phần vật thể nhô ra ngoài thân xe.

Rule cần kiểm chứng:

- Có chỉ bbox phần nhô ra ngoài hay bbox toàn bộ cargo?
- Hazard và vehicle có được overlap bbox hay không?
- Khi boundary giữa cargo và vehicle khó thấy thì xử lý thế nào?

### Rule đang được đề xuất

Không kéo bbox `vehicle` để bao toàn bộ phần hazard.

Thay vào đó:

    [ vehicle ] + [ attached_hazard ]

Rule này chưa freeze ở v0 và sẽ được kiểm tra bằng calibration.

---

## 4. Taxonomy

Taxonomy dự kiến:

### Label 1 — `vehicle`

Dùng cho thân phương tiện.

Có thể có attribute:

`vehicle_type`

Giá trị dự kiến:

- car
- truck
- bus
- motorcycle
- other
- unknown

### Label 2 — `attached_hazard`

Dùng cho phần nhô/mở bất thường.

Attribute dự kiến:

`hazard_type`

Giá trị:

- cargo_overhang
- oversized_load
- open_door
- other
- unknown

Có thể thêm:

`certainty`

Giá trị:

- clear
- uncertain

### Chưa chốt ở v0

Nhóm cần quyết định trước v1:

- Có cần label riêng cho `open_door` hay chỉ dùng attribute?
- Có cần một label/tag riêng để đánh dấu trường hợp cần review không?
- `unknown` dùng cho unknown subtype hay dùng cho cả trường hợp chưa chắc object có phải hazard?

Taxonomy cuối cùng phải khớp với:

`03_ontology_and_cvat_setup.md`

và:

`03_cvat_labels.json`

---

## 5. Inclusion / exclusion

### Dự kiến INCLUDE

Annotate vehicle/hazard nếu:

- Nhìn thấy rõ phương tiện.
- Có vật thể nhô đáng kể ra ngoài thân xe.
- Hàng hóa lớn hơn boundary thông thường của vehicle.
- Cửa xe đang mở ra ngoài.
- Hazard bị che một phần nhưng vẫn nhận biết được.

### Dự kiến EXCLUDE

Không coi các object sau là attached hazard:

- Gương chiếu hậu thông thường.
- Bánh xe.
- Cản xe bình thường.
- Bóng đổ.
- Reflection.
- Một vehicle khác đứng sát.
- Vật thể nằm gần xe nhưng không có bằng chứng liên quan.

### Điểm cần calibration

Khái niệm:

**"nhô đáng kể"**

chưa có threshold định lượng ở v0.

Nhóm cần xem ảnh thực tế để quyết định có cần threshold rõ hơn hay chỉ cần rule định tính.

---

## 6. Visibility / occlusion

### Occlusion một phần

Hướng dự kiến:

Nếu vẫn nhận biết được object:

→ vẫn annotation.

Nếu không nhìn thấy đầy đủ boundary:

→ không tự suy đoán quá mức phần bị che.

### Truncated bởi mép ảnh

Nếu object bị cắt bởi mép ảnh nhưng vẫn nhận biết được:

→ dự kiến vẫn annotation.

BBox kết thúc ở mép ảnh.

### Object nhỏ / xa

Nếu object quá nhỏ để phân biệt rõ:

→ chưa quyết định LABEL / IGNORE / UNKNOWN ở v0.

Cần calibration để thống nhất.

### Reflection

Dự kiến:

→ không annotation reflection như object thật.

---

## 7. Ambiguity / escalation

Ở v0, nhóm xác định có bốn loại quyết định cần guideline v1 làm rõ:

### LABEL

Khi đủ bằng chứng object thuộc scope.

### IGNORE

Khi đủ bằng chứng object không thuộc scope.

### UNKNOWN

Khi chắc chắn đây là object thuộc scope nhưng không xác định được subtype hoặc attribute.

Ví dụ dự kiến:

- chắc chắn là cargo hazard,
- nhưng không biết nên gọi là `cargo_overhang` hay `oversized_load`.

### ESCALATE

Khi evidence không đủ để biết có nên label hay không.

Ví dụ:

- một vật dài nằm phía sau truck;
- vị trí tiếp xúc với truck bị che;
- không thể biết đó là cargo của truck hay object phía sau.

### Việc phải chốt trước v1

Cần quyết định cách biểu diễn ESCALATE trong CVAT, ví dụ:

- attribute;
- tag;
- hoặc label review riêng.

Quyết định này phải xuất hiện được trong CVAT export,
không chỉ ghi chú hoặc nói miệng.

---

## 8. Temporal rule

**Không áp dụng — task ảnh tĩnh.**

Không sử dụng thông tin của frame trước hoặc sau.

Mỗi ảnh được annotation độc lập.

Không dùng track.

---

## 9. Examples / Edge cases cần kiểm chứng

Ở v0 chưa gán `sample_id` thật.

Sau khi chọn ảnh `example` hoặc `calibration`,
thay `TBD` bằng ID thật như `BDDxx`.

Không sử dụng ảnh `blind` làm ví dụ.

| #  | sample_id | Trường hợp                                                    | Hướng xử lý dự kiến ở v0   | Điều cần kiểm chứng                         |
| -- | --------- | ---------------------------------------------------------------- | --------------------------------- | ------------------------------------------------ |
| 1  | TBD       | Xe bình thường, không có phần nhô                         | Chỉ`vehicle`                   | Xác định baseline bbox vehicle                |
| 2  | TBD       | Xe tải có thanh thép/hàng dài nhô phía sau                | `vehicle` + `attached_hazard` | Hazard bbox chỉ phần nhô hay toàn bộ cargo? |
| 3  | TBD       | Xe máy chở hàng rộng sang hai bên                           | `vehicle` + `attached_hazard` | Thế nào là "oversized"?                       |
| 4  | TBD       | Ô tô đang mở cửa                                            | `vehicle` + hazard cho cửa     | Open door có cùng label với cargo không?     |
| 5  | TBD       | Hazard bị vehicle khác che một phần                          | Vẫn label phần nhìn thấy      | Visible bbox hay amodal bbox?                    |
| 6  | TBD       | Hazard đi ra ngoài mép ảnh                                   | Bbox đến mép ảnh              | Có cần attribute truncated không?             |
| 7  | TBD       | Vật dài sát phía sau xe nhưng không thấy điểm gắn      | ESCALATE                          | Cách biểu diễn escalation trong CVAT          |
| 8  | TBD       | Vật nằm gần vehicle nhưng rõ ràng không gắn với vehicle | IGNORE                            | Có cần lưu dấu quyết định ignore không?  |
| 9  | TBD       | Chắc chắn có hazard nhưng không biết loại                 | `hazard_type=unknown`           | Phân biệt UNKNOWN và ESCALATE                 |
| 10 | TBD       | Hai phần hàng nhô tách biệt trên cùng vehicle             | Có thể dùng 2 hazard bbox      | Khi nào split thành instance mới?             |

### 8 edge case tối thiểu của nhóm

Tối thiểu cần giữ các case:

1. Cargo nhô phía sau.
2. Hàng cồng kềnh hai bên.
3. Cửa xe mở.
4. Occlusion.
5. Truncation ở mép ảnh.
6. Không rõ object có gắn với vehicle.
7. Object gần xe nhưng không liên quan.
8. Nhiều hazard / boundary khó xác định.

Các case này sẽ tiếp tục được đưa vào `edge_case_cards.md`.
Bài yêu cầu cuối buổi có ít nhất 8 trường hợp khó.

---

## 10. Common mistakes — giả thuyết ở v0

Các lỗi nhóm dự đoán annotator có thể mắc:

1. Gộp vehicle và phần nhô vào một bbox duy nhất.
2. Bbox vehicle quá rộng vì bao luôn cargo.
3. Bỏ sót cargo nhỏ nhưng nhô rõ ra ngoài.
4. Coi gương hoặc bộ phận bình thường của xe là hazard.
5. Coi object nằm gần vehicle là attached hazard.
6. Đoán boundary của phần bị occluded.
7. Không label cửa xe đang mở.
8. Dùng `unknown` cho mọi trường hợp không chắc.
9. Gộp nhiều hazard tách biệt thành một bbox lớn.
10. Dùng thông tin từ ảnh/frame khác để suy luận.

Các lỗi này mới là giả thuyết ở v0.

Sau calibration, nhóm sẽ xem lỗi nào thực sự xảy ra để sửa guideline v1/v2.
