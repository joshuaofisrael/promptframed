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
        base = BLOCK.sub("", h)
        if "<!-- buy:end -->" not in base:
            print("no buy:end marker:", slug); continue
        new = base.replace("<!-- buy:end -->", "<!-- buy:end -->" + render(d), 1)
        if new != h:
            changed.append(slug)
            if not check:
                p.write_text(new)
    print(("would change: " if check else "changed: ") + ", ".join(changed or ["none"]))
    sys.exit(1 if (check and changed) else 0)


if __name__ == "__main__":
    main()
