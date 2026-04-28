import asyncio
from playwright.async_api import async_playwright
from datetime import datetime

async def get_techcareer_events():
    """
    Techcareer.net etkinliklerini Playwright ile çeker.
    Bootcamp, Hackathon ve Yarışmaları kapsar.
    """
    etkinlikler = []
    url = "https://www.techcareer.net/events"

    print(f"URL'e gidiliyor: {url}")
    print("Techcareer etkinlikleri JS render ile alınıyor...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
        )
        page = await context.new_page()

        try:
            # Sayfaya git ve içeriğin yüklenmesini bekle
            await page.goto(url, wait_until="domcontentloaded", timeout=30000)
            
            # Etkinlik kartlarını temsil eden seçicileri bekle
            await page.wait_for_selector(".event-card, .card, a[href*='/bootcamp/'], a[href*='/hackathon/']", timeout=10000)

            # Tüm kartları çek
            # Techcareer'de etkinlikler genellikle link (a) etiketidir
            cards = await page.query_selector_all("a[href*='/bootcamp/'], a[href*='/hackathon/'], a[href*='/events/']")

            seen_links = set()

            for card in cards:
                try:
                    # Link çekme
                    href = await card.get_attribute("href") or ""
                    if not href or href in seen_links:
                        continue
                    
                    if not href.startswith("http"):
                        href = "https://www.techcareer.net" + href
                    
                    seen_links.add(href)

                    # Başlık (Title)
                    # Genellikle h3 veya kart içindeki güçlü metinler
                    title_el = await card.query_selector("h2, h3, .title, .event-title")
                    title = (await title_el.inner_text()).strip() if title_el else "Başlık Belirtilmemiş"

                    # Tarih (Date)
                    # Techcareer'de tarihler genellikle badge veya span içinde olur
                    date_el = await card.query_selector(".date, .event-date, span:has-text('2026'), span:has-text('2025')")
                    tarih = (await date_el.inner_text()).strip() if date_el else "Tarih Belirtilmemiş"

                    # Şehir / Tür (Online/Fiziksel)
                    sehir = "Online"
                    if "İstanbul" in title or "Ankara" in title: # Basit bir tahmin
                        sehir = "İstanbul/Ankara"

                    etkinlikler.append({
                        "etkinlik_adi": title,
                        "sehir": sehir,
                        "tarih": tarih,
                        "durum": "Yaklaşan",
                        "link": href,
                        "kaynak": "techcareer"
                    })

                except Exception as e:
                    continue

        except Exception as e:
            print(f"Techcareer scraper hatası: {e}")
        finally:
            await browser.close()

    print(f"Techcareer: {len(etkinlikler)} etkinlik bulundu.")
    return etkinlikler

# index.py içinden çağrılabilmesi için
def scrape_techcareer():
    return asyncio.run(get_techcareer_events())