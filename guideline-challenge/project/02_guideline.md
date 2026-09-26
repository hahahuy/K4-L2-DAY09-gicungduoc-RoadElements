# Annotation guideline — Attached Hazard phía sau phương tiện

**Version:** v1

<!--
v0 = chưa có bản nháp. Đổi dòng Version ở trên thành v1 khi xong bản nháp đầu, v2 sau calibration, v3 sau blind
handoff; mỗi lần tăng version ghi một dòng vào 08_revision_log.md. `make freeze` đòi v2 trở lên.

File này là thứ nhóm peer nhận nguyên văn trong blind pack và là Guide dán vào CVAT. Peer KHÔNG nhận
edge_case_cards.md, gold_decisions.csv hay sample_pack.csv. Rule nào peer cần biết phải nằm ở đây.
No hidden rules: rule chỉ giải thích bằng miệng thì coi như không tồn tại.
Ví dụ trong guideline chỉ dùng ảnh split example hoặc calibration, không dùng ảnh blind.
-->

## 1. Objective + scope

Mục tiêu là phát hiện hàng hóa cồng kềnh hoặc vật liệu dài nhô phía sau phương tiện
đang lưu thông trong ảnh đường phố góc nhìn tài xế. Annotation phải tách đúng:

- Thân xe nguyên bản, dùng class `Vehicle`.
- Khối hàng nhô phía sau, dùng class `Attached_Hazard`.

Kết quả được dùng cho hai mục đích: ước lượng kích thước và khoảng cách của xe,
đồng thời xác định phần không gian thực tế bị chiếm dụng phía sau xe để tránh va
chạm.

### Trong scope

Chỉ label khi ảnh cho thấy đồng thời cả ba bằng chứng:

1. Có một phương tiện nhận diện được, gồm ô tô, xe tải hoặc xe máy.
2. Có hàng hóa cồng kềnh hoặc vật liệu dài nhô rõ ràng phía sau thân xe, ước lượng
   lớn hơn 20 cm.
3. Có quan hệ trực quan cho thấy phần nhô được gắn, chở hoặc kéo cùng phương tiện.

### Ngoài scope

Không tạo annotation cho:

- Cửa, cốp hoặc bửng xe đang mở nhưng không có hàng hóa nhô ra.
- Vật nhô sang hai bên xe nhưng không nhô phía sau.
- Gương chiếu hậu tiêu chuẩn, ô/dù hoặc phụ kiện thông thường của xe.
- Vật thể nằm hoàn toàn bên trong thùng hoặc khoang xe.
- Người đi bộ, xe không có hàng nhô phía sau hoặc vật thể nền như biển báo, cây,
  thùng rác.
- Mọi vật thể không đủ bằng chứng để kết luận là hàng hóa gắn với xe.

## 2. Annotation unit

Đơn vị annotation là từng instance trong mỗi ảnh tĩnh. Mỗi phương tiện có hàng nhô
đủ điều kiện tạo hai loại annotation:

- Một box `Vehicle` cho thân xe nguyên bản.
- Một hoặc nhiều box `Attached_Hazard` cho các khối hàng nhô phía sau.

Mỗi phương tiện là một instance riêng. Nếu một phương tiện có nhiều kiện hàng tạo
thành một khối nhô liên tục hoặc cùng chiếm một vùng phía sau xe, gộp thành một
`Attached_Hazard`. Nếu các khối tách rời rõ ràng và không thể coi là một khối liên
tục, tạo một box cho mỗi khối nhưng tất cả phải trỏ về cùng `Parent_ID` của xe.

Không tạo `Vehicle` cho phần hàng, và không tạo `Attached_Hazard` nếu không thể
xác định phương tiện cha.

## 3. Geometry rule

Sử dụng bounding box dạng rectangle trong CVAT.

### Box `Vehicle`

- Box chỉ bao quanh thân xe nguyên bản, không bao gồm hàng nhô phía sau.
- Bao gồm toàn bộ phần thân xe nhìn thấy, kể cả phần bị che một phần bởi hàng hóa
  hoặc vật thể khác nếu vị trí của thân xe có thể xác định chắc chắn.
- Không mở rộng box vào vùng không khí, nền hoặc vùng chỉ thuộc hàng hóa.

### Box `Attached_Hazard`

- Box bao quanh toàn bộ khối hàng nhô phía sau mà có thể nhìn thấy.
- Không bao gồm thân xe, giá đỡ hoặc khoảng không giữa xe và hàng nếu các phần đó
  không phải là hàng hóa.
- Nếu nhiều kiện hàng chạm nhau hoặc tạo thành một khối nhô liên tục, dùng một box
  gộp bao sát toàn bộ khối.

### Quy tắc chung

- Box phải ôm sát biên ngoài của vật thể theo phần nhìn thấy trong ảnh.
- Không dùng box amodal để suy đoán phần bị che hoặc nằm ngoài ảnh.
- Nếu vật thể bị cắt bởi mép ảnh, box dừng tại mép ảnh.
- Sai lệch tối đa chấp nhận được là 2 px trên mỗi cạnh ở ảnh gốc 1280 x 720.
- Khi không thể đặt box sát một cạnh vì bằng chứng hình ảnh không đủ, dùng
  `IGNORE`/`ESCALATE` theo mục 7 thay vì đoán.

## 4. Taxonomy

Task chỉ có hai class dạng rectangle:

| Class | Ý nghĩa | Số lượng mỗi phương tiện |
|---|---|---|
| `Vehicle` | Thân xe nguyên bản, không gồm phần hàng nhô | Một |
| `Attached_Hazard` | Hàng hóa cồng kềnh hoặc vật liệu dài nhô phía sau xe | Một hoặc nhiều nếu các khối tách rời rõ ràng |

`Attached_Hazard` phải có attribute `Parent_ID`, là mã định danh của box
`Vehicle` tương ứng trong cùng ảnh. Giá trị phải trỏ duy nhất tới đúng xe cha, ví dụ
`V01`, `V02`.

Quy tắc đặt ID:

- Đánh số các xe từ trái sang phải theo vị trí trung tâm của box `Vehicle`, bắt đầu
  từ `V01`.
- Mỗi `Attached_Hazard` ghi đúng `Parent_ID` của xe mà nó gắn vào.
- Nếu CVAT tự sinh số ID khác với quy ước hiển thị, annotator vẫn phải ghi giá trị
  tham chiếu ổn định theo hướng dẫn của task và kiểm tra lại trong export.
- Không thêm attribute loại hàng, hướng nhô hoặc mức độ nguy hiểm; các thuộc tính
  này không thuộc downstream contract.

## 5. Inclusion / exclusion

### LABEL

Chọn `LABEL` và tạo box cho cả `Vehicle` và `Attached_Hazard` khi:

- Xe gốc nhìn thấy đủ để vẽ box riêng.
- Phần hàng nhô phía sau nhìn thấy rõ và lớn hơn khoảng 20 cm theo ước lượng trong
  ảnh.
- Có bằng chứng trực quan về quan hệ gắn/chở giữa xe và hàng.
- Có thể đặt box với sai lệch không quá 2 px mỗi cạnh.

Nếu có nhiều xe trong ảnh, xử lý độc lập từng xe. Xe không có hàng nhô không cần
label chỉ vì nó xuất hiện trong ảnh.

### IGNORE

Không tạo box cho các trường hợp ngoài scope hoặc thiếu bằng chứng. `IGNORE` được
thể hiện bằng cách không tạo annotation cho vật thể đó; không dùng class giả và
không vẽ box bao quanh nền.

Các trường hợp thường `IGNORE` gồm:

- Không có hàng nhô phía sau.
- Vật thể chỉ nằm trong khoang xe.
- Không chắc vật thể là hàng hóa gắn với xe hay là vật thể nền.
- Không thể tách phần hàng khỏi thân xe hoặc không xác định được xe cha.

## 6. Visibility / occlusion

Chỉ annotate khi phần xe, phần hàng và quan hệ giữa chúng có đủ bằng chứng trực
quan.

- Bị che một phần: vẫn label nếu đường biên còn lại đủ rõ để xác định vật thể và
  đặt box hợp lý. Box vẫn theo phạm vi nhìn thấy, không suy đoán phần khuất.
- Bị cắt bởi mép ảnh: label phần nhìn thấy nếu xe cha và hàng nhô vẫn nhận diện
  được; box dừng tại mép ảnh.
- Xa, quá nhỏ, mờ, loá, phản chiếu hoặc bị bóng tối che đến mức không phân biệt
  được: `IGNORE`, không cố đoán.
- Khi hàng bị che nhưng phần gắn vào xe vẫn không thể xác nhận, `IGNORE` thay vì
  tạo `Attached_Hazard` dựa trên suy luận.
- Không dùng màu sắc, bóng đổ hoặc phản chiếu đơn thuần làm bằng chứng cho một
  hàng hóa.

## 7. Ambiguity / escalation

### Quyết định mặc định

- `LABEL`: đủ bằng chứng, tạo đúng hai class và điền `Parent_ID`.
- `IGNORE`: ngoài scope hoặc bằng chứng không đủ; không tạo box.
- `ESCALATE`: case có ảnh hưởng đến quy tắc chung hoặc QA/Lead cần chốt, nhưng
  annotator không thể tự quyết định nhất quán.

Không dùng `UNKNOWN` cho class hoặc `Parent_ID`. Nếu chưa xác định được xe cha,
không tạo `Attached_Hazard`.

### Khi nào được ESCALATE

Chỉ tạo Issue trên CVAT bằng **Open an issue** khi:

- Không rõ vật thể là hàng nhô hay một phần thân xe/cửa/cốp/bửng.
- Không rõ hàng có gắn với xe hay là vật thể nền phía sau.
- Có nhiều xe chồng lấn và không xác định được `Parent_ID`.
- Case có thể làm thay đổi cách áp dụng guideline cho nhiều ảnh khác.

Trước khi escalation, không tạo annotation suy đoán. Nếu case chỉ là một vật thể
không đủ bằng chứng và không cần QA/Lead thảo luận, áp dụng `IGNORE`.

Mẫu comment Issue:

`[Frame #<n> - Object #<id>] Không rõ <lý do>. Đã IGNORE theo rule bằng chứng không đủ.`

Trong task ảnh tĩnh, `<n>` là số ảnh/frame hiển thị trong CVAT và `<id>` là mã object
nếu CVAT có hiển thị. QA hoặc Project Lead là người quyết định cuối cùng và đóng
Issue. Quyết định `LABEL` được thể hiện bằng box/class/`Parent_ID`; quyết định
`IGNORE` được thể hiện bằng việc không tạo box; `ESCALATE` được thể hiện bằng Issue
trong CVAT Issue Tracker.

## 8. Temporal rule

Không áp dụng — task sử dụng ảnh tĩnh, không có chuỗi frame tương ứng và không dùng
track. Không suy luận chuyển động hoặc quan hệ giữa các ảnh khác nhau.

## 9. Examples

`sample_pack.csv` hiện chưa có sample ID cụ thể. Các ví dụ dưới đây là tình huống
quy tắc để annotator áp dụng trong calibration và blind test.

| sample_id | Thấy gì | Expected output | Rule áp dụng |
|---|---|---|---|
| Chưa có sample ID | Xe tải nhìn thấy rõ, một khối hàng dài nhô phía sau và điểm gắn với thùng xe rõ | Tạo một box `Vehicle` cho thân xe, một box `Attached_Hazard`, `Parent_ID` trỏ về xe | LABEL khi đủ ba bằng chứng trong mục 1 |
| Chưa có sample ID | Một xe máy chở nhiều kiện hàng chạm nhau, tạo thành một khối liên tục phía sau | Một `Vehicle` và một `Attached_Hazard` gộp toàn bộ khối hàng | Gộp các kiện tạo thành một khối nhô liên tục |
| Chưa có sample ID | Xe có cốp hoặc bửng mở nhưng không thấy hàng hóa nhô ra | Không tạo annotation | Cốp/bửng mở đơn thuần ngoài scope |
| Chưa có sample ID | Có vật thể phía sau xe nhưng không biết là hàng gắn với xe hay vật thể nền | Không tạo box; nếu cần QA/Lead chốt thì tạo Issue | Không suy đoán khi quan hệ gắn không rõ |
| Chưa có sample ID | Hàng nhô nhìn thấy nhưng xe cha bị che hoàn toàn hoặc không nhận diện được | Không tạo `Attached_Hazard` | Hazard phải có xe cha xác định được |
| Chưa có sample ID | Hai xe chồng lấn, khối hàng có thể thuộc một trong hai xe và không thể phân biệt | Không tạo box suy đoán; tạo Issue nếu là case cần chốt | Thiếu bằng chứng về `Parent_ID` |

## 10. Common mistakes

- Vẽ một box `Vehicle` bao gồm cả xe và hàng nhô. Luôn tách thân xe và hàng thành
  hai box riêng.
- Vẽ `Attached_Hazard` nhưng quên `Parent_ID`. Kiểm tra từng hazard đều trỏ đúng
  về một `Vehicle` trong cùng ảnh.
- Vẽ box quá rộng, gồm nền, không khí hoặc khoảng trống giữa xe và hàng. Phóng to
  ảnh và bám sát biên ngoài vật thể.
- Dùng một box hazard cho nhiều xe. Mỗi hazard phải thuộc đúng một xe cha.
- Tạo box cho cửa, cốp, bửng mở, gương, ô/dù hoặc vật nằm trong khoang xe. Đây là
  các trường hợp ngoài scope.
- Đánh dấu vật thể nền là hàng hóa chỉ vì nó nằm ngay sau xe. Cần có bằng chứng
  trực quan về quan hệ gắn/chở.
- Suy đoán phần bị che, phần nằm ngoài ảnh hoặc phần không nhìn thấy. Geometry là
  theo phần nhìn thấy, không phải amodal.
- Tạo `Attached_Hazard` khi không xác định được `Vehicle` cha. Trường hợp này phải
  `IGNORE` hoặc `ESCALATE`.
- Tạo nhiều box cho các kiện hàng đã tạo thành một khối liên tục. Khi đó phải gộp
  thành một box hazard.
- Gán ID cha không nhất quán. Đánh số xe từ trái sang phải và kiểm tra lại
  `Parent_ID` trước khi lưu/export.
