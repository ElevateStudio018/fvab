# Fönsterfabriken i Väst – ny webbplats

Statisk, modern omarbetning av fvab.se med en egen "fönsterkarm"-identitet: skarpa hörn, tunna ramlinjer, sval glasgrön palett, Archivo + IBM Plex Sans/Mono.
All text, alla bilder och alla PDF:er kommer från originalsajten; startsidans hero-bild kommer från företagets Google Maps-sida. Bilden i offertsektionen (`assets/img/cta/skjutdorr-4k.webp`) är uppskalad till 3840 px med image-upscaling.net.

- 16 sidor: start, produkter (8 produktsidor), galleri (514 referensbilder med filter + lightbox), hustillverkning (Isolla Bygg), om PVC, dokument (23 PDF:er), frakt, kontakt
- Sidorna genereras från `build.py` – ändra text där och kör `python3 build.py`
- Bilder: `assets/img/` (WebP). Galleriordning: `data/galleries.json`
- `tools/import_assets.py` – engångsimport från en wget-spegling av fvab.se (redan körd)
- Offertformuläret öppnar besökarens e-postklient med förfrågan ifylld till info@fvab.se. Koppla till t.ex. Formspree/Netlify Forms för att skicka direkt.

Öppna `index.html` i webbläsaren, eller publicera mappen på valfri statisk hosting (Netlify, Vercel, GitHub Pages).
