from api_config import client

# GROQ_MODEL = "llama-3.1-8b-instant"
GROQ_MODEL = "llama-3.3-70b-versatile"

def analyze_with_groq(raw_content):
    print("Groq veriyi analiz ediyor...")

    prompt = f"""
    Aşağıdaki JSON farklı kaynaklardan çekilmiş etkinlik verilerini içeriyor:
    1. BTK Akademi (Yazılım ve Kariyer Eğitimleri)
    2. Gaziantep Bilim Merkezi (Bilim ve Teknoloji Etkinlikleri)
    3. GDG Gaziantep (Geliştirici Topluluk Etkinlikleri)
    4. Coderspace (Bootcamp, Hackathon ve Kariyer Etkinlikleri)
    5. Techcareer (Bootcamp, Hackathon ve Yazılım Yarışmaları)
    6. Habitat Derneği (Girişimcilik, Dijital Dönüşüm ve Teknoloji Eğitimleri)
    Lütfen sadece üniversite öğrencileri ve mezunları için uygun olan teknoloji odaklı etkinlikleri normalize et.

    Kurallar:
    - SADECE şu kaynak adlarını kullan: 'btk_akademi', 'gaziantep_bilim_merkezi', 'gdg_gaziantep', 'coderspace','techcareer','habitat'.
    - TARİH DÜZELTME: Eğer tarih milisaniye formatındaysa (örn: 1778274000000), bunu 'GG.AA.YYYY SS:DD' formatına çevir. 
    - Coderspace verilerinde tarih 'Belirtilmemiş' ise, metin veya link içinden tarih bilgisini ayıklamaya çalış, bulamazsan 'Detay için linke tıklayın' yaz.
    - Şehir bilgisini veriden çek; online etkinlikler için 'Online' yaz. Şehir yoksa tahmin etme, boş bırak.
    - FİLTRELEME: Çocuklara, ilkokul, ortaokul veya lise düzeyine yönelik etkinlikleri (şenlik, aile atölyesi vb.) KESİNLİKLE DAHİL ETME.
    - Sadece yazılım, yapay zeka, kariyer, girişimcilik ve mühendislik odaklı içerikleri al.

    Çıktıyı şu JSON formatında ver:
    {{
      "etkinlikler": [
        {{
          "etkinlik_adi": "...",
          "sehir": "...",
          "tarih": "...",
          "durum": "Yaklaşan veya Devam Ediyor",
          "link": "...",
          "kaynak": "btk_akademi veya gaziantep_bilim_merkezi veya gdg_gaziantep veya coderspace"
        }}
      ]
    }}

    Veri:
    {raw_content}
    """

    try:
        completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=GROQ_MODEL,
            response_format={"type": "json_object"},
            temperature=0.2, # Daha tutarlı ve standart çıktılar için düşürdük
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"Groq API Hatası: {e}")
        return '{ "etkinlikler": [] }'