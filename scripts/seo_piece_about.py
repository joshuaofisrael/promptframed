#!/usr/bin/env python3
"""Add a short, factual "About the place" + "Hanging it" section to piece pages.

Why: Search Console (25 Oct) shows 59 pages "Discovered - currently not indexed";
piece pages were ~425 words with a one-line scene description, so Google sees
little unique value. This adds genuinely useful, place-specific copy (real facts,
what the painting shows, where the 2:3 portrait print hangs well), starting with
pieces that earn impressions or had indexing requested.

Idempotent: content lives between <!-- about:start --> and <!-- about:end -->,
inserted right after <!-- buy:end -->. Re-running replaces the block.
  python3 scripts/seo_piece_about.py --check   # exit 1 if any page would change
  python3 scripts/seo_piece_about.py           # write
"""
import re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

ABOUT = {
    "lauterbrunnen-valley-moon": {
        "h": "About this Lauterbrunnen poster",
        "place": "Lauterbrunnen is a village in the Bernese Oberland in Switzerland, set in a deep glacial valley walled by sheer limestone cliffs and often described as the valley of 72 waterfalls. The best known is Staubbach Falls, which drops roughly 300 metres straight off the cliff behind the village church; it inspired Goethe’s 1779 poem “Song of the Spirits over the Waters”. The car-free villages of Wengen and Mürren sit on the terraces above, with the Jungfrau region beyond.",
        "scene": "This Night Windows piece keeps the classic view: Staubbach Falls pouring off the cliff, the white church steeple and lit chalet windows in the valley, a stream under a stone bridge, wildflowers by a wooden fence, and snowy Alps under a full moon. It is a painted, moonlit reimagining rather than a photograph of one exact viewpoint.",
        "hang": "The artwork is a tall 2:3 portrait, so the 12×18 poster or black-framed print suits a narrow wall, a spot beside the bed or a hallway, and works well in a pair with another alpine piece such as <a href=\"./matterhorn-alpine-moon.html\">Matterhorn Alpine Moon</a>. For a feature wall, the 4×6 ft (48×72 in) peel and stick mural keeps the same portrait shape.",
    },
    "seljalandsfoss-waterfall-moon": {
        "h": "About this Seljalandsfoss poster",
        "place": "Seljalandsfoss is a waterfall in south Iceland, just off the Ring Road (Route 1), where the Seljalandsá river drops about 60 metres over an old sea cliff. It is famous because a footpath runs behind the curtain of water, so you can walk right around the falls; the path can be closed when it is icy in winter.",
        "scene": "This Night Windows piece shows the slender white fall dropping from a dark, moss-covered cliff into a misty pool, a lamplit footpath curving into the rock behind the water, a turf-roofed cottage with warm amber windows by the stream, and wildflowers on the green slopes under a full moon in thin cloud. It is a painted, moonlit reimagining rather than a photograph of one exact viewpoint.",
        "hang": "The artwork is a tall 2:3 portrait, which suits a single falling ribbon of water: hang the 12×18 poster or black-framed print on a narrow wall, beside a bed or in a hallway, or pair it with <a href=\"./skogafoss-waterfall-moon.html\">Skógafoss</a> for an Iceland wall. For a feature wall, the 4×6 ft (48×72 in) peel and stick mural keeps the same portrait shape.",
    },
    "havasu-falls-moon": {
        "h": "About this Havasu Falls poster",
        "place": "Havasu Falls is on Havasu Creek in a side canyon of the Grand Canyon in Arizona, on the land of the Havasupai Tribe. The falls drop about 30 metres (around 100 feet) into blue-green pools; the colour comes from calcium carbonate in the water, which also builds the travertine terraces. Visiting needs an advance permit from the tribe and a long hike in.",
        "scene": "This Night Windows piece shows the white fall plunging from a red rock cliff into a turquoise pool, small cascades spilling over travertine terraces in the foreground, green cottonwoods and towering canyon walls, and a full moon behind thin cloud. It is a painted, moonlit reimagining rather than a photograph of one exact viewpoint.",
        "hang": "The artwork is a tall 2:3 portrait. The 12×18 poster or black-framed print brings colour to a narrow wall, a reading corner or a hallway, and pairs well with <a href=\"./grand-canyon-rim-moon.html\">Grand Canyon Rim Moon</a> or the other <a href=\"../desert-canyon-wall-art.html\">desert and canyon pieces</a>. For a feature wall, the 4×6 ft (48×72 in) peel and stick mural keeps the same portrait shape.",
    },
    "moraine-lake-moon": {
        "h": "About this Moraine Lake poster",
        "place": "Moraine Lake is a glacier-fed lake in the Valley of the Ten Peaks in Banff National Park, Alberta, Canada. Its striking blue comes from rock flour, fine silt ground by glaciers that hangs in the water and reflects light. The view across the lake to the peaks was printed on the back of Canada’s $20 banknote in the 1969 and 1979 series.",
        "scene": "This Night Windows piece shows the jagged, snow-streaked Ten Peaks mirrored in still turquoise water, red canoes at the dock on the far shore, dark spruce and grey boulders in the foreground, and a full moon in thin cloud reflected in the lake. It is a painted, moonlit reimagining rather than a photograph of one exact viewpoint.",
        "hang": "The artwork is a tall 2:3 portrait. The 12×18 poster or black-framed print suits a bedroom, a narrow wall or a hallway, and pairs well with <a href=\"./banff-lake-louise-moon.html\">Banff Lake Louise Moon</a> for a Rockies pair. For a feature wall, the 4×6 ft (48×72 in) peel and stick mural keeps the same portrait shape.",
    },
    "plitvice-lakes-moon": {
        "h": "About this Plitvice Lakes poster",
        "place": "Plitvice Lakes National Park is in central Croatia and is the country’s oldest national park, founded in 1949 and listed as a UNESCO World Heritage Site in 1979. Sixteen named lakes step down a forested valley, joined by cascades and waterfalls; the natural dams between them are travertine, built up over thousands of years as calcium carbonate settles on moss and algae. The tallest fall, Veliki slap, drops about 78 metres, and wooden boardwalks carry visitors right over the water.",
        "scene": "This Night Windows piece shows turquoise pools spilling over terraced falls, a lantern-lit wooden boardwalk crossing the water, steep forested cliffs, and a full moon in a cloudy night sky. It is a painted, moonlit reimagining rather than a photograph of one exact viewpoint.",
        "hang": "The artwork is a tall 2:3 portrait. The 12×18 poster or black-framed print suits a bedroom, a narrow wall or a hallway, and pairs well with <a href=\"./lake-bled-island-moon.html\">Lake Bled Island Moon</a> or the other <a href=\"../waterfall-wall-art.html\">waterfall pieces</a>. For a feature wall, the 4×6 ft (48×72 in) peel and stick mural keeps the same portrait shape.",
    },
    "skogafoss-waterfall-moon": {
        "h": "About this Skógafoss poster",
        "place": "Skógafoss is one of Iceland’s best known waterfalls, on the Skógá river near the village of Skógar on the south coast, just off the Ring Road. The river drops about 60 metres over a former sea cliff in a curtain roughly 25 metres wide, and the spray often throws rainbows on sunny days. A staircase of several hundred steps climbs the slope beside the falls to a viewing platform at the top, where the Fimmvörðuháls hiking trail begins.",
        "scene": "This Night Windows piece shows the broad white curtain pouring over a sheer, moss-covered cliff into rising mist, the staircase path with its railing climbing the slope, the Skógá river running over dark rocks, mossy boulders and white wildflowers in the foreground, and a full moon among thin clouds. It is a painted, moonlit reimagining rather than a photograph of one exact viewpoint.",
        "hang": "The artwork is a tall 2:3 portrait. The 12×18 poster or black-framed print suits a bedroom, a narrow wall or a hallway, and pairs naturally with <a href=\"./seljalandsfoss-waterfall-moon.html\">Seljalandsfoss</a>, its neighbour along the south coast, for an Iceland wall (see the <a href=\"../iceland-nordic-wall-art.html\">Iceland and Nordic pieces</a>). For a feature wall, the 4×6 ft (48×72 in) peel and stick mural keeps the same portrait shape.",
    },
    "iguazu-falls-moon": {
        "h": "About this Iguazu Falls poster",
        "place": "Iguazu Falls is on the Iguazu River, on the border between Argentina and Brazil. Its name comes from the Guaraní words for “big water”. Roughly 275 separate falls spread along nearly 3 kilometres of river, and the most dramatic, the Devil’s Throat (Garganta del Diablo), is a U-shaped chasm about 80 metres deep. The national parks on both sides of the border are UNESCO World Heritage Sites.",
        "scene": "This Night Windows piece shows tier after tier of falls pouring through lush rainforest, mist rising from the gorge, and a full moon above the river. It is a painted, moonlit reimagining rather than a photograph of one exact viewpoint.",
        "hang": "The artwork is a tall 2:3 portrait. The 12×18 poster or black-framed print suits a living room nook, a narrow wall or a hallway, and pairs well with <a href=\"./victoria-falls-moon.html\">Victoria Falls Moon</a> for a pair of the world’s great waterfalls. For a feature wall, the 4×6 ft (48×72 in) peel and stick mural keeps the same portrait shape.",
    },
    "victoria-falls-moon": {
        "h": "About this Victoria Falls poster",
        "place": "Victoria Falls is on the Zambezi River, on the border between Zambia and Zimbabwe. Its local name, Mosi-oa-Tunya, means “the smoke that thunders”, after the spray that rises from the gorge. At about 1,700 metres wide and more than 100 metres high, it is often called the largest single curtain of falling water in the world, and it has been a UNESCO World Heritage Site since 1989. Around the full moon, when the river is high, the moonlight can make a lunar rainbow, or moonbow, in the spray.",
        "scene": "This Night Windows piece shows a wide curtain of white water plunging into a misty gorge lined with green rainforest, a moonbow arcing through the spray, and a full moon behind wispy clouds. It is a painted, moonlit reimagining rather than a photograph of one exact viewpoint.",
        "hang": "The artwork is a tall 2:3 portrait. The 12×18 poster or black-framed print suits a bedroom, a narrow wall or a hallway, and pairs well with <a href=\"./iguazu-falls-moon.html\">Iguazu Falls Moon</a> or the other <a href=\"../africa-middle-east-wall-art.html\">Africa and Middle East pieces</a>. For a feature wall, the 4×6 ft (48×72 in) peel and stick mural keeps the same portrait shape.",
    },

}

BLOCK = re.compile(r"\n?\s*<!-- about:start -->.*?<!-- about:end -->", re.S)


def render(d):
    return (
        "\n        <!-- about:start -->\n"
        '        <section class="piece-about">\n'
        f"          <h2>{d['h']}</h2>\n"
        f"          <p>{d['place']}</p>\n"
        "          <h3>In the painting</h3>\n"
        f"          <p>{d['scene']}</p>\n"
        "          <h3>Where it hangs best</h3>\n"
        f"          <p>{d['hang']}</p>\n"
        "        </section>\n"
        "        <!-- about:end -->"
    ).replace("’", "&rsquo;").replace("“", "&ldquo;").replace("”", "&rdquo;")


def main():
    check = "--check" in sys.argv
    changed = []
    for slug, d in ABOUT.items():
        p = ROOT / "pieces" / f"{slug}.html"
        h = p.read_text()
        if render(d).strip() in h:  # already current (other builders may sit between buy:end and the block)
            continue
        base = BLOCK.sub("", h)
        if "<!-- buy:end -->" not in base:
            print("no buy:end marker:", slug); continue
        new = base.replace("<!-- buy:end -->", "<!-- buy:end -->" + render(d), 1)
        if re.sub(r"\s+", "", new) != re.sub(r"\s+", "", h):  # ignore whitespace-only churn
            changed.append(slug)
            if not check:
                p.write_text(new)
    print(("would change: " if check else "changed: ") + ", ".join(changed or ["none"]))
    sys.exit(1 if (check and changed) else 0)


if __name__ == "__main__":
    main()
