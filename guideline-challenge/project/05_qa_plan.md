# QA plan + quality gates

## Flow

Guideline → Calibration → Production → Self-QC → Review → Rework → Quality Gate.

- **Ai review, review bao nhiêu:** QA owner review **100% box `attached_hazard`**, **100% xe có `has_hazard=true`**,
  **100% object `needs_review`**, và **20% ảnh** còn lại chọn ngẫu nhiên (tối thiểu 5 ảnh mỗi batch) để tìm hazard bị
  bỏ sót. Annotator mới: review 100% ở 20 ảnh đầu.
- **Chọn sample theo rule nào:** ưu tiên theo rủi ro — ảnh có xe tải/xe ba gác/xe máy chở hàng, ảnh có ô tô đỗ ven
  đường (dễ có cửa mở bị bỏ sót), ảnh đêm, rồi mới random.
- **Self-QC trước khi nộp:** annotator bật **Color by: Group** kiểm từng hazard đã cùng màu với một xe; quét
  **Attribute annotation** để không còn `__undefined__`.
- **Issue được ghi ở đâu, đóng thế nào:** mỗi issue một dòng trong bảng issue của batch (sample_id, object,
  severity, mô tả, người sửa). Chỉ đóng khi annotator sửa **và** reviewer xác nhận lại trên CVAT.
- **Khi phát hiện guideline gap:** ghi issue loại `Question`. Cùng một gap ≥ 2 lần thì spec owner thêm rule/ví dụ vào
  `02_guideline.md`, tăng version, ghi `08_revision_log.md`, dán lại Guide trên CVAT.

## Defect severity

| Severity | Định nghĩa cho project này | Ví dụ | Action mặc định |
|---|---|---|---|
| Critical | Bỏ sót hazard ≥ ngưỡng ở xe trong/sát làn xe mình; hoặc box xe phía trước bị phình vì gộp hazard | Sắt thép thò sau xe tải phía trước không có box hazard | Rework ngay, re-review 100% batch của annotator đó |
| Major | Sai liên kết, sai `hazard_type`/`side`, bỏ sót hazard ở xe xa, gộp hazard vào box xe ở xe xa | Hazard group nhầm sang xe bên cạnh; `side` theo hướng camera | Rework object, tính vào metric |
| Minor | Geometry vượt tolerance; thiếu `occluded`/`truncated` | Box hazard lệch 6 px; hở 8 px so với mép xe | Sửa khi rework, không chặn batch |
| Question | Guideline không trả lời được | Người đứng trên thùng xe tải có phải hazard không | Ghi issue, spec owner quyết định trong 1 ngày |

## Metrics

| Metric | Cách tính | Vì sao phù hợp với bài toán |
|---|---|---|
| Hazard recall | số hazard ≥ ngưỡng được vẽ / số hazard reviewer tìm thấy | Đo trực tiếp failure critical |
| Hazard recall (trong làn) | như trên, chỉ tính xe trong/sát làn xe mình | Tách riêng phần rủi ro cao |
| Link accuracy | số hazard có Group đúng xe / tổng hazard | Liên kết sai làm planner gắn không gian vào nhầm xe |
| Inflated-box rate | số box xe gồm cả phần nhô / số xe có hazard | Đo lỗi làm sai kích thước chuẩn |
| Attribute accuracy | số hazard đúng cả `hazard_type` và `side` / tổng hazard | Downstream xử lý theo loại và phía |
| Undefined rate | số object còn `__undefined__` / tổng object | Bắt lỗi quên gán do default |
| Escalation rate | số object `needs_review` / tổng object | Quá cao thì ngưỡng 10% chưa đủ rõ |

Metric high-risk tách riêng: **critical defect escape rate** = số lỗi critical reviewer bỏ lọt (phát hiện ở audit
sau) / tổng lỗi critical.

## Quality gate

```text
PASS if:
  critical defects = 0 trong phần review
  AND hazard recall >= 95% AND hazard recall (trong làn) = 100%
  AND link accuracy >= 98%
  AND inflated-box rate <= 2%
  AND attribute accuracy >= 90%
  AND undefined rate = 0%
REWORK if: có critical defect, hoặc link accuracy 90–98%, hoặc attribute accuracy 80–90%
REJECT / ESCALATE if: hazard recall < 85%, hoặc inflated-box rate > 10%, hoặc escalation rate > 30%
  (coi là guideline gap: sửa ngưỡng/ví dụ trước khi label tiếp)
```

Trade-off: Review 100% hazard tốn công nhưng hazard hiếm (vài phần trăm số xe), nên tổng khối lượng nhỏ, và đây là
chỗ lỗi critical. Recall trong làn đặt 100% vì một hazard bỏ sót phía trước đã đủ gây tai nạn. Attribute accuracy chỉ
90% vì `side` của xe đi xiên góc khó xác định bằng mắt; phần sát ranh giới đã được đẩy sang `needs_review`.
