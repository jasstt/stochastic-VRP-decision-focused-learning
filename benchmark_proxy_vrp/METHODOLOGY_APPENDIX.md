# Methodology Appendix

## A.1 Neden Bu Ek Var

Bu ek, projenin kendi ürettiği bulguları nasıl denetlediğini gösteren bir vaka analizidir. Amaç sonucu gizlemek değil, doğrulama sürecinin kendisini şeffaf kılmaktır.

Doğrulama zinciri şu raporlara dayanır:

- `vroom_comparison_report.md`: OR-Tools ve VROOM ile ilk solver-agnostiklik testi.
- `route_grouping_sensitivity_report.md`: n=4 route grouping tanı sinyali.
- `ordering_vs_grouping_divergence_report.md`: grouping ve ordering etkilerinin ayrıştırılması.
- `grouping_exposure_validation_n20_report.md`: n=20 doğrulama denemesi.
- `false_positive_mechanism_report.md`: n=4 sinyalinin neden yanıltıcı göründüğünün mekanizma analizi.
- `stockout_mechanism_diagnosis_report.md`: A.8'de açık kalan stockout mekanizması için capacity-utilization ve active-vehicle-count tanı testi.
- `x_dataset_expansion_report.md`: CVRPLIB X setinden gerçekten indirilen ve çalıştırılan 24 instance genişlemesi.
- `load_allocation_diagnosis_report.md`: route-level load allocation farkının stockout farkını açıklayıp açıklamadığına dair X-set tanısı.
- `objective_interaction_diagnosis_report.md`: objective bileşen farklarının stockout farkını load allocation'dan bağımsız açıklayıp açıklamadığı.
- `gams_lp_backend_probe_report.md`: GAMS MCP backend'inin mevcut lisansla X ölçeğindeki LP'leri hızlandırıp hızlandıramayacağı.

Bu ek, dağınık görünen bu raporları tek bir metodolojik anlatıya bağlar.

## A.2 İlk Sinyal (n=4)

İlk hipotez şuydu: OR-Tools ve VROOM aynı müşterileri farklı rota gruplarına veya farklı rota içi sıralara koyduğu için, route exposure'a duyarlı domain risk metrikleri değişiyor olabilir.

`route_grouping_sensitivity_report.md` bu hipotezi n=4 üzerinde ilk kez test etti. O rapor, route grouping farkı ile stockout değişimi arasında bir yön sinyali gözlemledi fakat bunu kesin kanıt olarak sunmadı. Rapor açıkça n=4 sınırını belirtti ve sonucu "hipotez oluşturan tanı testi" olarak konumlandırdı.

Daha sonra `ordering_vs_grouping_divergence_report.md` içinde `exposure_rank_diff_from_grouping` ayrıştırılınca daha güçlü görünen bir n=4 sinyali ortaya çıktı:

| Domain | n=4 r | n=4 p |
|---|---:|---:|
| atm | 0.9609 | 0.0391 |
| cargo | 0.9826 | 0.0174 |
| cold_chain | 0.9335 | 0.0665 |
| grocery | 0.9711 | 0.0289 |

Üç domain'de p<0.05 görünmesi dikkat çekiciydi. Ancak bu, rapor zincirinde nihai kanıt değil, daha büyük örneklemle test edilmesi gereken tanı sinyali olarak ele alındı.

## A.3 Doğrulama Denemesi (n=20)

`grouping_exposure_validation_n20_report.md`, aynı ilişkiyi 20 coordinate-capable CVRPLIB instance üzerinde tekrar test etti.

Instance seti şu ilkelerle genişletildi:

- Koordinat içeren CVRPLIB instance'lar seçildi.
- `E-n13-k4` gibi koordinatsız explicit-distance instance'lar n=20 doğrulama setine alınmadı.
- Küçük, orta ve büyük instance boyutları birlikte kullanıldı.
- Kapasite baskısı düşük ve yüksek örnekler birlikte dahil edildi.
- OR-Tools ve VROOM aynı custom-matrix provider hattı üzerinden koşturuldu.

n=20 sonucu n=4 sinyalini korumadı:

| Domain | n=4 r | n=4 p | n=20 r | n=20 p | Yön korundu mu? |
|---|---:|---:|---:|---:|---|
| atm | 0.9609 | 0.0391 | -0.1114 | 0.6399 | hayır |
| cargo | 0.9826 | 0.0174 | -0.1328 | 0.5767 | hayır |
| cold_chain | 0.9335 | 0.0665 | -0.2364 | 0.3155 | hayır |
| grocery | 0.9711 | 0.0289 | -0.2201 | 0.3512 | hayır |

Yön koruması 0/4 domain'de kaldı. Bootstrap sonuçları da aynı yöndedir:

| Domain | Observed r | p-value | Bootstrap 95% CI | Sıfırı kapsıyor mu? |
|---|---:|---:|---|---|
| atm | -0.1114 | 0.6399 | [-0.5002, 0.2196] | evet |
| cargo | -0.1328 | 0.5767 | [-0.5051, 0.1830] | evet |
| cold_chain | -0.2364 | 0.3155 | [-0.6136, 0.1387] | evet |
| grocery | -0.2201 | 0.3512 | [-0.5775, 0.0511] | evet |

Bu nedenle n=4'te güçlü görünen korelasyon n=20 üzerinde istatistiksel destek kazanmadı.

## A.4 Neden Çöktü: Mekanizma

`false_positive_mechanism_report.md`, n=4 sinyalinin mekanizmasını teşhis etti. Ana bulgu: `E-n13-k4` regresyon çizgisini domine eden aşırı etkili noktadır.

`E-n13-k4` için maksimum Cook's Distance değeri 24.1195 çıktı. n=4 için pratik eşik `4/n = 1.0` olduğundan bu değer eşiğin yaklaşık 24 katıdır.

Mekanizma şudur:

- `A-n32-k5` ve `P-n19-k2`: grouping exposure değeri 0.0.
- `B-n31-k5`: grouping exposure değeri 0.0772.
- `E-n13-k4`: grouping exposure değeri 0.3333 ve aynı anda yüksek pozitif stockout farkı.

Bu dört noktalı geometri, regresyon çizgisini tek yüksek-x/high-y noktaya bağladı. Böylece n=4 üzerinde yüksek r ve düşük p-value görüntüsü oluştu.

Leave-one-out analizi de aynı uyarıyı verdi. `E-n13-k4` çıkarılınca bazı domainlerde r=1.0 veya r=-1.0 göründü, fakat bu istatistiksel kanıt değildir; kalan veri üç noktadan ve yalnızca iki unique x seviyesinden oluştuğu için dejenere geometri üretir.

Overlap/remainder karşılaştırması sinyalin illüzyon olduğunu daha net gösterdi:

| Set | Domain | Instance sayısı | Pearson r | p-value |
|---|---:|---:|---:|---:|
| original_n4 | atm | 4 | 0.9609 | 0.0391 |
| n20_remainder | atm | 17 | -0.0662 | 0.8007 |
| original_n4 | cargo | 4 | 0.9826 | 0.0174 |
| n20_remainder | cargo | 17 | -0.0632 | 0.8095 |
| original_n4 | cold_chain | 4 | 0.9335 | 0.0665 |
| n20_remainder | cold_chain | 17 | -0.0944 | 0.7185 |
| original_n4 | grocery | 4 | 0.9711 | 0.0289 |
| n20_remainder | grocery | 17 | -0.1581 | 0.5444 |

Yeni 17 instance'da grouping exposure yüksek değerlere çıkmasına rağmen stockout farkı aynı yönde büyümedi. Bu, n=4 sinyalinin genel bir mekanizma değil, küçük örneklem geometrisi olduğunu gösterir.

## A.5 Genel Kural: Projenin Tüm Bulgularına Uygulanan İlke

> Küçük örneklemli (n<10) korelasyon iddiaları bu projede hiçbir zaman "kanıt" olarak sunulmaz, en fazla "hipotez üretici tanı sinyali" olarak işaretlenir.
> Bir korelasyon iddia edilmeden önce:
> (a) en az 15-20 instance ile tekrarlanmalı,
> (b) en az 3 farklı x (bağımsız değişken) seviyesi olmalı,
> (c) tek bir kategoriden gelen instance oranı toplam örneklemin %25'ini geçmemeli,
> (d) bootstrap güven aralığı sıfırı kapsıyorsa "korelasyon yok" olarak raporlanmalı.

Bu kural sadece route grouping analizi için değil, tüm benchmark bulguları için geçerlidir.

## A.6 Bu İlkenin Projenin Diğer Bulgularına Uygulanması

| Bulgu | Instance/Örneklem Sayısı | Bu Kurala Göre Durum |
|---|---|---|
| OSRM 3-bbox testi | 4 instance x 3 şehir | Sinyal var, kanıt değil. Rapor bunu "tekrarlanabilir erken sinyal" olarak işaretledi. |
| Domain adapter sıralaması (`cargo < atm < ...`) | 4 instance | Yön sinyali var, istatistiksel güç yok. Domain genellemesi için n>=20 gerekir. |
| Solver-agnostiklik | 4 -> 20 -> X24 instance | Interface iddiası ayakta; feasibility iddiası X setinde sınırlı. VROOM 21/24, OR-Tools 16/24 anchor-feasible oldu. |
| VRP kuantum QAOA sonuçları | n=1 veya tek problem boyutu | Ayrı bir çalışma; aynı ilke geçerli. Bu sonuçlar ölçek kanıtı değil, demo/tanı sonucu olarak okunmalı. |

## A.7 Hangi İddia Ayakta, Hangisi Çöktü

Bu doğrulama zincirinde çöken şey ana solver-agnostiklik iddiası değildir. Çöken şey, stockout farkını route grouping veya ordering divergence ile açıklama hipotezidir.

| İddia | Durum | Kanıt |
|---|---|---|
| Domain'lerin bağıl maliyet sıralaması motor-bağımsız | AYAKTA | 32 domain-engine run kapsandı; provider-level ortalamalarda cold_chain her iki motorda en pahalı, cargo her iki motorda en ucuz domain kaldı. |
| Feasibility motor-bağımsız | KISITLI | İlk küçük koşuda mismatch görülmedi; X24 koşusunda VROOM 21/24, OR-Tools 16/24 anchor-feasible oldu. Bu, interface'in çalıştığını ama zor X instance'larında solver/time-limit feasibility eşdeğerliği iddiasının genellenemeyeceğini gösterir. |
| Stockout sıralaması motor-bağımsız | KISMEN AYAKTA | Stockout değerleri benzer bantta kaldı, fakat bağıl sıralama değişti: OR-Tools `cold_chain > grocery > cargo > atm`, VROOM `grocery > cold_chain > atm > cargo`. |
| Grouping/ordering divergence stockout farkını açıklıyor | ÇÖKTÜ | n=20'de korelasyon sıfıra yaklaştı, yön korunmadı, bootstrap CI sıfırı kapsadı. |
| `E-n13-k4` kaynaklı sahte korelasyon | KANITLANDI | Cook's Distance 24.12; n20 remainder testinde r yaklaşık 0 ve p>0.5. |

Ana solver-agnostiklik iddiasının interface kısmı, yani stochastic decision layer'ın OR-Tools ve VROOM provider interface'leri üzerinden çalışması, ayakta kalmıştır. Ancak X24 koşusu feasibility eşdeğerliği iddiasını daraltmıştır: zor ve yüksek capacity-pressure X instance'larında VROOM daha fazla anchor route bulmuştur. Domain-level maliyet sıralaması ortak feasible sette yine korunmuştur; daha büyük örneklemle değişen kısım, hem feasibility kapsamı hem de stockout mekanizmasının açıklamasıdır.

Sonuç cümlesi:

> Solver-agnostic interface iddiası ayaktadır ve domain maliyet sıralaması ortak feasible sette korunmuştur. Ancak feasibility eşdeğerliği X24 üzerinde sınırlıdır; bu yüzden "motor değişse de her instance aynı şekilde feasible olur" cümlesi artık doğru değildir.

## A.8 Açık Kalan Soru

Stockout sıralamasının motora göre değişmesinin gerçek nedeni artık kısmen daraltılmıştır. Grouping divergence, ordering divergence ve grouping-exposure farkı bunu n=20 üzerinde açıklamadı. Capacity utilization ve vehicle count farkı da açıklamadı. X24 genişlemesinden gelen ortak feasible n=16 analizinde ise route-level load allocation güçlü bir aday mekanizma verdi.

Olası diğer adaylar:

- Route capacity utilization farkı: motorlar kapasiteyi farklı yoğunlukta dolduruyor olabilir. `stockout_mechanism_diagnosis_report.md` içinde n=20 üzerinde test edildi; mean utilization farkı tüm domainlerde tek x seviyesine düştüğü için A.5'e göre korelasyon raporlanamadı ve açıklayıcı mekanizma olarak desteklenmedi.
- Vehicle count veya aktif rota sayısı farkı: bir motor aynı instance için farklı sayıda etkin rota kullanıyor olabilir. Aynı raporda test edildi; OR-Tools ve VROOM 20/20 instance'ta aynı aktif araç sayısını kullandı, bu nedenle x-varyasyonu oluşmadı ve bu aday da stockout sıralama değişimini açıklamadı.
- Route-level load allocation farkı: aynı toplam yük, farklı route risk profillerine dağılıyor olabilir. `load_allocation_diagnosis_report.md` içinde X24 setinin ortak feasible n=16 alt kümesinde test edildi. Gini farkı tüm domainlerde pozitif aday sinyal verdi: r aralığı 0.8213-0.9023, p<=9.6e-5, bootstrap CI sıfırı dışladı. Load variance farkı daha da güçlüydü: r aralığı 0.8555-0.9121, p<=2.4e-5, bootstrap CI sıfırı dışladı. Ancak bu daha sonra `load_allocation_causal_test_report.md` içinde müdahale testiyle sınandı ve tek başına nedensel mekanizma olarak doğrulanmadı.
- Objective interaction farkı: domain objective'leri aynı feature'ları farklı ağırlıklarla kullandığı için stockout dışındaki maliyet bileşenleri ana sinyali taşıyor olabilir.

Objective interaction daha sonra `objective_interaction_diagnosis_report.md` içinde test edildi. Ham korelasyonlarda bazı objective bileşenleri stockout farkıyla ilişkili görünse de, `Load Variance Diff` kontrol edilince bağımsız aday sinyal büyük ölçüde kayboldu.

Load allocation son olarak X40 setinde müdahale testiyle sınandı. Bu testte 40 instance'ın 27'si common anchor-feasible kaldı ve route count eşleşti. Hibritler allocation kaynağına değil çoğunlukla route kaynağına yakın kaldı: `OR-Tools route + VROOM allocation` satırlarında allocation-source closer share 0.2184, route-source closer share 0.7816; `VROOM route + OR-Tools allocation` satırlarında allocation-source closer share 0.1379, route-source closer share 0.8621. Bu nedenle A.8 artık "load allocation tek başına kök neden" diye kapatılamaz.

Bu noktada A.8'in doğru durumu: stockout sıralama farkının kök nedeni hâlâ açık, fakat arama alanı daraldı. Sıradaki aday route topology'nin daha ince özellikleridir: route uzunluğu dağılımı, route içi yüksek-demand müşteri konumu, marginal capacity slack ve solver heuristic farkları.

## A.9 İlişkili Hipotezleri Ayrı Test Etmenin Riski

Capacity utilization ve vehicle count testleri metodolojik bir ders üretti. İlk bakışta iki ayrı hipotez gibi görünseler de bağımsız değiller:

```text
mean_utilization = total_route_load / (vehicle_capacity * active_vehicle_count)
```

Aynı instance'ta toplam talep aynıysa ve iki motor aynı sayıda aktif araç kullanıyorsa, instance-level mean utilization matematiksel olarak aynı kalır. Bu yüzden H1 (mean capacity utilization farkı) ve H2 (vehicle count farkı) ayrı ayrı test edildiğinde sahte bir kapsam hissi yaratabilir: iki hipotez koşulmuş gibi görünür, ama biri diğerinin sonucunu büyük ölçüde belirler.

Bu ders sonraki tanılara uygulanmalıdır. İlişkili hipotezler önce bağımlılık grafiğine dökülmeli; sonra aynı matematiksel kaynağı tekrar ölçen metrikler yerine gerçekten yeni bilgi taşıyan metrikler seçilmelidir. Bu turda o yeni bilgi route-level load allocation idi: mean utilization aynı kalırken route yük dağılımı, Gini ve variance üzerinden değişti.

## A.10 Objective Interaction Sonucu

Objective interaction testinde şu predictor farkları incelendi: route cost, planned load total, mean domain loss, mean load penalty loss, mean surplus, mean shortfall ve mean total cost. Hedef değişken yine signed stockout diff idi.

Ham korelasyonlarda cold-chain için `planned_load_total_diff` ve `mean_surplus_diff` aday sinyal verdi. Fakat route-level load allocation zaten güçlü bir mekanizma olduğu için, test ikinci aşamada `Load Variance Diff` kontrol edilerek tekrarlandı. Bu partial korelasyonlarda objective bileşenleri genel olarak bootstrap CI içinde sıfırı kapsadı; yani objective interaction, mevcut X24 ortak-feasible sette load allocation'dan bağımsız güçlü bir açıklama vermedi.

Doğru cümle:

> Objective interaction stockout farkıyla ilişkili olabilir, fakat mevcut X24 tanısında bağımsız ana mekanizma gibi görünmüyor. Ölçülen en güçlü mekanizma route-level load allocation farkıdır.

Henüz doğru olmayan cümle:

> Stockout sıralamasındaki motor farkı esas olarak domain objective ağırlıklarından kaynaklanır.

## A.11 GAMS Backend Dersi

GAMS MCP bağlantısı doğrulandı, ancak kurulu lisans GAMS Demo lisansıdır. X ölçeğine yakın sentetik bir LP probe'u `105 customer x 180 scenario` boyutunda 38,162 satır ve 38,267 sütun üretti. GAMS çözüm aşamasına geçmeden şu lisans limitiyle durdu:

```text
linear models of more than 2000 rows or columns
```

Bu nedenle mevcut ortamda GAMS backend'i proje LP'lerini hızlandırmaz; çünkü model solve edilmeden lisans limitine takılır. GAMS ancak non-demo lisans ve güçlü LP solver'larla, özellikle scenario count 200+ seviyesine çıktığında anlamlı bir hızlandırıcı olabilir.

## A.12 Load Allocation Müdahale Testi

`load_allocation_causal_test_report.md`, load allocation hipotezini korelasyondan müdahaleye taşıdı.

Deney tasarımı:

- OR-Tools route grupları sabit tutuldu, VROOM baseline route-level planlanan yük toplamları OR-Tools route'larına zorlandı.
- VROOM route grupları sabit tutuldu, OR-Tools baseline route-level planlanan yük toplamları VROOM route'larına zorlandı.
- Route etiketleri motorlar arasında anlamsız olduğu için allocation vektörleri büyükten küçüğe sıralanarak eşlendi.
- Aktif route sayısı farklı olan durumlar elendi; X40 koşusunda common-feasible 27 instance'ın tamamında route count eşitti.

Sonuç:

| Müdahale | Feasible satır | Allocation-source closer share | Route-source closer share |
|---|---:|---:|---:|
| OR-Tools route + VROOM allocation | 87/108 | 0.2184 | 0.7816 |
| VROOM route + OR-Tools allocation | 87/108 | 0.1379 | 0.8621 |

Doğru cümle:

> Load allocation, X24 üzerinde güçlü korelasyonel adaydı; fakat X40 müdahale testinde tek başına nedensel mekanizma olarak doğrulanmadı. Hibrit stockout sonuçları çoğunlukla allocation kaynağına değil route kaynağına yakın kaldı.

Henüz doğru olmayan cümle:

> Stockout sıralamasındaki motor farkının kök nedeni route-level load allocation'dır.
