import asyncio
import json
import sys
from datetime import datetime
import time
from scrapers.btk import scrape_btk_activities
from scrapers.gaziantep import scrape_gaziantep_activities
from scrapers.gdg import scrape_gdg_gaziantep_activities
from scrapers.techcareer import get_techcareer_events
from scrapers.youthall import get_youthall_events
from analyzer import analyze_with_groq
from filters import filter_university_events, filter_non_child_events

from supabase import create_client
from dotenv import load_dotenv
import os

load_dotenv()
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

def save_to_supabase(etkinlikler):
    print(f"\n--- Supabase'e kaydediliyor ({len(etkinlikler)} etkinlik) ---")

    for e in etkinlikler:
        try:
             
            # upsert(on_conflict="url") zaten varsa günceller, yoksa ekler.
            data = {
                "title": e.get("etkinlik_adi"),
                "institution": e.get("kurum"),
                "city": e.get("sehir"),
                "start_date": e.get("baslangic_tarihi"),
                "end_date": e.get("bitis_tarihi"),
                "event_type": e.get("etkinlik_turu"),
                "mode": e.get("mod"),
                "price": e.get("ucret"),
                "category": e.get("kategori"),
                # Model farklı anahtar adları döndürürse de alanları kaçırma.
                "image_url": e.get("gorsel_url") or e.get("image_url"),
                "description": e.get("aciklama") or e.get("description"),
                "url": e.get("link"),
                "source": e.get("kaynak"),
                "is_active": True,
                "updated_at": datetime.now().isoformat(),
            }

            # Tek bir çağrı ile hem insert hem update işlemi yapılır
            supabase.table("events").upsert(data, on_conflict="url").execute()
            print(f"  ✓ İşlem Başarılı: {e.get('etkinlik_adi')}")

        except Exception as err:
            print(f"  ✗ Hata ({e.get('etkinlik_adi')}): {err}")

async def main():
    print("--- Veri Toplama İşlemi Başladı ---")
    
    # Tarihi geçmişleri pasif yapma işlemi
    bugun_str = datetime.now().strftime("%d.%m.%Y")
    try:
        #Sadece 'is_active' olanları kontrol ederek veritabanı yükünü azaltın
        supabase.table("events").update({"is_active": False}).eq("is_active", True).lt("end_date", bugun_str).execute()
    except Exception as e:
        print(f"Eski etkinlikleri pasifleştirme hatası: {e}")

    # Supabase'deki mevcut URL'leri çek (mükerrer scrape/analizi azaltmak için)
    try:
        existing = supabase.table("events").select("url").execute()
        existing_urls = {row["url"] for row in existing.data}
    except Exception:
        existing_urls = set()
    
    try:
        results = await asyncio.gather(
            scrape_btk_activities(),
            scrape_gaziantep_activities(),
            scrape_gdg_gaziantep_activities(),
            get_techcareer_events(),
            get_youthall_events(),
        )
    except Exception as e:
        print(f"Veri toplama hatası: {e}")
        return

    btk_raw, gaziantep_raw, gdg_raw, techcareer_raw, youthall = results

    raw_data = {
        "btk_akademi": btk_raw,
        "gaziantep_bilim_merkezi": filter_university_events(gaziantep_raw),
        "gdg_gaziantep": filter_university_events(gdg_raw),
        "techcareer": filter_university_events(techcareer_raw),
        # Youthall genel kariyer etkinlikleri içerdiği için daha esnek filtre kullan.
        "youthall": filter_non_child_events(youthall),
    }

    clean_data = {k: v for k, v in raw_data.items() if v}
    
    # Sadece veritabanında olmayanları ayır
    for kaynak in list(clean_data.keys()):
        onceki_sayi = len(clean_data[kaynak])
        clean_data[kaynak] = [e for e in clean_data[kaynak] if e.get("link") not in existing_urls]
        print(f"{kaynak}: {onceki_sayi} → {len(clean_data[kaynak])} yeni etkinlik")

    clean_data = {k: v for k, v in clean_data.items() if v}

    if clean_data:
        tum_etkinlikler = []
        for kaynak, veri in clean_data.items():
            print(f"{kaynak} analiz ediliyor ({len(veri)} yeni etkinlik)...")
            payload = json.dumps({kaynak: veri}, ensure_ascii=False)
            
            try:
                structured_json = analyze_with_groq(payload)
                parsed = json.loads(structured_json)
                etkinlikler = parsed.get("etkinlikler", [])
                tum_etkinlikler.extend(etkinlikler)
                print(f"  → {len(etkinlikler)} etkinlik normalize edildi")
            except Exception as e:
                print(f"  → {kaynak} analiz hatası: {e}")
            
            time.sleep(6) # Rate limit koruması
        
        if tum_etkinlikler:
            save_to_supabase(tum_etkinlikler)
        else:
            print("Kaydedilecek yeni etkinlik bulunamadı.")
    else:
        print("Yeni etkinlik yok, analiz atlanıyor.")

if __name__ == "__main__":
    asyncio.run(main())