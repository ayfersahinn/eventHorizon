import asyncio
import re

import httpx

from filters import clean_text, filter_university_events


GAZIANTEP_EVENTS_URL = "https://gaziantepbilimmerkezi.com/etkinlikler/"


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
    except Exception as exc:
        item["detay_hatasi"] = f"{type(exc).__name__}: {exc}"
        item["tarih_detaylari"] = []
        return item

    item["tarih_detaylari"] = extract_gaziantep_dates(response.text)
    return item


async def scrape_gaziantep_activities():
    print(f"URL'e gidiliyor: {GAZIANTEP_EVENTS_URL}")
    print("Gaziantep Bilim Merkezi etkinlikleri HTML'den alınıyor...")

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
            for categories, link, title in cards:
                events.append(
                    {
                        "etkinlik_adi": clean_text(title),
                        "link": clean_text(link),
                        "kaynak": "gaziantep_bilim_merkezi",
                        "sehir": "Gaziantep",
                        "kategoriler": re.findall(r"category-([a-z0-9-]+)", categories or ""),
                    }
                )

            unique_events = []
            seen_links = set()
            for event in events:
                if event["link"] in seen_links:
                    continue
                seen_links.add(event["link"])
                unique_events.append(event)

            university_events = filter_university_events(unique_events)

            if not university_events:
                print("Gaziantep Bilim Merkezi sayfasında etkinlik bulunamadı.")
                return []

            detailed_events = await asyncio.gather(
                *(fetch_gaziantep_detail(http_client, event) for event in university_events)
            )
            return detailed_events
    except Exception as exc:
        print(f"Gaziantep Bilim Merkezi isteği başarısız oldu: {type(exc).__name__}: {exc}")
        return []
