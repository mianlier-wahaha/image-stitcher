from PIL import Image, ImageDraw
import math, os

S = 1024
ACCENT = (45, 212, 191, 255)
ACCENT_RING = (45, 212, 191, 70)
WHITE = (226, 232, 240, 255)

def lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))

def diag_gradient(c1, c2):
    layer = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for y in range(S):
        col = lerp(c1, c2, y / S)
        ld.line([(0, y), (S, y)], fill=col + (255,))
    return layer

def make_tile(size, sky_top, sky_bottom, sun, mC1, mC2):
    scale = size / 286.0
    layer = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    ld = ImageDraw.Draw(layer)
    for y in range(size):
        col = lerp(sky_top, sky_bottom, y / size)
        ld.line([(0, y), (size, y)], fill=col + (255,))
    if sun:
        cx, cy, r = [int(v * scale) for v in sun]
        ld.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(253, 224, 71, 255))
    p1 = [(0,205),(60,145),(110,188),(175,122),(235,182),(286,152),(286,286),(0,286)]
    p2 = [(0,235),(70,175),(130,218),(205,152),(286,212),(286,286),(0,286)]
    ld.polygon([(x*scale, y*scale) for x,y in p1], fill=mC1 + (255,))
    ld.polygon([(x*scale, y*scale) for x,y in p2], fill=mC2 + (255,))
    m = Image.new("L", (size, size), 0)
    ImageDraw.Draw(m).rounded_rectangle([0,0,size,size], radius=int(40*scale), fill=255)
    out = Image.new("RGBA", (size, size), (0,0,0,0))
    out.paste(layer, (0,0), m)
    ImageDraw.Draw(out).rounded_rectangle([0,0,size,size], radius=int(40*scale),
                                          outline=WHITE, width=max(4,int(6*scale)))
    return out

def dashed_line(d, p1, p2, dash=16, gap=16, width=8, fill=ACCENT):
    x1,y1 = p1; x2,y2 = p2
    dist = math.hypot(x2-x1, y2-y1)
    ang = math.atan2(y2-y1, x2-x1)
    pos = 0
    while pos < dist:
        a = pos; b = min(pos+dash, dist)
        xa,ya = x1+a*math.cos(ang), y1+a*math.sin(ang)
        xb,yb = x1+b*math.cos(ang), y1+b*math.sin(ang)
        d.line([(xa,ya),(xb,yb)], fill=fill, width=width)
        pos += dash+gap

def tri(d, tip, w, direction, fill=ACCENT):
    x,y = tip
    if direction == "right":
        d.polygon([(x,y),(x-w,y-w*0.6),(x-w,y+w*0.6)], fill=fill)
    elif direction == "left":
        d.polygon([(x,y),(x+w,y-w*0.6),(x+w,y+w*0.6)], fill=fill)
    elif direction == "up":
        d.polygon([(x,y),(x-w*0.6,y+w),(x+w*0.6,y+w)], fill=fill)
    else:
        d.polygon([(x,y),(x-w*0.6,y-w),(x+w*0.6,y-w)], fill=fill)

def base_bg(c1=(30,41,59), c2=(11,18,32)):
    img = Image.new("RGBA", (S,S), (0,0,0,0))
    bg = diag_gradient(c1, c2)
    mask = Image.new("L", (S,S), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0,0,S,S], radius=224, fill=255)
    img.paste(bg, (0,0), mask)
    ImageDraw.Draw(img).rounded_rectangle([26,26,S-26,S-26], radius=200,
                                          outline=ACCENT_RING, width=6)
    return img

def style_A():
    img = base_bg()
    tiles = [
        (208,208,(186,230,253),(224,242,254),(78,78,34),(14,165,233),(3,105,161)),
        (530,208,(186,230,253),(224,242,254),(208,78,34),(20,184,166),(15,118,110)),
        (208,530,(186,230,253),(224,242,254),(143,86,32),(139,92,246),(109,40,217)),
        (530,530,(186,230,253),(224,242,254),None,(34,197,94),(21,128,61)),
    ]
    for x,y,st,sb,sun,c1,c2 in tiles:
        t = make_tile(286, st, sb, sun, c1, c2)
        img.paste(t, (x,y), t)
    d = ImageDraw.Draw(img)
    dashed_line(d,(208,512),(816,512))
    dashed_line(d,(512,208),(512,816))
    tri(d,(816,512),26,"right"); tri(d,(208,512),26,"left")
    tri(d,(512,816),26,"down"); tri(d,(512,208),26,"up")
    return img

def style_B():
    img = base_bg()
    t = make_tile(720,(186,230,253),(224,242,254),(78,78,34),(14,165,233),(3,105,161))
    img.paste(t,(152,152),t)
    d = ImageDraw.Draw(img)
    dashed_line(d,(152,512),(872,512))
    dashed_line(d,(512,152),(512,872))
    tri(d,(872,512),34,"right"); tri(d,(152,512),34,"left")
    tri(d,(512,872),34,"down"); tri(d,(512,152),34,"up")
    return img

def style_C():
    img = base_bg()
    blocks = [
        (152,152,(45,212,191)),
        (552,152,(139,92,246)),
        (152,552,(251,146,60)),
        (552,552,(34,197,94)),
    ]
    d = ImageDraw.Draw(img)
    for x,y,c in blocks:
        fill = c + (255,)
        d.rounded_rectangle([x,y,x+320,y+320], radius=64, fill=fill,
                            outline=(255,255,255,60), width=4)
    # 中心缝 + 箭头
    d2 = ImageDraw.Draw(img)
    dashed_line(d2,(152,512),(872,512))
    dashed_line(d2,(512,152),(512,872))
    tri(d2,(872,512),30,"right"); tri(d2,(152,512),30,"left")
    tri(d2,(512,872),30,"down"); tri(d2,(512,152),30,"up")
    return img

def style_D():
    img = base_bg()
    d = ImageDraw.Draw(img)
    # 横向矩形（上）
    d.rounded_rectangle([152,212,872,512], radius=48, fill=(14,165,233,235),
                        outline=WHITE, width=6)
    # 竖向矩形（下，交叠形成十字咬合）
    d.rounded_rectangle([352,362,672,862], radius=48, fill=(139,92,246,235),
                        outline=WHITE, width=6)
    # 高亮十字缝
    dd = ImageDraw.Draw(img)
    dashed_line(dd,(152,512),(872,512))
    dashed_line(dd,(512,362),(512,862))
    tri(dd,(872,512),32,"right"); tri(dd,(152,512),32,"left")
    tri(dd,(512,862),32,"down"); tri(dd,(512,362),32,"up")
    return img

def style_E():
    img = base_bg()
    photos = [
        (420,152,232,-8,(186,230,253),(224,242,254),(143,86,32),(139,92,246),(109,40,217)),
        (380,430,300,6,(186,230,253),(224,242,254),(78,78,34),(14,165,233),(3,105,161)),
        (360,300,520,-3,(186,230,253),(224,242,254),None,(34,197,94),(21,128,61)),
    ]
    for size,x,y,ang,st,sb,sun,c1,c2 in photos:
        t = make_tile(size, st, sb, sun, c1, c2)
        rt = t.rotate(ang, resample=Image.BICUBIC, expand=True)
        img.alpha_composite(rt, (x, y))
    d = ImageDraw.Draw(img)
    dashed_line(d,(512,152),(512,872))
    return img

os.makedirs("build/variants", exist_ok=True)
variants = {
    "A_经典四宫格": style_A,
    "B_极简单图缝合": style_B,
    "C_彩色拼块": style_C,
    "D_双矩形拼合": style_D,
    "E_层叠照片": style_E,
}
for name, fn in variants.items():
    out = fn()
    path = f"build/variants/icon_{name}.png"
    out.save(path)
    print("saved", path, out.size)
print("ALL DONE")
