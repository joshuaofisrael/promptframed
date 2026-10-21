#!/usr/bin/env python3
"""Shop-by-category structure for moonlitwindows.com (written 19 Oct 2026, Joshua: "organize the
website under subcategories so it's easier to search").

What it does (idempotent; safe to re-run after any publish or collection-builder run):
  1. Tags every piece in products.json with  "categories": {region, country, place, scenes[]}.
     Rows that already have "categories" are left alone. New pieces get SEED tags if listed here,
     otherwise keyword auto-tags from gallery/catalog.json (title, description, keywords), marked
     "auto": true and printed so they can be reviewed.
  2. Generates browse.html (the Shop by category hub with search + filter chips) and one page per
     region / scene subcategory that has no hand-built collection page yet.
     Subcategories that already had a collection page (Asia, waterfalls, lakes, mountains, coastal,
     bedroom, murals) REUSE that page: its breadcrumb is re-pointed at the hub and any newly tagged
     piece missing from it is appended in a <!-- cats:more --> block (no duplicate pages, URLs kept).
  3. Puts the same nav (with a "Categories" dropdown) on every page, and a breadcrumb plus
     category links on every piece page (visible + BreadcrumbList JSON-LD).
  4. Updates sitemap.xml (new URLs + lastmod), llms.txt, and saves changed URLs for IndexNow.

  python3 scripts/build_categories.py           # write everything
  python3 scripts/build_categories.py --check   # dry run: exit 1 if anything would change / fails checks
  python3 scripts/build_categories.py --ping    # after commit+push: wait until live, IndexNow-ping changed URLs

Run order in a publish: publish script -> collection builders (if re-run) -> this script.
The publish scripts call build_categories.main([]) themselves, just before verify().
"""
from __future__ import annotations

import datetime
import html
import json
import re
import subprocess
import sys
import time
import unicodedata
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://moonlitwindows.com"
TODAY = datetime.date.today().isoformat()
PRODUCTS = ROOT / "products.json"
CATALOG = ROOT / "gallery" / "catalog.json"
SITEMAP = ROOT / "sitemap.xml"
LLMS = ROOT / "llms.txt"
CSS = ROOT / "styles.css"
HUB = "browse.html"
URLS_FILE = Path("/workspace/promptframed-private/category_changed_urls.json")
INDEXNOW = Path("/workspace/promptframed-private/indexnow_ping.py")
GA_ID = "G-663R8VD62L"
CF = """<script defer src='https://static.cloudflareinsights.com/beacon.min.js' data-cf-beacon='{"token": "899375a6262144aabf5184589abd580c"}'></script>"""
PRICE_SENT = ("Each comes as a 12×18 in poster ($35), the same print in a black frame ($69) or a 4×6 ft "
              "peel and stick wall mural ($149), with shipping included.")

# ------------------------------------------------------------------ taxonomy
# file: page URL. existing=True means a hand-built collection page that this script only patches.
REGIONS = [
    dict(key="nordic", label="Iceland & Nordic", file="iceland-nordic-wall-art.html", europe=True,
         h1="Iceland &amp; Nordic Wall Art: Moonlit Fjords, Falls and Black Sand",
         title="Iceland & Nordic Wall Art: Moonlit Fjord & Waterfall Prints | Moonlit Windows",
         desc="Iceland and Nordic wall art: {n} moonlit posters and framed prints of Skógafoss, Kirkjufell, the Faroes, Lofoten and Norway's fjords. From $35.",
         og="kirkjufell-waterfall-moon",
         intro=["Every Nordic piece in the Night Windows series in one place: Icelandic waterfalls and black sand, the Faroe Islands, Lofoten and the Norwegian fjords, each under a full moon with thin wispy cloud.",
                "Northern light is long and low, so these scenes keep cool greens, slate blues and silver water with only a few warm cabin windows. They suit calm bedrooms, Scandi and minimalist rooms, and anyone who has driven Iceland’s Ring Road or the Lofoten islands."]),
    dict(key="british-isles", label="Scotland, England & Ireland", file="british-isles-wall-art.html", europe=True,
         h1="Scotland, England &amp; Ireland Wall Art: Moonlit Highlands, Castles and Cliffs",
         title="Scotland, England & Ireland Wall Art: Moonlit Prints | Moonlit Windows",
         desc="Scotland, England and Ireland wall art: {n} moonlit prints of Eilean Donan, Skye, Glenfinnan, Bibury and the Cliffs of Moher. Poster $35, framed $69.",
         og="eilean-donan-castle-moon",
         intro=["Moonlit scenes from the British Isles: a Highland loch and Eilean Donan Castle, the Old Man of Storr on Skye, the Glenfinnan Viaduct, the Cotswold cottages of Bibury and the Cliffs of Moher on Ireland’s Atlantic coast.",
                "Heather, wet stone and dark water take moonlight beautifully. These prints suit a cosy living room, a study or a reading corner, and make a thoughtful gift for anyone with Scottish, English or Irish roots."]),
    dict(key="alps", label="The Alps", file="alps-wall-art.html", europe=True,
         h1="Alps Wall Art: Moonlit Alpine Lakes, Peaks and Castles",
         title="Alps Wall Art: Moonlit Alpine Lake & Mountain Prints | Moonlit Windows",
         desc="Alps wall art: {n} moonlit posters and framed prints of the Matterhorn, the Dolomites, Hallstatt, Lake Bled, Lauterbrunnen and Neuschwanstein. From $35.",
         og="hallstatt-lake-moon",
         intro=["The Alps by moonlight: the Matterhorn above Zermatt, the Tre Cime in the Dolomites, Hallstatt and Lake Bled on their still lakes, Staubbach Falls over Lauterbrunnen and Neuschwanstein on its crag.",
                "Snow holds moonlight better than anything, so alpine scenes read bright and clear even in a dim room. They pair well with lake and mountain pieces and suit a chalet-style bedroom, a hallway or a home office."]),
    dict(key="western-europe", label="Western & Central Europe", file="western-europe-wall-art.html", europe=True,
         h1="Western &amp; Central Europe Wall Art: Moonlit Old Towns, Canals and Castles",
         title="Western & Central Europe Wall Art: Moonlit Old Town Prints | Moonlit Windows",
         desc="Western and Central Europe wall art: {n} moonlit prints of Bruges, Colmar, Prague, Rothenburg, Hohenzollern, Mont Saint-Michel and Provence. From $35.",
         og="bruges-canal-moon",
         intro=["Fairytale Europe after dark: the canals of Bruges and Colmar, Rothenburg’s cobbled streets, Prague’s Charles Bridge, Hohenzollern Castle on its hill, Mont Saint-Michel on the tide and the lavender rows of Provence.",
                "Warm window light against blue night stone is the theme here, which makes these some of the cosiest pieces in the series. They suit dining rooms, hallways and travel walls, and work well as a set from one trip."]),
    dict(key="southern-europe", label="Italy, Greece & the Mediterranean", file="southern-europe-wall-art.html", europe=True,
         h1="Italy, Greece &amp; Mediterranean Wall Art: Moonlit Coasts and Old Towns",
         title="Italy, Greece & Mediterranean Wall Art: Moonlit Prints | Moonlit Windows",
         desc="Italy, Greece and Mediterranean wall art: {n} moonlit prints of Venice, Amalfi, Cinque Terre, Santorini, Dubrovnik and Lake Como. Poster $35, framed $69.",
         og="santorini-caldera-moon",
         intro=["Southern Europe under a full moon: Venice, Florence’s Ponte Vecchio, Tuscany, Lake Como, the Amalfi Coast and Cinque Terre in Italy, Santorini and Meteora in Greece, Dubrovnik and Plitvice in Croatia, and Sintra’s Pena Palace in Portugal.",
                "Pastel houses, lemon terraces and a silver path on the sea: these are the warmest, most romantic pieces in the series, suited to living rooms, kitchens and anyone missing a summer holiday."]),
    dict(key="asia", label="Asia", file="asian-wall-art.html", existing=True),
    dict(key="africa-middle-east", label="Africa, Middle East & Turkey", file="africa-middle-east-wall-art.html",
         h1="Africa, Middle East &amp; Turkey Wall Art: Moonlit Deserts, Kasbahs and Falls",
         title="Africa, Middle East & Turkey Wall Art: Moonlit Prints | Moonlit Windows",
         desc="Africa, Middle East and Turkey wall art: {n} moonlit prints of Petra, Chefchaouen, Cappadocia, Pamukkale and Victoria Falls. Poster $35, framed $69.",
         og="petra-treasury-night",
         intro=["Desert, mountain and river scenes from where three continents meet: Petra’s Treasury in Jordan, Chefchaouen’s blue lanes and a kasbah oasis in Morocco, Cappadocia’s fairy chimneys and the white terraces of Pamukkale in Turkey, and Victoria Falls with a moonbow on the Zambezi.",
                "Rose sandstone, blue walls and white travertine all glow softly under moonlight, giving these prints warm, earthy colour. They suit boho, Moroccan and desert-modern rooms."]),
    dict(key="north-america", label="USA & Canada", file="north-america-wall-art.html",
         h1="USA &amp; Canada Wall Art: Moonlit National Parks and Coasts",
         title="USA & Canada Wall Art: Moonlit National Park Prints | Moonlit Windows",
         desc="USA and Canada wall art: {n} moonlit national park prints of Banff, Moraine Lake, Yosemite, the Grand Canyon, Monument Valley and Big Sur. From $35.",
         og="moraine-lake-moon",
         intro=["North America’s great landscapes at night: Lake Louise and Moraine Lake in Banff, Yosemite’s Half Dome, the Grand Canyon, Havasu Falls, Monument Valley and Big Sur’s Bixby Bridge.",
                "Turquoise glacier lakes and red desert rock give this set strong colour that still stays calm under a cloud-veiled moon. Made for national park fans, a road-trip memory wall or a cabin."]),
    dict(key="south-america", label="South America", file="south-america-wall-art.html",
         h1="South America Wall Art: Moonlit Andes, Falls and Salt Flats",
         title="South America Wall Art: Moonlit Machu Picchu & Iguazu Prints | Moonlit Windows",
         desc="South America wall art: {n} moonlit prints of Machu Picchu, Iguazu Falls, Salar de Uyuni and Patagonia. Poster $35, framed $69, wall mural $149.",
         og="machu-picchu-mist",
         intro=["South America by moonlight: Machu Picchu rising from Andean mist in Peru, Iguazu Falls on the Argentina–Brazil border, the mirror of Salar de Uyuni in Bolivia and a glacial lake below Patagonia’s peaks.",
                "Some of the continent’s most famous places, each shown at night with natural moonlight and a few soft lights. They make a striking travel set, or a single statement piece above a sofa."]),
    dict(key="oceania", label="Oceania & the Pacific", file="oceania-pacific-wall-art.html",
         h1="Oceania &amp; Pacific Wall Art: Moonlit New Zealand, Tasmania and Islands",
         title="Oceania & Pacific Wall Art: Moonlit Island & Lake Prints | Moonlit Windows",
         desc="Oceania and Pacific wall art: {n} moonlit prints of Lake Tekapo, Cradle Mountain, Bora Bora and Hawaii's Na Pali Coast. Poster $35, framed $69.",
         og="lake-tekapo-church-moon",
         intro=["From the Southern Alps to the South Pacific: Lake Tekapo’s stone church in New Zealand, Cradle Mountain over Dove Lake in Tasmania, the overwater bungalows of Bora Bora and the emerald Na Pali Coast of Kauai, Hawaii.",
                "Turquoise water and dark green ridges under a southern moon. These suit coastal and tropical rooms, and make a lovely reminder of a honeymoon or a big trip."]),
    dict(key="imagined", label="Imagined Places", file="imagined-landscape-wall-art.html",
         h1="Imagined Landscape Wall Art: Moonlit Dreamscapes",
         title="Imagined Landscape Wall Art: Moonlit Dreamscape Prints | Moonlit Windows",
         desc="Imagined landscape wall art: {n} moonlit dreamscape posters and framed prints of meadows, cabins, cliffside towns and peaks above the clouds. From $35.",
         og="moonlit-alpine-meadow",
         intro=["The first Night Windows were not one exact place: an alpine meadow above a lit village, a lakeside cabin, a cliffside town, a lantern-lit walk to the sea, a gorge waterfall and snowy peaks above the clouds.",
                "Because they are not tied to a map, these are the easiest pieces to live with anywhere, especially in bedrooms and nurseries, and they pair with any region."]),
]
SCENES = [
    dict(key="waterfalls", label="Waterfalls", file="waterfall-wall-art.html", existing=True),
    dict(key="lakes", label="Lakes", file="lake-wall-art.html", existing=True),
    dict(key="mountains", label="Mountains", file="mountain-wall-art.html", existing=True),
    dict(key="coastal", label="Coastal & Sea", file="coastal-wall-art.html", existing=True),
    dict(key="castles", label="Castles & Palaces", file="castle-wall-art.html",
         h1="Castle Wall Art: Moonlit Castles, Palaces and Fortresses",
         title="Castle Wall Art: Moonlit Castle & Palace Prints | Moonlit Windows",
         desc="Castle wall art: {n} moonlit posters and framed prints of Neuschwanstein, Hohenzollern, Eilean Donan, Pena Palace, Bled and Mont Saint-Michel. From $35.",
         og="neuschwanstein-castle-moon",
         intro=["Every castle and palace in the series: Neuschwanstein and Hohenzollern in Germany, Eilean Donan and a ruined loch-side castle in Scotland, Bled Castle, Sintra’s Pena Palace, Prague Castle above the Vltava, Mont Saint-Michel and Dubrovnik’s walls.",
                "Lit windows on old stone under a full moon is the most storybook look in the collection, loved for kids’ rooms, libraries and fantasy-themed spaces."]),
    dict(key="villages", label="Villages & Old Towns", file="village-old-town-wall-art.html",
         h1="Village &amp; Old Town Wall Art: Moonlit Streets, Harbours and Cottages",
         title="Village & Old Town Wall Art: Moonlit Street Prints | Moonlit Windows",
         desc="Village and old town wall art: {n} moonlit prints of Hallstatt, Manarola, Santorini, Bibury, Rothenburg, Colmar and Chefchaouen. Poster $35, framed $69.",
         og="rothenburg-old-town-moon",
         intro=["Small places with warm windows: Hallstatt, Bellagio, Manarola and Santorini on the water, Reine in Lofoten, Bibury’s cottages, Rothenburg, Colmar, Bruges, Dubrovnik, Chefchaouen and the imagined villages that started the series.",
                "These are the cosiest pieces in the collection: lamplight, cobbles and flowers under a quiet moon. They suit kitchens, dining rooms and entryways."]),
    dict(key="canals-bridges", label="Bridges & Canals", file="bridge-canal-wall-art.html",
         h1="Bridge &amp; Canal Wall Art: Moonlit Bridges, Viaducts and Canals",
         title="Bridge & Canal Wall Art: Moonlit Venice, Bruges & Prague | Moonlit Windows",
         desc="Bridge and canal wall art: {n} moonlit prints of Venice, the Ponte Vecchio, Charles Bridge, Bruges, Glenfinnan Viaduct and Bixby Bridge. From $35.",
         og="venetian-canal-moonrise",
         intro=["Water and stone arches by moonlight: Venice’s canals, the Ponte Vecchio in Florence, Prague’s Charles Bridge, the Rozenhoedkaai in Bruges, Colmar’s Petite Venise, the Glenfinnan Viaduct and Big Sur’s Bixby Bridge.",
                "A bridge gives a print a strong line to follow into the scene, and a canal doubles every lit window in the water. Good for offices, hallways and anyone who loves a city break."]),
    dict(key="temples", label="Temples & Ancient Sites", file="temple-ancient-wall-art.html",
         h1="Temple &amp; Ancient Site Wall Art: Moonlit Temples, Pagodas and Ruins",
         title="Temple & Ancient Site Wall Art: Moonlit Temple Prints | Moonlit Windows",
         desc="Temple and ancient site wall art: {n} moonlit prints of Angkor Wat, Bagan, the Taj Mahal, Machu Picchu, Petra and the Great Wall. Poster $35, framed $69.",
         og="angkor-wat-moon",
         intro=["Sacred and ancient places at night: Angkor Wat, Bagan, Bali’s jungle temple, the Chureito Pagoda below Mount Fuji, a Japanese temple pond, the Taj Mahal, Sigiriya, the Great Wall, Machu Picchu, Petra, the monasteries of Meteora, Cappadocia and Pamukkale.",
                "Moonlight softens old stone and keeps these places quiet and still, which makes them good for meditation corners, studies and calm living rooms."]),
    dict(key="countryside", label="Countryside, Forests & Meadows", file="countryside-forest-wall-art.html",
         h1="Countryside &amp; Forest Wall Art: Moonlit Meadows, Fields and Groves",
         title="Countryside & Forest Wall Art: Moonlit Meadow Prints | Moonlit Windows",
         desc="Countryside and forest wall art: {n} moonlit prints of Provence lavender, Tuscany, Kyoto bamboo, rice terraces and wildflower meadows. From $35.",
         og="provence-lavender-moon",
         intro=["Quiet green places: Provence lavender, Tuscan cypress roads, Kyoto’s bamboo grove, Bali’s jungle, misty rice terraces, the Li River’s bamboo banks, the Cotswolds, and the wildflower meadows and cabins of the first Night Windows.",
                "Soft greens and wildflowers make these the gentlest pieces in the series, ideal for bedrooms, nurseries and farmhouse or cottage rooms."]),
    dict(key="deserts", label="Deserts & Canyons", file="desert-canyon-wall-art.html",
         h1="Desert &amp; Canyon Wall Art: Moonlit Canyons, Dunes and Salt Flats",
         title="Desert & Canyon Wall Art: Moonlit Southwest & Desert Prints | Moonlit Windows",
         desc="Desert and canyon wall art: {n} moonlit prints of the Grand Canyon, Monument Valley, Havasu Falls, Petra, Cappadocia and Salar de Uyuni. From $35.",
         og="monument-valley-moon",
         intro=["Big open landscapes under a full moon: the Grand Canyon, Monument Valley and Havasu Falls in Arizona, Petra’s rose-red Siq, Cappadocia, a Moroccan kasbah at the edge of the dunes and the mirror of Salar de Uyuni.",
                "Red rock and sand turn warm and quiet at night. These suit desert-modern, Southwestern and boho rooms, and look great as a set of three."]),
]
ROOMS = [
    dict(label="Bedroom", file="moon-poster-bedroom.html"),
    dict(label="Feature wall (wall murals)", file="peel-and-stick-wall-murals.html"),
    dict(label="Every piece, every format", file="buy.html"),
]
EXISTING_KIND = {"asian-wall-art.html": "region", "waterfall-wall-art.html": "scene", "lake-wall-art.html": "scene",
                 "mountain-wall-art.html": "scene", "coastal-wall-art.html": "scene",
                 "moon-poster-bedroom.html": "room", "peel-and-stick-wall-murals.html": "room",
                 "european-wall-art.html": "region"}
R = {r["key"]: r for r in REGIONS}
S = {s["key"]: s for s in SCENES}

# slug: (region, country, place, scenes) -- the initial 80. Later pieces: auto_tag(), then review.
SEED = {
    "moonlit-alpine-meadow": ("imagined", None, "An imagined alpine valley", ["mountains", "countryside"]),
    "moonlit-mediterranean-village": ("imagined", None, "An imagined Mediterranean lake village", ["lakes", "villages"]),
    "snowy-peaks-above-clouds": ("imagined", None, "Imagined peaks above the clouds", ["mountains"]),
    "coastal-cliffside-town": ("imagined", None, "An imagined cliffside town", ["coastal", "villages"]),
    "lakeside-cabin": ("imagined", None, "An imagined lakeside cabin", ["lakes", "countryside"]),
    "hilltop-path-village": ("imagined", None, "An imagined hilltop village", ["villages", "countryside"]),
    "moonlit-waterfall": ("imagined", None, "An imagined gorge waterfall", ["waterfalls", "lakes"]),
    "wildflower-meadow-cabin": ("imagined", None, "An imagined mountain meadow", ["countryside"]),
    "northern-lights-fjord": ("nordic", "Norway", "A Norwegian fjord", ["coastal"]),
    "mediterranean-lantern-walk": ("imagined", None, "An imagined Mediterranean seaside walk", ["coastal", "villages"]),
    "moonlit-rice-terraces": ("asia", None, "Asian rice terraces", ["countryside"]),
    "venetian-canal-moonrise": ("southern-europe", "Italy", "Venice", ["canals-bridges", "villages"]),
    "japanese-temple-pond": ("asia", "Japan", "A Japanese temple garden", ["temples", "lakes"]),
    "moroccan-kasbah-night": ("africa-middle-east", "Morocco", "A Saharan kasbah oasis", ["deserts", "villages"]),
    "scottish-highlands-loch": ("british-isles", "Scotland", "Scottish Highlands", ["lakes", "mountains", "castles"]),
    "provence-lavender-moon": ("western-europe", "France", "Provence", ["countryside"]),
    "amalfi-terrace-night": ("southern-europe", "Italy", "Amalfi Coast", ["coastal", "villages"]),
    "patagonia-lake-peaks": ("south-america", "Chile & Argentina", "Patagonia", ["lakes", "mountains"]),
    "bali-jungle-temple": ("asia", "Indonesia", "Bali", ["temples", "countryside"]),
    "iceland-black-sand-moon": ("nordic", "Iceland", "South Iceland black sand beach", ["coastal"]),
    "cappadocia-fairy-chimneys": ("africa-middle-east", "Turkey", "Cappadocia", ["deserts", "temples"]),
    "santorini-caldera-moon": ("southern-europe", "Greece", "Santorini", ["coastal", "villages"]),
    "tuscany-cypress-hills": ("southern-europe", "Italy", "Tuscany", ["countryside"]),
    "machu-picchu-mist": ("south-america", "Peru", "Machu Picchu", ["temples", "mountains"]),
    "ha-long-bay-moon": ("asia", "Vietnam", "Ha Long Bay", ["coastal"]),
    "banff-lake-louise-moon": ("north-america", "Canada", "Lake Louise, Banff", ["lakes", "mountains"]),
    "petra-treasury-night": ("africa-middle-east", "Jordan", "Petra", ["temples", "deserts"]),
    "kyoto-bamboo-moon": ("asia", "Japan", "Arashiyama, Kyoto", ["countryside"]),
    "yosemite-half-dome-moon": ("north-america", "USA", "Yosemite, California", ["mountains"]),
    "norwegian-stave-church-fjord": ("nordic", "Norway", "A Norwegian fjord", ["coastal"]),
    "mont-saint-michel-moon": ("western-europe", "France", "Normandy", ["coastal", "castles"]),
    "hallstatt-lake-moon": ("alps", "Austria", "Hallstatt", ["lakes", "villages"]),
    "zhangjiajie-pillars-moon": ("asia", "China", "Zhangjiajie", ["mountains"]),
    "bagan-temples-night": ("asia", "Myanmar", "Bagan", ["temples"]),
    "matterhorn-alpine-moon": ("alps", "Switzerland", "Zermatt", ["mountains"]),
    "chefchaouen-blue-moon": ("africa-middle-east", "Morocco", "Chefchaouen", ["villages"]),
    "plitvice-lakes-moon": ("southern-europe", "Croatia", "Plitvice Lakes", ["waterfalls", "lakes"]),
    "neuschwanstein-castle-moon": ("alps", "Germany", "Bavarian Alps", ["castles"]),
    "angkor-wat-moon": ("asia", "Cambodia", "Angkor Wat", ["temples"]),
    "faroe-gasadalur-moon": ("nordic", "Faroe Islands", "Gásadalur", ["waterfalls", "coastal", "lakes"]),
    "dolomites-tre-cime-moon": ("alps", "Italy", "Dolomites", ["mountains"]),
    "lofoten-reine-moon": ("nordic", "Norway", "Reine, Lofoten", ["coastal", "villages"]),
    "cinque-terre-manarola-moon": ("southern-europe", "Italy", "Manarola, Cinque Terre", ["coastal", "villages"]),
    "lake-bled-island-moon": ("alps", "Slovenia", "Lake Bled", ["lakes", "castles"]),
    "guilin-li-river-moon": ("asia", "China", "Li River, Guilin", ["countryside"]),
    "meteora-monasteries-moon": ("southern-europe", "Greece", "Meteora", ["temples"]),
    "lauterbrunnen-valley-moon": ("alps", "Switzerland", "Lauterbrunnen", ["waterfalls", "lakes", "mountains", "villages"]),
    "mount-fuji-pagoda-moon": ("asia", "Japan", "Mount Fuji", ["temples", "mountains"]),
    "iguazu-falls-moon": ("south-america", "Argentina & Brazil", "Iguazu Falls", ["waterfalls", "lakes"]),
    "isle-of-skye-storr-moon": ("british-isles", "Scotland", "Isle of Skye", ["mountains"]),
    "sintra-pena-palace-moon": ("southern-europe", "Portugal", "Sintra", ["castles"]),
    "lake-como-bellagio-moon": ("southern-europe", "Italy", "Bellagio, Lake Como", ["lakes", "villages"]),
    "grand-canyon-rim-moon": ("north-america", "USA", "Grand Canyon, Arizona", ["deserts"]),
    "cliffs-of-moher-moon": ("british-isles", "Ireland", "Cliffs of Moher", ["coastal"]),
    "big-sur-bixby-bridge-moon": ("north-america", "USA", "Big Sur, California", ["coastal", "canals-bridges"]),
    "prague-charles-bridge-moon": ("western-europe", "Czech Republic", "Prague", ["canals-bridges", "castles"]),
    "taj-mahal-moon": ("asia", "India", "Agra", ["temples"]),
    "salar-de-uyuni-moon": ("south-america", "Bolivia", "Salar de Uyuni", ["lakes", "deserts"]),
    "victoria-falls-moon": ("africa-middle-east", "Zambia & Zimbabwe", "Victoria Falls", ["waterfalls", "lakes"]),
    "great-wall-mutianyu-moon": ("asia", "China", "Great Wall at Mutianyu", ["temples", "mountains"]),
    "lake-tekapo-church-moon": ("oceania", "New Zealand", "Lake Tekapo", ["lakes", "mountains"]),
    "bruges-canal-moon": ("western-europe", "Belgium", "Bruges", ["canals-bridges", "villages"]),
    "kirkjufell-waterfall-moon": ("nordic", "Iceland", "Kirkjufell, Snæfellsnes", ["waterfalls", "lakes", "mountains"]),
    "bibury-arlington-row-moon": ("british-isles", "England", "Bibury, Cotswolds", ["villages", "countryside"]),
    "na-pali-coast-moon": ("oceania", "Hawaii, USA", "Na Pali Coast, Kauai", ["coastal"]),
    "eilean-donan-castle-moon": ("british-isles", "Scotland", "Eilean Donan", ["castles", "coastal"]),
    "dubrovnik-old-town-moon": ("southern-europe", "Croatia", "Dubrovnik", ["coastal", "castles", "villages"]),
    "pamukkale-terraces-moon": ("africa-middle-east", "Turkey", "Pamukkale", ["lakes", "temples"]),
    "rothenburg-old-town-moon": ("western-europe", "Germany", "Rothenburg ob der Tauber", ["villages"]),
    "bora-bora-lagoon-moon": ("oceania", "French Polynesia", "Bora Bora", ["coastal"]),
    "colmar-petite-venise-moon": ("western-europe", "France", "Colmar, Alsace", ["canals-bridges", "villages"]),
    "glenfinnan-viaduct-moon": ("british-isles", "Scotland", "Glenfinnan", ["canals-bridges"]),
    "monument-valley-moon": ("north-america", "USA", "Monument Valley", ["deserts", "mountains"]),
    "sigiriya-rock-moon": ("asia", "Sri Lanka", "Sigiriya", ["temples"]),
    "cradle-mountain-dove-lake-moon": ("oceania", "Australia", "Cradle Mountain, Tasmania", ["lakes", "mountains"]),
    "skogafoss-waterfall-moon": ("nordic", "Iceland", "Skógafoss", ["waterfalls", "lakes"]),
    "seljalandsfoss-waterfall-moon": ("nordic", "Iceland", "Seljalandsfoss", ["waterfalls", "lakes"]),
    "moraine-lake-moon": ("north-america", "Canada", "Moraine Lake, Banff", ["lakes", "mountains"]),
    "hohenzollern-castle-moon": ("western-europe", "Germany", "Swabian Alb", ["castles"]),
    "havasu-falls-moon": ("north-america", "USA", "Havasu Falls, Arizona", ["waterfalls", "lakes", "deserts"]),
    "ponte-vecchio-florence-moon": ("southern-europe", "Italy", "Florence", ["canals-bridges"]),
}

# Auto-tag rules for new pieces (first match wins for country). Review the printed result.
COUNTRY_RULES = [
    (r"iceland|icelandic|reykjav|skaft|seljaland|jokuls", "Iceland", "nordic"),
    (r"faroe", "Faroe Islands", "nordic"), (r"norw|lofoten|fjord|tromso|bergen", "Norway", "nordic"),
    (r"swed|stockholm|lapland", "Sweden", "nordic"), (r"finland|helsinki", "Finland", "nordic"),
    (r"denmark|copenhagen", "Denmark", "nordic"), (r"greenland", "Greenland", "nordic"),
    (r"scotland|scottish|highland|skye|edinburgh|\bloch\b", "Scotland", "british-isles"),
    (r"ireland|irish|dublin|galway", "Ireland", "british-isles"), (r"wales|welsh|snowdon", "Wales", "british-isles"),
    (r"england|english|cotswold|london|cornwall|lake district|yorkshire", "England", "british-isles"),
    (r"switzerland|swiss|zermatt|lucerne|interlaken|jungfrau", "Switzerland", "alps"),
    (r"austria|austrian|salzburg|tyrol|vienna", "Austria", "alps"), (r"slovenia|\bbled\b", "Slovenia", "alps"),
    (r"dolomit|lake garda", "Italy", "alps"), (r"bavarian alps|konigssee|zugspitze", "Germany", "alps"),
    (r"italy|italian|venice|venetian|\brome\b|florence|tuscan|amalfi|sicily|\bcomo\b|positano|cinque", "Italy", "southern-europe"),
    (r"greece|greek|santorini|athens|mykonos|crete", "Greece", "southern-europe"),
    (r"croatia|dubrovnik|\bhvar\b", "Croatia", "southern-europe"), (r"portugal|lisbon|porto|sintra|algarve", "Portugal", "southern-europe"),
    (r"spain|spanish|seville|granada|barcelona|andalus|mallorca", "Spain", "southern-europe"),
    (r"montenegro|kotor", "Montenegro", "southern-europe"), (r"\bmalta\b", "Malta", "southern-europe"),
    (r"france|french|paris|provence|alsace|normandy|loire|brittany", "France", "western-europe"),
    (r"belgi|bruges|ghent", "Belgium", "western-europe"), (r"netherland|dutch|amsterdam|holland", "Netherlands", "western-europe"),
    (r"german|bavaria|berlin|rhine|black forest", "Germany", "western-europe"),
    (r"czech|prague|bohemia", "Czech Republic", "western-europe"), (r"hungar|budapest", "Hungary", "western-europe"),
    (r"poland|polish|krak", "Poland", "western-europe"),
    (r"japan|japanese|kyoto|tokyo|\bfuji|osaka|\bnara\b", "Japan", "asia"), (r"china|chinese|beijing|guilin|yangtze", "China", "asia"),
    (r"vietnam|hanoi|hoi an", "Vietnam", "asia"), (r"thailand|\bthai\b|bangkok|chiang", "Thailand", "asia"),
    (r"\bindia\b|indian|agra|rajasthan|kerala|varanasi", "India", "asia"), (r"nepal|himalaya|everest", "Nepal", "asia"),
    (r"\bbali\b|indonesia", "Indonesia", "asia"), (r"cambodia|angkor", "Cambodia", "asia"), (r"myanmar|bagan", "Myanmar", "asia"),
    (r"sri lanka", "Sri Lanka", "asia"), (r"korea|seoul", "South Korea", "asia"), (r"philippin", "Philippines", "asia"),
    (r"maldiv", "Maldives", "asia"),
    (r"morocc|marrakech|sahara", "Morocco", "africa-middle-east"), (r"egypt|pyramid|\bnile\b|cairo", "Egypt", "africa-middle-east"),
    (r"jordan|petra|wadi rum", "Jordan", "africa-middle-east"), (r"turkey|turkish|istanbul|cappadocia", "Turkey", "africa-middle-east"),
    (r"kenya|tanzania|kilimanjaro|serengeti|safari", "East Africa", "africa-middle-east"),
    (r"namibia|south africa|cape town|botswana|zambia|zimbabwe", "Southern Africa", "africa-middle-east"),
    (r"\boman\b|\buae\b|dubai|israel|jerusalem", "Middle East", "africa-middle-east"),
    (r"hawaii|kauai|\bmaui\b|oahu", "Hawaii, USA", "oceania"),
    (r"canada|canadian|banff|alberta|british columbia|quebec|jasper", "Canada", "north-america"),
    (r"\busa\b|america|arizona|\butah\b|california|colorado|alaska|new york|yellowstone|yosemite|oregon|wyoming|montana|\bmaine\b", "USA", "north-america"),
    (r"mexico|mexican|tulum|oaxaca", "Mexico", "north-america"),
    (r"\bperu|andes|machu", "Peru", "south-america"), (r"chile|atacama|torres del paine", "Chile", "south-america"),
    (r"argentin|patagonia", "Argentina", "south-america"), (r"brazil|rio de", "Brazil", "south-america"),
    (r"bolivia|uyuni", "Bolivia", "south-america"), (r"colombia|ecuador|galapagos", "South America", "south-america"),
    (r"new zealand|tekapo|milford|queenstown", "New Zealand", "oceania"), (r"australia|tasmania|sydney|uluru", "Australia", "oceania"),
    (r"polynesia|bora bora|tahiti|\bfiji|samoa", "South Pacific", "oceania"),
]
SCENE_RULES = [
    ("waterfalls", r"waterfall|\bfalls\b|foss\b|cascade"), ("lakes", r"\blake|\bloch|\bpond|lagoon|\bmere\b"),
    ("mountains", r"mountain|\bpeaks?\b|\balps?\b|alpine|summit|volcano|massif"),
    ("coastal", r"\bcoast|\bsea\b|ocean|\bbeach|harbou?r|\bbay\b|fjord|seaside|\bisland"),
    ("castles", r"castle|palace|fortress|citadel|chateau"),
    ("villages", r"village|old town|\btown\b|cottage|hamlet|street"),
    ("canals-bridges", r"canal|bridge|viaduct|aqueduct"),
    ("temples", r"temple|pagoda|monaster|shrine|stupa|ruins|ancient|mosque|cathedral|abbey"),
    ("countryside", r"meadow|forest|field|countryside|vineyard|bamboo|jungle|lavender|orchard|grove|rice terrace"),
    ("deserts", r"desert|canyon|\bdunes?\b|mesa|butte|salt flat|oasis"),
]

ORDER_REGIONS = [r["key"] for r in REGIONS]
CHANGED: list[str] = []
CHECK = False


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def norm(s: str) -> str:
    s = unicodedata.normalize("NFD", s.lower())
    return "".join(c for c in s if unicodedata.category(c) != "Mn")


def url_for(file: str) -> str:
    return f"{SITE}/" if file == "index.html" else f"{SITE}/{file}"


def write(path: Path, new: str) -> bool:
    old = path.read_text(encoding="utf-8") if path.exists() else None
    if old == new:
        return False
    CHANGED.append(str(path.relative_to(ROOT)))
    if not CHECK:
        path.write_text(new, encoding="utf-8")
    return True


# ------------------------------------------------------------------ tagging
def auto_tag(row: dict, cat: dict) -> dict:
    core = " ".join([row.get("title", ""), cat.get("description", ""), " ".join(cat.get("keywords", []))])
    t = norm(core + " " + (cat.get("alt", "") or "")[:220])
    region, country = "imagined", None
    for rx, c, r in COUNTRY_RULES:
        if re.search(rx, t):
            region, country = r, c
            break
    scenes = [k for k, rx in SCENE_RULES if re.search(rx, norm(core))]
    place = re.sub(r"\s+Moon$", "", row.get("title", ""))
    return {"region": region, "country": country, "place": place, "scenes": scenes or ["countryside"], "auto": True}


def tag_products(products: list, catalog: dict) -> list[str]:
    notes = []
    for row in products:
        if isinstance(row.get("categories"), dict) and row["categories"].get("region"):
            continue
        if row["slug"] in SEED:
            reg, country, place, scenes = SEED[row["slug"]]
            row["categories"] = {"region": reg, "country": country, "place": place, "scenes": scenes}
        else:
            row["categories"] = auto_tag(row, catalog.get(row["slug"], {}))
            notes.append(f"AUTO-TAGGED {row['slug']}: {row['categories']}  (review; edit products.json to correct)")
    return notes


# ------------------------------------------------------------------ shared HTML
def nav_html(p: str) -> str:
    reg = "\n".join(f'              <a href="{p}{r["file"]}">{esc(r["label"])}</a>' for r in REGIONS)
    sce = "\n".join(f'              <a href="{p}{s["file"]}">{esc(s["label"])}</a>' for s in SCENES)
    room = "\n".join(f'              <a href="{p}{r["file"]}">{esc(r["label"])}</a>' for r in ROOMS[:2])
    return f'''<nav class="nav" aria-label="Primary" data-nav="cats">
        <a href="{p}#gallery">Gallery</a>
        <details class="nav-browse">
          <summary>Categories</summary>
          <div class="nav-menu">
            <div class="nav-col"><p class="nav-head">By region</p>
{reg}
            </div>
            <div class="nav-col"><p class="nav-head">By scene</p>
{sce}
            </div>
            <div class="nav-col"><p class="nav-head">By room</p>
{room}
              <a class="nav-all" href="{p}{HUB}">All categories &amp; search</a>
            </div>
          </div>
        </details>
        <a href="{p}night-windows.html">The series</a>
        <a href="{p}buy.html">Shop Posters, Prints &amp; Wall Murals</a>
        <a href="{p}guide-print-sizes.html">Print sizes</a>
        <a href="{p}how-it-works.html">How it works</a>
        <a href="{p}about.html">About</a>
        <a href="{p}contact.html">Contact</a>
        <a href="https://www.instagram.com/moonnightshadeart/" rel="me">@moonnightshadeart</a>
        <script>document.addEventListener("click",function(e){{document.querySelectorAll("details.nav-browse[open]").forEach(function(d){{if(!d.contains(e.target))d.removeAttribute("open")}})}});document.addEventListener("keydown",function(e){{if(e.key==="Escape")document.querySelectorAll("details.nav-browse[open]").forEach(function(d){{d.removeAttribute("open")}})}});</script>
      </nav>'''


NAV_RE = re.compile(r'<nav class="nav"[^>]*>.*?</nav>', re.S)


def inject_nav(t: str, p: str) -> str:
    return NAV_RE.sub(lambda m: nav_html(p), t, count=1)


CSS_START, CSS_END = "/* cats:start (scripts/build_categories.py) */", "/* cats:end */"
CSS_BLOCK = CSS_START + """
.nav { align-items: center; }
.nav-browse { position: relative; }
.nav-browse > summary { list-style: none; cursor: pointer; color: var(--muted); min-height: 44px; display: inline-flex; align-items: center; gap: 0.3rem; }
.nav-browse > summary::-webkit-details-marker { display: none; }
.nav-browse > summary::after { content: "\\25BE"; font-size: 0.8em; }
.nav-browse[open] > summary, .nav-browse > summary:hover { color: var(--ink); }
.nav-menu { position: absolute; left: 0; top: 100%; z-index: 40; width: min(44rem, calc(100vw - 2rem)); display: grid; grid-template-columns: repeat(3, minmax(0, 1fr)); gap: 0.4rem 1.2rem; padding: 1rem 1.1rem; background: var(--bg-elev); border: 1px solid var(--line); border-radius: 14px; box-shadow: 0 18px 40px rgba(0,0,0,0.45); }
.nav-menu .nav-col { display: flex; flex-direction: column; }
.nav-menu .nav-head { margin: 0 0 0.25rem; font-size: 0.72rem; letter-spacing: 0.16em; text-transform: uppercase; color: var(--accent); }
.nav .nav-menu a { min-height: 34px; font-size: 0.93rem; }
.nav .nav-menu a.nav-all { color: var(--accent); margin-top: 0.4rem; }
@media (max-width: 900px) {
  .nav-browse { width: 100%; order: -1; }
  .nav-menu { position: static; width: 100%; box-shadow: none; margin: 0.2rem 0 0.6rem; grid-template-columns: repeat(2, minmax(0, 1fr)); padding: 0.8rem; }
  .nav-menu .nav-col:last-child { grid-column: 1 / -1; }
}
@media (max-width: 360px) { .nav-menu { grid-template-columns: 1fr; } }
.breadcrumb a { color: var(--muted); }
.cat-tree { display: grid; grid-template-columns: repeat(auto-fit, minmax(min(100%, 17rem), 1fr)); gap: 1rem; margin: 1rem 0 2rem; }
.cat-box { background: rgba(18, 24, 38, 0.92); border: 1px solid var(--line); border-radius: var(--radius); padding: 1rem 1.2rem; }
.cat-box h2 { font-size: 1.5rem; margin: 0 0 0.5rem; }
.cat-box h3 { font-size: 0.78rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--dim); margin: 0.7rem 0 0.2rem; font-family: var(--sans); }
.cat-box ul { list-style: none; margin: 0; padding: 0; }
.cat-box li { display: flex; justify-content: space-between; gap: 0.6rem; padding: 0.28rem 0; border-bottom: 1px dashed var(--line); }
.cat-box li span { color: var(--dim); font-size: 0.9rem; }
.filter-bar { background: rgba(7, 11, 20, 0.94); padding: 0.8rem 0; border-bottom: 1px solid var(--line); }
.filter-bar input[type=search] { width: 100%; font: inherit; color: var(--ink); background: var(--bg-elev); border: 1px solid var(--line); border-radius: 999px; padding: 0.65rem 1rem; }
.chips { display: flex; flex-wrap: wrap; gap: 0.4rem; margin-top: 0.55rem; }
.chips .chip-label { font-size: 0.75rem; letter-spacing: 0.14em; text-transform: uppercase; color: var(--dim); align-self: center; margin-right: 0.2rem; }
.chip { font: inherit; font-size: 0.88rem; color: var(--muted); background: transparent; border: 1px solid var(--line); border-radius: 999px; padding: 0.3rem 0.75rem; cursor: pointer; min-height: 36px; }
.chip[aria-pressed=true] { color: #1a1408; background: var(--accent); border-color: var(--accent); }
.filter-count { margin: 0.5rem 0 0; color: var(--dim); font-size: 0.9rem; }
.card[hidden] { display: none !important; }
.card .place { color: var(--dim); font-size: 0.92rem; margin: 0.2rem 0 0; }
@media (max-width: 640px) { .chips { flex-wrap: nowrap; overflow-x: auto; padding-bottom: 0.3rem; } .chip { flex: 0 0 auto; } }
""" + CSS_END


def head(title: str, desc: str, url: str, og_img: str, og_alt: str, lds: list, p: str = "./") -> str:
    T, D = esc(title), esc(desc)
    ld = "\n".join(f'  <script type="application/ld+json" data-ld="{k}">\n{v}\n  </script>' for k, v in lds)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <!-- Google tag (gtag.js) -->
  <script async src="https://www.googletagmanager.com/gtag/js?id={GA_ID}"></script>
  <script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{GA_ID}');</script>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{T}</title>
  <meta name="description" content="{D}" />
  <meta name="robots" content="index, follow" />
  <link rel="canonical" href="{url}">
  <meta property="og:site_name" content="Moonlit Windows" />
  <meta property="og:type" content="website" />
  <meta property="og:title" content="{T}" />
  <meta property="og:description" content="{D}" />
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{og_img}" />
  <meta property="og:image:alt" content="{esc(og_alt)}" />
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="{T}" />
  <meta name="twitter:description" content="{D}" />
  <meta name="twitter:image" content="{og_img}" />
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,560&family=Outfit:wght@380;560;650&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{p}styles.css">
{ld}
</head>'''


def header(p: str = "./") -> str:
    return f'''  <div class="wrap">
    <header class="site-header">
      <a class="brand" href="{p}"><span class="brand-series">Night Windows</span><span class="brand-studio">Prompt Framed</span></a>
      {nav_html(p)}
    </header>'''


def footer(p: str = "./") -> str:
    reg = " · ".join(f'<a href="{p}{r["file"]}">{esc(r["label"])}</a>' for r in REGIONS)
    sce = " · ".join(f'<a href="{p}{s["file"]}">{esc(s["label"])}</a>' for s in SCENES)
    return f'''  <footer class="site-footer">
    <div class="wrap"><div class="footer-shop"><a href="{p}buy.html">Shop Posters, Prints &amp; Wall Murals</a> · $35 poster · $69 framed · 12×18 · shipping included</div>
      <div><a href="{p}{HUB}">Shop by category</a> · By region: {reg}</div>
      <div>By scene: {sce} · <a href="{p}peel-and-stick-wall-murals.html">Peel and stick wall murals</a> · Night Shade Art on Instagram: <a href="https://www.instagram.com/moonnightshadeart/" rel="me">@moonnightshadeart</a></div>
    </div>
    <div class="operated-by footer-legal"><p>© 2026 Joshua Israel Ventures LLC. All rights reserved. Moonlit Windows is owned and operated by Joshua Israel Ventures LLC.</p><p class="footer-legal-links"><a href="{p}terms.html">Terms</a> · <a href="{p}privacy.html">Privacy</a> · <a href="{p}disclaimer.html">Disclaimer</a> · <a href="{p}contact.html">Contact</a></p></div>
  </footer>
{CF}
</body>
</html>
'''


PUBLISHER = {"@type": "Organization", "@id": SITE + "/#org", "name": "Joshua Israel Ventures LLC", "url": SITE + "/",
             "legalName": "Joshua Israel Ventures LLC",
             "brand": {"@type": "Brand", "name": "Moonlit Windows", "alternateName": ["Night Shade Art", "Night Windows", "Prompt Framed"]}}


def crumbs_ld(items: list) -> dict:
    return {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": u} for i, (n, u) in enumerate(items)]}


def blurbs() -> dict:
    b = (ROOT / "buy.html").read_text(encoding="utf-8")
    out = {}
    for m in re.finditer(r'<article class="(card[^"]*)" id="([^"]+)">.*?\.jpg (\d+)w".*?<h2>.*?</h2>\s*<p>(.*?)</p>', b, re.S):
        out[m.group(2)] = (m.group(1), m.group(3), m.group(4))
    return out


def short_alt(cat: dict, row: dict) -> str:
    a = (cat.get("alt") or row["title"]).strip()
    if len(a) > 150:
        cut = a[:150].rsplit(",", 1)[0]
        a = cut if len(cut) > 60 else a[:150].rsplit(" ", 1)[0]
    return a


def is_live(st: dict) -> bool:
    return st.get("status") == "live" and all(str(st.get(k) or "").startswith("https://buy.stripe.com/")
                                              for k in ("posterUrl", "framedUrl", "muralUrl"))


def place_line(c: dict) -> str:
    bits = [c.get("place") or ""]
    if c.get("country") and c["country"] not in (c.get("place") or ""):
        bits.append(c["country"])
    return ", ".join(b for b in bits if b)


def buy_card(row: dict, cat: dict, bl: dict, suffix: str, p: str = "./") -> str:
    cls, w, blurb = bl.get(row["slug"], ("card", "1024", esc(cat.get("description", ""))))
    s, t, st, a = row["slug"], esc(row["title"]), row.get("stripe", {}), row["asset"]
    alt = esc(f"{short_alt(cat, row)}, {row['title']} {suffix}")
    img = (f'<a href="{p}pieces/{s}.html"><img src="{p}assets/thumbs/{a}" srcset="{p}assets/thumbs/{a} 600w, {p}assets/{a} {w}w" '
           f'sizes="(max-width: 640px) 92vw, (max-width: 1100px) 45vw, 22rem" decoding="async" alt="{alt}" loading="lazy"></a>')
    pl = esc(place_line(row["categories"]))
    if is_live(st):
        buy = f'''          <div class="actions buy-actions">
            <a class="btn" data-buy="{s}" data-sku="poster" href="{st['posterUrl']}">Poster · $35</a>
            <a class="btn secondary" data-buy="{s}" data-sku="framed" href="{st['framedUrl']}">Framed · $69</a>
            <a class="btn secondary" data-buy="{s}" data-sku="mural" href="{st['muralUrl']}">Wall mural · $149</a>
          </div>'''
    else:
        buy = '          <p class="note">This window opens for orders soon.</p>'
    return f'''      <article class="{cls}" id="{s}">
        {img}
        <div class="meta">
          <h3><a href="{p}pieces/{s}.html">{t}</a></h3>
          <p class="place">{pl}</p>
          <p>{blurb}</p>
          <p class="price-line">$35 poster · $69 framed (12×18) · $149 peel &amp; stick wall mural (4×6 ft)</p>
{buy}
        </div>
      </article>'''


def members(products, kind, key):
    if kind == "region":
        return [r for r in products if r["categories"]["region"] == key]
    return [r for r in products if key in r["categories"]["scenes"]]


def cat_page(kind: str, sub: dict, products, catalog, bl, counts) -> str:
    items = members(products, kind, sub["key"])
    n = len(items)
    url = url_for(sub["file"])
    desc = sub["desc"].format(n=n)
    by, anchor = ("By region", "by-region") if kind == "region" else ("By scene", "by-scene")
    suffix = "wall art poster and framed print"
    groups = []
    if kind == "region":
        label_of = lambda r: r["categories"].get("country") or ("Imagined places" if sub["key"] == "imagined" else sub["label"])
        order = []
        for r in items:
            if label_of(r) not in order:
                order.append(label_of(r))
        if len(order) > 1:
            first = list(order)
            order.sort(key=lambda c: (-sum(1 for r in items if label_of(r) == c), first.index(c)))
            groups = [(c, [r for r in items if label_of(r) == c]) for c in order]
        else:
            groups = [("", items)]
    else:
        for rk in ORDER_REGIONS:
            g = [r for r in items if r["categories"]["region"] == rk]
            if g:
                groups.append((R[rk]["label"], g))
    sections = []
    for gl, g in groups:
        cards = "\n".join(buy_card(r, catalog.get(r["slug"], {}), bl, suffix) for r in g)
        gid = re.sub(r"[^a-z0-9]+", "-", norm(gl)).strip("-")
        h = f'    <h2 id="{gid}">{esc(gl)} <span class="note">({len(g)})</span></h2>\n' if gl else ""
        sections.append(f'''{h}    <section class="grid" aria-label="{esc(gl or sub['label'])}">
{cards}
    </section>''')
    ordered = [x for _, g in groups for x in g]
    og_row = next((r for r in items if r["slug"] == sub.get("og")), items[0])
    og = f"{SITE}/assets/{og_row['asset']}"
    sibl = REGIONS if kind == "region" else SCENES
    other = SCENES if kind == "region" else REGIONS
    okind = "scene" if kind == "region" else "region"
    sib = " · ".join(f'<a href="./{x["file"]}">{esc(x["label"])}</a> ({counts[kind][x["key"]]})' for x in sibl if x["key"] != sub["key"])
    cross_keys = set()
    for r in items:
        cross_keys.update(r["categories"]["scenes"] if kind == "region" else [r["categories"]["region"]])
    cross = " · ".join(f'<a href="./{x["file"]}">{esc(x["label"])}</a>' for x in other if x["key"] in cross_keys)
    search_q = f"./{HUB}?{kind}={sub['key']}#all"
    ld_main = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": html.unescape(sub["h1"]), "url": url, "description": desc,
         "isPartOf": {"@type": "WebSite", "name": "Moonlit Windows", "url": SITE + "/"}, "publisher": PUBLISHER,
         "mainEntity": {"@type": "ItemList", "numberOfItems": n, "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": f"{r['title']} poster & framed print",
              "url": f"{SITE}/pieces/{r['slug']}.html"} for i, r in enumerate(ordered)]}},
        crumbs_ld([("Home", SITE + "/"), ("Shop by category", f"{SITE}/{HUB}"), (sub["label"], url)])]}
    intro1, intro2 = sub["intro"]
    return f'''{head(sub["title"], desc, url, og, f"{og_row['title']} {suffix}", [(f"category-{sub['key']}", json.dumps(ld_main, ensure_ascii=False, indent=2))])}
<body data-products="products.json" data-category="{kind}:{sub['key']}">
{header()}
    <p class="note breadcrumb"><a href="./">Home</a> › <a href="./{HUB}">Shop by category</a> › <a href="./{HUB}#{anchor}">{by}</a> › {esc(sub["label"])}</p>
    <section class="hero left">
      <div class="kicker">Shop by category · {by.lower()}</div>
      <h1>{sub["h1"]}</h1>
      <p class="sale-line">{n} moonlit art prints · $35 poster · $69 framed · 12×18 · $149 peel &amp; stick wall mural (4×6 ft) · shipping included</p>
      <p class="answer-first">{esc(intro1)} {esc(PRICE_SENT)}</p>
      <p>{esc(intro2)}</p>
      <p class="note"><a href="{search_q}">Search and filter {esc(sub["label"])}</a> · Also by {okind}: {cross}</p>
    </section>

{chr(10).join(sections)}

    <section class="prose">
      <h2>More ways to browse</h2>
      <p><strong>{"Other regions" if kind == "region" else "Other scenes"}:</strong> {sib}.</p>
      <p><strong>By room:</strong> <a href="./moon-poster-bedroom.html">moon posters for the bedroom</a> · <a href="./peel-and-stick-wall-murals.html">peel and stick wall murals for a feature wall</a> · <a href="./guide-print-sizes.html">print size guide</a>.</p>
      <p>See every category with counts and a search box on the <a href="./{HUB}">Shop by category</a> page, or browse <a href="./night-windows.html">the whole Night Windows series</a>.</p>
    </section>
  </div>
{footer()}'''


HUB_JS = r'''  <script>
(function () {
  var q = document.getElementById("f-q"), grid = document.getElementById("all-pieces");
  var cards = [].slice.call(grid.querySelectorAll(".card")), chips = [].slice.call(document.querySelectorAll(".chip[data-group]"));
  var count = document.getElementById("f-count"), empty = document.getElementById("f-empty"), st = { region: "", scene: "" };
  function norm(s) { return (s || "").toLowerCase().normalize("NFD").replace(/[\u0300-\u036f]/g, ""); }
  function apply(save) {
    var words = norm(q.value).trim().split(/\s+/).filter(Boolean), n = 0;
    cards.forEach(function (c) {
      var ok = (!st.region || c.getAttribute("data-region") === st.region) &&
               (!st.scene || (" " + c.getAttribute("data-scenes") + " ").indexOf(" " + st.scene + " ") > -1);
      if (ok && words.length) { var h = c.getAttribute("data-text"); ok = words.every(function (w) { return h.indexOf(w) > -1; }); }
      c.hidden = !ok; if (ok) n++;
    });
    chips.forEach(function (b) { b.setAttribute("aria-pressed", st[b.getAttribute("data-group")] === b.getAttribute("data-value") ? "true" : "false"); });
    count.textContent = "Showing " + n + " of " + cards.length + " pieces";
    empty.hidden = n > 0;
    if (save && window.history && history.replaceState) {
      var u = new URLSearchParams();
      if (q.value.trim()) u.set("q", q.value.trim());
      if (st.region) u.set("region", st.region);
      if (st.scene) u.set("scene", st.scene);
      var s = u.toString();
      history.replaceState(null, "", location.pathname + (s ? "?" + s : "") + location.hash);
    }
  }
  chips.forEach(function (b) {
    b.addEventListener("click", function () {
      var g = b.getAttribute("data-group"), v = b.getAttribute("data-value");
      st[g] = st[g] === v ? "" : v; apply(true);
    });
  });
  q.addEventListener("input", function () { apply(true); });
  document.getElementById("f-reset").addEventListener("click", function () { q.value = ""; st.region = ""; st.scene = ""; apply(true); });
  var p = new URLSearchParams(location.search);
  q.value = p.get("q") || ""; st.region = p.get("region") || ""; st.scene = p.get("scene") || "";
  apply(false);
})();
  </script>'''


def hub_page(products, catalog, bl, counts) -> str:
    n = len(products)
    url = f"{SITE}/{HUB}"
    title = "Shop Wall Art by Category: Region, Scene & Room | Moonlit Windows"
    desc = (f"Browse all {n} Night Windows moonlit prints by region, scene and room, or search by place. "
            "Posters $35, framed $69, wall murals $149, shipping included.")
    assert len(desc) <= 155, f"hub description {len(desc)} chars"
    eu = [r for r in REGIONS if r.get("europe")]
    non_eu = [r for r in REGIONS if not r.get("europe")]
    li = lambda x, c: f'          <li><a href="./{x["file"]}">{esc(x["label"])}</a><span>{c}</span></li>'
    eu_total = sum(counts["region"][r["key"]] for r in eu)
    region_box = f'''      <div class="cat-box" id="by-region">
        <h2>By region</h2>
        <h3>Europe ({eu_total}) · <a href="./european-wall-art.html">highlights</a></h3>
        <ul>
{chr(10).join(li(r, counts["region"][r["key"]]) for r in eu)}
        </ul>
        <h3>Rest of the world</h3>
        <ul>
{chr(10).join(li(r, counts["region"][r["key"]]) for r in non_eu)}
        </ul>
      </div>'''
    scene_box = f'''      <div class="cat-box" id="by-scene">
        <h2>By scene</h2>
        <ul>
{chr(10).join(li(s, counts["scene"][s["key"]]) for s in SCENES)}
        </ul>
      </div>'''
    room_box = f'''      <div class="cat-box" id="by-room">
        <h2>By room &amp; format</h2>
        <ul>
{chr(10).join(li(r, counts["room"][r["file"]]) for r in ROOMS)}
        </ul>
        <h3>Help choosing</h3>
        <ul>
          <li><a href="./guide-print-sizes.html">Print size guide</a><span>12×18 · 4×6 ft</span></li>
          <li><a href="./how-it-works.html">How ordering works</a><span>Stripe</span></li>
        </ul>
      </div>'''
    chips_r = "\n".join(f'        <button type="button" class="chip" data-group="region" data-value="{r["key"]}" aria-pressed="false">{esc(r["label"])} ({counts["region"][r["key"]]})</button>' for r in REGIONS)
    chips_s = "\n".join(f'        <button type="button" class="chip" data-group="scene" data-value="{s["key"]}" aria-pressed="false">{esc(s["label"])} ({counts["scene"][s["key"]]})</button>' for s in SCENES)
    cards = []
    for row in sorted(products, key=lambda r: (ORDER_REGIONS.index(r["categories"]["region"]), r.get("photoNumber", 0))):
        c = row["categories"]
        cat = catalog.get(row["slug"], {})
        cls, w, blurb = bl.get(row["slug"], ("card", "1024", ""))
        s, a = row["slug"], row["asset"]
        text = norm(" ".join([row["title"], c.get("place") or "", c.get("country") or "", R[c["region"]]["label"],
                              " ".join(S[k]["label"] for k in c["scenes"]), "europe" if R[c["region"]].get("europe") else "",
                              " ".join(cat.get("keywords", [])), html.unescape(re.sub("<[^>]+>", "", blurb))]))
        text = re.sub(r"\s+", " ", text.replace('"', ""))
        cards.append(f'''      <article class="{cls}" data-region="{c["region"]}" data-scenes="{" ".join(c["scenes"])}" data-text="{esc(text)}">
        <a href="./pieces/{s}.html"><img src="./assets/thumbs/{a}" srcset="./assets/thumbs/{a} 600w, ./assets/{a} {w}w" sizes="(max-width: 640px) 92vw, (max-width: 1100px) 45vw, 22rem" decoding="async" loading="lazy" alt="{esc(short_alt(cat, row))}, {esc(row["title"])} wall art print"></a>
        <div class="meta">
          <h3><a href="./pieces/{s}.html">{esc(row["title"])}</a></h3>
          <p class="place">{esc(place_line(c))} · <a href="./{R[c["region"]]["file"]}">{esc(R[c["region"]]["label"])}</a></p>
          <p class="price-line">$35 poster · $69 framed · $149 mural</p>
        </div>
      </article>''')
    ld = {"@context": "https://schema.org", "@graph": [
        {"@type": "CollectionPage", "name": "Shop Night Windows wall art by category", "url": url, "description": desc,
         "isPartOf": {"@type": "WebSite", "name": "Moonlit Windows", "url": SITE + "/"}, "publisher": PUBLISHER,
         "hasPart": [{"@type": "CollectionPage", "name": f"{x['label']} wall art", "url": url_for(x["file"])} for x in REGIONS + SCENES],
         "mainEntity": {"@type": "ItemList", "numberOfItems": n, "itemListElement": [
             {"@type": "ListItem", "position": i + 1, "name": r["title"], "url": f"{SITE}/pieces/{r['slug']}.html"}
             for i, r in enumerate(sorted(products, key=lambda r: r.get("photoNumber", 0)))]}},
        crumbs_ld([("Home", SITE + "/"), ("Shop by category", url)])]}
    return f'''{head(title, desc, url, f"{SITE}/assets/night-windows-contact-sheet.jpg", "The Night Windows series of moonlit landscape wall art prints", [("browse-hub", json.dumps(ld, ensure_ascii=False, indent=2))])}
<body data-products="products.json">
{header()}
    <p class="note breadcrumb"><a href="./">Home</a> › Shop by category</p>
    <section class="hero left">
      <div class="kicker">Shop by category</div>
      <h1>Shop Night Windows Wall Art by Region, Scene and Room</h1>
      <p class="sale-line">{n} moonlit art prints · $35 poster · $69 framed · 12×18 · $149 peel &amp; stick wall mural (4×6 ft) · shipping included</p>
      <p class="answer-first">All {n} Night Windows pieces, sorted so you can find a place quickly: by region (from Iceland and the Alps to Asia, the national parks of the USA and Canada, and the South Pacific), by scene (waterfalls, lakes, mountains, coasts, castles, old towns, bridges, temples, countryside and deserts) or by room. {esc(PRICE_SENT)}</p>
      <p>Know what you want? Type a place, a country or a mood in the search box, or tap a chip to filter. <a href="#all">Jump to search</a></p>
    </section>

    <section class="cat-tree" aria-label="Categories">
{region_box}
{scene_box}
{room_box}
    </section>

    <h2 id="all">Search all {n} pieces</h2>
    <div class="filter-bar" role="search">
      <label class="note" for="f-q">Search by place, country or scene</label>
      <input id="f-q" type="search" placeholder="Try Iceland, castle, Italy, waterfall, Japan…" autocomplete="off">
      <div class="chips" aria-label="Filter by region"><span class="chip-label">Region</span>
{chips_r}
      </div>
      <div class="chips" aria-label="Filter by scene"><span class="chip-label">Scene</span>
{chips_s}
      </div>
      <p class="filter-count"><span id="f-count" aria-live="polite">Showing {n} of {n} pieces</span> · <button type="button" class="chip" id="f-reset">Clear filters</button></p>
    </div>
    <p class="note" id="f-empty" hidden>No pieces match that yet. Try a country or a broader word, or <a href="./contact.html">tell us the place you would like to see painted</a>.</p>
    <section class="grid" id="all-pieces" aria-label="All Night Windows pieces">
{chr(10).join(cards)}
    </section>
  </div>
{HUB_JS}
{footer()}'''


# ------------------------------------------------------------------ piece pages
CRUMB_S, CRUMB_E = "<!-- cats:crumb:start -->", "<!-- cats:crumb:end -->"
LINKS_S, LINKS_E = "<!-- cats:links:start -->", "<!-- cats:links:end -->"
LD_RE = re.compile(r'(<script type="application/ld\+json"[^>]*>\n)(.*?)(\n  </script>)', re.S)


def patch_piece(t: str, row: dict) -> str:
    c = row["categories"]
    reg = R[c["region"]]
    s, title = row["slug"], row["title"]
    crumb = (f'{CRUMB_S}<p class="note breadcrumb"><a href="../">Home</a> › <a href="../{HUB}">Shop by category</a> › '
             f'<a href="../{reg["file"]}">{esc(reg["label"])}</a> › {esc(title)}</p>{CRUMB_E}')
    t = re.sub(r"\n\s*" + re.escape(CRUMB_S) + r".*?" + re.escape(CRUMB_E), "", t, flags=re.S)
    t = t.replace("</header>", "</header>\n    " + crumb, 1)
    scenes = " · ".join(f'<a href="../{S[k]["file"]}">{esc(S[k]["label"])}</a>' for k in c["scenes"])
    country = c.get("country") or ""
    more = (f' · <a href="../{HUB}?q={urllib.request.quote(norm(country))}#all">More from {esc(country)}</a>' if country else "")
    links = (f'{LINKS_S}<p class="note cat-links">Browse by category: <a href="../{reg["file"]}">{esc(reg["label"])}</a> · '
             f'{scenes}{more} · <a href="../{HUB}">All categories</a></p>{LINKS_E}')
    t = re.sub(r"\n\s*" + re.escape(LINKS_S) + r".*?" + re.escape(LINKS_E), "", t, flags=re.S)
    if "<!-- buy:end -->" not in t:
        raise SystemExit(f"{s}: no buy:end marker")
    t = t.replace("<!-- buy:end -->", "<!-- buy:end -->\n        " + links, 1)

    def fix_ld(m):
        d = json.loads(m.group(2))
        for g in d.get("@graph", [d]):
            if g.get("@type") == "BreadcrumbList":
                g["itemListElement"] = crumbs_ld([("Home", SITE + "/"), ("Shop by category", f"{SITE}/{HUB}"),
                                                  (reg["label"], url_for(reg["file"])),
                                                  (title, f"{SITE}/pieces/{s}.html")])["itemListElement"]
        return m.group(1) + json.dumps(d, indent=2, ensure_ascii=False) + m.group(3)
    return LD_RE.sub(fix_ld, t)


# ------------------------------------------------------------------ existing collection pages
MORE_S, MORE_E = "<!-- cats:more:start -->", "<!-- cats:more:end -->"


def patch_existing(file: str, t: str, products, catalog, bl) -> str:
    kind = EXISTING_KIND[file]
    by, anchor = {"region": ("By region", "by-region"), "scene": ("By scene", "by-scene"), "room": ("By room", "by-room")}[kind]

    def crumb(m):
        last = m.group(1).rsplit("›", 1)[-1].strip()
        return (f'<p class="note breadcrumb"><a href="./">Home</a> › <a href="./{HUB}">Shop by category</a> › '
                f'<a href="./{HUB}#{anchor}">{by}</a> › {last}</p>')
    t = re.sub(r'<p class="note breadcrumb">(.*?)</p>', crumb, t, count=1, flags=re.S)

    def fix_ld(m):
        d = json.loads(m.group(2))
        for g in d.get("@graph", [d]):
            if g.get("@type") == "BreadcrumbList":
                for it in g["itemListElement"]:
                    if it.get("position") == 2 and it.get("item", "").endswith("/buy.html"):
                        it["name"], it["item"] = "Shop by category", f"{SITE}/{HUB}"
        return m.group(1) + json.dumps(d, indent=2, ensure_ascii=False) + m.group(3)
    t = LD_RE.sub(fix_ld, t)
    t = re.sub(r"\n\s*" + re.escape(MORE_S) + r".*?" + re.escape(MORE_E), "", t, flags=re.S)
    sub = next((x for x in REGIONS + SCENES if x["file"] == file and x.get("existing")), None)
    if sub:
        k = "region" if sub in REGIONS else "scene"
        have = set(re.findall(r'href="\./pieces/([^"]+)\.html"', t))
        missing = [r for r in members(products, k, sub["key"]) if r["slug"] not in have]
        if missing:
            cards = "\n".join(buy_card(r, catalog.get(r["slug"], {}), bl, "wall art poster and framed print") for r in missing)
            block = (f'{MORE_S}\n    <h2 id="new-in-category">New in {esc(sub["label"].lower())}</h2>\n'
                     f'    <section class="grid" aria-label="New in {esc(sub["label"])}">\n{cards}\n    </section>\n    {MORE_E}')
            if '\n    <section class="prose"' in t:
                t = t.replace('\n    <section class="prose"', "\n    " + block + '\n\n    <section class="prose"', 1)
            else:
                t = t.replace("  </div>\n  <footer", "    " + block + "\n  </div>\n  <footer", 1)
    return t


# ------------------------------------------------------------------ sitemap / llms
def update_sitemap(new_files: list, og_by_file: dict, changed_urls: list) -> None:
    xml = SITEMAP.read_text(encoding="utf-8")
    for f in new_files:
        loc = url_for(f)
        if f"<loc>{loc}</loc>" in xml:
            continue
        img = f"<image:image><image:loc>{og_by_file[f]}</image:loc></image:image>" if og_by_file.get(f) else ""
        xml = xml.replace("</urlset>", f"  <url><loc>{loc}</loc><lastmod>{TODAY}</lastmod>{img}</url>\n</urlset>", 1)
    for u in changed_urls:
        xml = re.sub(rf"(<loc>{re.escape(u)}</loc>)(<lastmod>[^<]*</lastmod>)?", rf"\g<1><lastmod>{TODAY}</lastmod>", xml)
    write(SITEMAP, xml)


def update_llms(counts) -> None:
    t = LLMS.read_text(encoding="utf-8")
    lines = ["## Browse by category",
             f"- [Shop by category]({SITE}/{HUB}): Every piece sorted by region, scene and room, with a search box and filter chips"]
    for r in REGIONS:
        lines.append(f"- [{r['label']} wall art]({url_for(r['file'])}): {counts['region'][r['key']]} moonlit pieces (region)")
    for s in SCENES:
        lines.append(f"- [{s['label']} wall art]({url_for(s['file'])}): {counts['scene'][s['key']]} moonlit pieces (scene)")
    block = "\n".join(lines) + "\n\n"
    t = re.sub(r"## Browse by category\n.*?\n\n(?=## )", "", t, flags=re.S)
    t = t.replace("## Representative pieces", block + "## Representative pieces", 1)
    write(LLMS, t)


# ------------------------------------------------------------------ main
def main(argv=None) -> int:
    global CHECK
    argv = sys.argv[1:] if argv is None else argv
    CHECK = "--check" in argv
    CHANGED.clear()
    if "--ping" in argv:
        return ping()
    products = json.loads(PRODUCTS.read_text(encoding="utf-8"))
    catalog = {c["slug"]: c for c in json.loads(CATALOG.read_text(encoding="utf-8"))}
    for note in tag_products(products, catalog):
        print("  " + note)
    write(PRODUCTS, json.dumps(products, indent=2, ensure_ascii=False) + "\n")
    bl = blurbs()
    problems = []
    for row in products:
        c = row["categories"]
        if c["region"] not in R:
            problems.append(f"{row['slug']}: unknown region {c['region']}")
        problems += [f"{row['slug']}: unknown scene {k}" for k in c["scenes"] if k not in S]
    if problems:
        print("\n".join("  ! " + p for p in problems))
        return 1
    counts = {"region": {r["key"]: len(members(products, "region", r["key"])) for r in REGIONS},
              "scene": {s["key"]: len(members(products, "scene", s["key"])) for s in SCENES}, "room": {}}
    for r in ROOMS:
        counts["room"][r["file"]] = len(set(re.findall(r'href="\./pieces/([^"]+)\.html"', (ROOT / r["file"]).read_text(encoding="utf-8"))))

    new_files, og_by_file = [HUB], {HUB: f"{SITE}/assets/night-windows-contact-sheet.jpg"}
    write(ROOT / HUB, hub_page(products, catalog, bl, counts))
    titles = {}
    for kind, subs in (("region", REGIONS), ("scene", SCENES)):
        for sub in subs:
            if sub.get("existing"):
                continue
            if counts[kind][sub["key"]] == 0:
                problems.append(f"{sub['file']}: no pieces")
                continue
            d = sub["desc"].format(n=counts[kind][sub["key"]])
            if len(d) > 155:
                problems.append(f"{sub['file']}: meta description {len(d)} chars > 155")
            if sub["title"] in titles:
                problems.append(f"duplicate title {sub['title']}")
            titles[sub["title"]] = sub["file"]
            write(ROOT / sub["file"], cat_page(kind, sub, products, catalog, bl, counts))
            new_files.append(sub["file"])
            og_row = next((r for r in products if r["slug"] == sub.get("og")), None) or members(products, kind, sub["key"])[0]
            og_by_file[sub["file"]] = f"{SITE}/assets/{og_row['asset']}"
    by_slug = {r["slug"]: r for r in products}
    for f in sorted((ROOT / "pieces").glob("*.html")):
        row = by_slug.get(f.stem)
        t = inject_nav(f.read_text(encoding="utf-8"), "../")
        if row:
            t = patch_piece(t, row)
        write(f, t)
    generated = set(new_files)
    for f in sorted(ROOT.glob("*.html")):
        if f.name in generated:
            continue
        t = inject_nav(f.read_text(encoding="utf-8"), "./")
        if f.name in EXISTING_KIND:
            t = patch_existing(f.name, t, products, catalog, bl)
        write(f, t)
    css = CSS.read_text(encoding="utf-8")
    css = re.sub(r"\n*" + re.escape(CSS_START) + r".*?" + re.escape(CSS_END) + r"\n*", "\n", css, flags=re.S).rstrip("\n")
    write(CSS, css + "\n\n" + CSS_BLOCK + "\n")
    changed_urls = [url_for(rel) for rel in CHANGED if rel.endswith(".html")]
    update_sitemap(new_files, og_by_file, changed_urls)
    update_llms(counts)
    if not CHECK:
        for rel in [c for c in CHANGED if c.endswith(".html")]:
            t = (ROOT / rel).read_text(encoding="utf-8")
            for m in re.finditer(r'<script type="application/ld\+json"[^>]*>(.*?)</script>', t, re.S):
                try:
                    json.loads(m.group(1))
                except Exception as e:
                    problems.append(f"{rel}: bad JSON-LD {e}")
            for need in ("googletagmanager.com/gtag/js?id=" + GA_ID, "static.cloudflareinsights.com/beacon.min.js", 'data-nav="cats"'):
                if need not in t:
                    problems.append(f"{rel}: missing {need}")
            if re.search(r"\bAI\b|ChatGPT|Higgsfield|github\.io", re.sub(r"<script.*?</script>", "", t, flags=re.S)):
                problems.append(f"{rel}: banned word in visible HTML")
    print(f"Category tree ({len(products)} pieces):")
    for r in REGIONS:
        print(f"  region  {r['label']:<36} {counts['region'][r['key']]:>3}  /{r['file']}")
    for s in SCENES:
        print(f"  scene   {s['label']:<36} {counts['scene'][s['key']]:>3}  /{s['file']}")
    for r in ROOMS:
        print(f"  room    {r['label']:<36} {counts['room'][r['file']]:>3}  /{r['file']}")
    print(f"{'Would change' if CHECK else 'Changed'}: {len(CHANGED)} file(s)")
    if not CHECK and CHANGED:
        try:
            old = json.loads(URLS_FILE.read_text()) if URLS_FILE.exists() else []
            urls = sorted(set(old) | set(changed_urls) | {url_for(f) for f in new_files})
            URLS_FILE.write_text(json.dumps(urls, indent=1))
        except Exception as e:
            print(f"  WARN could not save IndexNow list: {e}")
    for p in problems:
        print("  ! " + p)
    if problems:
        return 1
    return 1 if (CHECK and CHANGED) else 0


def ping() -> int:
    urls = json.loads(URLS_FILE.read_text()) if URLS_FILE.exists() else []
    if not urls:
        print("nothing to ping")
        return 0
    probe = f"{SITE}/{HUB}"
    for _ in range(40):
        try:
            if urllib.request.urlopen(urllib.request.Request(probe, headers={"Cache-Control": "no-cache"}), timeout=20).status == 200:
                break
        except Exception:
            pass
        time.sleep(15)
    else:
        print("hub not live after 10 min; not pinged")
        return 1
    r = subprocess.run([sys.executable, str(INDEXNOW), *urls], capture_output=True, text=True)
    print(r.stdout.strip(), r.stderr.strip())
    if re.search(r"IndexNow 20[02]\b", r.stdout):
        URLS_FILE.write_text("[]")
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
