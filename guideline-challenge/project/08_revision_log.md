# Revision log

Guideline v1 = bản nháp đầu; v2 = sau calibration nội bộ; v3 = sau blind handoff. Mỗi lần tăng `Version` trong
`02_guideline.md`, thêm một hoặc nhiều dòng vào bảng: đổi gì và vì sao, kèm bằng chứng (sample_id, dòng
calibration report, câu hỏi trong clarification log, feedback của peer).

Cột Version ghi dạng `v1`, `v2`, `v3` — `make status` tìm dòng bảng có `v2` và dòng có `v3`.

| Version | Đổi gì | Vì sao | Bằng chứng |
|---|---|---|---|
| v1 | Bản nháp đầu: luôn tách `vehicle` (thân xe chuẩn) + `attached_hazard` (chỉ phần nằm ngoài box xe), liên kết bằng Group + `has_hazard`, ngưỡng nhô ≥ 10% hoặc ≥ 15 px, `side` theo thân xe | Downstream cần kích thước xe chuẩn và không gian bị chiếm thêm; gộp một box làm sai cả hai | `01_problem_statement.md`, EC01, EC02 |
| v2 | Bổ sung quy tắc xác định `side` cho cửa hé mở nhỏ và quy tắc escalation cho ảnh ngược sáng/ban đêm | Kết quả calibration nội bộ cho thấy cần clarify trường hợp sát ngưỡng và khuất tầm nhìn | `06_calibration_report.csv` (OVH05, OVH06, OVH11) |
