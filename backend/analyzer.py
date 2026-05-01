from api_config import client
from datetime import datetime
import time

GROQ_MODEL = "llama-3.3-70b-versatile"

def analyze_with_groq(raw_content):
    print("Groq veriyi analiz ediyor...")
    bugun = datetime.now().strftime("%d.%m.%Y")
    prompt = f"""
    Bugünün tarihi: {bugun}
    
    Aşağıdaki JSON farklı kaynaklardan çekilmiş etkinlik verilerini içeriyor:
    1. BTK Akademi (Yazılım ve Kariyer Eğitimleri)
    2. Gaziantep Bilim Merkezi (Bilim ve Teknoloji Etkinlikleri)
    3. GDG Gaziantep (Geliştirici Topluluk Etkinlikleri)
    4. Techcareer (Bootcamp, Hackathon ve Yazılım Yarışmaları)
    5. Youthall (Kariyer etkinlikleri, zirveler, eğitimler)
    Lütfen sadece üniversite öğrencileri ve mezunları için uygun olan teknoloji odaklı etkinlikleri normalize et.

    Kurallar:
    - SADECE şu kaynak adlarını kullan: 'btk_akademi', 'gaziantep_bilim_merkezi', 'gdg_gaziantep', 'techcareer', 'youthall'.
    - GEÇMİŞ ETKİNLİK FİLTRESİ: Bitiş tarihi bugünden ({bugun}) önce olan etkinlikleri KESİNLİKLE ÇIKART. Sadece bugün veya sonrası olan etkinlikleri dahil et. Tarihi 'Detay için linke tıklayın' olanları dahil et.
   - TARİH DÜZELTME: 
    1. Eğer tarih milisaniye formatındaysa (örn: 1778274000000), bunu 'GG.AA.YYYY' formatına çevir.
    2. Eğer tarih metin formatındaysa (örn: '28 Nisan 2026' veya '28/04/2026'), bunu MUTLAKA 'GG.AA.YYYY' formatına (örn: '28.04.2026') dönüştür. 
    3. Ay isimlerini (Ocak, Şubat...) sayısal karşılıklarıyla (01, 02...) değiştir.
    4. EĞER bir etkinliğin bitiş tarihi net değilse ve başlangıç tarihi geçmişte kalmışsa, bu etkinliği JSON listesine dahil etme.
    - Şehir bilgisini veriden çek; online etkinlikler için 'Online' yaz. Şehir yoksa tahmin etme, boş bırak.
    - FİLTRELEME: Çocuklara, ilkokul, ortaokul veya lise düzeyine yönelik etkinlikleri KESİNLİKLE DAHİL ETME.
    - Sadece yazılım, yapay zeka, kariyer, girişimcilik ve mühendislik odaklı içerikleri al.
    - ETKİNLİK TÜRÜ: Her etkinlik için uygun türü belirle: 'Bootcamp', 'Workshop', 'Hackathon', 'Kurs', 'Konferans', 'Webinar', 'Yarışma' veya 'Diğer'.
    - MOD: Etkinliğin formatını belirle: 'Online', 'Yüz Yüze' veya 'Hibrit'.
    - ÜCRET: Ücretsizse 'Ücretsiz', ücretliyse 'Ücretli' yaz. Belirtilmemişse 'Belirtilmemiş' yaz.
    - KATEGORİ: Etkinliğin ana konusunu belirle: 'Yapay Zeka', 'Web Geliştirme', 'Mobil', 'Siber Güvenlik', 'Veri Bilimi', 'Blockchain', 'Girişimcilik', 'Kariyer', 'Donanım', 'Oyun' veya 'Diğer'.
    - GÖRSEL: Etkinliğin görseli varsa URL'ini al, yoksa null bırak.
    - AÇIKLAMA: Etkinliğin kısa açıklamasını al, yoksa null bırak.

    Çıktıyı şu JSON formatında ver:
    {{
      "etkinlikler": [
        {{
          "etkinlik_adi": "...",
          "kurum": "...",
          "sehir": "...",
          "baslangic_tarihi": "GG.AA.YYYY veya Detay için linke tıklayın",
          "bitis_tarihi": "GG.AA.YYYY veya null",
          "etkinlik_turu": "Bootcamp | Workshop | Hackathon | Kurs | Konferans | Webinar | Yarışma | Diğer",
          "mod": "Online | Yüz Yüze | Hibrit",
          "ucret": "Ücretsiz | Ücretli | Belirtilmemiş",
          "kategori": "Yapay Zeka | Web Geliştirme | Mobil | Siber Güvenlik | Veri Bilimi | Blockchain | Girişimcilik | Kariyer | Donanım | Oyun | Diğer",
          "gorsel_url": "... veya null",
          "aciklama": "... veya null",
          "link": "...",
          "kaynak": "btk_akademi | gaziantep_bilim_merkezi | gdg_gaziantep | techcareer | youthall",
          "durum": "Yaklaşan | Devam Ediyor"
        }}
      ]
    }}

    Veri:
    {raw_content}
    """

    for attempt in range(3):
        try:
            completion = client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=GROQ_MODEL,
                response_format={"type": "json_object"},
                temperature=0.1,
            )
            return completion.choices[0].message.content
        except Exception as e:
            if "429" in str(e):
                wait = 90 * (attempt + 1)
                print(f"Rate limit, {wait} saniye bekleniyor...")
                time.sleep(wait)
            else:
                print(f"Groq API Hatası: {e}")
                return '{ "etkinlikler": [] }'

    return '{ "etkinlikler": [] }'