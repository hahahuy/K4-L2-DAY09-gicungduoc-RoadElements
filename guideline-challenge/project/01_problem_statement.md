# Problem statement + downstream contract

## Bài toán

Khi xe có **phần nhô nguy hiểm** — hàng/vật liệu thò ra ngoài thùng xe tải, hàng cồng kềnh trên xe máy/xe ba gác,
cửa ô tô đang mở — annotator phải vẽ **box xe theo đúng kích thước thân xe** và **box riêng cho phần nhô**, rồi
**liên kết** hai box với nhau. Khó ở chỗ ranh giới "đâu là thân xe, đâu là phần nhô" và ngưỡng "nhô bao nhiêu thì
phải vẽ".

## Downstream contract

1. **Downstream task / model / user là ai?** (a) Detector + bộ ước lượng kích thước/theo dõi xe: cần box xe có kích
   thước **chuẩn** (không bị phình vì hàng hoặc cửa). (b) Module lập kế hoạch đường đi (planner): cần biết **không
   gian bị chiếm thêm** bởi phần nhô để giữ khoảng cách an toàn.
2. **Output annotation nào thực sự cần?** Box `vehicle` (kèm `vehicle_type`, `has_hazard`), box `attached_hazard`
   (kèm `hazard_type`, `side`), **liên kết** hazard ↔ vehicle bằng Group của CVAT, và `needs_review` / tag
   `image_escalate` để escalate.
3. **Failure nào gây hậu quả lớn nhất?** **Bỏ sót phần nhô** ở xe trong hoặc sát làn xe mình (ego) — ví dụ sắt thép
   thò sau xe tải phía trước, cửa ô tô mở về phía lòng đường. Planner sẽ tính sai khoảng trống và có thể đâm vào.
   Đây là decision `critical`. Gộp phần nhô vào box xe (làm phình kích thước xe) là `major`.
4. **Khi ambiguity không resolve được, ai / ở đâu là escalation path?** Annotator vẫn vẽ box hazard khi nghi ngờ và
   tick `needs_review`. Nếu cả ảnh không xác định được (quá tối, bị che quá nhiều) thì thêm tag `image_escalate`. QA
   owner xử lý theo `05_qa_plan.md`.

## Scope

- **Trong scope:** ô tô, xe tải, bus, xe máy, xe ba gác/xe đẩy hàng, xe đạp. Phần nhô gồm: hàng/vật liệu thò ra ngoài
  thân/thùng xe (trước, sau, hai bên), hàng cồng kềnh vượt bề ngang xe máy/xe ba gác, cửa xe (cửa bên, cốp, cửa sau
  xe tải) đang mở ra ngoài thân xe.
- **Ngoài scope (không vẽ):** hàng chất cao trên nóc/thùng nhưng **không** thò ra khỏi mép trước/sau/bên; gương chiếu
  hậu; người bước xuống xe; phản chiếu; xe trong ảnh quảng cáo.
- **Geometry tolerance:** mỗi cạnh box lệch ≤ 3 px là đạt; vật cao < 40 px thì lệch ≤ 10% chiều cao là đạt. Box
  `attached_hazard` phải **chạm hoặc chồng ≤ 5 px** lên mép box xe ở phía nhô ra.

## Output chấm được

LABEL (box `vehicle` + `attached_hazard` đúng loại, đúng phía), IGNORE (không vẽ hazard cho hàng không thò ra),
UNKNOWN (`hazard_type=other`), ESCALATE (`needs_review=true` hoặc tag `image_escalate`), liên kết (`has_hazard=true`
trên xe + hai box cùng Group), và decision geometry (box xe không bị phình). Tất cả nằm trong export
**CVAT for images 1.1**.

## Dữ liệu và giới hạn

Ảnh `data/` gốc của lab không có cảnh phần nhô; giảng viên cho phép dùng **16 ảnh ngoài** (đường phố Việt Nam do
nhóm chụp hoặc thu thập hợp pháp), đăng ký vào `data/overhang/` bằng `add_images.py` với sample_id `OVH01`–`OVH16`
theo danh sách cảnh trong `HUONG_DAN_ANH.md`. Giới hạn: ảnh tĩnh nên không biết cửa đang mở ra hay đóng lại; số ảnh ít
nên mỗi loại hazard chỉ có 3–5 ảnh.
