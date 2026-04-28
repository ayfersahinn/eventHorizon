import asyncio
from playwright.async_api import async_playwright
from datetime import datetime


async def get_coderspace_events():
    """
    Coderspace etkinliklerini Playwright ile çeker.
    Site JavaScript tabanlı (SPA) olduğu için headless browser gereklidir.
    
    Kurulum (ilk seferinde):
        pip install playwright
        playwright install chromium
    """
    etkinlikler = []

    print("URL'e gidiliyor: https://coderspace.io/etkinlikler")
    print("Coderspace etkinlikleri JS render ile alınıyor...")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/124.0.0.0 Safari/537.36"
            )
        )
        page = await context.new_page()

        try:
            await page.goto(
                "https://coderspace.io/etkinlikler",
                wait_until="networkidle",
                timeout=30000,
            )

            # Etkinlik kartlarının yüklenmesini bekle
            # Coderspace'de kartlar genellikle article, .event-card veya benzeri bir seçiciyle geliyor
            # Birkaç olası seçiciyi deneyelim
            selectors_to_try = [
                "article",
                "[class*='event']",
                "[class*='card']",
                "a[href*='/etkinlik']",
            ]

            loaded_selector = None
            for selector in selectors_to_try:
                try:
                    await page.wait_for_selector(selector, timeout=5000)
                    loaded_selector = selector
                    break
                except Exception:
                    continue

            if not loaded_selector:
                print("Coderspace: Etkinlik kartları bulunamadı (selector eşleşmedi).")
                await browser.close()
                return etkinlikler

            # Tüm etkinlik linklerini bul
            event_links = await page.eval_on_selector_all(
                "a[href*='/etkinlik']",
                """
                elements => elements.map(el => ({
                    href: el.href,
                    text: el.innerText.trim()
                }))
                """,
            )

            # Sayfanın ham HTML'ini de parse edelim (yedek yöntem)
            # Her kartı ayrı ayrı işle
            cards = await page.query_selector_all(
                "a[href*='/etkinlik'], article, [class*='EventCard'], [class*='event-card']"
            )

            seen_links = set()

            for card in cards:
                try:
                    # Link
                    href = await card.get_attribute("href") or ""
                    if not href:
                        link_el = await card.query_selector("a[href*='/etkinlik']")
                        if link_el:
                            href = await link_el.get_attribute("href") or ""

                    if href and not href.startswith("http"):
                        href = "https://coderspace.io" + href

                    if href in seen_links or not href:
                        continue
                    seen_links.add(href)

                    # Başlık
                    title_el = await card.query_selector(
                        "h1, h2, h3, h4, [class*='title'], [class*='name']"
                    )
                    title = ""
                    if title_el:
                        title = (await title_el.inner_text()).strip()

                    if not title:
                        title = (await card.inner_text()).strip().split("\n")[0]

                    if not title or len(title) < 3:
                        continue

                    # Tarih
                    date_el = await card.query_selector(
    "span.date, div.event-date, [class*='Date'], .post-date"
)
                    tarih = ""
                    if date_el:
                        tarih = (
                            await date_el.get_attribute("datetime")
                            or (await date_el.inner_text()).strip()
                        )

                    # Şehir / Konum
                    location_el = await card.query_selector(
                        "[class*='location'], [class*='city'], [class*='place']"
                    )
                    sehir = "Online"
                    if location_el:
                        sehir = (await location_el.inner_text()).strip() or "Online"

                    # Durum belirleme
                    now = datetime.now()
                    durum = "Yaklaşan"
                    try:
                        if tarih:
                            # ISO tarih veya Türkçe tarih parse denemesi
                            event_dt = datetime.fromisoformat(tarih.replace("Z", "+00:00"))
                            if event_dt.date() < now.date():
                                durum = "Geçmiş"
                            elif event_dt.date() == now.date():
                                durum = "Devam Ediyor"
                    except ValueError:
                        pass

                    etkinlikler.append(
                        {
                            "etkinlik_adi": title,
                            "sehir": sehir,
                            "tarih": tarih or "Belirtilmemiş",
                            "durum": durum,
                            "link": href,
                            "kaynak": "coderspace",
                        }
                    )

                except Exception as e:
                    print(f"Coderspace kart parse hatası: {e}")
                    continue

        except Exception as e:
            print(f"Coderspace scraper hatası: {e}")

        finally:
            await browser.close()

    if not etkinlikler:
        print("Coderspace için etkinlik bulunamadı.")
    else:
        print(f"Coderspace: {len(etkinlikler)} etkinlik bulundu.")

    return etkinlikler


def scrape_coderspace():
    """index.py'den senkron olarak çağrılabilir wrapper."""
    return asyncio.run(get_coderspace_events())


if __name__ == "__main__":
    import json

    results = scrape_coderspace()
    print(json.dumps(results, ensure_ascii=False, indent=2))