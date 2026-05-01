"use client";
import { createClient } from "@supabase/supabase-js";
import { useState, useEffect, useMemo, useRef } from "react";
import {
  MapPin,
  Calendar,
  Search,
  Filter,
  ChevronDown,
  ExternalLink,
  Cpu,
  Zap,
  BookOpen,
  Trophy,
  Users,
  Globe,
  Wifi,
  Clock,
  Star,
  TrendingUp,
  Menu,
  X,
  Sun,
  Moon,
  ArrowRight,
  Layers,
  Tag,
  Building2,
  GraduationCap,
  Code2,
  Rocket,
  Target,
} from "lucide-react";
const supabase = createClient(
  process.env.NEXT_PUBLIC_SUPABASE_URL,
  process.env.NEXT_PUBLIC_SUPABASE_KEY
);


const categoryIcons = {
  "Yapay Zeka": Cpu,
  Blockchain: Layers,
  "Siber Güvenlik": Target,
  Hackathon: Trophy,
  Mobil: Rocket,
  "Veri Bilimi": TrendingUp,
};

function formatCompactNumber(value) {
  if (!Number.isFinite(value)) return "-";
  return new Intl.NumberFormat("tr-TR", {
    notation: "compact",
    maximumFractionDigits: 1,
  }).format(value);
}

function GradientOrb({ x, y, color, size = 300, opacity = 0.15 }) {
  return (
    <div
      style={{
        position: "absolute",
        left: x,
        top: y,
        width: size,
        height: size,
        borderRadius: "50%",
        background: color,
        opacity,
        filter: "blur(80px)",
        pointerEvents: "none",
        zIndex: 0,
      }}
    />
  );
}

function InstitutionBadge({ name, color, dark }) {
  return (
    <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
      <div
        style={{
          width: 28,
          height: 28,
          borderRadius: 6,
          background: color,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          flexShrink: 0,
        }}
      >
        <Building2 size={14} color="white" />
      </div>
      <span
        style={{
          fontSize: 12,
          fontWeight: 600,
          letterSpacing: "0.02em",
          color: dark ? "#8896b3" : "#64748b",
        }}
      >
        {name}
      </span>
    </div>
  );
}

function EventCard({ event, dark }) {
  const [hovered, setHovered] = useState(false);
  const Icon = categoryIcons[event.category] || Zap;
  const hasSeatData =
    Number.isFinite(event.seats) &&
    Number.isFinite(event.totalSeats) &&
    event.totalSeats > 0;
  const occupancyPercent = hasSeatData
    ? Math.round((event.seats / event.totalSeats) * 100)
    : 0;
  const isAlmostFull = hasSeatData && occupancyPercent > 75;

  const bg = dark
    ? hovered
      ? "#1e2535"
      : "#161c2d"
    : hovered
      ? "#f8faff"
      : "#ffffff";

  const border = dark
    ? hovered
      ? "#3b4a6b"
      : "#232b3e"
    : hovered
      ? "#c7d4f0"
      : "#e8edf7";

  return (
    <div
      onMouseEnter={() => setHovered(true)}
      onMouseLeave={() => setHovered(false)}
      style={{
        background: bg,
        border: `1px solid ${border}`,
        borderRadius: 16,
        overflow: "hidden",
        transition: "all 0.25s ease",
        transform: hovered ? "translateY(-4px)" : "none",
        boxShadow: hovered
          ? dark
            ? "0 16px 40px rgba(0,0,0,0.4)"
            : "0 16px 40px rgba(80,120,220,0.12)"
          : "none",
        cursor: "pointer",
        position: "relative",
      }}
    >
      {event.featured && (
        <div
          style={{
            position: "absolute",
            top: 12,
            right: 12,
            background: "linear-gradient(135deg, #f59e0b, #f97316)",
            color: "white",
            fontSize: 10,
            fontWeight: 700,
            letterSpacing: "0.08em",
            padding: "3px 8px",
            borderRadius: 20,
            zIndex: 2,
            textTransform: "uppercase",
          }}
        >
          ⭐ Öne Çıkan
        </div>
      )}

      <div
        style={{
          height: 120,
          background: event.imageUrl
            ? `url(${event.imageUrl}) center/cover no-repeat`
            : `linear-gradient(135deg, ${event.institutionColor}22, ${event.institutionColor}44)`,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          position: "relative",
          borderBottom: `1px solid ${border}`,
        }}
      >
        {event.imageUrl ? (
          <div
            style={{
              position: "absolute",
              inset: 0,
              background: "linear-gradient(180deg, rgba(0,0,0,0.05), rgba(0,0,0,0.35))",
            }}
          />
        ) : (
          <div
            style={{
              width: 56,
              height: 56,
              borderRadius: 14,
              background: event.institutionColor,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              boxShadow: `0 8px 24px ${event.institutionColor}44`,
            }}
          >
            <Icon size={24} color="white" />
          </div>
        )}
      </div>

      <div style={{ padding: "16px 18px 18px" }}>
        <div
          style={{
            display: "flex",
            gap: 6,
            marginBottom: 10,
            flexWrap: "wrap",
          }}
        >
          <span
            style={{
              fontSize: 11,
              fontWeight: 700,
              letterSpacing: "0.06em",
              textTransform: "uppercase",
              padding: "3px 8px",
              borderRadius: 20,
              background:
                event.mode === "Online"
                  ? dark
                    ? "#1a3a5c"
                    : "#dbeafe"
                  : dark
                    ? "#1a3a2c"
                    : "#dcfce7",
              color:
                event.mode === "Online"
                  ? dark
                    ? "#60a5fa"
                    : "#1d4ed8"
                  : dark
                    ? "#4ade80"
                    : "#15803d",
            }}
          >
            {event.mode === "Online" ? (
              <>
                <Wifi size={9} style={{ display: "inline", marginRight: 3 }} />
                {event.mode}
              </>
            ) : (
              <>
                <Users size={9} style={{ display: "inline", marginRight: 3 }} />
                {event.mode}
              </>
            )}
          </span>

          <span
            style={{
              fontSize: 11,
              fontWeight: 700,
              letterSpacing: "0.04em",
              textTransform: "uppercase",
              padding: "3px 8px",
              borderRadius: 20,
              background: dark ? "#2a1f4a" : "#ede9fe",
              color: dark ? "#a78bfa" : "#6d28d9",
            }}
          >
            {event.type}
          </span>

          <span
            style={{
              fontSize: 11,
              fontWeight: 700,
              letterSpacing: "0.04em",
              padding: "3px 8px",
              borderRadius: 20,
              background:
                event.price === "Ücretsiz"
                  ? dark
                    ? "#1c3a28"
                    : "#d1fae5"
                  : dark
                    ? "#3a1c1c"
                    : "#fee2e2",
              color:
                event.price === "Ücretsiz"
                  ? dark
                    ? "#34d399"
                    : "#065f46"
                  : dark
                    ? "#f87171"
                    : "#991b1b",
            }}
          >
            {event.price}
          </span>
        </div>

        <h3
          style={{
            fontSize: 15,
            fontWeight: 700,
            lineHeight: 1.4,
            marginBottom: 10,
            color: dark ? "#e2e8f5" : "#0f172a",
          }}
        >
          {event.title}
        </h3>

        <InstitutionBadge
          name={event.institution}
          color={event.institutionColor}
          dark={dark}
        />

        <div
          style={{
            display: "flex",
            gap: 14,
            marginTop: 12,
            marginBottom: 12,
            color: dark ? "#8896b3" : "#64748b",
            fontSize: 12,
          }}
        >
          <span style={{ display: "flex", alignItems: "center", gap: 4 }}>
            <MapPin size={12} /> {event.city}
          </span>
          <span style={{ display: "flex", alignItems: "center", gap: 4 }}>
            <Calendar size={12} /> {event.date}
          </span>
        </div>

        {hasSeatData ? (
          <div style={{ marginBottom: 14 }}>
            <div
              style={{
                display: "flex",
                justifyContent: "space-between",
                fontSize: 11,
                marginBottom: 4,
                color: dark ? "#8896b3" : "#64748b",
              }}
            >
              <span>{event.seats} kontenjan doldu</span>
              <span style={{ color: isAlmostFull ? "#f97316" : undefined }}>
                {event.totalSeats - event.seats} yer kaldı
              </span>
            </div>
            <div
              style={{
                height: 4,
                background: dark ? "#232b3e" : "#e8edf7",
                borderRadius: 99,
              }}
            >
              <div
                style={{
                  height: "100%",
                  width: `${occupancyPercent}%`,
                  background: isAlmostFull
                    ? "linear-gradient(90deg, #f59e0b, #f97316)"
                    : "linear-gradient(90deg, #3b82f6, #6366f1)",
                  borderRadius: 99,
                  transition: "width 0.6s ease",
                }}
              />
            </div>
          </div>
        ) : (
          <div
            style={{
              marginBottom: 14,
              fontSize: 12,
              color: dark ? "#9fb0ce" : "#475569",
              lineHeight: 1.5,
              display: "-webkit-box",
              WebkitLineClamp: 3,
              WebkitBoxOrient: "vertical",
              overflow: "hidden",
            }}
          >
            {event.description || "Kontenjan bilgisi kaynakta paylaşılmamış."}
          </div>
        )}

        <div
          style={{
            display: "flex",
            gap: 6,
            flexWrap: "wrap",
            marginBottom: 14,
          }}
        >
         {(event.tags || []).map((tag) => (
            <span
              key={tag}
              style={{
                fontSize: 10,
                fontWeight: 600,
                padding: "2px 7px",
                borderRadius: 6,
                background: dark ? "#1e2535" : "#f1f5f9",
                color: dark ? "#94a3b8" : "#475569",
                border: `1px solid ${dark ? "#2d3748" : "#e2e8f0"}`,
              }}
            >
              {tag}
            </span>
          ))}
        </div>

        <a
          href={event.url || "#"}
          target="_blank"
          rel="noreferrer"
          style={{
            width: "100%",
            padding: "10px 16px",
            borderRadius: 10,
            border: "none",
            background: "linear-gradient(135deg, #3b82f6, #6366f1)",
            color: "white",
            fontSize: 13,
            fontWeight: 700,
            cursor: event.url ? "pointer" : "not-allowed",
            opacity: event.url ? 1 : 0.6,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 6,
            letterSpacing: "0.02em",
            textDecoration: "none",
          }}
        >
          Detaya Git <ArrowRight size={14} />
        </a>
      </div>
    </div>
  );
}

function FilterChip({ label, active, onClick, dark }) {
  return (
    <button
      onClick={onClick}
      style={{
        padding: "6px 14px",
        borderRadius: 99,
        border: `1.5px solid ${active ? "#3b82f6" : dark ? "#2d3a52" : "#d1d9e8"}`,
        background: active
          ? "linear-gradient(135deg, #3b82f6, #6366f1)"
          : dark
            ? "#161c2d"
            : "#f8faff",
        color: active ? "white" : dark ? "#8896b3" : "#64748b",
        fontSize: 13,
        fontWeight: active ? 700 : 500,
        cursor: "pointer",
        transition: "all 0.2s",
        whiteSpace: "nowrap",
      }}
    >
      {label}
    </button>
  );
}

export default function EventsHorizon() {
  const [dark, setDark] = useState(true);
  const [selectedCity, setSelectedCity] = useState("Tümü");
  const [selectedType, setSelectedType] = useState("Tümü");
  const [selectedInstitution, setSelectedInstitution] = useState("Tümü");
  const [selectedPrice, setSelectedPrice] = useState("Tümü");
  const [searchQuery, setSearchQuery] = useState("");
  const [menuOpen, setMenuOpen] = useState(false);
  const [events, setEvents] = useState([]);
  const [currentPage, setCurrentPage] = useState(1);
  const eventsSectionRef = useRef(null);
  const hiddenInstitutions = useMemo(
    () => new Set(["coderspace", "habitat"]),
    []
  );

  useEffect(() => {
    const sourceColors = {
      btk_akademi: "#2563eb",
      gaziantep_bilim_merkezi: "#16a34a",
      gdg_gaziantep: "#ea580c",
      techcareer: "#7c3aed",
      youthall: "#0891b2",
    };

    supabase
      .from("events")
      .select("*")
      .eq("is_active", true)
      .then(({ data }) =>
        setEvents(
          (data || []).map((e) => ({
            ...e,
            title: e.title || "Başlık yok",
            type: e.event_type || e.type || "Diğer",
            date: e.start_date || e.date || "Tarih belirtilmemiş",
            city: e.city || "Online",
            price: e.price || "Belirtilmemiş",
            mode: e.mode || "Online",
            category: e.category || "Diğer",
            tags: Array.isArray(e.tags) ? e.tags : [],
            imageUrl: e.image_url || null,
            description: e.description || null,
            url: e.url || null,
            institutionColor: sourceColors[e.source] || "#3b82f6",
          }))
        )
      );
  }, []);

  const cities = useMemo(() => {
    const values = new Set(
      events.map((e) => e.city).filter((v) => typeof v === "string" && v.trim())
    );
    return ["Tümü", ...Array.from(values).sort((a, b) => a.localeCompare(b, "tr"))];
  }, [events]);

  const eventTypes = useMemo(() => {
    const values = new Set(
      events.map((e) => e.type).filter((v) => typeof v === "string" && v.trim())
    );
    return ["Tümü", ...Array.from(values).sort((a, b) => a.localeCompare(b, "tr"))];
  }, [events]);

  const institutions = useMemo(() => {
    const values = new Set(
      events
        .map((e) => e.institution)
        .filter((v) => typeof v === "string" && v.trim())
        .filter((v) => !hiddenInstitutions.has(v.toLowerCase()))
    );
    return ["Tümü", ...Array.from(values).sort((a, b) => a.localeCompare(b, "tr"))];
  }, [events, hiddenInstitutions]);

  const priceOptions = useMemo(() => {
    const values = new Set(
      events.map((e) => e.price).filter((v) => typeof v === "string" && v.trim())
    );
    return ["Tümü", ...Array.from(values).sort((a, b) => a.localeCompare(b, "tr"))];
  }, [events]);

  const stats = useMemo(() => {
    const activeEventCount = events.length;
    const institutionCount = Math.max(institutions.length - 1, 0); // "Tümü" hariç
    const cityCount = Math.max(cities.length - 1, 0); // "Tümü" hariç

    return [
      { label: "Aktif Etkinlik", value: formatCompactNumber(activeEventCount) },
      { label: "Kurum", value: formatCompactNumber(institutionCount) },
      { label: "Şehir", value: formatCompactNumber(cityCount) },
    ];
  }, [events, institutions.length, cities.length]);

  const quickAccessItems = useMemo(
    () => [
      {
        icon: TrendingUp,
        label: "Popüler Kurslar",
        count: events.filter((e) => ["Kurs", "Bootcamp"].includes(e.type)).length,
        onClick: () => {
          setSelectedType("Kurs");
          setSelectedPrice("Tümü");
        },
      },
      {
        icon: Trophy,
        label: "Yaklaşan Hackathonlar",
        count: events.filter((e) => e.type === "Hackathon").length,
        onClick: () => {
          setSelectedType("Hackathon");
          setSelectedPrice("Tümü");
        },
      },
      {
        icon: Rocket,
        label: "Bootcamp'ler",
        count: events.filter((e) => e.type === "Bootcamp").length,
        onClick: () => {
          setSelectedType("Bootcamp");
          setSelectedPrice("Tümü");
        },
      },
      {
        icon: GraduationCap,
        label: "Sertifika Programları",
        count: events.filter(
          (e) =>
            (e.title || "").toLowerCase().includes("sertifika") ||
            (e.description || "").toLowerCase().includes("sertifika")
        ).length,
        onClick: () => {
          setSelectedType("Tümü");
          setSearchQuery("sertifika");
        },
      },
      {
        icon: Code2,
        label: "Workshop'lar",
        count: events.filter((e) => e.type === "Workshop").length,
        onClick: () => {
          setSelectedType("Workshop");
          setSelectedPrice("Tümü");
        },
      },
    ],
    [events]
  );

  const topNavItems = useMemo(() => {
    const popularCoursesCount = events.filter((e) =>
      ["Kurs", "Bootcamp"].includes(e.type)
    ).length;
    const hackathonCount = events.filter((e) => e.type === "Hackathon").length;

    return [
      {
        icon: TrendingUp,
        label: "Popüler Kurslar",
        visible: popularCoursesCount > 0,
        onClick: () => {
          setSelectedType("Kurs");
          setSelectedPrice("Tümü");
        },
      },
      {
        icon: Trophy,
        label: "Hackathonlar",
        visible: hackathonCount > 0,
        onClick: () => {
          setSelectedType("Hackathon");
          setSelectedPrice("Tümü");
        },
      },
    ].filter((item) => item.visible);
  }, [events]);

  const scrollToEvents = () => {
    requestAnimationFrame(() => {
      eventsSectionRef.current?.scrollIntoView({
        behavior: "smooth",
        block: "start",
      });
    });
  };

  useEffect(() => {
    if (!cities.includes(selectedCity)) setSelectedCity("Tümü");
  }, [cities, selectedCity]);

  useEffect(() => {
    if (!eventTypes.includes(selectedType)) setSelectedType("Tümü");
  }, [eventTypes, selectedType]);

  useEffect(() => {
    if (!institutions.includes(selectedInstitution)) setSelectedInstitution("Tümü");
  }, [institutions, selectedInstitution]);

  useEffect(() => {
    if (!priceOptions.includes(selectedPrice)) setSelectedPrice("Tümü");
  }, [priceOptions, selectedPrice]);
  const bg = dark ? "#0d1120" : "#f0f4ff";
  const surface = dark ? "#161c2d" : "#ffffff";
  const surfaceBorder = dark ? "#232b3e" : "#e8edf7";
  const textPrimary = dark ? "#e2e8f5" : "#0f172a";
  const textSecondary = dark ? "#8896b3" : "#64748b";
  const navBg = dark ? "rgba(13,17,32,0.85)" : "rgba(240,244,255,0.85)";

  const filtered = events.filter((e) => {
    if (selectedCity !== "Tümü" && e.city !== selectedCity) return false;
    if (selectedType !== "Tümü" && e.type !== selectedType) return false;
    if (
      selectedInstitution !== "Tümü" &&
      e.institution !== selectedInstitution
    )
      return false;
    if (selectedPrice !== "Tümü" && e.price !== selectedPrice) return false;
    if (
      searchQuery &&
      !e.title.toLowerCase().includes(searchQuery.toLowerCase()) &&
      !e.institution.toLowerCase().includes(searchQuery.toLowerCase()) &&
      !e.tags.some((t) => t.toLowerCase().includes(searchQuery.toLowerCase()))
    )
      return false;
    return true;
  });
  const itemsPerPage = 9;
  const totalPages = Math.max(1, Math.ceil(filtered.length / itemsPerPage));
  const paginatedEvents = filtered.slice(
    (currentPage - 1) * itemsPerPage,
    currentPage * itemsPerPage
  );

  useEffect(() => {
    setCurrentPage(1);
  }, [
    selectedCity,
    selectedType,
    selectedInstitution,
    selectedPrice,
    searchQuery,
  ]);

  useEffect(() => {
    if (currentPage > totalPages) {
      setCurrentPage(totalPages);
    }
  }, [currentPage, totalPages]);

  const featuredEvents = events.filter((e) => e.featured);
  const upcomingHackathons = events.filter((e) => e.type === "Hackathon");
  const popularCourses = events
    .filter((e) => ["Kurs", "Bootcamp"].includes(e.type))
    .slice(0, 3);

  return (
    <div
      style={{
        background: bg,
        minHeight: "100vh",
        fontFamily: "'Segoe UI', system-ui, sans-serif",
        position: "relative",
        overflow: "hidden",
      }}
    >
      {/* Navbar */}
      <nav
        style={{
          position: "sticky",
          top: 0,
          zIndex: 100,
          background: navBg,
          backdropFilter: "blur(20px)",
          borderBottom: `1px solid ${surfaceBorder}`,
          padding: "0 24px",
          height: 64,
          display: "flex",
          alignItems: "center",
          justifyContent: "space-between",
        }}
      >
        <div style={{ display: "flex", alignItems: "center", gap: 6 }}>
          <div
            style={{
              width: 58,
              height: 58,
              borderRadius: 10,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              overflow: "hidden",
            }}
          >
            <img
              src="/eventhorizon-logo.png"
              alt="Event Horizon logo"
              style={{ width: 60, height: 60, objectFit: "contain" }}
            />
          </div>
          <div>
            <span
              style={{
                fontSize: 21,
                fontWeight: 800,
                color: textPrimary,
                letterSpacing: "-0.03em",
              }}
            >
              Events{" "}
              <span
                style={{
                  background: "linear-gradient(135deg, #3b82f6, #a855f7)",
                  WebkitBackgroundClip: "text",
                  WebkitTextFillColor: "transparent",
                }}
              >
                Horizon
              </span>
            </span>
          </div>
        </div>

        <div style={{ display: "flex", alignItems: "center", gap: 8 }}>
          {topNavItems.length > 0 && (
            <nav style={{ display: "flex", gap: 4 }}>
              {topNavItems.map(({ icon: Icon, label, onClick }) => (
                <button
                  key={label}
                  onClick={() => {
                    onClick();
                    scrollToEvents();
                  }}
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 5,
                    padding: "6px 12px",
                    borderRadius: 8,
                    border: "none",
                    background: "transparent",
                    color: textSecondary,
                    fontSize: 13,
                    fontWeight: 500,
                    cursor: "pointer",
                  }}
                >
                  <Icon size={14} />
                  {label}
                </button>
              ))}
            </nav>
          )}

          <button
            onClick={() => setDark(!dark)}
            style={{
              width: 36,
              height: 36,
              borderRadius: 8,
              border: `1px solid ${surfaceBorder}`,
              background: surface,
              color: textSecondary,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              cursor: "pointer",
            }}
          >
            {dark ? <Sun size={15} /> : <Moon size={15} />}
          </button>
        </div>
      </nav>

      {/* Hero */}
      <section
        style={{
          position: "relative",
          padding: "80px 24px 60px",
          textAlign: "center",
          overflow: "hidden",
        }}
      >
        <GradientOrb
          x="5%"
          y="-20%"
          color="#3b82f6"
          size={500}
          opacity={0.12}
        />
        <GradientOrb
          x="60%"
          y="-10%"
          color="#a855f7"
          size={400}
          opacity={0.1}
        />
        <GradientOrb
          x="30%"
          y="60%"
          color="#06b6d4"
          size={300}
          opacity={0.08}
        />

        <div
          style={{
            position: "relative",
            zIndex: 1,
            maxWidth: 720,
            margin: "0 auto",
          }}
        >
          <div
            style={{
              display: "inline-flex",
              alignItems: "center",
              gap: 6,
              padding: "5px 14px",
              borderRadius: 99,
              border: `1px solid ${dark ? "#2d3a52" : "#c7d4f0"}`,
              background: dark ? "#161c2d" : "#eef2ff",
              color: dark ? "#60a5fa" : "#3b82f6",
              fontSize: 12,
              fontWeight: 600,
              letterSpacing: "0.04em",
              marginBottom: 20,
            }}
          >
            <Cpu size={12} /> AI Destekli Platform · Türkiye Geneli
          </div>

          <h1
            style={{
              fontSize: "clamp(32px, 5vw, 56px)",
              fontWeight: 900,
              lineHeight: 1.1,
              letterSpacing: "-0.04em",
              color: textPrimary,
              marginBottom: 16,
            }}
          >
            Şehrindeki teknoloji
            <br />
            <span
              style={{
                background:
                  "linear-gradient(135deg, #3b82f6 0%, #a855f7 50%, #06b6d4 100%)",
                WebkitBackgroundClip: "text",
                WebkitTextFillColor: "transparent",
              }}
            >
              fırsatlarını keşfet.
            </span>
          </h1>

          <p
            style={{
              fontSize: 17,
              color: textSecondary,
              lineHeight: 1.6,
              marginBottom: 36,
              maxWidth: 520,
              margin: "0 auto 36px",
            }}
          >
            Türkiye genelindeki teknoloji etkinliklerini, kursları ve
            hackathonları tek platformda keşfet. AI destekli akıllı filtreleme
            ile sana en uygun fırsatı bul.
          </p>

          {/* Search Bar */}
          <div
            style={{
              display: "flex",
              gap: 10,
              maxWidth: 580,
              margin: "0 auto",
              flexWrap: "wrap",
              justifyContent: "center",
            }}
          >
            <div
              style={{
                flex: 1,
                minWidth: 240,
                position: "relative",
              }}
            >
              <Search
                size={16}
                style={{
                  position: "absolute",
                  left: 14,
                  top: "50%",
                  transform: "translateY(-50%)",
                  color: textSecondary,
                }}
              />
              <input
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                placeholder="Etkinlik, kurum veya teknoloji ara..."
                style={{
                  width: "100%",
                  padding: "13px 16px 13px 40px",
                  borderRadius: 12,
                  border: `1.5px solid ${dark ? "#2d3a52" : "#c7d4f0"}`,
                  background: dark ? "#161c2d" : "#ffffff",
                  color: textPrimary,
                  fontSize: 14,
                  outline: "none",
                  boxSizing: "border-box",
                }}
              />
            </div>

            <select
              value={selectedCity}
              onChange={(e) => setSelectedCity(e.target.value)}
              style={{
                padding: "13px 16px",
                borderRadius: 12,
                border: `1.5px solid ${dark ? "#2d3a52" : "#c7d4f0"}`,
                background: dark ? "#161c2d" : "#ffffff",
                color: textPrimary,
                fontSize: 14,
                cursor: "pointer",
                outline: "none",
              }}
            >
              {cities.map((c) => (
                <option key={c} value={c}>
                  {c === "Tümü" ? "🏙 Şehir Seç" : `📍 ${c}`}
                </option>
              ))}
            </select>

            <button
              style={{
                padding: "13px 22px",
                borderRadius: 12,
                border: "none",
                background: "linear-gradient(135deg, #3b82f6, #6366f1)",
                color: "white",
                fontSize: 14,
                fontWeight: 700,
                cursor: "pointer",
                display: "flex",
                alignItems: "center",
                gap: 6,
                whiteSpace: "nowrap",
              }}
            >
              <Search size={15} /> Ara
            </button>
          </div>

          {/* Stats */}
          <div
            style={{
              display: "flex",
              justifyContent: "center",
              gap: 32,
              marginTop: 40,
              flexWrap: "wrap",
            }}
          >
            {stats.map(({ label, value }) => (
              <div key={label} style={{ textAlign: "center" }}>
                <div
                  style={{
                    fontSize: 26,
                    fontWeight: 800,
                    color: textPrimary,
                    letterSpacing: "-0.03em",
                    background: "linear-gradient(135deg, #3b82f6, #a855f7)",
                    WebkitBackgroundClip: "text",
                    WebkitTextFillColor: "transparent",
                  }}
                >
                  {value}
                </div>
                <div
                  style={{
                    fontSize: 12,
                    color: textSecondary,
                    fontWeight: 500,
                  }}
                >
                  {label}
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Main Content */}
      <div
        style={{
          maxWidth: 1280,
          margin: "0 auto",
          padding: "0 24px 60px",
          display: "flex",
          gap: 24,
        }}
      >
        {/* Sidebar */}
        <aside style={{ width: 240, flexShrink: 0 }}>
          <div
            style={{
              background: surface,
              border: `1px solid ${surfaceBorder}`,
              borderRadius: 16,
              padding: 20,
              marginBottom: 16,
              position: "sticky",
              top: 80,
            }}
          >
            <h3
              style={{
                fontSize: 13,
                fontWeight: 700,
                letterSpacing: "0.06em",
                textTransform: "uppercase",
                color: textSecondary,
                marginBottom: 16,
                display: "flex",
                alignItems: "center",
                gap: 6,
              }}
            >
              <Filter size={13} /> Filtreler
            </h3>

            <div style={{ marginBottom: 20 }}>
              <div
                style={{
                  fontSize: 12,
                  fontWeight: 600,
                  color: textSecondary,
                  marginBottom: 8,
                  textTransform: "uppercase",
                  letterSpacing: "0.05em",
                }}
              >
                Etkinlik Türü
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                {eventTypes.map((t) => (
                  <button
                    key={t}
                    onClick={() => setSelectedType(t)}
                    style={{
                      padding: "7px 10px",
                      borderRadius: 8,
                      border: "none",
                      background:
                        selectedType === t
                          ? dark
                            ? "#1e3a6e"
                            : "#dbeafe"
                          : "transparent",
                      color:
                        selectedType === t
                          ? dark
                            ? "#60a5fa"
                            : "#1d4ed8"
                          : textSecondary,
                      fontSize: 13,
                      fontWeight: selectedType === t ? 700 : 400,
                      cursor: "pointer",
                      textAlign: "left",
                      display: "flex",
                      alignItems: "center",
                      gap: 8,
                    }}
                  >
                    {selectedType === t && (
                      <div
                        style={{
                          width: 4,
                          height: 4,
                          borderRadius: "50%",
                          background: "#3b82f6",
                        }}
                      />
                    )}
                    {t}
                  </button>
                ))}
              </div>
            </div>

            <div style={{ marginBottom: 20 }}>
              <div
                style={{
                  fontSize: 12,
                  fontWeight: 600,
                  color: textSecondary,
                  marginBottom: 8,
                  textTransform: "uppercase",
                  letterSpacing: "0.05em",
                }}
              >
                Ücret
              </div>
              <div style={{ display: "flex", gap: 6 }}>
                {priceOptions.map((p) => (
                  <button
                    key={p}
                    onClick={() => setSelectedPrice(p)}
                    style={{
                      flex: 1,
                      padding: "7px 6px",
                      borderRadius: 8,
                      border: `1px solid ${selectedPrice === p ? "#3b82f6" : surfaceBorder}`,
                      background:
                        selectedPrice === p
                          ? "linear-gradient(135deg, #3b82f6, #6366f1)"
                          : "transparent",
                      color: selectedPrice === p ? "white" : textSecondary,
                      fontSize: 11,
                      fontWeight: 600,
                      cursor: "pointer",
                    }}
                  >
                    {p}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <div
                style={{
                  fontSize: 12,
                  fontWeight: 600,
                  color: textSecondary,
                  marginBottom: 8,
                  textTransform: "uppercase",
                  letterSpacing: "0.05em",
                }}
              >
                Kurum
              </div>
              <div style={{ display: "flex", flexDirection: "column", gap: 4 }}>
                {institutions.map((i) => (
                  <button
                    key={i}
                    onClick={() => setSelectedInstitution(i)}
                    style={{
                      padding: "7px 10px",
                      borderRadius: 8,
                      border: "none",
                      background:
                        selectedInstitution === i
                          ? dark
                            ? "#1e3a6e"
                            : "#dbeafe"
                          : "transparent",
                      color:
                        selectedInstitution === i
                          ? dark
                            ? "#60a5fa"
                            : "#1d4ed8"
                          : textSecondary,
                      fontSize: 12,
                      fontWeight: selectedInstitution === i ? 700 : 400,
                      cursor: "pointer",
                      textAlign: "left",
                    }}
                  >
                    {i}
                  </button>
                ))}
              </div>
            </div>
          </div>

          {/* Quick Links */}
          <div
            style={{
              background: surface,
              border: `1px solid ${surfaceBorder}`,
              borderRadius: 16,
              padding: 20,
            }}
          >
            <h3
              style={{
                fontSize: 13,
                fontWeight: 700,
                letterSpacing: "0.06em",
                textTransform: "uppercase",
                color: textSecondary,
                marginBottom: 14,
              }}
            >
              Hızlı Erişim
            </h3>
            {quickAccessItems.map(({ icon: Icon, label, count, onClick }) => (
              <button
                key={label}
                onClick={onClick}
                style={{
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  width: "100%",
                  padding: "8px 10px",
                  borderRadius: 8,
                  border: "none",
                  background: "transparent",
                  color: textPrimary,
                  fontSize: 12,
                  fontWeight: 500,
                  cursor: "pointer",
                  marginBottom: 2,
                  gap: 8,
                }}
              >
                <span style={{ display: "flex", alignItems: "center", gap: 8 }}>
                  <Icon size={13} style={{ color: "#6366f1" }} />
                  {label}
                </span>
                <span
                  style={{
                    fontSize: 10,
                    fontWeight: 700,
                    padding: "2px 7px",
                    borderRadius: 99,
                    background: dark ? "#1e2535" : "#f1f5f9",
                    color: textSecondary,
                  }}
                >
                  {count}
                </span>
              </button>
            ))}
          </div>
        </aside>

        {/* Main */}
        <main style={{ flex: 1, minWidth: 0 }}>
          {/* City Filter Chips */}
          <div
            style={{
              display: "flex",
              gap: 8,
              marginBottom: 20,
              overflowX: "auto",
              paddingBottom: 4,
            }}
          >
            <span
              style={{
                display: "flex",
                alignItems: "center",
                fontSize: 13,
                color: textSecondary,
                fontWeight: 500,
                whiteSpace: "nowrap",
                paddingRight: 4,
              }}
            >
              <MapPin size={13} style={{ marginRight: 4 }} /> Şehir:
            </span>
            {cities.map((c) => (
              <FilterChip
                key={c}
                label={c}
                active={selectedCity === c}
                onClick={() => setSelectedCity(c)}
                dark={dark}
              />
            ))}
          </div>

          {/* Result Header */}
          <div
            ref={eventsSectionRef}
            style={{
              display: "flex",
              justifyContent: "space-between",
              alignItems: "center",
              marginBottom: 20,
            }}
          >
            <div>
              <h2
                style={{
                  fontSize: 20,
                  fontWeight: 800,
                  color: textPrimary,
                  letterSpacing: "-0.02em",
                }}
              >
                {filtered.length} Etkinlik Bulundu
              </h2>
              <p style={{ fontSize: 13, color: textSecondary, marginTop: 2 }}>
                {selectedCity !== "Tümü" ? `${selectedCity} · ` : ""}
                {selectedType !== "Tümü" ? `${selectedType} · ` : ""}
                Tüm tarihler
              </p>
            </div>
          </div>

          {/* Featured Banner */}
          {featuredEvents.length > 0 &&
            selectedCity !== "İstanbul" &&
            selectedCity !== "Ankara" && (
              <div
                style={{
                  marginBottom: 24,
                  padding: "20px 24px",
                  borderRadius: 16,
                  background: "linear-gradient(135deg, #1e3a6e22, #4c1d9522)",
                  border: `1px solid ${dark ? "#2d3a6e" : "#bfdbfe"}`,
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "space-between",
                  gap: 16,
                  flexWrap: "wrap",
                }}
              >
                <div style={{ display: "flex", alignItems: "center", gap: 14 }}>
                  <div
                    style={{
                      width: 44,
                      height: 44,
                      borderRadius: 12,
                      background: "linear-gradient(135deg,#f59e0b,#f97316)",
                      display: "flex",
                      alignItems: "center",
                      justifyContent: "center",
                    }}
                  >
                    <Star size={20} color="white" />
                  </div>
                  <div>
                    <div
                      style={{
                        fontSize: 14,
                        fontWeight: 800,
                        color: textPrimary,
                      }}
                    >
                      Gaziantep Tech Hackathon 2025
                    </div>
                    <div style={{ fontSize: 12, color: textSecondary }}>
                      5–7 Haziran · Ücretsiz · Yüz Yüze
                    </div>
                  </div>
                </div>
                <button
                  style={{
                    padding: "9px 18px",
                    borderRadius: 10,
                    border: "none",
                    background: "linear-gradient(135deg,#f59e0b,#f97316)",
                    color: "white",
                    fontSize: 13,
                    fontWeight: 700,
                    cursor: "pointer",
                    display: "flex",
                    alignItems: "center",
                    gap: 6,
                  }}
                >
                  Hemen Başvur <ArrowRight size={13} />
                </button>
              </div>
            )}

          {/* Event Grid */}
          {filtered.length === 0 ? (
            <div
              style={{
                textAlign: "center",
                padding: "60px 20px",
                color: textSecondary,
              }}
            >
              <Search size={36} style={{ marginBottom: 12, opacity: 0.4 }} />
              <div style={{ fontSize: 16, fontWeight: 600 }}>
                Sonuç bulunamadı
              </div>
              <div style={{ fontSize: 13, marginTop: 6 }}>
                Filtrelerinizi değiştirmeyi deneyin
              </div>
            </div>
          ) : (
            <div
              style={{
                display: "grid",
                gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))",
                gap: 18,
              }}
            >
              {paginatedEvents.map((event) => (
                <EventCard key={event.id} event={event} dark={dark} />
              ))}
            </div>
          )}

          {filtered.length > itemsPerPage && (
            <div
              style={{
                marginTop: 20,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                gap: 10,
                flexWrap: "wrap",
              }}
            >
              <button
                onClick={() => setCurrentPage((p) => Math.max(1, p - 1))}
                disabled={currentPage === 1}
                style={{
                  padding: "8px 12px",
                  borderRadius: 8,
                  border: `1px solid ${surfaceBorder}`,
                  background: dark ? "#161c2d" : "#ffffff",
                  color: textPrimary,
                  cursor: currentPage === 1 ? "not-allowed" : "pointer",
                  opacity: currentPage === 1 ? 0.5 : 1,
                  fontSize: 12,
                  fontWeight: 600,
                }}
              >
                Önceki
              </button>

              <span
                style={{
                  fontSize: 12,
                  color: textSecondary,
                  fontWeight: 600,
                }}
              >
                Sayfa {currentPage} / {totalPages}
              </span>

              <button
                onClick={() =>
                  setCurrentPage((p) => Math.min(totalPages, p + 1))
                }
                disabled={currentPage === totalPages}
                style={{
                  padding: "8px 12px",
                  borderRadius: 8,
                  border: `1px solid ${surfaceBorder}`,
                  background: dark ? "#161c2d" : "#ffffff",
                  color: textPrimary,
                  cursor: currentPage === totalPages ? "not-allowed" : "pointer",
                  opacity: currentPage === totalPages ? 0.5 : 1,
                  fontSize: 12,
                  fontWeight: 600,
                }}
              >
                Sonraki
              </button>
            </div>
          )}

          {/* Upcoming Hackathons Section */}
          <div style={{ marginTop: 40 }}>
            <div
              style={{
                display: "flex",
                alignItems: "center",
                marginBottom: 18,
              }}
            >
              <h2
                style={{
                  fontSize: 18,
                  fontWeight: 800,
                  color: textPrimary,
                  display: "flex",
                  alignItems: "center",
                  gap: 8,
                  letterSpacing: "-0.02em",
                }}
              >
                <Trophy size={18} style={{ color: "#f59e0b" }} /> Yaklaşan
                Hackathonlar
              </h2>
            </div>
            <div
              style={{
                display: "flex",
                gap: 16,
                overflowX: "auto",
                paddingBottom: 8,
              }}
            >
              {upcomingHackathons.map((e) => (
                <div
                  key={e.id}
                  style={{
                    minWidth: 260,
                    background: surface,
                    border: `1px solid ${surfaceBorder}`,
                    borderRadius: 14,
                    padding: "16px 18px",
                    flexShrink: 0,
                  }}
                >
                  <div
                    style={{
                      display: "flex",
                      alignItems: "center",
                      gap: 10,
                      marginBottom: 12,
                    }}
                  >
                    <div
                      style={{
                        width: 40,
                        height: 40,
                        borderRadius: 10,
                        background: e.institutionColor,
                        display: "flex",
                        alignItems: "center",
                        justifyContent: "center",
                      }}
                    >
                      <Trophy size={18} color="white" />
                    </div>
                    <div>
                      <div
                        style={{
                          fontSize: 13,
                          fontWeight: 700,
                          color: textPrimary,
                        }}
                      >
                        {e.title}
                      </div>
                      <div style={{ fontSize: 11, color: textSecondary }}>
                        {e.institution}
                      </div>
                    </div>
                  </div>
                  <div
                    style={{
                      display: "flex",
                      justifyContent: "space-between",
                      fontSize: 12,
                      color: textSecondary,
                    }}
                  >
                    <span
                      style={{ display: "flex", alignItems: "center", gap: 4 }}
                    >
                      <Calendar size={11} />
                      {e.date}
                    </span>
                    <span
                      style={{ display: "flex", alignItems: "center", gap: 4 }}
                    >
                      <MapPin size={11} />
                      {e.city}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}
