from api_config import client


GROQ_MODEL = "llama-3.3-70b-versatile"


def analyze_with_groq(raw_content):
    print("Groq veriyi analiz ediyor...")

    prompt = f"""
    Aşağıdaki JSON farklı kaynaklardan çekilmiş etkinlik verilerini içeriyor:
    1. BTK Akademi resmi etkinlik API'si
    2. Gaziantep Bilim Merkezi etkinlik sayfası ve detay sayfaları
    3. GDG Gaziantep topluluk sayfası

    Lütfen sadece üniversite öğrencileri için uygun olan etkinlikleri tek bir listede normalize et.

    Kurallar:
    - Her etkinlik için tek bir nesne döndür.
    - Gaziantep Bilim Merkezi verisinde 'tarih_detaylari' içinde birden fazla tarih varsa her tarihi tek string içinde okunabilir biçimde birleştir.
    - Şehir bilinmiyorsa tahmin etme; boş string ver.
    - BTK verisinde Gaziantep olanları özellikle doğru ayıkla.
    - Çocuklara, ebeveyn-çocuk gruplarına, ailelere, ilkokul/ortaokul/lise düzeyine hitap eden etkinlikleri dahil etme.
    - Eğitim, kamp, söyleşi, teknoloji, yapay zeka, kariyer, girişimcilik gibi üniversite öğrencilerine uygun etkinlikleri tercih et.
    - Link alanında etkinliğin kendi linkini kullan.
    - 'kaynak' alanına 'btk_akademi', 'gaziantep_bilim_merkezi' veya 'gdg_gaziantep' yaz.

    Çıktıyı şu JSON formatında ver:
    {{
      "etkinlikler": [
        {{
          "etkinlik_adi": "...",
          "sehir": "...",
          "tarih": "...",
          "durum": "Yeni veya Devam Ediyor veya Yaklaşan",
          "link": "...",
          "kaynak": "btk_akademi veya gaziantep_bilim_merkezi veya gdg_gaziantep"
        }}
      ]
    }}

    Veri:
    {raw_content}
    """

    completion = client.chat.completions.create(
        messages=[{"role": "user", "content": prompt}],
        model=GROQ_MODEL,
        response_format={"type": "json_object"},
    )
    return completion.choices[0].message.content
