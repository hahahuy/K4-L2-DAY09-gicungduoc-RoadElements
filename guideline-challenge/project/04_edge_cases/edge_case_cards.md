# Edge-case library

Kho nội bộ của nhóm, **không gửi cho peer**. Card dùng ảnh example/calibration đã được chép rule sang
`02_guideline.md` (§3, §5–§7, §9). Card về ảnh blind chỉ nằm ở đây, decision tương ứng có trong `gold_decisions.csv`.
Mỗi card viết theo cảnh đã lên danh sách trong `HUONG_DAN_ANH.md` — **sửa dòng Observation cho khớp ảnh thật**.

---

CASE ID: EC01
Sample: OVH01
Scene: Xe tải chở sắt thép thò sau thùng
Observation: Bó sắt thò ra khỏi mép sau thùng khoảng 1/4 chiều dài xe
Decision: LABEL
Expected: `vehicle truck has_hazard=true` (thân + thùng); `attached_hazard protruding_load side=rear` từ mép thùng tới đầu bó sắt; cùng Group
Rationale: Box xe chuẩn cho ước lượng kích thước; hazard cho planner (contract câu 1)
Common mistake: Một box to bao cả xe và bó sắt
Diversity: critical

---

CASE ID: EC02
Sample: OVH02
Scene: Ô tô đỗ ven đường mở cửa
Observation: Cửa phía lòng đường mở ra ngoài thân xe
Decision: LABEL
Expected: `vehicle car` theo thân xe đóng cửa; `attached_hazard open_door side=` theo phía cửa **của xe**; Group
Rationale: Cửa mở chiếm thêm làn; side theo thân xe để downstream biết phía bị mở rộng
Common mistake: Chọn side theo hướng camera
Diversity: conflict

---

CASE ID: EC03
Sample: OVH03
Scene: Xe máy chở thùng hàng rộng hơn tay lái
Observation: Hàng vượt bề ngang ở cả hai bên
Decision: LABEL
Expected: `vehicle motorcycle` (xe + người + phần hàng trong bề ngang tay lái); hai hazard `oversized_cargo` left và right; Group cả ba
Rationale: §2 hai phía khác nhau = hai box
Common mistake: Một box hazard bao cả khối hàng lẫn xe
Diversity: conflict

---

CASE ID: EC04
Sample: OVH04
Scene: Xe tải chở hàng chất cao
Observation: Hàng cao hơn cabin nhưng không thò khỏi mép trước/sau/bên
Decision: IGNORE
Expected: Không có `attached_hazard`; nếu vẽ xe thì `has_hazard=false`
Rationale: Downstream cần không gian ngang/dọc, không cần chiều cao (scope §1)
Common mistake: Vẽ hazard `side=top`/`other` cho hàng chất cao
Diversity: negative

---

CASE ID: EC05
Sample: OVH05
Scene: Cửa xe hé mở nhỏ
Observation: Khe cửa mở khoảng 8–12% bề ngang xe
Decision: ESCALATE
Expected: Vẽ `open_door` + `needs_review=true`
Rationale: §7 sát ngưỡng thì nghiêng về vẽ vì bỏ sót nguy hiểm hơn
Common mistake: Bỏ qua vì "chỉ hé"
Diversity: ambiguity / escalation

---

CASE ID: EC06
Sample: OVH06
Scene: Xe máy chở hàng trong dòng xe
Observation: Một phần khối hàng bị xe khác che
Decision: LABEL
Expected: Hazard ôm phần nhìn thấy; `needs_review=true` nếu không thấy điểm xa nhất
Rationale: §6 không đoán phần bị che
Common mistake: Kéo box hazard ra sau vật che để "đoán" kích thước hàng
Diversity: occlusion

---

CASE ID: EC07
Sample: OVH08
Scene: Ô tô mở cốp sau
Observation: Cánh cốp mở lên trên và ra sau
Decision: LABEL
Expected: `open_door side=rear`, ôm phần cánh cốp nằm ngoài thân xe đóng cốp
Rationale: §3 cửa mở chỉ tính phần ngoài thân
Common mistake: Mở rộng box xe lên trên để bao cánh cốp
Diversity: edge

---

CASE ID: EC08
Sample: OVH09
Scene: Xe ba gác chở hàng cồng kềnh
Observation: Hàng vượt cả chiều dài (phía sau) lẫn bề ngang (hai bên)
Decision: LABEL
Expected: `vehicle cart`; hazard riêng cho từng phía nhô vượt ngưỡng; Group tất cả
Rationale: §2 mỗi phía một box để planner biết phía nào bị mở rộng
Common mistake: Một hazard duy nhất bao quanh cả xe
Diversity: conflict

---

CASE ID: EC09
Sample: OVH11
Scene: Ban đêm/ngược sáng
Observation: Hàng thò sau xe chỉ thấy lờ mờ
Decision: LABEL hoặc ESCALATE
Expected: Thấy đường viền → vẽ hazard; không thấy → không vẽ và thêm `image_escalate` nếu cả ảnh không đọc được
Rationale: §6 chỉ vẽ khi phân biệt được đường viền
Common mistake: Đoán hình dạng hàng từ đèn xe
Diversity: low_visibility

---

CASE ID: EC10
Sample: OVH15
Scene: Xe tải phía trước trong làn xe mình
Observation: Vật liệu dài thò ra sau thùng, ngay trước camera
Decision: LABEL
Expected: `attached_hazard protruding_load side=rear` + box xe không phình; Group
Rationale: Bỏ sót hazard trong làn là failure critical (contract câu 3)
Common mistake: Chỉ vẽ box xe to bao luôn vật liệu
Diversity: critical

---
