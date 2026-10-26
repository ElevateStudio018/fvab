"""One-time import of the scraped fvab.se mirror into assets/.
Usage: python3 tools/import_assets.py <mirror-dir>/www.fvab.se <gmaps-img-dir>
Writes optimized WebP images, PDFs and data/galleries.json."""
import json, re, shutil, sys, html
from pathlib import Path
from PIL import Image, ImageFile, ImageOps

ImageFile.LOAD_TRUNCATED_IMAGES = True

SRC, MAPS = Path(sys.argv[1]), Path(sys.argv[2])
ROOT = Path(__file__).resolve().parent.parent
IMG = ROOT / "assets/img"


def webp(src, dst, maxw=2000, q=80):
    dst = dst.with_suffix(".webp")
    dst.parent.mkdir(parents=True, exist_ok=True)
    im = ImageOps.exif_transpose(Image.open(src))
    if im.mode in ("P", "LA", "RGBA"):
        im = im.convert("RGBA")
        bg = Image.new("RGB", im.size, "white")
        bg.paste(im, mask=im.split()[-1])
        im = bg
    im = im.convert("RGB")
    if im.width > maxw:
        im = im.resize((maxw, round(im.height * maxw / im.width)), Image.LANCZOS)
    im.save(dst, "WEBP", quality=q, method=6)
    return dst.relative_to(ROOT).as_posix(), im.width, im.height


def slug(name):
    s = name.lower().translate(str.maketrans("åäö", "aao"))
    return re.sub(r"[^a-z0-9]+", "-", Path(s).stem).strip("-")


# Reference galleries: full-size images linked from bildspel/*.html, in page order
GALLERIES = {
    "fonster": "fonster-galleri.html", "skjutdorrar": "skjutdorrar-galleri.html",
    "dorrar": "balkongdorrar-galleri.html", "kombi": "kombi-galleri.html",
    "fasad": "fasad-galleri.html", "persienner": "rullgardiner-galleri.html",
    "garderober": "garderob_galleri.html",
}
data = {}
for key, page in GALLERIES.items():
    s = (SRC / "bildspel" / page).read_text(encoding="utf-8", errors="replace")
    seen, items = set(), []
    for href in re.findall(r'<a href="([^":]+\.(?:jpe?g|png|gif))"', s, re.I):
        href = html.unescape(href)
        f = SRC / "bildspel" / href
        if href.lower() in seen or not f.exists():
            continue
        seen.add(href.lower())
        items.append(webp(f, IMG / "galleri" / key / slug(href.replace("/", "-")), 1600)[0])
    data[key] = items
    print(key, len(items))

# Isolla Bygg / hustillverkning
iso = []
for name, title in [("LENA.JPG", "Tillbyggnad i Kållekär"), ("ADAM.JPG", "Attefallshus Mölndal"),
                    ("NG.jpg", "Attefallshus Norra Granliden"), ("HJÄRTUM.JPG", "Sutterränghus i Hjärtum"),
                    ("FABRIK.JPG", "Produktion av SIP-moduler")]:
    iso.append([webp(SRC / "images/isolla_galleri" / name, IMG / "hus" / slug(name))[0], title])
iso.append([webp(SRC / "images/thumbnail_IMG_5194.jpg", IMG / "hus/sip-element")[0], "SIP-element"])
data["hus"] = iso

# Technical drawings (ritningar)
for d in ["fonster", "balkong", "kombi", "skjutdorrar/temp"]:
    for f in sorted((SRC / "images" / d).glob("*.jpg")):
        webp(f, IMG / "ritningar" / d.split("/")[0] / slug(f.name), 800, 90)

# Accessories, suppliers, freight, misc
for d, out in [("glas", "tillval/glas"), ("handtag", "tillval/handtag"), ("sprojs", "tillval/sprojs"), ("frakt", "frakt")]:
    for f in sorted((SRC / "images" / d).iterdir()):
        if f.suffix.lower() in (".jpg", ".jpeg", ".png"):
            webp(f, IMG / out / slug(f.name), 1200)
for rel, out in [("images/IMG_1738.jpg", "frakt/lastbil"), ("images/content/veka70.jpg", "logos/veka"),
                 ("images/content/press_glas.jpg", "logos/pressglas"), ("images/content/roto.jpg", "logos/roto"),
                 ("images/WINKHAUS.jpg", "logos/winkhaus"), ("images/HOPPE.jpg", "logos/hoppe"), ("images/ISOTRA.jpg", "logos/isotra"),
                 ("images/792.jpg", "tillval/glas-monster"), ("images/DSC03699_1.jpg", "tillval/persienn"),
                 ("images/DSC03982.JPG", "tillval/rullgardin"), ("images/3212-160.jpg", "tillval/myggnat"),
                 ("images/GetAttachmentCA94Y80U.jpg", "tillval/ovrigt-1"), ("images/GetAttachmentCA97K56V.jpg", "tillval/ovrigt-2"),
                 ("images/kontakt3.jpg", "misc/kontakt"), ("images/tak.jpg", "misc/takfonster"),
                 ("images/content/bw-ritningar.gif", "misc/takfonster-ritning"), ("images/IMAG2348.jpg", "misc/persienner"),
                 ("images/munkedal.jpg", "misc/fasad-munkedal")]:
    if (SRC / rel).exists():
        webp(SRC / rel, IMG / out, 1600)

# Google Maps photo (the place photo linked by the client)
for f in sorted(MAPS.glob("*.jpg")):
    webp(f, IMG / "maps" / f.stem, 2400, 82)

# Documents
for f in list((SRC / "pdf").glob("*.pdf")) + list((SRC / "pdf/doc").glob("*.pdf")):
    dst = ROOT / "dokument" / slug(f.name)
    dst = dst.with_suffix(".pdf")
    dst.parent.mkdir(exist_ok=True)
    shutil.copy(f, dst)
shutil.copy(SRC / "images/favicon.ico", ROOT / "favicon.ico")

(ROOT / "data").mkdir(exist_ok=True)
(ROOT / "data/galleries.json").write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")
