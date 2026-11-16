#!/usr/bin/env python3
"""Genera variants/variante-{a,b,c}.html a partir del mismo contenido."""
import json, os, sys, html

OUT = sys.argv[1]
SITE = "https://ltmpartners.site"
E = html.escape

# ───────────────────────── CONTENIDO (copiado de ltmpartners.site) ─────────────────────────
BRANDS = [
    ("1xBet", "https://i.ibb.co/67jfyp5D/1xbet-logo-png-seeklogo-355459-removebg-preview.png"),
    ("1Win", "https://i.ibb.co/hJ6RFwXv/1win-official-logo.png"),
    ("Stake", "https://i.ibb.co/xSJSD6m6/stake.png"),
    ("Novibet", "https://i.ibb.co/RGfcf5M6/Novibet-780x228.png"),
    ("Pin-Up", "https://i.ibb.co/B2zSXNgV/Pin-Up-Logo-2018-Global-s1280.png"),
    ("BC.Game", "https://i.ibb.co/7tFMJ8JS/13d0b148684103ce7a2d7976cb16e6e9-removebg-preview.png"),
    ("Melbet", "https://i.ibb.co/601TPWnN/mlbet.png"),
    ("Betjam", "https://i.ibb.co/84bJ5FG8/betjam.png"),
    ("Betwinner", "https://i.ibb.co/HLjRksp4/images-1.png"),
]
STATS = [  # (valor, prefijo, sufijo, etiqueta)
    (200, "", "+", "Creadores y streamers"),
    (4, "", "", "GEOs clave activos"),
    (100, "", "%", "Audiencia verificada"),
]
SERVICES = [
    ("tv", "Representación de talentos", "Control total de audiencias +18 en Kick, Twitch e Instagram. Gestión exclusiva de streamers."),
    ("target", "Estrategia CPA y FTD", "Orientados a resultados reales, depósitos y retención de jugadores."),
    ("shield", "Verificación y estadísticas por GEO", "Reportes transparentes, prevención antifraude y métricas verificadas."),
    ("megaphone", "Campañas orgánicas", "Integraciones nativas de marca, reels y streams temáticos que convierten."),
]
MODELS = [
    ("CPA", "Costo por adquisición",
     "La marca paga por cada jugador referido que cumple la condición acordada en la campaña.",
     "Condición de calificación y tarifa por GEO"),
    ("FTD", "Primer depósito",
     "El resultado se mide en jugadores que realizan su primer depósito en la plataforma de la marca.",
     "Depósito mínimo y tarifa por GEO"),
]
METHOD = [
    ("Diagnóstico", "Definimos con la marca el objetivo, los GEOs y el modelo de pago (CPA o FTD)."),
    ("Selección de talento", "Elegimos creadores con audiencia +18 verificada en el mercado objetivo."),
    ("Activación", "Integraciones nativas, reels y streams temáticos alineados con la marca."),
    ("Medición y reporte", "Reportes transparentes por GEO, prevención antifraude y optimización continua."),
]
CREATORS = [  # nombre, plataforma, país, bandera, categoría, métrica, enlace, imagen
    ("Jongotti", "Kick", "Chile", "🇨🇱", "IRL / Slots", "100K seguidores", "https://kick.com/jongottii", f"{SITE}/images/jongotti.jpg"),
    ("Ivo Theiler", "Instagram", "Argentina", "🇦🇷", "IRL Lifestyle", "+1M vistas", "https://www.instagram.com/ivotheiler_", f"{SITE}/images/ivotheiler.jpg"),
    ("Juan Antonucci", "Instagram", "Argentina", "🇦🇷", "IRL / Lifestyle", "+500K vistas", "https://www.instagram.com/juanantonuccid", f"{SITE}/images/juan.jpg"),
    ("Nicolas Andres", "Instagram", "Chile", "🇨🇱", "IRL / Lifestyle", "Alta interacción", "https://www.instagram.com/nicoandress_p/", f"{SITE}/images/nicolas.jpg"),
]
IMG = f"{SITE}/images/"
GEOS = [
    {"key": "chile", "flag": "🇨🇱", "title": "Chile", "tier": "Tier 1 LATAM",
     "tagline": "Amplia cobertura en Kick, Twitch e Instagram",
     "description": "Mercado líder en valor por jugador y retención en la región.",
     "stats": [["Streamers exclusivos", "65+"], ["Audiencia mensual", "2.8M+"], ["FTD promedio", "14.6%"], ["Plataformas principales", "Kick · IG"]],
     "creators": [
         {"name": "Jongotti", "platform": "Kick", "tag": "IRL / Slots", "metric": "100K seguidores", "link": "https://kick.com/jongottii", "img": IMG + "jongotti.jpg"},
         {"name": "Bynico", "platform": "Kick", "tag": "Juegos / Slots", "metric": "+750 vistas", "link": "https://kick.com/byn1co", "img": IMG + "byn1co.jpg"},
         {"name": "Nicolas Andres", "platform": "Instagram", "tag": "IRL / Lifestyle", "metric": "Alta interacción", "link": "https://www.instagram.com/nicoandress_p/", "img": IMG + "nicolas.jpg"}]},
    {"key": "bolivia", "flag": "🇧🇴", "title": "Bolivia", "tier": "Alto crecimiento",
     "tagline": "Fuerte presencia en transmisiones", "description": "Mercado de rápida expansión y eficiencia.",
     "stats": [["Influencers activos", "45+"], ["Audiencia mensual", "1.4M+"], ["FTD promedio", "16.8%"], ["Plataformas principales", "Kick · Reels"]],
     "creators": [{"name": "Carlitos Leanos", "platform": "Instagram", "tag": "Blogger", "metric": "+50K seguidores", "link": "https://www.instagram.com/carlitosleanos/", "img": IMG + "carlitosleanos.jpg"}]},
    {"key": "argentina", "flag": "🇦🇷", "title": "Argentina", "tier": "Tráfico masivo",
     "tagline": "Tráfico masivo de entretenimiento", "description": "El mayor volumen orgánico en habla hispana.",
     "stats": [["Creadores en roster", "80+"], ["Audiencia mensual", "6.2M+"], ["FTD promedio", "12.4%"], ["Plataformas principales", "Twitch · IG"]],
     "creators": [
         {"name": "Ivo Theiler", "platform": "Instagram", "tag": "IRL Lifestyle", "metric": "+1M vistas", "link": "https://www.instagram.com/ivotheiler_", "img": IMG + "ivotheiler.jpg"},
         {"name": "Juan Antonucci", "platform": "Instagram", "tag": "IRL / Lifestyle", "metric": "+500K vistas", "link": "https://www.instagram.com/juanantonuccid", "img": IMG + "juan.jpg"}]},
    {"key": "peru", "flag": "🇵🇪", "title": "Perú", "tier": "Mercado regulado",
     "tagline": "Conversión de alto valor.", "description": "Fuerte tradición de slots y crash.",
     "stats": [["Streamers activos", "40+"], ["Audiencia mensual", "1.9M+"], ["FTD promedio", "15.1%"], ["Plataformas principales", "Kick · TikTok"]],
     "creators": [{"name": "Diego \"ElPeru\"", "platform": "Kick", "tag": "Slots · apuestas altas", "metric": "310K+ seguidores", "link": "", "img": ""}]},
    {"key": "colombia", "flag": "🇨🇴", "title": "Colombia", "tier": "Listo para Coljuegos",
     "tagline": "Ecosistema consolidado.", "description": "Acceso a audiencias maduras.",
     "stats": [["Talentos afiliados", "50+"], ["Audiencia mensual", "3.1M+"], ["FTD promedio", "13.8%"], ["Plataformas principales", "Instagram · Kick"]],
     "creators": [{"name": "Camilo Parra", "platform": "Kick", "tag": "Casino y ruleta", "metric": "390K+ seguidores", "link": "", "img": ""}]},
    {"key": "mexico", "flag": "🇲🇽", "title": "México", "tier": "Mercado de gran escala",
     "tagline": "Mercado de mayor escala.", "description": "Rápido crecimiento en apuestas digitales.",
     "stats": [["Creadores en red", "75+"], ["Audiencia mensual", "7.8M+"], ["FTD promedio", "11.9%"], ["Plataformas principales", "YouTube · Kick"]],
     "creators": [{"name": "Rodrigo \"ElAzteca\"", "platform": "YouTube", "tag": "Reseñas de casino", "metric": "1.8M+ vistas", "link": "", "img": ""}]},
    {"key": "global", "flag": "🌐", "title": "Global", "tier": "Transfronterizo",
     "tagline": "Comunidades hispanas globales.", "description": "Tráfico proveniente de EE. UU., España y LATAM.",
     "stats": [["Creadores globales", "90+"], ["GEOs conectados", "17 países"], ["FTD promedio", "$85+ USD"], ["Plataformas principales", "Kick · Twitch"]],
     "creators": [{"name": "IberianBets ES", "platform": "Twitch", "tag": "Apuestas altas · UE", "metric": "890K+ vistas", "link": "", "img": ""}]},
]
LEGAL = [("Política de privacidad", f"{SITE}/privacidad"), ("Política de cookies", f"{SITE}/cookies"),
         ("Términos y condiciones", f"{SITE}/terminos"), ("Cumplimiento", f"{SITE}/cumplimiento")]
CALENDLY = "https://calendly.com/tkzykv/30min"
TELEGRAM = "https://t.me/tkykv"
WHATSAPP = "https://wa.me/56930645385"
EMAIL = "cristobal@ltmpartners.site"

ICONS = {
    "tv": '<rect width="20" height="15" x="2" y="7" rx="2"/><path d="m17 2-5 5-5-5"/>',
    "target": '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>',
    "shield": '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    "megaphone": '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    "arrow": '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>',
    "send": '<path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/>',
    "chat": '<path d="M7.9 20A9 9 0 1 0 4 16.1L2 22Z"/>',
    "mail": '<rect width="20" height="16" x="2" y="4" rx="2"/><path d="m22 7-10 5L2 7"/>',
    "cal": '<rect width="18" height="18" x="3" y="4" rx="2"/><path d="M16 2v4M8 2v4M3 10h18"/>',
    "menu": '<path d="M4 7h16M4 12h16M4 17h16"/>',
    "x": '<path d="M18 6 6 18M6 6l12 12"/>',
}
def ico(name, cls="ico"):
    return f'<svg class="{cls}" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.75" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">{ICONS[name]}</svg>'

SPADE = ('<svg class="logo-mark" viewBox="0 0 100 100" aria-hidden="true"><path d="M 50 11 C 52 14, 66 28, 77 40 C 86 50, 88 64, 82 74 C 75 83, 63 84, 55 76 C 54 75, 52 73, 51 72 C 52 76, 56 83, 62 89 L 38 89 C 44 83, 48 76, 49 72 C 48 73, 46 75, 45 76 C 37 84, 25 83, 18 74 C 12 64, 14 50, 23 40 C 34 28, 48 14, 50 11 Z" fill="none" stroke="currentColor" stroke-width="6" stroke-linejoin="round"/>'
         '<path d="M 33 23.5 C 35 24, 38 27, 41 27.5 C 43 27, 45 28.5, 46 31 C 44 32.5, 44 34.5, 47 35 C 49 33, 52 33.5, 53 36 C 51 37.5, 49 38, 48 40.5 C 47.5 42, 49 43, 50 43.5 C 53 41.5, 57 41.5, 61 43 C 65 44, 68 47, 67.5 50.5 C 66.5 54, 63.5 56.5, 60.5 57 C 59.5 60, 57.5 63, 55.5 66 L 53.5 71.5 L 52 76.5 L 50.5 72.5 C 50 67, 48.5 62, 47.5 57 C 46.5 52, 47 48, 44.5 46 L 43 45 L 39.5 41.5 L 36.5 37 L 33 32.5 C 32 30, 31.5 27, 33 23.5 Z" fill="currentColor"/></svg>')

def todo(txt):
    return f'<span class="todo">[COMPLETAR: {E(txt)}]</span>'

def initials(name):
    parts = [p for p in name.replace('"', "").split() if p]
    return (parts[0][0] + (parts[1][0] if len(parts) > 1 else "")).upper()

# ───────────────────────── SECCIONES ─────────────────────────
NAV = [("Servicios", "#servicios"), ("Metodología", "#metodologia"), ("Creadores", "#creadores"), ("GEOs", "#geos"), ("Contacto", "#contacto")]

def brand_html():
    return f'<a href="#inicio" class="brand" aria-label="LTM Partners, inicio">{SPADE}<span class="brand-txt"><b>LTM</b> PARTNERS</span></a>'

def nav():
    links = "".join(f'<a href="{h}" class="nav-link">{t}</a>' for t, h in NAV)
    mlinks = "".join(f'<a href="{h}">{t}</a>' for t, h in NAV)
    return f'''
<a href="#main" class="skip">Saltar al contenido</a>
<header class="nav" id="nav">
  <div class="wrap nav-in">
    {brand_html()}
    <nav class="nav-links" aria-label="Principal">{links}</nav>
    <div class="nav-cta">
      <a class="btn btn-ghost btn-sm" href="{CALENDLY}" target="_blank" rel="noopener">Agendar llamada</a>
      <a class="btn btn-primary btn-sm" href="#postular">Conviértete en afiliado {ico("arrow")}</a>
    </div>
    <button class="menu-btn" id="menu-btn" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu">{ico("menu")}</button>
  </div>
</header>
<div class="menu" id="menu" hidden>
  <button class="menu-close" id="menu-close" aria-label="Cerrar menú">{ico("x")}</button>
  <nav aria-label="Móvil">{mlinks}</nav>
  <a class="btn btn-primary" href="#postular">Conviértete en afiliado {ico("arrow")}</a>
  <a class="btn btn-ghost" href="{CALENDLY}" target="_blank" rel="noopener">Agendar llamada</a>
</div>'''

def head(v, num, eyebrow, title, lead=""):
    lead_html = f'<p class="lead">{lead}</p>' if lead else ""
    if v == "a":
        return f'<div class="sec-head" data-reveal><p class="eyebrow"><span class="acc">{num}</span> / {eyebrow}</p><h2 class="h2">{title}</h2>{lead_html}</div>'
    if v == "b":
        return f'<div class="sec-head" data-reveal><div class="sec-meta"><span class="num">{num}</span><span class="eyebrow">{eyebrow}</span></div><div><h2 class="h2">{title}</h2>{lead_html}</div></div>'
    return f'<div class="sec-head" data-reveal><p class="eyebrow">{eyebrow}</p><h2 class="h2">{title}</h2>{lead_html}</div>'

def counter(n, pre, suf):
    return f'<span class="count" data-count="{n}" data-prefix="{pre}" data-suffix="{suf}">{pre}{n}{suf}</span>'

HERO_P = "Selección de talento, colaboraciones comerciales y campañas con objetivos definidos para los mercados adecuados. Orientados a CPA y performance verificable."

def hero_ctas():
    return f'''<div class="ctas">
      <a class="btn btn-primary" href="{CALENDLY}" target="_blank" rel="noopener">Hablar sobre una campaña {ico("arrow")}</a>
      <a class="btn btn-ghost" href="#postular">Postular como creador {ico("arrow")}</a>
    </div>'''

def hero(v):
    markets = [(g["flag"], g["title"], g["tier"]) for g in GEOS]
    if v == "a":
        rows = "".join(f'<li><span class="dot"></span><span>{f} {t}</span><span class="mono dim">{E(tier)}</span></li>' for f, t, tier in markets)
        return f'''
<section class="hero" id="inicio">
  <div class="wrap hero-grid">
    <div data-reveal>
      <p class="eyebrow"><span class="acc">●</span> Tráfico iGaming · LATAM</p>
      <h1 class="h1">Conectamos marcas de iGaming con <span class="acc">creadores de LATAM.</span></h1>
      <p class="lead">{HERO_P}</p>
      {hero_ctas()}
    </div>
    <aside class="panel" data-reveal style="--i:2" aria-label="Mercados">
      <div class="panel-head"><span>MERCADOS</span><span class="dim">modelo: CPA / FTD</span></div>
      <ul class="market-list">{rows}</ul>
    </aside>
  </div>
</section>'''
    if v == "b":
        line_list = " · ".join(t for _, t, _ in markets)
        return f'''
<section class="hero" id="inicio">
  <div class="wrap">
    <p class="eyebrow hero-eyebrow">Tráfico iGaming · LATAM</p>
    <h1 class="display hero-title" aria-label="Conectamos marcas de iGaming con creadores de LATAM.">
      <span class="line" aria-hidden="true"><span>Conectamos marcas</span></span>
      <span class="line" aria-hidden="true"><span>de iGaming con</span></span>
      <span class="line" aria-hidden="true"><span><em>creadores de LATAM.</em></span></span>
    </h1>
    <div class="hero-foot">
      <p class="lead hero-lead">{HERO_P}</p>
      <div>
        {hero_ctas()}
        <p class="hero-markets">{line_list}</p>
      </div>
    </div>
  </div>
</section>'''
    # c: bento hero con contadores incluidos
    chips = "".join(f'<li>{f} {t}</li>' for f, t, _ in markets)
    stats = "".join(f'<div class="card tile tile-stat" data-reveal style="--i:{i+1}">{counter(n, p, s)}<p>{l}</p></div>' for i, (n, p, s, l) in enumerate(STATS))
    return f'''
<section class="hero" id="inicio">
  <div class="wrap bento hero-bento" id="cifras">
    <div class="card tile tile-hero" data-reveal>
      <p class="eyebrow">Tráfico iGaming · LATAM</p>
      <h1 class="h1">Conectamos marcas de iGaming con <span class="acc">creadores de LATAM.</span></h1>
      <p class="lead">{HERO_P}</p>
      {hero_ctas()}
    </div>
    {stats}
    <div class="card tile tile-stat tile-models" data-reveal style="--i:4"><span class="count static">CPA / FTD</span><p>Modelos de performance</p></div>
    <div class="card tile tile-markets" data-reveal style="--i:5"><p class="tile-label">Mercados</p><ul class="chips">{chips}</ul></div>
  </div>
</section>'''

def brands(v):
    def one_set(hidden):
        imgs = "".join(f'<img class="brand-logo" src="{src}" alt="{"" if hidden else E(n)}" loading="lazy" decoding="async" width="120" height="40" data-name="{E(n)}" onerror="var s=document.createElement(\'span\');s.className=\'brand-name\';s.textContent=this.dataset.name;this.replaceWith(s)">' for n, src in BRANDS)
        return f'<div class="marquee-set"{" aria-hidden=\"true\"" if hidden else ""}>{imgs}</div>'
    return f'''
<section class="brands" id="marcas" aria-label="Marcas">
  <div class="wrap"><p class="brands-title" data-reveal>Generamos tráfico de alto impacto para marcas líderes</p></div>
  <div class="marquee" data-reveal><div class="marquee-track">{one_set(False)}{one_set(True)}</div></div>
</section>'''

def stats(v):
    if v == "c":
        return ""  # en C los contadores viven en el bento del hero (#cifras)
    items = "".join(f'<div class="stat" data-reveal style="--i:{i}">{counter(n, p, s)}<p>{l}</p></div>' for i, (n, p, s, l) in enumerate(STATS))
    items += f'<div class="stat" data-reveal style="--i:3"><span class="count static">CPA / FTD</span><p>Modelos de performance</p></div>'
    return f'<section class="stats" id="cifras" aria-label="Cifras"><div class="wrap stats-grid">{items}</div></section>'

def models(v):
    cards = "".join(f'''<article class="card model hoverable" data-reveal style="--i:{i}">
        <p class="model-code">{code}</p><h3 class="h3">{name}</h3><p>{desc}</p>
        <p class="model-todo">{todo(t)}</p></article>''' for i, (code, name, desc, t) in enumerate(MODELS))
    return f'''
<section class="sec" id="modelos">
  <div class="wrap">
    {head(v, "01", "Modelos", "Modelos CPA y FTD", "Campañas orientadas a resultados medibles, no a impresiones.")}
    <div class="models-grid">{cards}</div>
  </div>
</section>'''

def services(v):
    cards = "".join(f'''<article class="card svc hoverable" data-reveal style="--i:{i}">
        <span class="svc-ico">{ico(icon)}</span><span class="svc-n">0{i+1}</span>
        <h3 class="h3">{t}</h3><p>{d}</p></article>''' for i, (icon, t, d) in enumerate(SERVICES))
    return f'''
<section class="sec" id="servicios">
  <div class="wrap">
    {head(v, "02", "Servicios", "Nuestros servicios de performance", "Cada campaña está diseñada para generar resultados medibles en los mercados más competitivos de LATAM.")}
    <div class="svc-grid">{cards}</div>
  </div>
</section>'''

def method(v):
    steps = "".join(f'''<li class="step" data-reveal style="--i:{i}"><span class="step-n">{i+1:02d}</span><div><h3 class="h3">{t}</h3><p>{d}</p></div></li>''' for i, (t, d) in enumerate(METHOD))
    return f'''
<section class="sec" id="metodologia">
  <div class="wrap">
    {head(v, "03", "Metodología", "Cómo trabajamos", "De la definición del objetivo al reporte verificado.")}
    <ol class="steps">{steps}</ol>
    <p class="note" data-reveal>{todo("plazos de cada etapa y frecuencia de los reportes")}</p>
  </div>
</section>'''

def creator_card(c, i):
    name, plat, country, flag, tag, metric, link, img = c
    return f'''<a class="card creator" href="{link}" target="_blank" rel="noopener" data-reveal style="--i:{i}">
      <div class="creator-media"><span class="creator-ph" aria-hidden="true">{initials(name)}</span>
        <img src="{img}" alt="{E(name)}" loading="lazy" decoding="async" onerror="this.remove()"></div>
      <div class="creator-body">
        <div class="creator-top"><h3 class="h3">{E(name)}</h3><span class="badge">{plat}</span></div>
        <p class="dim">{flag} {country} · {tag}</p>
        <p class="metric">{metric}</p>
      </div></a>'''

def creators(v):
    cards = "".join(creator_card(c, i) for i, c in enumerate(CREATORS))
    return f'''
<section class="sec" id="creadores">
  <div class="wrap">
    {head(v, "04", "Talentos", "Creadores destacados", "Creadores exclusivos con audiencias verificadas y alto rendimiento en conversión.")}
    <div class="creators-grid">{cards}</div>
  </div>
</section>'''

def geos(v):
    tabs = "".join(f'<button class="geo-tab" role="tab" id="tab-{g["key"]}" aria-controls="geo-panel" aria-selected="{"true" if i == 0 else "false"}" tabindex="{0 if i == 0 else -1}" data-geo="{g["key"]}"><span aria-hidden="true">{g["flag"]}</span> {g["title"]}</button>' for i, g in enumerate(GEOS))
    return f'''
<section class="sec" id="geos">
  <div class="wrap">
    {head(v, "05", "Nuestra red", "Dominio geolocalizado", "Audiencias reales y verificadas en los mercados con mayor crecimiento de la región.")}
    <div class="geo-tabs" role="tablist" aria-label="Mercados" data-reveal>{tabs}</div>
    <div class="geo-panel" id="geo-panel" role="tabpanel" aria-labelledby="tab-chile" aria-live="polite"></div>
  </div>
</section>'''

def contact(v):
    return f'''
<section class="sec cta" id="contacto">
  <div class="wrap">
    <div class="cta-box card" data-reveal>
      <h2 class="h2">¿Listo para escalar tu marca en LATAM?</h2>
      <p class="lead">Déjanos tus requerimientos o agenda una sesión rápida con nuestro equipo de managers.</p>
      <div class="ctas">
        <a class="btn btn-primary" href="{TELEGRAM}" target="_blank" rel="noopener">{ico("send")} Contactar por Telegram</a>
        <a class="btn btn-ghost" href="{WHATSAPP}" target="_blank" rel="noopener">{ico("chat")} WhatsApp directo</a>
        <a class="btn btn-ghost" href="mailto:{EMAIL}">{ico("mail")} Enviar correo</a>
        <a class="btn btn-ghost" href="{CALENDLY}" target="_blank" rel="noopener">{ico("cal")} Agendar llamada</a>
      </div>
    </div>
  </div>
</section>'''

def form(v):
    return f'''
<section class="sec" id="postular">
  <div class="wrap form-wrap">
    {head(v, "06", "Creadores", "Postular a la red", "¿Eres creador o streamer? Envíanos tu canal y te contactamos.")}
    <form class="card form" id="apply-form" action="mailto:{EMAIL}" method="post" enctype="text/plain" data-reveal novalidate>
      <div class="field"><label for="f-nombre">Nombre / nickname</label><input id="f-nombre" name="nombre" type="text" autocomplete="nickname" required></div>
      <div class="field"><label for="f-canal">Link a tu canal principal</label><input id="f-canal" name="canal" type="url" inputmode="url" placeholder="https://" required></div>
      <label class="check"><input type="checkbox" name="mayor" required> Confirmo que soy mayor de 18 años.</label>
      <p class="form-msg" id="form-msg" role="status"></p>
      <button class="btn btn-primary btn-block" type="submit">Enviar postulación {ico("arrow")}</button>
      <p class="fine">Se abrirá tu app de correo con los datos listos para enviar a {EMAIL}.</p>
    </form>
  </div>
</section>'''

def footer(v):
    links = "".join(f'<a href="{h}" target="_blank" rel="noopener">{t}</a>' for t, h in LEGAL)
    return f'''
<footer class="footer">
  <div class="wrap">
    <div class="foot-top">
      {brand_html()}
      <nav class="foot-links" aria-label="Legal">{links}</nav>
    </div>
    <div class="foot-rg">
      <span class="age" aria-label="Solo mayores de 18 años">+18</span>
      <p>Contenido dirigido exclusivamente a mayores de 18 años. El juego puede generar adicción: juega con responsabilidad, fija límites de tiempo y dinero y busca ayuda si lo necesitas. {todo("línea de ayuda de juego responsable por país")}</p>
    </div>
    <p class="copy">© 2026 LTM Partners.</p>
  </div>
</footer>'''

# ───────────────────────── CSS ─────────────────────────
BASE_CSS = r"""
*,*::before,*::after{box-sizing:border-box}
html{-webkit-text-size-adjust:100%;scroll-behavior:smooth;scroll-padding-top:80px}
body{margin:0;background:var(--bg);color:var(--text);font-family:var(--font-body);font-size:16px;line-height:1.6;-webkit-font-smoothing:antialiased;overflow-x:hidden}
img{max-width:100%;display:block}
a{color:inherit;text-decoration:none}
h1,h2,h3,p,ol,ul{margin:0}
ul,ol{padding:0;list-style:none}
button{font:inherit;color:inherit}
.wrap{width:100%;max-width:1200px;margin:0 auto;padding:0 16px}
@media(min-width:768px){.wrap{padding:0 40px}}
.ico{width:18px;height:18px;flex:none}
.dim{color:var(--muted)}
.acc{color:var(--accent)}
.skip{position:absolute;left:12px;top:-80px;z-index:100;background:var(--accent);color:var(--accent-ink);padding:10px 14px;border-radius:8px}
.skip:focus{top:12px}
:focus-visible{outline:2px solid var(--accent);outline-offset:3px}
.todo{display:inline-block;font-family:var(--font-mono,monospace);font-size:.78em;letter-spacing:0;color:var(--text);border:1px dashed var(--accent);border-radius:4px;padding:1px 6px;background:color-mix(in srgb,var(--accent) 10%,transparent)}

/* NAV */
.nav{position:fixed;inset:0 0 auto;z-index:50;height:64px}
.nav::before{content:"";position:absolute;inset:0;background:var(--nav-bg);border-bottom:1px solid var(--line);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px);opacity:0;transition:opacity .3s cubic-bezier(.22,1,.36,1)}
.nav.scrolled::before{opacity:1}
.nav-in{position:relative;height:100%;display:flex;align-items:center;justify-content:space-between;gap:24px}
.brand{display:inline-flex;align-items:center;gap:10px;color:var(--text)}
.logo-mark{width:26px;height:26px;color:var(--accent)}
.brand-txt{font-size:1.05rem;letter-spacing:.06em;font-weight:300}
.brand-txt b{font-weight:800}
.nav-links{display:none;gap:28px}
.nav-link{font-size:.9rem;color:var(--muted);position:relative;padding:6px 0;transition:color .15s ease-out}
.nav-link::after{content:"";position:absolute;left:0;right:0;bottom:0;height:1px;background:var(--accent);transform:scaleX(0);transform-origin:left;transition:transform .25s cubic-bezier(.22,1,.36,1)}
.nav-link:hover{color:var(--text)}
.nav-link:hover::after{transform:scaleX(1)}
.nav-cta{display:none;gap:10px}
.menu-btn{display:inline-flex;background:none;border:1px solid var(--line);border-radius:8px;padding:8px;cursor:pointer}
.menu-btn .ico{width:20px;height:20px}
@media(min-width:960px){.nav-links,.nav-cta{display:flex}.menu-btn{display:none}}
.menu{position:fixed;inset:0;z-index:60;background:var(--bg);display:flex;flex-direction:column;justify-content:center;gap:14px;padding:24px;opacity:0;transform:translateY(-8px);transition:opacity .25s cubic-bezier(.22,1,.36,1),transform .25s cubic-bezier(.22,1,.36,1)}
.menu.open{opacity:1;transform:none}
.menu[hidden]{display:none}
.menu nav{display:flex;flex-direction:column;margin-bottom:16px}
.menu nav a{font-size:1.6rem;padding:10px 0;border-bottom:1px solid var(--line)}
.menu-close{position:absolute;top:14px;right:16px;background:none;border:1px solid var(--line);border-radius:8px;padding:8px;cursor:pointer}

/* BOTONES: el hover anima solo transform y opacity */
.btn{position:relative;display:inline-flex;align-items:center;justify-content:center;gap:8px;min-height:46px;padding:0 20px;border-radius:var(--radius-btn);font-weight:600;font-size:.94rem;line-height:1;white-space:nowrap;cursor:pointer;border:1px solid transparent;transition:transform .2s cubic-bezier(.22,1,.36,1);isolation:isolate}
.btn::after{content:"";position:absolute;inset:-1px;border-radius:inherit;z-index:-1;opacity:0;transition:opacity .2s ease-out}
.btn:hover{transform:translateY(-1px)}
.btn:hover::after{opacity:1}
.btn:active{transform:translateY(0) scale(.98)}
.btn .ico{transition:transform .2s cubic-bezier(.22,1,.36,1)}
.btn:hover .ico:last-child{transform:translateX(2px)}
.btn-sm{min-height:38px;padding:0 14px;font-size:.86rem}
.btn-block{width:100%}
.btn-primary{background:var(--accent);color:var(--accent-ink)}
.btn-primary::after{background:rgba(255,255,255,.14)}
.btn-ghost{border-color:var(--line2);color:var(--text)}
.btn-ghost::after{background:rgba(255,255,255,.05)}
.ctas{display:flex;flex-wrap:wrap;gap:12px}

/* CARDS: realce de hover con pseudo-elemento (opacity) */
.card{position:relative;background:var(--surface);border:1px solid var(--line);border-radius:var(--radius);isolation:isolate}
.card::after{content:"";position:absolute;inset:-1px;border-radius:inherit;border:1px solid var(--accent);opacity:0;pointer-events:none;transition:opacity .25s ease-out}
a.card:hover::after,.card.hoverable:hover::after{opacity:.6}
a.card{transition:transform .25s cubic-bezier(.22,1,.36,1)}
a.card:hover{transform:translateY(-3px)}

/* REVEAL */
.js [data-reveal]{opacity:0;transform:translateY(14px);transition:opacity .4s cubic-bezier(.22,1,.36,1),transform .4s cubic-bezier(.22,1,.36,1);transition-delay:calc(var(--i,0) * 70ms)}
.js [data-reveal].in{opacity:1;transform:none}
.count{font-variant-numeric:tabular-nums}

/* MARQUEE */
.brands{padding:40px 0;border-top:1px solid var(--line);border-bottom:1px solid var(--line)}
.brands-title{text-align:center;font-size:.75rem;letter-spacing:.2em;text-transform:uppercase;color:var(--muted);margin-bottom:24px}
.marquee{overflow:hidden;-webkit-mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent);mask-image:linear-gradient(90deg,transparent,#000 12%,#000 88%,transparent)}
.marquee-track{display:flex;width:max-content;animation:mq 38s linear infinite;will-change:transform}
.marquee:hover .marquee-track{animation-play-state:paused}
.marquee-set{display:flex;align-items:center;gap:56px;padding-right:56px}
.brand-logo{height:34px;width:auto;max-width:130px;object-fit:contain;opacity:.42;filter:grayscale(1);transition:opacity .2s ease-out}
.brand-logo:hover{opacity:1;filter:none}
.brand-name{font-weight:600;font-size:1.05rem;letter-spacing:.02em;color:var(--muted);white-space:nowrap}
@keyframes mq{to{transform:translate3d(-50%,0,0)}}

/* SECCIONES */
.sec{padding:88px 0}
@media(min-width:768px){.sec{padding:120px 0}}
.lead{color:var(--muted);font-size:1.05rem;max-width:56ch}
.h3{font-size:1.08rem;font-weight:600;line-height:1.3}
.sec-head{margin-bottom:44px}

.models-grid{display:grid;gap:16px}
@media(min-width:768px){.models-grid{grid-template-columns:1fr 1fr}}
.model{padding:28px}
.model-code{font-family:var(--font-mono,var(--font-body));font-size:2.4rem;font-weight:600;color:var(--accent);line-height:1;margin-bottom:16px}
.model p{color:var(--muted)}
.model .h3{margin-bottom:8px;color:var(--text)}
.model-todo{margin-top:16px}

.svc-grid{display:grid;gap:16px}
@media(min-width:768px){.svc-grid{grid-template-columns:1fr 1fr}}
.svc{padding:28px}
.svc-ico{display:inline-flex;width:40px;height:40px;align-items:center;justify-content:center;border:1px solid var(--line2);border-radius:10px;color:var(--accent);margin-bottom:20px}
.svc-n{position:absolute;top:24px;right:24px;font-family:var(--font-mono,var(--font-body));font-size:.78rem;color:var(--muted)}
.svc .h3{margin-bottom:8px}
.svc p{color:var(--muted);font-size:.95rem}

.steps{display:grid;gap:0;border-top:1px solid var(--line);counter-reset:s}
@media(min-width:900px){.steps{grid-template-columns:repeat(4,1fr);border-top:0}}
.step{display:flex;gap:16px;padding:24px 0;border-bottom:1px solid var(--line)}
@media(min-width:900px){.step{flex-direction:column;padding:24px 24px 24px 0;border-bottom:0;border-top:1px solid var(--line)}}
.step-n{font-family:var(--font-mono,var(--font-body));color:var(--accent);font-size:.85rem;min-width:28px;padding-top:2px}
.step p{color:var(--muted);font-size:.95rem;margin-top:6px}
.note{margin-top:24px;color:var(--muted);font-size:.9rem}

.creators-grid{display:grid;grid-auto-flow:column;grid-auto-columns:min(78%,280px);gap:16px;overflow-x:auto;scroll-snap-type:x mandatory;padding-bottom:12px;scrollbar-width:thin}
.creators-grid > *{scroll-snap-align:start}
@media(min-width:960px){.creators-grid{grid-auto-flow:row;grid-template-columns:repeat(4,1fr);overflow:visible}}
.creator{display:flex;flex-direction:column;overflow:hidden}
.creator-media{position:relative;aspect-ratio:4/5;background:var(--surface2);overflow:hidden;border-radius:calc(var(--radius) - 1px) calc(var(--radius) - 1px) 0 0}
.creator-media img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover;opacity:.9;transition:transform .4s cubic-bezier(.22,1,.36,1),opacity .4s ease-out}
.creator:hover .creator-media img{transform:scale(1.04);opacity:1}
.creator-ph{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font-size:2.4rem;font-weight:600;color:var(--muted);letter-spacing:.04em}
.creator-body{padding:18px}
.creator-top{display:flex;align-items:center;justify-content:space-between;gap:8px;margin-bottom:4px}
.badge{font-size:.72rem;padding:3px 8px;border:1px solid var(--line2);border-radius:999px;color:var(--muted);white-space:nowrap}
.creator .dim{font-size:.88rem}
.metric{margin-top:10px;font-weight:600;color:var(--accent);font-size:.9rem}

/* GEOS */
.geo-tabs{display:flex;gap:8px;overflow-x:auto;padding-bottom:8px;margin-bottom:28px;scrollbar-width:none}
.geo-tabs::-webkit-scrollbar{display:none}
@media(min-width:768px){.geo-tabs{flex-wrap:wrap}}
.geo-tab{position:relative;flex:none;display:inline-flex;align-items:center;gap:6px;padding:9px 16px;border-radius:999px;background:transparent;border:1px solid var(--line2);color:var(--muted);cursor:pointer;font-size:.9rem;transition:transform .2s cubic-bezier(.22,1,.36,1)}
.geo-tab:hover{color:var(--text);transform:translateY(-1px)}
.geo-tab[aria-selected="true"]{color:var(--accent-ink);background:var(--accent);border-color:var(--accent)}
.geo-panel{transition:opacity .2s ease-out,transform .2s ease-out}
.geo-panel.out{opacity:0;transform:translateY(6px)}
.geo-head{display:flex;flex-wrap:wrap;align-items:flex-end;justify-content:space-between;gap:12px;padding-bottom:20px;border-bottom:1px solid var(--line);margin-bottom:20px}
.geo-title{font-size:1.8rem;font-weight:600;line-height:1.1}
.geo-tier{font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:var(--accent)}
.geo-tagline{margin-top:6px}
.geo-desc{color:var(--muted);font-size:.95rem}
.geo-stats{display:grid;grid-template-columns:1fr 1fr;gap:12px;margin-bottom:24px}
@media(min-width:900px){.geo-stats{grid-template-columns:repeat(4,1fr)}}
.geo-stat{padding:18px}
.geo-stat p:first-child{font-size:.74rem;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);margin-bottom:6px}
.geo-stat p:last-child{font-size:1.5rem;font-weight:600;font-variant-numeric:tabular-nums}
.geo-creators-title{font-size:.78rem;letter-spacing:.12em;text-transform:uppercase;color:var(--muted);margin-bottom:12px}
.geo-creators{display:grid;gap:10px}
@media(min-width:768px){.geo-creators{grid-template-columns:repeat(auto-fill,minmax(300px,1fr))}}
.mini{display:flex;align-items:center;gap:14px;padding:14px}
.mini-av{position:relative;width:44px;height:44px;border-radius:50%;background:var(--surface2);overflow:hidden;flex:none;display:flex;align-items:center;justify-content:center;font-size:.85rem;color:var(--muted);font-weight:600}
.mini-av img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.mini-main{flex:1;min-width:0}
.mini-main b{display:block;font-weight:600}
.mini-main span{font-size:.85rem;color:var(--muted)}
.mini-side{text-align:right;font-size:.82rem}
.mini-side .metric{margin-top:4px;font-size:.82rem}

/* CTA + FORM */
.cta-box{padding:40px 24px;text-align:center}
@media(min-width:768px){.cta-box{padding:64px}}
.cta-box .lead{margin:16px auto 32px}
.cta-box .ctas{justify-content:center}
.form-wrap{display:grid;gap:8px}
@media(min-width:900px){.form-wrap{grid-template-columns:1fr 1fr;gap:64px;align-items:start}}
.form{padding:28px;display:grid;gap:18px}
.field label{display:block;font-size:.82rem;color:var(--muted);margin-bottom:6px}
.field input{width:100%;min-height:46px;padding:10px 14px;background:var(--bg);color:var(--text);border:1px solid var(--line2);border-radius:var(--radius-btn);font:inherit;font-size:16px}
.field input:focus{outline:none;border-color:var(--accent);box-shadow:0 0 0 3px color-mix(in srgb,var(--accent) 25%,transparent)}
.field input[aria-invalid="true"]{border-color:#e5484d}
.check{display:flex;gap:10px;align-items:flex-start;font-size:.9rem;color:var(--muted)}
.check input{margin-top:4px;accent-color:var(--accent);width:16px;height:16px}
.form-msg{font-size:.88rem;color:#ff8a8a;min-height:0}
.form-msg:empty{display:none}
.fine{font-size:.8rem;color:var(--muted)}

/* FOOTER */
.footer{border-top:1px solid var(--line);padding:48px 0 32px}
.foot-top{display:flex;flex-direction:column;gap:20px;padding-bottom:28px;border-bottom:1px solid var(--line)}
@media(min-width:768px){.foot-top{flex-direction:row;align-items:center;justify-content:space-between}}
.foot-links{display:flex;flex-wrap:wrap;gap:12px 22px;font-size:.88rem;color:var(--muted)}
.foot-links a{transition:color .15s ease-out}
.foot-links a:hover{color:var(--text)}
.foot-rg{display:flex;gap:16px;align-items:flex-start;padding:24px 0;font-size:.86rem;color:var(--muted);max-width:820px}
.age{flex:none;display:inline-flex;align-items:center;justify-content:center;width:44px;height:44px;border-radius:50%;border:1.5px solid var(--text);color:var(--text);font-weight:700;font-size:.9rem}
.copy{font-size:.82rem;color:var(--muted)}

@media (prefers-reduced-motion:reduce){
  *,*::before,*::after{transition-duration:.01ms!important;animation-duration:.01ms!important;transition-delay:0s!important}
  .js [data-reveal]{opacity:1;transform:none}
  .marquee-track{animation:none;width:auto;flex-wrap:wrap;justify-content:center}
  .marquee{-webkit-mask-image:none;mask-image:none}
  .marquee-set{flex-wrap:wrap;justify-content:center;gap:28px 40px;padding:0 16px}
  .marquee-set[aria-hidden]{display:none}
}
"""

CSS_A = r"""
:root{--bg:#07090A;--surface:#0C0F10;--surface2:#121617;--line:#1B2122;--line2:#273032;--text:#E6ECEA;--muted:#83908D;--accent:#5FE3B1;--accent-ink:#04120C;--nav-bg:rgba(7,9,10,.88);--radius:4px;--radius-btn:4px;
--font-body:"Inter",system-ui,sans-serif;--font-mono:"IBM Plex Mono",ui-monospace,monospace}
.eyebrow,.brands-title,.badge,.geo-tier,.geo-stat p:first-child,.geo-creators-title,.panel,.svc-n,.fine,.btn,.nav-link,.copy{font-family:var(--font-mono)}
.btn{font-weight:500;letter-spacing:.01em;font-size:.86rem}
.eyebrow{font-size:.78rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:18px}
.h1{font-size:clamp(2.1rem,5.4vw,3.6rem);font-weight:600;letter-spacing:-.03em;line-height:1.05;margin-bottom:22px}
.h2{font-size:clamp(1.7rem,3.6vw,2.6rem);font-weight:600;letter-spacing:-.025em;line-height:1.1;margin-bottom:14px}
.hero{padding:128px 0 72px}
.hero-grid{display:grid;gap:48px;align-items:center}
@media(min-width:960px){.hero-grid{grid-template-columns:1.2fr .8fr}.hero{padding:168px 0 104px}}
.hero .lead{margin-bottom:32px}
.panel{border:1px solid var(--line2);background:var(--surface);font-size:.86rem}
.panel-head{display:flex;justify-content:space-between;padding:12px 16px;border-bottom:1px solid var(--line2);font-size:.74rem;letter-spacing:.12em}
.market-list li{display:grid;grid-template-columns:10px 1fr auto;gap:12px;align-items:center;padding:11px 16px;border-bottom:1px solid var(--line)}
.market-list li:last-child{border-bottom:0}
.market-list .mono{font-size:.74rem}
.dot{width:6px;height:6px;border-radius:50%;background:var(--accent);box-shadow:0 0 0 3px rgba(95,227,177,.12)}
.stats{border-bottom:1px solid var(--line)}
.stats-grid{display:grid;grid-template-columns:1fr 1fr;padding:0}
@media(min-width:768px){.stats-grid{grid-template-columns:repeat(4,1fr)}}
.stat{padding:32px 16px;border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.stat:nth-child(2n){border-right:0}
@media(min-width:768px){.stat{border-bottom:0;padding:44px 24px}.stat:nth-child(2n){border-right:1px solid var(--line)}.stat:last-child{border-right:0}}
.stat .count{display:block;font-family:var(--font-mono);font-size:clamp(1.9rem,4vw,2.9rem);font-weight:500;letter-spacing:-.02em;color:var(--text)}
.stat .count.static{font-size:clamp(1.3rem,2.6vw,1.9rem);padding-top:.35em}
.stat p{font-family:var(--font-mono);font-size:.74rem;text-transform:uppercase;letter-spacing:.12em;color:var(--muted);margin-top:8px}
.count.ticking{color:var(--accent)}
.svc-grid,.models-grid{gap:0;border:1px solid var(--line);}
.svc,.model{border:0;border-radius:0;border-bottom:1px solid var(--line)}
@media(min-width:768px){.svc:nth-child(odd),.model:nth-child(odd){border-right:1px solid var(--line)}.svc:nth-last-child(-n+2),.model{border-bottom:0}}
.svc:last-child{border-bottom:0}
.card.svc::after,.card.model::after{inset:0;border-radius:0}
.svc.hoverable:hover::after,.model.hoverable:hover::after{opacity:.5}
.svc-ico{border-radius:4px}
.model-code{font-weight:500}
.geo-tab{border-radius:4px;font-family:var(--font-mono);font-size:.82rem}
.geo-stats{gap:0;border:1px solid var(--line)}
.geo-stat{border:0;border-radius:0;border-right:1px solid var(--line);border-bottom:1px solid var(--line)}
.geo-stat:nth-child(2n){border-right:0}
@media(min-width:900px){.geo-stat{border-bottom:0}.geo-stat:nth-child(2n){border-right:1px solid var(--line)}.geo-stat:last-child{border-right:0}}
.geo-stat p:last-child{font-family:var(--font-mono);font-weight:500}
.geo-title{font-weight:600;letter-spacing:-.02em}
.creator-media{border-radius:3px 3px 0 0}
.metric{font-family:var(--font-mono);font-weight:500}
.cta-box{text-align:left}
.cta-box .lead{margin:16px 0 32px}
.cta-box .ctas{justify-content:flex-start}
"""

CSS_B = r"""
:root{--bg:#0B0A09;--surface:#121110;--surface2:#1A1816;--line:#232120;--line2:#34312E;--text:#EFEBE4;--muted:#958F86;--accent:#D9B65A;--accent-ink:#141006;--nav-bg:rgba(11,10,9,.88);--radius:2px;--radius-btn:999px;
--font-body:"Inter",system-ui,sans-serif;--font-display:"Instrument Serif",Georgia,serif;--font-mono:"Inter",system-ui,sans-serif}
.display,.h2,.geo-title,.model-code,.step-n,.stat .count,.cta-box .h2{font-family:var(--font-display);font-weight:400}
.eyebrow{font-size:.74rem;letter-spacing:.22em;text-transform:uppercase;color:var(--muted)}
.hero{padding:136px 0 80px;border-bottom:1px solid var(--line)}
@media(min-width:960px){.hero{padding:176px 0 112px}}
.hero-eyebrow{margin-bottom:28px}
.hero-title{font-size:clamp(3rem,10.5vw,8.6rem);line-height:.95;letter-spacing:-.025em;margin-bottom:56px}
.hero-title .line{display:block;overflow:hidden;padding-bottom:.06em}
.hero-title .line>span{display:block;transform:translateY(105%);transition:transform .9s cubic-bezier(.22,1,.36,1)}
.hero-title .line:nth-child(2)>span{transition-delay:.09s}
.hero-title .line:nth-child(3)>span{transition-delay:.18s}
.no-js .hero-title .line>span,.hero-title.in .line>span{transform:none}
.hero-title em{font-style:italic;color:var(--accent)}
.hero-foot{display:grid;gap:32px;align-items:end}
@media(min-width:900px){.hero-foot{grid-template-columns:1fr 1fr;gap:64px}}
.hero-lead{font-size:1.12rem}
.hero-markets{margin-top:20px;font-size:.84rem;color:var(--muted);letter-spacing:.02em}
.h2{font-size:clamp(2.4rem,6vw,4.6rem);line-height:1;letter-spacing:-.02em;margin-bottom:18px}
.sec-head{display:grid;gap:18px;margin-bottom:56px;padding-top:28px;border-top:1px solid var(--line2)}
@media(min-width:900px){.sec-head{grid-template-columns:220px 1fr;gap:40px}}
.sec-meta{display:flex;gap:14px;align-items:baseline}
.num{font-family:var(--font-display);font-size:1.4rem;color:var(--accent)}
.stats-grid{display:grid;grid-template-columns:1fr 1fr;gap:40px 24px;padding:72px 16px}
@media(min-width:768px){.stats-grid{grid-template-columns:repeat(4,1fr);padding:96px 40px}}
.stat{border-left:1px solid var(--line2);padding-left:18px}
.stat .count{display:block;font-size:clamp(3rem,7vw,5.2rem);line-height:1;letter-spacing:-.02em}
.stat .count.static{font-size:clamp(2rem,4.2vw,3.2rem);padding-top:.3em}
.stat p{color:var(--muted);font-size:.86rem;margin-top:10px}
.stats{border-bottom:1px solid var(--line)}
.card{background:transparent}
.svc-grid,.models-grid{gap:0}
.svc,.model{border:0;border-top:1px solid var(--line);padding:32px 0}
@media(min-width:768px){.svc:nth-child(odd),.model:nth-child(odd){padding-right:40px}.svc:nth-child(even),.model:nth-child(even){padding-left:40px;border-left:1px solid var(--line)}}
.card.svc::after,.card.model::after{display:none}
.svc-ico{display:none}
.svc-n{position:static;display:block;font-family:var(--font-display);font-size:1.3rem;color:var(--accent);margin-bottom:14px}
.svc .h3,.model .h3,.step .h3{font-family:var(--font-display);font-weight:400;font-size:1.9rem;line-height:1.1;letter-spacing:-.01em}
.svc p{font-size:1rem;max-width:44ch}
.model-code{font-size:4.4rem}
.step-n{font-size:1.6rem}
.creator{border:0;background:transparent}
.creator-media{border-radius:2px}
.creator-body{padding:16px 0 0}
.creator .h3{font-family:var(--font-display);font-weight:400;font-size:1.7rem}
.card.creator::after{display:none}
.creator:hover .h3{color:var(--accent)}
.creator .h3{transition:color .15s ease-out}
.geo-tab{font-size:.9rem}
.geo-title{font-size:clamp(2.6rem,6vw,4rem);line-height:1}
.geo-stat{background:transparent;border:0;border-left:1px solid var(--line2);border-radius:0;padding:4px 0 4px 18px}
.geo-stat p:last-child{font-family:var(--font-display);font-weight:400;font-size:2.4rem;line-height:1.1}
.geo-stats{gap:28px 20px;margin-bottom:40px}
.mini{background:transparent;border-left:0;border-right:0;border-radius:0}
.cta-box{border:0;border-top:1px solid var(--line2);border-bottom:1px solid var(--line2);background:transparent;padding:72px 0}
.cta-box .h2{font-size:clamp(2.6rem,7vw,5.4rem)}
.cta-box::after{display:none}
.form{background:var(--surface);border-radius:4px}
"""

CSS_C = r"""
:root{--bg:#060708;--surface:#0D0E10;--surface2:#15171A;--line:#1C1F23;--line2:#2A2E34;--text:#ECEEF1;--muted:#8A9099;--accent:#4C8DFF;--accent-ink:#030814;--nav-bg:rgba(6,7,8,.86);--radius:14px;--radius-btn:10px;
--font-body:"Manrope",system-ui,sans-serif;--font-mono:"Manrope",system-ui,sans-serif}
.eyebrow{font-size:.76rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);margin-bottom:14px;font-weight:600}
.h1{font-size:clamp(2rem,4.8vw,3.5rem);font-weight:700;letter-spacing:-.035em;line-height:1.04;margin-bottom:20px}
.h2{font-size:clamp(1.7rem,3.6vw,2.6rem);font-weight:700;letter-spacing:-.03em;line-height:1.1;margin-bottom:12px}
.h3{font-weight:700;letter-spacing:-.01em}
.hero{padding:96px 0 40px}
@media(min-width:960px){.hero{padding:112px 0 64px}}
.bento{display:grid;gap:12px;grid-template-columns:1fr 1fr}
.tile{padding:22px}
.tile-hero{grid-column:1/-1;padding:28px 22px}
.tile-hero .lead{margin-bottom:28px}
.tile-stat{display:flex;flex-direction:column;justify-content:space-between;min-height:132px}
.tile-stat .count{font-size:clamp(2rem,4vw,3rem);font-weight:700;letter-spacing:-.03em;line-height:1}
.tile-stat .count.static{font-size:clamp(1.4rem,2.6vw,2rem)}
.tile-stat p,.tile-label{color:var(--muted);font-size:.86rem;margin-top:10px}
.tile-label{margin:0 0 14px}
.tile-markets{grid-column:1/-1}
.chips{display:flex;flex-wrap:wrap;gap:8px}
.chips li{font-size:.86rem;padding:6px 12px;border:1px solid var(--line2);border-radius:999px}
@media(min-width:960px){
  .hero-bento{grid-template-columns:repeat(12,1fr);grid-auto-rows:minmax(150px,auto)}
  .tile-hero{grid-column:1/span 8;grid-row:1/span 3;padding:48px;display:flex;flex-direction:column;justify-content:flex-end}
  .tile-stat{grid-column:span 2}
  .hero-bento .tile-stat:nth-of-type(2){grid-column:9/span 4}
  .hero-bento .tile-stat:nth-of-type(3){grid-column:9/span 2}
  .hero-bento .tile-stat:nth-of-type(4){grid-column:11/span 2}
  .tile-models{grid-column:9/span 4!important}
  .tile-markets{grid-column:1/-1}
}
/* resplandor que sigue al cursor (solo punteros finos) */
.card::before{content:"";position:absolute;inset:0;border-radius:inherit;z-index:-1;pointer-events:none;opacity:0;transition:opacity .3s ease-out;background:radial-gradient(420px circle at var(--mx,50%) var(--my,50%),rgba(76,141,255,.10),transparent 45%)}
@media (hover:hover) and (pointer:fine){.card:hover::before{opacity:1}.card:hover::after{opacity:.35}}
.card::after{mask:radial-gradient(300px circle at var(--mx,50%) var(--my,50%),#000,transparent 70%);-webkit-mask:radial-gradient(300px circle at var(--mx,50%) var(--my,50%),#000,transparent 70%)}
.stats{display:none}
@media(min-width:768px){
  .svc-grid{grid-template-columns:repeat(12,1fr)}
  .svc:nth-child(1),.svc:nth-child(4){grid-column:span 7}
  .svc:nth-child(2),.svc:nth-child(3){grid-column:span 5}
  .svc{min-height:220px;display:flex;flex-direction:column;justify-content:flex-end}
}
.svc-ico{position:absolute;top:24px;left:28px;margin:0;border-radius:10px}
.svc{padding-top:92px}
@media(min-width:960px){
  .creators-grid{grid-template-columns:repeat(12,1fr);grid-auto-rows:auto}
  .creator:nth-child(1){grid-column:span 6;grid-row:span 2}
  .creator:nth-child(2),.creator:nth-child(3){grid-column:span 3}
  .creator:nth-child(4){grid-column:7/span 6;flex-direction:row}
  .creator:nth-child(4) .creator-media{aspect-ratio:auto;width:42%;min-height:260px;border-radius:13px 0 0 13px}
  .creator:nth-child(4) .creator-body{align-self:flex-end}
  .creator:nth-child(1) .creator-media{aspect-ratio:auto;flex:1;min-height:420px}
}
.creator-media{border-radius:13px 13px 0 0}
.geo-tab[aria-selected="true"]{color:#fff;background:rgba(76,141,255,.16);border-color:var(--accent)}
.geo-stat p:last-child{font-weight:700;letter-spacing:-.02em}
.mini{border-radius:12px}
.cta-box{background:linear-gradient(180deg,var(--surface2),var(--surface))}
"""

FONTS = {
    "a": "family=IBM+Plex+Mono:wght@400;500&family=Inter:wght@400;500;600&display=swap",
    "b": "family=Instrument+Serif:ital@0;1&family=Inter:wght@400;500;600&display=swap",
    "c": "family=Manrope:wght@400;500;600;700&display=swap",
}
TITLES = {"a": "LTM Partners · Terminal", "b": "LTM Partners · Editorial", "c": "LTM Partners · Bento"}
CSS = {"a": CSS_A, "b": CSS_B, "c": CSS_C}
THEME = {"a": "#07090A", "b": "#0B0A09", "c": "#060708"}

# ───────────────────────── JS (compartido) ─────────────────────────
JS = r"""
(function(){
  var root=document.documentElement; root.classList.remove('no-js'); root.classList.add('js');
  var reduce=window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var hasIO='IntersectionObserver' in window;

  /* NAV */
  var nav=document.getElementById('nav');
  function onScroll(){nav.classList.toggle('scrolled',window.scrollY>12)}
  onScroll(); window.addEventListener('scroll',onScroll,{passive:true});

  /* MENÚ MÓVIL */
  var menu=document.getElementById('menu'),btn=document.getElementById('menu-btn'),closeB=document.getElementById('menu-close');
  function openMenu(){menu.hidden=false;requestAnimationFrame(function(){menu.classList.add('open')});btn.setAttribute('aria-expanded','true');document.body.style.overflow='hidden';closeB.focus()}
  function closeMenu(){menu.classList.remove('open');btn.setAttribute('aria-expanded','false');document.body.style.overflow='';setTimeout(function(){menu.hidden=true},reduce?0:250)}
  btn.addEventListener('click',openMenu); closeB.addEventListener('click',function(){closeMenu();btn.focus()});
  menu.addEventListener('click',function(e){if(e.target.closest('a'))closeMenu()});
  document.addEventListener('keydown',function(e){if(e.key==='Escape'&&!menu.hidden){closeMenu();btn.focus()}});

  /* REVEAL */
  var revealEls=[].slice.call(document.querySelectorAll('[data-reveal]'));
  if(reduce||!hasIO){revealEls.forEach(function(el){el.classList.add('in')})}
  else{
    var ro=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){e.target.classList.add('in');ro.unobserve(e.target)}})},{threshold:.12,rootMargin:'0px 0px -6% 0px'});
    revealEls.forEach(function(el){ro.observe(el)});
  }
  var heroTitle=document.querySelector('.hero-title');
  if(heroTitle){requestAnimationFrame(function(){requestAnimationFrame(function(){heroTitle.classList.add('in')})})}

  /* CONTADORES: el HTML ya trae el valor real; solo se anima si hay movimiento permitido */
  var counters=[].slice.call(document.querySelectorAll('.count[data-count]'));
  function fmt(el,v){return (el.dataset.prefix||'')+v+(el.dataset.suffix||'')}
  function run(el){
    var target=+el.dataset.count,dur=1100,t0=null;
    el.classList.add('ticking');
    function step(t){if(!t0)t0=t;var p=Math.min(1,(t-t0)/dur),e=1-Math.pow(1-p,3);el.textContent=fmt(el,Math.round(target*e));if(p<1)requestAnimationFrame(step);else{el.textContent=fmt(el,target);el.classList.remove('ticking')}}
    requestAnimationFrame(step);
  }
  if(!reduce&&hasIO){
    counters.forEach(function(el){el.textContent=fmt(el,0)});
    var co=new IntersectionObserver(function(es){es.forEach(function(e){if(e.isIntersecting){run(e.target);co.unobserve(e.target)}})},{threshold:.4});
    counters.forEach(function(el){co.observe(el)});
  }

  /* GEOS */
  var GEOS=__GEOS__;
  var panel=document.getElementById('geo-panel');
  var tabs=[].slice.call(document.querySelectorAll('.geo-tab'));
  function h(tag,cls,txt){var n=document.createElement(tag);if(cls)n.className=cls;if(txt!=null)n.textContent=txt;return n}
  function initials(s){var p=s.replace(/"/g,'').split(/\s+/).filter(Boolean);return ((p[0]||'')[0]+((p[1]||'')[0]||'')).toUpperCase()}
  function build(g){
    var f=document.createDocumentFragment();
    var head=h('div','geo-head'),l=h('div');
    l.appendChild(h('p','geo-tier',g.tier));
    var t=h('h3','geo-title',g.flag+' '+g.title);l.appendChild(t);
    l.appendChild(h('p','geo-tagline',g.tagline));
    head.appendChild(l);head.appendChild(h('p','geo-desc',g.description));f.appendChild(head);
    var st=h('div','geo-stats');
    g.stats.forEach(function(s){var c=h('div','card geo-stat');c.appendChild(h('p',null,s[0]));c.appendChild(h('p',null,s[1]));st.appendChild(c)});
    f.appendChild(st);
    f.appendChild(h('p','geo-creators-title','Creadores en '+g.title));
    var list=h('div','geo-creators');
    g.creators.forEach(function(c){
      var card=h(c.link?'a':'div','card mini');
      if(c.link){card.href=c.link;card.target='_blank';card.rel='noopener'}
      var av=h('span','mini-av',initials(c.name));
      if(c.img){var im=new Image();im.alt='';im.loading='lazy';im.onerror=function(){im.remove()};im.src=c.img;av.appendChild(im)}
      var main=h('span','mini-main');main.appendChild(h('b',null,c.name));main.appendChild(h('span',null,c.tag));
      var side=h('span','mini-side');side.appendChild(h('span','badge',c.platform));side.appendChild(h('p','metric',c.metric));
      card.appendChild(av);card.appendChild(main);card.appendChild(side);
      if(!c.link){var todo=h('span','todo','[COMPLETAR: enlace y foto]');todo.style.marginTop='6px';main.appendChild(todo)}
      list.appendChild(card);
    });
    f.appendChild(list);
    return f;
  }
  function show(key,focus){
    var g=GEOS.filter(function(x){return x.key===key})[0]||GEOS[0];
    tabs.forEach(function(b){var on=b.dataset.geo===g.key;b.setAttribute('aria-selected',on);b.tabIndex=on?0:-1;if(on&&focus)b.focus()});
    panel.setAttribute('aria-labelledby','tab-'+g.key);
    function swap(){panel.textContent='';panel.appendChild(build(g));bindGlow(panel);panel.classList.remove('out')}
    if(reduce||!panel.childNodes.length){swap()}else{panel.classList.add('out');setTimeout(swap,180)}
  }
  tabs.forEach(function(b,i){
    b.addEventListener('click',function(){show(b.dataset.geo)});
    b.addEventListener('keydown',function(e){
      var k=e.key,n=null;
      if(k==='ArrowRight')n=tabs[(i+1)%tabs.length];else if(k==='ArrowLeft')n=tabs[(i-1+tabs.length)%tabs.length];else if(k==='Home')n=tabs[0];else if(k==='End')n=tabs[tabs.length-1];
      if(n){e.preventDefault();show(n.dataset.geo,true)}
    });
  });

  /* RESPLANDOR QUE SIGUE AL CURSOR (variante C; inofensivo en las demás) */
  var fine=window.matchMedia('(hover:hover) and (pointer:fine)').matches;
  function bindGlow(scope){
    if(!fine||reduce||!document.body.classList.contains('v-c'))return;
    [].forEach.call(scope.querySelectorAll('.card'),function(c){
      var raf=0;
      c.addEventListener('pointermove',function(e){var r=c.getBoundingClientRect(),x=e.clientX-r.left,y=e.clientY-r.top;cancelAnimationFrame(raf);raf=requestAnimationFrame(function(){c.style.setProperty('--mx',x+'px');c.style.setProperty('--my',y+'px')})});
    });
  }
  bindGlow(document);
  show(GEOS[0].key);

  /* FORMULARIO: arma un correo con los datos (no hay backend) */
  var form=document.getElementById('apply-form'),msg=document.getElementById('form-msg');
  form.addEventListener('submit',function(e){
    e.preventDefault();
    var bad=[].filter.call(form.elements,function(el){if(!el.willValidate)return false;var ok=el.checkValidity();el.setAttribute('aria-invalid',ok?'false':'true');return !ok});
    if(bad.length){msg.textContent='Revisa los campos marcados: nombre, un enlace válido (https://…) y confirmar mayoría de edad.';bad[0].focus();return}
    msg.textContent='';
    var n=form.nombre.value.trim(),c=form.canal.value.trim();
    var body='Nombre / nickname: '+n+'\nCanal principal: '+c+'\nConfirmo que soy mayor de 18 años: sí';
    window.location.href='mailto:__EMAIL__?subject='+encodeURIComponent('Postulación a la red: '+n)+'&body='+encodeURIComponent(body);
  });
  [].forEach.call(form.querySelectorAll('input'),function(el){el.addEventListener('input',function(){if(el.getAttribute('aria-invalid')==='true'&&el.checkValidity())el.setAttribute('aria-invalid','false')})});
})();
"""

def page(v):
    js = JS.replace("__GEOS__", json.dumps(GEOS, ensure_ascii=False)).replace("__EMAIL__", EMAIL)
    body = "".join([nav(), '<main id="main">', hero(v), brands(v), stats(v), models(v), services(v), method(v),
                    creators(v), geos(v), contact(v), form(v), "</main>", footer(v)])
    return f'''<!DOCTYPE html>
<html lang="es" class="no-js">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{TITLES[v]}</title>
<meta name="description" content="LTM Partners conecta marcas de iGaming con creadores de LATAM. Campañas CPA y FTD con audiencias +18 verificadas.">
<meta name="theme-color" content="{THEME[v]}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?{FONTS[v]}">
<style>{BASE_CSS}{CSS[v]}</style>
</head>
<body class="v-{v}">
{body}
<script>{js}</script>
</body>
</html>
'''

os.makedirs(OUT, exist_ok=True)
for v in "abc":
    p = os.path.join(OUT, f"variante-{v}.html")
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(page(v))
    print(p, os.path.getsize(p))
