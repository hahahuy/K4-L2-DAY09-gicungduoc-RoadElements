# Checklist bài Lab Day 9 — Overhang Project

> Trạng thái: ✅ Xong · 🔲 Chưa làm · ⚠️ Cần bổ sung

---

## Pha 1 — Team + Problem (G1: Topic Lock) `phút 0–35`

| # | Việc | File | Trạng thái | Ghi chú |
|---|---|---|---|---|
| 1.1 | Điền tên nhóm (ví dụ `team07`) | [00_team.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/00_team.md) L5 | ✅ | gicungduoc |
| 1.2 | Điền nhóm peer test bài mình | [00_team.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/00_team.md) L6 | ✅ | tự tìm |
| 1.3 | Điền nhóm mình test bài | [00_team.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/00_team.md) L7 | ✅ | tự tìm |
| 1.4 | Điền GitHub username 5 thành viên | [00_team.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/00_team.md) L13–17 | ✅ | Đã điền đủ 5 GitHub username |
| 1.5 | Problem statement + downstream contract | [01_problem_statement.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/01_problem_statement.md) | ✅ | Đã viết đầy đủ 4 câu |

---

## Pha 2 — Guideline v1 + Ontology `phút 35–80`

| # | Việc | File | Trạng thái | Ghi chú |
|---|---|---|---|---|
| 2.1 | Guideline 10 mục bắt buộc | [02_guideline.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/02_guideline.md) | ✅ | Đã viết đầy đủ, Version v1 |
| 2.2 | Ontology table đầy đủ | [03_ontology_and_cvat_setup.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/03_ontology_and_cvat_setup.md) | ✅ | 11 dòng + rationale |
| 2.3 | Giải thích class vs attribute | [03_ontology_and_cvat_setup.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/03_ontology_and_cvat_setup.md) | ✅ | Đã viết |
| 2.4 | Bắt đầu edge case cards | [edge_case_cards.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/04_edge_cases/edge_case_cards.md) | ✅ | 10 cards EC01–EC10 |

---

## Pha 3 — CVAT Setup + Sample Pack (G2: CVAT Ready) `phút 80–110`

| # | Việc | File | Trạng thái | Ghi chú |
|---|---|---|---|---|
| 3.1 | `03_cvat_labels.json` khớp ontology | [03_cvat_labels.json](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/03_cvat_labels.json) | ✅ | vehicle + attached_hazard + image_escalate |
| 3.2 | Sample pack đủ ảnh, đúng cấu trúc | [sample_pack.csv](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/sample_pack.csv) | ✅ | 16 ảnh OVH01–16 |
| 3.3 | **Thu thập 16 ảnh thật** theo danh sách cảnh | [HUONG_DAN_ANH.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/HUONG_DAN_ANH.md) | ✅ | Xong |
| 3.4 | Chạy `add_images.py` đăng ký ảnh vào `data/overhang/` | [add_images.py](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/add_images.py) | ✅ | Đã chạy |
| 3.5 | Ghi nguồn ảnh vào ATTRIBUTION.txt | `ATTRIBUTION.txt` | ✅ | Ảnh do AI tạo |
| 3.6 | `make pack SPLIT=calibration` gom ảnh | `build/calibration/` | ✅ | Xong (có 7 ảnh) |
| 3.7 | Tạo task calibration trên CVAT | CVAT localhost:8080 | 🔲 | Mỗi thành viên tạo Tasks |
| 3.8 | Dán `03_cvat_labels.json` vào task (tab Raw) | CVAT | ✅ | Đủ 3 label: vehicle, attached_hazard, image_escalate |
| 3.9 | Dán `02_guideline.md` vào Guide của task | CVAT | ✅ | Thêm tại Task Description của Task  |
| 3.10 | **Điền phiên bản CVAT** | [03_ontology_and_cvat_setup.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/03_ontology_and_cvat_setup.md) L34 | ✅ | CVAT 2.74.1 tại http://localhost:8080 |
| 3.11 | **Điền tên task calibration** | [03_ontology_and_cvat_setup.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/03_ontology_and_cvat_setup.md) L35 | 🔲 | Ví dụ `gicungduoc-calib-v1-tien` |
| 3.12 | **Xác nhận đã dán Guide** | [03_ontology_and_cvat_setup.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/03_ontology_and_cvat_setup.md) L36 | ✅ | Đã có  |
| 3.13 | **Setup test** - Một thành viên chưa tham gia setup và mở Task | [03_ontology_and_cvat_setup.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/03_ontology_and_cvat_setup.md) L44 | ✅ | Sử dụng Guideline để hiểu rõ Tasks |

---

## Pha 4 — Calibration Nội Bộ (G3: Calibration) `phút 120–140`

| # | Việc | File | Trạng thái | Ghi chú |
|---|---|---|---|---|
| 4.1 | Mỗi thành viên label **độc lập** trên CVAT | CVAT | 🔲 | Không nhìn nhau |
| 4.2 | Export mỗi người → `06_calibration_exports/` | `project/06_calibration_exports/` | 🔲 | Ví dụ `tien.zip`, `tung.zip`... |
| 4.3 | Chạy `make calib FILES="..."` đo bất đồng | `06_calibration_measure.csv` | 🔲 | Tool tạo tự động |
| 4.4 | Điền `06_calibration_report.csv` ≥ 3 bất đồng | [06_calibration_report.csv](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/06_calibration_report.csv) | 🔲 | diagnosis + action + rule_change |

---

## Pha 5 — Refine + QA + Gold Freeze (G4: Gold Frozen) `phút 140–160`

| # | Việc | File | Trạng thái | Ghi chú |
|---|---|---|---|---|
| 5.1 | Sửa guideline v1 → **v2** dựa trên calibration | [02_guideline.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/02_guideline.md) L3 | 🔲 | Đổi `v1` → `v2` |
| 5.2 | Ghi dòng **v2** vào revision log | [08_revision_log.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/08_revision_log.md) | 🔲 | Đổi gì, vì sao, bằng chứng |
| 5.3 | QA plan đầy đủ | [05_qa_plan.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/05_qa_plan.md) | ✅ | Flow, severity, metrics, gate đã viết |
| 5.4 | **Viết gold_decisions.csv** cho ảnh blind OVH12–16 | [gold_decisions.csv](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/04_edge_cases/gold_decisions.csv) | 🔲 | **≥ 10 dòng, ≥ 2 critical, ≥ 1 `geometry:`, mỗi ảnh blind ≥ 1 dòng** |
| 5.5 | Chạy `make freeze` (CHỈ 1 NGƯỜI) | `project/FREEZE.txt` + tag `gold-freeze` | 🔲 | Cần guideline ≥ v2 trước |
| 5.6 | Push: `git push --follow-tags` | git | 🔲 | Ngay sau freeze |

---

## Pha 6 — Blind Handoff Test (G5: Handoff Complete) `phút 160–185`

| # | Việc | File | Trạng thái | Ghi chú |
|---|---|---|---|---|
| 6.1 | `make handoff` → tạo `blind-pack.zip` | `handoff/blind-pack.zip` | 🔲 | Gửi cho nhóm peer |
| 6.2 | Nhận export từ peer | `07_blind_handoff/peer_output/` | 🔲 | File zip của peer |
| 6.3 | Ghi clarification log (câu hỏi peer trong blind window) | [clarification_log.csv](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/07_blind_handoff/clarification_log.csv) | 🔲 | Mỗi câu hỏi = 1 dòng |

---

## Pha 7 — Score + Diagnose `phút 185–205`

| # | Việc | File | Trạng thái | Ghi chú |
|---|---|---|---|---|
| 7.1 | `make score FILE=<peer>.zip` | `07_blind_handoff/transfer_score.csv` | 🔲 | Tạo bảng so sánh |
| 7.2 | Điền `correct` (1/0) + `note` từng dòng | `transfer_score.csv` | 🔲 | Geometry → mở CVAT xem |
| 7.3 | `make gts` tính GTS score | `07_blind_handoff/gts_summary.md` | 🔲 | GTS = 0.60D + 0.20C + 0.10G + 0.10I |
| 7.4 | Chép 5 câu feedback peer vào peer_feedback.md | [peer_feedback.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/07_blind_handoff/peer_feedback.md) | 🔲 | Phần 1: peer trả lời |
| 7.5 | Phân loại nguyên nhân + xử lý từng feedback | [peer_feedback.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/07_blind_handoff/peer_feedback.md) | 🔲 | Phần 2: bảng owner |

---

## Pha 8 — Final Revision + Nộp (G6: Final) `phút 205–240`

| # | Việc | File | Trạng thái | Ghi chú |
|---|---|---|---|---|
| 8.1 | Guideline v2 → **v3** dựa trên blind test | [02_guideline.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/02_guideline.md) L3 | 🔲 | Thêm rule/ví dụ từ feedback peer |
| 8.2 | Ghi dòng **v3** vào revision log | [08_revision_log.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/08_revision_log.md) | 🔲 | `make status` kiểm dòng v2 và v3 |
| 8.3 | Edge case cards ≥ 8 (có critical + escalation) | [edge_case_cards.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/04_edge_cases/edge_case_cards.md) | ✅ | Đã có 10 cards |
| 8.4 | Điền `09_cvat_export_or_task_reference.txt` | [09_cvat_export_or_task_reference.txt](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/project/09_cvat_export_or_task_reference.txt) | 🔲 | CVAT version, task tên, export path |
| 8.5 | `make check` báo đủ 6 gate | terminal | 🔲 | Kiểm cuối cùng |
| 8.6 | `git add project && git commit && git push --follow-tags` | git | 🔲 | Nộp bài |

---

## Tóm tắt: Việc PHẢI LÀM TRƯỚC khi đến lab

> [!IMPORTANT]
> Bài lab này dùng **ảnh ngoài** (không dùng ảnh BDD/LISA/GTSDB có sẵn). Nhóm **phải** thu thập 16 ảnh trước hoặc trong buổi lab.

| Ưu tiên | Việc | Ai làm |
|---|---|---|
| ✅ | **Thu thập 16 ảnh** đúng danh sách cảnh trong [HUONG_DAN_ANH.md](file:///d:/vinai-thuc-chien/lab/day9/K4-L2-DAY09-gicungduoc-RoadElements/guideline-challenge/HUONG_DAN_ANH.md) | Cả nhóm |
| ✅ | Đăng ký ảnh: `py add_images.py <thư mục>` → `py lab9.py samples` | CVAT owner (Tùng) |
| 🟡 | Điền GitHub username 5 người | Mỗi người |
| ✅ | Điền tên nhóm, nhóm peer (sau khi Lab Coach công bố) | Tiến |
| 🟢 | Bật CVAT trên máy mỗi người (`docker compose start`) | Mỗi người |

## Tóm tắt: Việc trong buổi lab (theo thứ tự)

| Ưu tiên | Việc | Ai | Phụ thuộc |
|---|---|---|---|
| 🔴 | Calibration: mỗi người label độc lập + export | Cả 5 | Có ảnh + CVAT ready |
| 🔴 | Đo bất đồng + ghi calibration report | Huy (QA) | Export xong |
| 🔴 | Sửa guideline v1 → v2 + revision log v2 | Tiến (spec) | Calibration xong |
| 🔴 | Viết gold_decisions.csv (≥10 dòng, ≥2 critical) | Thái (gold) | Có ảnh blind thật |
| 🔴 | `make freeze` (CHỈ 1 NGƯỜI) | Thái (gold) | v2 + gold xong |
| 🔴 | `make handoff` → gửi peer | Tùng (CVAT) | Freeze xong |
| 🔴 | Nhận export peer → `make score` → điền correct/note | Thái + Huy | Peer gửi export |
| 🔴 | `make gts` + peer_feedback + phân loại | Huy (QA) | Score xong |
| 🔴 | Guideline v2 → v3 + revision log v3 | Tiến (spec) | GTS + feedback |
| 🟡 | Điền `09_cvat_export_or_task_reference.txt` | Tùng (CVAT) | Có task cuối |
| 🟡 | `make check` + commit + push | Dinh (revision) | Mọi thứ xong |

---

## Phân bổ điểm (Rubric 100đ)

| Tiêu chí | Điểm | Trạng thái |
|---|---|---|
| Problem + downstream | 10 | ✅ Đã viết |
| Ontology + CVAT setup | 15 | ⚠️ Ontology xong, CVAT TODO còn nhiều |
| Guideline clarity + completeness | 20 | ⚠️ v1 xong, cần v2 + v3 |
| Edge-case library | 15 | ⚠️ Cards xong, gold_decisions.csv trống |
| QA design + metrics | 15 | ✅ Đã viết đầy đủ |
| Calibration evidence | 5 | 🔲 Chưa label |
| Blind handoff transferability | 20 | 🔲 Chưa bắt đầu |

> [!CAUTION]
> **Critical cap:** Nếu peer mắc critical error vì guideline thiếu/mơ hồ → phần Blind Handoff tối đa **10/20**. Guideline phải rõ ràng!
