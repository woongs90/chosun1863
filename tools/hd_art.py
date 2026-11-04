"""고해상도(48px 원본) 도트 그림 도구 + 1번 방(왕궁)·여학생 시안"""
import os, sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

TS = 48
W, H = 17 * TS, 13 * TS

def sh(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3])

def mix(a, b, t):
    return tuple(int(a[i] * (1 - t) + b[i] * t) for i in range(3))

def layer():
    return Image.new('RGBA', (W, H), (0, 0, 0, 0))

def outline(lay, strength=0.45, thick=1):
    """RTP 방식 윤곽선: 검정이 아니라 바로 옆 색을 어둡게 한 색으로 테두리"""
    a = np.pad(np.array(lay), ((thick, thick), (thick, thick), (0, 0)))   # 가장자리에서 반대편으로 넘어가지 않게 여백을 두고 계산
    alpha = a[:, :, 3] > 0
    out = a.copy()
    for _ in range(thick):
        filled = alpha.copy()
        rgb = a[:, :, :3].astype(int)
        acc = np.zeros(a.shape[:2] + (3,), int); cnt = np.zeros(a.shape[:2], int)
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            sa = np.roll(alpha, (dy, dx), (0, 1)); sr = np.roll(rgb, (dy, dx), (0, 1))
            m = sa & ~alpha
            acc[m] += sr[m]; cnt[m] += 1
            filled |= sa
        edge = cnt > 0
        col = (acc[edge] / cnt[edge][:, None] * strength).astype(np.uint8)
        out[edge, :3] = col
        out[edge, 3] = 255
        a = out.copy(); alpha = a[:, :, 3] > 0
    return Image.fromarray(out[thick:-thick, thick:-thick])

def soft_shadow(base, box, alpha=90, blur=6):
    s = layer(); ImageDraw.Draw(s).ellipse(box, fill=(10, 6, 4, alpha))
    base.alpha_composite(s.filter(ImageFilter.GaussianBlur(blur)))

def noise_fill(img, box, base, amount=8, seed=0):
    x0, y0, x1, y1 = box
    rng = np.random.default_rng(seed)
    h, w = y1 - y0, x1 - x0
    n = rng.integers(-amount, amount + 1, (h, w, 1))
    arr = np.clip(np.array(base[:3])[None, None, :] + n, 0, 255).astype(np.uint8)
    img.paste(Image.fromarray(arr, 'RGB'), (x0, y0))

def vgrad(d, box, top, bottom):
    x0, y0, x1, y1 = box
    for y in range(y0, y1):
        t = (y - y0) / max(1, y1 - y0 - 1)
        d.line([(x0, y), (x1 - 1, y)], fill=mix(top, bottom, t))

def hgrad(d, box, left, right, mid=None):
    x0, y0, x1, y1 = box
    for x in range(x0, x1):
        t = (x - x0) / max(1, x1 - x0 - 1)
        c = mix(left, right, t) if mid is None else (mix(left, mid, t * 2) if t < 0.5 else mix(mid, right, (t - 0.5) * 2))
        d.line([(x, y0), (x, y1 - 1)], fill=c)

# ======================================================================== 바닥: 마루
def floor_maru(img, box, base=(178, 124, 76), seed=1):
    rnd = random.Random(seed)
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    ph = 12
    for y in range(y0, y1, ph):
        x = x0 - rnd.randint(0, 120)
        while x < x1:
            L = rnd.randint(110, 220)
            c = sh(base, 0.95 + rnd.random() * 0.08)
            c = mix(c, (190, 130, 70), rnd.random() * 0.08)
            xa, xb = max(x, x0), min(x + L, x1)
            if xb > xa:
                vgrad(d, (xa, y, xb, min(y + ph, y1)), sh(c, 1.04), sh(c, 0.95))
                # 나뭇결
                for g in range(rnd.randint(1, 3)):
                    gy = y + rnd.randint(2, ph - 3); amp = rnd.uniform(0.4, 1.4); fr = rnd.uniform(0.02, 0.06); ph0 = rnd.random() * 6
                    pts = [(gx, gy + amp * math.sin(gx * fr + ph0)) for gx in range(xa, xb, 3)]
                    if len(pts) > 1: d.line(pts, fill=sh(c, 0.92))
                if rnd.random() < 0.08:
                    kx = rnd.randint(xa, max(xa, xb - 8)); ky = y + rnd.randint(3, ph - 5)
                    d.ellipse([kx, ky, kx + 6, ky + 3], outline=sh(c, 0.75))
                d.line([(xa, y), (xb - 1, y)], fill=sh(c, 1.08))                  # 윗면 빛
                d.line([(xa, min(y + ph, y1) - 1), (xb - 1, min(y + ph, y1) - 1)], fill=sh(c, 0.78))  # 틈
                if x + L < x1:
                    d.line([(x + L - 1, y), (x + L - 1, y + ph - 1)], fill=sh(c, 0.74))
                    d.line([(x + L, y), (x + L, y + ph - 1)], fill=sh(c, 1.15))
            x += L

def rug(img, box, field=(150, 34, 40), trim=(216, 172, 80)):
    d = ImageDraw.Draw(img)
    x0, y0, x1, y1 = box
    soft_shadow(img, (x0 + 4, y0 + 6, x1 + 6, y1 + 8), 60, 4)
    d.rectangle([x0, y0, x1 - 1, y1 - 1], fill=field)
    noise_fill(img, (x0 + 14, y0 + 14, x1 - 14, y1 - 14), field, 6, seed=9)
    d = ImageDraw.Draw(img)
    for i, c in enumerate([sh(trim, 0.7), trim, sh(trim, 1.15)]):
        d.rectangle([x0 + 3 + i, y0 + 3 + i, x1 - 4 - i, y1 - 4 - i], outline=c)
    d.rectangle([x0 + 10, y0 + 10, x1 - 11, y1 - 11], outline=sh(trim, 0.85), width=2)
    # 회(回) 무늬 띠
    for x in range(x0 + 16, x1 - 16, 12):
        for y in (y0 + 5, y1 - 10):
            d.rectangle([x, y, x + 6, y + 4], outline=sh(trim, 0.9))
    for y in range(y0 + 16, y1 - 16, 12):
        for x in (x0 + 5, x1 - 10):
            d.rectangle([x, y, x + 4, y + 6], outline=sh(trim, 0.9))
    # 가운데 꽃 문양
    cx, cy = (x0 + x1) // 2, (y0 + y1) // 2
    for r, c in [(26, sh(field, 1.18)), (18, trim), (10, sh(field, 0.8)), (4, trim)]:
        d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=c, width=2)
    for k in range(8):
        a = k * math.pi / 4
        d.ellipse([cx + math.cos(a) * 34 - 5, cy + math.sin(a) * 34 - 5, cx + math.cos(a) * 34 + 5, cy + math.sin(a) * 34 + 5], fill=sh(field, 1.2), outline=trim)

# ======================================================================== 벽: 궁궐
DAN_GREEN = (52, 128, 112); DAN_BLUE = (52, 92, 150); DAN_RED = (196, 62, 52); DAN_WHITE = (240, 236, 220)
PILLAR = (168, 44, 38)

def palace_walls(img):
    d = ImageDraw.Draw(img)
    # 맨 윗줄: 지붕 밑(서까래) + 서까래 끝 단청
    vgrad(d, (0, 0, W, 34), (40, 30, 30), (70, 52, 46))
    for x in range(0, W, 8):
        d.line([(x, 0), (x, 33)], fill=(54, 40, 36))
        d.line([(x + 1, 0), (x + 1, 33)], fill=(84, 62, 54))
    for x in range(4, W, 12):
        cx, cy = x + 2, 40
        d.ellipse([cx - 6, cy - 6, cx + 6, cy + 6], fill=DAN_GREEN, outline=(30, 60, 52))
        d.ellipse([cx - 4, cy - 4, cx + 4, cy + 4], fill=DAN_WHITE)
        d.ellipse([cx - 2, cy - 2, cx + 2, cy + 2], fill=DAN_RED)
    # 벽면: 창방(단청 띠) + 회벽 + 하방
    y = 48
    vgrad(d, (0, y, W, y + 14), sh(DAN_GREEN, 1.15), sh(DAN_GREEN, 0.85))
    for x in range(0, W, 24):
        d.rectangle([x + 2, y + 3, x + 21, y + 10], fill=DAN_BLUE)
        d.rectangle([x + 5, y + 5, x + 18, y + 8], fill=DAN_WHITE)
        d.ellipse([x + 9, y + 4, x + 14, y + 9], fill=DAN_RED)
    d.line([(0, y + 13), (W, y + 13)], fill=(30, 50, 44))
    noise_fill(img, (0, y + 14, W, y + 42), (236, 226, 204), 5, seed=3)
    d = ImageDraw.Draw(img)
    vgrad(d, (0, y + 14, W, y + 20), (200, 190, 168), (236, 226, 204))          # 띠 밑 그림자
    vgrad(d, (0, y + 42, W, y + 48), (120, 70, 44), (84, 48, 30))               # 하방
    d.line([(0, y + 42), (W, y + 42)], fill=(150, 96, 60))
    # 기둥
    for x in range(0, W, 3 * TS):
        px = x + 2
        hgrad(d, (px, 34, px + 12, 96), sh(PILLAR, 0.75), sh(PILLAR, 0.7), mid=sh(PILLAR, 1.35))
        d.rectangle([px - 1, 34, px + 12, 37], fill=DAN_GREEN)
    # 옆벽, 아랫벽 (두께감)
    for (bx, by, bw, bh) in [(0, 96, TS, 12 * TS - 96), (16 * TS, 96, TS, 12 * TS - 96), (0, 12 * TS, W, TS)]:
        vgrad(d, (bx, by, bx + bw, by + bh), (58, 44, 42), (44, 32, 30))
    d.rectangle([TS - 6, 96, TS - 1, 12 * TS - 1], fill=(120, 70, 44)); d.line([(TS - 6, 96), (TS - 6, 12 * TS)], fill=(150, 96, 60))
    d.rectangle([16 * TS, 96, 16 * TS + 5, 12 * TS - 1], fill=(100, 58, 36))
    d.rectangle([TS, 12 * TS, 16 * TS + 5, 12 * TS + 5], fill=(100, 58, 36))

# ======================================================================== 물건들
def obj_screen_hunyo(base, tx, ty, tw):
    """훈요 10조 병풍 (글씨 병풍)"""
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = tx * TS, ty * TS - 34
    n = 8; pw = (tw * TS - 8) // n
    for i in range(n):
        px = X + 4 + i * pw
        top = Y + (2 if i % 2 else 0)
        d.rectangle([px, top, px + pw - 1, top + 76], fill=(96, 50, 34))
        d.rectangle([px + 3, top + 4, px + pw - 4, top + 70], fill=(240, 230, 200) if i != 7 else (214, 204, 176))
        shade_x = px + pw - 4
        d.line([(shade_x, top + 4), (shade_x, top + 70)], fill=(200, 186, 152))
        if i != 7:
            for j in range(5):
                d.line([(px + pw // 2, top + 9 + j * 12), (px + pw // 2, top + 15 + j * 12)], fill=(50, 40, 40), width=2)
                d.point((px + pw // 2 - 3, top + 12 + j * 12), fill=(50, 40, 40))
        d.line([(px, top + 74), (px + pw - 1, top + 74)], fill=(140, 84, 54))
    for fx in (X + 10, X + tw * TS - 16):
        d.rectangle([fx, Y + 76, fx + 6, Y + 82], fill=(70, 40, 26))
    soft_shadow(base, (X + 4, Y + 70, X + tw * TS, Y + 90), 80, 5)
    base.alpha_composite(outline(lay, 0.5))

def obj_hanging_scroll(base, tx, ty):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = tx * TS + 8, ty * TS + 2
    d.rectangle([X - 2, Y, X + 33, Y + 3], fill=(80, 46, 30))
    d.rectangle([X, Y + 3, X + 31, Y + 40], fill=(214, 190, 140))
    d.rectangle([X + 3, Y + 6, X + 28, Y + 36], fill=(244, 236, 212))
    # 임금 그림
    d.ellipse([X + 11, Y + 9, X + 20, Y + 18], fill=(236, 200, 166)); d.rectangle([X + 10, Y + 7, X + 21, Y + 10], fill=(30, 26, 34))
    d.polygon([(X + 8, Y + 34), (X + 10, Y + 19), (X + 21, Y + 19), (X + 23, Y + 34)], fill=(180, 40, 40))
    d.rectangle([X + 14, Y + 22, X + 17, Y + 25], fill=(220, 180, 70))
    d.rectangle([X - 3, Y + 40, X + 34, Y + 44], fill=(80, 46, 30))
    d.rectangle([X - 5, Y + 41, X - 3, Y + 43], fill=(220, 190, 110)); d.rectangle([X + 34, Y + 41, X + 36, Y + 43], fill=(220, 190, 110))
    base.alpha_composite(outline(lay, 0.5))

def obj_wall_map(base, tx, ty, tw):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = tx * TS + 4, ty * TS + 5
    w = tw * TS - 8
    d.rectangle([X, Y, X + w, Y + 34], fill=(96, 56, 34))
    d.rectangle([X + 3, Y + 3, X + w - 3, Y + 31], fill=(230, 214, 172))
    d.polygon([(X + 30, Y + 30), (X + 24, Y + 20), (X + 34, Y + 10), (X + 52, Y + 7), (X + 70, Y + 9), (X + 64, Y + 18), (X + 56, Y + 30)], fill=(150, 180, 120))
    d.line([(X + 34, Y + 10), (X + 52, Y + 6), (X + 72, Y + 8)], fill=(80, 120, 190), width=2)
    d.ellipse([X + 38, Y + 15, X + 42, Y + 19], fill=(190, 40, 40)); d.ellipse([X + 48, Y + 22, X + 51, Y + 25], fill=(40, 60, 120))
    d.line([(X + 49, Y + 22), (X + 41, Y + 18)], fill=(190, 40, 40))
    base.alpha_composite(outline(lay, 0.5))

def obj_throne(base, tx, ty, tw, th):
    X, Y = tx * TS, ty * TS
    # 일월오봉도 병풍
    lay = layer(); d = ImageDraw.Draw(lay)
    sx0, sy0, sx1, sy1 = X + 6, Y - 40, X + tw * TS - 6, Y + 22
    d.rectangle([sx0, sy0, sx1, sy1], fill=(110, 56, 34))
    d.rectangle([sx0 + 4, sy0 + 4, sx1 - 4, sy1 - 4], fill=(40, 70, 110))
    for i, (px, ph) in enumerate([(0.12, 18), (0.3, 28), (0.5, 38), (0.7, 28), (0.88, 18)]):
        cx = sx0 + (sx1 - sx0) * px
        d.polygon([(cx - 18, sy1 - 4), (cx, sy1 - 4 - ph), (cx + 18, sy1 - 4)], fill=(60, 120, 90))
        d.line([(cx, sy1 - 4 - ph), (cx + 9, sy1 - 4 - ph // 2)], fill=(110, 170, 130))
    d.ellipse([sx0 + 16, sy0 + 8, sx0 + 28, sy0 + 20], fill=(230, 70, 50))   # 해
    d.ellipse([sx1 - 28, sy0 + 8, sx1 - 16, sy0 + 20], fill=(240, 240, 230))  # 달
    d.rectangle([sx0 + 4, sy1 - 10, sx1 - 4, sy1 - 4], fill=(70, 130, 170))
    for wx in range(sx0 + 6, sx1 - 6, 8):
        d.arc([wx, sy1 - 12, wx + 8, sy1 - 4], 180, 360, fill=(230, 240, 245))
    for k in range(1, 4):
        xx = sx0 + (sx1 - sx0) * k // 4
        d.line([(xx, sy0 + 4), (xx, sy1 - 4)], fill=(90, 46, 28))
    base.alpha_composite(outline(lay, 0.5))
    # 단(계단 있는 대)
    lay = layer(); d = ImageDraw.Draw(lay)
    dx0, dy0, dx1, dy1 = X + 2, Y + 20, X + tw * TS - 2, Y + th * TS - 4
    d.rectangle([dx0, dy0, dx1, dy1], fill=(150, 36, 36))
    d.rectangle([dx0, dy0, dx1, dy0 + 30], fill=(176, 48, 44))
    d.line([(dx0, dy0), (dx1, dy0)], fill=(214, 90, 80))
    d.rectangle([dx0 + 3, dy0 + 3, dx1 - 3, dy0 + 27], outline=(220, 176, 80))
    for i in range(3):
        sy = dy1 - 18 + i * 6
        d.rectangle([X + tw * TS // 2 - 26 - i * 4, sy, X + tw * TS // 2 + 26 + i * 4, sy + 6], fill=sh((150, 36, 36), 1.15 - i * 0.12))
        d.line([(X + tw * TS // 2 - 26 - i * 4, sy), (X + tw * TS // 2 + 26 + i * 4, sy)], fill=(214, 90, 80))
    # 어좌
    cx = X + tw * TS // 2
    d.rectangle([cx - 24, dy0 - 18, cx + 24, dy0 + 6], fill=(214, 168, 70))
    d.rectangle([cx - 20, dy0 - 14, cx + 20, dy0 + 2], fill=(180, 40, 44))
    for k in range(3):
        d.ellipse([cx - 12 + k * 10, dy0 - 10, cx - 6 + k * 10, dy0 - 4], fill=(230, 196, 90))
    d.rectangle([cx - 20, dy0 + 6, cx + 20, dy0 + 18], fill=(196, 150, 60))
    d.rectangle([cx - 16, dy0 + 6, cx + 16, dy0 + 14], fill=(160, 36, 40))
    d.rectangle([cx - 28, dy0 - 6, cx - 22, dy0 + 18], fill=(196, 150, 60)); d.rectangle([cx + 22, dy0 - 6, cx + 28, dy0 + 18], fill=(196, 150, 60))
    soft_shadow(base, (dx0 + 6, dy1 - 6, dx1 + 8, dy1 + 10), 90, 6)
    base.alpha_composite(outline(lay, 0.45))

def obj_pillar(base, tx, ty):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = tx * TS, ty * TS
    cx = X + 24
    soft_shadow(base, (cx - 14, Y + 34, cx + 22, Y + 50), 90, 4)
    d.polygon([(cx - 18, Y + 44), (cx - 14, Y + 34), (cx + 14, Y + 34), (cx + 18, Y + 44), (cx + 14, Y + 47), (cx - 14, Y + 47)], fill=(150, 144, 132))
    d.line([(cx - 14, Y + 34), (cx + 14, Y + 34)], fill=(186, 180, 168))
    hgrad(d, (cx - 11, Y - 40, cx + 11, Y + 38), sh(PILLAR, 0.7), sh(PILLAR, 0.66), mid=sh(PILLAR, 1.4))
    d.rectangle([cx - 13, Y - 44, cx + 12, Y - 36], fill=DAN_GREEN)
    d.rectangle([cx - 13, Y - 40, cx + 12, Y - 38], fill=DAN_WHITE)
    base.alpha_composite(outline(lay, 0.45))

def obj_desk(base, tx, ty, tw):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = tx * TS + 4, ty * TS + 8
    w = tw * TS - 8
    soft_shadow(base, (X + 4, Y + 26, X + w + 6, Y + 40), 80, 4)
    d.rectangle([X, Y, X + w, Y + 18], fill=(150, 98, 58))
    d.line([(X, Y), (X + w, Y)], fill=(196, 140, 92)); d.line([(X, Y + 1), (X + w, Y + 1)], fill=(176, 120, 76))
    for gx in range(X + 6, X + w - 4, 9):
        d.line([(gx, Y + 4), (gx + 5, Y + 14)], fill=(136, 88, 52))
    d.rectangle([X, Y + 18, X + w, Y + 24], fill=(104, 64, 38))
    d.polygon([(X + 2, Y + 24), (X + 8, Y + 24), (X + 6, Y + 32), (X + 2, Y + 32)], fill=(94, 56, 32))
    d.polygon([(X + w - 8, Y + 24), (X + w - 2, Y + 24), (X + w - 2, Y + 32), (X + w - 6, Y + 32)], fill=(94, 56, 32))
    # 종이 + 벼루 + 붓
    d.rectangle([X + 10, Y + 3, X + 34, Y + 14], fill=(246, 240, 222)); d.line([(X + 13, Y + 6), (X + 30, Y + 6)], fill=(90, 80, 80)); d.line([(X + 13, Y + 9), (X + 26, Y + 9)], fill=(90, 80, 80))
    d.rectangle([X + w - 26, Y + 4, X + w - 12, Y + 13], fill=(46, 46, 54)); d.ellipse([X + w - 23, Y + 6, X + w - 17, Y + 10], fill=(20, 20, 26))
    d.line([(X + 40, Y + 12), (X + 54, Y + 4)], fill=(120, 80, 40), width=2); d.line([(X + 38, Y + 13), (X + 41, Y + 11)], fill=(30, 30, 30), width=2)
    base.alpha_composite(outline(lay, 0.45))

def obj_chest(base, tx, ty, tw):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = tx * TS + 6, ty * TS + 4
    w = tw * TS - 12
    soft_shadow(base, (X + 4, Y + 34, X + w + 6, Y + 46), 90, 4)
    d.rectangle([X, Y, X + w, Y + 14], fill=(156, 70, 40))           # 뚜껑 윗면
    d.line([(X, Y), (X + w, Y)], fill=(204, 120, 80))
    d.rectangle([X, Y + 14, X + w, Y + 38], fill=(120, 50, 30))      # 앞면
    d.line([(X, Y + 14), (X + w, Y + 14)], fill=(80, 32, 20))
    for bx in (X + 10, X + w - 16):
        d.rectangle([bx, Y, bx + 6, Y + 38], fill=(206, 168, 84)); d.line([(bx, Y), (bx, Y + 38)], fill=(240, 210, 130))
        for ry in (Y + 5, Y + 22, Y + 32):
            d.point((bx + 3, ry), fill=(120, 90, 40))
    cx = X + w // 2
    d.rectangle([cx - 8, Y + 16, cx + 8, Y + 30], fill=(214, 176, 90)); d.rectangle([cx - 6, Y + 18, cx + 6, Y + 28], fill=(236, 204, 120))
    d.ellipse([cx - 2, Y + 21, cx + 2, Y + 25], fill=(60, 40, 20))
    base.alpha_composite(outline(lay, 0.45))

def obj_cabinet(base, tx, ty, tw):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = tx * TS + 4, ty * TS - 30
    w = tw * TS - 8
    soft_shadow(base, (X + 4, Y + 66, X + w + 8, Y + 80), 90, 4)
    d.rectangle([X, Y, X + w, Y + 8], fill=(150, 82, 50)); d.line([(X, Y), (X + w, Y)], fill=(196, 120, 80))
    d.rectangle([X, Y + 8, X + w, Y + 74], fill=(122, 62, 36))
    for i, (yy) in enumerate([Y + 12, Y + 42]):
        d.rectangle([X + 5, yy, X + w // 2 - 3, yy + 26], fill=(140, 74, 44), outline=(96, 46, 26))
        d.rectangle([X + w // 2 + 3, yy, X + w - 5, yy + 26], fill=(140, 74, 44), outline=(96, 46, 26))
        for hx in (X + 5, X + w - 9):
            d.rectangle([hx, yy + 4, hx + 4, yy + 8], fill=(214, 176, 90)); d.rectangle([hx, yy + 18, hx + 4, yy + 22], fill=(214, 176, 90))
        d.ellipse([X + w // 2 - 7, yy + 10, X + w // 2 - 1, yy + 16], fill=(230, 196, 110)); d.ellipse([X + w // 2 + 1, yy + 10, X + w // 2 + 7, yy + 16], fill=(230, 196, 110))
    d.rectangle([X + 4, Y + 74, X + 10, Y + 78], fill=(80, 40, 24)); d.rectangle([X + w - 10, Y + 74, X + w - 4, Y + 78], fill=(80, 40, 24))
    base.alpha_composite(outline(lay, 0.45))

def obj_plant(base, tx, ty):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = tx * TS, ty * TS
    cx = X + 24
    soft_shadow(base, (cx - 14, Y + 38, cx + 18, Y + 48), 80, 4)
    d.polygon([(cx - 12, Y + 26), (cx + 12, Y + 26), (cx + 9, Y + 44), (cx - 9, Y + 44)], fill=(120, 168, 150))
    d.rectangle([cx - 13, Y + 24, cx + 13, Y + 27], fill=(150, 196, 178))
    d.line([(cx - 6, Y + 30), (cx - 5, Y + 40)], fill=(200, 230, 220))
    leaf = (70, 140, 70)
    for ang, ln in [(-70, 28), (-100, 32), (-130, 26), (-50, 22), (-150, 20), (-85, 24)]:
        a = math.radians(ang)
        ex, ey = cx + math.cos(a) * ln, Y + 26 + math.sin(a) * ln
        d.line([(cx, Y + 26), ((cx + ex) / 2 + 3, (Y + 26 + ey) / 2), (ex, ey)], fill=leaf, width=3)
        d.line([(cx, Y + 26), ((cx + ex) / 2 + 3, (Y + 26 + ey) / 2)], fill=(110, 180, 100))
    d.ellipse([cx + 4, Y + 2, cx + 10, Y + 8], fill=(240, 236, 250)); d.ellipse([cx - 10, Y + 6, cx - 4, Y + 12], fill=(240, 236, 250))
    base.alpha_composite(outline(lay, 0.5))

def obj_gate_door_right(base):
    lay = layer(); d = ImageDraw.Draw(lay)
    X, Y = 16 * TS, 9 * TS - 10
    d.rectangle([X - 2, Y, X + 30, Y + 66], fill=(90, 44, 28))
    d.rectangle([X + 2, Y + 4, X + 26, Y + 62], fill=(176, 52, 40))
    d.line([(X + 14, Y + 4), (X + 14, Y + 62)], fill=(110, 30, 24))
    for yy in (Y + 12, Y + 30, Y + 48):
        for xx in (X + 6, X + 20):
            d.ellipse([xx - 2, yy - 2, xx + 2, yy + 2], fill=(230, 196, 90))
    d.rectangle([X + 9, Y + 30, X + 19, Y + 38], fill=(214, 176, 90))
    base.alpha_composite(outline(lay, 0.45))

def palace_room_hd():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    floor_maru(img, (TS, 2 * TS, 16 * TS, 12 * TS))
    rug(img, (6 * TS, 5 * TS, 11 * TS, 10 * TS))
    palace_walls(img)
    obj_gate_door_right(base=img)
    objs = [(2, lambda: obj_screen_hunyo(img, 2, 2, 3)), (1, lambda: obj_hanging_scroll(img, 6, 1)), (1, lambda: obj_wall_map(img, 8, 1, 2)),
            (2, lambda: obj_throne(img, 12, 2, 3, 2)), (4, lambda: obj_pillar(img, 5, 4)), (4, lambda: obj_pillar(img, 11, 4)),
            (6, lambda: obj_desk(img, 3, 6, 2)), (6, lambda: obj_cabinet(img, 14, 6, 2)), (7, lambda: obj_chest(img, 12, 7, 2)),
            (2, lambda: obj_plant(img, 1, 2)), (11, lambda: obj_plant(img, 15, 11))]
    for _, fn in sorted(objs, key=lambda o: o[0]):
        fn()
    return img.convert('RGB')

# ======================================================================== 48px 캐릭터 (여학생 시안)
def chara_hd(spec, d_, step):
    """d_: 0 아래 1 왼쪽 2 오른쪽 3 위, step: 0,1,2"""
    S = 48
    lay = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    skin, skin_d = (250, 214, 182), (226, 178, 146)
    hair, hair_l, hair_d = spec['hair'], sh(spec['hair'], 1.9), sh(spec['hair'], 0.7)
    top, top_l, top_d = spec['top'], sh(spec['top'], 1.3), sh(spec['top'], 0.72)
    bob = 1 if step != 1 else 0
    cx = 24
    long_hair = spec.get('hairstyle') == 'long'
    hy = 3 + bob
    if long_hair and d_ != 3:
        hd = sh(spec['hair'], 0.7)
        if d_ == 0: d.rounded_rectangle([cx - 12, hy + 8, cx + 11, hy + 29], 5, fill=hd)
        elif d_ == 1: d.rounded_rectangle([cx - 2, hy + 8, cx + 12, hy + 30], 5, fill=hd)
        else: d.rounded_rectangle([cx - 13, hy + 8, cx + 1, hy + 30], 5, fill=hd)
    # 다리
    lift = {0: (0, 2), 1: (0, 0), 2: (2, 0)}[step]
    leg = skin if spec.get('lower') == 'skirt' else spec['bottom']
    sock = spec.get('socks', (246, 246, 246))
    for i, lx in enumerate((cx - 6, cx + 1)):
        ly = 37 - lift[i]
        d.rectangle([lx, ly, lx + 4, 43 - lift[i]], fill=leg)
        if spec.get('lower') == 'skirt':
            d.rectangle([lx, ly + 3, lx + 4, 43 - lift[i]], fill=sock)
        d.rectangle([lx - 1, 44 - lift[i], lx + 5, 46 - lift[i]], fill=spec.get('shoes', (50, 40, 40)))
    # 몸통
    by = 25 + bob
    d.rounded_rectangle([cx - 9, by, cx + 8, by + 12], 3, fill=top)
    d.line([(cx - 9, by + 1), (cx - 9, by + 11)], fill=top_l)
    if spec.get('lower') == 'skirt':
        d.polygon([(cx - 10, by + 10), (cx + 9, by + 10), (cx + 11, by + 15), (cx - 12, by + 15)], fill=spec['bottom'])
        for px in range(cx - 9, cx + 9, 4):
            d.line([(px, by + 11), (px - 1, by + 15)], fill=sh(spec['bottom'], 0.7))
    else:
        d.rectangle([cx - 8, by + 11, cx + 7, by + 13], fill=sh(spec['bottom'], 0.9))
    if d_ == 0:
        d.polygon([(cx - 3, by), (cx + 2, by), (cx - 1, by + 5)], fill=(248, 248, 248))
        d.line([(cx - 4, by), (cx - 1, by + 6)], fill=top_d); d.line([(cx + 3, by), (cx, by + 6)], fill=top_d)
        acc = spec.get('accent')
        if acc:
            d.polygon([(cx - 4, by + 2), (cx - 1, by + 3), (cx - 4, by + 5)], fill=acc); d.polygon([(cx + 3, by + 2), (cx, by + 3), (cx + 3, by + 5)], fill=acc)
            d.rectangle([cx - 2, by + 2, cx + 1, by + 4], fill=sh(acc, 0.8))
        d.point((cx - 1, by + 8), fill=(220, 200, 120)); d.point((cx - 1, by + 10), fill=(220, 200, 120))
    # 팔
    sw = {0: (2, -2), 1: (0, 0), 2: (-2, 2)}[step]
    if d_ in (0, 3):
        for i, ax in enumerate((cx - 12, cx + 9)):
            ay = by + 1 + (sw[i] if d_ == 0 else -sw[i]) // 2
            d.rounded_rectangle([ax, ay, ax + 3, ay + 10], 1, fill=top_d)
            d.rectangle([ax, ay + 10, ax + 3, ay + 12], fill=skin if d_ == 0 else skin_d)
    else:
        ax = cx - 2 + (sw[0] if d_ == 1 else -sw[0])
        d.rounded_rectangle([ax, by + 1, ax + 4, by + 11], 1, fill=top_d)
        d.rectangle([ax, by + 11, ax + 4, by + 13], fill=skin)
    # 머리
    if d_ == 3:
        d.ellipse([cx - 12, hy, cx + 11, hy + 22], fill=hair)
        if long_hair: d.rounded_rectangle([cx - 12, hy + 10, cx + 11, hy + 30], 5, fill=hair)
        d.arc([cx - 9, hy + 2, cx + 6, hy + 14], 200, 300, fill=hair_l, width=2)
        for k in range(4): d.line([(cx - 6 + k * 4, hy + 12), (cx - 7 + k * 4, hy + (28 if long_hair else 20))], fill=hair_d)
        if spec.get('ribbon'):
            d.polygon([(cx - 5, hy + 15), (cx - 1, hy + 17), (cx - 5, hy + 19)], fill=spec['ribbon']); d.polygon([(cx + 4, hy + 15), (cx, hy + 17), (cx + 4, hy + 19)], fill=spec['ribbon'])
    else:
        d.ellipse([cx - 11, hy + 2, cx + 10, hy + 22], fill=skin)
        d.ellipse([cx - 12, hy, cx + 11, hy + 13], fill=hair)
        if d_ == 0:
            for fx in range(cx - 10, cx + 10, 4):
                d.polygon([(fx, hy + 9), (fx + 4, hy + 9), (fx + 2, hy + 13 + (fx % 3))], fill=hair)
            d.rectangle([cx - 12, hy + 6, cx - 10, hy + 18], fill=hair); d.rectangle([cx + 9, hy + 6, cx + 11, hy + 18], fill=hair)
            for ex in (cx - 6, cx + 3):
                d.rectangle([ex, hy + 13, ex + 2, hy + 17], fill=(40, 30, 40)); d.point((ex, hy + 13), fill=(255, 255, 255)); d.point((ex + 2, hy + 17), fill=(90, 70, 110))
            d.rectangle([cx - 9, hy + 18, cx - 7, hy + 19], fill=(246, 160, 160)); d.rectangle([cx + 6, hy + 18, cx + 8, hy + 19], fill=(246, 160, 160))
            d.line([(cx - 1, hy + 20), (cx, hy + 20)], fill=(200, 110, 100))
        else:
            back = 1 if d_ == 1 else -1
            if d_ == 1:
                d.ellipse([cx - 5, hy, cx + 12, hy + 21], fill=hair)
                d.polygon([(cx - 12, hy + 6), (cx - 2, hy + 4), (cx - 6, hy + 11)], fill=hair)
                d.rectangle([cx - 8, hy + 13, cx - 6, hy + 17], fill=(40, 30, 40)); d.point((cx - 8, hy + 13), fill=(255, 255, 255))
                d.rectangle([cx - 10, hy + 18, cx - 8, hy + 19], fill=(246, 160, 160))
            else:
                d.ellipse([cx - 13, hy, cx + 4, hy + 21], fill=hair)
                d.polygon([(cx + 11, hy + 6), (cx + 1, hy + 4), (cx + 5, hy + 11)], fill=hair)
                d.rectangle([cx + 5, hy + 13, cx + 7, hy + 17], fill=(40, 30, 40)); d.point((cx + 7, hy + 13), fill=(255, 255, 255))
                d.rectangle([cx + 7, hy + 18, cx + 9, hy + 19], fill=(246, 160, 160))
        d.arc([cx - 9, hy + 1, cx + 6, hy + 10], 200, 320, fill=hair_l, width=2)
        if spec.get('ribbon') and d_ != 0:
            rx = cx + 9 if d_ == 1 else cx - 12
            d.polygon([(rx, hy + 4), (rx + 4, hy + 2), (rx + 4, hy + 8)], fill=spec['ribbon'])
    return outline(lay, 0.4)

def chara_sheet(spec, path):
    sheet = Image.new('RGBA', (144, 192), (0, 0, 0, 0))
    for d_ in range(4):
        for st in range(3):
            sheet.alpha_composite(chara_hd(spec, d_, st), (st * 48, d_ * 48))
    sheet.save(path)
    return sheet

if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    room = palace_room_hd()
    room.save(os.path.join(out, 'hd_palace.png'))
    spec_f = dict(hair=(40, 32, 40), hairstyle='long', ribbon=(214, 52, 66), top=(44, 58, 108), accent=(214, 52, 66), lower='skirt', bottom=(54, 62, 110), shoes=(40, 34, 34))
    sheet = chara_sheet(spec_f, os.path.join(out, 'hd_student_f.png'))
    print('ok')
