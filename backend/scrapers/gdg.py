import json
import re

import httpx

from filters import clean_text, filter_university_events


GDG_GAZIANTEP_URL = "https://gdg.community.dev/gdg-gaziantep/"


def extract_next_data(html):
    match = re.search(
        r'<script id="__NEXT_DATA__" type="application/json">(.*?)</script>',
        html,
        flags=re.DOTALL,
    )
    if not match:
        return {}

    try:
        return json.loads(match.group(1))
    except json.JSONDecodeError:
        return {}


def collect_candidate_lists(page_props):
    candidates = []
    for key, value in page_props.items():
        if isinstance(value, list) and "event" in key.casefold():
            candidates.append(value)
        elif isinstance(value, dict):
            for nested_key, nested_value in value.items():
                if isinstance(nested_value, list) and "event" in nested_key.casefold():
                    candidates.append(nested_value)
    return candidates


def normalize_gdg_event(raw_event):
    title = clean_text(
        raw_event.get("title")
        or raw_event.get("name")
        or raw_event.get("event_name")
        or raw_event.get("display_title")
    )
    if not title:
        return None

    start_date = clean_text(
        raw_event.get("start_date")
        or raw_event.get("startDate")
        or raw_event.get("date")
        or raw_event.get("event_date")
    )

    event_url = clean_text(
        raw_event.get("url")
        or raw_event.get("event_url")
        or raw_event.get("absolute_url")
        or raw_event.get("href")
        or GDG_GAZIANTEP_URL
    )

    location = clean_text(
        raw_event.get("location")
        or raw_event.get("venue_name")
        or raw_event.get("city")
        or "Gaziantep"
    )

    status = clean_text(
        raw_event.get("status")
        or raw_event.get("state")
        or raw_event.get("event_status")
        or "Yaklaşan"
    )

    description = clean_text(raw_event.get("description") or raw_event.get("summary"))

    return {
        "etkinlik_adi": title,
        "tarih": start_date,
        "link": event_url,
        "sehir": "Gaziantep",
        "durum": status,
        "kaynak": "gdg_gaziantep",
        "aciklama": description,
        "konum": location,
    }


async def scrape_gdg_gaziantep_activities():
    print(f"URL'e gidiliyor: {GDG_GAZIANTEP_URL}")
    print("GDG Gaziantep etkinlikleri sayfa verisinden alınıyor...")

    try:
        async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as http_client:
            response = await http_client.get(GDG_GAZIANTEP_URL)
            response.raise_for_status()
            html = response.text
    except Exception as exc:
        print(f"GDG Gaziantep isteği başarısız oldu: {type(exc).__name__}: {exc}")
        return []

    if "There are currently no upcoming events" in html:
        print("GDG Gaziantep için yaklaşan etkinlik bulunamadı.")
        return []

    next_data = extract_next_data(html)
    page_props = next_data.get("props", {}).get("pageProps", {})
    candidate_lists = collect_candidate_lists(page_props)

    events = []
    seen_links = set()
    for candidate_list in candidate_lists:
        for raw_event in candidate_list:
            if not isinstance(raw_event, dict):
                continue
            normalized = normalize_gdg_event(raw_event)
            if not normalized:
                continue
            if normalized["link"] in seen_links:
                continue
            seen_links.add(normalized["link"])
            events.append(normalized)

    university_events = filter_university_events(events)

    if not university_events:
        print("GDG Gaziantep veri yapısında üniversite öğrencilerine uygun etkinlik bulunamadı.")
        return []

    return university_events
