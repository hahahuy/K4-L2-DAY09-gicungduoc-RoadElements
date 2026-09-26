# Annotation guideline — Traffic light state và ego relevance

**Version:** v2

Peer chỉ nhận file này. Rule không viết ở đây thì không tồn tại. Ảnh ví dụ gọi bằng `sample_id` trong catalog (`BDD02`, `LISA16`, …).

## 1. Objective + scope

Annotation này cho planner biết **xe ego phải dừng hay được đi**. Vì vậy mỗi đầu đèn cần ba thứ cùng lúc: màu bóng đang sáng (`state`), kiểu mặt đèn (`direction`), và đèn đó có điều khiển **đúng đường ego đang đi** hay không (`relevance`).

Trong scope: mọi đầu đèn giao thông có vỏ nhìn thấy. Ngoài scope: đèn phanh, xi-nhan, đèn đường, biển quảng cáo, biển tên phố, đèn hiệu cửa hàng, phản chiếu trên mặt đường.

Ego mặc định **đi thẳng trên làn hiện tại**. Chỉ coi ego đang rẽ khi vạch làn trong ảnh cho thấy xe đang ở làn rẽ.

## 2. Annotation unit

- Một ảnh tĩnh = một đơn vị. Không suy `state` từ ảnh khác.
- **Một đầu đèn vật lý = một rectangle** `traffic_light`. Hai bóng trên cùng một vỏ dọc là một đầu đèn, không phải hai box.
- Đèn người đi bộ là một đầu đèn riêng (`direction=pedestrian`), không gộp với đèn xe cạnh nó.
- Tag `image_escalate` gắn cho cả ảnh, không gắn cho từng đèn.

## 3. Geometry rule

Công cụ: **Rectangle**, chế độ **Shape** (pack này là ảnh rời, không phải video).

- Box ôm **vỏ đèn nhìn thấy**, gồm lưỡi che nếu dính liền vỏ.
- Không gồm cột, tay đòn ngang, dây điện, hay biển gắn cạnh đèn.
- Bị che: ôm phần vỏ còn thấy, không vẽ nốt phần khuất.
- Nhiều đầu đèn trên cùng một tay đòn: **mỗi đầu một box**, các box không chồng lên nhau quá 20% diện tích.
- Ngưỡng kích thước: nếu chiều cao box ôm vừa vỏ **dưới 8 px** thì không vẽ (coi là chấm màu, không phải đầu đèn). Từ 8 px trở lên thì vẽ, dù không đọc được màu.

Tolerance: mỗi cạnh lệch tối đa 3 px so với vỏ. Box kéo dài xuống cột là sai, dù attribute đúng.

## 4. Taxonomy

Class: `traffic_light` (rectangle), `image_escalate` (tag). Mọi dropdown mặc định `__undefined__`. Còn `__undefined__` trong export là chưa gán, tính là lỗi. Checkbox `needs_review` mặc định tắt; chỉ bật khi mục 7 bảo bật.

| Label | Attribute | Giá trị | Chọn khi |
|---|---|---|---|
| `traffic_light` | `state` | `red`, `yellow`, `green`, `off`, `unknown` | Màu **bóng đang sáng** của đúng đầu đèn này. Không có bóng sáng nhưng vỏ rõ: `off`. Thấy vỏ mà không đọc được màu: `unknown` |
| | `direction` | `round`, `left`, `right`, `straight`, `pedestrian`, `unknown` | Hình trên mặt đèn. Đèn tròn không mũi tên = `round`. Mũi tên trái/phải/thẳng = `left` / `right` / `straight`. Không thấy mặt đèn: `unknown` |
| | `relevance` | `ego`, `cross`, `unknown` | `ego` chỉ khi đầu đèn điều khiển đúng chuyển động ego đang đi. `cross` khi điều khiển đường cắt ngang, làn rẽ mà ego không ở trong đó, hoặc người đi bộ. Không đủ bằng chứng: `unknown` |
| | `needs_review` | checkbox | Bật đúng các dòng mục 7 ghi ESCALATE. Không bật "cho chắc" trên ca đã rõ |
| `image_escalate` | (không attribute) | tag cả ảnh | Khi **quá nửa** số đầu đèn đạt ngưỡng 8 px có `state=unknown` |

`state` để `mutable=true` vì cùng một đầu đèn đổi màu giữa các frame. Ba attribute kia cố định trên một đầu đèn.

## 5. Inclusion / exclusion

**Vẽ `traffic_light` khi tất cả đều đúng:**

1. Nhìn thấy vỏ đèn (hình chữ nhật tối, thường 3 khoang dọc hoặc ngang), không chỉ một chấm sáng.
2. Chiều cao vỏ quy về box ≥ 8 px.
3. Gán đủ `state`, `direction`, `relevance`. Hết `__undefined__`.

**Không vẽ:**

- Đèn hậu, đèn phanh, xi-nhan, đèn trên nóc taxi.
- Đèn cao áp, đèn đường, đèn cửa sổ, biển sáng của cửa hàng.
- Biển báo (kể cả biển vàng hình thoi, biển tên phố, biển xanh chỉ đường).
- Phản chiếu đèn trên mặt đường ướt hoặc trên nắp capo.
- Chấm xanh/đỏ xa không tách được vỏ, box sẽ thấp hơn 8 px.
- Bóng đèn người đi bộ dạng icon rời không có vỏ 3 khoang: vẫn vẽ **nếu** đó là đầu đèn người đi bộ có vỏ; icon vẽ trên biển hoặc trên cửa hàng thì không vẽ.

Đèn người đi bộ có vỏ: vẽ, `direction=pedestrian`, `relevance=cross` (không điều khiển xe ego).

## 6. Visibility / occlusion

- Che một phần, vẫn thấy vỏ và thấy màu: vẽ phần vỏ còn lại, gán `state` theo bóng thấy, không bật `needs_review`.
- Thấy vỏ, không thấy bóng nào sáng và không đủ tối để kết luận đèn tắt: `state=unknown`, bật `needs_review`.
- Thấy vỏ, rõ ràng không bóng nào sáng (đèn tắt): `state=off`, không bật `needs_review`.
- Mưa, đêm, ngược sáng: vẫn vẽ từng đầu đèn đọc được. Không lấy màu từ đầu đèn bên cạnh. `LISA16` là ca mẫu: mũi tên trái đỏ trong khi hai đầu đèn cạnh đã xanh — ba `state` khác nhau là đúng.
- Không thấy mặt đèn hướng về phía nào (chỉ thấy cạnh hoặc chấm sáng trong đêm): `relevance=unknown`, `direction=unknown`, bật `needs_review`.

## 7. Ambiguity / escalation

Quy tắc relevance, áp dụng theo thứ tự, dừng ở dòng đầu tiên khớp:

1. Không chắc vỏ đèn hay chỉ là chấm sáng / phản chiếu → không vẽ (IGNORE).
2. `direction=pedestrian` → `relevance=cross`.
3. Mũi tên (`left`, `right`, `straight`) và ego **không** ở làn của mũi tên đó → `relevance=cross`.
4. Mũi tên và ego đang ở đúng làn đó, mặt đèn hướng về camera → `relevance=ego`.
5. Đèn `round` hoặc `straight`, mặt hướng về camera, gắn trên lối ego đang đi (trên đầu làn hoặc góc đường phía trước ego) → `relevance=ego`.
6. Đèn quay mặt sang đường vuông góc, hoặc nhìn nghiêng rõ là của đường cắt ngang → `relevance=cross`.
7. Còn lại → `relevance=unknown` và bật `needs_review`. **Cấm mặc định `ego`.**

| Tình huống | Quyết định | Trong CVAT |
|---|---|---|
| Đọc được màu, vỏ ≥ 8 px, relevance chốt được bằng 1–6 | LABEL | box + đủ attribute, `needs_review` tắt |
| Vỏ ≥ 8 px nhưng không đọc được màu | ESCALATE object | vẽ, `state=unknown`, `needs_review` bật |
| Không chốt được relevance (dòng 7) | ESCALATE object | vẽ, `relevance=unknown`, `needs_review` bật |
| Chấm sáng không có vỏ, hoặc phản chiếu mặt đường | IGNORE | không có box |
| Quá nửa đầu đèn ≥ 8 px có `state=unknown` | ESCALATE ảnh | tag `image_escalate`, vẫn giữ các box đọc được |
| Ảnh không có đầu đèn | IGNORE cả ảnh | không box, không tag |

## 8. Temporal rule

Pack nộp dùng **Shape**, mỗi ảnh một quyết định. Nếu sau này dựng clip LISA thành task video thì chuyển sang **Track**, một đầu đèn một track, và chỉ `state` được đổi theo frame (`mutable`).

Khi hai frame LISA cùng nằm trong pack (ví dụ `LISA01` và `LISA16`): đó vẫn là hai ảnh. `state` của frame này không được chép sang frame kia. Cùng một gantry có thể đỏ hết ở frame trước và xanh một phần ở frame sau.

Không nội suy "đèn sắp xanh". Không thấy bóng sáng thì `unknown` hoặc `off`, không đoán theo xe khác đang chạy.

## 9. Examples

| sample_id | Thấy gì | Expected output | Rule |
|---|---|---|---|
| `LISA16` | Ba đầu đèn lớn: mũi tên trái còn đỏ; đèn giữa và đèn phải đã xanh | Ba box. Trái: `state=red`, `direction=left`. Giữa và phải: `state=green`, `direction=round`. Ego đi vào ngã tư không nằm trong làn rẽ trái → trái `relevance=cross`; hai đèn tròn đối diện lối đi thẳng `relevance=ego`. Không tag | §4 state từng đầu; §7 dòng 3 và 5 |
| `BDD15` | Cao tốc, không vỏ đèn; chỉ có xe và biển xanh | Không box, không tag | §5 negative |
| `BDD26` | Đêm, một đèn xanh gần bên trái nhìn rõ vỏ; một đèn đỏ nhỏ xa hơn không thấy hướng mặt | Đèn xanh: `state=green`, `direction=round`, `relevance=ego` nếu mặt hướng về lối ego, ngược lại `unknown` + `needs_review`. Đèn đỏ nếu không thấy hướng mặt: `state=red`, `relevance=unknown`, `needs_review` bật. Không vẽ đèn đường | §6 đêm; §7 dòng 7 |
| `BDD09` | Cao tốc ban ngày, đèn hậu xe phía trước, không có vỏ đèn | Không box, không tag. Đèn hậu không phải `traffic_light` | §5 exclusion |

## 10. Common mistakes

1. Một box bao cả tay đòn và mọi đầu đèn trên đó. Mỗi đầu đèn một box.
2. Box kéo dài theo cột. Box chỉ cao bằng vỏ.
3. Gán `state` theo đầu đèn bên cạnh. `LISA16` chứng minh các đầu đèn trên cùng gantry có thể khác màu.
4. Thấy đèn đỏ là gán `relevance=ego`. Đèn đỏ của đường cắt ngang không bắt ego dừng.
5. Vẽ phản chiếu trên đường ướt, đèn phanh, hoặc biển sáng.
6. Đèn dưới 8 px vẫn vẽ, hoặc đèn đọc được vỏ nhưng bỏ vì "xa".
7. Để `__undefined__`. Quét bằng **Attribute annotation** trước khi lưu.
8. Bật `image_escalate` chỉ vì trời mưa, trong khi các vỏ đèn vẫn đọc được màu. Tag chỉ khi quá nửa số đầu đèn ≥ 8 px có `state=unknown`.
