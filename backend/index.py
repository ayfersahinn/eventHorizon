import asyncio
import json
import sys

# Scraper'ları import ediyoruz
from scrapers.btk import scrape_btk_activities
from scrapers.gaziantep import scrape_gaziantep_activities
from scrapers.gdg import scrape_gdg_gaziantep_activities
from scrapers.coderspace import get_coderspace_events 
from scrapers.techcareer import get_techcareer_events
from analyzer import analyze_with_groq
from filters import filter_university_events
from scrapers.techcareer import get_techcareer_events
from scrapers.habitat import get_habitat_events
async def main():
    print("--- Veri Toplama İşlemi Başladı ---")

    try:
        results = await asyncio.gather(
            scrape_btk_activities(),
            scrape_gaziantep_activities(),
            scrape_gdg_gaziantep_activities(),
            get_coderspace_events(),
            get_techcareer_events(),
            get_habitat_events()
        )
    except Exception as e:
        print(f"Veri toplama hatası: {e}")
        return

    btk_raw, gaziantep_raw, gdg_raw, coderspace_raw, techcareer_raw, habitat = results

    # --- KRİTİK DEĞİŞİKLİK: BTK verilerini filtrelemeden alıyoruz ---
    # BTK zaten resmi ve kaliteli eğitimler verdiği için onları doğrudan kabul ediyoruz.
    # Diğer kaynakları ise senin yazdığın filtreden geçiriyoruz.
    
    raw_data = {
        "btk_akademi": btk_raw,  # Filtrelemedik, hepsi gelsin
        "gaziantep_bilim_merkezi": filter_university_events(gaziantep_raw),
        "gdg_gaziantep": filter_university_events(gdg_raw),
        "coderspace": filter_university_events(coderspace_raw),
        "techcareer": filter_university_events(techcareer_raw),
        "habitat": filter_university_events(habitat),
    }

    # Sadece etkinlik bulunan kaynakları tutalım
    clean_data = {k: v for k, v in raw_data.items() if v}

    if clean_data:
        print(f"Groq veriyi analiz ediyor... (BTK: {len(btk_raw)} adet eklendi)")
        payload = json.dumps(clean_data, ensure_ascii=False)
        
        # Token limitini aşmamak için güvenli kesme (15000 karakter)
        if len(payload) > 10000:
            print("Uyarı: Veri çok büyük, optimize ediliyor...")
            payload = payload[:10000]

        try:
            # ANALYZER.PY içinde modelin "llama-3.1-8b-instant" olduğundan emin ol!
            structured_json = analyze_with_groq(payload)
            print("\n--- SONUÇLAR ---")
            print(structured_json)
        except Exception as e:
            print(f"Analiz hatası: {e}")
    else:
        print("Kriterlere uygun etkinlik bulunamadı.")

if __name__ == "__main__":
    asyncio.run(main())