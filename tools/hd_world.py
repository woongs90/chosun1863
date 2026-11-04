"""고화질(48px 원본) 방 8개 원경 그림. 방 배치는 make_world.ROOMS를 그대로 씁니다."""
import os, sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hd_art import (TS, W, H, sh, mix, layer, outline, soft_shadow, noise_fill, vgrad, hgrad,
                    floor_maru, rug as rug_hd, DAN_GREEN, DAN_BLUE, DAN_RED, DAN_WHITE, PILLAR,
                    obj_screen_hunyo, obj_hanging_scroll, obj_wall_map, obj_throne, obj_desk as _desk_basic,
                    obj_chest, obj_cabinet, obj_plant, obj_gate_door_right)
import make_world as MW

WOOD = (150, 98, 58); WOOD_L = (196, 140, 92); WOOD_D = (100, 62, 36)
PAPER = (244, 236, 214)

def put(base, lay, strength=0.45):
    base.alpha_composite(outline(lay, strength))

def wood_top(d, box, c=WOOD, seed=0):
    x0, y0, x1, y1 = box
    d.rectangle([x0, y0, x1, y1], fill=c)
    d.line([(x0, y0), (x1, y0)], fill=sh(c, 1.3)); d.line([(x0, y0 + 1), (x1, y0 + 1)], fill=sh(c, 1.15))
    rnd = random.Random(seed)
    for gx in range(x0 + 4, x1 - 2, rnd.randint(7, 11)):
        d.line([(gx, y0 + 3), (gx + rnd.randint(2, 6), y1 - 2)], fill=sh(c, 0.9))

# ======================================================================== 바닥
def floor_earth(img, box, base, seed=2):
    x0, y0, x1, y1 = box
    rng = np.random.default_rng(seed)
    h, w = y1 - y0, x1 - x0
    n = rng.normal(0, 1, (h // 4 + 1, w // 4 + 1))
    n = np.kron(n, np.ones((4, 4)))[:h, :w]
    fine = rng.integers(-6, 7, (h, w))
    arr = np.clip(np.array(base)[None, None, :] + (n * 7 + fine)[:, :, None], 0, 255).astype(np.uint8)
    img.paste(Image.fromarray(arr, 'RGB'), (x0, y0))
    d = ImageDraw.Draw(img)
    rnd = random.Random(seed)
    for _ in range(90):
        x, y = rnd.randrange(x0, x1 - 3), rnd.randrange(y0, y1 - 3)
        c = sh(base, rnd.choice([0.78, 1.15]))
        d.ellipse([x, y, x + rnd.randint(2, 4), y + rnd.randint(1, 3)], fill=c)
    for _ in range(14):   # 짚 부스러기
        x, y = rnd.randrange(x0, x1 - 8), rnd.randrange(y0, y1 - 4)
        d.line([(x, y), (x + rnd.randint(4, 8), y + rnd.randint(-2, 2))], fill=(206, 176, 110))

def floor_stone(img, box, base, seed=3, size=24):
    x0, y0, x1, y1 = box
    d = ImageDraw.Draw(img)
    rnd = random.Random(seed)
    for ty in range(y0, y1, size):
        off = (size // 2) if ((ty - y0) // size) % 2 else 0
        for tx in range(x0 - off, x1, size):
            c = sh(base, 0.92 + rnd.random() * 0.12)
            a, b = max(tx, x0), min(tx + size, x1)
            if b <= a: continue
            vgrad(d, (a, ty, b, min(ty + size, y1)), sh(c, 1.06), sh(c, 0.95))
            d.line([(a, ty), (b - 1, ty)], fill=sh(c, 1.18))
            d.line([(a, ty + size - 1), (b - 1, ty + size - 1)], fill=sh(c, 0.7))
            if tx + size <= x1: d.line([(tx + size - 1, ty), (tx + size - 1, ty + size - 1)], fill=sh(c, 0.72))
            if tx >= x0: d.line([(tx, ty), (tx, ty + size - 1)], fill=sh(c, 1.1))
            for _ in range(3):
                px, py = rnd.randrange(a, b), rnd.randrange(ty, min(ty + size, y1))
                d.point((px, py), fill=sh(c, 0.85))

def floor_jeondol(img, box, base, seed=4):
    floor_stone(img, box, base, seed, size=48)
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    for ty in range(y0, y1, 48):
        for tx in range(x0, x1, 48):
            d.rectangle([tx + 6, ty + 6, tx + 41, ty + 41], outline=sh(base, 0.9))

def floor_grass(img, box, base, seed=5):
    x0, y0, x1, y1 = box
    rng = np.random.default_rng(seed)
    h, w = y1 - y0, x1 - x0
    n = np.kron(rng.normal(0, 1, (h // 6 + 1, w // 6 + 1)), np.ones((6, 6)))[:h, :w]
    arr = np.clip(np.array(base)[None, None, :] + (n * 9)[:, :, None] + rng.integers(-5, 6, (h, w, 1)), 0, 255).astype(np.uint8)
    img.paste(Image.fromarray(arr, 'RGB'), (x0, y0))
    d = ImageDraw.Draw(img)
    rnd = random.Random(seed)
    for _ in range(420):
        x, y = rnd.randrange(x0, x1 - 2), rnd.randrange(y0 + 3, y1)
        c = sh(base, rnd.choice([0.75, 1.25, 1.35]))
        d.line([(x, y), (x + rnd.choice([-1, 0, 1]), y - rnd.randint(2, 4))], fill=c)
    # 흙길 (9번째 줄)
    py0, py1 = 9 * TS - 6, 10 * TS + 6
    for y in range(py0, py1):
        edge = min(y - py0, py1 - y)
        for x in range(x0, x1, 1):
            pass
    path = Image.new('RGB', (x1 - x0, py1 - py0), (158, 128, 90))
    noise_fill(path, (0, 0, x1 - x0, py1 - py0), (158, 128, 90), 9, seed=6)
    mask = Image.new('L', path.size, 0)
    md = ImageDraw.Draw(mask)
    for x in range(0, path.size[0], 6):
        top = 4 + int(3 * math.sin(x / 23)); bot = path.size[1] - 4 - int(3 * math.sin(x / 31 + 1))
        md.rectangle([x, top, x + 6, bot], fill=255)
    img.paste(path, (x0, py0), mask.filter(ImageFilter.GaussianBlur(1.5)))
    d = ImageDraw.Draw(img)
    for _ in range(40):
        x, y = rnd.randrange(x0, x1 - 4), rnd.randrange(py0 + 6, py1 - 6)
        d.ellipse([x, y, x + 3, y + 2], fill=(128, 104, 74))
    # 꽃
    for _ in range(26):
        x, y = rnd.randrange(x0 + 4, x1 - 4), rnd.randrange(y0 + 6, y1 - 4)
        if py0 - 4 < y < py1 + 4: continue
        c = rnd.choice([(250, 240, 120), (250, 250, 250), (240, 150, 170)])
        for dx, dy in ((0, -1), (1, 0), (0, 1), (-1, 0)):
            d.point((x + dx, y + dy), fill=c)
        d.point((x, y), fill=(230, 180, 60))

def floor(img, kind, base, seed):
    box = (TS, 2 * TS, 16 * TS, 12 * TS)
    if kind == 'maru': floor_maru(img, box, base, seed)
    elif kind == 'earth': floor_earth(img, box, base, seed)
    elif kind == 'stone': floor_stone(img, box, base, seed)
    elif kind == 'jeondol': floor_jeondol(img, box, base, seed)
    elif kind == 'grass': floor_grass(img, box, base, seed)

# ======================================================================== 벽
def rafters(d, y_bottom, top_col):
    vgrad(d, (0, 0, W, y_bottom - 6), sh(top_col, 0.7), sh(top_col, 1.05))
    for x in range(0, W, 8):
        d.line([(x, 0), (x, y_bottom - 7)], fill=sh(top_col, 0.78))
        d.line([(x + 1, 0), (x + 1, y_bottom - 7)], fill=sh(top_col, 1.15))

def rafter_ends(d, y, dan=DAN_GREEN):
    for x in range(4, W, 12):
        cx = x + 2
        d.ellipse([cx - 6, y - 6, cx + 6, y + 6], fill=dan, outline=sh(dan, 0.5))
        d.ellipse([cx - 4, y - 4, cx + 4, y + 4], fill=DAN_WHITE)
        d.ellipse([cx - 2, y - 2, cx + 2, y + 2], fill=DAN_RED)

def giwa_top(d, top_col):
    vgrad(d, (0, 0, W, 34), sh(top_col, 0.8), sh(top_col, 1.1))
    for row, y in enumerate(range(-4, 34, 7)):
        off = 6 if row % 2 else 0
        for x in range(-12 + off, W, 12):
            d.chord([x, y, x + 12, y + 10], 180, 360, fill=sh(top_col, 1.25), outline=sh(top_col, 0.62))
            d.line([(x + 2, y + 2), (x + 6, y + 1)], fill=sh(top_col, 1.5))

def danchung_beam(d, y, h, dan1=DAN_GREEN, dan2=DAN_BLUE):
    vgrad(d, (0, y, W, y + h), sh(dan1, 1.15), sh(dan1, 0.85))
    for x in range(0, W, 24):
        d.rectangle([x + 2, y + 3, x + 21, y + h - 4], fill=dan2)
        d.rectangle([x + 5, y + 5, x + 18, y + h - 6], fill=DAN_WHITE)
        d.ellipse([x + 9, y + 4, x + 14, y + h - 5], fill=DAN_RED)
    d.line([(0, y + h - 1), (W, y + h - 1)], fill=sh(dan1, 0.45))

def side_walls(d, top_col, trim):
    for (bx, by, bw, bh) in [(0, 96, TS, 12 * TS - 96), (16 * TS, 96, TS, 12 * TS - 96), (0, 12 * TS, W, TS)]:
        vgrad(d, (bx, by, bx + bw, by + bh), sh(top_col, 1.1), sh(top_col, 0.85))
        for yy in range(by + 6, by + bh, 12):
            d.line([(bx + 3, yy), (bx + bw - 4, yy)], fill=sh(top_col, 0.95))
    d.rectangle([TS - 6, 96, TS - 1, 12 * TS - 1], fill=trim); d.line([(TS - 6, 96), (TS - 6, 12 * TS)], fill=sh(trim, 1.25))
    d.rectangle([16 * TS, 96, 16 * TS + 5, 12 * TS - 1], fill=sh(trim, 0.8))
    d.rectangle([TS, 12 * TS, 16 * TS + 5, 12 * TS + 5], fill=sh(trim, 0.8))

def walls(img, th):
    d = ImageDraw.Draw(img)
    kind = th['face_kind']; top = th['top']
    if th.get('top_pat') == 'giwa':
        giwa_top(d, top)
    else:
        rafters(d, 46, top)
    if kind in ('palace', 'temple'):
        rafter_ends(d, 40, th.get('dan1', DAN_GREEN))
        danchung_beam(d, 48, 14, th.get('dan1', DAN_GREEN), th.get('dan2', DAN_BLUE))
        noise_fill(img, (0, 62, W, 90), th['face'], 5, seed=3)
        d = ImageDraw.Draw(img)
        vgrad(d, (0, 62, W, 68), sh(th['face'], 0.82), th['face'])
        vgrad(d, (0, 90, W, 96), (120, 70, 44), (84, 48, 30)); d.line([(0, 90), (W, 90)], fill=(150, 96, 60))
        post = th.get('post', PILLAR)
        step = 3 * TS if kind == 'palace' else 4 * TS
        for x in range(0, W, step):
            hgrad(d, (x + 2, 34, x + 14, 96), sh(post, 0.75), sh(post, 0.7), mid=sh(post, 1.35))
            d.rectangle([x + 1, 34, x + 14, 37], fill=th.get('dan1', DAN_GREEN))
    elif kind == 'earth':
        rafter_ends(d, 40, (120, 90, 60))
        noise_fill(img, (0, 48, W, 92), th['face'], 9, seed=7)
        d = ImageDraw.Draw(img)
        rnd = random.Random(8)
        for _ in range(160):
            x, y = rnd.randrange(0, W - 6), rnd.randrange(50, 90)
            d.line([(x, y), (x + rnd.randint(3, 6), y + rnd.randint(-1, 1))], fill=(214, 186, 120))
        for x in range(0, W, 2 * TS):
            hgrad(d, (x, 46, x + 10, 96), (96, 66, 40), (80, 54, 32), mid=(140, 100, 64))
        d.rectangle([0, 46, W, 50], fill=(112, 78, 48)); d.line([(0, 46), (W, 46)], fill=(150, 108, 70))
        vgrad(d, (0, 90, W, 96), (110, 80, 52), (80, 56, 34))
    elif kind == 'wood':
        rafter_ends(d, 40, (120, 80, 50))
        for x in range(0, W, 6):
            c = sh(th['face'], 0.92 + ((x // 6) % 3) * 0.06)
            vgrad(d, (x, 48, x + 6, 92), sh(c, 1.08), sh(c, 0.9))
            d.line([(x, 48), (x, 92)], fill=sh(c, 0.7))
        d.rectangle([0, 46, W, 52], fill=sh(th['face'], 0.6)); d.line([(0, 46), (W, 46)], fill=sh(th['face'], 0.85))
        vgrad(d, (0, 90, W, 96), sh(th['face'], 0.6), sh(th['face'], 0.45))
    elif kind == 'palisade':
        vgrad(d, (0, 0, W, 50), (60, 96, 70), (40, 74, 52))
        rnd = random.Random(9)
        for _ in range(60):     # 나무 꼭대기
            x = rnd.randrange(-10, W); y = rnd.randrange(-6, 26); r = rnd.randint(10, 18)
            d.ellipse([x, y, x + r * 2, y + r], fill=rnd.choice([(52, 104, 64), (70, 124, 76), (44, 90, 58)]))
        for x in range(0, W, 10):
            c = sh(th['face'], 0.9 + ((x // 10) % 2) * 0.12)
            hgrad(d, (x, 52, x + 9, 96), sh(c, 0.8), sh(c, 0.75), mid=sh(c, 1.25))
            d.polygon([(x, 52), (x + 9, 52), (x + 4, 42)], fill=sh(c, 1.1), outline=sh(c, 0.6))
        d.rectangle([0, 70, W, 74], fill=sh(th['face'], 0.55)); d.line([(0, 70), (W, 70)], fill=sh(th['face'], 0.8))
    side_walls(ImageDraw.Draw(img), th['top'] if kind != 'palisade' else (52, 84, 58), (120, 70, 44) if kind != 'palisade' else (110, 80, 50))

def side_door(img, side, th):
    lay = layer(); d = ImageDraw.Draw(lay)
    x = 0 if side == 'left' else 16 * TS
    y = 9 * TS
    fl = th['floor_col']
    vgrad(d, (x, y - 6, x + TS, y + TS + 6), sh(fl, 0.75), sh(fl, 0.6))
    d.rectangle([x, y - 10, x + TS - 1, y - 6], fill=(96, 60, 36)); d.rectangle([x, y + TS + 6, x + TS - 1, y + TS + 10], fill=(96, 60, 36))
    d.line([(x, y - 10), (x + TS - 1, y - 10)], fill=(150, 104, 66))
    cx, cy = x + 24, y + 24
    arrow = [(cx + 6, cy - 8), (cx + 6, cy + 8), (cx - 6, cy)] if side == 'left' else [(cx - 6, cy - 8), (cx - 6, cy + 8), (cx + 6, cy)]
    d.polygon(arrow, fill=(250, 224, 150))
    put(img, lay, 0.55)

# ======================================================================== 물건
def o_desk(img, x, y, w, h, things=('paper',), **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS + 4, y * TS + 8
    ww = w * TS - 8
    soft_shadow(img, (X + 4, Y + 26, X + ww + 6, Y + 40), 80, 4)
    wood_top(d, (X, Y, X + ww, Y + 18), WOOD, seed=x * 7 + y)
    d.rectangle([X, Y + 18, X + ww, Y + 24], fill=WOOD_D)
    for lx in (X + 2, X + ww - 7):
        d.rectangle([lx, Y + 24, lx + 5, Y + 32], fill=sh(WOOD_D, 0.9))
    for t in things:
        if t == 'paper':
            d.rectangle([X + 8, Y + 3, X + 30, Y + 14], fill=PAPER)
            for j in (6, 9, 12): d.line([(X + 11, Y + j), (X + 27 - (j % 4), Y + j)], fill=(100, 90, 86))
        elif t == 'ink':
            d.rectangle([X + ww - 24, Y + 4, X + ww - 10, Y + 13], fill=(46, 46, 54)); d.ellipse([X + ww - 21, Y + 6, X + ww - 15, Y + 10], fill=(20, 20, 26))
            d.line([(X + ww - 34, Y + 13), (X + ww - 28, Y + 4)], fill=(120, 80, 40), width=2)
        elif t == 'book':
            d.rectangle([X + 10, Y + 2, X + 40, Y + 14], fill=(236, 222, 186)); d.line([(X + 25, Y + 2), (X + 25, Y + 14)], fill=(150, 110, 70))
            for j in (5, 8, 11):
                d.line([(X + 13, Y + j), (X + 22, Y + j)], fill=(110, 100, 90)); d.line([(X + 28, Y + j), (X + 37, Y + j)], fill=(110, 100, 90))
            d.rectangle([X + 44, Y + 4, X + 60, Y + 13], fill=(70, 70, 120)); d.line([(X + 44, Y + 4), (X + 60, Y + 4)], fill=(120, 120, 170))
        elif t == 'scrolls':
            for i in range(3 if ww > 90 else 2):
                sx = X + 6 + i * 34
                d.rectangle([sx, Y + 4, sx + 26, Y + 12], fill=PAPER)
                d.rectangle([sx - 2, Y + 3, sx + 1, Y + 13], fill=(130, 80, 50)); d.rectangle([sx + 25, Y + 3, sx + 28, Y + 13], fill=(130, 80, 50))
                d.line([(sx + 4, Y + 8), (sx + 20, Y + 8)], fill=(110, 100, 90))
        elif t == 'board':
            d.rectangle([X + 8, Y + 2, X + ww - 8, Y + 14], fill=(196, 156, 104))
            d.line([(X + 8, Y + 2), (X + ww - 8, Y + 2)], fill=(226, 190, 140))
            for i in range(X + 11, X + ww - 11, 4):
                for j in (Y + 5, Y + 9):
                    d.rectangle([i, j, i + 2, j + 2], fill=(130, 92, 58))
        elif t == 'map':
            d.rectangle([X + 6, Y + 2, X + ww - 6, Y + 15], fill=(228, 212, 172))
            d.polygon([(X + 20, Y + 13), (X + 16, Y + 8), (X + 26, Y + 4), (X + 44, Y + 4), (X + 50, Y + 9), (X + 40, Y + 13)], fill=(150, 182, 122))
            d.rectangle([X + ww - 26, Y + 3, X + ww - 7, Y + 14], fill=(150, 180, 210))
            d.line([(X + ww - 30, Y + 4), (X + ww - 30, Y + 9)], fill=(120, 80, 40)); d.polygon([(X + ww - 30, Y + 4), (X + ww - 24, Y + 6), (X + ww - 30, Y + 8)], fill=(200, 40, 40))
    put(img, lay)

def o_chest(img, x, y, w, h, **k): obj_chest(img, x, y, w)
def o_cabinet(img, x, y, w, h, **k): obj_cabinet(img, x, y, w)
def o_plant(img, x, y, w, h, **k): obj_plant(img, x, y)
def o_throne(img, x, y, w, h, **k): obj_throne(img, x, y, w, h)
def o_screen(img, x, y, w, h, **k): obj_screen_hunyo(img, x, y, w)

def o_pillar(img, x, y, w, h, color=PILLAR, **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS, y * TS; cx = X + 24
    soft_shadow(img, (cx - 14, Y + 34, cx + 22, Y + 50), 90, 4)
    d.polygon([(cx - 18, Y + 44), (cx - 14, Y + 34), (cx + 14, Y + 34), (cx + 18, Y + 44), (cx + 14, Y + 47), (cx - 14, Y + 47)], fill=(150, 144, 132))
    d.line([(cx - 14, Y + 34), (cx + 14, Y + 34)], fill=(186, 180, 168))
    hgrad(d, (cx - 11, Y - 40, cx + 11, Y + 38), sh(color, 0.7), sh(color, 0.66), mid=sh(color, 1.4))
    d.rectangle([cx - 13, Y - 44, cx + 12, Y - 36], fill=DAN_GREEN); d.rectangle([cx - 13, Y - 40, cx + 12, Y - 38], fill=DAN_WHITE)
    put(img, lay)

def o_wall(img, x, y, w, h, kind='scroll', figure=False, **k):
    X, Y = x * TS, y * TS
    if kind == 'scroll' and figure:
        obj_hanging_scroll(img, x, y); return
    if kind == 'map':
        obj_wall_map(img, x, y, w); return
    lay = layer(); d = ImageDraw.Draw(lay)
    if kind == 'scroll':
        d.rectangle([X + 8, Y + 2, X + 40, Y + 5], fill=(80, 46, 30))
        d.rectangle([X + 10, Y + 5, X + 38, Y + 40], fill=(214, 190, 140)); d.rectangle([X + 13, Y + 8, X + 35, Y + 37], fill=PAPER)
        for j in range(3): d.line([(X + 18 + j * 6, Y + 11), (X + 18 + j * 6, Y + 33)], fill=(60, 50, 50), width=2)
        d.rectangle([X + 7, Y + 40, X + 41, Y + 44], fill=(80, 46, 30))
    elif kind in ('paper', 'hanja'):
        ww = w * TS - 14
        d.rectangle([X + 7, Y + 5, X + 7 + ww, Y + 39], fill=(110, 70, 44))
        d.rectangle([X + 10, Y + 8, X + 4 + ww, Y + 36], fill=PAPER)
        if kind == 'paper':
            for j in range(Y + 12, Y + 34, 4):
                d.line([(X + 14, j), (X + ww - 2 - ((j // 4) % 3) * 6, j)], fill=(96, 86, 80))
            d.ellipse([X + ww - 8, Y + 28, X + ww - 2, Y + 34], fill=(190, 50, 46))
        else:
            for i in range(X + 14, X + ww - 4, 12):
                for j in (Y + 12, Y + 24):
                    d.rectangle([i, j, i + 8, j + 8], outline=(60, 50, 50)); d.line([(i + 4, j + 1), (i + 4, j + 7)], fill=(60, 50, 50)); d.line([(i + 1, j + 4), (i + 7, j + 4)], fill=(60, 50, 50))
    elif kind == 'grid':
        ww = w * TS - 10
        d.rectangle([X + 5, Y + 4, X + 5 + ww, Y + 40], fill=(110, 70, 44)); d.rectangle([X + 8, Y + 7, X + 2 + ww, Y + 37], fill=(226, 214, 176))
        d.polygon([(X + 20, Y + 34), (X + 16, Y + 18), (X + 40, Y + 10), (X + 90, Y + 12), (X + 110, Y + 22), (X + 96, Y + 34)], fill=(176, 196, 150))
        d.rectangle([X + ww - 26, Y + 8, X + ww, Y + 26], fill=(150, 180, 210))
        for i in range(X + 10, X + ww, 18): d.line([(i, Y + 7), (i, Y + 37)], fill=(160, 140, 110))
        for j in range(Y + 13, Y + 37, 8): d.line([(X + 8, j), (X + ww, j)], fill=(160, 140, 110))
        for (mx, my) in [(X + 30, Y + 22), (X + 70, Y + 16), (X + 100, Y + 28)]:
            d.polygon([(mx, my - 3), (mx + 3, my), (mx, my + 3), (mx - 3, my)], fill=(80, 60, 60))
        d.ellipse([X + 54, Y + 26, X + 59, Y + 31], fill=(60, 80, 160))
    elif kind == 'painting':
        ww = w * TS - 10
        d.rectangle([X + 5, Y + 3, X + 5 + ww, Y + 41], fill=(110, 66, 40)); d.rectangle([X + 9, Y + 7, X + 1 + ww, Y + 37], fill=(222, 208, 170))
        d.rectangle([X + 9, Y + 26, X + 1 + ww, Y + 37], fill=(140, 166, 116))
        d.polygon([(X + 22, Y + 26), (X + 38, Y + 13), (X + 54, Y + 26)], fill=(160, 64, 54)); d.rectangle([X + 26, Y + 26, X + 50, Y + 33], fill=(196, 160, 110))
        for i, c in enumerate([(70, 70, 90), (70, 70, 90), (60, 60, 140), (140, 40, 40)]):
            px = X + 62 + i * 7
            d.ellipse([px, Y + 22, px + 4, Y + 26], fill=(236, 200, 166)); d.rectangle([px, Y + 26, px + 4, Y + 33], fill=c)
    elif kind == 'portraits':
        for i in range(w):
            px = X + i * TS + 6
            d.rectangle([px, Y + 3, px + 36, Y + 42], fill=(110, 66, 40)); d.rectangle([px + 3, Y + 6, px + 33, Y + 39], fill=(226, 212, 176))
            d.ellipse([px + 12, Y + 9, px + 24, Y + 21], fill=(236, 200, 166)); d.rectangle([px + 11, Y + 7, px + 25, Y + 11], fill=(30, 26, 34))
            col = [(120, 70, 60), (70, 90, 130), (90, 112, 70), (160, 40, 40)][i % 4]
            d.polygon([(px + 7, Y + 38), (px + 10, Y + 22), (px + 26, Y + 22), (px + 29, Y + 38)], fill=col)
    elif kind == 'hair':
        d.rectangle([X + 6, Y + 3, X + 42, Y + 42], fill=(110, 66, 40)); d.rectangle([X + 9, Y + 6, X + 39, Y + 39], fill=(230, 218, 184))
        d.ellipse([X + 16, Y + 9, X + 32, Y + 25], fill=(236, 200, 166))
        d.arc([X + 16, Y + 9, X + 32, Y + 25], 200, 340, fill=(40, 30, 30), width=3)
        d.line([(X + 31, Y + 16), (X + 34, Y + 34)], fill=(40, 30, 30), width=3)
        d.polygon([(X + 14, Y + 38), (X + 17, Y + 25), (X + 31, Y + 25), (X + 34, Y + 38)], fill=(110, 90, 140))
    put(img, lay, 0.5)

def o_jar(img, x, y, w, h, content=None, color=(120, 80, 50), **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS, y * TS; cx = X + 24
    soft_shadow(img, (cx - 16, Y + 36, cx + 20, Y + 48), 80, 4)
    d.ellipse([cx - 17, Y + 10, cx + 17, Y + 44], fill=color)
    d.chord([cx - 17, Y + 10, cx + 17, Y + 44], 90, 270, fill=sh(color, 1.18))
    d.ellipse([cx - 10, Y + 4, cx + 10, Y + 14], fill=sh(color, 0.8)); d.ellipse([cx - 8, Y + 5, cx + 8, Y + 12], fill=sh(color, 0.55))
    if content: d.ellipse([cx - 7, Y + 6, cx + 7, Y + 11], fill=content); d.point((cx - 3, Y + 7), fill=sh(content, 1.2))
    d.line([(cx - 11, Y + 20), (cx - 12, Y + 32)], fill=sh(color, 1.45), width=2)
    d.arc([cx - 15, Y + 22, cx + 15, Y + 30], 0, 180, fill=sh(color, 0.8))
    put(img, lay)

def vase_shape(d, cx, top, s, col=(124, 172, 152)):
    pts = [(cx - 4 * s, top), (cx + 4 * s, top), (cx + 5 * s, top + 3 * s), (cx + 12 * s, top + 9 * s), (cx + 12 * s, top + 17 * s),
           (cx + 8 * s, top + 26 * s), (cx + 6 * s, top + 30 * s), (cx - 6 * s, top + 30 * s), (cx - 8 * s, top + 26 * s), (cx - 12 * s, top + 17 * s), (cx - 12 * s, top + 9 * s), (cx - 5 * s, top + 3 * s)]
    d.polygon(pts, fill=col)
    d.polygon([(cx - 10 * s, top + 10 * s), (cx - 6 * s, top + 8 * s), (cx - 7 * s, top + 22 * s), (cx - 9 * s, top + 20 * s)], fill=sh(col, 1.2))
    for (ox, oy) in [(-4, 12), (5, 18)]:
        d.ellipse([cx + (ox - 3) * s, top + (oy - 3) * s, cx + (ox + 3) * s, top + (oy + 3) * s], outline=(250, 250, 246))
        d.point((cx + ox * s, top + oy * s), fill=(250, 250, 246))
    for (ox, oy) in [(3, 11), (-5, 21)]:
        d.arc([cx + (ox - 2) * s, top + (oy - 1) * s, cx + (ox + 2) * s, top + (oy + 1) * s], 180, 360, fill=(40, 40, 40))

def o_display(img, x, y, w, h, **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS, y * TS; ww = w * TS
    soft_shadow(img, (X + 8, Y + 36, X + ww - 2, Y + 48), 80, 4)
    wood_top(d, (X + 6, Y + 26, X + ww - 6, Y + 36), (140, 86, 52), seed=11)
    d.rectangle([X + 6, Y + 36, X + ww - 6, Y + 44], fill=(96, 56, 32))
    vase_shape(d, X + ww // 2, Y - 8, 1.1)
    put(img, lay)

def o_vase(img, x, y, w, h, **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS, y * TS
    soft_shadow(img, (X + 10, Y + 36, X + 40, Y + 48), 80, 4)
    vase_shape(d, X + 24, Y + 4, 1.25)
    put(img, lay)

def o_kiln(img, x, y, w, h, **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS, y * TS; ww, hh = w * TS, h * TS
    soft_shadow(img, (X + 6, Y + hh - 20, X + ww + 8, Y + hh + 6), 100, 6)
    d.ellipse([X + 2, Y - 10, X + ww - 2, Y + hh], fill=(156, 86, 58))
    rnd = random.Random(12)
    for j, yy in enumerate(range(Y - 4, Y + hh - 8, 9)):
        off = 0 if j % 2 else 8
        for xx in range(X + off, X + ww, 16):
            d.rectangle([xx + 1, yy + 1, xx + 14, yy + 7], fill=sh((156, 86, 58), 0.9 + rnd.random() * 0.2))
    mask = Image.new('L', lay.size, 0); ImageDraw.Draw(mask).ellipse([X + 2, Y - 10, X + ww - 2, Y + hh], fill=255)
    lay.putalpha(Image.fromarray(np.minimum(np.array(lay.split()[3]), np.array(mask))))
    d = ImageDraw.Draw(lay)
    d.arc([X + 2, Y - 10, X + ww - 2, Y + hh], 200, 320, fill=(196, 124, 90), width=3)
    cx = X + ww // 2
    d.chord([cx - 22, Y + hh - 46, cx + 22, Y + hh + 2], 180, 360, fill=(36, 18, 12))
    d.rectangle([cx - 22, Y + hh - 22, cx + 22, Y + hh - 6], fill=(36, 18, 12))
    put(img, lay)
    img.alpha_composite(MW_glow((cx, Y + hh - 16), 30, (255, 150, 50)))
    d2 = ImageDraw.Draw(img)
    for i, c in enumerate([(255, 120, 40), (255, 180, 60), (255, 236, 150)]):
        d2.ellipse([cx - 14 + i * 4, Y + hh - 24 + i * 3, cx + 14 - i * 4, Y + hh - 8], fill=c)

def MW_glow(center, r, col):
    g = layer(); gd = ImageDraw.Draw(g)
    cx, cy = center
    for i in range(10, 0, -1):
        rr = r * i / 10
        gd.ellipse([cx - rr, cy - rr, cx + rr, cy + rr], fill=col + (int(14 * (11 - i)),))
    return g.filter(ImageFilter.GaussianBlur(r / 4))

def o_shelf(img, x, y, w, h, stuff='pots', **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS + 2, y * TS - 34; ww = w * TS - 4
    soft_shadow(img, (X + 4, Y + 72, X + ww + 8, Y + 84), 90, 4)
    d.rectangle([X, Y, X + ww, Y + 80], fill=(112, 70, 42))
    d.rectangle([X, Y, X + ww, Y + 4], fill=(150, 98, 60)); d.line([(X, Y), (X + ww, Y)], fill=(190, 134, 90))
    d.rectangle([X + 4, Y + 6, X + ww - 4, Y + 74], fill=(70, 42, 26))
    for sy in (Y + 28, Y + 52):
        d.rectangle([X + 2, sy, X + ww - 2, sy + 4], fill=(150, 98, 60)); d.line([(X + 2, sy), (X + ww - 2, sy)], fill=(190, 134, 90))
    rnd = random.Random(x * 3 + y)
    for row, by in enumerate((Y + 27, Y + 51, Y + 73)):
        ix = X + 7
        while ix < X + ww - 12:
            if stuff == 'pots':
                c = rnd.choice([(124, 172, 152), (190, 160, 120), (150, 110, 80), (230, 226, 214)])
                hgt = rnd.randint(12, 18)
                d.ellipse([ix, by - hgt, ix + 11, by], fill=c); d.rectangle([ix + 3, by - hgt - 3, ix + 8, by - hgt + 2], fill=c)
                d.line([(ix + 2, by - hgt + 4), (ix + 2, by - 4)], fill=sh(c, 1.25))
                ix += 15
            elif stuff == 'tools':
                c = rnd.choice([(180, 184, 196), (120, 80, 50)])
                d.rectangle([ix + 3, by - 18, ix + 5, by], fill=c); d.rectangle([ix + 1, by - 6, ix + 7, by], fill=(120, 80, 50))
                ix += 11
            elif stuff == 'books':
                for b in range(rnd.randint(3, 5)):
                    c = rnd.choice([(196, 176, 136), (170, 60, 50), (70, 80, 130), (110, 130, 80)])
                    hh = rnd.randint(14, 19)
                    d.rectangle([ix, by - hh, ix + 4, by], fill=c); d.line([(ix, by - hh), (ix, by)], fill=sh(c, 1.3))
                    ix += 5
                ix += 4
            elif stuff == 'ink':
                d.rectangle([ix, by - 14, ix + 6, by], fill=(40, 40, 46)); d.rectangle([ix + 1, by - 10, ix + 5, by - 6], fill=(200, 170, 80))
                d.rectangle([ix + 10, by - 6, ix + 22, by], fill=(70, 70, 76))
                ix += 26
    put(img, lay)

def o_rack(img, x, y, w, h, gap=False, **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS + 2, y * TS - 36; ww = w * TS - 4
    soft_shadow(img, (X + 4, Y + 74, X + ww + 8, Y + 86), 90, 4)
    d.rectangle([X, Y, X + ww, Y + 82], fill=(100, 66, 40)); d.line([(X, Y), (X + ww, Y)], fill=(160, 112, 72))
    for sy in (Y + 4, Y + 30, Y + 56):
        d.rectangle([X + 4, sy, X + ww - 4, sy + 22], fill=(56, 36, 22))
        for i, bx in enumerate(range(X + 6, X + ww - 6, 5)):
            if gap and sy == Y + 30 and 6 <= i <= 7: continue
            c = (196, 156, 100) if i % 3 else (180, 140, 90)
            d.rectangle([bx, sy + 2, bx + 3, sy + 21], fill=c); d.line([(bx, sy + 2), (bx, sy + 21)], fill=sh(c, 1.2))
            d.rectangle([bx, sy + 2, bx + 3, sy + 4], fill=(120, 84, 50))
        d.rectangle([X + 2, sy + 22, X + ww - 2, sy + 25], fill=(150, 104, 66))
    put(img, lay)

def o_wood(img, x, y, w, h, **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS, y * TS
    soft_shadow(img, (X + 4, Y + h * TS - 14, X + w * TS + 8, Y + h * TS + 4), 90, 5)
    rnd = random.Random(x + y)
    for row in range(5):
        for i in range(int(w * TS / 15)):
            cx = X + 8 + i * 15 + (row % 2) * 7
            cy = Y + 4 + row * 16
            if cx + 8 > X + w * TS or cy + 16 > Y + h * TS + 4: continue
            r = 8
            c = sh((170, 120, 74), 0.9 + rnd.random() * 0.2)
            d.ellipse([cx - r, cy, cx + r, cy + 2 * r], fill=c)
            for rr, cc in [(5, sh(c, 1.15)), (3, sh(c, 0.9)), (1, sh(c, 0.75))]:
                d.ellipse([cx - rr, cy + r - rr, cx + rr, cy + r + rr], outline=cc)
    put(img, lay)

def o_wheel(img, x, y, w, h, **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS, y * TS; cx = X + 24
    soft_shadow(img, (cx - 18, Y + 32, cx + 22, Y + 46), 80, 4)
    d.ellipse([cx - 20, Y + 16, cx + 20, Y + 40], fill=(110, 78, 48)); d.ellipse([cx - 18, Y + 14, cx + 18, Y + 34], fill=(140, 100, 62))
    d.ellipse([cx - 9, Y + 6, cx + 9, Y + 26], fill=(124, 172, 152)); d.ellipse([cx - 5, Y + 6, cx + 5, Y + 11], fill=(90, 130, 116))
    d.line([(cx - 6, Y + 12), (cx - 7, Y + 22)], fill=(170, 210, 196))
    put(img, lay)

def o_basket(img, x, y, w, h, **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS, y * TS; cx = X + 24
    soft_shadow(img, (cx - 18, Y + 34, cx + 22, Y + 46), 80, 4)
    d.ellipse([cx - 19, Y + 14, cx + 19, Y + 42], fill=(186, 150, 96))
    for j in range(Y + 20, Y + 40, 4): d.arc([cx - 18, j - 6, cx + 18, j + 6], 10, 170, fill=(150, 116, 70))
    d.ellipse([cx - 16, Y + 10, cx + 16, Y + 22], fill=(150, 116, 70))
    for i in range(3):
        d.rectangle([cx - 12 + i * 3, Y + 6 - i * 2, cx + 10 + i * 2, Y + 16 - i * 2], fill=(248, 244, 232))
    put(img, lay)

def o_tent(img, x, y, w, h, **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS, y * TS; ww, hh = w * TS, h * TS
    soft_shadow(img, (X - 4, Y + hh - 16, X + ww + 10, Y + hh + 6), 100, 6)
    apex = (X + ww // 2, Y - 34)
    d.polygon([(X - 4, Y + hh - 2), apex, (X + ww + 4, Y + hh - 2)], fill=(220, 206, 170))
    d.polygon([apex, (X + ww + 4, Y + hh - 2), (X + ww // 2 + 18, Y + hh - 2)], fill=(196, 180, 144))
    for i in range(1, 6):
        xx = X - 4 + (ww + 8) * i / 6
        d.line([apex, (xx, Y + hh - 2)], fill=(180, 164, 128))
    d.polygon([(X + ww // 2 - 16, Y + hh - 2), (X + ww // 2, Y + hh - 40), (X + ww // 2 + 16, Y + hh - 2)], fill=(70, 50, 40))
    d.line([apex, (apex[0], apex[1] - 10)], fill=(110, 80, 50), width=2)
    d.polygon([(apex[0], apex[1] - 10), (apex[0] + 12, apex[1] - 6), (apex[0], apex[1] - 2)], fill=(190, 40, 40))
    put(img, lay)

def o_armory(img, x, y, w, h, **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS, y * TS; ww, hh = w * TS, h * TS
    soft_shadow(img, (X, Y + hh - 14, X + ww + 10, Y + hh + 6), 100, 6)
    # 벽
    for i, xx in enumerate(range(X + 2, X + ww - 2, 8)):
        c = sh((150, 106, 66), 0.92 + (i % 2) * 0.1)
        vgrad(d, (xx, Y - 6, xx + 8, Y + hh), sh(c, 1.08), sh(c, 0.88)); d.line([(xx, Y - 6), (xx, Y + hh)], fill=sh(c, 0.7))
    # 지붕
    d.polygon([(X - 8, Y), (X + ww // 2, Y - 34), (X + ww + 8, Y)], fill=(70, 66, 76))
    for j in range(5):
        yy = Y - 30 + j * 7
        span = (j + 1) * (ww + 16) / 6
        for xx in range(int(X + ww // 2 - span / 2), int(X + ww // 2 + span / 2), 10):
            d.chord([xx, yy, xx + 10, yy + 8], 180, 360, fill=(96, 92, 104), outline=(52, 48, 58))
    d.line([(X - 8, Y), (X + ww + 8, Y)], fill=(40, 36, 44), width=2)
    cx = X + ww // 2
    d.rectangle([cx - 18, Y + hh - 44, cx + 18, Y + hh], fill=(84, 52, 30)); d.line([(cx, Y + hh - 44), (cx, Y + hh)], fill=(60, 36, 20))
    d.rectangle([cx - 20, Y + hh - 46, cx + 20, Y + hh - 44], fill=(60, 36, 20))
    for yy in (Y + hh - 36, Y + hh - 14):
        d.rectangle([cx - 16, yy, cx + 16, yy + 3], fill=(170, 170, 176))
    d.rectangle([cx - 4, Y + hh - 26, cx + 4, Y + hh - 20], fill=(214, 176, 90))
    put(img, lay)

def o_banner(img, x, y, w, h, color=(180, 40, 40), **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS, y * TS
    soft_shadow(img, (X + 12, Y + 38, X + 36, Y + 48), 70, 3)
    d.rectangle([X + 22, Y - 40, X + 25, Y + 44], fill=(100, 70, 44)); d.line([(X + 22, Y - 40), (X + 22, Y + 44)], fill=(150, 110, 70))
    d.polygon([(X + 23, Y - 46), (X + 26, Y - 40), (X + 20, Y - 40)], fill=(200, 200, 210))
    d.polygon([(X + 26, Y - 38), (X + 46, Y - 34), (X + 42, Y - 24), (X + 46, Y - 14), (X + 26, Y - 18)], fill=color)
    d.line([(X + 26, Y - 36), (X + 44, Y - 32)], fill=sh(color, 1.3))
    d.ellipse([X + 31, Y - 32, X + 39, Y - 24], fill=sh(color, 1.4))
    d.rectangle([X + 16, Y + 40, X + 31, Y + 46], fill=(120, 116, 110))
    put(img, lay)

def o_weapons(img, x, y, w, h, **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS, y * TS; ww = w * TS
    soft_shadow(img, (X + 4, Y + 34, X + ww + 6, Y + 46), 80, 4)
    d.rectangle([X + 4, Y + 28, X + ww - 4, Y + 34], fill=(120, 80, 48)); d.line([(X + 4, Y + 28), (X + ww - 4, Y + 28)], fill=(170, 120, 78))
    d.rectangle([X + 4, Y + 6, X + ww - 4, Y + 10], fill=(120, 80, 48))
    for lx in (X + 6, X + ww - 10): d.rectangle([lx, Y + 6, lx + 4, Y + 42], fill=(96, 62, 36))
    for i, sx in enumerate(range(X + 14, X + ww - 10, 10)):
        d.rectangle([sx, Y - 30, sx + 2, Y + 30], fill=(130, 96, 60))
        if i % 2:
            d.polygon([(sx - 2, Y - 30), (sx + 4, Y - 30), (sx + 1, Y - 44)], fill=(200, 204, 214)); d.line([(sx + 1, Y - 43), (sx + 1, Y - 31)], fill=(240, 240, 250))
        else:
            d.arc([sx - 8, Y - 34, sx + 6, Y + 10], 270, 90, fill=(140, 90, 50), width=2)
    put(img, lay)

def o_lantern(img, x, y, w, h, **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS, y * TS; cx = X + 24
    soft_shadow(img, (cx - 12, Y + 38, cx + 16, Y + 48), 70, 3)
    d.rectangle([cx - 1, Y - 6, cx + 2, Y + 42], fill=(96, 62, 36)); d.rectangle([cx - 8, Y + 40, cx + 9, Y + 45], fill=(110, 74, 44))
    for i, (r, c) in enumerate([(16, (226, 96, 120)), (12, (240, 140, 160)), (8, (250, 190, 200))]):
        for k2 in range(7):
            a = math.pi + k2 * math.pi / 6
            px, py = cx + math.cos(a) * r, Y - 6 + math.sin(a) * r * 0.6
            d.ellipse([px - 5, py - 7, px + 5, py + 3], fill=c)
    d.ellipse([cx - 9, Y - 14, cx + 9, Y + 2], fill=(255, 236, 170))
    put(img, lay, 0.55)
    img.alpha_composite(MW_glow((cx, Y - 8), 26, (255, 210, 160)))

def o_stand(img, x, y, w, h, **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS, y * TS; cx = X + 24
    soft_shadow(img, (cx - 14, Y + 36, cx + 18, Y + 46), 70, 3)
    wood_top(d, (cx - 14, Y + 26, cx + 14, Y + 34), (150, 98, 58))
    d.rectangle([cx - 14, Y + 34, cx + 14, Y + 40], fill=WOOD_D)
    d.ellipse([cx - 11, Y + 10, cx + 11, Y + 28], fill=(34, 30, 46))
    d.polygon([(cx - 8, Y + 12), (cx, Y + 2), (cx + 8, Y + 12)], fill=(34, 30, 46))
    for (px, py, c) in [(cx, Y + 3, (230, 196, 80)), (cx - 5, Y + 16, (210, 60, 70)), (cx + 5, Y + 16, (90, 160, 210)), (cx, Y + 21, (230, 196, 80))]:
        d.ellipse([px - 2, py - 2, px + 2, py + 2], fill=c)
    put(img, lay)

def o_typecase(img, x, y, w, h, **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS + 4, y * TS + 6; ww = w * TS - 8
    soft_shadow(img, (X + 4, Y + 28, X + ww + 6, Y + 40), 80, 4)
    d.rectangle([X, Y, X + ww, Y + 22], fill=(120, 84, 54)); d.line([(X, Y), (X + ww, Y)], fill=(170, 124, 84))
    d.rectangle([X + 3, Y + 3, X + ww - 3, Y + 19], fill=(70, 50, 34))
    for i in range(X + 5, X + ww - 5, 5):
        for j in range(Y + 5, Y + 18, 4):
            d.rectangle([i, j, i + 3, j + 2], fill=(172, 168, 150)); d.point((i + 1, j + 1), fill=(90, 86, 76))
    d.rectangle([X, Y + 22, X + ww, Y + 30], fill=(96, 66, 42))
    put(img, lay)

def o_boxs(img, x, y, w, h, color=(120, 90, 60), **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS, y * TS
    soft_shadow(img, (X + 6, Y + 34, X + w * TS + 4, Y + 46), 80, 4)
    for i in range(w):
        bx = X + i * TS + 6; by = Y + 10 - (i % 2) * 6
        d.rectangle([bx, by, bx + 36, by + 12], fill=sh(color, 1.12)); d.line([(bx, by), (bx + 36, by)], fill=sh(color, 1.35))
        d.rectangle([bx, by + 12, bx + 36, by + 30], fill=sh(color, 0.85))
        if color[0] > 200:   # 노란 종이 더미
            for j in range(by + 2, by + 12, 2): d.line([(bx + 2, j), (bx + 34, j)], fill=sh(color, 0.92))
        else:
            d.rectangle([bx + 10, by + 16, bx + 26, by + 24], fill=(230, 214, 170)); d.line([(bx + 13, by + 20), (bx + 23, by + 20)], fill=(140, 40, 40))
    put(img, lay)

def o_stable(img, x, y, w, h, **k):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = x * TS + 6, y * TS + 14
    soft_shadow(img, (X + 2, Y + 18, X + 40, Y + 32), 70, 3)
    wood_top(d, (X, Y, X + 36, Y + 12), WOOD)
    d.rectangle([X, Y + 12, X + 36, Y + 17], fill=WOOD_D)
    for lx in (X + 2, X + 30): d.rectangle([lx, Y + 17, lx + 4, Y + 24], fill=sh(WOOD_D, 0.9))
    d.rectangle([X + 6, Y + 2, X + 28, Y + 10], fill=PAPER); d.line([(X + 9, Y + 5), (X + 22, Y + 5)], fill=(100, 90, 86))
    d.ellipse([X + 22, Y + 5, X + 27, Y + 10], fill=(190, 40, 40))
    put(img, lay)

def o_soju(img, x, y, w, h, **k):
    o_jar(img, x, y, w, h, content=(226, 234, 240), color=(78, 64, 58))
    d = ImageDraw.Draw(img)
    X, Y = x * TS, y * TS
    d.rectangle([X + 17, Y + 22, X + 31, Y + 32], fill=(236, 226, 190)); d.rectangle([X + 17, Y + 22, X + 31, Y + 32], outline=(150, 120, 80))
    d.line([(X + 24, Y + 24), (X + 24, Y + 30)], fill=(60, 40, 40)); d.line([(X + 21, Y + 27), (X + 27, Y + 27)], fill=(60, 40, 40))

def o_gate(img, x, y, w, h, **k):
    X, Y = x * TS, y * TS; ww, hh = w * TS, h * TS
    cx, cy = X + ww // 2, Y + hh // 2 - 4
    img.alpha_composite(MW_glow((cx, cy), 90, (255, 230, 160)))
    lay = layer(); d = ImageDraw.Draw(lay)
    d.ellipse([cx - 52, cy - 66, cx + 52, cy + 66], fill=(96, 72, 40))
    d.ellipse([cx - 48, cy - 62, cx + 48, cy + 62], fill=(214, 176, 90))
    d.ellipse([cx - 42, cy - 56, cx + 42, cy + 56], fill=(110, 84, 50))
    for i in range(16):
        a = i * math.pi / 8
        px, py = cx + math.cos(a) * 45, cy + math.sin(a) * 59
        d.ellipse([px - 3, py - 3, px + 3, py + 3], fill=(255, 236, 160))
    d.ellipse([cx - 38, cy - 52, cx + 38, cy + 52], fill=(255, 246, 214))
    d.ellipse([cx - 26, cy - 38, cx + 26, cy + 38], fill=(255, 252, 240))
    # 받침대와 세 홈
    d.rectangle([cx - 46, cy + 56, cx + 46, cy + 70], fill=(150, 144, 132)); d.line([(cx - 46, cy + 56), (cx + 46, cy + 56)], fill=(196, 190, 178))
    for i, c in enumerate([(124, 172, 152), (240, 234, 214), (150, 146, 130)]):
        hx = cx - 30 + i * 30
        d.ellipse([hx - 7, cy + 58, hx + 7, cy + 68], fill=sh(c, 0.55)); d.ellipse([hx - 5, cy + 59, hx + 5, cy + 66], fill=c)
    put(img, lay, 0.5)

DRAW = {
    'desk': o_desk, 'chest': o_chest, 'screen': o_screen, 'wall': o_wall, 'throne': o_throne, 'pillar': o_pillar, 'jar': o_jar,
    'display': o_display, 'kiln': o_kiln, 'shelf': o_shelf, 'rack': o_rack, 'wood': o_wood, 'wheel': o_wheel, 'basket': o_basket,
    'tent': o_tent, 'armory': o_armory, 'banner': o_banner, 'weapons': o_weapons, 'lantern': o_lantern, 'stand': o_stand,
    'typecase': o_typecase, 'boxs': o_boxs, 'gate': o_gate, 'stable': o_stable, 'plant': o_plant, 'cabinet': o_cabinet,
    'soju': o_soju, 'vase': o_vase,
}

def render_room(room):
    th = MW.THEMES[room['key']]
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    floor(img, th['floor'][0], th['floor'][1], room['map'])
    if room.get('rug'):
        x, y, w, h, c, t = room['rug']
        rug_hd(img, (x * TS, y * TS, (x + w) * TS, (y + h) * TS), c, t)
    walls(img, th)
    if 'left' in room['doors']: side_door(img, 'left', th)
    if 'right' in room['doors']: side_door(img, 'right', th)
    if 'right_gate' in room['doors']: obj_gate_door_right(img)
    walls_first = [o for o in room['objs'] if o['style'] == 'wall']
    rest = sorted([o for o in room['objs'] if o['style'] != 'wall'], key=lambda o: (o['y'] + o['h']))
    for o in walls_first + rest:
        DRAW[o['style']](img, o['x'], o['y'], o['w'], o['h'], **o['kw'])
    return img.convert('RGB')

if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for room in MW.ROOMS:
        render_room(room).save(os.path.join(out, room['parallax'] + '.png'))
    print('rooms', len(MW.ROOMS))
