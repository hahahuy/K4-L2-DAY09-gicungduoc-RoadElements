# Problem statement + downstream contract

## Bài toán

Phát hiện **hàng hóa cồng kềnh nhô phía sau phương tiện đang lưu thông** trong ảnh đường phố góc nhìn tài xế. Khó khăn chính là tách phần hàng nhô ra khỏi thân xe gốc trong ảnh đơn mà không nhầm với vật thể nền hoặc phần thân xe.

## Downstream contract

1. **Downstream task / model / user là ai?** Hai nhóm dùng kết quả. Nhóm 3D object detection/depth estimation cần box `Vehicle` ôm sát thân xe nguyên bản để dùng kích thước chuẩn của xe ước lượng khoảng cách. Nhóm motion planning/obstacle avoidance cần `Attached_Hazard` để xác định không gian chiếm dụng thực tế và vùng va chạm phía sau xe khi bám đuôi.
2. **Output annotation nào thực sự cần?** Mỗi xe có hàng hóa nhô rõ ràng phía sau được vẽ một box `Vehicle` chỉ cho thân xe gốc và một box `Attached_Hazard` ôm sát khối hàng nhô. Nếu nhiều kiện hàng tạo thành một khối nhô liên tục, dùng một box gộp. Trên `Attached_Hazard`, chỉ ghi `Parent_ID` của `Vehicle` gốc. Hazard luôn là hàng cồng kềnh nhô phía sau, nên không cần thuộc tính loại hoặc hướng.
3. **Failure nào gây hậu quả lớn nhất?** Critical nhất là bỏ sót `Attached_Hazard` (false negative): hệ thống coi vùng nguy hiểm phía sau xe là khoảng trống và có thể va chạm. Major là gộp cả xe và phần hàng vào một box `Vehicle`, làm sai kích thước/quỹ đạo xe. Major nữa là thiếu `Parent_ID`, khiến hệ thống hiểu nhầm phần hàng là chướng ngại tĩnh thay vì di chuyển cùng xe.
4. **Khi ambiguity không resolve được, ai / ở đâu là escalation path?** Chỉ label khi nhìn rõ xe gốc, khối hàng nhô phía sau, và quan hệ gắn giữa chúng. Nếu không phân biệt được với vật thể nền, vật thể trong xe hoặc phần thân xe thì `IGNORE`; không tạo nhãn suy đoán. Chỉ tạo Issue trên CVAT bằng *Open an issue* khi case được chọn để QA/Lead thảo luận, theo mẫu: `[Frame #<n> - Object #<id>] Không rõ <lý do>. Đã IGNORE theo rule bằng chứng không đủ.` QA/Project Lead quyết định và đóng issue.

## Scope

- **Trong scope (bắt buộc label):** Hàng hóa cồng kềnh hoặc vật liệu dài gắn với xe ô tô, xe tải hoặc xe máy và nhô rõ ràng phía sau thân xe, ước lượng trên 20 cm. Chỉ label khi nhìn thấy đồng thời xe gốc, phần hàng nhô và quan hệ gắn giữa chúng.
- **Ngoài scope (ignore):** Cửa/cốp/bửng mở, vật nhô hai bên xe, gương chiếu hậu tiêu chuẩn, ô/dù, vật thể nằm hoàn toàn trong thùng/khoang xe, người đi bộ, vật thể nền như biển báo/cây/thùng rác, và mọi vật thể không đủ bằng chứng là hàng gắn với xe.
- **Geometry tolerance:** Bounding box theo phần nhìn thấy, ôm sát biên ngoài của thân xe hoặc phần nhô; không bao gồm nền/không khí không thuộc vật thể. Sai lệch tối đa 2 px mỗi cạnh ở ảnh gốc được chấp nhận.

## Output chấm được

Blind test kiểm tra: `LABEL` (hai box đúng class, geometry và `Parent_ID`), `IGNORE` (không tạo box cho background, ngoài scope hoặc bằng chứng không đủ), và `ESCALATE` (Issue CVAT có vùng khoanh và comment khi QA cần chốt case). Class, geometry và `Parent_ID` phải xuất hiện trong CVAT export; escalation được kiểm tra trong Issue Tracker của task.

## Dữ liệu và giới hạn

Nguồn ảnh là 26 ảnh dashcam BDD100K có sẵn tại `data/bdd100k/` (1280 x 720), gồm highway, city street và residential, với điều kiện ban ngày, đêm, chạng vạng, mưa và tuyết. Đây là ảnh tĩnh, không có chuỗi frame tương ứng, nên không thể xác nhận chuyển động bằng thời gian; scope chỉ giữ các ca có bằng chứng trực quan rõ ràng. Một số ảnh có thể là negative không có hàng nhô phía sau xe và vẫn được giữ để kiểm tra quyết định `IGNORE`.
