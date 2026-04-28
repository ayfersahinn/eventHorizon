import uuid

import httpx


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

    try:
        async with httpx.AsyncClient(timeout=60.0) as http_client:
            response = await http_client.post(BTK_EVENTS_API_URL, json=payload, headers=headers)
            response.raise_for_status()
            data = response.json()
    except Exception as exc:
        print(f"BTK API isteği başarısız oldu: {type(exc).__name__}: {exc}")
        return []

    events = []
    for key in ("upcomingEvents", "ongoingEvents"):
        section = data.get(key, {})
        events.extend(section.get("resultSet", []))

    if not events:
        print("BTK API yanıtında etkinlik bulunamadı.")

    return events
