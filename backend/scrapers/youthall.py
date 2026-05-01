import asyncio
import re
from datetime import datetime

import httpx
from bs4 import BeautifulSoup


TR_MONTHS = {
    "ocak": "01",
    "şubat": "02",
    "mart": "03",
    "nisan": "04",
    "mayıs": "05",
    "haziran": "06",
    "temmuz": "07",
    "ağustos": "08",
    "eylül": "09",
    "ekim": "10",
    "kasım": "11",
    "aralık": "12",
}

TURKEY_CITIES = [
    "Adana","Adıyaman","Afyonkarahisar","Ağrı","Aksaray","Amasya","Ankara","Antalya","Ardahan","Artvin",
    "Aydın","Balıkesir","Bartın","Batman","Bayburt","Bilecik","Bingöl","Bitlis","Bolu","Burdur","Bursa",
    "Çanakkale","Çankırı","Çorum","Denizli","Diyarbakır","Düzce","Edirne","Elazığ","Erzincan","Erzurum",
    "Eskişehir","Gaziantep","Giresun","Gümüşhane","Hakkâri","Hatay","Iğdır","Isparta","İstanbul","İzmir",
    "Kahramanmaraş","Karabük","Karaman","Kars","Kastamonu","Kayseri","Kilis","Kırıkkale","Kırklareli","Kırşehir",
    "Kocaeli","Konya","Kütahya","Malatya","Manisa","Mardin","Mersin","Muğla","Muş","Nevşehir","Niğde","Ordu",
    "Osmaniye","Rize","Sakarya","Samsun","Şanlıurfa","Siirt","Sinop","Sivas","Şırnak","Tekirdağ","Tokat",
    "Trabzon","Tunceli","Uşak","Van","Yalova","Yozgat","Zonguldak",
]




def _extract_city(text: str) -> str:
    """
    Kart metninden yalnızca bilinen şehir adını veya 'Online' döner.
    Şehir bulunamazsa boş string döner — tahmin yapmaz.
    """
    s = re.sub(r"\s+", " ", text.replace("\u00a0", " ")).strip()

    # 1. Online
    if re.search(r"\bOnline\b", s, re.IGNORECASE):
        return "Online"

    # 2. Bilinen Türkiye şehri
    found = []
    for city in TURKEY_CITIES:
        if re.search(rf"(?<!\w){re.escape(city)}(?!\w)", s, re.IGNORECASE):
            if city not in found:
                found.append(city)
    if found:
        return "/".join(found[:2])

    # Şehir bulunamadı — boş bırak, Groq veya kullanıcı halleder
    return ""


def _normalize_dd_month(text: str, year: int) -> str | None:
    """
    "04 Mayıs" gibi yılsız tarihi "DD.MM.YYYY" formatına çevirir.
    """
    if not text:
        return None
    s = re.sub(r"\s+", " ", text.replace("\u00a0", " ")).strip()
    m = re.search(r"\b(\d{1,2})\s+([A-Za-zÇĞİÖŞÜçğıöşü]+)\b", s, re.IGNORECASE)
    if not m:
        return None
    day = f"{int(m.group(1)):02d}"
    mon = TR_MONTHS.get(m.group(2).lower())
    if not mon:
        return None
    return f"{day}.{mon}.{year}"


async def get_youthall_events():
    """
    Youthall etkinlik listesini statik HTML'den çeker.
    Playwright kullanmaz (hızlı + rate limit dostu).
    """
    url = "https://www.youthall.com/tr/events/"
    print(f"URL'e gidiliyor: {url}")
    print("Youthall etkinlikleri HTML'den alınıyor...")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept-Language": "tr-TR,tr;q=0.9,en;q=0.8",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    }

    now = datetime.now()
    etkinlikler: list[dict] = []

    async with httpx.AsyncClient(headers=headers, timeout=30, follow_redirects=True) as client:
        resp = await client.get(url)
        resp.raise_for_status()

    soup = BeautifulSoup(resp.text, "html.parser")

    cards = soup.select("a")
    seen = set()

    for a in cards:
        href = a.get("href") or ""
        if not href:
            continue

        if href.startswith("/"):
            full = "https://www.youthall.com" + href
        else:
            full = href

        txt = a.get_text(" ", strip=True)
        if not txt or ("Başlangıç" not in txt and "Bitiş" not in txt):
            continue

        if full in seen:
            continue
        seen.add(full)

        # Başlık: "Son Başvuru" öncesi tüm metin, olduğu gibi
        if "Son Başvuru" in txt:
            title = txt.split("Son Başvuru")[0].strip()
        else:
            title = txt.split("Başlangıç")[0].strip()

        title = re.sub(r"\s+", " ", title).strip()
        if len(title) < 5:
            continue

        # Şehir: tüm metinden ayrıca çıkar, title'a dokunma
        sehir = _extract_city(txt)

        image_tag = a.select_one("img")
        gorsel_url = ""
        if image_tag:
            gorsel_url = (image_tag.get("src") or image_tag.get("data-src") or "").strip()
            if gorsel_url.startswith("//"):
                gorsel_url = "https:" + gorsel_url
            elif gorsel_url.startswith("/"):
                gorsel_url = "https://www.youthall.com" + gorsel_url

        aciklama = ""
        title_node = a.select_one("h1, h2, h3, h4, h5, h6, .title")
        if title_node:
            clone = BeautifulSoup(str(a), "html.parser")
            title_clone = clone.select_one("h1, h2, h3, h4, h5, h6, .title")
            if title_clone:
                title_clone.extract()
            aciklama = re.sub(r"\s+", " ", clone.get_text(" ", strip=True)).strip()

        # Tarih: "Başlangıç 05 Mayıs" gibi
        start_raw = None
        m = re.search(r"\bBaşlangıç\b\s*([0-9]{1,2}\s+[A-Za-zÇĞİÖŞÜçğıöşü]+)", txt, re.IGNORECASE)
        if m:
            start_raw = m.group(1)
        start_date = _normalize_dd_month(start_raw, now.year) if start_raw else None

        etkinlikler.append(
            {
                "etkinlik_adi": title,
                "sehir": sehir,
                "tarih": start_date or "Detay için linke tıklayın",
                "durum": "Yaklaşan",
                "gorsel_url": gorsel_url or None,
                "aciklama": aciklama or None,
                "link": full,
                "kaynak": "youthall",
            }
        )

    print(f"Youthall: {len(etkinlikler)} etkinlik bulundu.")
    return etkinlikler


def scrape_youthall():
    return asyncio.run(get_youthall_events())