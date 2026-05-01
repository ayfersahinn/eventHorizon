# ⚡ Events Horizon

> Türkiye'deki teknoloji etkinliklerini, kursları ve hackathonları yapay zeka destekli bir altyapıyla tek platformda toplayan akıllı web platformu.

![Next.js](https://img.shields.io/badge/Next.js-16-black?style=flat-square&logo=next.js)
![Python](https://img.shields.io/badge/Python-3.11-blue?style=flat-square&logo=python)
![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-green?style=flat-square&logo=supabase)
![Groq](https://img.shields.io/badge/Groq-LLaMA_3.3_70B-orange?style=flat-square)
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-Automated-blue?style=flat-square&logo=github-actions)

---

## 🎯 Proje Hakkında

Events Horizon, BTK Akademi, Techcareer, Youthall ve GDG Gaziantep gibi farklı kaynaklardan etkinlik verilerini otomatik olarak toplayıp yapay zeka ile normalize eden ve kullanıcılara sunan bir platformdur.

**İlk odak noktası:** Gaziantep  
**Hedef:** Türkiye geneli

---

## ✨ Özellikler

- 🤖 **AI Destekli Normalizasyon** — Groq API (LLaMA 3.3 70B) ile ham veri anlamlı formata dönüştürülür
- 🔍 **Akıllı Filtreleme** — Şehir, etkinlik türü, ücret ve kategori bazlı filtreleme
- 🌙 **Dark / Light Mode** — Sistem tercihine uyumlu tema desteği
- ⚡ **Gerçek Zamanlı Veri** — Frontend doğrudan Supabase'den okur
- 🔄 **Günlük Güncelleme** — GitHub Actions ile her gece otomatik scraping
- 📱 **Responsive Tasarım** — Mobil ve masaüstü uyumlu

---

## 🏗️ Sistem Mimarisi

```
Scrapers (Python)
    │
    ▼
Groq AI (LLaMA 3.3 70B)
    │  Ham veriyi normalize eder
    ▼
Supabase (PostgreSQL)
    │  Etkinlikleri saklar
    ▼
Next.js Frontend
    │  Kullanıcıya sunar
    ▼
GitHub Actions
   Her gece 02:00 UTC'de tetikler
```

---

## 🛠️ Tech Stack

### Backend
| Teknoloji | Kullanım |
|-----------|----------|
| Python 3.11 | Ana programlama dili |
| Playwright | JavaScript render gerektiren siteler |
| httpx + asyncio | Paralel HTTP istekleri |
| BeautifulSoup4 | HTML ayrıştırma |
| Groq API | LLaMA 3.3 70B ile AI analizi |
| Supabase Python SDK | Veritabanı işlemleri |

### Frontend
| Teknoloji | Kullanım |
|-----------|----------|
| Next.js 16 | React framework |
| Tailwind CSS | Styling |
| Lucide React | İkonlar |
| @supabase/supabase-js | Veritabanı bağlantısı |

### Altyapı
| Teknoloji | Kullanım |
|-----------|----------|
| Supabase | PostgreSQL veritabanı |
| GitHub Actions | Günlük otomasyon |


---

## 📦 Veri Kaynakları

| Kaynak | Yöntem | İçerik |
|--------|--------|--------|
| BTK Akademi | REST API | Yazılım ve kariyer eğitimleri |
| Techcareer | Playwright | Bootcamp, hackathon, yarışmalar |
| Youthall | Playwright | Gençlik ve kariyer etkinlikleri |
| GDG Gaziantep | community.dev | Geliştirici topluluk etkinlikleri |
| Gaziantep Bilim Merkezi | httpx + HTML | Yerel teknoloji etkinlikleri |

---

## 🚀 Kurulum

### Gereksinimler
- Python 3.11+
- Node.js 18+
- Supabase hesabı
- Groq API anahtarı

### Backend

```bash
cd backend
pip install -r requirements.txt
playwright install chromium
```

`.env` dosyası oluştur:

```env
GROQ_API_KEY=your_groq_api_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_anon_key
```

Scraper'ı çalıştır:

```bash
python index.py
```

### Frontend

```bash
cd frontend
npm install
```

`.env.local` dosyası oluştur:

```env
NEXT_PUBLIC_SUPABASE_URL=https://your-project.supabase.co
NEXT_PUBLIC_SUPABASE_KEY=your_anon_key
```

Geliştirme sunucusunu başlat:

```bash
npm run dev
```

---

## 🗄️ Veritabanı Şeması

Supabase'de `events` tablosu:

```sql
create table events (
  id uuid default gen_random_uuid() primary key,
  title text,
  institution text,
  city text,
  start_date text,
  end_date text,
  event_type text,      -- Bootcamp, Workshop, Hackathon, Kurs...
  mode text,            -- Online, Yüz Yüze, Hibrit
  price text,           -- Ücretsiz, Ücretli, Belirtilmemiş
  category text,        -- Yapay Zeka, Siber Güvenlik...
  image_url text,
  description text,
  url text unique,
  source text,
  is_active boolean default true,
  created_at timestamp default now(),
  updated_at timestamp default now()
);
```

---

## ⚙️ GitHub Actions

Her gece 02:00 UTC'de otomatik olarak çalışır. Manuel tetiklemek için:

**Actions → Daily Scraper → Run workflow**

Gerekli secrets:
- `GROQ_API_KEY`
- `SUPABASE_URL`
- `SUPABASE_KEY`

---

## 🤖 AI Destekli Geliştirme

Bu proje, bir ekip tarafından **vibe coding** yaklaşımıyla geliştirilmiştir. Geliştirme sürecinde:

- **Claude (Anthropic)** — Kod yazımı, hata ayıklama ve mimari kararlar
- **Groq / LLaMA 3.3 70B** — Runtime'da veri normalizasyonu ve AI analizi
- **Cursor / VS Code** — Geliştirme ortamı

AI araçları; scraper geliştirme, veritabanı tasarımı, frontend bileşenleri ve otomasyon altyapısının kurulmasında aktif olarak kullanılmıştır. Kod gözden geçirme, test ve domain kararları ekip tarafından alınmıştır.

> Bu yaklaşım hakkında daha fazla bilgi için: [Anthropic — Claude for Coding](https://www.anthropic.com)

---

## 🗺️ Yol Haritası

- [x] Backend scraper altyapısı
- [x] Groq AI normalizasyonu
- [x] Supabase entegrasyonu
- [x] Next.js frontend
- [x] GitHub Actions otomasyonu
- [ ] Etkinlik detay sayfaları
- [ ] Kullanıcı bildirimleri
- [ ] SEO optimizasyonu
- [ ] Tüm Türkiye geneline yaygınlaştırma
- [ ] Mobil uygulama

---

*Events Horizon — Türkiye'nin teknoloji fırsatları platformu* ⚡
