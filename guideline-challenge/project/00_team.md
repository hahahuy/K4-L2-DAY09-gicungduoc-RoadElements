# Team

Điền trước phút 15. Thay mọi placeholder; còn sót thì `make status` báo ở gate G1.

- **Team:** gicungduoc
- **Nhóm peer test bài của mình:** Hoa Thanh Que
- **Nhóm mình test bài của:** Hoa Thanh Que
- **Problem family:** Boundary & occlusion edge-cases — phần nhô nguy hiểm (hàng thò ra, hàng cồng kềnh, cửa xe mở): `vehicle` + `attached_hazard` có liên kết
- **Nguồn ảnh:** ảnh ngoài được giảng viên cho phép, đăng ký vào `data/overhang/` (`OVH01`–`OVH16`) bằng `add_images.py`

| Thành viên | GitHub | Vai trò chính | File phụ trách |
|---|---|---|---|
| Nguyễn Văn Tiến (2A202602056) | nvantien24042002 | spec owner | `01`, `02` |
| Nguyễn Đức Tùng (2A202602227) | NDTung23 | CVAT owner | `03_*`, `sample_pack.csv`, `09` |
| Bùi Quang Thái (2A202603020) | ThaiHE1735 | gold owner | `04_edge_cases/` |
| Hà Quang Huy (2A202602263) | hahahuy | QA owner | `05`, `06`, `07_blind_handoff/` |
| Võ Quốc Dinh (2A202602318) | VQuocDinh | revision & review | `08`, hỗ trợ calibration |

Gợi ý chia vai (nhóm 2–3 người thì gộp): **spec owner** (`01`, `02`), **CVAT owner** (`03_*`, `sample_pack.csv`,
`09`), **gold owner** (`04_edge_cases/`), **QA owner** (`05`, `06`, `07_blind_handoff/`). Mỗi file một người sửa
chính để tránh xung đột git. Calibration thì mọi người cùng label.
