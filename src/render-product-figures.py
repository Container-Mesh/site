#!/usr/bin/env python3
"""Draw sample ContainerMesh windows. These are illustrations, not captured screens."""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

OUT = Path(__file__).resolve().parent / "assets" / "product"
SANS = "/System/Library/Fonts/Supplemental/Avenir Next.ttc"
MONO = "/System/Library/Fonts/Menlo.ttc"

INK = (48, 42, 36)
MUTED = (112, 102, 91)
LINE = (228, 221, 211)
PAPER = (255, 253, 249)
CANVAS = (246, 241, 232)
ROW = (243, 237, 228)
WHITE = (255, 255, 255)
ORANGE = (189, 65, 13)
GREEN = (40, 112, 68)
FIELD = (255, 255, 255)


def face(size, weight="regular", mono=False):
    if mono:
        index = 1 if weight == "bold" else 0
        return ImageFont.truetype(MONO, size, index=index)
    index = {"regular": 0, "medium": 5, "bold": 8, "demi": 2}.get(weight, 0)
    return ImageFont.truetype(SANS, size, index=index)


def window(width, height):
    image = Image.new("RGBA", (width, height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    draw.rounded_rectangle((0, 0, width - 1, height - 1), 18, fill=CANVAS)
    for index, color in enumerate(((255, 95, 87), (254, 188, 46), (40, 200, 64))):
        x = 22 + index * 22
        draw.ellipse((x, 18, x + 13, 31), fill=color)
    return image, draw


def text(draw, xy, value, font, fill=INK):
    draw.text(xy, value, font=font, fill=fill)


def button(draw, box, label, font):
    draw.rounded_rectangle(box, 7, fill=WHITE, outline=LINE, width=1)
    tw = font.getlength(label)
    x = box[0] + (box[2] - box[0] - tw) / 2
    y = box[1] + (box[3] - box[1] - font.size) / 2 - 1
    text(draw, (x, y), label, font)


def pill(draw, box, label, font, fill, ink):
    draw.rounded_rectangle(box, 8, fill=fill)
    tw = font.getlength(label)
    x = box[0] + (box[2] - box[0] - tw) / 2
    text(draw, (x, box[1] + 6), label, font, ink)


def status(draw, width):
    text(draw, (78, 16), "●", face(13, "bold"), GREEN)
    text(draw, (96, 15), "Connected", face(15, "medium"))
    button(draw, (188, 12, 252, 36), "Pause", face(13, "medium"))
    text(draw, (268, 16), "4 containers", face(14), MUTED)
    text(draw, (372, 16), "4 routes ready", face(14), MUTED)
    button(draw, (width - 112, 12, width - 18, 36), "Settings", face(13, "medium"))


def containers():
    image, draw = window(1180, 640)
    status(draw, 1180)
    draw.rounded_rectangle((16, 54, 1164, 624), 14, fill=PAPER, outline=LINE, width=1)
    text(draw, (36, 70), "Containers", face(26, "bold"))
    draw.rounded_rectangle((760, 72, 1020, 106), 8, fill=WHITE, outline=LINE, width=1)
    text(draw, (776, 80), "Search", face(15), MUTED)
    button(draw, (1036, 72, 1144, 106), "Refresh", face(15, "medium"))
    draw.rectangle((16, 122, 1164, 168), fill=ROW)
    text(draw, (36, 134), "▾", face(16, "bold"), MUTED)
    text(draw, (58, 132), "▣", face(16, "bold"), ORANGE)
    text(draw, (84, 132), "shop", face(17, "bold"))
    text(draw, (900, 134), "In hostname", face(14), MUTED)
    draw.rounded_rectangle((1004, 134, 1044, 156), 11, fill=(226, 226, 226))
    draw.ellipse((1006, 136, 1024, 154), fill=WHITE)
    text(draw, (1088, 134), "3", face(15), MUTED)
    rows = ("shop-web", "shop-api", "shop-db")
    y = 180
    for name in rows:
        text(draw, (40, y + 16), "▣", face(16, "bold"), ORANGE)
        text(draw, (68, y + 8), name, face(16, "medium"))
        draw.rounded_rectangle((68, y + 34, 250, y + 64), 6, fill=FIELD, outline=LINE, width=1)
        text(draw, (78, y + 39), name, face(14, mono=True))
        text(draw, (258, y + 40), ".mesh.test", face(15), MUTED)
        button(draw, (900, y + 22, 1012, y + 56), "Disable", face(14, "medium"))
        button(draw, (1024, y + 22, 1072, y + 56), "Copy", face(14, "medium"))
        draw.line((36, y + 78, 1144, y + 78), fill=LINE, width=1)
        y += 78
    text(draw, (40, y + 16), "▣", face(16, "bold"), ORANGE)
    text(draw, (68, y + 8), "worker", face(16, "medium"))
    draw.rounded_rectangle((68, y + 34, 230, y + 64), 6, fill=FIELD, outline=LINE, width=1)
    text(draw, (78, y + 39), "worker", face(14, mono=True))
    text(draw, (238, y + 40), ".mesh.test", face(15), MUTED)
    button(draw, (900, y + 22, 1012, y + 56), "Disable", face(14, "medium"))
    button(draw, (1024, y + 22, 1072, y + 56), "Copy", face(14, "medium"))
    image.save(OUT / "containers.png")


def menu():
    image, draw = window(420, 360)
    draw.rounded_rectangle((0, 0, 419, 44), 18, fill=(236, 236, 236))
    draw.rectangle((0, 22, 419, 44), fill=(236, 236, 236))
    text(draw, (150, 12), "ContainerMesh", face(14, "medium"))
    draw.rounded_rectangle((18, 58, 402, 342), 12, fill=(248, 248, 248), outline=LINE, width=1)
    lines = [
        ("ContainerMesh · Connected", False),
        ("4 containers with ready routes", False),
        None,
        ("Open ContainerMesh", True),
        ("Settings", True),
        ("Pause networking", True),
        ("Connection checks", True),
        ("View logs", True),
        None,
        ("Quit ContainerMesh", True),
    ]
    y = 72
    for line in lines:
        if line is None:
            draw.line((30, y + 6, 390, y + 6), fill=LINE, width=1)
            y += 16
            continue
        label, command = line
        text(draw, (34, y), label, face(15, "medium" if command else "regular"), INK if command else MUTED)
        y += 28
    image.save(OUT / "menu.png")


def settings():
    image, draw = window(980, 560)
    status(draw, 980)
    draw.rounded_rectangle((16, 54, 964, 544), 14, fill=PAPER, outline=LINE, width=1)
    text(draw, (36, 72), "‹ Containers", face(15, "medium"), MUTED)
    text(draw, (160, 68), "Settings", face(26, "bold"))
    tabs = ("General", "Docker", "Names", "Connection checks", "Logs")
    x = 36
    for index, label in enumerate(tabs):
        width = int(face(14, "medium").getlength(label)) + 28
        if index == 0:
            draw.rounded_rectangle((x, 118, x + width, 150), 8, fill=(248, 226, 206))
            text(draw, (x + 14, 126), label, face(14, "bold"), ORANGE)
        else:
            text(draw, (x + 14, 126), label, face(14), INK)
        x += width + 8
    rows = (
        ("Open at login", False),
        ("Start hidden", True),
        ("Show in menu bar", True),
        ("Hide Dock icon", False),
    )
    y = 180
    for label, on in rows:
        text(draw, (48, y), label, face(17))
        draw.rounded_rectangle((820, y - 2, 876, y + 24), 13, fill=(ORANGE if on else (226, 226, 226)))
        knob = 852 if on else 822
        draw.ellipse((knob, y, knob + 22, y + 22), fill=WHITE)
        y += 52
    note = "Open at login brings ContainerMesh back and reconnects when networking was left on."
    text(draw, (48, y + 8), note, face(15), MUTED)
    image.save(OUT / "settings.png")


def names():
    image, draw = window(980, 460)
    status(draw, 980)
    draw.rounded_rectangle((16, 54, 964, 444), 14, fill=PAPER, outline=LINE, width=1)
    text(draw, (36, 72), "‹ Containers", face(15, "medium"), MUTED)
    text(draw, (160, 68), "Settings", face(26, "bold"))
    text(draw, (520, 126), "Names", face(14, "bold"), ORANGE)
    text(draw, (48, 180), "Default domain", face(17))
    draw.rounded_rectangle((250, 172, 520, 208), 8, fill=WHITE, outline=LINE, width=1)
    text(draw, (264, 180), "mesh.test", face(16, mono=True))
    text(draw, (48, 236), "Include Compose stack in hostname", face(17))
    draw.rounded_rectangle((820, 232, 876, 258), 13, fill=(226, 226, 226))
    draw.ellipse((822, 234, 844, 256), fill=WHITE)
    text(draw, (48, 300), "Example", face(17))
    text(draw, (250, 300), "container.mesh.test", face(16, mono=True))
    image.save(OUT / "names.png")


def setup():
    image, draw = window(860, 420)
    draw.rounded_rectangle((16, 16, 844, 404), 14, fill=PAPER, outline=LINE, width=1)
    steps = (("Docker", True), ("Checks", True), ("Connect", False))
    x = 36
    for label, done in steps:
        fill = (248, 226, 206) if done else ORANGE
        ink = ORANGE if done else (255, 244, 221)
        width = 120
        draw.rounded_rectangle((x, 36, x + width, 70), 8, fill=fill)
        text(draw, (x + 16, 44), label if done else "Connect", face(14, "bold"), ink)
        x += width + 8
    text(draw, (36, 100), "ContainerMesh will connect on launch and keep names", face(18), MUTED)
    text(draw, (36, 128), "up to date until you pause it.", face(18), MUTED)
    text(draw, (36, 176), "container.mesh.test", face(18, mono=True))
    button(draw, (36, 300, 250, 340), "Check again", face(15, "medium"))
    pill(draw, (270, 300, 560, 340), "Enable automatic networking", face(15, "bold"), ORANGE, (255, 244, 221))
    image.save(OUT / "setup.png")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    containers()
    menu()
    settings()
    names()
    setup()
    print("wrote", OUT)


if __name__ == "__main__":
    main()
