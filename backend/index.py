import asyncio
import json

from analyzer import analyze_with_groq
from filters import filter_university_events
from scrapers import (
    scrape_btk_activities,
    scrape_gaziantep_activities,
    scrape_gdg_gaziantep_activities,
)


async def main():
    btk_events, gaziantep_events, gdg_events = await asyncio.gather(
        scrape_btk_activities(),
        scrape_gaziantep_activities(),
        scrape_gdg_gaziantep_activities(),
    )

    raw_data = {
        "btk_akademi": btk_events,
        "gaziantep_bilim_merkezi": gaziantep_events,
        "gdg_gaziantep": gdg_events,
    }

    if any(raw_data.values()):
        structured_json = analyze_with_groq(json.dumps(raw_data, ensure_ascii=False))
        parsed_json = json.loads(structured_json)
        parsed_json["etkinlikler"] = filter_university_events(parsed_json.get("etkinlikler", []))
        print("\n--- SONUÇLAR ---")
        print(json.dumps(parsed_json, ensure_ascii=False, indent=2))
    else:
        print("Hiçbir kaynaktan veri çekilemedi.")


if __name__ == "__main__":
    asyncio.run(main())