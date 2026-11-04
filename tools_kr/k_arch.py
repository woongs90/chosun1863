"""종로 사진관 편 건물·소품 (1945~1953 서울·38선·부산·흥남·판문점, 1983 여의도)
 shophouse  근대 상가(2층, 큰 간판)       hanok / choga  기와집 / 초가집(정면)
 pole·wires 전봇대와 전선                  tram       전차 (옆모습)
 poster_board 벽보판   banner 현수막      flagpole   깃대
 prison_wall 서대문 형무소 담·문·망루      capitol    조선 총독부(중앙청) 건물
 station    서울역(붉은 벽돌 + 돔)          seokjojeon 덕수궁 석조전(돌기둥)
 c47 비행기 · tent 천막 · booth 기표소 · ballot_box 투표함 · shack 판잣집 · stall 노점 · ship 화물선 · truss_bridge 철교
 sign38 38선 표지 · barrier 차단기 · kbs 방송국 · paper_wall 벽보 가득한 벽
 사진관 안: backdrop 촬영 배경막 · tripod 큰 사진기 · darkroom 암실 문 · shelf 진열장 · counter 계산대 · wardrobe 장롱
"""
import math, random
from PIL import Image, ImageDraw
from k_gfx import Prop, soft_shadow, label, TS, F, sh, mix, glow, _paste

WHITE = (244, 242, 236)
RED_T, BLUE_T = (205, 46, 58), (0, 71, 160)
GIWA = (78, 84, 92)

def text_c(d, xy, t, size, fill, kind='sans', anchor='mm'):
    d.text(xy, t, font=F(size, kind), fill=fill, anchor=anchor)

# ------------------------------------------------------------------ 태극기 (국기 규격: 가로:세로 = 3:2)
def taegeukgi(w, h=None, wave=0.0, aged=False):
    """정확한 태극기 그림 (RGBA). 4괘: 건(왼쪽 위) 감(오른쪽 위) 리(왼쪽 아래) 곤(오른쪽 아래).
    태극: 깃면 대각선(왼쪽 위~오른쪽 아래) 위에 작은 반원 둘 - 왼쪽은 아래로 볼록, 오른쪽은 위로 볼록. 위 빨강, 아래 파랑."""
    if h is None: h = w * 2 // 3
    S = 4
    W_, H_ = w * S, h * S
    im = Image.new('RGBA', (W_, H_), (255, 255, 255, 255))
    d = ImageDraw.Draw(im)
    cx, cy = W_ / 2, H_ / 2
    R = H_ / 4                                  # 태극 지름 = 세로의 1/2
    L = math.hypot(W_, H_)
    ux, uy = W_ / L, H_ / L                     # 대각선 방향(왼쪽 위 → 오른쪽 아래)
    nx, ny = uy, -ux                            # 대각선에 수직(위쪽)
    # 태극 = 위 반원(빨강) + 아래 반원(파랑) + 작은 반원 둘
    def semi(cx_, cy_, r, up, col):
        pts = []
        for i in range(61):
            a = math.pi * i / 60
            vx = math.cos(a) * ux + math.sin(a) * nx * (1 if up else -1)
            vy = math.cos(a) * uy + math.sin(a) * ny * (1 if up else -1)
            pts.append((cx_ + vx * r, cy_ + vy * r))
        d.polygon(pts, fill=col)
    red, blue = RED_T, BLUE_T
    semi(cx, cy, R, True, red)                  # 대각선 위쪽 = 빨강
    semi(cx, cy, R, False, blue)                # 대각선 아래쪽 = 파랑
    # 왼쪽 작은 반원(대각선 왼쪽 위 절반의 가운데): 아래로 볼록 → 빨강이 아래로 내려옴
    lx, ly = cx - ux * R / 2, cy - uy * R / 2
    semi(lx, ly, R / 2, False, red)
    # 오른쪽 작은 반원: 위로 볼록 → 파랑이 위로 올라옴
    rx, ry = cx + ux * R / 2, cy + uy * R / 2
    semi(rx, ry, R / 2, True, blue)
    # 4괘 (태극 지름 D = 세로 1/2 기준): 괘 길이 D/2, 효 너비 D/12, 효 사이·끊긴 틈 D/24, 태극과 괘 사이 D/4
    D_ = 2 * R
    bar_w = D_ / 12; gap = D_ / 24; blen = D_ / 2; brk = D_ / 24
    inner = R + D_ / 4
    def gwae(dirx, diry, pattern):
        # dir: 가운데에서 모서리 쪽 단위 벡터, pattern: 안쪽부터 바깥쪽으로 3효 (True=이어진 효)
        px_, py_ = -diry, dirx                   # 효 방향(괘 길이 방향)
        for k, solid in enumerate(pattern):
            off = inner + k * (bar_w + gap) + bar_w / 2
            mx, my = cx + dirx * off, cy + diry * off
            segs = [(-blen / 2, blen / 2)] if solid else [(-blen / 2, -brk / 2), (brk / 2, blen / 2)]
            for a, b in segs:
                p1 = (mx + px_ * a - dirx * bar_w / 2, my + py_ * a - diry * bar_w / 2)
                p2 = (mx + px_ * b - dirx * bar_w / 2, my + py_ * b - diry * bar_w / 2)
                p3 = (mx + px_ * b + dirx * bar_w / 2, my + py_ * b + diry * bar_w / 2)
                p4 = (mx + px_ * a + dirx * bar_w / 2, my + py_ * a + diry * bar_w / 2)
                d.polygon([p1, p2, p3, p4], fill=(0, 0, 0))
    D1 = (-ux, -uy); D2 = (ux, -uy); D3 = (-ux, uy); D4 = (ux, uy)
    gwae(*D1, [True, True, True])               # 건 ☰ 왼쪽 위
    gwae(*D4, [False, False, False])            # 곤 ☷ 오른쪽 아래
    gwae(*D2, [False, True, False])             # 감 ☵ 오른쪽 위
    gwae(*D3, [True, False, True])              # 리 ☲ 왼쪽 아래
    im = im.resize((w, h), Image.LANCZOS)
    if aged:
        a = Image.new('RGBA', im.size, (232, 214, 170, 60)); im.alpha_composite(a)
    if wave:
        arr = im.copy(); out = Image.new('RGBA', im.size, (0, 0, 0, 0))
        for x in range(w):
            dy = int(round(math.sin(x / w * math.pi * 1.6 + wave) * h * 0.04))
            out.paste(arr.crop((x, 0, x + 1, h)), (x, dy))
        im = out
    return im

def hinomaru(w, h=None):
    if h is None: h = w * 2 // 3
    im = Image.new('RGBA', (w, h), (250, 250, 248, 255)); d = ImageDraw.Draw(im)
    r = h * 3 / 10
    d.ellipse([w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r], fill=(200, 30, 40))
    return im

def us_flag(w, h=None):
    if h is None: h = int(w * 10 / 19)
    im = Image.new('RGBA', (w, h), (255, 255, 255, 255)); d = ImageDraw.Draw(im)
    for k in range(13):
        if k % 2 == 0: d.rectangle([0, k * h / 13, w, (k + 1) * h / 13], fill=(178, 34, 52))
    d.rectangle([0, 0, w * 0.4, h * 7 / 13], fill=(60, 59, 110))
    for i in range(5):
        for j in range(6):
            d.point((int(w * 0.4 * (j + 0.5) / 6), int(h * 7 / 13 * (i + 0.5) / 5)), fill=(255, 255, 255))
    return im

def un_flag(w, h=None):
    if h is None: h = w * 2 // 3
    im = Image.new('RGBA', (w, h), (91, 146, 229, 255)); d = ImageDraw.Draw(im)
    r = h * 0.32
    d.ellipse([w / 2 - r, h / 2 - r, w / 2 + r, h / 2 + r], outline=(255, 255, 255), width=max(1, w // 30))
    d.ellipse([w / 2 - r * 0.45, h / 2 - r * 0.45, w / 2 + r * 0.45, h / 2 + r * 0.45], outline=(255, 255, 255), width=max(1, w // 40))
    return im

# ------------------------------------------------------------------ 근대 상가
def shophouse(big, tx, ty, w=3, h=3, wall=(196, 176, 150), roof='flat', sign=None, sign_c=(40, 60, 70), sign_t=(250, 240, 210),
              shutter=(120, 90, 60), door='center', seed=0, floors=2, poster=False, flags=0, glass=True, awning=None, night=False, broken=False):
    """1940년대 종로 2층 상가 앞모습. roof: flat(난간) / giwa(기와) / tin(함석)"""
    rnd = random.Random(seed + tx * 13 + ty * 7)
    X, Y, W, H = tx * TS, ty * TS, w * TS, h * TS
    soft_shadow(big, [X + 4, Y + H - 8, X + W + 8, Y + H + 6], 90, 5)
    with Prop(big, X - 6, Y - 30, W + 12, H + 30, 0.5) as d:
        ox, oy = 6, 30
        if roof == 'giwa':
            rh = 26
            d.polygon([(ox - 6, oy + rh), (ox + W + 6, oy + rh), (ox + W - 4, oy + 2), (ox + 4, oy + 2)], fill=GIWA)
            for xx in range(ox - 4, ox + W + 6, 5): d.line([(xx, oy + 4), (xx - 2, oy + rh)], fill=sh(GIWA, 0.75))
            for xx in range(ox - 6, ox + W + 6, 5): d.chord([xx, oy + rh - 3, xx + 5, oy + rh + 2], 0, 180, fill=sh(GIWA, 1.25))
            d.rectangle([ox + 2, oy - 2, ox + W - 2, oy + 3], fill=sh(GIWA, 0.6))
            d.polygon([(ox - 8, oy + 1), (ox + 2, oy - 2), (ox + 6, oy + 4)], fill=sh(GIWA, 0.8))
            d.polygon([(ox + W + 8, oy + 1), (ox + W - 2, oy - 2), (ox + W - 6, oy + 4)], fill=sh(GIWA, 0.8))
            wy0 = oy + rh
        elif roof == 'tin':
            rh = 18
            d.polygon([(ox - 4, oy + rh), (ox + W + 4, oy + rh), (ox + W, oy + 4), (ox, oy + 4)], fill=(120, 116, 106))
            for xx in range(ox, ox + W, 4): d.line([(xx, oy + 4), (xx, oy + rh)], fill=(150, 146, 136))
            wy0 = oy + rh
        else:
            d.rectangle([ox, oy + 4, ox + W, oy + 14], fill=sh(wall, 0.92))
            d.rectangle([ox - 2, oy + 2, ox + W + 2, oy + 6], fill=sh(wall, 1.08))
            for xx in range(ox + 6, ox + W - 4, 10): d.rectangle([xx, oy + 7, xx + 4, oy + 12], fill=sh(wall, 0.78))
            wy0 = oy + 14
        d.rectangle([ox, wy0, ox + W, oy + H - 2], fill=wall)
        for yy in range(wy0 + 6, oy + H - 2, 7): d.line([(ox + 1, yy), (ox + W - 1, yy)], fill=sh(wall, 0.94))
        for _ in range(w * 3):
            sx, sy = ox + rnd.randint(3, W - 8), wy0 + rnd.randint(3, max(4, H - (wy0 - oy) - 10))
            d.rectangle([sx, sy, sx + rnd.randint(2, 6), sy + rnd.randint(3, 8)], fill=sh(wall, 0.9))
        gy = oy + H - 44
        if floors >= 2:
            n = w + 1
            for k in range(n):
                wx = ox + 8 + (W - 16) * (k + 0.5) / n
                ww = min(16, (W - 16) / n - 6)
                lit = night and rnd.random() < 0.5
                d.rectangle([wx - ww / 2 - 2, wy0 + 6, wx + ww / 2 + 2, wy0 + 30], fill=(226, 216, 196))
                d.rectangle([wx - ww / 2, wy0 + 8, wx + ww / 2, wy0 + 28], fill=(250, 210, 130) if lit else (70, 84, 96))
                if broken and rnd.random() < 0.5:
                    d.polygon([(wx - ww / 2, wy0 + 8), (wx + 2, wy0 + 16), (wx - ww / 2, wy0 + 24)], fill=(30, 30, 34))
                d.line([(wx, wy0 + 8), (wx, wy0 + 28)], fill=(226, 216, 196)); d.line([(wx - ww / 2, wy0 + 17), (wx + ww / 2, wy0 + 17)], fill=(226, 216, 196))
        # 간판 (가로로 긴 나무 간판)
        sy0 = gy - 16
        if sign:
            d.rectangle([ox + 4, sy0, ox + W - 4, gy - 1], fill=sign_c)
            d.rectangle([ox + 4, sy0, ox + W - 4, sy0 + 1], fill=sh(sign_c, 1.5))
            d.rectangle([ox + 4, gy - 2, ox + W - 4, gy - 1], fill=sh(sign_c, 0.6))
            fs = 13 if len(sign) <= (w * 2 + 1) else 11
            d.text((ox + W / 2, sy0 + 8), sign, font=F(fs, 'serif'), fill=sign_t, anchor='mm')
        if poster:
            for k in range(2):
                px_ = ox + 6 + rnd.randint(0, max(1, W - 24))
                pc = rnd.choice([(236, 226, 196), (230, 236, 240), (240, 220, 210)])
                d.rectangle([px_, sy0 - 26 + k * 3, px_ + 12, sy0 - 8 + k * 3], fill=pc)
                for yy in range(sy0 - 23 + k * 3, sy0 - 10 + k * 3, 3): d.line([(px_ + 2, yy), (px_ + 10, yy)], fill=(80, 70, 60))
        # 1층
        d.rectangle([ox, gy, ox + W, oy + H - 2], fill=sh(wall, 0.86))
        dxm = ox + W / 2 if door == 'center' else (ox + W - 22 if door == 'right' else ox + 22)
        if glass:
            for k in range(w * 2):
                gx0 = ox + 4 + k * (W - 8) / (w * 2)
                gx1 = gx0 + (W - 8) / (w * 2) - 3
                if gx0 - 4 < dxm < gx1 + 4: continue
                d.rectangle([gx0, gy + 4, gx1, oy + H - 8], fill=(250, 212, 140) if night else (84, 100, 108))
                d.line([(gx0 + 2, gy + 6), (gx0 + 2, gy + 18)], fill=(130, 150, 160))
                d.rectangle([gx0, oy + H - 8, gx1, oy + H - 3], fill=sh(wall, 0.7))
        else:
            for k in range(int(W / 8)):
                xx = ox + 2 + k * 8
                if abs(xx + 4 - dxm) < 10: continue
                d.rectangle([xx, gy + 3, xx + 7, oy + H - 3], fill=sh(shutter, 0.92 + (k % 2) * 0.1))
                d.line([(xx, gy + 3), (xx, oy + H - 3)], fill=sh(shutter, 0.65))
        d.rectangle([dxm - 9, gy + 3, dxm + 9, oy + H - 2], fill=sh(shutter, 0.6))
        d.rectangle([dxm - 7, gy + 6, dxm + 7, gy + 22], fill=(90, 110, 118) if not night else (250, 210, 130))
        d.line([(dxm, gy + 3), (dxm, oy + H - 2)], fill=sh(shutter, 0.4))
        if awning:
            ac = awning
            d.polygon([(ox + 2, gy - 1), (ox + W - 2, gy - 1), (ox + W + 2, gy + 9), (ox - 2, gy + 9)], fill=ac)
            for xx in range(ox + 2, ox + W, 10): d.polygon([(xx, gy - 1), (xx + 5, gy - 1), (xx + 6, gy + 9), (xx + 1, gy + 9)], fill=sh(ac, 1.25))
        for k in range(flags):
            fx = ox + 10 + k * (W - 20) / max(1, flags - 1) if flags > 1 else ox + W / 2
            d.line([(fx, sy0 - 2), (fx + 10, sy0 - 18)], fill=(130, 100, 70))
            fl = taegeukgi(18, 12)
            _fl = fl
            d._image.paste(_fl, (int(fx + 8), int(sy0 - 30)), _fl)

# ------------------------------------------------------------------ 기와집·초가집
def hanok(big, tx, ty, w=4, h=2, wall=(236, 230, 214), wood=(120, 80, 50), roof=GIWA, seed=0, doors=True):
    X, Y, W, H = tx * TS, ty * TS, w * TS, h * TS
    soft_shadow(big, [X + 6, Y + H - 6, X + W + 8, Y + H + 6], 90, 5)
    with Prop(big, X - 14, Y - 34, W + 28, H + 34, 0.5) as d:
        ox, oy = 14, 34
        # 처마 곡선 지붕
        rh = 40
        top = [(ox - 12, oy + rh - 8), (ox + 6, oy + 6), (ox + W - 6, oy + 6), (ox + W + 12, oy + rh - 8)]
        d.polygon([(ox - 14, oy + rh - 12), (ox + 4, oy + 2), (ox + W - 4, oy + 2), (ox + W + 14, oy + rh - 12), (ox + W + 8, oy + rh), (ox - 8, oy + rh)], fill=roof)
        for xx in range(ox - 6, ox + W + 8, 5): d.line([(xx, oy + 6), (xx + (xx - ox - W / 2) * 0.08, oy + rh - 2)], fill=sh(roof, 0.75))
        for xx in range(ox - 10, ox + W + 10, 5): d.chord([xx, oy + rh - 4, xx + 5, oy + rh + 1], 0, 180, fill=sh(roof, 1.3))
        d.rectangle([ox + 4, oy - 2, ox + W - 4, oy + 4], fill=sh(roof, 0.55))
        d.polygon([(ox - 2, oy - 4), (ox + 8, oy - 2), (ox + 6, oy + 4), (ox - 4, oy + 2)], fill=sh(roof, 0.75))
        d.polygon([(ox + W + 2, oy - 4), (ox + W - 8, oy - 2), (ox + W - 6, oy + 4), (ox + W + 4, oy + 2)], fill=sh(roof, 0.75))
        wy = oy + rh
        d.rectangle([ox, wy, ox + W, oy + H - 6], fill=wall)
        d.rectangle([ox, wy, ox + W, wy + 3], fill=sh(wall, 0.7))
        # 기둥과 문
        n = w * 2
        for k in range(n + 1):
            xx = ox + k * W / n
            d.rectangle([xx - 2, wy, xx + 2, oy + H - 6], fill=wood)
        if doors:
            for k in range(n):
                x0 = ox + k * W / n + 4; x1 = ox + (k + 1) * W / n - 4
                d.rectangle([x0, wy + 8, x1, oy + H - 12], fill=(238, 232, 214))
                for xx in range(int(x0) + 3, int(x1), 4): d.line([(xx, wy + 8), (xx, oy + H - 12)], fill=sh(wood, 1.2))
                for yy in range(int(wy) + 11, oy + H - 12, 5): d.line([(x0, yy), (x1, yy)], fill=sh(wood, 1.2))
        # 기단
        d.rectangle([ox - 4, oy + H - 6, ox + W + 4, oy + H], fill=(170, 164, 150))
        d.line([(ox - 4, oy + H - 6), (ox + W + 4, oy + H - 6)], fill=(200, 196, 184))

def choga(big, tx, ty, w=3, h=2, wall=(214, 196, 160), seed=0, snow=False, lit=False):
    X, Y, W, H = tx * TS, ty * TS, w * TS, h * TS
    rnd = random.Random(seed + tx * 7)
    soft_shadow(big, [X + 6, Y + H - 6, X + W + 8, Y + H + 6], 90, 5)
    with Prop(big, X - 12, Y - 26, W + 24, H + 26, 0.5) as d:
        ox, oy = 12, 26
        rc = (196, 170, 110) if not snow else (236, 238, 242)
        d.chord([ox - 10, oy, ox + W + 10, oy + 70], 180, 360, fill=rc)
        d.rectangle([ox - 10, oy + 34, ox + W + 10, oy + 40], fill=sh(rc, 0.86))
        if not snow:
            for _ in range(40):
                xx = ox + rnd.randint(-6, W + 6); yy = oy + rnd.randint(8, 34)
                d.line([(xx, yy), (xx + 2, yy + 6)], fill=sh(rc, 0.8))
            for k in range(4): d.arc([ox - 6, oy + 4 + k * 8, ox + W + 6, oy + 66 + k * 8], 200, 340, fill=(140, 110, 70))
        wy = oy + 38
        d.rectangle([ox, wy, ox + W, oy + H - 4], fill=wall)
        for k in range(w * 3):
            sx, sy = ox + rnd.randint(2, W - 6), wy + rnd.randint(2, max(3, H - 46))
            d.rectangle([sx, sy, sx + 4, sy + 3], fill=sh(wall, 0.88))
        d.rectangle([ox + W / 2 - 10, wy + 6, ox + W / 2 + 10, oy + H - 4], fill=(110, 80, 50))
        d.rectangle([ox + W / 2 - 8, wy + 8, ox + W / 2 + 8, oy + H - 6], fill=(250, 210, 120) if lit else (226, 216, 190))
        for yy in range(int(wy) + 11, oy + H - 6, 4): d.line([(ox + W / 2 - 8, yy), (ox + W / 2 + 8, yy)], fill=(150, 120, 80))
        d.line([(ox + W / 2, wy + 8), (ox + W / 2, oy + H - 6)], fill=(150, 120, 80))
        d.rectangle([ox - 4, oy + H - 4, ox + W + 4, oy + H], fill=(150, 140, 120))

# ------------------------------------------------------------------ 거리 소품
def pole(big, x, y, h=150, lamp=False):
    """전봇대 (x, y = 밑동)"""
    soft_shadow(big, [x - 4, y - 3, x + 18, y + 4], 70, 3)
    with Prop(big, x - 22, y - h - 4, 44, h + 6, 0.5) as d:
        cx = 22
        d.rectangle([cx - 3, 6, cx + 3, h + 4], fill=(110, 86, 62)); d.line([(cx - 2, 6), (cx - 2, h + 4)], fill=(140, 110, 80))
        for yy in (14, 26):
            d.rectangle([cx - 18, yy, cx + 18, yy + 3], fill=(90, 70, 50))
            for xx in (cx - 15, cx - 6, cx + 6, cx + 15): d.rectangle([xx - 1, yy - 4, xx + 1, yy], fill=(230, 230, 220))
        if lamp:
            d.line([(cx, 40), (cx + 12, 44)], fill=(60, 60, 60), width=2); d.chord([cx + 6, 42, cx + 20, 52], 180, 360, fill=(60, 70, 60))
    return (x - 15, y - h + 10), (x + 15, y - h + 10)

def wires(big, pts, col=(40, 40, 40, 200)):
    lay = Image.new('RGBA', big.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    for (a, b) in zip(pts, pts[1:]):
        mx, my = (a[0] + b[0]) / 2, max(a[1], b[1]) + 14
        seg = [(a[0] + (b[0] - a[0]) * t / 12, (1 - t / 12) ** 2 * a[1] + 2 * (1 - t / 12) * (t / 12) * my + (t / 12) ** 2 * b[1]) for t in range(13)]
        d.line(seg, fill=col, width=1)
        d.line([(x, y + 6) for x, y in seg], fill=col, width=1)
    big.alpha_composite(lay)

def tram(big, x, y, col=(196, 150, 70), num='12', w=150, broken=False):
    """전차 옆모습 (x, y = 왼쪽 아래 바퀴 선)"""
    soft_shadow(big, [x + 4, y - 6, x + w + 4, y + 6], 90, 4)
    with Prop(big, x - 4, y - 92, w + 8, 96, 0.5) as d:
        ox, oy = 4, 92
        d.line([(ox + w / 2, 4), (ox + w / 2 + 20, 0)], fill=(40, 40, 40), width=2)               # 전차 막대
        d.rectangle([ox + w / 2 - 20, 12, ox + w / 2 + 20, 16], fill=(60, 60, 60))
        d.rounded_rectangle([ox, 16, ox + w, oy - 10], 10, fill=col)
        d.rectangle([ox, oy - 34, ox + w, oy - 10], fill=sh(col, 0.85))
        d.rectangle([ox + 2, 16, ox + w - 2, 22], fill=(230, 222, 200))
        for k in range(7):
            wx = ox + 10 + k * (w - 20) / 7
            d.rectangle([wx, 26, wx + (w - 20) / 7 - 5, oy - 40], fill=(70, 86, 96) if not broken or k % 3 else (30, 30, 30))
            d.line([(wx + 2, 28), (wx + 2, oy - 44)], fill=(130, 150, 160))
        d.rectangle([ox + w / 2 - 9, 26, ox + w / 2 + 9, oy - 12], fill=sh(col, 0.6))
        d.text((ox + 18, oy - 22), num, font=F(11), fill=(250, 240, 200), anchor='mm')
        for wx in (ox + 22, ox + 44, ox + w - 44, ox + w - 22):
            d.ellipse([wx - 8, oy - 16, wx + 8, oy], fill=(40, 38, 36)); d.ellipse([wx - 3, oy - 11, wx + 3, oy - 5], fill=(110, 106, 100))

def tracks(big, y, x0, x1):
    d = ImageDraw.Draw(big)
    for yy in (y, y + 22):
        d.rectangle([x0, yy, x1, yy + 3], fill=(120, 116, 110)); d.line([(x0, yy), (x1, yy)], fill=(190, 186, 180))
    for xx in range(int(x0), int(x1), 14): d.rectangle([xx, y - 2, xx + 6, y + 27], fill=(90, 84, 76, 120))

def poster_board(big, x, y, w=96, h=60, kind='mix', seed=1, titles=None):
    """벽보판: kind mix / rally_r(신탁 통치 반대) / rally_l(3상 결정 지지) / election / mourning"""
    rnd = random.Random(seed)
    with Prop(big, x, y, w, h + 14, 0.5) as d:
        d.rectangle([0, 0, w - 1, h], fill=(120, 90, 60)); d.rectangle([3, 3, w - 4, h - 3], fill=(150, 120, 86))
        d.rectangle([6, h, 9, h + 13], fill=(100, 76, 50)); d.rectangle([w - 10, h, w - 7, h + 13], fill=(100, 76, 50))
        n = max(2, w // 26)
        for k in range(n):
            px_ = 6 + k * (w - 12) / n + rnd.randint(-2, 2); pw = (w - 12) / n - 4
            py = 6 + rnd.randint(0, 6); ph = h - 14 - rnd.randint(0, 8)
            pc = rnd.choice([(240, 232, 206), (232, 238, 242), (244, 226, 214), (226, 236, 214)])
            d.rectangle([px_, py, px_ + pw, py + ph], fill=pc)
            t = (titles[k % len(titles)] if titles else None)
            if t:
                for i, ch in enumerate(t[:6]):
                    d.text((px_ + pw / 2, py + 8 + i * 12), ch, font=F(10, 'serif'), fill=(150, 30, 30) if k % 2 == 0 else (30, 40, 90), anchor='mm')
            else:
                for yy in range(int(py) + 5, int(py + ph) - 3, 4): d.line([(px_ + 3, yy), (px_ + pw - 3, yy)], fill=(90, 80, 70))

def banner(big, x0, x1, y, text, col=(244, 240, 228), tcol=(30, 30, 40), size=16, poles=True, h=26):
    with Prop(big, x0 - 4, y - 6, x1 - x0 + 8, h + 60, 0.5) as d:
        if poles:
            d.rectangle([0, 0, 4, h + 56], fill=(110, 84, 60)); d.rectangle([x1 - x0 + 2, 0, x1 - x0 + 6, h + 56], fill=(110, 84, 60))
        d.rectangle([5, 6, x1 - x0 + 2, 6 + h], fill=col)
        d.line([(5, 6), (x1 - x0 + 2, 6)], fill=sh(col, 0.8))
        tw = d.textlength(text, font=F(size, 'serif'))
        fs = size if tw < (x1 - x0 - 10) else max(9, int(size * (x1 - x0 - 10) / tw))
        d.text(((x1 - x0) / 2 + 4, 6 + h / 2), text, font=F(fs, 'serif'), fill=tcol, anchor='mm')

def flagpole(big, x, y, h=170):
    soft_shadow(big, [x - 3, y - 2, x + 30, y + 5], 70, 3)
    with Prop(big, x - 14, y - h - 8, 28, h + 12, 0.5) as d:
        d.rectangle([12, 6, 15, h + 8], fill=(200, 200, 196)); d.line([(12, 6), (12, h + 8)], fill=(240, 240, 236))
        d.ellipse([9, 0, 18, 8], fill=(220, 190, 90))
        d.rectangle([4, h + 2, 23, h + 10], fill=(150, 146, 136))

# ------------------------------------------------------------------ 큰 건물
def prison_wall(big, x0, x1, y_bottom, gate_cx, h=118, tower_x=None):
    """서대문 형무소: 붉은 벽돌 담 + 가운데 문 + 망루"""
    with Prop(big, x0, y_bottom - h - 70, x1 - x0, h + 74, 0.5) as d:
        oy = 70
        brick = (150, 70, 52)
        d.rectangle([0, oy, x1 - x0, oy + h], fill=brick)
        for yy in range(oy, oy + h, 7):
            d.line([(0, yy), (x1 - x0, yy)], fill=sh(brick, 0.72))
            off = (yy // 7) % 2 * 7
            for xx in range(off, x1 - x0, 14): d.line([(xx, yy), (xx, yy + 7)], fill=sh(brick, 0.72))
        d.rectangle([0, oy - 6, x1 - x0, oy + 2], fill=(110, 100, 96))
        gx = gate_cx - x0
        # 정문
        d.rectangle([gx - 64, oy - 30, gx + 64, oy + h], fill=sh(brick, 1.08))
        for yy in range(oy - 30, oy + h, 7): d.line([(gx - 64, yy), (gx + 64, yy)], fill=sh(brick, 0.78))
        d.polygon([(gx - 70, oy - 30), (gx + 70, oy - 30), (gx + 60, oy - 46), (gx - 60, oy - 46)], fill=(100, 96, 96))
        d.rectangle([gx - 40, oy + 10, gx + 40, oy + h], fill=(30, 26, 26))
        d.chord([gx - 40, oy - 10, gx + 40, oy + 30], 180, 360, fill=(30, 26, 26))
        for xx in range(int(gx - 36), int(gx + 38), 8): d.line([(xx, oy + 4), (xx, oy + h)], fill=(70, 66, 62))   # 열린 문 안 창살
        # 망루
        if tower_x is not None:
            tx_ = tower_x - x0
            d.rectangle([tx_ - 18, oy - 50, tx_ + 18, oy + h], fill=sh(brick, 0.94))
            d.rectangle([tx_ - 24, oy - 64, tx_ + 24, oy - 46], fill=(220, 214, 200))
            d.polygon([(tx_ - 28, oy - 64), (tx_ + 28, oy - 64), (tx_, oy - 70 - 10)], fill=(90, 90, 96))
            for k in range(3): d.rectangle([tx_ - 18 + k * 13, oy - 60, tx_ - 10 + k * 13, oy - 50], fill=(60, 66, 76))

def capitol(big, x0, x1, y_bottom, cx, h=150, color=(196, 192, 182), banner_text=None):
    """조선 총독부 건물(광복 뒤 중앙청): 넓은 화강암 건물 + 가운데 돔"""
    W = x1 - x0
    with Prop(big, x0, y_bottom - h - 90, W, h + 94, 0.5) as d:
        oy = 90
        stone = color
        d.rectangle([0, oy + 30, W, oy + h], fill=stone)
        for yy in range(oy + 34, oy + h, 8): d.line([(0, yy), (W, yy)], fill=sh(stone, 0.92))
        # 층마다 창
        for f in range(3):
            yy = oy + 40 + f * 34
            for xx in range(10, W - 10, 18):
                if abs(xx - (cx - x0)) < 70: continue
                d.rectangle([xx, yy, xx + 9, yy + 20], fill=(64, 74, 84)); d.rectangle([xx - 1, yy - 2, xx + 10, yy], fill=sh(stone, 1.1))
        # 가운데 튀어나온 부분 + 돌기둥
        gx = cx - x0
        d.rectangle([gx - 86, oy + 4, gx + 86, oy + h], fill=sh(stone, 1.04))
        d.rectangle([gx - 92, oy, gx + 92, oy + 10], fill=sh(stone, 1.12))
        for k in range(8):
            xx = gx - 70 + k * 20
            d.rectangle([xx - 4, oy + 20, xx + 4, oy + h - 14], fill=sh(stone, 1.12)); d.line([(xx + 3, oy + 20), (xx + 3, oy + h - 14)], fill=sh(stone, 0.86))
        d.rectangle([gx - 30, oy + h - 40, gx + 30, oy + h], fill=(50, 50, 56))
        d.rectangle([gx - 86, oy + h - 14, gx + 86, oy + h], fill=sh(stone, 0.86))
        # 돔
        d.rectangle([gx - 40, oy - 40, gx + 40, oy + 2], fill=sh(stone, 1.06))
        for k in range(6): d.rectangle([gx - 34 + k * 13, oy - 34, gx - 28 + k * 13, oy - 6], fill=(70, 80, 90))
        d.chord([gx - 42, oy - 92, gx + 42, oy - 20], 180, 360, fill=(110, 126, 120))
        for k in range(-3, 4): d.arc([gx - 40 + abs(k) * 4, oy - 92, gx + 40 - abs(k) * 4, oy - 20], 180, 360, fill=(90, 104, 100))
        d.line([(gx, oy - 92), (gx, oy - 56)], fill=(90, 104, 100))
        d.rectangle([gx - 6, oy - 100, gx + 6, oy - 88], fill=(110, 126, 120))
        d.rectangle([0, oy + 26, W, oy + 32], fill=sh(stone, 1.1))
        if banner_text:
            d.rectangle([gx - 84, oy + 34, gx + 84, oy + 52], fill=(244, 240, 228))
            d.text((gx, oy + 43), banner_text, font=F(12, 'serif'), fill=(150, 30, 30), anchor='mm')

def station(big, x0, x1, y_bottom, cx, h=130):
    """서울역(경성역): 붉은 벽돌 + 화강암 띠 + 가운데 초록 돔"""
    W = x1 - x0
    brick, stone = (164, 82, 60), (220, 210, 190)
    with Prop(big, x0, y_bottom - h - 80, W, h + 84, 0.5) as d:
        oy = 80
        d.rectangle([0, oy + 20, W, oy + h], fill=brick)
        for yy in range(oy + 24, oy + h, 6): d.line([(0, yy), (W, yy)], fill=sh(brick, 0.86))
        for yy in (oy + 20, oy + 60, oy + h - 20): d.rectangle([0, yy, W, yy + 5], fill=stone)
        for xx in range(8, W - 8, 22):
            if abs(xx - (cx - x0)) < 64: continue
            d.rectangle([xx, oy + 30, xx + 10, oy + 54], fill=(70, 84, 90)); d.chord([xx, oy + 26, xx + 10, oy + 36], 180, 360, fill=(70, 84, 90))
            d.rectangle([xx, oy + 70, xx + 10, oy + h - 26], fill=(70, 84, 90))
        gx = cx - x0
        d.rectangle([gx - 60, oy + 4, gx + 60, oy + h], fill=sh(brick, 1.06))
        d.rectangle([gx - 60, oy + 4, gx + 60, oy + 10], fill=stone)
        for k in range(3):
            ax = gx - 40 + k * 40
            d.rectangle([ax - 14, oy + h - 46, ax + 14, oy + h], fill=(50, 46, 44)); d.chord([ax - 14, oy + h - 60, ax + 14, oy + h - 32], 180, 360, fill=(50, 46, 44))
        d.rectangle([gx - 30, oy + 22, gx + 30, oy + 46], fill=stone)
        d.ellipse([gx - 10, oy + 24, gx + 10, oy + 44], fill=(250, 250, 240), outline=(60, 60, 60))
        d.line([(gx, oy + 34), (gx, oy + 27)], fill=(30, 30, 30)); d.line([(gx, oy + 34), (gx + 5, oy + 36)], fill=(30, 30, 30))
        dome = (96, 140, 120)
        d.rectangle([gx - 34, oy - 12, gx + 34, oy + 6], fill=stone)
        d.chord([gx - 38, oy - 66, gx + 38, oy + 4], 180, 360, fill=dome)
        for k in range(-3, 4): d.arc([gx - 36 + abs(k) * 5, oy - 66, gx + 36 - abs(k) * 5, oy + 4], 180, 360, fill=sh(dome, 0.8))
        d.rectangle([gx - 5, oy - 76, gx + 5, oy - 62], fill=dome); d.line([(gx, oy - 80), (gx, oy - 76)], fill=(60, 60, 60))
        for sx in (12, W - 40):
            d.chord([sx, oy - 14, sx + 28, oy + 24], 180, 360, fill=dome)
        d.text((gx, oy + 14), '서울역', font=F(11, 'serif'), fill=(60, 40, 30), anchor='mm')

def seokjojeon(big, x0, x1, y_bottom, cx, h=150):
    """덕수궁 석조전: 돌기둥 늘어선 서양식 건물 + 세모 지붕"""
    W = x1 - x0
    stone = (222, 216, 200)
    with Prop(big, x0, y_bottom - h - 50, W, h + 54, 0.5) as d:
        oy = 50
        d.rectangle([0, oy + 20, W, oy + h - 20], fill=sh(stone, 0.95))
        gx = cx - x0
        # 세모 지붕
        d.polygon([(gx - 120, oy + 22), (gx + 120, oy + 22), (gx, oy - 26)], fill=sh(stone, 1.06))
        d.polygon([(gx - 104, oy + 18), (gx + 104, oy + 18), (gx, oy - 16)], fill=sh(stone, 0.9))
        d.rectangle([0, oy + 18, W, oy + 30], fill=sh(stone, 1.08))
        # 돌기둥
        n = 12
        for k in range(n):
            xx = 14 + k * (W - 28) / (n - 1)
            d.rectangle([xx - 6, oy + 30, xx + 6, oy + h - 26], fill=sh(stone, 1.1))
            d.line([(xx + 4, oy + 30), (xx + 4, oy + h - 26)], fill=sh(stone, 0.82))
            d.rectangle([xx - 9, oy + 28, xx + 9, oy + 34], fill=sh(stone, 1.15))
            d.ellipse([xx - 10, oy + 28, xx - 4, oy + 34], fill=sh(stone, 0.9)); d.ellipse([xx + 4, oy + 28, xx + 10, oy + 34], fill=sh(stone, 0.9))
        for k in range(n - 1):
            xx = 14 + (k + 0.5) * (W - 28) / (n - 1)
            d.rectangle([xx - 7, oy + 52, xx + 7, oy + h - 40], fill=(70, 80, 88))
        # 계단 기단
        for k in range(5):
            d.rectangle([gx - 90 - k * 6, oy + h - 26 + k * 5, gx + 90 + k * 6, oy + h - 21 + k * 5], fill=sh(stone, 1.02 - k * 0.03))
        d.rectangle([0, oy + h - 26, W, oy + h], fill=sh(stone, 0.86))

def c47(big, x, y, s=1.0):
    """C-47 수송기 (위에서 비스듬히 본 모습, x,y = 동체 가운데)"""
    w, h = int(300 * s), int(150 * s)
    soft_shadow(big, [x - w / 2 + 20, y + 20 * s, x + w / 2 - 10, y + 52 * s], 80, 8, True)
    with Prop(big, x - w / 2, y - h / 2, w, h, 0.5) as d:
        cx, cy = w / 2, h / 2
        body = (170, 172, 160)
        d.polygon([(cx - 140 * s, cy + 4 * s), (cx + 10 * s, cy - 6 * s), (cx + 10 * s, cy + 6 * s)], fill=sh(body, 0.9))   # 꼬리 쪽 동체
        d.rounded_rectangle([cx - 30 * s, cy - 13 * s, cx + 130 * s, cy + 13 * s], int(12 * s), fill=body)
        d.polygon([(cx - 135 * s, cy - 2 * s), (cx - 118 * s, cy - 2 * s), (cx - 128 * s, cy - 34 * s)], fill=sh(body, 1.05))   # 꼬리 날개
        d.rectangle([cx - 140 * s, cy - 2 * s, cx - 104 * s, cy + 4 * s], fill=sh(body, 0.85))
        d.polygon([(cx + 20 * s, cy - 2 * s), (cx + 60 * s, cy - 2 * s), (cx + 70 * s, cy - 72 * s), (cx + 52 * s, cy - 72 * s)], fill=sh(body, 1.08))   # 위 날개
        d.polygon([(cx + 20 * s, cy + 4 * s), (cx + 60 * s, cy + 4 * s), (cx + 74 * s, cy + 70 * s), (cx + 54 * s, cy + 70 * s)], fill=sh(body, 0.94))
        for ey in (-36, 38):
            d.rounded_rectangle([cx + 40 * s, cy + (ey - 7) * s, cx + 80 * s, cy + (ey + 7) * s], int(6 * s), fill=sh(body, 0.8))
            d.ellipse([cx + 78 * s, cy + (ey - 14) * s, cx + 84 * s, cy + (ey + 14) * s], fill=(70, 70, 70))
        for k in range(6): d.rectangle([cx - 10 * s + k * 16 * s, cy - 9 * s, cx - 4 * s + k * 16 * s, cy - 4 * s], fill=(60, 74, 84))
        d.polygon([(cx + 112 * s, cy - 10 * s), (cx + 126 * s, cy - 6 * s), (cx + 126 * s, cy + 2 * s), (cx + 112 * s, cy)], fill=(60, 74, 84))
        d.rectangle([cx - 24 * s, cy - 2 * s, cx - 14 * s, cy + 12 * s], fill=sh(body, 0.6))     # 문
        d.ellipse([cx - 100 * s, cy - 8 * s, cx - 92 * s, cy], fill=(240, 240, 240)); d.text((cx - 96 * s, cy - 4 * s), '★', font=F(int(8 * s)), fill=(40, 50, 100), anchor='mm')

def tent(big, x, y, w=120, h=70, col=(200, 190, 160), sign=None, open_=True):
    """군용 천막 (x,y = 아래 가운데)"""
    soft_shadow(big, [x - w / 2 + 4, y - 6, x + w / 2 + 8, y + 6], 80, 4)
    with Prop(big, x - w / 2 - 4, y - h - 4, w + 8, h + 8, 0.5) as d:
        ox, oy = 4, 4
        d.polygon([(ox, oy + h), (ox + 10, oy + 20), (ox + w / 2, oy), (ox + w - 10, oy + 20), (ox + w, oy + h)], fill=col)
        d.polygon([(ox + w / 2, oy), (ox + w - 10, oy + 20), (ox + w, oy + h), (ox + w / 2, oy + h)], fill=sh(col, 0.86))
        if open_:
            d.polygon([(ox + w / 2 - 18, oy + h), (ox + w / 2, oy + 26), (ox + w / 2 + 18, oy + h)], fill=(60, 50, 40))
        for k in range(4): d.line([(ox + 10 + k * (w - 20) / 3, oy + 20 + (8 if k in (0, 3) else 0)), (ox + 10 + k * (w - 20) / 3, oy + h)], fill=sh(col, 0.75))
        if sign:
            d.rectangle([ox + w / 2 - 34, oy + 30, ox + w / 2 + 34, oy + 44], fill=(244, 240, 228))
            d.text((ox + w / 2, oy + 37), sign, font=F(10), fill=(40, 40, 50), anchor='mm')

def table(big, x, y, w=96, h=40, col=(150, 106, 66), cloth=None, things=()):
    soft_shadow(big, [x + 4, y + h - 4, x + w + 6, y + h + 6], 70, 4)
    with Prop(big, x, y, w, h + 14, 0.5) as d:
        top = cloth or col
        d.rectangle([0, 0, w - 1, h - 10], fill=top); d.rectangle([0, h - 12, w - 1, h - 4], fill=sh(top, 0.8))
        if cloth: d.rectangle([0, h - 4, w - 1, h + 10], fill=sh(cloth, 0.86))
        else:
            d.rectangle([3, h - 4, 7, h + 12], fill=sh(col, 0.7)); d.rectangle([w - 8, h - 4, w - 4, h + 12], fill=sh(col, 0.7))
        for (kind, tx_, ty_) in things:
            if kind == 'paper': d.rectangle([tx_, ty_, tx_ + 14, ty_ + 10], fill=(244, 240, 226)); d.line([(tx_ + 2, ty_ + 3), (tx_ + 11, ty_ + 3)], fill=(90, 90, 90))
            if kind == 'book': d.rectangle([tx_, ty_, tx_ + 12, ty_ + 9], fill=(70, 60, 110))
            if kind == 'ink': d.rectangle([tx_, ty_, tx_ + 5, ty_ + 6], fill=(30, 30, 40))
            if kind == 'mic': d.line([(tx_, ty_ + 10), (tx_, ty_)], fill=(60, 60, 60), width=2); d.ellipse([tx_ - 4, ty_ - 6, tx_ + 4, ty_ + 2], fill=(90, 90, 96))
            if kind == 'flag_un': fl = un_flag(16, 11); d.line([(tx_, ty_ + 14), (tx_, ty_ - 2)], fill=(200, 200, 200)); d._image.paste(fl, (int(tx_) + 1, int(ty_) - 2), fl)
            if kind == 'flag_red':
                d.line([(tx_, ty_ + 14), (tx_, ty_ - 2)], fill=(200, 200, 200)); d.rectangle([tx_ + 1, ty_ - 2, tx_ + 16, ty_ + 8], fill=(190, 40, 40))
                d.rectangle([tx_ + 1, ty_ - 2, tx_ + 16, ty_], fill=(40, 70, 160)); d.rectangle([tx_ + 1, ty_ + 6, tx_ + 16, ty_ + 8], fill=(40, 70, 160))
            if kind == 'flag_cn':
                d.line([(tx_, ty_ + 14), (tx_, ty_ - 2)], fill=(200, 200, 200)); d.rectangle([tx_ + 1, ty_ - 2, tx_ + 16, ty_ + 8], fill=(214, 40, 40))
                d.rectangle([tx_ + 3, ty_, tx_ + 5, ty_ + 2], fill=(250, 220, 60))
            if kind == 'box': d.rectangle([tx_, ty_, tx_ + 22, ty_ + 18], fill=(170, 130, 80)); d.rectangle([tx_ + 6, ty_ - 1, tx_ + 16, ty_ + 1], fill=(40, 40, 40))

def booth(big, x, y, w=60, h=80, curtain=(210, 70, 70)):
    soft_shadow(big, [x + 4, y + h - 6, x + w + 6, y + h + 6], 70, 4)
    with Prop(big, x, y, w, h + 4, 0.5) as d:
        d.rectangle([0, 0, w - 1, h], fill=(170, 130, 86)); d.rectangle([3, 3, w - 4, h - 2], fill=(210, 190, 150))
        d.rectangle([6, 8, w - 7, h - 4], fill=curtain)
        for xx in range(8, w - 8, 5): d.line([(xx, 8), (xx, h - 4)], fill=sh(curtain, 0.78))
        d.rectangle([0, 0, w - 1, 6], fill=(130, 96, 60))
        d.text((w / 2, 3), '기표소', font=F(8), fill=(250, 240, 210), anchor='mm')

def ballot_box(big, x, y):
    soft_shadow(big, [x + 2, y + 28, x + 40, y + 36], 70, 3)
    with Prop(big, x, y, 40, 36, 0.5) as d:
        d.rectangle([2, 6, 37, 32], fill=(150, 110, 70)); d.rectangle([0, 2, 39, 8], fill=(120, 86, 54))
        d.rectangle([12, 4, 27, 6], fill=(20, 20, 20)); d.rectangle([10, 14, 30, 24], fill=(244, 240, 226))
        d.text((20, 19), '투표함', font=F(7), fill=(40, 40, 40), anchor='mm')

def shack(big, tx, ty, w=2, h=2, seed=0, col=(140, 110, 80)):
    """판잣집: 널빤지 벽 + 함석·루핑 지붕"""
    rnd = random.Random(seed + tx * 11 + ty)
    X, Y, W, H = tx * TS, ty * TS, w * TS, h * TS
    soft_shadow(big, [X + 4, Y + H - 6, X + W + 8, Y + H + 6], 80, 4)
    with Prop(big, X - 6, Y - 12, W + 12, H + 12, 0.5) as d:
        ox, oy = 6, 12
        rc = rnd.choice([(110, 110, 104), (90, 80, 70), (120, 100, 80)])
        d.polygon([(ox - 6, oy + 18), (ox + W + 6, oy + 14), (ox + W, oy), (ox, oy + 3)], fill=rc)
        for xx in range(ox, ox + W, 6): d.line([(xx, oy + 2), (xx - 2, oy + 17)], fill=sh(rc, 0.8))
        d.rectangle([ox, oy + 16, ox + W, oy + H - 2], fill=col)
        for xx in range(ox, ox + W, 7):
            c = sh(col, 0.85 + rnd.random() * 0.3)
            d.rectangle([xx, oy + 16, xx + 6, oy + H - 2], fill=c); d.line([(xx, oy + 16), (xx, oy + H - 2)], fill=sh(col, 0.6))
        for _ in range(2):
            px_, py_ = ox + rnd.randint(4, W - 16), oy + rnd.randint(20, H - 20)
            d.rectangle([px_, py_, px_ + 12, py_ + 9], fill=rnd.choice([(200, 190, 160), (160, 170, 180), (180, 140, 110)]))
        dx = ox + rnd.randint(8, W - 22)
        d.rectangle([dx, oy + H - 30, dx + 14, oy + H - 2], fill=(70, 54, 40))
        d.rectangle([ox + W - 18, oy + 22, ox + W - 6, oy + 32], fill=(80, 96, 104))

def stall(big, x, y, w=96, goods='fish', awn=(170, 150, 110)):
    soft_shadow(big, [x + 4, y + 30, x + w + 6, y + 42], 70, 4)
    with Prop(big, x, y - 26, w, 70, 0.5) as d:
        d.rectangle([2, 0, w - 3, 3], fill=(110, 84, 60))
        d.polygon([(0, 4), (w, 4), (w - 4, 20), (4, 20)], fill=awn)
        for xx in range(6, w - 6, 9): d.line([(xx, 4), (xx - 1, 20)], fill=sh(awn, 0.8))
        d.rectangle([4, 20, 6, 60], fill=(100, 76, 50)); d.rectangle([w - 7, 20, w - 5, 60], fill=(100, 76, 50))
        d.rectangle([2, 40, w - 3, 52], fill=(140, 104, 66)); d.rectangle([2, 52, w - 3, 58], fill=(110, 80, 50))
        rnd = random.Random(w + int(x))
        for k in range(int(w / 12)):
            gx = 6 + k * 11
            if goods == 'fish': d.ellipse([gx, 36, gx + 10, 41], fill=(150, 160, 170)); d.polygon([(gx + 10, 38), (gx + 13, 35), (gx + 13, 42)], fill=(130, 140, 150))
            elif goods == 'cloth': d.rectangle([gx, 30, gx + 9, 40], fill=rnd.choice([(190, 60, 60), (60, 90, 160), (230, 220, 190), (90, 140, 90)]))
            elif goods == 'pots': d.ellipse([gx, 30, gx + 10, 40], fill=rnd.choice([(150, 90, 50), (120, 70, 40)]))
            elif goods == 'cans': d.rectangle([gx + 1, 32, gx + 8, 40], fill=rnd.choice([(200, 200, 190), (190, 160, 60), (160, 60, 50)]))
            elif goods == 'veg': d.ellipse([gx, 33, gx + 9, 41], fill=rnd.choice([(110, 160, 70), (220, 150, 60), (200, 70, 60)]))

def ship(big, x0, x1, y_deck, h=150, col=(70, 74, 82), name=None, snow=False):
    """화물선 옆모습 (부두에 닿은 쪽이 아래)"""
    W = x1 - x0
    with Prop(big, x0, y_deck - h, W, h + 30, 0.5) as d:
        oy = h
        hull = col
        d.polygon([(0, oy - 60), (W, oy - 60), (W - 30, oy + 26), (30, oy + 26)], fill=hull)
        d.rectangle([20, oy - 64, W - 20, oy - 56], fill=(200, 196, 186))
        for xx in range(40, W - 40, 30): d.ellipse([xx, oy - 40, xx + 8, oy - 32], fill=(40, 44, 50))
        d.rectangle([30, oy + 14, W - 30, oy + 26], fill=(120, 40, 36))
        # 갑판 위 구조물
        sx = W * 0.58
        d.rectangle([sx - 80, oy - 120, sx + 60, oy - 64], fill=(226, 222, 212))
        for k in range(8): d.rectangle([sx - 74 + k * 17, oy - 112, sx - 64 + k * 17, oy - 102], fill=(60, 70, 80))
        d.rectangle([sx - 60, oy - 140, sx + 30, oy - 120], fill=(236, 232, 222))
        d.rectangle([sx - 20, oy - h + 6, sx + 10, oy - 140], fill=(40, 40, 44)); d.rectangle([sx - 20, oy - h + 14, sx + 10, oy - h + 22], fill=(200, 60, 50))
        for mx in (W * 0.2, W * 0.86):
            d.line([(mx, oy - 64), (mx, oy - h + 10)], fill=(90, 80, 70), width=4)
            d.line([(mx, oy - h + 30), (mx + 50, oy - 70)], fill=(90, 80, 70), width=2)
        if name: d.text((W * 0.2, oy - 20), name, font=F(12), fill=(230, 226, 214), anchor='mm')
        if snow:
            d.rectangle([20, oy - 66, W - 20, oy - 63], fill=(246, 248, 252)); d.rectangle([sx - 80, oy - 122, sx + 60, oy - 118], fill=(246, 248, 252))

def truss_bridge(big, x0, x1, y_top, y_bot, broken_at=None):
    """철교 (위아래로 놓인 다리: x0~x1 너비, y_top~y_bot 길이)"""
    W, H = x1 - x0, y_bot - y_top
    with Prop(big, x0 - 8, y_top, W + 16, H, 0.5) as d:
        deck = (120, 110, 100)
        d.rectangle([8, 0, W + 8, H], fill=deck)
        for yy in range(0, H, 8): d.line([(8, yy), (W + 8, yy)], fill=sh(deck, 0.85))
        for side in (0, W + 6):
            d.rectangle([side, 0, side + 10, H], fill=(70, 70, 76))
            for yy in range(0, H, 24): d.line([(side, yy), (side + 10, yy + 24)], fill=(110, 110, 116), width=2)
        if broken_at is not None:
            by = broken_at - y_top
            d.rectangle([0, by - 16, W + 16, by + 16], fill=(0, 0, 0, 0))
            for k in range(8):
                xx = k * (W + 16) / 8
                d.polygon([(xx, by - 16), (xx + 6, by - 6 - (k % 3) * 4), (xx + 12, by - 16)], fill=deck)
                d.polygon([(xx, by + 16), (xx + 6, by + 6 + (k % 2) * 4), (xx + 12, by + 16)], fill=deck)

def sign38(big, x, y, text='38 선', sub='北緯 38度線'):
    """38선 표지판 (x,y = 밑동)"""
    soft_shadow(big, [x - 4, y - 3, x + 30, y + 5], 70, 3)
    with Prop(big, x - 40, y - 96, 80, 98, 0.5) as d:
        d.rectangle([36, 40, 43, 96], fill=(120, 100, 76)); d.rectangle([33, 92, 46, 97], fill=(90, 80, 70))
        d.rectangle([2, 4, 77, 44], fill=(240, 236, 222)); d.rectangle([2, 4, 77, 44], outline=(60, 50, 40))
        d.text((40, 18), text, font=F(15, 'serif'), fill=(30, 30, 30), anchor='mm')
        d.text((40, 34), sub, font=F(9, 'serif'), fill=(60, 60, 60), anchor='mm')

def barrier(big, x0, x1, y, up=False):
    with Prop(big, x0 - 4, y - 50, x1 - x0 + 8, 60, 0.5) as d:
        d.rectangle([0, 20, 10, 56], fill=(120, 110, 100))
        if up:
            d.line([(6, 24), (30, -20 + 50)], fill=(230, 230, 220), width=5)
        else:
            for k in range(int((x1 - x0) / 12)):
                d.rectangle([6 + k * 12, 24, 18 + k * 12, 30], fill=(220, 50, 50) if k % 2 == 0 else (240, 240, 236))

def kbs(big, x0, x1, y_bottom, cx, h=150):
    W = x1 - x0
    with Prop(big, x0, y_bottom - h - 20, W, h + 24, 0.5) as d:
        oy = 20
        c = (210, 206, 196)
        d.rectangle([0, oy, W, oy + h], fill=c)
        for f in range(6):
            for k in range(int(W / 16)):
                d.rectangle([4 + k * 16, oy + 8 + f * 20, 14 + k * 16, oy + 20 + f * 20], fill=(80, 100, 120))
        d.rectangle([cx - x0 - 60, oy - 14, cx - x0 + 60, oy + 4], fill=(40, 70, 140))
        d.text((cx - x0, oy - 5), 'KBS 한국방송공사', font=F(12), fill=(250, 250, 250), anchor='mm')
        d.rectangle([cx - x0 - 30, oy + h - 36, cx - x0 + 30, oy + h], fill=(50, 56, 64))

def paper_wall(big, x0, x1, y0, y1, seed=3, names=None):
    """이산가족 찾기 벽보: 손으로 쓴 종이가 빈틈없이"""
    rnd = random.Random(seed)
    with Prop(big, x0, y0, x1 - x0, y1 - y0, 0.4) as d:
        d.rectangle([0, 0, x1 - x0, y1 - y0], fill=(150, 140, 126))
        y = 2
        while y < y1 - y0 - 10:
            x = 2 + rnd.randint(-6, 0)
            while x < x1 - x0 - 6:
                pw, ph = rnd.randint(14, 24), rnd.randint(16, 24)
                c = rnd.choice([(248, 246, 238), (244, 240, 226), (250, 250, 246), (236, 240, 244), (246, 236, 220)])
                d.rectangle([x, y, x + pw, y + ph], fill=c)
                for yy in range(y + 4, y + ph - 2, 4): d.line([(x + 3, yy), (x + pw - 3, yy)], fill=(40, 40, 50) if rnd.random() < 0.8 else (180, 40, 40))
                x += pw + rnd.randint(0, 2)
            y += 18 + rnd.randint(0, 4)

# ------------------------------------------------------------------ 사진관 안
def backdrop(big, x, y, w=150, h=110, kind='garden'):
    """촬영 배경막 (그림이 그려진 천)"""
    with Prop(big, x, y, w, h + 6, 0.5) as d:
        d.rectangle([0, 0, w - 1, 4], fill=(90, 70, 50))
        if kind == 'garden':
            for yy in range(6, h):
                t = (yy - 6) / h
                d.line([(2, yy), (w - 3, yy)], fill=mix((170, 186, 196), (206, 196, 170), t))
            d.ellipse([w * 0.1, h * 0.35, w * 0.5, h * 0.75], fill=(120, 140, 110)); d.ellipse([w * 0.45, h * 0.3, w * 0.9, h * 0.75], fill=(110, 132, 104))
            d.rectangle([w * 0.3, h * 0.55, w * 0.34, h * 0.9], fill=(130, 110, 90))
            d.polygon([(w * 0.55, h * 0.95), (w * 0.62, h * 0.55), (w * 0.69, h * 0.55), (w * 0.76, h * 0.95)], fill=(210, 204, 186))
            d.rectangle([w * 0.6, h * 0.45, w * 0.71, h * 0.55], fill=(200, 194, 176))
        else:
            d.rectangle([2, 6, w - 3, h], fill=(110, 104, 100))
            for xx in range(4, w - 3, 8): d.line([(xx, 6), (xx + 2, h)], fill=(96, 90, 86))
        d.rectangle([2, h - 6, w - 3, h], fill=sh((150, 140, 120), 0.8))

def tripod(big, x, y, s=1.0):
    """큰 나무 사진기 (삼각대 위, 주름 상자 + 검은 천). x,y = 다리 가운데 바닥"""
    soft_shadow(big, [x - 22 * s, y - 4, x + 26 * s, y + 6], 80, 4, True)
    with Prop(big, x - 34 * s, y - 92 * s, 68 * s, 94 * s, 0.5) as d:
        cx, by = 34 * s, 92 * s
        wood = (130, 90, 56)
        d.line([(cx, by - 46 * s), (cx - 24 * s, by)], fill=wood, width=int(3 * s)); d.line([(cx, by - 46 * s), (cx + 24 * s, by)], fill=wood, width=int(3 * s))
        d.line([(cx, by - 46 * s), (cx + 2 * s, by - 2)], fill=sh(wood, 0.8), width=int(3 * s))
        d.rectangle([cx - 20 * s, by - 74 * s, cx + 20 * s, by - 46 * s], fill=(150, 104, 64))
        d.rectangle([cx - 14 * s, by - 70 * s, cx + 14 * s, by - 50 * s], fill=(40, 34, 30))      # 주름 상자
        for k in range(4): d.line([(cx - 14 * s, by - 68 * s + k * 5 * s), (cx + 14 * s, by - 68 * s + k * 5 * s)], fill=(80, 70, 60))
        d.ellipse([cx - 7 * s, by - 66 * s, cx + 7 * s, by - 54 * s], fill=(70, 74, 80)); d.ellipse([cx - 4 * s, by - 63 * s, cx + 4 * s, by - 57 * s], fill=(150, 170, 190))
        d.polygon([(cx - 22 * s, by - 76 * s), (cx + 22 * s, by - 76 * s), (cx + 26 * s, by - 88 * s), (cx - 26 * s, by - 88 * s)], fill=(30, 30, 34))   # 검은 천
        d.rectangle([cx - 26 * s, by - 90 * s, cx + 26 * s, by - 86 * s], fill=(50, 50, 54))

def darkroom_door(big, x, y, w=48, h=86, lit=True):
    with Prop(big, x, y - 16, w, h + 16, 0.5) as d:
        d.rectangle([2, 16, w - 3, h + 14], fill=(70, 50, 40)); d.rectangle([6, 20, w - 7, h + 12], fill=(40, 30, 26))
        d.rectangle([w / 2 - 14, 30, w / 2 + 14, 42], fill=(240, 230, 210)); d.text((w / 2, 36), '암실', font=F(9), fill=(150, 30, 30), anchor='mm')
        d.ellipse([w / 2 - 6, 2, w / 2 + 6, 14], fill=(240, 60, 50) if lit else (110, 40, 40))
        d.ellipse([w - 14, 60, w - 10, 64], fill=(210, 180, 100))
    if lit: glow(big, x + w / 2, y - 8, 16, (255, 70, 50), 90)

def shelf(big, x, y, w=96, h=90, kind='cameras'):
    with Prop(big, x, y, w, h + 4, 0.5) as d:
        wood = (124, 86, 56)
        d.rectangle([0, 0, w - 1, h], fill=wood); d.rectangle([3, 3, w - 4, h - 3], fill=sh(wood, 0.7))
        rows = 3
        for r in range(rows):
            yy = 3 + (r + 1) * (h - 6) / rows
            d.rectangle([3, yy - 3, w - 4, yy], fill=sh(wood, 1.15))
            rnd = random.Random(r * 7 + w)
            xx = 6
            while xx < w - 14:
                if kind == 'cameras':
                    t = rnd.random()
                    if t < 0.4: d.rectangle([xx, yy - 14, xx + 14, yy - 4], fill=(40, 38, 40)); d.ellipse([xx + 4, yy - 13, xx + 10, yy - 7], fill=(100, 110, 120)); xx += 18
                    elif t < 0.7: d.rectangle([xx, yy - 12, xx + 9, yy - 3], fill=rnd.choice([(230, 190, 60), (220, 220, 210), (200, 70, 50)])); xx += 12
                    else: d.rectangle([xx, yy - 18, xx + 12, yy - 3], fill=(240, 236, 226)); d.rectangle([xx + 2, yy - 16, xx + 10, yy - 6], fill=(150, 140, 120)); xx += 15
                else:
                    d.rectangle([xx, yy - 16, xx + 5, yy - 3], fill=rnd.choice([(150, 50, 40), (60, 70, 120), (90, 110, 70), (180, 160, 110)])); xx += 6

def photo_wall(big, x, y, w=150, h=70, seed=5):
    rnd = random.Random(seed)
    with Prop(big, x, y, w, h, 0.4) as d:
        k = 0
        for r in range(2):
            for c in range(5):
                px_ = 4 + c * (w - 8) / 5 + rnd.randint(-2, 2); py_ = 4 + r * (h - 8) / 2 + rnd.randint(-2, 2)
                pw, ph = (w - 8) / 5 - 6, (h - 8) / 2 - 6
                d.rectangle([px_, py_, px_ + pw, py_ + ph], fill=(70, 50, 36))
                d.rectangle([px_ + 2, py_ + 2, px_ + pw - 2, py_ + ph - 2], fill=(214, 200, 170))
                # 인물 사진 흉내
                d.ellipse([px_ + pw / 2 - 4, py_ + 5, px_ + pw / 2 + 4, py_ + 13], fill=(120, 100, 80))
                d.rectangle([px_ + pw / 2 - 7, py_ + 13, px_ + pw / 2 + 7, py_ + ph - 2], fill=(110, 92, 74))
                k += 1

def counter(big, x, y, w=150, h=46, things=True, sign=None):
    """계산대: 위에 금전 등록기 · 신문 · 장부 (윗면 위로 올라온 물건도 잘리지 않게 16px 위부터 그림)"""
    soft_shadow(big, [x + 4, y + h - 4, x + w + 6, y + h + 6], 80, 4)
    T = 18
    with Prop(big, x, y - T, w, h + 4 + T, 0.5) as d:
        wood = (150, 100, 60)
        d.rectangle([0, T, w - 1, T + 12], fill=sh(wood, 1.25)); d.line([(0, T), (w - 1, T)], fill=sh(wood, 1.45), width=2)
        d.rectangle([0, T + 12, w - 1, T + h], fill=wood)
        for xx in range(6, w - 6, 24): d.rectangle([xx, T + 18, xx + 18, T + h - 6], fill=sh(wood, 0.84))
        if things:
            # 금전 등록기
            d.rectangle([10, T - 14, 40, T + 6], fill=(54, 54, 60)); d.rectangle([14, T - 11, 36, T - 4], fill=(200, 190, 150))
            d.polygon([(8, T + 6), (42, T + 6), (38, T - 1), (12, T - 1)], fill=(80, 80, 88))
            # 신문
            d.rectangle([w - 64, T - 2, w - 22, T + 9], fill=(244, 240, 226)); d.rectangle([w - 62, T, w - 40, T + 3], fill=(40, 36, 34))
            for yy in (T + 5, T + 7): d.line([(w - 60, yy), (w - 26, yy)], fill=(110, 104, 96))
            # 장부
            d.rectangle([w / 2 - 14, T + 1, w / 2 + 10, T + 9], fill=(120, 40, 40)); d.line([(w / 2 - 2, T + 1), (w / 2 - 2, T + 9)], fill=(240, 220, 180))
        if sign:
            d.rounded_rectangle([w / 2 - 34, T + 16, w / 2 + 34, T + 34], 4, fill=(60, 40, 26))
            d.text((w / 2, T + 25), sign, font=F(13), fill=(250, 232, 190), anchor='mm')

def wardrobe(big, x, y, w=72, h=96):
    soft_shadow(big, [x + 4, y + h - 4, x + w + 6, y + h + 6], 80, 4)
    with Prop(big, x, y, w, h + 4, 0.5) as d:
        wood = (110, 70, 44)
        d.rectangle([0, 0, w - 1, h], fill=wood)
        d.rectangle([4, 4, w / 2 - 2, h - 20], fill=sh(wood, 1.12)); d.rectangle([w / 2 + 1, 4, w - 5, h - 20], fill=sh(wood, 1.12))
        for (hx, hy) in ((w / 2 - 6, h / 2 - 10), (w / 2 + 4, h / 2 - 10)): d.ellipse([hx, hy, hx + 4, hy + 4], fill=(220, 190, 100))
        d.rectangle([4, h - 16, w - 5, h - 4], fill=sh(wood, 0.9))
        for (cx_, cy_) in ((12, 12), (w - 16, 12), (12, h - 30), (w - 16, h - 30)): d.rectangle([cx_, cy_, cx_ + 6, cy_ + 6], fill=(200, 170, 90))

def window_wall(big, x, y, w=60, h=50, night=False):
    with Prop(big, x, y, w, h, 0.5) as d:
        d.rectangle([0, 0, w - 1, h - 1], fill=(120, 90, 60))
        d.rectangle([4, 4, w - 5, h - 5], fill=(40, 50, 70) if night else (170, 200, 220))
        d.line([(w / 2, 4), (w / 2, h - 5)], fill=(120, 90, 60), width=2); d.line([(4, h / 2), (w - 5, h / 2)], fill=(120, 90, 60), width=2)

def crate(big, x, y, s=1.0, col=(176, 136, 90)):
    soft_shadow(big, [x + 2, y + 24 * s, x + 32 * s, y + 32 * s], 70, 3)
    with Prop(big, x, y, 34 * s, 32 * s, 0.5) as d:
        d.rectangle([0, 4 * s, 32 * s, 30 * s], fill=col); d.rectangle([0, 0, 32 * s, 6 * s], fill=sh(col, 1.15))
        d.line([(2, 6 * s), (30 * s, 28 * s)], fill=sh(col, 0.75)); d.line([(30 * s, 6 * s), (2, 28 * s)], fill=sh(col, 0.75))

def sandbags(big, x, y, w=96):
    with Prop(big, x, y, w, 30, 0.5) as d:
        for r in range(2):
            for k in range(int(w / 16)):
                xx = k * 16 + (8 if r else 0)
                if xx + 15 > w: continue
                d.rounded_rectangle([xx, 14 - r * 10, xx + 15, 26 - r * 10], 4, fill=(176, 160, 120))
                d.line([(xx + 3, 18 - r * 10), (xx + 12, 18 - r * 10)], fill=(150, 136, 100))

def boat_small(big, x, y, w=110):
    with Prop(big, x, y, w, 40, 0.5) as d:
        d.polygon([(0, 10), (w, 10), (w - 14, 34), (14, 34)], fill=(120, 86, 56)); d.rectangle([4, 8, w - 4, 12], fill=(150, 110, 70))
        for xx in range(20, w - 20, 22): d.line([(xx, 12), (xx, 30)], fill=(90, 64, 40))
