"""One-time asset preparation. Requires Pillow; the viewer only needs pico2d."""

import json
from pathlib import Path

from PIL import Image

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "kyo_original.png"
# Original sheet coordinates (top-left origin). Exclude border boxes and portraits.
STRIPS = {
    "walk": (0, 125, 750, 252),
    "run": (70, 285, 735, 405),
    "jump": (75, 420, 665, 579),
    "attack": (0, 750, 910, 880),
}


def main():
    source = Image.open(SOURCE).convert("RGBA")
    background = source.getpixel((0, 0))[:3]
    source.putdata([
        (r, g, b, 0 if (r, g, b) == background else a)
        for r, g, b, a in source.getdata()
    ])
    clips = {}
    for name, region in STRIPS.items():
        strip = source.crop(region)
        alpha = strip.getchannel("A")
        occupied = [alpha.crop((x, 0, x + 1, strip.height)).getbbox() is not None
                    for x in range(strip.width)]
        spans = []
        start = None
        for x, present in enumerate(occupied + [False]):
            if present and start is None:
                start = x
            elif not present and start is not None:
                spans.append((start, x))
                start = None
        frames = []
        for left, right in spans:
            bounds = alpha.crop((left, 0, right, strip.height)).getbbox()
            top, bottom = bounds[1], bounds[3]
            frames.append((strip.crop((left, top, right, bottom)),
                           [region[0] + left, region[1] + top, right - left, bottom - top]))
        clips[name] = frames

    padding = 4
    width = max(sum(im.width + padding for im, _ in frames) + padding
                for frames in clips.values())
    height = sum(max(im.height for im, _ in frames) + padding
                 for frames in clips.values()) + padding
    atlas = Image.new("RGBA", (width, height))
    metadata = {"source": "https://spritedatabase.net/file/5276", "animations": {}}
    y = padding
    for name, frames in clips.items():
        x = padding
        records = []
        for im, original in frames:
            atlas.paste(im, (x, y))
            records.append({"x": x, "y": y, "w": im.width, "h": im.height,
                            "original": original})
            x += im.width + padding
        metadata["animations"][name] = records
        y += max(im.height for im, _ in frames) + padding
        print(name, len(frames), [(im.width, im.height) for im, _ in frames])
    atlas.save(HERE / "kyo_animation.png")
    (HERE / "kyo_animation.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
