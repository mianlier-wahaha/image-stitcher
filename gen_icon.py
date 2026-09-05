from PIL import Image, ImageDraw
import math, os

S = 1024
ACCENT = (45, 212, 191, 255)
ACCENT_RING = (45, 212, 191, 70)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def diag_gradient(c1, c2):
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for y in range(S):
        t = y / S
        col = lerp(c1, c2, t)
        ld.line([(0, y), (S, y)], fill=col + (255,))
    return layer

def make_tile(size, sky_top, sky_bottom, sun, mC1, mC2):
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for y in range(size):
        t = y / size
        col = lerp(sky_top, sky_bottom, t)
        ld.line([(0, y), (size, y)], fill=col + (255,))
    if sun:
        cx, cy, r = sun
        ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(253, 224, 71, 255))
    p1 = [(0,205),(60,145),(110,188),(175,122),(235,182),(286,152),(286,286),(0,286)]
    p2 = [(0,235),(70,175),(130,218),(205,152),(286,212),(286,286),(0,286)]
    ld.polygon(p1, fill=mC1 + (255,))
    ld.polygon(p2, fill=mC2 + (255,))
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, size, size], radius=40, fill=255)
    out = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    out.paste(layer, (0, 0), m)
    ImageDraw.Draw(out).rounded_rectangle([0, 0, size, size], radius=40,
                                          outline=(226, 232, 240, 255), width=6)
    return out

def dashed_line(d, p1, p2, dash=16, gap=16, width=8, fill=ACCENT):
    x1, y1 = p1; x2, y2 = p2
    dist = math.hypot(x2 - x1, y2 - y1)
    ang = math.atan2(y2 - y1, x2 - x1)
    pos = 0
    while pos < dist:
        a = pos; b = min(pos + dash, dist)
        xa, ya = x1 + a * math.cos(ang), y1 + a * math.sin(ang)
        xb, yb = x1 + b * math.cos(ang), y1 + b * math.sin(ang)
        d.line([(xa, ya), (xb, yb)], fill=fill, width=width)
        pos += dash + gap

def tri(d, tip, w, direction, fill=ACCENT):
    # direction: 'right','left','up','down'
    x, y = tip
    if direction == "right":
        d.polygon([(x, y), (x - w, y - w * 0.6), (x - w, y + w * 0.6)], fill=fill)
    elif direction == "left":
        d.polygon([(x, y), (x + w, y - w * 0.6), (x + w, y + w * 0.6)], fill=fill)
    elif direction == "up":
        d.polygon([(x, y), (x - w * 0.6, y + w), (x + w * 0.6, y + w)], fill=fill)
    else:
        d.polygon([(x, y), (x - w * 0.6, y - w), (x + w * 0.6, y - w)], fill=fill)

img = Image.new("RGBA", (S, S), (0, 0, 0, 0))

# 背景
bg = diag_gradient((30, 41, 59), (11, 18, 32))
mask = Image.new("L", (S, S), 0)
ImageDraw.Draw(mask).rounded_rectangle([0, 0, S, S], radius=224, fill=255)
img.paste(bg, (0, 0), mask)
ImageDraw.Draw(img).rounded_rectangle([26, 26, S - 26, S - 26], radius=200,
                                      outline=ACCENT_RING, width=6)

# 四张照片
tiles = [
    (208, 208, (186, 230, 253), (224, 242, 254), (78, 78, 34), (14, 165, 233), (3, 105, 161)),
    (530, 208, (186, 230, 253), (224, 242, 254), (208, 78, 34), (20, 184, 166), (15, 118, 110)),
    (208, 530, (186, 230, 253), (224, 242, 254), (143, 86, 32), (139, 92, 246), (109, 40, 217)),
    (530, 530, (186, 230, 253), (224, 242, 254), None, (34, 197, 94), (21, 128, 61)),
]
for x, y, st, sb, sun, c1, c2 in tiles:
    t = make_tile(286, st, sb, sun, c1, c2)
    img.paste(t, (x, y), t)

d = ImageDraw.Draw(img)
# 拼接缝（虚线十字）
dashed_line(d, (208, 512), (816, 512))
dashed_line(d, (512, 208), (512, 816))
# 四向箭头
tri(d, (816, 512), 26, "right")
tri(d, (208, 512), 26, "left")
tri(d, (512, 816), 26, "down")
tri(d, (512, 208), 26, "up")

os.makedirs("build", exist_ok=True)
img.save("build/icon_1024.png")
print("saved build/icon_1024.png", img.size)
