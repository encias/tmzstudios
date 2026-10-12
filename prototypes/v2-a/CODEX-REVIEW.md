# Codex değerlendirmesi — V2 A taslağı (12 Ekim 2026)

Kaynak: codex exec, brief + build.py + 3 kapak görseli. Uygulananlar en altta.


8. **Kart bilgisini iki okunaklı katmana ayır — `.card h2`, `.card .meta`, `.tag`:** Uzun tür metni ile tek satırlık statü aynı sırada sıkışıyor. Başlığı `1.4rem`; metayı `display:grid;gap:6px`; statüyü `white-space:normal;font-size:.75rem;letter-spacing:.04em` yap.

9. **Renk dilini projelerin önüne geçirmeme — `:root`, `.eyebrow`, `.tag`:** Sürekli altın vurgu Wynn’e uyuyor, Gratis’in mor dünyasıyla aynı anlamı taşımıyor. Zemini `#111110`, metni `#f2f0eb` yönünde nötrleştir; vurguyu seçim ve odak durumlarında yoğunlaştır.

10. **Detayı görsel arşivden proje anlatımına dönüştür — `.head`, `.facts`, `.shots`:** Tek fikir cümlesi ve görsel sırası tasarım kararlarını kanıtlamıyor. “Brief → Katkım → İki temel karar → Sonuç” ekle; her seçili görsele neyi gösterdiğini açıklayan kısa `figcaption` yaz.

11. **Görsel ritmini içeriğe göre kur — `.shots figure:nth-child(3n+1)`:** Her üçüncü görseli büyütmek önem sırasını dosya sırasına teslim ediyor. “Genel görünüş / mekânsal ilişki / malzeme detayı” rollerine göre `.shot-wide` ve `.shot-pair` sınıfları ata.

12. **AI yorumunun kanıtını göster — Gratis detay şablonu:** “Yeni yorum 2026” etiketi dönüşümü açıklamıyor. Aynı açıdaki özgün ve yeni görseli yan yana göster; değişenler, korunanlar ve kontrol edilmemiş unsurları belirt; mobilde alt alta okunabilsin.

13. **Dönüş yolunu baştan görünür yap — `.bar`, `.pager`, `data-index`:** İndekse dönüş yalnız sayfa sonunda; filtre korunması da galeri konumunun korunması anlamına gelmiyor. Üste “← İşlere dön” ekle; dönüşte filtre, scroll ve seçilen kart odağı birlikte geri gelsin.

14. **Hareketi kapak sürekliliğine bağla — `.card img`, `.hero`, detay geçişi:** Mevcut `scale(1.03)` A yönünün karakterini tek başına kurmuyor. Seçilen kapak aynı kadrajdan detay kapağına 450–550ms geçsin; metin 120ms sonra 180ms’de belirsin; hareket azaltmada doğrudan geçiş kullan.

15. **Eksik erişim ve içerikleri tamamla — `.bar nav`, `FILTERS`, proje verisi:** CV, üretim yaklaşımı, Grafik & Dijital ve Seya örneği eksik. Mobilde giriş bağlantısını saklama; gerçek içerikle bu alanları ekle; teslimi giriş korunumu, geri dönüş, videosuz kapak ve cihaz testleriyle doğrula.

## Uygulananlar (Claude, 12 Ekim)
- 2: varsayılan etiket "Müşteri için tasarım" (uygulandı mı bilgisi doğrulanmadı, iddia edilmiyor).
- 3, 4: giriş boşluğu ve başlık küçüldü; arayüz cümlesi yerine iş tanımı.
- 5: sütunlar 1 / 2 (761px+) / 3 (1200px+).
- 6: detay kapağı kırpılmıyor (height:auto).
- 8: kart başlığı 1.4rem, meta iki satır, statü sarabiliyor.
- 13: detay sayfası üstünde "← İşlere dön" (filtreyi koruyan bağlantı).

## Sahip kararına bırakılanlar
- 1: açılış videosunu V2'ye bağlamak (sonraki adım).
- 7, 9: tipografi ve palet değişikliği — mevcut Cormorant + Inter çizgisi sahibin seçimi.
- 10–12, 15: proje anlatımı (brief → katkı → karar → sonuç), Gratis özgün/AI karşılaştırması, CV ve Seya içeriği — gerçek bilgi sahipten gelmeli.
- 14: kapaktan detaya paylaşımlı geçiş hareketi — yön seçilince.
