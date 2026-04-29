import asyncio
from playwright.async_api import async_playwright

async def get_habitat_events():
    """
    Habitat Derneği eğitim ve etkinliklerini Playwright ile çeker.
    Detay sayfasına girerek gerçek tarihi alır.
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

        # --- 1. ADIM: Liste sayfasından linkleri topla ---
        list_page = await context.new_page()
        collected_links = []

        try:
            await list_page.goto(url, wait_until="domcontentloaded", timeout=60000)
            await list_page.wait_for_selector(
                "article, .elementor-post, a[href*='/egitim/'], a[href*='/etkinlik/']",
                timeout=15000
            )

            cards = await list_page.query_selector_all(
                "article, .elementor-post, a[href*='/egitim/'], a[href*='/etkinlik/']"
            )

            seen_links = set()

            for card in cards:
                try:
                    href = await card.get_attribute("href") or ""
                    if not href:
                        link_el = await card.query_selector("a")
                        href = await link_el.get_attribute("href") if link_el else ""

                    if (
                        not href
                        or href in seen_links
                        or "habitatdernegi.org" not in href
                        or "/egitim-ve-etkinlikler/" in href
                    ):
                        continue

                    seen_links.add(href)

                    # Başlık (liste sayfasından al, detayda doğrulanacak)
                    title_el = await card.query_selector(
                        "h1, h2, h3, .title, .elementor-post__title"
                    )
                    title = (await title_el.inner_text()).strip() if title_el else ""

                    if len(title) < 5:
                        continue

                    collected_links.append({"href": href, "title": title})

                except Exception:
                    continue

        except Exception as e:
            print(f"Habitat liste sayfası hatası: {e}")
        finally:
            await list_page.close()

        print(f"Habitat: {len(collected_links)} link toplandı, detay sayfaları ziyaret ediliyor...")

        # --- 2. ADIM: Her etkinliğin detay sayfasına gir, tarihi çek ---
        for item in collected_links:
            detail_page = await context.new_page()
            try:
                await detail_page.goto(item["href"], wait_until="domcontentloaded", timeout=30000)

                # Başlığı detay sayfasından da almayı dene (daha güvenilir)
                title_el = await detail_page.query_selector("h1, h2, .entry-title, .elementor-heading-title")
                title = (await title_el.inner_text()).strip() if title_el else item["title"]

                # Tarih için birden fazla seçici dene
                tarih = None
                date_selectors = [
                    ".elementor-post-date",
                    ".entry-date",
                    "time",
                    "[class*='date']",
                    "[class*='Date']",
                    ".post-date",
                    "span.date",
                ]

                for sel in date_selectors:
                    date_el = await detail_page.query_selector(sel)
                    if date_el:
                        # Önce datetime attribute'u dene
                        tarih = await date_el.get_attribute("datetime")
                        if not tarih:
                            tarih = (await date_el.inner_text()).strip()
                        if tarih:
                            break

                # Tarih bulunamadıysa sayfanın metninde ara (fallback)
                if not tarih:
                    body_text = await detail_page.inner_text("body")
                    # Türkçe tarih formatını ara: "15 Mayıs 2025", "15.05.2025" gibi
                    import re
                    match = re.search(
                        r"\b(\d{1,2})[.\s/](\d{1,2}|\w+)[.\s/](\d{4})\b",
                        body_text
                    )
                    tarih = match.group(0) if match else "Detay için linke tıklayın"

                # Şehir / konum
                location_el = await detail_page.query_selector(
                    "[class*='location'], [class*='city'], [class*='place'], [class*='venue']"
                )
                sehir = (
                    (await location_el.inner_text()).strip()
                    if location_el
                    else "Online/Türkiye Geneli"
                )

                etkinlikler.append({
                    "etkinlik_adi": title,
                    "sehir": sehir,
                    "tarih": tarih,
                    "durum": "Aktif / Başvuru Açık",
                    "link": item["href"],
                    "kaynak": "habitat",
                })

                print(f"  ✓ {title[:50]} → {tarih}")

            except Exception as e:
                print(f"  ✗ Detay sayfası hatası ({item['href']}): {e}")
                # Hata olsa bile etkinliği ekle, tarih bilinmiyor olarak işaretle
                etkinlikler.append({
                    "etkinlik_adi": item["title"],
                    "sehir": "Online/Türkiye Geneli",
                    "tarih": "Detay için linke tıklayın",
                    "durum": "Aktif / Başvuru Açık",
                    "link": item["href"],
                    "kaynak": "habitat",
                })
            finally:
                await detail_page.close()

        await browser.close()

    print(f"Habitat: {len(etkinlikler)} etkinlik bulundu.")
    return etkinlikler


def scrape_habitat():
    """Senkron wrapper"""
    return asyncio.run(get_habitat_events())