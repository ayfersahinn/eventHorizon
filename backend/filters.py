import re
from html import unescape


EXCLUDED_KEYWORDS = {
    "çocuk",
    "cocuk",
    "ebeveyn",
    "parent",
    "aile",
    "ilkokul",
    "ortaokul",
    "lise",
    "şenlik",
    "senlik",
}

INCLUDED_KEYWORDS = {
    "üniversite",
    "universite",
    "öğrenci",
    "ogrenci",
    "kariyer",
    "girişim",
    "girisim",
    "teknoloji",
    "yapay zeka",
    "ai",
    "python",
    "opencv",
    "pcb",
    "tasarım",
    "tasarim",
    "mekanik",
    "bilim söyleşisi",
    "soylesi",
    "kamp",
    "eğitim",
    "egitim",
    "workshop",
    "atölye",
    "atolye",
}


def clean_text(value):
    if not value:
        return ""
    value = re.sub(r"<[^>]+>", " ", value)
    value = unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def is_university_friendly(text):
    normalized_text = clean_text(text).casefold()
    if not normalized_text:
        return False
    if any(keyword in normalized_text for keyword in EXCLUDED_KEYWORDS):
        return False
    return any(keyword in normalized_text for keyword in INCLUDED_KEYWORDS)


def filter_university_events(events):
    filtered = []
    for event in events:
        searchable_parts = [
            event.get("etkinlik_adi", ""),
            event.get("tarih", ""),
            event.get("durum", ""),
            event.get("sehir", ""),
            " ".join(event.get("kategoriler", [])),
            " ".join(
                f"{item.get('tarih', '')} {item.get('mekan', '')}"
                for item in event.get("tarih_detaylari", [])
            ),
        ]
        if is_university_friendly(" ".join(searchable_parts)):
            filtered.append(event)
    return filtered


def filter_non_child_events(events):
    """
    Youthall gibi kaynaklarda daha geniş kapsam korumak için
    sadece çocuk/okul öncesi-lise odaklı etkinlikleri eler.
    """
    filtered = []
    for event in events:
        searchable_parts = [
            event.get("etkinlik_adi", ""),
            event.get("tarih", ""),
            event.get("durum", ""),
            event.get("sehir", ""),
            event.get("aciklama", ""),
            " ".join(event.get("kategoriler", [])),
            " ".join(
                f"{item.get('tarih', '')} {item.get('mekan', '')}"
                for item in event.get("tarih_detaylari", [])
            ),
        ]
        normalized_text = clean_text(" ".join(searchable_parts)).casefold()
        if not normalized_text:
            continue
        if any(keyword in normalized_text for keyword in EXCLUDED_KEYWORDS):
            continue
        filtered.append(event)
    return filtered
