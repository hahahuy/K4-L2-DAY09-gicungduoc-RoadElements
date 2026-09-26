# Thu thập ảnh ngoài cho đề tài Overhang (không nộp, chỉ để nhóm làm theo)

Giảng viên cho dùng ảnh ngoài `data/`. `sample_pack.csv` và các ví dụ trong `02_guideline.md` đã đặt sẵn
`OVH01`–`OVH16` theo đúng cảnh dưới đây, nên **ảnh phải đúng cảnh và đúng thứ tự**.

## 1. Chuẩn bị ảnh

- Nguồn: ảnh nhóm tự chụp trên đường (từ camera hành trình hoặc điện thoại đặt ngang tầm xe), hoặc ảnh có license
  cho phép dùng học tập. Ghi nguồn của từng ảnh vào `ATTRIBUTION.txt` (thêm dòng, không xoá dòng cũ).
- **Không** dùng ảnh thấy rõ mặt người hoặc biển số đọc được. Làm mờ trước khi đưa vào repo nếu cần.
- Ảnh ngang, cạnh dài khoảng 1280–1920 px, định dạng `.jpg` hoặc `.png`.
- Đặt tên file có số đứng đầu theo đúng thứ tự bảng dưới: `01_xetai_sat.jpg`, `02_oto_mocua.jpg`, …, `16_...jpg`.
  Script sắp theo tên file, nên số đứng đầu quyết định ảnh nào thành `OVH01`, `OVH02`, …

| ID | Split | Cảnh cần có |
|---|---|---|
| OVH01 | example | Xe tải chở sắt thép/ống thò ra **sau** thùng, nhìn rõ |
| OVH02 | example | Ô tô đỗ ven đường, **cửa bên mở** ra phía lòng đường |
| OVH03 | example | Xe máy chở thùng/bao hàng **rộng hơn tay lái** cả hai bên |
| OVH04 | example | Xe tải chở hàng chất cao nhưng **gọn trong thùng** (không thò ra) |
| OVH05 | calibration | Cửa xe **hé** mở nhỏ |
| OVH06 | calibration | Xe máy chở hàng **bị xe khác che** một phần |
| OVH07 | calibration | Xe chở ống/cây dài thò ra **phía trước** |
| OVH08 | calibration | Ô tô **mở cốp** sau |
| OVH09 | calibration | Xe ba gác chở hàng vượt **cả dài lẫn ngang** |
| OVH10 | calibration | Hàng chất cao trên nóc/thùng, **không thò** khỏi mép |
| OVH11 | calibration | **Ban đêm/ngược sáng**, có hàng thò sau xe |
| OVH12 | blind | Ô tô đỗ mở cửa rõ ràng — **cảnh khác** OVH02 |
| OVH13 | blind | Xe máy chở hàng cồng kềnh **giữa nhiều xe máy khác** |
| OVH14 | blind | Hàng thò ra **bị xe khác che** một phần |
| OVH15 | blind | Xe tải chở vật liệu dài thò ra **ngay phía trước, trong làn** xe mình |
| OVH16 | blind | Cửa hé hoặc hàng buộc **sát mép**, khó quyết định |

Ảnh blind (OVH12–16) **không được** là cùng cảnh/cùng xe với ảnh example/calibration.

## 2. Đăng ký ảnh vào lab

Đặt 16 ảnh vào một thư mục, ví dụ `anh_overhang/`. Trong thư mục `guideline-challenge/` chạy:

```bash
py add_images.py đường\dẫn\tới\anh_overhang
py lab9.py samples
```

Lệnh thứ hai phải liệt kê `OVH01`–`OVH16` với source `overhang`. Kiểm tra bảng `original_name` trong
`data/catalog.csv` khớp đúng thứ tự trên. Commit cả `data/overhang/`, `data/catalog.csv` và `add_images.py`.

## 3. Viết gold sau khi có ảnh

`gold_decisions.csv` chỉ viết được sau khi có ảnh blind thật. Mẫu cho từng ảnh (sửa theo ảnh thật, mở ở **kích thước
gốc** trước khi chốt):

```csv
OVH12,d1,"vehicle car has_hazard=true cho ô tô đỗ (khoảng x=...,y=...); box theo thân xe cửa đóng",major,"§3 box xe chuẩn"
OVH12,d2,"attached_hazard open_door side=<left|right> cùng Group với ô tô ở d1",major,"§4 side theo thân xe; §5 Group"
OVH12,d3,"geometry: box ô tô không gồm cánh cửa mở, lệch ≤3 px mỗi cạnh",minor,"§3; §10 lỗi 1"
OVH13,d1,"attached_hazard oversized_cargo cùng Group với đúng xe máy chở hàng (khoảng x=...), không gắn nhầm xe bên cạnh",major,"§5 liên kết"
OVH14,d1,"attached_hazard protruding_load, needs_review=true (không thấy điểm xa nhất)",major,"§6"
OVH15,d1,"có attached_hazard protruding_load side=rear cho vật liệu thò sau xe tải phía trước",critical,"Bỏ sót hazard trong làn là failure critical"
OVH15,d2,"vehicle truck has_hazard=true và box xe KHÔNG gồm phần vật liệu thò ra",critical,"Box phình làm sai khoảng cách"
OVH16,d1,"ESCALATE: attached_hazard có needs_review=true, hoặc ảnh có tag image_escalate",major,"§7 sát ngưỡng"
```

Cần tối thiểu 10 dòng, ≥ 2 `critical`, ≥ 1 dòng `geometry:`, mỗi ảnh blind ≥ 1 dòng. Ghi chú: `lab9.py score` chỉ
đọc class + attribute, **không đọc Group**. Với decision về liên kết, mở export của peer trong CVAT (GUIDE mục 6,
chọn **Color by: Group**) để chấm bằng mắt.
