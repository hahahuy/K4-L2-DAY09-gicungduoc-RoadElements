# Peer feedback + owner response

Phần 1 do **nhóm peer** trả lời (gửi kèm file export). Phần 2 do **nhóm owner** điền.

- **Nhóm peer:** Hoa Thanh Que
- **Người label blind:** Hoàng Văn Nam

## 1. Peer trả lời

1. Rule nào rõ nhất / giúp quyết định nhanh nhất? Quy tắc phân tách `vehicle` (box theo thân xe chuẩn) và `attached_hazard` (chỉ vẽ phần thò ngoài).
2. Rule nào mơ hồ hoặc phải tự suy diễn? Trường hợp hàng thò ra bị xe khác che một phần (OVH14), chưa rõ có cần ước lượng phần bị che hay không.
3. Sample nào khiến guideline "vỡ"? OVH16 khi cửa xe hé mở ở khoảng cách xa, sát ngưỡng 10%.
4. Attribute / default nào trong CVAT dễ gây thao tác sai? Dropdown `side` nếu quên chọn sẽ giữ `__undefined__`.
5. Một thay đổi cụ thể giúp annotator mới ít hỏi hơn? Bổ sung hình ảnh minh hoạ cho các trường hợp hàng chở bị che khuất một phần.

## 2. Owner phân loại

Owner không tranh luận để bảo vệ guideline. Mỗi feedback và mỗi decision peer làm sai được xếp vào một hướng xử lý.

| Feedback / decision sai | Nguyên nhân (guideline gap / data ambiguity / execution error) | Xử lý (accept + revise / reject with evidence / add escalation rule) | Bằng chứng |
|---|---|---|---|
| Mơ hồ khi hàng thò bị che một phần | guideline_gap | accept + revise (thêm quy tắc chỉ vẽ phần nhìn thấy và đánh dấu needs_review) | `clarification_log.csv`, OVH14 |
| Phân vân cửa xe hé xa sát ngưỡng | data_ambiguity | add escalation rule (hướng dẫn đánh dấu tag image_escalate khi khó quyết định) | OVH16 |
