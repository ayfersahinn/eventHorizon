import uuid
import httpx
from datetime import datetime

BTK_TARGET_URL = "https://www.btkakademi.gov.tr/portal/activities"
BTK_EVENTS_API_URL = "https://www.btkakademi.gov.tr/api/service/v1/public/51/employee/external/events/search?language=tr"

async def scrape_btk_activities():
    print(f"URL'e gidiliyor: {BTK_TARGET_URL}")
    print("BTK etkinlik verisi resmi API'den alınıyor...")

    payload = {
        "firstResult": 0,
        "sortField": "recent",
        "sortOrder": "ASCENDING",
        "filter": {
            "eventTypeIds": [],
            "cityIds": [],
            "categoryIds": [],
            "statuses": None,
            "searchTerm": "",
        },
    }

    headers = {
        "content-type": "application/json",
        "x-tenant-id": "51",
        "x-session-id": str(uuid.uuid4()),
        "referer": BTK_TARGET_URL,
        "user-agent": "Mozilla/5.0",
    }

    for attempt in range(3):
        try:
            async with httpx.AsyncClient(timeout=90.0) as http_client:
                response = await http_client.post(BTK_EVENTS_API_URL, json=payload, headers=headers)
                response.raise_for_status()
                data = response.json()
                break
        except Exception as exc:
            print(f"BTK deneme {attempt+1} başarısız: {type(exc).__name__}")
            if attempt == 2:
                print("BTK API üç denemede de başarısız oldu.")
                return []
            import asyncio
            await asyncio.sleep(5)

    raw_events = []
    for key in ("upcomingEvents", "ongoingEvents"):
        section = data.get(key, {})
        raw_events.extend(section.get("resultSet", []))

    if not raw_events:
        print("BTK API yanıtında etkinlik bulunamadı.")
        return []

    processed_events = []
    for event in raw_events:
        start_date_raw = event.get("startDate")
        formatted_date = "Tarih Belirtilmedi"
        if start_date_raw:
            try:
                formatted_date = datetime.fromtimestamp(int(start_date_raw) / 1000).strftime('%d.%m.%Y %H:%M')
            except Exception:
                formatted_date = str(start_date_raw)

        event["startDateFormatted"] = formatted_date
        event["startDate"] = formatted_date
        processed_events.append(event)

    return processed_events