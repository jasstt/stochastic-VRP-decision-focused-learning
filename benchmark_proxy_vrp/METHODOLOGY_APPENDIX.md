# Methodology Appendix

## A.1 Neden Bu Ek Var

Bu ek, projenin kendi ürettiği bulguları nasıl denetlediğini gösteren bir vaka analizidir. Amaç sonucu gizlemek değil, doğrulama sürecinin kendisini şeffaf kılmaktır.

Doğrulama zinciri beş rapora dayanır:

- `vroom_comparison_report.md`: OR-Tools ve VROOM ile ilk solver-agnostiklik testi.
- `route_grouping_sensitivity_report.md`: n=4 route grouping tanı sinyali.
- `ordering_vs_grouping_divergence_report.md`: grouping ve ordering etkilerinin ayrıştırılması.
- `grouping_exposure_validation_n20_report.md`: n=20 doğrulama denemesi.
- `false_positive_mechanism_report.md`: n=4 sinyalinin neden yanıltıcı göründüğünün mekanizma analizi.

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
| Solver-agnostiklik | 4 -> 20 instance | Ana interface/feasibility iddiası ayakta; ikincil mekanizma hipotezi n=20 ile düzeltildi. |
| VRP kuantum QAOA sonuçları | n=1 veya tek problem boyutu | Ayrı bir çalışma; aynı ilke geçerli. Bu sonuçlar ölçek kanıtı değil, demo/tanı sonucu olarak okunmalı. |

## A.7 Hangi İddia Ayakta, Hangisi Çöktü

Bu doğrulama zincirinde çöken şey ana solver-agnostiklik iddiası değildir. Çöken şey, stockout farkını route grouping veya ordering divergence ile açıklama hipotezidir.

| İddia | Durum | Kanıt |
|---|---|---|
| Domain'lerin bağıl maliyet sıralaması motor-bağımsız | AYAKTA | 32 domain-engine run kapsandı; provider-level ortalamalarda cold_chain her iki motorda en pahalı, cargo her iki motorda en ucuz domain kaldı. |
| Feasibility motor-bağımsız | AYAKTA | OR-Tools ve VROOM aynı 16 instance-domain koşulunda feasible oldu; 32/32 run tamamlandı, feasibility mismatch görülmedi. |
| Stockout sıralaması motor-bağımsız | KISMEN AYAKTA | Stockout değerleri benzer bantta kaldı, fakat bağıl sıralama değişti: OR-Tools `cold_chain > grocery > cargo > atm`, VROOM `grocery > cold_chain > atm > cargo`. |
| Grouping/ordering divergence stockout farkını açıklıyor | ÇÖKTÜ | n=20'de korelasyon sıfıra yaklaştı, yön korunmadı, bootstrap CI sıfırı kapsadı. |
| `E-n13-k4` kaynaklı sahte korelasyon | KANITLANDI | Cook's Distance 24.12; n20 remainder testinde r yaklaşık 0 ve p>0.5. |

Ana solver-agnostiklik iddiası, yani stochastic decision layer'ın OR-Tools ve VROOM provider interface'leri üzerinden çalışması, feasibility kapsamının eşleşmesi ve domain-level maliyet sıralamasının korunması ayakta kalmıştır. Daha büyük örneklemle sarsılan iddia, bu motor-bağımsızlığın altındaki stockout mekanizmasını route grouping veya ordering divergence ile açıklama girişimiydi.

Sonuç cümlesi:

> Ana solver-agnostiklik iddiası (domain sıralaması ve feasibility motor-bağımsız) ayakta kalmıştır ve daha büyük örneklemle sarsılmamıştır. Çöken iddia, bu motor-bağımsızlığın altındaki mekanizmayı açıklamaya çalışan ikincil bir hipotezdi. Bu ayrım önemlidir: asıl bulgu hâlâ geçerli, sadece "neden" sorusunun cevabı hâlâ açık kalmıştır.

## A.8 Açık Kalan Soru

Stockout sıralamasının motora göre değişmesinin gerçek nedeni hâlâ bilinmiyor. Grouping divergence, ordering divergence ve grouping-exposure farkı bunu n=20 üzerinde açıklamadı.

Olası diğer adaylar:

- Route capacity utilization farkı: motorlar kapasiteyi farklı yoğunlukta dolduruyor olabilir.
- Vehicle count veya aktif rota sayısı farkı: bir motor aynı instance için farklı sayıda etkin rota kullanıyor olabilir.
- Route-level load allocation farkı: aynı toplam yük, farklı route risk profillerine dağılıyor olabilir.
- Objective interaction farkı: domain objective'leri aynı feature'ları farklı ağırlıklarla kullandığı için stockout dışındaki maliyet bileşenleri ana sinyali taşıyor olabilir.

Bu sorunun cevabı için ayrı bir tanı çalışması gerekir. Bu ek, stockout mekanizmasını kapatılmış bir sonuç olarak sunmaz; açık soru olarak bırakır.
