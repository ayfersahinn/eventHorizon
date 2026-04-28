import asyncio
from playwright.async_api import async_playwright

async def get_habitat_events():
    """
    Habitat Derneği eğitim ve etkinliklerini Playwright ile çeker.
    Girişimcilik, dijital dönüşüm ve teknoloji eğitimlerine odaklanır.
    """
    etkinlikler = []
    url = "https://habitatdernegi.org/egitim-ve-etkinlikler/"

    print(f"URL'e gidiliyor: {url}")
    print("Habitat Derneği etkinlikleri alınıyor...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        try:
            # Sayfaya git ve içeriğin yüklenmesini bekle
            await page.goto(url, wait_until="domcontentloaded", timeout=60000)
            
            # Kartların veya liste elemanlarının yüklenmesi için bekle
            # Habitat genellikle elementor veya özel post tipleri kullanır
            await page.wait_for_selector("article, .elementor-post, a[href*='/egitim/'], a[href*='/etkinlik/']", timeout=15000)

            # Sayfadaki etkinlik linklerini ve kartlarını yakala
            cards = await page.query_selector_all("article, .elementor-post, a[href*='/egitim/'], a[href*='/etkinlik/']")

            seen_links = set()

            for card in cards:
                try:
                    # Link çekme
                    href = await card.get_attribute("href") or ""
                    if not href:
                        link_el = await card.query_selector("a")
                        href = await link_el.get_attribute("href") if link_el else ""
                    
                    # Filtre: Sadece eğitim veya etkinlik linklerini al, ana sayfayı/kategorileri dışla
                    if not href or href in seen_links or "habitatdernegi.org" not in href or "/egitim-ve-etkinlikler/" in href:
                        continue
                    
                    seen_links.add(href)

                    # Başlık (Title)
                    title_el = await card.query_selector("h1, h2, h3, .title, .elementor-post__title")
                    title = (await title_el.inner_text()).strip() if title_el else "Habitat Eğitim/Etkinlik"

                    # Tarih (Habitat genellikle meta-data olarak sunar)
                    date_el = await card.query_selector(".elementor-post-date, .date, .time, span")
                    tarih = (await date_el.inner_text()).strip() if date_el else "Detay için sayfayı inceleyin"

                    # Kısa başlıkları (örn: "İncele") atla
                    if len(title) < 5:
                        continue

                    etkinlikler.append({
                        "etkinlik_adi": title,
                        "sehir": "Online/Türkiye Geneli",
                        "tarih": tarih,
                        "durum": "Aktif / Başvuru Açık",
                        "link": href,
                        "kaynak": "habitat"
                    })

                except Exception:
                    continue

        except Exception as e:
            print(f"Habitat scraper hatası: {e}")
        finally:
            await browser.close()

    print(f"Habitat: {len(etkinlikler)} etkinlik bulundu.")
    return etkinlikler

def scrape_habitat():
    """Senkron wrapper"""
    return asyncio.run(get_habitat_events())