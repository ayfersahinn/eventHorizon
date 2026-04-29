import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
import re


def _parse_tarih(tarih_str: str):
    """Tarih stringini datetime objesine çevirmeyi dener, başarısızsa None döner."""
    if not tarih_str:
        return None
    for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y", "%d %B %Y"):
        try:
            return datetime.strptime(tarih_str.strip(), fmt)
        except ValueError:
            continue
    try:
        return datetime.fromisoformat(tarih_str.replace("Z", "+00:00")).replace(tzinfo=None)
    except Exception:
        return None


async def get_coderspace_events():
    etkinlikler = []
    now = datetime.now()

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

        # --- 1. ADIM: Liste sayfasından linkleri topla ---
        list_page = await context.new_page()
        collected_links = []

        try:
            await list_page.goto(
                "https://coderspace.io/etkinlikler",
                wait_until="domcontentloaded",
                timeout=60000,
            )
            await list_page.wait_for_timeout(4000)

            selectors_to_try = [
                "a[href*='/etkinlik']",
                "[class*='EventCard']",
                "[class*='event-card']",
                "[class*='card']",
                "article",
            ]

            loaded_selector = None
            for selector in selectors_to_try:
                try:
                    await list_page.wait_for_selector(selector, timeout=5000)
                    loaded_selector = selector
                    break
                except Exception:
                    continue

            if not loaded_selector:
                print("Coderspace: Etkinlik kartları bulunamadı.")
                await list_page.close()
                await browser.close()
                return etkinlikler

            cards = await list_page.query_selector_all(
                "a[href*='/etkinlik'], [class*='EventCard'], [class*='event-card'], article"
            )

            seen_links = set()

            for card in cards:
                try:
                    href = await card.get_attribute("href") or ""
                    if not href:
                        link_el = await card.query_selector("a[href*='/etkinlik']")
                        href = await link_el.get_attribute("href") if link_el else ""

                    if href and not href.startswith("http"):
                        href = "https://coderspace.io" + href

                    if not href or href in seen_links:
                        continue
                    if href.rstrip("/") == "https://coderspace.io/etkinlikler":
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

                    # Liste kartından tarih okumayı dene → geçmişse atla
                    date_el = await card.query_selector(
                        "time, span.date, div.event-date, [class*='Date'], [class*='date'], .post-date"
                    )
                    liste_tarih = None
                    if date_el:
                        raw = await date_el.get_attribute("datetime") or (await date_el.inner_text()).strip()
                        liste_tarih = _parse_tarih(raw)

                    if liste_tarih and liste_tarih.date() < now.date():
                        print(f"  ⏭ Geçmiş etkinlik atlandı (liste): {title[:50]}")
                        continue

                    collected_links.append({"href": href, "title": title})

                except Exception as e:
                    print(f"Coderspace kart parse hatası: {e}")
                    continue

        except Exception as e:
            print(f"Coderspace liste sayfası hatası: {e}")
        finally:
            await list_page.close()

        print(f"Coderspace: {len(collected_links)} aday link bulundu, detaylar kontrol ediliyor...")

        # --- 2. ADIM: Detay sayfasından gerçek tarihi çek ---
        for item in collected_links:
            detail_page = await context.new_page()
            try:
                await detail_page.goto(
                    item["href"],
                    wait_until="domcontentloaded",
                    timeout=30000,
                )
                await detail_page.wait_for_timeout(2000)

                # Başlık
                title_el = await detail_page.query_selector(
                    "h1, h2, .entry-title, [class*='title'], [class*='Title']"
                )
                title = (await title_el.inner_text()).strip() if title_el else item["title"]

                # Tarih
                tarih = None
                date_selectors = [
                    "time",
                    "[class*='date']",
                    "[class*='Date']",
                    "[class*='time']",
                    "[class*='Time']",
                    ".post-date",
                    "span.date",
                    "[class*='start']",
                    "[class*='Start']",
                ]
                for sel in date_selectors:
                    date_el = await detail_page.query_selector(sel)
                    if date_el:
                        tarih = await date_el.get_attribute("datetime")
                        if not tarih:
                            tarih = (await date_el.inner_text()).strip()
                        if tarih:
                            break

                # Fallback: regex ile body'den tarih ara
                if not tarih:
                    body_text = await detail_page.inner_text("body")
                    match = re.search(
                        r"\b(\d{1,2})[.\s/](\d{1,2}|\w+)[.\s/](\d{4})\b",
                        body_text,
                    )
                    tarih = match.group(0) if match else None

                # Tarih bulunduysa geçmiş kontrolü yap
                if tarih:
                    dt = _parse_tarih(tarih)
                    if dt and dt.date() < now.date():
                        print(f"  ⏭ Geçmiş etkinlik atlandı (detay): {title[:50]}")
                        await detail_page.close()
                        continue
                    durum = "Devam Ediyor" if dt and dt.date() == now.date() else "Yaklaşan"
                else:
                    tarih = "Detay için linke tıklayın"
                    durum = "Yaklaşan"

                # Konum
                location_el = await detail_page.query_selector(
                    "[class*='location'], [class*='city'], [class*='place'], [class*='venue']"
                )
                sehir = (
                    (await location_el.inner_text()).strip() if location_el else "Online"
                )

                etkinlikler.append({
                    "etkinlik_adi": title,
                    "sehir": sehir,
                    "tarih": tarih,
                    "durum": durum,
                    "link": item["href"],
                    "kaynak": "coderspace",
                })
                print(f"  ✓ {title[:50]} → {tarih}")

            except Exception as e:
                print(f"  ✗ Detay sayfası hatası ({item['href']}): {e}")
                etkinlikler.append({
                    "etkinlik_adi": item["title"],
                    "sehir": "Online",
                    "tarih": "Detay için linke tıklayın",
                    "durum": "Yaklaşan",
                    "link": item["href"],
                    "kaynak": "coderspace",
                })
            finally:
                await detail_page.close()

        await browser.close()

    if not etkinlikler:
        print("Coderspace için etkinlik bulunamadı.")
    else:
        print(f"Coderspace: {len(etkinlikler)} etkinlik bulundu.")

    return etkinlikler


def scrape_coderspace():
    return asyncio.run(get_coderspace_events())


if __name__ == "__main__":
    import json
    results = scrape_coderspace()
    print(json.dumps(results, ensure_ascii=False, indent=2))