import asyncio
import re
from datetime import datetime
import httpx
from filters import clean_text, filter_university_events

GAZIANTEP_EVENTS_URL = "https://gaziantepbilimmerkezi.com/etkinlikler/"
COCUK_KEYWORDS = ["çocuk", "cocuk", "aile", "şenlik", "senlik", "ilkokul", "ortaokul", "lise", "mini", "kids", "bebek"]

def extract_gaziantep_dates(detail_html):
    matches = re.findall(
        r"<strong>\s*([^<]+?)\s*</strong><br>\s*Mekan:\s*([^<]+)<br>",
        detail_html,
        flags=re.IGNORECASE,
    )
    return [
        {
            "tarih": clean_text(date_text),
            "mekan": clean_text(location_text),
        }
        for date_text, location_text in matches
    ]

async def fetch_gaziantep_detail(http_client, item):
    try:
        response = await http_client.get(item["link"])
        response.raise_for_status()
        item["tarih_detaylari"] = extract_gaziantep_dates(response.text)
    except Exception as exc:
        item["detay_hatasi"] = f"{type(exc).__name__}: {exc}"
        item["tarih_detaylari"] = []
    return item

async def scrape_gaziantep_activities():
    print(f"Gaziantep Bilim Merkezi taranıyor...")
    try:
        async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as http_client:
            response = await http_client.get(GAZIANTEP_EVENTS_URL)
            response.raise_for_status()
            html = response.text

            cards = re.findall(
                r'<li class="portfolio-item[^"]*?(category-[^"]*?)?[^"]*?">.*?<div class="image_links hover-title"><a href="([^"]+)" target="_blank">([^<]+)</a></div>.*?</li>',
                html,
                flags=re.DOTALL,
            )

            events = []
            seen_links = set()
            for categories, link, title in cards:
                clean_link = clean_text(link)
                if clean_link in seen_links: continue
                
                title_text = clean_text(title)
                if any(k in title_text.lower() for k in COCUK_KEYWORDS): continue

                seen_links.add(clean_link)
                events.append({
                    "etkinlik_adi": title_text,
                    "link": clean_link,
                    "kaynak": "gaziantep_bilim_merkezi",
                    "sehir": "Gaziantep",
                })

            university_events = filter_university_events(events)
            if not university_events: return []

            detailed_events = await asyncio.gather(
                *(fetch_gaziantep_detail(http_client, event) for event in university_events)
            )

            now = datetime.now()
            aktif_events = []
            for event in detailed_events:
                tarih_detaylari = event.get("tarih_detaylari", [])
                for td in tarih_detaylari:
                    tarih_str = td.get("tarih", "")
                    # Sadece GG.AA.YYYY formatını yakalayan sıkı kontrol
                    m = re.search(r"(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{4})", tarih_str)
                    if m:
                        try:
                            dt = datetime(int(m.group(3)), int(m.group(2)), int(m.group(1)))
                            if dt.date() >= now.date():
                                aktif_events.append(event)
                                break
                        except ValueError: continue
            
            print(f"Gaziantep: {len(aktif_events)} aktif etkinlik bulundu.")
            return aktif_events

    except Exception as exc:
        print(f"Gaziantep Hatası: {exc}")
        return []