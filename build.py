"""Generates the static site. Run: python3 build.py"""
import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
GAL = json.loads((ROOT / "data/galleries.json").read_text(encoding="utf-8"))
ARROW = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>'
ARROW_UR = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M7 17L17 7M9 7h8v8"/></svg>'
DL = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 4v12M6 10l6 6 6-6M5 20h14"/></svg>'
MARK = '<svg class="mark" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linejoin="round"><path d="M5 29V14a11 11 0 0 1 22 0v15z"/><path d="M16 3.5V29M5 17h22"/><circle cx="19.5" cy="22" r=".9" fill="currentColor" stroke="none"/></svg>'
I = "assets/img/"
TEL1, TEL1_H = "+46707144001", "0707-14 40 01"
TEL2, TEL2_H = "+46520650301", "0520-65 03 01"
MAIL = "info@fvab.se"
HERO = I + "maps/maps-1.webp"

NAV = [("index.html", "Hem"), ("produkter.html", "Produkter"), ("galleri.html", "Galleri"),
       ("hustillverkning.html", "Hustillverkning"), ("info.html", "Om PVC"), ("dokument.html", "Dokument"),
       ("frakt.html", "Frakt"), ("kontakt.html", "Kontakt")]


def esc(s):
    return html.escape(s, quote=True)


def page(path, title, desc, body, active="", og=HERO):
    links = "".join(f'<li><a href="{h}"{" aria-current=page" if h == active else ""}>{t}</a></li>' for h, t in NAV[1:])
    logo = f'<a class="logo" href="index.html" aria-label="Fönsterfabriken i Väst – startsida">{MARK}<span>Fönsterfabriken<small>i Väst AB</small></span></a>'
    out = f"""<!doctype html>
<html lang="sv">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:image" content="{og}">
<meta property="og:locale" content="sv_SE">
<link rel="icon" href="favicon.ico">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,300;0,400;0,500;1,300&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
<header class="site-header">
  <nav class="nav" aria-label="Huvudmeny">
    {logo}
    <ul>{links}</ul>
    <a class="btn btn-primary" href="kontakt.html#offert">Begär offert {ARROW}</a>
    <button class="burger" aria-label="Meny" aria-expanded="false"><span></span><span></span></button>
  </nav>
</header>
<main>
{body}
</main>
<footer class="footer">
  <div class="wrap">
    <div class="footer-top">
      <div>
        {logo}
        <p class="muted" style="max-width:36ch">Svensktillverkade, underhållsfria och energibesparande PVC-fönster och dörrar. Tillverkning i Lödöse – lager och utställning i Lilla Edet.</p>
      </div>
      <div><h4>Produkter</h4><ul>{"".join(f'<li><a href="{p["slug"]}.html">{p["title"]}</a></li>' for p in PRODUCTS)}</ul></div>
      <div><h4>Sidor</h4><ul>{"".join(f'<li><a href="{h}">{t}</a></li>' for h, t in NAV[2:])}</ul></div>
      <div><h4>Kontakt</h4><ul><li><a href="tel:{TEL1}">{TEL1_H}</a></li><li><a href="tel:{TEL2}">{TEL2_H}</a></li><li><a href="mailto:{MAIL}">{MAIL}</a></li><li style="margin-top:8px">Göteborgsvägen 90<br>463 33 Lilla Edet</li></ul></div>
    </div>
    <div class="footer-bottom"><span>© Fönsterfabriken i Väst AB</span><span>PVC-fönster &amp; dörrar · Lilla Edet · Göteborg</span></div>
  </div>
</footer>
<div class="lb" role="dialog" aria-modal="true" aria-label="Bildvisning"><img src="" alt=""><button class="close" aria-label="Stäng">×</button><button class="nav-btn prev" aria-label="Föregående">‹</button><button class="nav-btn next" aria-label="Nästa">›</button><div class="cap"></div></div>
<script src="assets/js/main.js" defer></script>
</body>
</html>
"""
    (ROOT / path).write_text(out, encoding="utf-8")


def photos(items, alt, cat=None, cls="", limit=None):
    items = items[:limit] if limit else items
    c = f' data-cat="{cat}"' if cat else ""
    return "".join(f'<a href="{src}" data-lb{c}><img src="{src}" alt="{esc(alt)}" loading="lazy"></a>' for src in items)


def drawings(rows, folder, cls=""):
    out = "".join(f'<div class="drawing"><div class="pic"><img src="{I}ritningar/{folder}/{f}.webp" alt="{esc(t)}" loading="lazy"></div><div>{f"<b>{esc(k)}</b>" if k else ""}<span>{esc(t)}</span></div></div>'
                  for f, k, t in rows)
    return f'<div class="drawings {cls}">{out}</div>'


def doclinks(rows):
    return '<ul class="doclist">' + "".join(f'<li><a href="dokument/{f}.pdf" target="_blank" rel="noopener">{esc(t)}<span>PDF {DL}</span></a></li>' for t, f in rows) + "</ul>"


def page_hero(eyebrow, title, lead):
    return f'''<section class="page-hero"><div class="wrap">
  <span class="eyebrow">{eyebrow}</span>
  <h1>{title}</h1>
  <p class="lead">{lead}</p>
</div></section>'''


CTA = f'''<section class="cta reveal">
  <img src="{I}cta/skjutdorr-4k.webp" alt="" loading="lazy">
  <div class="wrap">
    <span class="eyebrow" style="color:#cfe1ea">Fönster &amp; dörrar efter mått</span>
    <h2>Berätta vad du planerar – vi tar fram en offert.</h2>
    <p>Allt tillverkas på beställning i vår fabrik i Lödöse. Välkommen att besöka utställningen i Lilla Edet, eller skicka en förfrågan direkt.</p>
    <div class="btns"><a class="btn btn-light" href="kontakt.html#offert">Begär offert {ARROW}</a><a class="btn btn-ghost" href="tel:{TEL1}">Ring {TEL1_H}</a></div>
  </div>
</section>'''

# ---------------------------------------------------------------- products
PRODUCTS = [
    dict(slug="fonster", title="Fönster", short="Energisnåla PVC-fönster med 2- eller 3-glas, dreh-kipp och specialformer.",
         cover=I + "galleri/fonster/fonster-412.webp", gal="fonster"),
    dict(slug="balkongdorrar", title="Balkong- & altandörrar", short="Inåt- och utåtgående dörrar, pardörrar och källardörrar.",
         cover=I + "galleri/dorrar/dorrar-413.webp", gal="dorrar"),
    dict(slug="skjutdorrar", title="Skjutdörrar", short="Upp till 8 m breda och 2,5 m höga – vår storsäljare.",
         cover=I + "galleri/skjutdorrar/skjutdorrar-1312.webp", gal="skjutdorrar"),
    dict(slug="kombinerade-dorrar", title="Kombinerade dörrar", short="Skjutdörr och svängdörr i samma parti – stor öppning.",
         cover=I + "galleri/kombi/kombidorrar-6.webp", gal="kombi"),
    dict(slug="takfonster", title="Takfönster", short="Tyska ROTO-takfönster, motsvarighet till Velux.",
         cover=I + "galleri/dorrar/dorrar-817.webp", gal=None),
    dict(slug="fasader", title="Underhållsfria fasader", short="Fasadpanel i vinyl som aldrig behöver målas.",
         cover=I + "galleri/fasad/fasad-812.webp", gal="fasad"),
    dict(slug="persienner", title="Persienner & rullgardiner", short="Persienner, rullgardiner och myggnät anpassade till fönstren.",
         cover=I + "galleri/persienner/rull-15.webp", gal="persienner"),
    dict(slug="tillval", title="Tillval", short="Glas, handtag och lås, spröjs och övriga tillbehör.",
         cover=I + "tillval/sprojs/1.webp", gal=None),
]
PBY = {p["slug"]: p for p in PRODUCTS}
SKIP = {"fonster": 6, "skjutdorrar": 3}  # leading product shots in the original galleries
GAL_LABEL = {"fonster": "Fönster", "skjutdorrar": "Skjutdörrar", "dorrar": "Balkong- & altandörrar", "kombi": "Kombinerade dörrar",
             "fasad": "Fasader", "persienner": "Persienner & rullgardiner", "garderober": "Garderober"}


def pcard(p, cls="reveal"):
    return f'''<a class="pcard {cls}" href="{p["slug"]}.html">
  <div class="img"><img src="{p["cover"]}" alt="{esc(p["title"])}" loading="lazy"></div>
  <div class="body"><h3>{p["title"]}<span class="arrow">{ARROW_UR}</span></h3><p>{p["short"]}</p></div>
</a>'''


def refs(key, title="Referenser", n=12):
    items = GAL[key][SKIP.get(key, 0):]
    return f'''<section style="padding-top:0"><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow">{title}</span><h2>Monterat hos våra kunder</h2></div>
  <a class="btn btn-ghost" href="galleri.html?kategori={key}">Se alla {len(GAL[key])} bilder {ARROW}</a></div>
  <div class="photos lg reveal" data-lb-group>{photos(items, GAL_LABEL[key], limit=n)}</div>
</div></section>'''


def product_page(slug, lead, intro_html, stats, specs, extra, eyebrow="Produkter", docs=None):
    p = PBY[slug]
    stat_html = "".join(f'<div class="stat"><b>{v}</b><span>{k}</span></div>' for v, k in stats)
    spec_html = "".join(f"<dt>{k}</dt><dd>{v}</dd>" for k, v in specs)
    doc_html = f'<h4 style="margin-top:24px;font-size:.75rem;letter-spacing:.14em;text-transform:uppercase;color:var(--muted);font-weight:500">Dokument</h4>{doclinks(docs)}' if docs else ""
    body = f'''<section class="page-hero"><div class="wrap split">
  <div><span class="eyebrow">{eyebrow}</span><h1>{p["title"]}</h1><p class="lead">{lead}</p>
  <div class="btns" style="display:flex;flex-wrap:wrap;gap:10px;margin-top:2rem"><a class="btn btn-primary" href="kontakt.html#offert">Begär offert {ARROW}</a>{f'<a class="btn btn-ghost" href="galleri.html?kategori={p["gal"]}">Se referenser</a>' if p["gal"] else ""}</div></div>
  <div class="rounded reveal" style="aspect-ratio:4/3;max-width:640px;justify-self:end;width:100%"><img src="{p["cover"]}" alt="{esc(p["title"])}" fetchpriority="high"></div>
</div></section>
<section style="padding-top:0"><div class="wrap">
  {f'<div class="stats reveal" style="margin-bottom:64px">{stat_html}</div>' if stats else ""}
  <div class="p-intro" style="padding-top:0">
    <div class="p-text prose reveal">{intro_html}</div>
    <aside class="spec reveal"><dl>{spec_html}</dl>{doc_html}<a class="btn btn-primary" href="kontakt.html#offert">Begär offert {ARROW}</a></aside>
  </div>
</div></section>
{extra}
{refs(p["gal"]) if p["gal"] else ""}
{CTA}'''
    page(f"{slug}.html", f"{p['title']} – Fönsterfabriken i Väst", p["short"], body, "produkter.html", p["cover"])


# Fönster
product_page("fonster",
    "Svensktillverkade, underhållsfria och energibesparande PVC-fönster – i Göteborg och hela Västsverige.",
    """<p>Fönstren tillverkas av tyskt, miljövänligt material utan bly. Profilerna är väderbeständiga och underhållsfria – man behöver aldrig måla fönstren, men kan polera dem för att bevara glansen.</p>
<p>Profilerna består av fem kammare för bättre isolering och är förstärkta med metall.</p>
<p>Vi erbjuder ett stort urval av glas, både för privatpersoner och företag. Olika design för badrumsglas, härdat och laminerat glas finns som tillval.</p>
<p>Beslagen är av tyskt ursprung och har olika lösningar. Standardfönster öppnas inåt och är ställbara i vädringsläge, så kallat dreh-kipp. Men det finns fler möjligheter: utåtgående funktion används på balkongdörrar och pardörrar, och skjutdörrar – med sin unika funktion – blev storsäljare på bara några månader.</p>""",
    [("1,0 <small>W/m²K</small>", "U-värde, 2-glas"), ("0,7 <small>W/m²K</small>", "U-värde, 3-glas"),
     ("1,3 / 1,0", "Hela konstruktionen, 2- resp. 3-glas"), ("5", "Kammare i profilen")],
    [("Material", "PVC-profil, tysk, blyfri"), ("Glas", "2- eller 3-glas med argon"), ("Öppning", "Dreh-kipp (inåt + vädring), kipp, fast"),
     ("Former", "Rektangulära, runda, halvrunda, 45°"), ("Underhåll", "Ingen målning – någonsin")],
    f'''<section style="padding-top:0"><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow">Utföranden</span><h2>Ritningar och funktioner</h2></div><p class="muted" style="max-width:40ch">Alla fönster tillverkas efter mått. Kombinera fasta och öppningsbara lufter fritt.</p></div>
  <div class="reveal">{drawings([
      ("1", "Fast", "Fast fönster, smalt"), ("2", "Fast", "Fast fönster, brett"),
      ("3", "Fast med mittpost", "Vertikal mittpost"), ("6", "Fast med mittpost", "Vertikal och horisontell mittpost"),
      ("4", "Fast med mittpost", "Horisontell mittpost"), ("5", "Fast med mittpost", "Dubbel vertikal mittpost"),
      ("10", "Dreh-kipp", "En luft, sidohängt inåtgående med vädring"), ("14", "Kipp", "Underkantshängt"),
      ("9", "Dreh-kipp", "Två lufter, sidohängda inåtgående med vädring"),
      ("17", "Kombination", "Fasta fönster och 2-lufts dreh-kipp"), ("15", "Kombination", "Fasta fönster och kippfönster"),
      ("13", "Kombination", "Fasta fönster och 1-lufts dreh-kipp"), ("7", "Specialform", "Kvadratfönster vänt 45°"),
      ("arch-2", "Specialform", "Halvrunt fönster"), ("arch", "Specialform", "Runt fönster"),
      ("8", "Kombination", "Fast fönster och dreh-kipp"), ("16", "Kombination", "Dreh-kipp och kipp"),
      ("12", "Kombination", "Fast fönster och två 1-lufts dreh-kipp")], "fonster")}</div>
</div></section>''',
    docs=[("Montering fönster", "montering-fonster"), ("Monteringsbok", "monteringsbok"), ("Skötselråd", "skotsel")])

# Balkongdörrar
product_page("balkongdorrar",
    "Balkongdörrar, altandörrar och pardörrar i PVC – stabila, säkra och lättmonterade.",
    """<p>Vi erbjuder ett stort urval av balkongdörrar och pardörrar. Dörren har spanjolettlåsning, vilket låser dörren runt om. Säkerhetsklass V-1 och V-2 finns som tillval.</p>
<p>Modulerna är stabila och lättmonterade. Ett stort urval av konstruktionslösningar garanterar att du alltid hittar något som passar dig. Olika färger på profiler och beslag erbjuds som tillval.</p>
<p>Välj mellan standardtröskel på 67 mm och låg aluminiumtröskel.</p>
<p>Dörrarna finns med 2- och 3-glas energikassetter fyllda med argon, värmekoefficient 1,0 W/m²K respektive 0,7 W/m²K. Hela konstruktionen ligger på 1,3 W/m²K med dubbelglas och 1,0 W/m²K med trippelglas.</p>
<p>Tillverkning och utställning finns i Lilla Edet.</p>""",
    [("1 100 <small>mm</small>", "Max bredd, enkel dörr"), ("1 800 <small>mm</small>", "Max bredd, pardörr"),
     ("0,7 <small>W/m²K</small>", "U-värde glas, 3-glas"), ("V-1 / V-2", "Säkerhetsklass som tillval")],
    [("Låsning", "Spanjolett, låser runt om"), ("Tröskel", "Standard 67 mm eller låg aluminium"), ("Gångjärn", "3 st Dr. Hahn (utåtgående)"),
     ("Tillval", "Handtag och lås, glas, bröstning, spröjs"), ("Färg", "Profiler och beslag i valfri färg")],
    f'''<section style="padding-top:0"><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow">Utföranden</span><h2>Dörrtyper</h2></div><p class="muted" style="max-width:40ch">Samtliga kan kompletteras med handtag och lås, glas, bröstning och spröjs.</p></div>
  <div class="reveal">{drawings([
      ("1", "Diagram A", "Sidohängd inåtgående dörr med vädring (dreh-kipp)"),
      ("3", "Diagram B", "Sidohängd utåtgående dörr med handtagsstyrd broms och 3 gångjärn – även med låg aluminiumtröskel"),
      ("7", "Diagram C", "Pardörr inåtgående med vädring på ena dörren – även med låg aluminiumtröskel"),
      ("2", "Diagram AA", "Sidohängd inåtgående dörr med låg aluminiumtröskel, handtagsstyrd broms och 3 gångjärn"),
      ("5", "Diagram D", "Källardörr med sandwichpanel i stället för glas, inåtgående"),
      ("6", "Diagram F", "Källardörr med sandwichpanel i stället för glas, utåtgående"),
      ("8", "Diagram G", "Pardörr utåtgående med öppning 180°, låg aluminiumtröskel och handtagsstyrd broms")], "balkong")}</div>
</div></section>''',
    docs=[("Montering dörrar", "montering-dorr"), ("Justering dörrar", "justering-dorr"), ("Ritningar & priser", "profil")])

# Skjutdörrar
product_page("skjutdorrar",
    "Skjutdörrar i PVC med olika konstruktioner och i olika prisklasser – upp till 8 meter breda.",
    """<p>Vi erbjuder skjutdörrar med olika konstruktioner och i olika prisklasser. Maximal höjd är 2,5 m och maximal bredd 8 m – och det går att bygga på med glaspartier. Öppningen är hälften av dörrens bredd. Dörren har vädringsfunktion och glider smidigt åt sidan.</p>
<p>Enligt Boverkets regler ska glaset upp till 60 cm från golvet vara säkerhetsglas, både på insidan och utsidan. Det är möjligt bara om glasrutan delas med en impost – annars ska hela glaset vara säkerhetsglas. Säkerhetsglas är antingen härdat glas (som en duschvägg) eller laminerat glas (som en bilruta).</p>
<p>Spanjoletten låser dörren runt om. Säkerhetsklass V-1 och V-2 finns som tillval. Försäkringsbolag kräver att dörren ska vara låsbar med nyckel – se olika alternativ av handtag och lås under <a class="link" href="tillval.html">Tillval</a>.</p>
<h3>Modell S</h3>
<p>Standardmodell som tillverkas upp till 3,4 m bredd som tvådelad och 6 m bredd som fyrdelad. System 3130 S är anpassat för upp till 130 kg och system 4150 S upp till 150 kg. Dörren glider in i karmen i nedersta delen och fastnar i vädringsläge; översta delen trycker man in manuellt.</p>
<h3>Modell Z</h3>
<p>Har självindragande mekanism: när handtaget vrids dras dörren in i öppningen. Man slipper trycka in dörren, vilket är behagligt vid bredare konstruktioner. System 160-Z är anpassat för 160 kg och system 200-Z för 200 kg.</p>
<p>Vi erbjuder både frakt och montering av partierna, med ROT-avdrag och till rimlig kostnad. Tillverkning och utställning finns i Lilla Edet.</p>""",
    [("8 <small>m</small>", "Max bredd"), ("2,5 <small>m</small>", "Max höjd"), ("200 <small>kg</small>", "Max dörrvikt, system 200-Z"), ("1,0 <small>W/m²K</small>", "Hela konstruktionen, 3-glas")],
    [("Modeller", "S (standard) och Z (självindragande)"), ("System", "3130 S · 4150 S · 160-Z · 200-Z"), ("Glas", "2- eller 3-glas med argon; säkerhetsglas"),
     ("Låsning", "Spanjolett, V-1/V-2 som tillval"), ("Montering", "Frakt och montering med ROT-avdrag")],
    f'''<section style="padding-top:0"><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow">Utföranden</span><h2>Konfigurationer</h2></div><p class="muted" style="max-width:40ch">Alla ritningar är sedda från insidan, när du står framför dörren.</p></div>
  <div class="reveal">{drawings([
      ("ab", "Diagram A–B", "Tvådelad skjutdörr upp till 3,4 m – från höger till vänster eller vänster till höger"),
      ("cdef", "Diagram C–F", "Tredelad skjutdörr upp till 5 m – med en skjutbar dörr från center eller från sidan"),
      ("aabb", "Diagram AA–BB", "Tvådelad med dörrblad på båda sidor – en dörr skjutbar, den andra fast, samma glasyta"),
      ("ccddeee", "Diagram CC–FF", "Tredelad med dörrblad på båda sidor – en dörr skjutbar, samma glasyta"),
      ("hj", "Diagram H–J", "Tvådelad skjutdörr upp till 4 m"),
      ("klmn", "Diagram K–N", "Tredelad skjutdörr upp till 6 m"),
      ("fyrdelad", "Fyrdelad", "Fyrdelad dörr med öppning i mitten, upp till 8 m")], "skjutdorrar", "wide")}</div>
</div></section>''',
    docs=[("Montering skjutdörrar", "montering-patio"), ("Justering skjutdörrar", "justering-skjutdorr"),
          ("Lås och handtag – tillbehör & priser", "info"), ("Ritningar & priser", "profil")])

# Kombinerade dörrar
product_page("kombinerade-dorrar",
    "Skjutdörr och svängdörr i samma parti – för stora, ljusa öppningar.",
    """<p>Dörren har en vädringsfunktion och glider smidigt åt sidan. Den har hög säkerhet eftersom den låses med spanjoletter.</p>
<p>Modulerna är stabila och lättmonterade. Ett stort urval av konstruktionslösningar garanterar att du alltid hittar något som passar dig. Olika färger på profiler och beslag erbjuds som tillval, och partierna finns med dubbel- eller trippelglas.</p>
<p>Tillverkning och utställning finns i Lilla Edet.</p>""",
    [("1,2 <small>W/m²K</small>", "Hela konstruktionen, 2-glas"), ("1,0 <small>W/m²K</small>", "Hela konstruktionen, 3-glas")],
    [("Låsning", "Spanjoletter"), ("Glas", "Dubbel- eller trippelglas"), ("Färg", "Profiler och beslag i valfri färg")],
    f'''<section style="padding-top:0"><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow">Utföranden</span><h2>Kombinationer</h2></div></div>
  <div class="reveal">{drawings([
      ("1", "", "Kombinerad skjutdörr och inåtgående dörr med impost"),
      ("2", "", "Kombinerad skjutdörr och utåtgående dörr med impost"),
      ("3", "", "Skjutdörr som går över vägen"),
      ("4", "", "Skjutdörr och inåtgående dörr utan mittstolpe – stor öppning"),
      ("5", "", "Dubbla skjutdörrar och inåtgående dörr")], "kombi", "wide")}</div>
</div></section>''',
    docs=[("Ritningar kombinerade dörrar", "fonster")])

# Takfönster
product_page("takfonster",
    "Tyska takfönster från ROTO – motsvarighet till Velux, med samma egenskaper och dimensioner.",
    """<p>Tyska takfönster från ROTO är en motsvarighet till Velux och har samma egenskaper och samma dimensioner. ROTO tillverkar fönster i både trä och PVC.</p>
<p>Vi erbjuder även persienner och rullgardiner till takfönster.</p>
<p>Mer information finns på tillverkarens webbplats, <a class="link" href="https://www.roto-frank.com" target="_blank" rel="noopener">roto-frank.com</a>.</p>""",
    [], [("Tillverkare", "ROTO, Tyskland"), ("Material", "Trä eller PVC"), ("Mått", "Samma dimensioner som Velux"), ("Tillbehör", "Persienner och rullgardiner")],
    f'''<section style="padding-top:0"><div class="wrap"><div class="split reveal">
  <div class="drawing" style="padding:32px"><div class="pic" style="height:auto"><img src="{I}misc/takfonster-ritning.webp" alt="Ritning takfönster" style="max-height:none" loading="lazy"></div></div>
  <div><span class="eyebrow">Byte av takfönster</span><h2>Passar i befintliga öppningar</h2><p class="lead" style="margin-top:1rem">Eftersom måtten är desamma som hos Velux kan ROTO-fönster ersätta befintliga takfönster utan att öppningen behöver ändras.</p></div>
</div></div></section>''')

# Fasader
product_page("fasader",
    "Underhållsfria fasader i vinyl – ett fräscht yttre som aldrig behöver målas om.",
    """<p>Vi levererar och monterar underhållsfri fasadpanel. Panelen behöver aldrig målas och håller färgen år efter år – ett bra komplement när huset ändå får nya, underhållsfria fönster.</p>
<p>Fasaderna passar både vid renovering och nybyggnation. I galleriet nedan ser du hus där vi bytt både fönster och fasad.</p>
<p>Vi tillverkar även SIP-element för hustillverkning – läs mer under <a class="link" href="hustillverkning.html">Hustillverkning</a>.</p>""",
    [], [("Material", "Vinylpanel (PVC)"), ("Underhåll", "Ingen målning"), ("Passar", "Renovering och nyproduktion")],
    "", eyebrow="Produkter")

# Persienner
product_page("persienner",
    "Persienner, rullgardiner och myggnät – anpassade efter våra fönster och dörrar.",
    """<p>Vi erbjuder persienner, rullgardiner och myggnät som passar fönster, dörrar och takfönster. Persiennerna kommer från den tjeckiska tillverkaren <a class="link" href="https://www.isotra.cz" target="_blank" rel="noopener">Isotra</a>.</p>
<p>Montering är enkel – instruktioner för rullgardiner finns som PDF här bredvid och under <a class="link" href="dokument.html">Dokument</a>.</p>""",
    [], [("Produkter", "Persienner, rullgardiner, myggnät"), ("Tillverkare", "Isotra"), ("Passar", "Fönster, dörrar och takfönster")],
    f'''<section style="padding-top:0"><div class="wrap"><div class="tiles reveal">
  <div class="tile"><div class="img"><img src="{I}tillval/persienn.webp" alt="Persienn" loading="lazy"></div><div class="body"><h3>Persienner</h3><p>Monteras direkt på bågen – följer med när fönstret öppnas.</p></div></div>
  <div class="tile"><div class="img"><img src="{I}tillval/rullgardin.webp" alt="Rullgardin" loading="lazy"></div><div class="body"><h3>Rullgardiner</h3><p>Mörkläggande eller ljusfiltrerande, i flera färger och mönster.</p></div></div>
  <div class="tile"><div class="img"><img src="{I}tillval/myggnat.webp" alt="Myggnät" loading="lazy"></div><div class="body"><h3>Myggnät</h3><p>För fönster och dörrar – frisk luft utan insekter.</p></div></div>
</div></div></section>''',
    docs=[("Montering rullgardiner", "en-installation-rollite")])

# Tillval
def swatches(folder, files, label):
    return "".join(f'<a href="{I}tillval/{folder}/{f}.webp" data-lb><img src="{I}tillval/{folder}/{f}.webp" alt="{label} {n}" loading="lazy"></a>'
                   for n, f in enumerate(files, 1))


body = f'''{page_hero("Produkter", "Tillval", "Gör fönstren och dörrarna till dina egna – välj glas, handtag och lås, spröjs och övriga tillbehör.")}
<section style="padding-top:0"><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow">01 · Glas</span><h2>Glas</h2></div><p class="muted" style="max-width:44ch">Vi tillhandahåller alla glasalternativ som finns på marknaden: energiglas med argon och varma kanter, solskydd, ljudisolerande, smutsavvisande, matt och mönstrat, brandsäkert samt härdat och laminerat säkerhetsglas.</p></div>
  <div class="photos reveal" data-lb-group>{swatches("glas", [str(i) for i in range(1, 21)] + ["laminerat-glas"], "Glas")}</div>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow">02 · Handtag och lås</span><h2>Handtag och lås</h2></div><p class="muted" style="max-width:44ch">Standardhandtag, låsbara handtag, barnsäkerhet, grephandtag och handtag för ASSA-lås. Se prislistan för lås och handtag.</p></div>
  <div class="photos reveal" data-lb-group>{swatches("handtag", [str(i) for i in range(1, 13)], "Handtag")}</div>
  <p style="margin-top:20px"><a class="link" href="dokument/info.pdf" target="_blank" rel="noopener">Lås och handtag – tillbehör &amp; priser (PDF)</a></p>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow">03 · Spröjs</span><h2>Spröjs</h2></div><p class="muted" style="max-width:44ch">Spröjs ger fönstren en klassisk karaktär – välj mönster som passar husets stil.</p></div>
  <div class="photos reveal" data-lb-group>{swatches("sprojs", ["1","2","3","4","5","6","7","8","9","10","11","12","15","712","715","003","000"], "Spröjs")}</div>
</div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow">04 · Övrigt</span><h2>Övriga tillbehör</h2></div></div>
  <div class="tiles reveal">
    <a class="tile" href="persienner.html"><div class="img"><img src="{I}tillval/persienn.webp" alt="" loading="lazy"></div><div class="body"><h3>Persienner</h3><p>Se persienner och rullgardiner →</p></div></a>
    <a class="tile" href="persienner.html"><div class="img"><img src="{I}tillval/myggnat.webp" alt="" loading="lazy"></div><div class="body"><h3>Myggnät</h3><p>För fönster och dörrar →</p></div></a>
    <div class="tile"><div class="img"><img src="{I}tillval/ovrigt-1.webp" alt="" loading="lazy"></div><div class="body"><h3>Övriga tillbehör</h3><p>Fönsterbänkar, foder och annat som behövs vid montering.</p></div></div>
  </div>
</div></section>
{CTA}'''
page("tillval.html", "Tillval – glas, handtag, spröjs | Fönsterfabriken i Väst", "Glas, handtag och lås, spröjs, persienner och myggnät till PVC-fönster och dörrar.", body, "produkter.html", PBY["tillval"]["cover"])

# ---------------------------------------------------------------- produkter overview
body = f'''{page_hero("Produkter", "Fönster och dörrar i PVC – tillverkade efter mått", "Allt tillverkas på beställning i vår fabrik i Lödöse. Energisnålt, underhållsfritt och kostnadseffektivt.")}
<section style="padding-top:0"><div class="wrap"><div class="grid">{"".join(pcard(p) for p in PRODUCTS)}</div></div></section>
{CTA}'''
page("produkter.html", "Produkter – Fönsterfabriken i Väst", "PVC-fönster, balkongdörrar, skjutdörrar, kombinerade dörrar, takfönster, fasader och tillval.", body, "produkter.html")

# ---------------------------------------------------------------- home
FEAT = PRODUCTS[:4]
home = f'''
<section class="hero">
  <div class="hero-inner">
    <img src="{HERO}" alt="Villa med PVC-fönster, skjutdörrar och burspråk från Fönsterfabriken i Väst" fetchpriority="high">
    <a class="hero-tag" href="kontakt.html">Utställning i Lilla Edet →</a>
    <div class="hero-content">
      <div>
        <span class="eyebrow" style="color:#cfe1ea">Svensktillverkade PVC-fönster &amp; dörrar</span>
        <h1>Fönster som släpper in ljuset – och håller ute vädret</h1>
      </div>
      <div>
        <p>PVC är ett perfekt material för konstruktion – därför väljer allt fler PVC-fönster och dörrar i sina fastigheter. Energisnåla, underhållsfria och kostnadseffektiva.</p>
        <div class="btns"><a class="btn btn-light" href="kontakt.html#offert">Begär offert {ARROW}</a><a class="btn btn-ghost" href="produkter.html">Se produkter</a></div>
        <div class="glass-chips"><span>U 0,7 W/m²K</span><span>5 kammare</span><span>Upp till 8 m</span></div>
      </div>
    </div>
  </div>
</section>

<section><div class="wrap">
  <div class="split top">
    <div class="reveal"><span class="eyebrow">Fönsterfabriken i Väst</span><h2>Hög kvalitet och säkerhet – med ett framtidstänkande.</h2></div>
    <div class="reveal">
      <p class="lead" style="max-width:none">Våra fönster är energisnåla, underhållsfria och kostnadseffektiva. Vi tillhandahåller alla de glasalternativ som finns på marknaden.</p>
      <p class="muted" style="margin-top:1rem">Vi tillverkar fönster, balkongdörrar, skjutdörrar och kombinerade partier efter mått i vår fabrik i Lödöse, med lager och utställning i Lilla Edet. Vi erbjuder frakt och montering till rimlig kostnad – med ROT-avdrag.</p>
      <div class="facts"><div><b>0,7</b><span>U-värde, 3-glas (W/m²K)</span></div><div><b>8 m</b><span>Max bredd skjutdörr</span></div><div><b>500+</b><span>Referensbilder</span></div></div>
    </div>
  </div>
  <div class="values">
    <div class="value reveal"><span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3v2M12 19v2M4.2 4.2l1.4 1.4M18.4 18.4l1.4 1.4M3 12h2M19 12h2M4.2 19.8l1.4-1.4M18.4 5.6l1.4-1.4"/><circle cx="12" cy="12" r="4"/></svg></span><h3>Energisnåla</h3><p>Femkammarprofiler förstärkta med metall och 2- eller 3-glas med argon. U-värde ned till 0,7 W/m²K i glaset.</p></div>
    <div class="value reveal"><span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l7 3v6c0 4.5-3 7.5-7 9-4-1.5-7-4.5-7-9V6z"/><path d="M9 12l2 2 4-4"/></svg></span><h3>Underhållsfria</h3><p>Väder- och färgbeständiga profiler i tyskt, blyfritt material. Fönstren behöver aldrig målas – bara poleras.</p></div>
    <div class="value reveal"><span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="7" width="18" height="12" rx="2"/><path d="M3 11h18M7 15h3"/></svg></span><h3>Kostnadseffektiva</h3><p>Direkt från fabrik, tillverkat efter mått. Frakt och montering till rimlig kostnad, med ROT-avdrag.</p></div>
  </div>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow">Produkter</span><h2>Vårt sortiment</h2></div><a class="btn btn-ghost" href="produkter.html">Alla produkter {ARROW}</a></div>
  <div class="grid">{"".join(pcard(p) for p in PRODUCTS)}</div>
</div></section>

<section class="dark"><div class="wrap">
  <div class="split top">
    <div class="reveal"><span class="eyebrow">Fördelar med PVC-fönster</span><h2>Ett material byggt för det svenska klimatet.</h2>
      <p class="lead" style="margin-top:1.2rem">Profiler från VEKA, beslag från Roto och Winkhaus, handtag från Hoppe och glas från Press Glas.</p>
      <a class="btn btn-light" style="margin-top:2rem" href="info.html">Läs mer om PVC {ARROW}</a></div>
    <ul class="ticks reveal">{"".join(f"<li>{t}</li>" for t in ["Energibesparande", "Underhållsfria", "Lång livslängd", "Väderbeständiga", "Färgbeständiga", "Miljövänliga", "Ljudisolerande", "Måttbeställning", "Elegant design", "Hög säkerhet"])}</ul>
  </div>
</div></section>

<section><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow">Galleri</span><h2>Från våra kunder</h2></div><a class="btn btn-ghost" href="galleri.html">Hela galleriet {ARROW}</a></div>
  <div class="photos lg reveal" data-lb-group>{photos([I + "galleri/skjutdorrar/skjutdorrar-115.webp", I + "galleri/fonster/fonster-114.webp", I + "galleri/dorrar/dorrar-1011.webp", I + "galleri/fasad/fasad-214.webp", I + "galleri/skjutdorrar/skjutdorrar-1811.webp", I + "galleri/fonster/fonster-4311.webp", I + "galleri/dorrar/dorrar-815.webp", I + "galleri/skjutdorrar/skjutdorrar-1311.webp"], "Referens")}</div>
</div></section>

<section style="padding-top:0"><div class="wrap">
  <div class="split">
    <div class="rounded reveal" style="aspect-ratio:4/3"><img src="{I}hus/lena.webp" alt="Tillbyggnad i Kållekär" loading="lazy"></div>
    <div class="reveal"><span class="eyebrow">Isolla Bygg</span><h2>Hustillverkning med SIP-element</h2>
      <p class="lead" style="margin-top:1.2rem">Utöver fönster och dörrar bygger vi tillbyggnader, attefallshus och hela hus med egentillverkade SIP-moduler och underhållsfria fasader.</p>
      <a class="btn btn-primary" style="margin-top:2rem" href="hustillverkning.html">Se referenser {ARROW}</a></div>
  </div>
</div></section>
{CTA}'''
page("index.html", "Fönsterfabriken i Väst – PVC-fönster och dörrar i Lilla Edet & Göteborg",
     "Svensktillverkade, underhållsfria och energibesparande PVC-fönster och dörrar. Tillverkning i Lödöse, utställning i Lilla Edet.", home, "index.html")

# ---------------------------------------------------------------- galleri
order = ["fonster", "skjutdorrar", "dorrar", "kombi", "fasad", "persienner", "garderober"]
total = sum(len(GAL[k]) for k in order)
btns = f'<button class="active" data-filter="alla">Alla<span class="count">{total}</span></button>' + "".join(
    f'<button data-filter="{k}">{GAL_LABEL[k]}<span class="count">{len(GAL[k])}</span></button>' for k in order)
allphotos = "".join(photos(GAL[k][SKIP.get(k, 0):] + GAL[k][:SKIP.get(k, 0)], GAL_LABEL[k], cat=k) for k in order)
body = f'''{page_hero("Galleri", "Referenser", f"Över {total} bilder på fönster, dörrar och fasader som vi levererat och monterat. Filtrera på produkt och klicka för att förstora.")}
<section style="padding-top:0"><div class="wrap">
  <div class="filters">{btns}</div>
  <div class="photos" data-lb-group>{allphotos}</div>
  <p class="sticky-note" style="margin-top:24px">Se även <a class="link" href="hustillverkning.html">hustillverkning och SIP-element</a>.</p>
</div></section>
{CTA}'''
page("galleri.html", "Galleri – Fönsterfabriken i Väst", "Referensbilder på PVC-fönster, skjutdörrar, balkongdörrar, fasader, persienner och garderober.", body, "galleri.html")

# ---------------------------------------------------------------- hustillverkning
h = GAL["hus"]
cells = "".join(f'<figure class="ref{" big" if i == 0 else ""} reveal"><a href="{src}" data-lb><img src="{src}" alt="{esc(t)}" loading="lazy"></a><figcaption>{esc(t)}</figcaption></figure>' for i, (src, t) in enumerate(h))
body = f'''{page_hero("Isolla Bygg", "Hustillverkning", "Tillbyggnader, attefallshus och hela hus – byggda med egentillverkade SIP-element, underhållsfria fasader och våra egna fönster och dörrar.")}
<section style="padding-top:0"><div class="wrap">
  <div class="refs" data-lb-group>{cells}</div>
</div></section>
<section style="padding-top:0"><div class="wrap"><div class="services">
  <div class="service reveal"><h3><span>01</span>SIP-element</h3><p>Vi producerar SIP-moduler (Structural Insulated Panels) i egen regi – välisolerade, lätta och snabba att resa på plats.</p></div>
  <div class="service reveal"><h3><span>02</span>Underhållsfri fasad</h3><p>Husen kläs med underhållsfri fasadpanel som aldrig behöver målas. <a class="link" href="fasader.html">Läs mer om fasader</a></p></div>
  <div class="service reveal span"><h3><span>03</span>Referensprojekt</h3><ul class="service-list">
    <li>Tillbyggnad i Kållekär<span>Tillbyggnad</span></li><li>Attefallshus Mölndal<span>Attefallshus</span></li>
    <li>Attefallshus Norra Granliden<span>Attefallshus</span></li><li>Norra Granliden<span>Tillbyggnad</span></li>
    <li>Suterränghus i Hjärtum<span>Nybyggnad</span></li><li>Produktion av SIP-moduler<span>Fabrik, Lödöse</span></li></ul></div>
</div></div></section>
{CTA}'''
page("hustillverkning.html", "Hustillverkning – Isolla Bygg | Fönsterfabriken i Väst", "Tillbyggnader, attefallshus och hus med SIP-element och underhållsfria fasader.", body, "hustillverkning.html", h[0][0])

# ---------------------------------------------------------------- info
logos = [("veka", "VEKA – profiler"), ("roto", "Roto – beslag"), ("winkhaus", "Winkhaus – beslag"), ("hoppe", "Hoppe – handtag"),
         ("pressglas", "Press Glas – glas"), ("isotra", "Isotra – persienner")]
body = f'''{page_hero("Om PVC", "Fördelar med PVC-fönster", "PVC är ett perfekt material för konstruktion. Här är varför – och vilka leverantörer vi arbetar med.")}
<section style="padding-top:0"><div class="wrap"><div class="services">
  <div class="service reveal"><h3><span>01</span>Fördelar</h3><ul class="ticks" style="grid-template-columns:1fr 1fr;margin-top:12px">{"".join(f"<li>{t}</li>" for t in ["Energibesparande", "Underhållsfria", "Lång livslängd", "Väderbeständiga", "Färgbeständiga", "Miljövänliga", "Ljudisolerande", "Måttbeställning", "Elegant design"])}</ul></div>
  <div class="service reveal"><h3><span>02</span>Utbud av glas</h3><ul class="ticks" style="grid-template-columns:1fr 1fr;margin-top:12px">{"".join(f"<li>{t}</li>" for t in ["2-glaskassett U 1,1", "3-glaskassett U 0,8", "Med argon", "Med varma kanter", "Med solskydd", "Ljudisolerande", "Smutsavvisande", "Matt/mönstrat glas", "Brandsäkert", "Säkerhetsglas"])}</ul></div>
  <div class="service reveal span"><h3><span>03</span>Beslag</h3><ul class="service-list">
    <li>Inåtgående dreh-kipp<span>Sidohängda med vädring</span></li>
    <li>Utåtgående med gömda gångjärn<span>Dörrar och fönster</span></li>
    <li>Handtagsstyrda bromsar för dörrar<span>Utåtgående dörrar</span></li></ul></div>
</div></div></section>
<section style="padding-top:0"><div class="wrap">
  <div class="section-head reveal"><div><span class="eyebrow">Leverantörer</span><h2>Tysk och europeisk kvalitet</h2></div></div>
  <div class="logos reveal">{"".join(f'<div><img src="{I}logos/{f}.webp" alt="{esc(t)}" loading="lazy"></div>' for f, t in logos)}</div>
  <div class="logos" style="margin-top:8px">{"".join(f'<span>{esc(t)}</span>' for f, t in logos)}</div>
</div></section>
{CTA}'''
page("info.html", "Fördelar med PVC-fönster – Fönsterfabriken i Väst", "Fördelar med PVC-fönster, glasalternativ, beslag och leverantörer.", body, "info.html")

# ---------------------------------------------------------------- dokument
groups = [
    ("01", "Certifikat", [("Certifikat 2-glas, U-värde", "2glas"), ("Certifikat 3-glas, U-värde", "3glas"), ("Certifikat 2-glas, Rw", "glas-2gl-rw"),
                         ("Certifikat 3-glas, Rw", "glas-3gl-rw"), ("Certifikat profil, säkerhet", "certificat-security-profil"),
                         ("Teknisk data, profil (Softline 70 AD)", "teh-data-profil-softline-70-ad-data"), ("P-märkning glas", "p-mark-glas"),
                         ("P-märkning profil / profilkatalog", "profil-katalog"), ("Ritningar profil (VEKA)", "veka")]),
    ("02", "Montering", [("Monteringsbok", "monteringsbok"), ("Montering fönster", "montering-fonster"), ("Montering dörrar", "montering-dorr"),
                        ("Montering skjutdörrar", "montering-patio"), ("Montering rullgardiner", "en-installation-rollite")]),
    ("03", "Justering", [("Justering dörrar", "justering-dorr"), ("Justering Designo", "justering-designo"), ("Justering skjutdörrar", "justering-skjutdorr")]),
    ("04", "Rapporter & övrigt", [("SP-rapport fönster", "sp-raport"), ("Skötselråd", "skotsel"), ("Garantikort", "garantikort"),
                                 ("Lås och handtag – tillbehör & priser", "info"), ("Ritningar & priser, dörrar", "profil"), ("Ritningar kombinerade dörrar", "fonster")]),
]
cards = "".join(f'<div class="service reveal"><h3><span>{n}</span>{t}</h3>{doclinks(rows)}</div>' for n, t, rows in groups)
body = f'''{page_hero("Dokument", "Certifikat, montering och skötsel", "Ladda ner certifikat, monteringsanvisningar, justeringsguider och garantikort.")}
<section style="padding-top:0"><div class="wrap"><div class="docs">{cards}</div></div></section>
{CTA}'''
page("dokument.html", "Dokument – Fönsterfabriken i Väst", "Certifikat, monteringsanvisningar, justering, skötselråd och garantikort.", body, "dokument.html")

# ---------------------------------------------------------------- frakt
fr = [I + "frakt/" + f + ".webp" for f in ["lastbil", "dsc01452", "dsc05354", "dsc01445", "dsc01378"]]
body = f'''{page_hero("Frakt", "Information om frakt och leverans", "Hämta själv i Lilla Edet eller låt oss leverera med egen lastbil till närliggande områden.")}
<section style="padding-top:0"><div class="wrap">
  <div class="split top">
    <div class="rounded reveal" style="aspect-ratio:4/3"><img src="{fr[0]}" alt="Fönsterfabrikens lastbil" loading="lazy"></div>
    <div class="services" style="grid-template-columns:1fr">
      <div class="service reveal"><h3><span>01</span>Egen transport</h3>
        <p>Kommer du med egen transport ska du tänka på att ta med tillräckligt med spännband och kartong. Fönster och dörrar ska köras stående.</p>
        <p>I priset ingår lastning med truck. Om ert transportmedel inte är avsett för den typen av lastning, ta med hjälp eller beställ lastningshjälp i förväg. Lastning kostar 250 kr + moms per timme och person, minsta debitering 30 minuter.</p>
        <p>Specialtillverkade pallar kan beställas i förväg.</p></div>
      <div class="service reveal"><h3><span>02</span>Leverans med vår lastbil</h3>
        <p>Vi har egen lastbil och erbjuder leverans av fönsterpartier till närliggande områden – begär offert för leverans.</p>
        <p>I priset ingår 30 minuter för avlastning på plats, som ordnas av kunden; föraren får inte hjälpa till på grund av ansvarsfördelning. Tid därutöver debiteras med 250 kr + moms per påbörjad timme. Har kunden beställt montering hjälper montörerna till att lasta av.</p>
        <p>Vid behov står kunden för kostnaden för kran, truck eller liknande. Är transportsträckan väldigt lång kan du begära en prisoffert på frakten.</p></div>
    </div>
  </div>
  <div class="photos lg reveal" style="margin-top:48px" data-lb-group>{photos(fr[1:], "Frakt av fönsterpartier")}</div>
</div></section>
{CTA}'''
page("frakt.html", "Frakt – Fönsterfabriken i Väst", "Frakt, lastning och leverans av PVC-fönster och dörrar.", body, "frakt.html")

# ---------------------------------------------------------------- kontakt
typer = ["Fönster", "Balkongdörr", "Skjutdörr", "Kombinerad dörr", "Takfönster", "Fasad", "Persienner/rullgardiner", "Hustillverkning"]
chips = "".join(f'<input type="checkbox" id="t{i}" name="typ" value="{t}"><label for="t{i}">{t}</label>' for i, t in enumerate(typer))
tj = "".join(f'<input type="checkbox" id="s{i}" name="tjanst" value="{t}"><label for="s{i}">{t}</label>' for i, t in enumerate(["Hämtar själv", "Leverans", "Montering"]))
body = f'''{page_hero("Kontakt", "Välkommen till Fönsterfabriken i Väst", "Ring, mejla eller besök utställningen i Lilla Edet. Skicka gärna mått och önskemål så återkommer vi med offert.")}
<section style="padding-top:0"><div class="wrap">
  <div class="contact-grid" id="offert">
    <div class="contact-info reveal">
      <span class="eyebrow" style="margin:0">Kontaktuppgifter</span>
      <dl>
        <div><dt>Telefon</dt><dd><a href="tel:{TEL1}">{TEL1_H}</a><br><a href="tel:{TEL2}">{TEL2_H}</a></dd></div>
        <div><dt>E-post</dt><dd><a href="mailto:{MAIL}">{MAIL}</a><br><a href="mailto:alina@fvab.se">alina@fvab.se</a></dd></div>
        <div><dt>Kontaktperson</dt><dd>Alina Andrews</dd></div>
        <div><dt>Lager och utställning</dt><dd>Göteborgsvägen 90<br>463 33 Lilla Edet</dd></div>
        <div><dt>Tillverkning</dt><dd>Skeppsbyggaregatan 7<br>463 71 Lödöse</dd></div>
      </dl>
    </div>
    <form class="form reveal" id="forfragan">
      <h2>Begär offert</h2>
      <p class="muted">Formuläret öppnar ditt e-postprogram med förfrågan ifylld.</p>
      <div class="row"><div><label for="namn">Namn *</label><input id="namn" name="namn" required autocomplete="name"></div>
      <div><label for="epost">E-post *</label><input id="epost" name="epost" type="email" required autocomplete="email"></div></div>
      <div class="row"><div><label for="telefon">Telefon</label><input id="telefon" name="telefon" type="tel" autocomplete="tel"></div>
      <div><label for="ort">Ort</label><input id="ort" name="ort"></div></div>
      <label>Vad gäller det?</label><div class="chips">{chips}</div>
      <div class="row"><div><label for="glas">Glas</label><select id="glas" name="glas"><option value="">Vet ej</option><option>2-glas</option><option>3-glas</option></select></div>
      <div><label>Leverans</label><div class="chips">{tj}</div></div></div>
      <label for="beskrivning">Mått, antal och önskemål *</label><textarea id="beskrivning" name="beskrivning" required placeholder="T.ex. 4 st dreh-kipp-fönster 1190 × 1180 mm, vita, 3-glas…"></textarea>
      <button class="btn btn-primary" type="submit">Skicka förfrågan {ARROW}</button>
    </form>
  </div>
  <div class="map reveal"><iframe title="Karta – Fönsterfabriken i Väst, Göteborgsvägen 90, Lilla Edet" loading="lazy" referrerpolicy="no-referrer-when-downgrade" src="https://www.google.com/maps?q=F%C3%B6nsterfabriken+i+V%C3%A4st+AB,+G%C3%B6teborgsv%C3%A4gen+90,+463+33+Lilla+Edet&output=embed"></iframe></div>
  <p style="margin-top:14px"><a class="link" href="https://www.google.com/maps/place/F%C3%B6nsterfabriken+i+V%C3%A4st+AB/@58.1257583,12.134969,17z/data=!4m6!3m5!1s0x4645402566c173e7:0xf1128126c739261f!8m2!3d58.1257583!4d12.134969" target="_blank" rel="noopener">Vägbeskrivning i Google Maps {ARROW}</a></p>
</div></section>'''
page("kontakt.html", "Kontakt – Fönsterfabriken i Väst", "Kontakta Fönsterfabriken i Väst AB – Göteborgsvägen 90, Lilla Edet. Tel 0707-14 40 01.", body, "kontakt.html")

print("Built", len(list(ROOT.glob("*.html"))), "pages")
