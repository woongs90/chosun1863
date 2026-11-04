"""넓은 화면용 방 그림: 가운데 17칸(원래 방) + 양옆 6칸씩 바깥 마당 장식.
화면이 좁은 기기는 가운데만, 넓은 기기는 마당까지 보입니다."""
import os, sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hd_art import TS, W, H, sh, mix, layer, outline, soft_shadow, noise_fill, vgrad, hgrad, obj_plant
import hd_world as HW
import make_world as MW

MARGIN = 6                    # 양옆 칸 수
MW_PX = MARGIN * TS           # 288
WIDE_W = W + 2 * MW_PX        # 1392

def put(base, lay, s=0.5):
    base.alpha_composite(outline(lay, s))

# ======================================================================== 바닥
def ground_bakseok(img, box, base, seed):
    """궁궐 마당 박석: 크기가 제각각인 넓적한 돌"""
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    d.rectangle([x0, y0, x1, y1], fill=sh(base, 0.72))
    rnd = random.Random(seed)
    y = y0
    while y < y1:
        rh = rnd.choice([20, 24, 28])
        x = x0 - rnd.randint(0, 30)
        while x < x1:
            rw = rnd.randint(26, 46)
            c = sh(base, 0.9 + rnd.random() * 0.16)
            c = mix(c, (176, 160, 130), rnd.random() * 0.2)
            a, b = max(x + 1, x0), min(x + rw - 1, x1)
            if b > a:
                vgrad(d, (a, y + 1, b, min(y + rh - 1, y1)), sh(c, 1.05), sh(c, 0.93))
                d.line([(a, y + 1), (b - 1, y + 1)], fill=sh(c, 1.16))
                if rnd.random() < 0.25:
                    gx, gy = rnd.randint(a, max(a, b - 3)), rnd.randint(y + 3, y + rh - 4)
                    d.point((gx, gy), fill=sh(c, 0.82))
            x += rw
        y += rh
    for _ in range(40):  # 돌 틈 풀
        gx, gy = rnd.randrange(x0, x1 - 2), rnd.randrange(y0, y1 - 3)
        d.line([(gx, gy), (gx + 1, gy - 3)], fill=(96, 140, 80))

def ground(img, kind, box, seed):
    if kind == 'bakseok': ground_bakseok(img, box, (172, 164, 150), seed)
    elif kind == 'earth': HW.floor_earth(img, box, (182, 152, 112), seed)
    elif kind == 'darkearth': HW.floor_earth(img, box, (158, 128, 92), seed)
    elif kind == 'grass': HW.floor_grass(img, box, (100, 146, 80), seed)
    elif kind == 'stone': HW.floor_stone(img, box, (160, 154, 142), seed, 32)

def path_row(img, kind, x0, x1, seed):
    """문에서 바깥으로 이어지는 길 (9번째 줄)"""
    if kind == 'grass':
        return  # 풀밭 바닥이 이미 흙길을 그림
    d = ImageDraw.Draw(img)
    y0, y1 = 9 * TS + 2, 10 * TS - 2
    rnd = random.Random(seed)
    if kind in ('bakseok', 'stone'):
        x = x0
        while x < x1:
            w = rnd.randint(34, 44)
            c = (198, 190, 174) if kind == 'bakseok' else (182, 176, 166)
            c = sh(c, 0.95 + rnd.random() * 0.08)
            soft_shadow(img, (x + 2, y1 - 4, x + w + 2, y1 + 4), 60, 3)
            d = ImageDraw.Draw(img)
            d.rounded_rectangle([x + 2, y0 + 2, x + w - 2, y1 - 2], 5, fill=c, outline=sh(c, 0.72))
            d.line([(x + 6, y0 + 4), (x + w - 6, y0 + 4)], fill=sh(c, 1.12))
            x += w + rnd.randint(4, 8)
    else:
        path = Image.new('RGB', (x1 - x0, y1 - y0 + 8))
        noise_fill(path, (0, 0, path.width, path.height), (150, 118, 82), 8, seed=seed)
        mask = Image.new('L', path.size, 0); md = ImageDraw.Draw(mask)
        for x in range(0, path.width, 6):
            md.rectangle([x, 3 + int(2 * math.sin(x / 19)), x + 6, path.height - 3 - int(2 * math.sin(x / 27 + 1))], fill=255)
        img.paste(path, (x0, y0 - 4), mask.filter(ImageFilter.GaussianBlur(1.5)))

# ======================================================================== 위쪽 담장 / 울타리
def top_trees(d, x0, x1, seed, y_max=46):
    rnd = random.Random(seed)
    vgrad(d, (x0, 0, x1, y_max), (54, 96, 70), (40, 76, 56))
    for _ in range(int((x1 - x0) / 7)):
        x = rnd.randrange(x0 - 16, x1); y = rnd.randrange(-8, y_max - 18); r = rnd.randint(10, 18)
        d.ellipse([x, y, x + r * 2, y + r + 4], fill=rnd.choice([(52, 104, 64), (68, 122, 74), (44, 88, 58), (80, 132, 80)]))

def top_damjang(img, x0, x1, seed, cap=(70, 66, 74), face=(226, 214, 190), pattern=True):
    d = ImageDraw.Draw(img)
    top_trees(d, x0, x1, seed)
    # 기와 지붕 머리
    vgrad(d, (x0, 38, x1, 58), sh(cap, 1.15), sh(cap, 0.85))
    for row, y in enumerate((38, 45, 51)):
        off = 6 if row % 2 else 0
        for x in range(x0 - 12 + off, x1, 12):
            d.chord([x, y, x + 12, y + 9], 180, 360, fill=sh(cap, 1.3), outline=sh(cap, 0.6))
    d.line([(x0, 58), (x1, 58)], fill=sh(cap, 0.5))
    # 벽면: 아래는 돌, 위는 회벽 + 꽃담 무늬
    noise_fill(img, (x0, 59, x1, 96), face, 5, seed=seed + 1)
    d = ImageDraw.Draw(img)
    vgrad(d, (x0, 59, x1, 64), sh(face, 0.8), face)
    rnd = random.Random(seed)
    for y in range(78, 96, 9):
        off = rnd.randint(0, 14)
        for x in range(x0 - off, x1, 16):
            c = sh((150, 140, 128), 0.9 + rnd.random() * 0.15)
            d.rectangle([max(x, x0), y, min(x + 14, x1 - 1), y + 7], fill=c, outline=sh(c, 0.7))
    if pattern:
        for x in range(x0 + 20, x1 - 24, 64):
            d.rectangle([x, 64, x + 22, 74], outline=(176, 110, 80), width=2)
            d.line([(x + 11, 64), (x + 11, 74)], fill=(176, 110, 80), width=2)

def top_earthwall(img, x0, x1, seed):
    d = ImageDraw.Draw(img)
    top_trees(d, x0, x1, seed)
    # 초가 머리 (볏짚)
    vgrad(d, (x0, 36, x1, 58), (214, 184, 112), (170, 140, 80))
    rnd = random.Random(seed)
    for _ in range((x1 - x0) * 2):
        x = rnd.randrange(x0, x1); y = rnd.randrange(38, 56)
        d.line([(x, y), (x + rnd.randint(-2, 2), y + rnd.randint(3, 6))], fill=rnd.choice([(232, 204, 132), (150, 120, 70)]))
    d.line([(x0, 58), (x1, 58)], fill=(110, 86, 50))
    noise_fill(img, (x0, 59, x1, 96), (184, 150, 108), 9, seed=seed + 2)
    d = ImageDraw.Draw(img)
    vgrad(d, (x0, 59, x1, 66), (130, 100, 70), (184, 150, 108))
    for _ in range(int((x1 - x0) / 9)):
        x, y = rnd.randrange(x0, x1 - 10), rnd.randrange(68, 92)
        d.ellipse([x, y, x + rnd.randint(6, 12), y + rnd.randint(4, 7)], fill=sh((150, 130, 110), 0.9 + rnd.random() * 0.2), outline=(110, 90, 70))

def top_palisade(img, x0, x1, seed):
    d = ImageDraw.Draw(img)
    vgrad(d, (x0, 0, x1, 50), (60, 96, 70), (40, 74, 52))
    rnd = random.Random(seed)
    for _ in range(int((x1 - x0) / 13)):
        x = rnd.randrange(x0 - 10, x1); y = rnd.randrange(-6, 26); r = rnd.randint(10, 18)
        d.ellipse([x, y, x + r * 2, y + r], fill=rnd.choice([(52, 104, 64), (70, 124, 76), (44, 90, 58)]))
    face = (136, 98, 62)
    for x in range(x0, x1, 10):
        c = sh(face, 0.9 + ((x // 10) % 2) * 0.12)
        hgrad(d, (x, 52, x + 9, 96), sh(c, 0.8), sh(c, 0.75), mid=sh(c, 1.25))
        d.polygon([(x, 52), (x + 9, 52), (x + 4, 42)], fill=sh(c, 1.1), outline=sh(c, 0.6))
    d.rectangle([x0, 70, x1, 74], fill=sh(face, 0.55)); d.line([(x0, 70), (x1, 70)], fill=sh(face, 0.8))

# ======================================================================== 바깥 물건 (모두 816 캔버스 좌표, 타일 단위)
def pine(img, tx, ty, seed=0, big=1.0):
    """소나무: (tx, ty)가 밑동 칸"""
    rnd = random.Random(seed)
    X, Y = tx * TS + 24, ty * TS + 40
    soft_shadow(img, (X - 46 * big, Y - 6, X + 54 * big, Y + 14), 90, 6)
    lay = layer(); d = ImageDraw.Draw(lay)
    tr = (118, 72, 48)
    d.polygon([(X - 7, Y), (X + 7, Y), (X + 4, Y - 70 * big), (X - 2, Y - 70 * big)], fill=tr)
    d.line([(X - 4, Y - 4), (X - 1, Y - 66 * big)], fill=sh(tr, 1.3), width=2)
    for k in range(5):
        yy = Y - 14 - k * 13
        d.line([(X - 6, yy), (X - 2, yy - 2)], fill=sh(tr, 0.7))
    greens = [(40, 86, 58), (54, 106, 66), (70, 126, 76), (92, 146, 88)]
    clusters = [(-30, -64, 30), (26, -70, 28), (-4, -96, 34), (-38, -92, 22), (34, -100, 22), (0, -124, 26), (-16, -48, 18), (20, -46, 16)]
    for i, g in enumerate(greens):
        for (ox, oy, r) in clusters:
            r2 = (r - i * 5) * big
            if r2 <= 3: continue
            cx, cy = X + ox * big - i * 2, Y + oy * big - i * 3
            d.ellipse([cx - r2, cy - r2 * 0.62, cx + r2, cy + r2 * 0.62], fill=g)
    for _ in range(40):
        ox, oy, r = rnd.choice(clusters)
        cx = X + (ox + rnd.randint(-r, r) * 0.8) * big; cy = Y + (oy + rnd.randint(-r // 2, r // 2) * 0.6) * big
        d.line([(cx - 3, cy), (cx + 3, cy - 1)], fill=(120, 170, 110))
    put(img, lay, 0.5)

def stone_lantern(img, tx, ty):
    X, Y = tx * TS + 24, ty * TS + 44
    soft_shadow(img, (X - 18, Y - 6, X + 22, Y + 6), 90, 4)
    lay = layer(); d = ImageDraw.Draw(lay)
    s = (178, 172, 160)
    d.rectangle([X - 14, Y - 8, X + 14, Y], fill=sh(s, 0.85)); d.line([(X - 14, Y - 8), (X + 14, Y - 8)], fill=sh(s, 1.15))
    d.rectangle([X - 5, Y - 38, X + 5, Y - 8], fill=s); d.line([(X - 5, Y - 38), (X - 5, Y - 8)], fill=sh(s, 1.15))
    d.polygon([(X - 14, Y - 40), (X + 14, Y - 40), (X + 10, Y - 46), (X - 10, Y - 46)], fill=sh(s, 0.95))
    d.rectangle([X - 10, Y - 66, X + 10, Y - 46], fill=sh(s, 1.02))
    d.rectangle([X - 5, Y - 62, X + 5, Y - 50], fill=(255, 214, 140)); d.line([(X, Y - 62), (X, Y - 50)], fill=(220, 160, 90))
    d.polygon([(X - 18, Y - 66), (X + 18, Y - 66), (X + 8, Y - 76), (X - 8, Y - 76)], fill=sh(s, 0.9))
    d.line([(X - 18, Y - 66), (X + 18, Y - 66)], fill=sh(s, 0.7))
    d.ellipse([X - 4, Y - 84, X + 4, Y - 74], fill=sh(s, 1.05))
    put(img, lay, 0.5)
    img.alpha_composite(HW.MW_glow((X, Y - 56), 22, (255, 210, 150)))

def dmu(img, tx, ty):
    """드므: 궁궐 화재 대비 물그릇"""
    X, Y = tx * TS + 24, ty * TS + 30
    soft_shadow(img, (X - 22, Y + 6, X + 24, Y + 18), 90, 4)
    lay = layer(); d = ImageDraw.Draw(lay)
    br = (92, 104, 88)
    d.ellipse([X - 20, Y - 12, X + 20, Y + 14], fill=br)
    d.chord([X - 20, Y - 12, X + 20, Y + 14], 100, 260, fill=sh(br, 1.25))
    d.ellipse([X - 18, Y - 16, X + 18, Y - 2], fill=sh(br, 0.85))
    d.ellipse([X - 15, Y - 14, X + 15, Y - 4], fill=(80, 130, 170)); d.line([(X - 8, Y - 10), (X + 2, Y - 11)], fill=(170, 210, 230))
    for ox in (-14, 14):
        d.ellipse([X + ox - 3, Y - 2, X + ox + 3, Y + 4], fill=sh(br, 0.65))
    d.rectangle([X - 12, Y + 12, X + 12, Y + 16], fill=(150, 144, 132))
    put(img, lay, 0.5)

def onggi(d, cx, by, s, col=(112, 72, 46)):
    d.ellipse([cx - 13 * s, by - 30 * s, cx + 13 * s, by], fill=col)
    d.chord([cx - 13 * s, by - 30 * s, cx + 13 * s, by], 100, 260, fill=sh(col, 1.2))
    d.ellipse([cx - 9 * s, by - 34 * s, cx + 9 * s, by - 24 * s], fill=sh(col, 0.8))
    d.ellipse([cx - 7 * s, by - 33 * s, cx + 7 * s, by - 26 * s], fill=sh(col, 0.55))
    d.line([(cx - 8 * s, by - 22 * s), (cx - 9 * s, by - 10 * s)], fill=sh(col, 1.45), width=2)

def jangdok(img, tx, ty, w=3):
    """장독대: 돌 단 위 항아리들 (w x 2칸)"""
    X, Y = tx * TS, ty * TS
    soft_shadow(img, (X, Y + 80, X + w * TS + 8, Y + 98), 90, 5)
    lay = layer(); d = ImageDraw.Draw(lay)
    s = (168, 160, 146)
    d.rectangle([X + 2, Y + 50, X + w * TS - 2, Y + 90], fill=sh(s, 0.85))
    d.rectangle([X + 2, Y + 40, X + w * TS - 2, Y + 52], fill=s); d.line([(X + 2, Y + 40), (X + w * TS - 2, Y + 40)], fill=sh(s, 1.15))
    rnd = random.Random(tx * 7 + ty)
    for yy in range(Y + 56, Y + 88, 10):
        for xx in range(X + 4 + rnd.randint(0, 8), X + w * TS - 8, 16):
            d.rectangle([xx, yy, xx + 13, yy + 8], outline=sh(s, 0.7))
    jars = []
    n = w * 2
    for i in range(n):
        cx = X + 14 + i * (w * TS - 28) / max(1, n - 1)
        jars.append((cx, Y + 48 - (i % 2) * 14, 0.9 + (i * 37 % 5) * 0.06))
    for cx, by, s2 in sorted(jars, key=lambda j: j[1]):
        onggi(d, cx, by, s2, mix((112, 72, 46), (86, 56, 40), (cx % 3) / 3))
    put(img, lay, 0.5)

def well(img, tx, ty):
    X, Y = tx * TS + 48, ty * TS + 50
    soft_shadow(img, (X - 40, Y + 16, X + 44, Y + 34), 90, 5)
    lay = layer(); d = ImageDraw.Draw(lay)
    s = (160, 154, 140)
    d.ellipse([X - 36, Y - 14, X + 36, Y + 30], fill=sh(s, 0.85))
    d.ellipse([X - 36, Y - 22, X + 36, Y + 18], fill=s)
    for k in range(10):
        a = k * math.pi / 5
        d.line([(X + math.cos(a) * 28, Y - 2 + math.sin(a) * 15), (X + math.cos(a) * 36, Y - 2 + math.sin(a) * 20)], fill=sh(s, 0.7))
    d.ellipse([X - 26, Y - 15, X + 26, Y + 11], fill=(40, 60, 76)); d.ellipse([X - 18, Y - 9, X + 10, Y + 3], fill=(70, 110, 140))
    wood = (130, 86, 52)
    d.rectangle([X - 40, Y - 56, X - 34, Y + 4], fill=wood); d.rectangle([X + 34, Y - 56, X + 40, Y + 4], fill=wood)
    d.rectangle([X - 44, Y - 60, X + 44, Y - 54], fill=sh(wood, 1.15))
    d.line([(X, Y - 54), (X, Y - 22)], fill=(90, 70, 50))
    onggi(d, X, Y - 10, 0.5, (150, 110, 70))
    put(img, lay, 0.5)

def woodpile(img, tx, ty, w=2):
    X, Y = tx * TS, ty * TS
    soft_shadow(img, (X, Y + 38, X + w * TS + 6, Y + 50), 90, 4)
    lay = layer(); d = ImageDraw.Draw(lay)
    for row in range(3):
        y = Y + 36 - row * 12
        off = 7 if row % 2 else 0
        for x in range(X + 4 + off, X + w * TS - 10, 14):
            c = (150, 102, 62)
            d.ellipse([x, y - 6, x + 13, y + 6], fill=(196, 150, 100), outline=(110, 72, 42))
            d.ellipse([x + 4, y - 2, x + 9, y + 2], outline=(160, 116, 74))
    put(img, lay, 0.5)

def haystack(img, tx, ty):
    X, Y = tx * TS + 24, ty * TS + 44
    soft_shadow(img, (X - 26, Y - 6, X + 30, Y + 8), 90, 4)
    lay = layer(); d = ImageDraw.Draw(lay)
    d.ellipse([X - 24, Y - 34, X + 24, Y + 2], fill=(206, 172, 96))
    d.polygon([(X - 22, Y - 22), (X + 22, Y - 22), (X, Y - 58)], fill=(222, 190, 112))
    d.polygon([(X - 8, Y - 46), (X + 8, Y - 46), (X, Y - 64)], fill=(180, 146, 80))
    rnd = random.Random(tx * 13 + ty)
    for _ in range(50):
        x = X + rnd.randint(-20, 20); y = Y + rnd.randint(-50, -4)
        d.line([(x, y), (x + rnd.randint(-1, 1), y + 4)], fill=rnd.choice([(240, 214, 140), (160, 128, 70)]))
    d.line([(X - 22, Y - 22), (X + 22, Y - 22)], fill=(140, 110, 60), width=2)
    put(img, lay, 0.5)

def pagoda(img, tx, ty):
    """3층 석탑 (2칸 폭), (tx, ty) 밑단 왼쪽 칸"""
    X, Y = tx * TS + 48, ty * TS + 44
    soft_shadow(img, (X - 44, Y - 8, X + 50, Y + 10), 100, 6)
    lay = layer(); d = ImageDraw.Draw(lay)
    s = (180, 174, 162)
    d.rectangle([X - 38, Y - 14, X + 38, Y], fill=sh(s, 0.85)); d.line([(X - 38, Y - 14), (X + 38, Y - 14)], fill=sh(s, 1.15))
    d.rectangle([X - 30, Y - 34, X + 30, Y - 14], fill=sh(s, 0.95))
    y = Y - 34
    for i, (bw, bh) in enumerate([(22, 26), (18, 16), (14, 13)]):
        d.rectangle([X - bw, y - bh, X + bw, y], fill=s)
        d.line([(X - bw, y - bh), (X - bw, y)], fill=sh(s, 1.15)); d.line([(X + bw, y - bh), (X + bw, y)], fill=sh(s, 0.75))
        d.line([(X - bw + 4, y - bh), (X - bw + 4, y)], fill=sh(s, 0.85)); d.line([(X + bw - 4, y - bh), (X + bw - 4, y)], fill=sh(s, 0.85))
        y -= bh
        rw = bw + 12
        d.polygon([(X - rw, y), (X + rw, y), (X + rw - 6, y - 6), (X - rw + 6, y - 6)], fill=sh(s, 0.92))
        d.line([(X - rw, y), (X + rw, y)], fill=sh(s, 0.65))
        d.polygon([(X - rw, y), (X - rw - 4, y - 5), (X - rw + 6, y - 6)], fill=sh(s, 0.92))
        d.polygon([(X + rw, y), (X + rw + 4, y - 5), (X + rw - 6, y - 6)], fill=sh(s, 0.92))
        y -= 6
    d.rectangle([X - 2, y - 18, X + 2, y], fill=(150, 130, 90))
    for k in range(3): d.ellipse([X - 5, y - 6 - k * 6, X + 5, y - 1 - k * 6], fill=(170, 150, 100))
    put(img, lay, 0.5)

def bush(img, tx, ty, flowers=None, seed=0):
    X, Y = tx * TS + 24, ty * TS + 40
    soft_shadow(img, (X - 22, Y - 4, X + 26, Y + 8), 80, 4)
    lay = layer(); d = ImageDraw.Draw(lay)
    rnd = random.Random(seed + tx * 5 + ty)
    for (ox, oy, r, c) in [(-10, -14, 14, (52, 104, 62)), (10, -14, 14, (52, 104, 62)), (0, -24, 15, (66, 122, 72)), (-6, -26, 9, (90, 146, 88)), (8, -18, 8, (90, 146, 88))]:
        d.ellipse([X + ox - r, Y + oy - r * 0.8, X + ox + r, Y + oy + r * 0.8], fill=c)
    if flowers:
        for _ in range(7):
            fx, fy = X + rnd.randint(-18, 18), Y + rnd.randint(-34, -8)
            d.ellipse([fx - 2, fy - 2, fx + 2, fy + 2], fill=flowers)
    put(img, lay, 0.5)

def rock(img, tx, ty, seed=0):
    X, Y = tx * TS + 24, ty * TS + 38
    soft_shadow(img, (X - 18, Y - 2, X + 20, Y + 8), 80, 3)
    lay = layer(); d = ImageDraw.Draw(lay)
    s = (150, 146, 138)
    d.polygon([(X - 16, Y + 2), (X - 12, Y - 14), (X - 2, Y - 20), (X + 12, Y - 14), (X + 16, Y + 2)], fill=s)
    d.polygon([(X - 12, Y - 14), (X - 2, Y - 20), (X + 2, Y - 8), (X - 10, Y - 4)], fill=sh(s, 1.2))
    d.ellipse([X + 6, Y - 6, X + 11, Y - 3], fill=(110, 150, 90))
    put(img, lay, 0.5)

def bamboo(img, tx, ty, seed=0):
    X, Y = tx * TS + 24, ty * TS + 44
    soft_shadow(img, (X - 24, Y - 6, X + 28, Y + 6), 80, 4)
    lay = layer(); d = ImageDraw.Draw(lay)
    rnd = random.Random(seed + tx)
    for i in range(5):
        x = X - 16 + i * 8 + rnd.randint(-2, 2); top = Y - 70 - rnd.randint(0, 30)
        c = (110, 160, 90) if i % 2 else (90, 140, 76)
        d.rectangle([x, top, x + 4, Y], fill=c); d.line([(x, top), (x, Y)], fill=sh(c, 1.25))
        for yy in range(top + 12, Y, 14): d.line([(x - 1, yy), (x + 5, yy)], fill=sh(c, 0.7))
        for k in range(3):
            ly = top + 6 + k * 16; s = 1 if (k + i) % 2 else -1
            d.polygon([(x + 2, ly), (x + 2 + s * 16, ly - 4), (x + 2 + s * 14, ly + 1)], fill=(70, 130, 70))
    put(img, lay, 0.5)

def flowerbed(img, tx, ty, w=2, col=(240, 140, 170)):
    X, Y = tx * TS, ty * TS
    lay = layer(); d = ImageDraw.Draw(lay)
    d.rectangle([X + 4, Y + 14, X + w * TS - 4, Y + 44], fill=(110, 82, 56))
    for x in range(X + 4, X + w * TS - 6, 10):
        d.rectangle([x, Y + 40, x + 9, Y + 46], fill=(170, 162, 148), outline=(120, 114, 104))
    rnd = random.Random(tx * 3 + ty)
    for _ in range(10 * w):
        fx, fy = rnd.randint(X + 8, X + w * TS - 8), rnd.randint(Y + 14, Y + 38)
        d.line([(fx, fy), (fx, fy + 6)], fill=(70, 130, 60))
        d.ellipse([fx - 3, fy - 3, fx + 3, fy + 3], fill=rnd.choice([col, (250, 230, 120), (250, 250, 250)]))
    put(img, lay, 0.5)

def crates(img, tx, ty):
    X, Y = tx * TS, ty * TS
    soft_shadow(img, (X, Y + 38, X + 52, Y + 50), 80, 4)
    lay = layer(); d = ImageDraw.Draw(lay)
    for (bx, by, s) in [(X + 2, Y + 18, 26), (X + 22, Y + 22, 24), (X + 10, Y - 2, 22)]:
        c = (160, 112, 66)
        d.rectangle([bx, by, bx + s, by + s], fill=c); d.rectangle([bx, by, bx + s, by + 5], fill=sh(c, 1.2))
        d.line([(bx, by + s), (bx + s, by + 5)], fill=sh(c, 0.7), width=2); d.rectangle([bx, by, bx + s, by + s], outline=sh(c, 0.6))
    put(img, lay, 0.5)

def barrel(img, tx, ty):
    X, Y = tx * TS + 24, ty * TS + 42
    soft_shadow(img, (X - 16, Y - 4, X + 18, Y + 6), 80, 3)
    lay = layer(); d = ImageDraw.Draw(lay)
    c = (146, 98, 58)
    d.rounded_rectangle([X - 14, Y - 34, X + 14, Y], 6, fill=c)
    hgrad(d, (X - 13, Y - 32, X + 13, Y - 2), sh(c, 0.85), sh(c, 0.8), mid=sh(c, 1.25))
    for yy in (Y - 28, Y - 8): d.rectangle([X - 14, yy, X + 14, yy + 3], fill=(90, 86, 84))
    d.ellipse([X - 13, Y - 38, X + 13, Y - 30], fill=sh(c, 1.15), outline=sh(c, 0.6))
    put(img, lay, 0.5)

def flagpole(img, tx, ty, color=(180, 40, 40)):
    HW.o_banner(img, tx, ty, 1, 1, color=color)

def pots_rack(img, tx, ty, w=2):
    """건조 중인 그릇들 (공방)"""
    X, Y = tx * TS, ty * TS
    soft_shadow(img, (X, Y + 38, X + w * TS + 6, Y + 50), 80, 4)
    lay = layer(); d = ImageDraw.Draw(lay)
    wood = (140, 96, 58)
    d.rectangle([X + 2, Y + 30, X + w * TS - 2, Y + 36], fill=wood); d.line([(X + 2, Y + 30), (X + w * TS - 2, Y + 30)], fill=sh(wood, 1.25))
    for lx in (X + 6, X + w * TS - 10): d.rectangle([lx, Y + 36, lx + 4, Y + 46], fill=sh(wood, 0.8))
    for i, x in enumerate(range(X + 10, X + w * TS - 10, 18)):
        c = (190, 170, 140) if i % 2 else (176, 140, 104)
        d.ellipse([x - 8, Y + 12, x + 8, Y + 30], fill=c); d.ellipse([x - 5, Y + 9, x + 5, Y + 15], fill=sh(c, 0.7))
        d.line([(x - 5, Y + 16), (x - 6, Y + 26)], fill=sh(c, 1.2))
    put(img, lay, 0.5)

def logs(img, tx, ty, w=3):
    """큰 통나무 더미 (대장도감 경판용 나무)"""
    X, Y = tx * TS, ty * TS
    soft_shadow(img, (X, Y + 40, X + w * TS + 6, Y + 52), 90, 4)
    lay = layer(); d = ImageDraw.Draw(lay)
    for row, (y, n) in enumerate([(Y + 30, 0), (Y + 14, 1)]):
        x0, x1 = X + 4 + row * 10, X + w * TS - 4 - row * 10
        for k in range(2 - row):
            yy = y - k * 0
        bark = (120, 80, 48)
        d.rounded_rectangle([x0, y - 9, x1, y + 9], 9, fill=bark)
        d.line([(x0 + 6, y - 6), (x1 - 6, y - 6)], fill=sh(bark, 1.3))
        d.ellipse([x1 - 12, y - 9, x1 + 4, y + 9], fill=(206, 160, 106), outline=(110, 72, 42))
        d.ellipse([x1 - 7, y - 4, x1 - 1, y + 4], outline=(170, 120, 76))
    put(img, lay, 0.5)

def bell_post(img, tx, ty):
    """사찰 범종각 대신 작은 종 걸이"""
    X, Y = tx * TS + 24, ty * TS + 44
    soft_shadow(img, (X - 26, Y - 4, X + 28, Y + 8), 80, 4)
    lay = layer(); d = ImageDraw.Draw(lay)
    wood = (150, 70, 50)
    d.rectangle([X - 24, Y - 70, X - 19, Y], fill=wood); d.rectangle([X + 19, Y - 70, X + 24, Y], fill=wood)
    d.rectangle([X - 28, Y - 76, X + 28, Y - 68], fill=(60, 110, 96)); d.line([(X - 28, Y - 76), (X + 28, Y - 76)], fill=(100, 160, 140))
    b = (96, 110, 92)
    d.line([(X, Y - 68), (X, Y - 58)], fill=(60, 60, 60))
    d.polygon([(X - 9, Y - 58), (X + 9, Y - 58), (X + 13, Y - 26), (X - 13, Y - 26)], fill=b)
    d.ellipse([X - 13, Y - 30, X + 13, Y - 22], fill=sh(b, 0.8))
    d.line([(X - 6, Y - 54), (X - 9, Y - 30)], fill=sh(b, 1.35), width=2)
    put(img, lay, 0.5)

OBJ = {'pine': pine, 'lantern': stone_lantern, 'dmu': dmu, 'jangdok': jangdok, 'well': well, 'woodpile': woodpile,
       'haystack': haystack, 'pagoda': pagoda, 'bush': bush, 'rock': rock, 'bamboo': bamboo, 'flowerbed': flowerbed,
       'crates': crates, 'barrel': barrel, 'flag': flagpole, 'pots': pots_rack, 'logs': logs, 'bell': bell_post,
       'plant': lambda img, tx, ty, **k: obj_plant(img, tx, ty)}

# 방마다 바깥 마당 구성.  위치는 (물건, 방에서 떨어진 칸 d(0=벽 바로 옆), 줄 y, 추가 인자, 차지하는 폭)
#  d 0~2: 16:9 화면부터 보이는 곳 / 3~5: 아주 넓은 화면에서만 보이는 곳
SIDES = {
    'palace': dict(ground='bakseok', top='damjang', both=[('lantern', 1, 4), ('dmu', 1, 7), ('pine', 4, 5), ('bush', 3, 11, {'flowers': (240, 120, 150)}),
                                                     ('flowerbed', 1, 11, {'w': 2}, 2), ('rock', 5, 8), ('bush', 4, 2)]),
    'workshop': dict(ground='earth', top='earthwall', both=[('pots', 0, 4, {'w': 2}, 2), ('woodpile', 0, 6, {'w': 2}, 2), ('jangdok', 1, 10, {'w': 2}, 2),
                                                        ('pine', 4, 5), ('well', 3, 2, {}, 2), ('haystack', 4, 11), ('rock', 5, 8)]),
    'mansion': dict(ground='earth', top='damjang', both=[('jangdok', 0, 3, {'w': 3}, 3), ('bush', 1, 6, {'flowers': (250, 240, 120)}), ('pine', 4, 7),
                                                     ('bamboo', 1, 11), ('flowerbed', 3, 11, {'w': 2}, 2), ('lantern', 5, 3)]),
    'ganghwa': dict(ground='grass', top='palisade', both=[('crates', 0, 4), ('barrel', 1, 6), ('flag', 2, 3, {'color': (180, 40, 40)}), ('haystack', 1, 11),
                                                      ('pine', 4, 6), ('pine', 3, 11, {'seed': 3}), ('rock', 5, 3), ('bush', 5, 8)]),
    'dojang': dict(ground='darkearth', top='earthwall', both=[('logs', 0, 4, {'w': 3}, 3), ('woodpile', 0, 6, {'w': 2}, 2), ('barrel', 2, 11),
                                                          ('pine', 4, 7), ('haystack', 4, 11), ('bush', 4, 3), ('rock', 1, 11)]),
    'yuan': dict(ground='bakseok', top='damjang', both=[('lantern', 1, 4), ('dmu', 1, 7), ('pine', 4, 5), ('flowerbed', 1, 11, {'w': 2}, 2),
                                                  ('bush', 4, 11, {'flowers': (250, 250, 250)}), ('rock', 5, 8), ('bush', 3, 2)]),
    'temple': dict(ground='stone', top='damjang', both=[('lantern', 1, 4), ('pagoda', 2, 7, {}, 2), ('pine', 5, 5), ('bell', 1, 11),
                                                    ('bamboo', 4, 11), ('bush', 3, 2), ('rock', 5, 9)]),
    'ending': dict(ground='bakseok', top='damjang', both=[('lantern', 1, 4), ('dmu', 1, 7), ('pine', 4, 5), ('flowerbed', 1, 11, {'w': 2}, 2),
                                                    ('bush', 4, 11, {'flowers': (240, 120, 150)}), ('rock', 5, 8), ('lantern', 4, 2)]),
}

# 오른쪽 마당은 왼쪽과 다르게 (없으면 왼쪽과 같은 구성)
RIGHT = {
    'palace': [('lantern', 1, 4), ('dmu', 1, 7), ('bamboo', 4, 3), ('pine', 4, 11, {'big': 0.9}), ('bush', 2, 11, {'flowers': (250, 240, 120)}), ('rock', 5, 7)],
    'workshop': [('jangdok', 0, 3, {'w': 3}, 3), ('pots', 0, 6, {'w': 2}, 2), ('haystack', 1, 11), ('pine', 4, 11), ('woodpile', 3, 7, {'w': 2}, 2), ('bush', 5, 4)],
    'mansion': [('lantern', 1, 3), ('well', 0, 6, {}, 2), ('pine', 4, 4), ('jangdok', 0, 10, {'w': 2}, 2), ('bamboo', 4, 11), ('rock', 5, 8)],
    'ganghwa': [('barrel', 0, 4), ('crates', 1, 6), ('flag', 2, 4, {'color': (40, 80, 160)}), ('pine', 4, 4), ('haystack', 2, 11), ('pine', 5, 11, {'seed': 9}), ('bush', 4, 7)],
    'dojang': [('woodpile', 0, 4, {'w': 2}, 2), ('logs', 0, 6, {'w': 3}, 3), ('pine', 4, 11), ('barrel', 1, 11), ('bush', 4, 3), ('haystack', 5, 7)],
    'yuan': [('lantern', 1, 4), ('dmu', 1, 7), ('bamboo', 4, 3), ('pine', 4, 11, {'big': 0.9}), ('flowerbed', 1, 11, {'w': 2, 'col': (180, 140, 240)}, 2), ('rock', 5, 7)],
    'temple': [('lantern', 1, 4), ('bamboo', 3, 3), ('pine', 4, 7), ('bush', 1, 7, {'flowers': (250, 250, 250)}), ('lantern', 1, 11), ('pine', 4, 11, {'big': 0.85, 'seed': 4})],
    'ending': [('lantern', 1, 4), ('dmu', 1, 7), ('bamboo', 4, 3), ('pine', 4, 10), ('flowerbed', 0, 11, {'w': 2}, 2), ('lantern', 4, 7)],
}

def render_side(room, side):
    """side='left'|'right'. 816 캔버스의 왼쪽 288px에 그린 뒤 잘라 냄"""
    spec = SIDES[room['key']]
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    seed = room['map'] * 10 + (1 if side == 'left' else 2)
    ground(img, spec['ground'], (0, 96, MW_PX, H), seed)
    has_door = (side == 'left' and 'left' in room['doors']) or (side == 'right' and ('right' in room['doors'] or 'right_gate' in room['doors']))
    if has_door:
        path_row(img, spec['ground'], 0, MW_PX, seed)
    elif spec['ground'] == 'grass':
        pass
    t = spec['top']
    if t == 'damjang':
        cap = (70, 66, 74) if room['key'] != 'yuan' else (56, 56, 70)
        top_damjang(img, 0, MW_PX, seed, cap=cap)
    elif t == 'earthwall': top_earthwall(img, 0, MW_PX, seed)
    elif t == 'palisade': top_palisade(img, 0, MW_PX, seed)
    # 위쪽 담장 그림자
    sl = layer(); ImageDraw.Draw(sl).rectangle([0, 96, MW_PX, 106], fill=(0, 0, 0, 70))
    img.alpha_composite(sl.filter(ImageFilter.GaussianBlur(3)))
    items = []
    for it in (RIGHT.get(room['key'], spec['both']) if side == 'right' else spec['both']):
        name, dist, y = it[0], it[1], it[2]
        kw = it[3] if len(it) > 3 else {}
        w = it[4] if len(it) > 4 else 1
        if has_door and y in (9,) and name not in ('pine',):
            continue
        tx = (MARGIN - dist - w) if side == 'left' else dist
        items.append((y, name, tx, kw))
    for y, name, tx, kw in sorted(items, key=lambda i: i[0]):
        kw = dict(kw)
        if name in ('pine', 'bush', 'rock', 'bamboo') and 'seed' not in kw:
            kw['seed'] = seed + tx
        OBJ[name](img, tx, y, **kw)
    return img.crop((0, 0, MW_PX, H))

def render_wide(room):
    core = HW.render_room(room).convert('RGBA')
    img = Image.new('RGBA', (WIDE_W, H), (0, 0, 0, 255))
    img.paste(render_side(room, 'left'), (0, 0))
    img.paste(render_side(room, 'right'), (MW_PX + W, 0))
    img.alpha_composite(core, (MW_PX, 0))
    d = ImageDraw.Draw(img)
    # 건물 바깥 기단(돌 받침)과 처마 그림자
    for x0, sgn in ((MW_PX, -1), (MW_PX + W, 1)):
        sh_l = Image.new('RGBA', img.size, (0, 0, 0, 0)); sd = ImageDraw.Draw(sh_l)
        if sgn < 0: sd.rectangle([x0 - 16, 90, x0, H], fill=(0, 0, 0, 80))
        else: sd.rectangle([x0, 90, x0 + 16, H], fill=(0, 0, 0, 80))
        img.alpha_composite(sh_l.filter(ImageFilter.GaussianBlur(5)))
        d = ImageDraw.Draw(img)
        s = (164, 156, 142)
        if sgn < 0: bx0, bx1 = x0 - 8, x0
        else: bx0, bx1 = x0, x0 + 8
        for y in range(96, H, 16):
            c = sh(s, 0.92 + ((y // 16) % 3) * 0.05)
            d.rectangle([bx0, y, bx1 - 1, min(y + 15, H - 1)], fill=c, outline=sh(c, 0.7))
        # 처마 끝 (지붕 모서리)
        if sgn < 0: d.polygon([(x0, 0), (x0, 100), (x0 - 10, 92), (x0 - 10, 0)], fill=(44, 36, 40))
        else: d.polygon([(x0, 0), (x0, 100), (x0 + 10, 92), (x0 + 10, 0)], fill=(44, 36, 40))
    return img.convert('RGB')

if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    only = sys.argv[2:] if len(sys.argv) > 2 else None
    for room in MW.ROOMS:
        if only and room['key'] not in only: continue
        render_wide(room).save(os.path.join(out, room['parallax'] + '.png'))
    print('wide rooms ok')
