"""8개 방: 도트(타일셋풍) 원경 그림 + MV 맵 파일 + MapInfos 생성.
16x16 픽셀 격자로 그린 뒤 3배(48px 타일) 확대합니다."""
import json, os, sys, random

from PIL import Image, ImageDraw

OUT = sys.argv[1] if __name__ == '__main__' and len(sys.argv) > 1 else None
W, H = 17, 13
T = 16
OUTL = (40, 28, 26)

def sh(c, f):
    return tuple(max(0, min(255, int(v * f))) for v in c[:3])

class Px:
    def __init__(self):
        self.im = Image.new('RGB', (W * T, H * T), (0, 0, 0))
        self.d = ImageDraw.Draw(self.im)
    def r(self, x, y, w, h, c):
        if w <= 0 or h <= 0: return
        self.d.rectangle([x, y, x + w - 1, y + h - 1], fill=tuple(c[:3]))
    def o(self, x, y, w, h, c=OUTL):
        self.d.rectangle([x, y, x + w - 1, y + h - 1], outline=tuple(c[:3]))
    def p(self, x, y, c):
        if 0 <= x < W * T and 0 <= y < H * T:
            self.im.putpixel((x, y), tuple(c[:3]))
    def e(self, x, y, w, h, c, out=None):
        self.d.ellipse([x, y, x + w - 1, y + h - 1], fill=tuple(c[:3]), outline=tuple(out[:3]) if out else None)
    def line(self, pts, c, w=1):
        self.d.line(pts, fill=tuple(c[:3]), width=w)
    def poly(self, pts, c, out=None):
        self.d.polygon(pts, fill=tuple(c[:3]), outline=tuple(out[:3]) if out else None)

# ======================================================================== 바닥
def floor(P, kind, base, seed=1):
    rnd = random.Random(seed)
    X0, Y0, X1, Y1 = T, 2 * T, 16 * T, 12 * T
    if kind == 'maru':
        for y in range(Y0, Y1, 4):
            c = sh(base, 0.94 + rnd.random() * 0.1)
            P.r(X0, y, X1 - X0, 4, c)
            P.r(X0, y + 3, X1 - X0, 1, sh(base, 0.78))
            x = X0 + rnd.randint(0, 30)
            while x < X1:
                P.r(x, y, 1, 3, sh(base, 0.8))
                x += rnd.randint(28, 52)
    elif kind == 'earth':
        P.r(X0, Y0, X1 - X0, Y1 - Y0, base)
        for _ in range(700):
            x = rnd.randint(X0, X1 - 1); y = rnd.randint(Y0, Y1 - 1)
            P.p(x, y, sh(base, 0.86 if rnd.random() < 0.6 else 1.1))
    elif kind == 'stone':
        for ty in range(Y0, Y1, 8):
            for tx in range(X0, X1, 8):
                c = sh(base, 0.93 + rnd.random() * 0.1)
                P.r(tx, ty, 8, 8, c)
                P.r(tx, ty, 8, 1, sh(c, 1.1)); P.r(tx, ty, 1, 8, sh(c, 1.06))
                P.r(tx, ty + 7, 8, 1, sh(c, 0.78)); P.r(tx + 7, ty, 1, 8, sh(c, 0.82))
    elif kind == 'jeondol':  # 네모 전돌
        for ty in range(Y0, Y1, 16):
            for tx in range(X0, X1, 16):
                c = sh(base, 0.95 + rnd.random() * 0.08)
                P.r(tx, ty, 16, 16, c)
                P.o(tx, ty, 16, 16, sh(base, 0.78))
                P.r(tx + 1, ty + 1, 14, 1, sh(c, 1.08))
    elif kind == 'grass':
        P.r(X0, Y0, X1 - X0, Y1 - Y0, base)
        for _ in range(500):
            x = rnd.randint(X0, X1 - 2); y = rnd.randint(Y0, Y1 - 2)
            P.p(x, y, sh(base, 1.15)); P.p(x, y + 1, sh(base, 0.85))
        # 흙길
        P.r(X0, 9 * T, X1 - X0, T, (156, 128, 92))
        for _ in range(140):
            x = rnd.randint(X0, X1 - 1); y = rnd.randint(9 * T, 10 * T - 1)
            P.p(x, y, (136, 110, 78))

def rug(P, x, y, w, h, c, trim):
    X, Y = x * T, y * T
    P.r(X, Y, w * T, h * T, c)
    P.o(X + 1, Y + 1, w * T - 2, h * T - 2, trim)
    P.o(X + 3, Y + 3, w * T - 6, h * T - 6, sh(trim, 0.85))
    for i in range(X + 6, X + w * T - 6, 6):
        P.p(i, Y + 5, trim); P.p(i, Y + h * T - 6, trim)

# ======================================================================== 벽
def walls(P, th):
    top = th['top']; face = th['face']
    # 천장(맨 윗줄) + 옆벽 + 아랫벽
    P.r(0, 0, W * T, T, top)
    P.r(0, T, T, 11 * T, top); P.r(16 * T, T, T, 11 * T, top)
    P.r(0, 12 * T, W * T, T, top)
    pat = th.get('top_pat', 'beam')
    for x in range(0, W * T, 8):
        if pat == 'giwa':
            for y in range(0, T, 4):
                P.e(x - (2 if (y // 4) % 2 else 0), y, 9, 5, sh(top, 1.12), sh(top, 0.7))
        else:
            P.r(x, 0, 1, T, sh(top, 0.85))
    P.r(0, T - 2, W * T, 2, sh(top, 0.7))
    # 벽면 (둘째 줄)
    kind = th['face_kind']
    Y = T
    if kind == 'palace':
        P.r(0, Y, W * T, T, face)
        P.r(0, Y, W * T, 4, th.get('dan1', (60, 120, 100)))
        for x in range(0, W * T, 6):
            P.r(x, Y + 1, 3, 2, th.get('dan2', (200, 70, 60)))
        for x in range(0, W * T, 3 * T):
            P.r(x, Y, 4, T, th.get('post', (170, 44, 40))); P.r(x + 1, Y, 1, T, sh(th.get('post', (170, 44, 40)), 1.25))
    elif kind == 'earth':
        P.r(0, Y, W * T, T, face)
        rnd = random.Random(3)
        for _ in range(220):
            P.p(rnd.randint(0, W * T - 1), rnd.randint(Y, Y + T - 1), sh(face, 0.85))
        for x in range(0, W * T, 2 * T):
            P.r(x, Y, 3, T, (110, 78, 50))
        P.r(0, Y, W * T, 2, (110, 78, 50))
    elif kind == 'wood':
        for x in range(0, W * T, 4):
            P.r(x, Y, 4, T, sh(face, 0.92 + (x // 4 % 3) * 0.06))
            P.r(x, Y, 1, T, sh(face, 0.72))
        P.r(0, Y, W * T, 2, sh(face, 0.6))
    elif kind == 'palisade':
        for x in range(0, W * T, 5):
            c = sh(face, 0.9 + (x // 5 % 2) * 0.12)
            P.r(x, Y + 2, 4, T - 2, c)
            P.poly([(x, Y + 2), (x + 3, Y + 2), (x + 1, Y - 1)], c)
            P.r(x + 3, Y + 2, 1, T - 2, sh(face, 0.7))
        P.r(0, Y + 7, W * T, 1, sh(face, 0.6))
    elif kind == 'temple':
        P.r(0, Y, W * T, T, face)
        P.r(0, Y, W * T, 5, (52, 110, 96))
        for x in range(0, W * T, 8):
            P.r(x + 1, Y + 1, 5, 3, (214, 88, 66)); P.r(x + 3, Y + 2, 1, 1, (240, 220, 140))
        for x in range(0, W * T, 4 * T):
            P.r(x, Y, 4, T, (120, 70, 46))
    P.r(0, 2 * T - 2, W * T, 2, th.get('base', sh(face, 0.65)))
    # 옆벽 안쪽 테두리
    P.r(T - 2, 2 * T, 2, 10 * T, sh(top, 1.35)); P.r(16 * T, 2 * T, 2, 10 * T, sh(top, 1.35))
    P.r(T, 12 * T, 15 * T, 2, sh(top, 1.35))

def side_door(P, side, th, label_color=(240, 214, 140)):
    x = 0 if side == 'left' else 16 * T
    y = 9 * T
    fl = th['floor_col']
    P.r(x, y, T, T, sh(fl, 0.8))
    P.r(x, y - 2, T, 2, (90, 60, 40)); P.r(x, y + T, T, 2, (90, 60, 40))
    # 화살표
    cx, cy = x + 8, y + 8
    if side == 'left':
        P.poly([(cx + 3, cy - 4), (cx + 3, cy + 4), (cx - 3, cy)], label_color)
    else:
        P.poly([(cx - 3, cy - 4), (cx - 3, cy + 4), (cx + 3, cy)], label_color)

def palace_gate_door(P):
    x, y = 16 * T, 9 * T
    P.r(x, y - 3, T, T + 6, (60, 30, 22))
    P.r(x + 2, y - 1, T - 3, T + 2, (176, 52, 40))
    P.r(x + 8, y - 1, 1, T + 2, (90, 30, 24))
    P.p(x + 6, y + 7, (230, 190, 80)); P.p(x + 10, y + 7, (230, 190, 80))
    P.r(x + 6, y + 9, 5, 3, (210, 170, 70))

# ======================================================================== 물건
def shadow(P, x, y, w):
    P.r(x + 2, y, w - 2, 2, (0, 0, 0)) if False else None

def box3d(P, X, Y, w, h, top, front, depth=5):
    P.r(X, Y, w, h - depth, top)
    P.r(X, Y + h - depth, w, depth, front)
    P.r(X, Y, w, 1, sh(top, 1.15))
    P.o(X, Y, w, h)
    P.r(X + 1, Y + h - depth, w - 2, 1, sh(front, 0.8))

WOOD = (156, 106, 64)
WOOD_D = (112, 74, 44)
PAPER = (236, 224, 192)

def o_desk(P, x, y, w, h, **k):
    X, Y = x * T, y * T
    box3d(P, X + 1, Y + 2, w * T - 2, 12, WOOD, WOOD_D)
    P.r(X + 3, Y + 14, 2, 2, WOOD_D); P.r(X + w * T - 5, Y + 14, 2, 2, WOOD_D)
    for item in k.get('things', ['paper']):
        if item == 'paper':
            P.r(X + 5, Y + 4, 8, 5, PAPER); P.o(X + 5, Y + 4, 8, 5, (150, 130, 100))
            P.r(X + 6, Y + 6, 5, 1, (90, 80, 70))
        if item == 'book':
            P.r(X + 10, Y + 3, 12, 6, (230, 216, 180)); P.r(X + 16, Y + 3, 1, 6, (150, 120, 80)); P.o(X + 10, Y + 3, 12, 6, (120, 90, 60))
        if item == 'scrolls':
            for i in range(3):
                P.r(X + 4 + i * 12, Y + 4, 9, 4, PAPER); P.r(X + 4 + i * 12, Y + 4, 1, 4, (150, 100, 60)); P.r(X + 12 + i * 12, Y + 4, 1, 4, (150, 100, 60))
        if item == 'board':
            P.r(X + 6, Y + 3, w * T - 12, 6, (190, 150, 100)); P.o(X + 6, Y + 3, w * T - 12, 6, (110, 80, 50))
            for i in range(X + 8, X + w * T - 8, 3):
                P.r(i, Y + 5, 2, 2, (120, 86, 54))
        if item == 'map':
            P.r(X + 4, Y + 3, w * T - 8, 7, (220, 206, 168)); P.o(X + 4, Y + 3, w * T - 8, 7, (130, 100, 70))
            P.r(X + 8, Y + 5, 6, 3, (120, 160, 110)); P.p(X + w * T - 10, Y + 5, (200, 40, 40))
        if item == 'ink':
            P.r(X + w * T - 8, Y + 4, 4, 4, (40, 40, 46))

def o_chest(P, x, y, w, h, **k):
    X, Y = x * T, y * T
    box3d(P, X + 2, Y + 2, w * T - 4, 13, (150, 86, 44), (110, 60, 30), depth=6)
    P.r(X + 2, Y + 6, w * T - 4, 1, (90, 50, 26))
    for bx in (X + 7, X + w * T - 9):
        P.r(bx, Y + 2, 2, 13, (214, 176, 80))
    P.r(X + w * T // 2 - 2, Y + 7, 4, 4, (230, 196, 90)); P.p(X + w * T // 2, Y + 9, OUTL)

def o_screen(P, x, y, w, h, **k):  # 병풍 (위로 솟음)
    X, Y = x * T, y * T - 8
    n = w * 4
    pw = (w * T - 2) // n
    for i in range(n):
        px = X + 1 + i * pw
        P.r(px, Y, pw, 22, (110, 60, 40))
        P.r(px + 1, Y + 1, pw - 2, 18, PAPER)
        for j in range(3):
            P.r(px + 2, Y + 4 + j * 5, 1, 3, (60, 50, 50))
        if i == 7 and k.get('erased'):
            P.r(px + 1, Y + 1, pw - 2, 18, (200, 190, 160))
    P.o(X, Y, w * T, 22)
    P.r(X + 2, Y + 22, 2, 2, OUTL); P.r(X + w * T - 4, Y + 22, 2, 2, OUTL)

def o_wall_frame(P, x, y, w, h, kind='scroll', **k):
    X, Y = x * T, y * T
    if kind == 'scroll':
        P.r(X + 3, Y + 1, w * T - 6, 1, (70, 40, 26)); P.r(X + 3, Y + 14, w * T - 6, 1, (70, 40, 26))
        P.r(X + 4, Y + 2, w * T - 8, 12, PAPER)
        if k.get('figure'):
            cx = X + w * T // 2
            P.e(cx - 2, Y + 3, 5, 4, (60, 40, 30)); P.r(cx - 3, Y + 7, 7, 6, (160, 40, 40))
        else:
            for i in range(X + 6, X + w * T - 6, 3):
                P.r(i, Y + 4, 1, 8, (70, 60, 60))
    elif kind == 'map':
        P.r(X + 2, Y + 2, w * T - 4, 12, (226, 212, 172)); P.o(X + 2, Y + 2, w * T - 4, 12, (110, 80, 50))
        P.r(X + 6, Y + 5, w * T - 14, 6, (140, 176, 120)); P.r(X + 4, Y + 4, 4, 3, (110, 150, 190))
        P.p(X + w * T // 2, Y + 8, (200, 40, 40)); P.p(X + w * T // 2 - 4, Y + 6, (200, 40, 40))
    elif kind == 'grid':
        P.r(X + 2, Y + 2, w * T - 4, 12, (226, 212, 172)); P.o(X + 2, Y + 2, w * T - 4, 12, (110, 80, 50))
        for i in range(X + 4, X + w * T - 3, 6): P.r(i, Y + 3, 1, 10, (170, 150, 120))
        for j in range(Y + 4, Y + 14, 3): P.r(X + 3, j, w * T - 6, 1, (170, 150, 120))
        P.p(X + 20, Y + 6, (60, 60, 160)); P.p(X + 12, Y + 10, (200, 40, 40))
    elif kind == 'painting':
        P.r(X + 2, Y + 1, w * T - 4, 14, (100, 66, 40)); P.r(X + 3, Y + 2, w * T - 6, 12, (214, 200, 160))
        P.r(X + 4, Y + 9, w * T - 8, 4, (120, 150, 100))
        P.poly([(X + 8, Y + 9), (X + 13, Y + 4), (X + 18, Y + 9)], (150, 60, 50))
        for i in range(3): P.r(X + 20 + i * 3, Y + 8, 1, 3, (40, 40, 60))
    elif kind == 'portraits':
        for i in range(w):
            P.r(X + i * T + 2, Y + 1, 12, 14, (100, 66, 40)); P.r(X + i * T + 3, Y + 2, 10, 12, (220, 206, 170))
            P.e(X + i * T + 6, Y + 3, 4, 4, (50, 40, 34)); P.r(X + i * T + 5, Y + 7, 6, 6, [(120, 70, 60), (70, 90, 120), (90, 110, 70), (140, 40, 40)][i % 4])
    elif kind == 'paper':
        P.r(X + 3, Y + 2, w * T - 6, 12, PAPER); P.o(X + 3, Y + 2, w * T - 6, 12, (130, 100, 70))
        for j in range(Y + 4, Y + 13, 2):
            P.r(X + 5, j, w * T - 12 - (j % 3) * 3, 1, (80, 70, 64))
    elif kind == 'hanja':
        P.r(X + 3, Y + 2, w * T - 6, 12, PAPER); P.o(X + 3, Y + 2, w * T - 6, 12, (130, 100, 70))
        for i in range(X + 5, X + w * T - 6, 5):
            P.r(i, Y + 4, 3, 3, (60, 50, 50)); P.r(i, Y + 9, 3, 3, (60, 50, 50))
    elif kind == 'hair':
        P.r(X + 2, Y + 1, 12, 14, (100, 66, 40)); P.r(X + 3, Y + 2, 10, 12, (226, 214, 180))
        P.e(X + 5, Y + 3, 6, 5, (230, 196, 160)); P.r(X + 5, Y + 3, 6, 1, (40, 30, 30)); P.r(X + 10, Y + 5, 1, 6, (40, 30, 30))
        P.r(X + 5, Y + 8, 6, 5, (90, 70, 120))

def o_throne(P, x, y, w, h, **k):
    X, Y = x * T, y * T
    box3d(P, X, Y + 4, w * T, h * T - 4, (150, 40, 40), (110, 28, 30), depth=7)
    P.o(X + 2, Y + 6, w * T - 4, h * T - 15, (214, 176, 80))
    cx = X + w * T // 2
    P.r(cx - 10, Y - 6, 20, 14, (214, 176, 80)); P.o(cx - 10, Y - 6, 20, 14)
    P.r(cx - 7, Y - 3, 14, 6, (170, 40, 44))
    P.r(cx - 8, Y + 8, 16, 7, (200, 160, 70)); P.o(cx - 8, Y + 8, 16, 7)
    # 일월오봉 대신 간단한 장식
    P.e(cx - 2, Y - 5, 4, 4, (250, 240, 200))

def o_pillar(P, x, y, w, h, color=(176, 44, 40), **k):
    X, Y = x * T, y * T
    P.e(X + 1, Y + 9, 14, 7, (150, 140, 124), OUTL)
    P.r(X + 4, Y - 12, 8, 23, color); P.o(X + 4, Y - 12, 8, 23)
    P.r(X + 6, Y - 11, 1, 21, sh(color, 1.3))
    P.r(X + 3, Y - 14, 10, 3, (60, 110, 96)); P.o(X + 3, Y - 14, 10, 3)

def o_jar(P, x, y, w, h, content=None, color=(120, 80, 50), **k):
    X, Y = x * T, y * T
    P.e(X + 2, Y + 2, 12, 13, color, OUTL)
    P.e(X + 4, Y + 1, 8, 4, sh(color, 0.7), OUTL)
    if content:
        P.e(X + 5, Y + 2, 6, 2, content)
    P.r(X + 4, Y + 6, 1, 4, sh(color, 1.35))

def o_display(P, x, y, w, h, vase=(120, 170, 150), **k):
    X, Y = x * T, y * T
    box3d(P, X + 2, Y + 8, w * T - 4, 8, WOOD, WOOD_D, depth=3)
    cx = X + w * T // 2
    P.e(cx - 5, Y - 2, 10, 11, vase, OUTL); P.r(cx - 2, Y - 6, 4, 5, vase); P.o(cx - 2, Y - 6, 4, 5)
    P.p(cx - 2, Y + 2, (250, 250, 250)); P.p(cx + 2, Y + 3, (40, 40, 40)); P.p(cx, Y + 5, (250, 250, 250))

def o_kiln(P, x, y, w, h, **k):
    X, Y = x * T, y * T
    P.e(X, Y - 4, w * T, h * T + 2, (150, 82, 56), OUTL)
    for j in range(Y, Y + h * T - 4, 5):
        P.r(X + 6, j, w * T - 12, 1, (118, 62, 44))
    cx = X + w * T // 2
    P.e(cx - 9, Y + h * T - 20, 18, 20, (40, 20, 14), OUTL)
    P.e(cx - 5, Y + h * T - 12, 10, 8, (255, 150, 40)); P.e(cx - 2, Y + h * T - 10, 4, 4, (255, 230, 120))

def o_shelf(P, x, y, w, h, stuff='pots', **k):
    X, Y = x * T, y * T - 10
    P.r(X + 1, Y, w * T - 2, 24, WOOD_D); P.o(X + 1, Y, w * T - 2, 24)
    for j in (Y + 8, Y + 16):
        P.r(X + 2, j, w * T - 4, 2, WOOD)
    for i in range(X + 4, X + w * T - 6, 7):
        if stuff == 'pots':
            P.e(i, Y + 2, 5, 6, (120, 170, 150), OUTL); P.e(i + 1, Y + 10, 5, 6, (180, 150, 110), OUTL)
        elif stuff == 'tools':
            P.r(i + 1, Y + 2, 2, 6, (170, 170, 180)); P.r(i, Y + 11, 4, 5, (90, 60, 40))
        elif stuff == 'books':
            P.r(i, Y + 2, 5, 6, (200, 180, 140)); P.r(i + 1, Y + 10, 4, 6, (170, 60, 50))
        elif stuff == 'ink':
            P.r(i, Y + 3, 4, 5, (40, 40, 44)); P.r(i, Y + 11, 5, 5, (90, 90, 96))

def o_rack(P, x, y, w, h, **k):
    X, Y = x * T, y * T - 12
    P.r(X, Y, w * T, 27, (96, 64, 40)); P.o(X, Y, w * T, 27)
    for j in (Y + 9, Y + 18):
        P.r(X + 1, j, w * T - 2, 2, (130, 90, 56))
    for i in range(X + 2, X + w * T - 3, 3):
        P.r(i, Y + 2, 2, 7, (186, 146, 96)); P.r(i, Y + 11, 2, 7, (176, 136, 90)); P.r(i, Y + 20, 2, 6, (186, 146, 96))
    if k.get('gap'):
        gx = X + 2 + 3 * 3 * 2
        P.r(gx, Y + 11, 5, 7, (60, 40, 26))

def o_wood(P, x, y, w, h, **k):
    X, Y = x * T, y * T
    for row in range(3):
        for i in range(w * 3):
            cx = X + 2 + i * 5 + (row % 2) * 2
            cy = Y + 2 + row * 9
            if cx + 7 > X + w * T: continue
            P.e(cx, cy, 8, 8, (166, 116, 70), OUTL); P.e(cx + 2, cy + 2, 4, 4, (200, 160, 110))

def o_wheel(P, x, y, w, h, **k):
    X, Y = x * T, y * T
    P.e(X + 1, Y + 3, 14, 11, (110, 80, 50), OUTL); P.e(X + 4, Y + 4, 8, 6, (130, 176, 156), OUTL)

def o_basket(P, x, y, w, h, **k):
    X, Y = x * T, y * T
    P.e(X + 1, Y + 3, 14, 12, (186, 150, 96), OUTL)
    for i in range(X + 3, X + 13, 3): P.r(i, Y + 5, 1, 8, (150, 116, 70))
    P.r(X + 4, Y + 4, 8, 3, (246, 242, 230))

def o_tent(P, x, y, w, h, **k):
    X, Y = x * T, y * T
    P.poly([(X, Y + h * T - 1), (X + w * T // 2, Y - 10), (X + w * T - 1, Y + h * T - 1)], (210, 196, 160), OUTL)
    for i in range(1, 4):
        xx = X + w * T // 2 + (i - 2) * 8
        P.line([(X + w * T // 2, Y - 8), (xx, Y + h * T - 2)], (170, 150, 120))
    P.poly([(X + w * T // 2 - 6, Y + h * T - 1), (X + w * T // 2, Y + h * T - 14), (X + w * T // 2 + 6, Y + h * T - 1)], (70, 50, 40))

def o_armory(P, x, y, w, h, **k):
    X, Y = x * T, y * T - 10
    P.poly([(X - 2, Y + 8), (X + w * T // 2, Y - 4), (X + w * T + 1, Y + 8)], (80, 70, 76), OUTL)
    P.r(X, Y + 8, w * T, h * T + 2, (140, 100, 64)); P.o(X, Y + 8, w * T, h * T + 2)
    for i in range(X + 3, X + w * T - 2, 4): P.r(i, Y + 9, 1, h * T, (112, 78, 48))
    cx = X + w * T // 2
    P.r(cx - 7, Y + h * T - 6, 14, 15, (80, 50, 30)); P.o(cx - 7, Y + h * T - 6, 14, 15)
    P.r(cx - 2, Y + h * T + 1, 4, 3, (210, 180, 80))

def o_banner(P, x, y, w, h, color=(180, 40, 40), **k):
    X, Y = x * T, y * T
    P.r(X + 7, Y - 14, 2, 30, (90, 60, 40))
    P.poly([(X + 9, Y - 13), (X + 16, Y - 10), (X + 9, Y - 6)], color, OUTL)

def o_weapons(P, x, y, w, h, **k):
    X, Y = x * T, y * T
    P.r(X + 1, Y + 10, w * T - 2, 3, WOOD_D)
    for i in range(X + 4, X + w * T - 3, 5):
        P.r(i, Y - 10, 1, 23, (120, 90, 60)); P.poly([(i - 1, Y - 10), (i + 1, Y - 10), (i, Y - 14)], (190, 190, 200))

def o_lantern(P, x, y, w, h, **k):
    X, Y = x * T, y * T
    P.r(X + 7, Y + 2, 2, 13, (90, 60, 40))
    P.e(X + 2, Y - 6, 12, 10, (236, 120, 140), OUTL)
    for i in range(3): P.e(X + 3 + i * 3, Y - 7, 4, 5, (250, 170, 190))
    P.e(X + 6, Y - 2, 4, 3, (255, 230, 150))

def o_stand(P, x, y, w, h, **k):  # 족두리 받침
    X, Y = x * T, y * T
    box3d(P, X + 3, Y + 8, 10, 8, WOOD, WOOD_D, depth=3)
    P.e(X + 4, Y + 2, 8, 7, (30, 28, 40), OUTL); P.p(X + 8, Y + 1, (220, 180, 60)); P.p(X + 6, Y + 4, (200, 60, 70))

def o_typecase(P, x, y, w, h, **k):
    X, Y = x * T, y * T
    box3d(P, X + 1, Y + 2, w * T - 2, 13, (120, 84, 54), (90, 60, 38))
    for i in range(X + 3, X + w * T - 3, 3):
        for j in range(Y + 4, Y + 10, 3):
            P.r(i, j, 2, 2, (170, 164, 140))

def o_box_small(P, x, y, w, h, color=(120, 90, 60), **k):
    X, Y = x * T, y * T
    for i in range(w):
        box3d(P, X + i * T + 2, Y + 4 - (i % 2) * 2, 12, 11 + (i % 2) * 2, color, sh(color, 0.75), depth=4)
        P.r(X + i * T + 5, Y + 6 - (i % 2) * 2, 6, 3, sh(color, 1.15))

def o_gate(P, x, y, w, h, **k):
    X, Y = x * T, y * T - 6
    P.e(X - 4, Y - 6, w * T + 8, h * T + 12, (255, 236, 160))
    P.e(X + 1, Y, w * T - 2, h * T + 4, (80, 64, 110), OUTL)
    P.e(X + 6, Y + 5, w * T - 12, h * T - 6, (255, 244, 200))
    P.e(X + 12, Y + 12, w * T - 24, h * T - 20, (255, 255, 240))
    for i, c in enumerate([(120, 175, 160), (225, 210, 175), (150, 140, 110)]):
        P.e(X + 10 + i * 10, Y + h * T - 2, 7, 6, c, OUTL)

def o_small_table(P, x, y, w, h, **k):
    X, Y = x * T, y * T
    box3d(P, X + 2, Y + 5, 12, 10, WOOD, WOOD_D, depth=4)
    P.r(X + 4, Y + 6, 8, 4, PAPER); P.r(X + 9, Y + 7, 2, 2, (200, 40, 40))

def o_vase_plant(P, x, y, w, h, **k):
    X, Y = x * T, y * T
    P.e(X + 4, Y + 6, 8, 9, (120, 160, 150), OUTL)
    for dx, dy in ((-3, -6), (0, -9), (3, -6), (5, -3), (-5, -3)):
        P.e(X + 6 + dx, Y + 4 + dy, 5, 5, (70, 130, 70), OUTL)

def o_cabinet(P, x, y, w, h, **k):
    X, Y = x * T, y * T - 12
    P.r(X + 1, Y, w * T - 2, 27, (126, 70, 44)); P.o(X + 1, Y, w * T - 2, 27)
    P.r(X + w * T // 2, Y + 2, 1, 23, (80, 44, 28))
    P.r(X + 4, Y + 3, w * T // 2 - 6, 22, (146, 84, 52)); P.r(X + w * T // 2 + 2, Y + 3, w * T // 2 - 6, 22, (146, 84, 52))
    P.p(X + w * T // 2 - 2, Y + 14, (220, 190, 90)); P.p(X + w * T // 2 + 2, Y + 14, (220, 190, 90))

def o_soju(P, x, y, w, h, **k):
    o_jar(P, x, y, w, h, content=(230, 236, 240), color=(70, 60, 56))
    X, Y = x * T, y * T
    P.r(X + 6, Y + 9, 4, 3, (236, 226, 190))

def o_vase(P, x, y, w, h, **k):
    X, Y = x * T, y * T
    cx = X + 8
    P.e(cx - 5, Y + 2, 10, 13, (120, 170, 150), OUTL); P.r(cx - 2, Y - 2, 4, 5, (120, 170, 150)); P.o(cx - 2, Y - 2, 4, 5)
    P.p(cx - 2, Y + 6, (250, 250, 250)); P.p(cx + 1, Y + 8, (40, 40, 40))

DRAW = {
    'desk': o_desk, 'chest': o_chest, 'screen': o_screen, 'wall': o_wall_frame, 'throne': o_throne,
    'pillar': o_pillar, 'jar': o_jar, 'display': o_display, 'kiln': o_kiln, 'shelf': o_shelf, 'rack': o_rack,
    'wood': o_wood, 'wheel': o_wheel, 'basket': o_basket, 'tent': o_tent, 'armory': o_armory, 'banner': o_banner,
    'weapons': o_weapons, 'lantern': o_lantern, 'stand': o_stand, 'typecase': o_typecase, 'boxs': o_box_small,
    'gate': o_gate, 'stable': o_small_table, 'plant': o_vase_plant, 'cabinet': o_cabinet, 'soju': o_soju, 'vase': o_vase,
}

# ======================================================================== 방 정의
# obj: (style, id or None, x, y, w, h, opts)  opts: events ('all'|'none'|list), trigger, draw kwargs
def O(style, oid, x, y, w=1, h=1, events='all', trigger=0, **kw):
    return dict(style=style, id=oid, x=x, y=y, w=w, h=h, events=events, trigger=trigger, kw=kw)

# npc: (id, sprite, x, y, dir)
DIRS = {'down': 2, 'left': 4, 'right': 6, 'up': 8}

THEMES = {
    'palace': dict(top=(70, 52, 50), top_pat='giwa', face_kind='palace', face=(236, 226, 200), floor=('maru', (176, 122, 74)), floor_col=(176, 122, 74)),
    'workshop': dict(top=(84, 66, 50), face_kind='earth', face=(196, 160, 116), floor=('earth', (164, 128, 90)), floor_col=(164, 128, 90)),
    'mansion': dict(top=(62, 48, 44), top_pat='giwa', face_kind='wood', face=(140, 96, 62), floor=('maru', (150, 102, 64)), floor_col=(150, 102, 64)),
    'ganghwa': dict(top=(52, 84, 58), face_kind='palisade', face=(136, 98, 62), floor=('grass', (104, 150, 82)), floor_col=(104, 150, 82)),
    'dojang': dict(top=(70, 54, 44), face_kind='wood', face=(150, 110, 70), floor=('maru', (160, 118, 78)), floor_col=(160, 118, 78)),
    'yuan': dict(top=(56, 56, 70), top_pat='giwa', face_kind='palace', face=(230, 222, 204), dan1=(52, 96, 140), floor=('jeondol', (150, 146, 136)), floor_col=(150, 146, 136)),
    'temple': dict(top=(60, 58, 66), top_pat='giwa', face_kind='temple', face=(232, 222, 196), floor=('stone', (150, 144, 132)), floor_col=(150, 144, 132)),
    'ending': dict(top=(40, 38, 54), top_pat='giwa', face_kind='palace', face=(214, 204, 186), dan1=(70, 60, 120), floor=('jeondol', (120, 116, 112)), floor_col=(120, 116, 112)),
}

ROOMS = [
  dict(map=1, key='palace', name='01 개경 왕궁 (918)', parallax='!bg_palace', rug=(6, 5, 5, 5, (150, 40, 44), (214, 176, 80)),
       objs=[O('screen', 'hunyo', 2, 2, 3, 1, erased=True), O('wall', 'portrait', 6, 1, 1, 1, kind='scroll', figure=True),
             O('wall', 'map_north', 8, 1, 2, 1, kind='map'), O('throne', 'throne', 12, 2, 3, 2, events=[(12, 3), (13, 3), (14, 3)]),
             O('desk', 'desk', 3, 6, 2, 1, things=['paper', 'ink']), O('chest', 'box', 12, 7, 2, 1),
             O('pillar', None, 5, 4), O('pillar', None, 11, 4), O('plant', None, 1, 2), O('plant', None, 15, 11),
             O('cabinet', None, 14, 6, 2, 1, events='none')],
       npcs=[('minister', 'npc_minister', 9, 8, 'down')], doors=['right_gate']),
  dict(map=2, key='workshop', name='02 청자 공방 (12세기)', parallax='!bg_workshop',
       objs=[O('wall', 'hanja', 2, 1, 2, 1, kind='hanja'), O('desk', 'book_song', 2, 5, 2, 1, things=['book']),
             O('chest', 'toolbox', 12, 2, 2, 1), O('display', 'sample', 7, 2, 2, 1), O('kiln', 'kiln', 12, 7, 3, 3),
             O('jar', 'jar_white', 2, 9, content=(244, 242, 236)), O('jar', 'jar_red', 4, 9, content=(176, 76, 52)),
             O('wheel', None, 9, 5), O('shelf', None, 14, 2, 2, 1, stuff='pots')],
       npcs=[('potter', 'npc_potter', 8, 5, 'down'), ('apprentice', 'npc_apprentice', 5, 7, 'down')], doors=['left', 'right']),
  dict(map=3, key='mansion', name='03 최충헌의 집 (무신 집권기)', parallax='!bg_mansion', rug=(5, 4, 7, 4, (70, 90, 70), (200, 170, 100)),
       objs=[O('wall', 'painting', 2, 1, 2, 1, kind='painting'), O('wall', 'rulers', 6, 1, 4, 1, kind='portraits'),
             O('boxs', 'paper_pile', 13, 3, 2, 1, color=(220, 190, 80)), O('cabinet', None, 11, 2, 2, 1),
             O('plant', None, 1, 2), O('vase', None, 15, 2), O('stable', None, 6, 10), O('jar', None, 14, 11, color=(110, 84, 60)),
             O('jar', None, 15, 11, color=(96, 74, 54)), O('plant', None, 1, 11)],
       npcs=[('manjeok', 'npc_slave_a', 8, 5, 'down'), ('sunjeong', 'npc_slave_b', 3, 7, 'right'),
             ('yeonbok', 'npc_slave_c', 8, 9, 'up'), ('mijoi', 'npc_slave_d', 13, 8, 'left')], doors=['left', 'right']),
  dict(map=4, key='ganghwa', name='04 강화도 군영 (대몽항쟁)', parallax='!bg_ganghwa',
       objs=[O('wall', 'castle_map', 2, 1, 2, 1, kind='map'), O('desk', 'records', 3, 6, 2, 1, things=['scrolls']),
             O('armory', 'armory', 12, 2, 3, 2, events=[(12, 3), (13, 3), (14, 3)]), O('tent', None, 6, 2, 3, 2),
             O('banner', None, 10, 3), O('banner', None, 4, 3, color=(40, 80, 160)), O('weapons', None, 14, 7, 2, 1),
             O('stable', 'mongol_letter', 11, 7)],
       npcs=[('soldier', 'npc_soldier', 7, 6, 'down')], doors=['left', 'right']),
  dict(map=5, key='dojang', name='05 대장도감 (대몽항쟁)', parallax='!bg_dojang',
       objs=[O('wall', 'notice', 2, 1, 2, 1, kind='paper'), O('wall', 'cheonja', 6, 1, 2, 1, kind='hanja'),
             O('rack', 'rack', 10, 2, 5, 1, gap=True), O('desk', 'board', 6, 8, 2, 1, things=['board']),
             O('shelf', 'ink_shelf', 2, 5, 1, 1, stuff='ink'), O('basket', 'paper_basket', 2, 9), O('wood', 'wood', 12, 8, 3, 2),
             O('desk', None, 9, 5, 2, 1, things=['board']), O('jar', None, 15, 11, color=(70, 70, 76))],
       npcs=[('monk', 'npc_monk', 5, 4, 'down')], doors=['left', 'right']),
  dict(map=6, key='yuan', name='06 개경 궁궐 (원 간섭기)', parallax='!bg_yuan', rug=(6, 4, 5, 6, (60, 70, 130), (220, 190, 100)),
       objs=[O('wall', 'decree', 2, 1, 2, 1, kind='paper'), O('wall', 'obj_hair', 5, 1, 1, 1, kind='hair'),
             O('wall', 'war_map', 11, 1, 3, 1, kind='grid'), O('stand', 'obj_jok', 3, 6), O('soju', 'obj_soju', 14, 5),
             O('vase', 'obj_celadon', 7, 7), O('lantern', 'obj_lantern', 14, 9), O('desk', 'jokbo', 3, 10, 2, 1, things=['book']),
             O('desk', 'war_table', 10, 7, 2, 1, things=['map']), O('pillar', None, 5, 3, color=(60, 90, 140)),
             O('pillar', None, 11, 4, color=(60, 90, 140))],
       npcs=[('king', 'npc_king', 8, 3, 'down'), ('lady', 'npc_lady', 4, 4, 'down')], doors=['left', 'right']),
  dict(map=7, key='temple', name='07 흥덕사 (고려 말)', parallax='!bg_temple',
       objs=[O('wall', 'colophon', 2, 1, 2, 1, kind='hanja'), O('wall', 'era_table', 5, 1, 2, 1, kind='paper'),
             O('wall', 'record', 8, 1, 1, 1, kind='scroll'), O('shelf', 'library', 12, 2, 3, 1, stuff='books'),
             O('typecase', 'typecase', 2, 7, 2, 1), O('desk', 'book', 8, 8, 2, 1, things=['book']),
             O('boxs', 'gunpowder', 14, 8, color=(90, 70, 60)), O('plant', None, 15, 11), O('lantern', None, 10, 4),
             O('lantern', None, 4, 4), O('plant', None, 1, 2)],
       npcs=[('monk', 'npc_monk2', 6, 5, 'down')], doors=['left', 'right']),
  dict(map=8, key='ending', name='08 개경 (여말선초, 1392)', parallax='!bg_ending', rug=(6, 5, 5, 6, (120, 30, 40), (220, 190, 100)),
       objs=[O('gate', 'gate', 7, 1, 3, 3, events=[(7, 3), (8, 3), (9, 3), (7, 2), (9, 2)]),
             O('desk', 'scrolls', 7, 8, 3, 1, things=['scrolls']), O('stable', 'land', 13, 9),
             O('pillar', None, 4, 3), O('pillar', None, 12, 3)],
       npcs=[('jeong_mongju', 'npc_scholar_a', 3, 6, 'down'), ('jeong_dojeon', 'npc_scholar_b', 13, 6, 'down'),
             ('yi_seonggye', 'npc_general', 5, 9, 'right')], doors=['left']),
]

# ======================================================================== 생성
def make_event(eid, name, x, y, trigger, sprite=None, direction=2):
    page = {
        "conditions": {"actorId": 1, "actorValid": False, "itemId": 1, "itemValid": False, "selfSwitchCh": "A",
                       "selfSwitchValid": False, "switch1Id": 1, "switch1Valid": False, "switch2Id": 1,
                       "switch2Valid": False, "variableId": 1, "variableValid": False, "variableValue": 0},
        "directionFix": False,
        "image": {"characterIndex": 0, "characterName": sprite or "", "direction": direction, "pattern": 1, "tileId": 0},
        "list": [{"code": 0, "indent": 0, "parameters": []}],
        "moveFrequency": 3,
        "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
        "moveSpeed": 3, "moveType": 0, "priorityType": 1, "stepAnime": False, "through": False,
        "trigger": trigger, "walkAnime": True}
    return {"id": eid, "name": name, "note": "", "pages": [page], "x": x, "y": y}

def snd():
    return {"name": "", "pan": 0, "pitch": 100, "volume": 90}

if __name__ == '__main__' and '--old' not in sys.argv:
    print('make_world.py는 방 배치(ROOMS) 모듈입니다. 지도는 wide_maps.py, 방 그림은 hd_wide.py로 만드세요. (예전 17칸 방식: --old)')
    sys.exit(0)

if __name__ == '__main__':
    os.makedirs(os.path.join(OUT, 'img/parallaxes'), exist_ok=True)
    os.makedirs(os.path.join(OUT, 'data'), exist_ok=True)
    infos = [None]
    for room in ROOMS:
        th = THEMES[room['key']]
        P = Px()
        floor(P, th['floor'][0], th['floor'][1], seed=room['map'])
        if room.get('rug'):
            rug(P, *room['rug'])
        walls(P, th)
        doors = room['doors']
        if 'left' in doors: side_door(P, 'left', th)
        if 'right' in doors: side_door(P, 'right', th)
        if 'right_gate' in doors: palace_gate_door(P)
        # 그림자 먼저
        for o in room['objs']:
            if o['y'] >= 2 and o['style'] not in ('wall',):
                X, Y = o['x'] * T, (o['y'] + o['h']) * T
                P.d.rectangle([X + 2, Y - 1, X + o['w'] * T - 1, Y], fill=sh(th['floor_col'], 0.7))
        for o in sorted(room['objs'], key=lambda o: o['y']):
            DRAW[o['style']](P, o['x'], o['y'], o['w'], o['h'], **o['kw'])
        big = P.im.resize((W * T * 3, H * T * 3), Image.NEAREST)
        big.save(os.path.join(OUT, 'img/parallaxes', room['parallax'] + '.png'))

        # 리전(벽)
        region = [[0] * W for _ in range(H)]
        for x in range(W):
            region[0][x] = region[1][x] = region[12][x] = 1
        for y in range(H):
            region[y][0] = region[y][16] = 1
        for o in room['objs']:
            for ty in range(o['y'], o['y'] + o['h']):
                for tx in range(o['x'], o['x'] + o['w']):
                    region[ty][tx] = 1
        data = [0] * (W * H * 6)
        for y in range(H):
            for x in range(W):
                data[(5 * H + y) * W + x] = region[y][x]

        events = [None]
        def add(name, x, y, trig=0, sprite=None, d=2):
            events.append(make_event(len(events), name, x, y, trig, sprite, d))
        for o in room['objs']:
            if not o['id'] or o['events'] == 'none': continue
            tiles = [(tx, ty) for ty in range(o['y'], o['y'] + o['h']) for tx in range(o['x'], o['x'] + o['w'])] if o['events'] == 'all' else o['events']
            for tx, ty in tiles: add(o['id'], tx, ty, o['trigger'])
        for nid, sprite, x, y, d in room['npcs']:
            add(nid, x, y, 0, '$' + sprite, DIRS[d])
        if 'left' in doors: add('back', 0, 9, 1)
        if 'right' in doors or 'right_gate' in doors: add('exit', 16, 9, 1)

        mp = {"autoplayBgm": False, "autoplayBgs": False, "battleback1Name": "", "battleback2Name": "", "bgm": snd(), "bgs": snd(),
              "disableDashing": False, "displayName": "", "encounterList": [], "encounterStep": 30, "height": H, "note": "",
              "parallaxLoopX": False, "parallaxLoopY": False, "parallaxName": room['parallax'], "parallaxShow": True,
              "parallaxSx": 0, "parallaxSy": 0, "scrollType": 0, "specifyBattleback": False, "tilesetId": 3, "width": W,
              "data": data, "events": events}
        json.dump(mp, open(os.path.join(OUT, 'data', 'Map%03d.json' % room['map']), 'w', encoding='utf-8'), ensure_ascii=False)
        infos.append({"id": room['map'], "expanded": False, "name": room['name'], "order": room['map'], "parentId": 0, "scrollX": 408, "scrollY": 312})
    json.dump(infos, open(os.path.join(OUT, 'data', 'MapInfos.json'), 'w', encoding='utf-8'), ensure_ascii=False)

    # 미리보기
    prev = Image.new('RGB', (816, 624 * 2))
    for i, room in enumerate(ROOMS):
        im = Image.open(os.path.join(OUT, 'img/parallaxes', room['parallax'] + '.png')).resize((204, 156))
        prev.paste(im, ((i % 4) * 204, (i // 4) * 156))
    prev.crop((0, 0, 816, 312)).save(os.path.join(sys.argv[2], '_rooms_preview.png'))
    print('rooms:', len(ROOMS))
