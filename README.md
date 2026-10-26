# Fönsterfabriken i Väst – ny webbplats

Statisk, modern omarbetning av fvab.se, i samma formspråk som Essens Arkitektur-sajten (varm papperston, rundade kort, pill-meny, Poppins) men med en kallare glasblå accent.
All text, alla bilder och alla PDF:er kommer från originalsajten; startsidans hero-bild kommer från företagets Google Maps-sida.

- 16 sidor: start, produkter (8 produktsidor), galleri (514 referensbilder med filter + lightbox), hustillverkning (Isolla Bygg), om PVC, dokument (23 PDF:er), frakt, kontakt
- Sidorna genereras från `build.py` – ändra text där och kör `python3 build.py`
- Bilder: `assets/img/` (WebP). Galleriordning: `data/galleries.json`
- `tools/import_assets.py` – engångsimport från en wget-spegling av fvab.se (redan körd)
- Offertformuläret öppnar besökarens e-postklient med förfrågan ifylld till info@fvab.se. Koppla till t.ex. Formspree/Netlify Forms för att skicka direkt.

Öppna `index.html` i webbläsaren, eller publicera mappen på valfri statisk hosting (Netlify, Vercel, GitHub Pages).
