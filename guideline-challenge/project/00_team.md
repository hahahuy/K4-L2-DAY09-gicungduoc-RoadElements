# Team

Điền trước phút 15. Thay mọi placeholder; còn sót thì `make status` báo ở gate G1.

- **Team:** TODO (ví dụ `team07`)
- **Nhóm peer test bài của mình:** TODO (cặp A ↔ B; số nhóm lẻ thì ring 3 nhóm A → B → C → A — Lab Coach công bố)
- **Nhóm mình test bài của:** TODO
- **Problem family:** Boundary & occlusion edge-cases — phần nhô nguy hiểm (hàng thò ra, hàng cồng kềnh, cửa xe mở): `vehicle` + `attached_hazard` có liên kết
- **Nguồn ảnh:** ảnh ngoài được giảng viên cho phép, đăng ký vào `data/overhang/` (`OVH01`–`OVH16`) bằng `add_images.py`

| Thành viên | GitHub | Vai trò chính | File phụ trách |
|---|---|---|---|
| Nguyễn Văn Tiến (2A202602056) | TODO | spec owner | `01`, `02` |
| Nguyễn Đức Tùng (2A202602227) | TODO | CVAT owner | `03_*`, `sample_pack.csv`, `09` |
| Bùi Quang Thái (2A202603020) | TODO | gold owner | `04_edge_cases/` |
| Hà Quang Huy (2A202602263) | TODO | QA owner | `05`, `06`, `07_blind_handoff/` |
| Võ Quốc Dinh (2A202602318) | TODO | revision & review | `08`, hỗ trợ calibration |

Gợi ý chia vai (nhóm 2–3 người thì gộp): **spec owner** (`01`, `02`), **CVAT owner** (`03_*`, `sample_pack.csv`,
`09`), **gold owner** (`04_edge_cases/`), **QA owner** (`05`, `06`, `07_blind_handoff/`). Mỗi file một người sửa
chính để tránh xung đột git. Calibration thì mọi người cùng label.
