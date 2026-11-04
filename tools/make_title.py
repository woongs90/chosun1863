"""타이틀 화면 (img/titles1/TimeGate_Title.png, 816x624) + 영상에서도 쓰는 그림 도구"""
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

FB = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
FS = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
def serif(sz): return ImageFont.truetype(FB, sz, index=1)
def sans(sz): return ImageFont.truetype(FS, sz, index=1)

W, H = 272, 208   # 도트 해상도 (x3 = 816x624)

def night_scene(seed=3, gate=True, palace=True):
    rnd = random.Random(seed)
    im = Image.new('RGB', (W, H))
    d = ImageDraw.Draw(im)
    for y in range(H):
        k = y / H
        c = (int(18 + 40 * k), int(16 + 22 * k), int(48 + 50 * k))
        d.line([(0, y), (W, y)], fill=c)
    for _ in range(140):
        x, y = rnd.randrange(W), rnd.randrange(int(H * 0.6))
        b = rnd.randint(150, 255)
        d.point((x, y), fill=(b, b, min(255, b + 20)))
        if rnd.random() < 0.08:
            d.point((x + 1, y), fill=(b, b, b)); d.point((x - 1, y), fill=(b, b, b))
            d.point((x, y + 1), fill=(b, b, b)); d.point((x, y - 1), fill=(b, b, b))
    d.ellipse([214, 18, 238, 42], fill=(250, 240, 200)); d.ellipse([220, 16, 244, 40], fill=(26, 22, 58))
    # 먼 산
    for layer, (base, col) in enumerate([(120, (40, 40, 80)), (138, (32, 32, 64))]):
        pts = [(0, H)]
        x = 0
        while x <= W:
            pts.append((x, base - rnd.randint(0, 22) - (10 if layer == 0 else 0)))
            x += rnd.randint(14, 30)
        pts.append((W, H))
        d.polygon(pts, fill=col)
    if palace:
        roof = (36, 30, 44); wall = (110, 36, 34)
        # 기단과 계단
        d.rectangle([40, 168, 232, 208], fill=(70, 64, 76))
        for i in range(6):
            d.rectangle([116 - i * 4, 168 + i * 6, 156 + i * 4, 173 + i * 6], fill=(92, 86, 96) if i % 2 else (82, 76, 88))
        # 기둥
        for x in range(62, 220, 22):
            d.rectangle([x, 136, x + 5, 168], fill=wall)
            d.point((x + 1, 138), fill=(170, 60, 50))
        d.rectangle([56, 132, 216, 137], fill=(56, 104, 92))
        for x in range(58, 214, 6):
            d.rectangle([x, 133, x + 2, 135], fill=(210, 80, 60))
        # 처마 지붕 (곡선)
        pts = []
        for i in range(0, 41):
            t = i / 40
            x = 30 + t * 212
            y = 128 - 10 * math.sin(math.pi * t) + 8 * (abs(t - 0.5) * 2) ** 3
            pts.append((x, y))
        top = [(70, 104), (202, 104)]
        d.polygon([pts[0]] + top + [pts[-1]] + pts[::-1], fill=roof)
        d.polygon(pts + [(242, 132), (30, 132)], fill=roof)
        for i in range(0, 41, 2):
            x, y = pts[i]
            d.line([(x, y), (x, y + 5)], fill=(54, 46, 62))
        d.line([(66, 104), (206, 104)], fill=(60, 52, 70), width=2)
        d.point((66, 103), fill=(90, 80, 100)); d.point((206, 103), fill=(90, 80, 100))
    return im

def glow_layer(size, cx, cy, r, color, strength=1.0):
    g = Image.new('RGBA', size, (0, 0, 0, 0))
    gd = ImageDraw.Draw(g)
    for i in range(12, 0, -1):
        rr = r * i / 12
        a = int(22 * strength * (13 - i) / 12)
        gd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=color + (a,))
    return g.filter(ImageFilter.GaussianBlur(r / 6))

def draw_gate(big, cx, cy, scale=1.0, t=0.0):
    """시간의 문 (816x624 해상도에 직접)"""
    w, h = int(150 * scale), int(190 * scale)
    big.alpha_composite(glow_layer(big.size, cx, cy, int(220 * scale), (255, 226, 150), 1.4))
    rays = Image.new('RGBA', big.size, (0, 0, 0, 0))
    rd = ImageDraw.Draw(rays)
    for i in range(14):
        a = t + i * math.pi / 7
        L = 330 * scale
        rd.polygon([(cx, cy), (cx + math.cos(a - 0.05) * L, cy + math.sin(a - 0.05) * L), (cx + math.cos(a + 0.05) * L, cy + math.sin(a + 0.05) * L)],
                   fill=(255, 236, 170, 22))
    big.alpha_composite(rays.filter(ImageFilter.GaussianBlur(3)))
    d = ImageDraw.Draw(big)
    d.ellipse([cx - w // 2 - 10, cy - h // 2 - 10, cx + w // 2 + 10, cy + h // 2 + 10], outline=(120, 90, 40, 255), width=int(10 * scale) + 2)
    d.ellipse([cx - w // 2 - 6, cy - h // 2 - 6, cx + w // 2 + 6, cy + h // 2 + 6], outline=(236, 196, 100, 255), width=int(6 * scale) + 1)
    inner = Image.new('RGBA', big.size, (0, 0, 0, 0))
    idr = ImageDraw.Draw(inner)
    idr.ellipse([cx - w // 2, cy - h // 2, cx + w // 2, cy + h // 2], fill=(255, 248, 220, 245))
    idr.ellipse([cx - w // 3, cy - h // 3, cx + w // 3, cy + h // 3], fill=(255, 255, 250, 255))
    big.alpha_composite(inner.filter(ImageFilter.GaussianBlur(4)))
    # 둘레 장식 (점)
    for i in range(16):
        a = i * math.pi / 8
        x = cx + math.cos(a) * (w / 2 + 8); y = cy + math.sin(a) * (h / 2 + 8)
        d.ellipse([x - 3 * scale, y - 3 * scale, x + 3 * scale, y + 3 * scale], fill=(255, 230, 150, 255))

def outlined(d, xy, text, font, fill, outline=(40, 22, 10), ow=6, anchor='mm'):
    x, y = xy
    for dx in range(-ow, ow + 1, 2):
        for dy in range(-ow, ow + 1, 2):
            if dx * dx + dy * dy <= ow * ow:
                d.text((x + dx, y + dy), text, font=font, fill=outline, anchor=anchor)
    d.text((x, y), text, font=font, fill=fill, anchor=anchor)

def logo(big, cx, cy, s=1.0, subtitle=True, alpha=255):
    lay = Image.new('RGBA', big.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f1 = serif(int(84 * s)); f2 = serif(int(30 * s))
    gl = Image.new('RGBA', big.size, (0, 0, 0, 0))
    ImageDraw.Draw(gl).text((cx, cy), '시간의 문', font=f1, fill=(255, 210, 120, 200), anchor='mm')
    lay.alpha_composite(gl.filter(ImageFilter.GaussianBlur(10)))
    outlined(d, (cx, cy), '시간의 문', f1, (255, 232, 160), ow=int(7 * s))
    if subtitle:
        yy = cy + int(70 * s)
        d.line([(cx - int(150 * s), yy), (cx - int(92 * s), yy)], fill=(236, 196, 100), width=2)
        d.line([(cx + int(92 * s), yy), (cx + int(150 * s), yy)], fill=(236, 196, 100), width=2)
        outlined(d, (cx, yy), '고려를 건너다', f2, (255, 246, 226), ow=int(4 * s))
    if alpha < 255:
        a = lay.split()[3].point(lambda v: v * alpha // 255)
        lay.putalpha(a)
    big.alpha_composite(lay)

def paste_icon(big, path, cx, cy, size, angle=0):
    ic = Image.open(path).convert('RGBA').resize((size, size), Image.NEAREST)
    if angle:
        ic = ic.rotate(angle, resample=Image.NEAREST, expand=True)
    gl = glow_layer(big.size, cx, cy, int(size * 0.9), (255, 236, 170), 0.8)
    big.alpha_composite(gl)
    big.alpha_composite(ic, (int(cx - ic.width / 2), int(cy - ic.height / 2)))

def sprite_frame(path, row, col=1, scale=1):
    sh = Image.open(path).convert('RGBA')
    fr = sh.crop((col * 48, row * 48, col * 48 + 48, row * 48 + 48))
    return fr.resize((48 * scale, 48 * scale), Image.NEAREST) if scale != 1 else fr

if __name__ == '__main__' and '--old' not in sys.argv:
    print('make_title.py는 그림 도구 모듈입니다. 타이틀 그림은 hd_title.py로 만드세요. (예전 816 타이틀: --old)')
    sys.exit(0)

if __name__ == '__main__':
    root = sys.argv[1]
    os.makedirs(os.path.join(root, 'img/titles1'), exist_ok=True)
    base = night_scene().resize((816, 624), Image.NEAREST).convert('RGBA')
    draw_gate(base, 408, 300, 1.0, t=0.2)
    pics = os.path.join(root, 'img/pictures')
    paste_icon(base, os.path.join(pics, 'item_celadon.png'), 210, 300, 84, angle=8)
    paste_icon(base, os.path.join(pics, 'item_takbon.png'), 606, 286, 84, angle=-8)
    paste_icon(base, os.path.join(pics, 'item_type.png'), 640, 400, 66, angle=10)
    chars = os.path.join(root, 'img/characters')
    m = sprite_frame(os.path.join(chars, '$student_m.png'), 3, 1, 2)
    f = sprite_frame(os.path.join(chars, '$student_f.png'), 3, 1, 2)
    base.alpha_composite(m, (408 - 104, 530)); base.alpha_composite(f, (408 + 8, 530))
    logo(base, 408, 128, 1.0)
    out = os.path.join(root, 'img/titles1/TimeGate_Title.png')
    base.convert('RGB').save(out)
    print(out)
