# Problem statement + downstream contract

## Bài toán

Phát hiện **phần nhô nguy hiểm gắn với phương tiện đang lưu thông** trong ảnh đường phố góc nhìn tài xế: cửa/cốp/bửng xe đang mở hoặc hàng cồng kềnh thò ra ngoài thân xe. Khó khăn chính là tách phần nhô khỏi thân xe gốc trong ảnh đơn, khi vật thể nhỏ, bị che khuất, ngược sáng hoặc trùng góc nhìn với vật thể nền.

## Downstream contract

1. **Downstream task / model / user là ai?** Hai nhóm dùng kết quả. Nhóm 3D object detection/depth estimation cần box `Vehicle` ôm sát thân xe nguyên bản để dùng kích thước chuẩn của xe ước lượng khoảng cách. Nhóm motion planning/obstacle avoidance cần `Attached_Hazard` để xác định không gian chiếm dụng thực tế và vùng va chạm khi vượt hoặc bám đuôi.
2. **Output annotation nào thực sự cần?** Mỗi phương tiện có phần nhô bất thường được vẽ box `Vehicle` chỉ cho thân xe gốc, và một box `Attached_Hazard` ôm sát phần nhô. Nếu nhiều kiện hàng cùng là một khối nhô ra, dùng một box gộp. Trên `Attached_Hazard`, ghi `Parent_ID` của `Vehicle` gốc, `Hazard_Type` = `Open_Part` hoặc `Oversized_Load`, `Intrusion_Direction` = `Side_Left`, `Side_Right`, hoặc `Rear_Overhang`, và `Uncertain` = `True` khi bằng chứng chưa đủ.
3. **Failure nào gây hậu quả lớn nhất?** Critical nhất là bỏ sót `Attached_Hazard` (false negative): hệ thống coi vùng nguy hiểm là khoảng trống và có thể va chạm. Major là gộp cả xe và phần nhô vào một box `Vehicle`, làm sai kích thước/quỹ đạo xe. Major nữa là thiếu `Parent_ID`, khiến hệ thống hiểu nhầm phần nhô là chướng ngại tĩnh thay vì di chuyển cùng xe.
4. **Khi ambiguity không resolve được, ai / ở đâu là escalation path?** Nếu task là video, kiểm tra 3--5 frame trước/sau: vật thể đi cùng xe là `Attached_Hazard`; đứng yên so với mặt đường là background và không vẽ. Với ảnh tĩnh hoặc vẫn không chắc, ưu tiên an toàn: tạm vẽ `Attached_Hazard`, đặt `Uncertain=True`, rồi tạo Issue trên CVAT bằng *Open an issue* tại vùng nghi ngờ. Comment theo mẫu: `[Frame #<n> - Object #<id>] Không rõ <lý do>. Đã tạm gán Attached_Hazard.` QA/Project Lead quyết định và đóng issue.

## Scope

- **Trong scope (bắt buộc label):** Xe ô tô, xe tải và xe máy có phần nhô nhìn thấy vượt khỏi bao thân xe thông thường (đặc biệt vượt quá gương hoặc ước lượng thò ra trên 20 cm); cửa/cốp/bửng mở; hàng hóa, vật liệu dài hoặc ô/dù gắn trên xe nhô ra hai bên hoặc phía sau.
- **Ngoài scope (ignore):** Gương chiếu hậu tiêu chuẩn, vật thể nằm hoàn toàn trong thùng/khoang xe, người đi bộ không gắn với xe, vật thể nền như biển báo/cây/thùng rác, và vật thể không đủ bằng chứng là gắn với một phương tiện. Trường hợp nghi ngờ thì không ignore mà áp dụng `Uncertain=True` và escalation.
- **Geometry tolerance:** Bounding box theo phần nhìn thấy, ôm sát biên ngoài của thân xe hoặc phần nhô; không bao gồm nền/không khí không thuộc vật thể. Sai lệch tối đa 2 px mỗi cạnh ở ảnh gốc được chấp nhận.

## Output chấm được

Blind test kiểm tra: `LABEL` (hai box đúng class và geometry), `IGNORE` (không tạo box cho background/ngoài scope), `UNKNOWN` (box `Attached_Hazard` với `Uncertain=True`), và `ESCALATE` (Issue CVAT có vùng khoanh và comment). Với mỗi `Attached_Hazard`, đánh giá đủ/sai `Parent_ID`, `Hazard_Type`, `Intrusion_Direction`, và geometry. Tất cả class/attribute xuất hiện trong CVAT export; escalation được kiểm tra trong Issue Tracker của task.

## Dữ liệu và giới hạn

Nguồn ảnh là 26 ảnh dashcam BDD100K có sẵn tại `data/bdd100k/` (1280 x 720), gồm highway, city street và residential, với điều kiện ban ngày, đêm, chạng vạng, mưa và tuyết. Đây là ảnh tĩnh, không có chuỗi frame tương ứng, nên không thể xác nhận chuyển động bằng thời gian; các ca nhập nhằng phải được gắn `Uncertain=True` và escalation trên CVAT. Một số ảnh có thể là negative không có phần nhô nguy hiểm và vẫn được giữ để kiểm tra quyết định `IGNORE`.
