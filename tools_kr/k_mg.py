"""척화비 아래에서 · 지도 9장 (29 x 13칸, 가운데 7~21칸을 걷는다)
 01 역관 집 사랑방 (1882 밤)        02 경복궁 중건 공사장 (1867)        03 운종가 장터 (1867 · 1871 · 1882)
 04 강화도 정족산성 아래 (1866 밤)   05 강화도 광성보 (1871)              06 강화부 연무당 (1876)
 07 하도감 훈련장 · 궐 앞 (1881)     08 선혜청 도봉소 (1882)              09 제물포 항구 (1882)
 시대가 갈수록 근대 물건(석유통 · 남포등 · 일본 상점 · 증기선 · 서양식 총)이 조금씩 섞여 든다.
"""
from k_mapbase import *
import k_mapbase as MB
from k_m1 import side_walls

MAP_NAMES = ['01 역관 집 사랑방', '02 경복궁 중건 공사장', '03 운종가 장터', '04 강화도 정족산성', '05 강화도 광성보', '06 강화부 연무당',
             '07 하도감 훈련장', '08 선혜청 도봉소', '09 제물포 항구']
GIWA = (70, 74, 82); GIWA_L = (110, 116, 126); WOOD = (128, 86, 54); WOOD_D = (90, 58, 36); WALL_W = (238, 232, 216); STONE_K = (176, 170, 158)
DAN_G = (60, 130, 110); DAN_R = (170, 60, 50); DAN_B = (60, 90, 150)
SKY_T, SKY_B = (132, 176, 214), (220, 228, 228)

def grid_open(ground='.', top=3, x0=7, x1=21):
    g = [list('B' * 29) for _ in range(13)]
    for y in range(top, 12):
        for x in range(x0, x1 + 1): g[y][x] = ground
    g[12][14] = ground; g[11][14] = ground
    return g

def skyk(b, h, top=SKY_T, bot=SKY_B):
    d = ImageDraw.Draw(b)
    for y in range(h): d.line([(0, y), (b.width, y)], fill=mix(top, bot, y / max(1, h - 1)))

def granite_mts(b, base_y, seed=3, col=(150, 150, 140), height=110, peaks=((0.3, 1.0), (0.62, 0.8))):
    """화강암 바위산 (북악산 · 인왕산 느낌)"""
    d = ImageDraw.Draw(b); rnd = random.Random(seed); W_ = b.width
    pts = [(0, base_y)]
    for x in range(0, W_ + 30, 30):
        h_ = 26 + rnd.randint(0, 16)
        for px_, ph in peaks:
            dx = abs(x - px_ * W_) / (W_ * 0.16)
            if dx < 1: h_ += height * ph * (1 - dx * dx)
        pts.append((x, base_y - h_))
    pts.append((W_, base_y))
    d.polygon(pts, fill=mix(col, (120, 150, 120), 0.35))
    for i in range(1, len(pts) - 2):
        x, y = pts[i]
        if rnd.random() < 0.5 and base_y - y > 50:
            d.polygon([(x, y + 4), (x + 18, y + 10), (x + 8, y + 36)], fill=sh(col, 1.18))
    for _ in range(int(W_ / 8)):
        x = rnd.randint(0, W_); y = base_y - rnd.randint(4, 40)
        d.ellipse([x, y, x + 9, y + 6], fill=rnd.choice([(70, 110, 80), (84, 124, 88), (60, 96, 72)]))

def giwa_roof(d, x0, x1, y_ridge, y_eave, col=GIWA, flare=16, ridge=True):
    """처마 끝이 살짝 들린 기와지붕 (정면)"""
    mid = (x0 + x1) / 2
    eave = [(x0 - flare, y_eave - 10)]
    for k in range(1, 20):
        t = k / 20; x = x0 - flare + (x1 - x0 + 2 * flare) * t
        eave.append((x, y_eave + 2 - 12 * (2 * t - 1) ** 4))
    eave.append((x1 + flare, y_eave - 10))
    top = [(x1 - (x1 - x0) * 0.08, y_ridge), (x0 + (x1 - x0) * 0.08, y_ridge)]
    d.polygon(eave + top, fill=col)
    for k in range(0, 40):
        t = k / 39; xa = x0 + (x1 - x0) * 0.08 + (x1 - x0) * 0.84 * t; xb = x0 - flare + (x1 - x0 + 2 * flare) * t
        d.line([(xa, y_ridge + 2), (xb, y_eave - 12 * (2 * t - 1) ** 4)], fill=sh(col, 0.8))
    for (x, y) in eave[1:-1:1]: d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=sh(col, 1.5))
    if ridge:
        d.rectangle([x0 + (x1 - x0) * 0.06, y_ridge - 6, x1 - (x1 - x0) * 0.06, y_ridge + 2], fill=sh(col, 0.55))
        for sx in (x0 + (x1 - x0) * 0.06, x1 - (x1 - x0) * 0.06):
            d.polygon([(sx - 6, y_ridge + 2), (sx + 6, y_ridge + 2), (sx + (8 if sx > mid else -8), y_ridge - 12)], fill=sh(col, 0.5))

def hall(b, x0, x1, y_base, wall_h=58, roof_h=46, wall=WALL_W, wood=WOOD, doors='changho', dan=False, roof=GIWA, sign=None, sign_c=(40, 34, 30)):
    """기와 건물 정면 (기단 · 기둥 · 창호/가게 · 지붕 · 현판)"""
    d = ImageDraw.Draw(b)
    d.rectangle([x0 - 8, y_base - 8, x1 + 8, y_base], fill=STONE_K); d.line([(x0 - 8, y_base - 8), (x1 + 8, y_base - 8)], fill=sh(STONE_K, 1.15))
    yt = y_base - 8 - wall_h
    d.rectangle([x0, yt, x1, y_base - 8], fill=wall)
    n = max(2, int((x1 - x0) / 48))
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        d.rectangle([x - 3, yt, x + 3, y_base - 8], fill=wood)
    for k in range(n):
        xa = x0 + (x1 - x0) * k / n + 5; xb = x0 + (x1 - x0) * (k + 1) / n - 5
        if doors == 'changho':
            d.rectangle([xa, yt + 8, xb, y_base - 12], fill=(236, 228, 204))
            for x in range(int(xa) + 4, int(xb), 6): d.line([(x, yt + 8), (x, y_base - 12)], fill=sh(wood, 1.15))
            for y in range(int(yt) + 12, y_base - 12, 7): d.line([(xa, y), (xb, y)], fill=sh(wood, 1.15))
        elif doors == 'shop':
            d.rectangle([xa, yt + 6, xb, y_base - 10], fill=(70, 50, 38))
        elif doors == 'wall':
            d.rectangle([xa, yt + 30, xb, y_base - 12], fill=sh(wall, 0.9))
        elif doors == 'store':      # 곳간 판자문
            d.rectangle([xa, yt + 6, xb, y_base - 10], fill=sh(wood, 1.1))
            for x in range(int(xa) + 6, int(xb), 8): d.line([(x, yt + 6), (x, y_base - 10)], fill=sh(wood, 0.8))
            d.rectangle([(xa + xb) / 2 - 3, (yt + y_base) / 2 - 3, (xa + xb) / 2 + 3, (yt + y_base) / 2 + 3], fill=(60, 60, 60))
    d.rectangle([x0 - 4, yt - 8, x1 + 4, yt], fill=wood)
    if dan:
        for x in range(int(x0), int(x1), 16):
            d.rectangle([x, yt - 8, x + 7, yt - 1], fill=DAN_G); d.rectangle([x + 8, yt - 8, x + 15, yt - 1], fill=DAN_R if (x // 16) % 2 else DAN_B)
    giwa_roof(d, x0, x1, yt - 8 - roof_h, yt - 6, roof)
    if sign:
        f = F(14, 'serif'); tw = d.textlength(sign, font=f)
        sx = (x0 + x1) / 2
        d.rectangle([sx - tw / 2 - 8, yt - 30, sx + tw / 2 + 8, yt - 10], fill=sign_c, outline=(200, 170, 100))
        d.text((sx, yt - 20), sign, font=f, fill=(240, 220, 160), anchor='mm')

def gwanghwamun(b, cx, base_y, scaffold=True):
    """광화문 (석축 홍예문 셋 + 2층 문루) · 공사 중이면 비계"""
    d = ImageDraw.Draw(b)
    W_, H_ = 420, 74
    d.rectangle([cx - W_ / 2, base_y - H_, cx + W_ / 2, base_y], fill=(196, 188, 170))
    for y in range(int(base_y - H_) + 8, int(base_y), 12):
        off = 0 if (y // 12) % 2 else 18
        for x in range(int(cx - W_ / 2) + off, int(cx + W_ / 2), 36): d.line([(x, y - 12), (x, y)], fill=(170, 162, 146))
        d.line([(cx - W_ / 2, y), (cx + W_ / 2, y)], fill=(170, 162, 146))
    for k, w_ in ((-1, 44), (0, 54), (1, 44)):
        ax = cx + k * 120
        d.chord([ax - w_ / 2, base_y - H_ + 14, ax + w_ / 2, base_y - H_ + 14 + w_], 180, 360, fill=(40, 34, 30))
        d.rectangle([ax - w_ / 2, base_y - H_ + 14 + w_ / 2, ax + w_ / 2, base_y], fill=(40, 34, 30))
    y1 = base_y - H_
    hall(b, cx - 150, cx + 150, y1, wall_h=40, roof_h=30, doors='wall', dan=True, wall=(170, 60, 50))
    giwa_roof(d, cx - 120, cx + 120, y1 - 128, y1 - 92, GIWA)
    d.rectangle([cx - 110, y1 - 92, cx + 110, y1 - 80], fill=(170, 60, 50))
    if scaffold:
        for x in range(int(cx - 170), int(cx + 180), 26): d.line([(x, y1 + 4), (x, y1 - 150)], fill=(150, 110, 70), width=3)
        for y in range(int(y1 - 140), int(y1), 24): d.line([(cx - 170, y), (cx + 170, y)], fill=(150, 110, 70), width=2)
        for x in range(int(cx - 170), int(cx + 150), 52): d.line([(x, y1), (x + 26, y1 - 24)], fill=(130, 96, 60), width=2)

def note_label(b, text, x=14 * TS + 24, y=12 * TS + 12):
    label(b, text, x, y, 12, back=(40, 30, 24, 230))

def sea(b, y0, y1, col=(58, 120, 168), deep=(34, 86, 140), seed=3):
    d = ImageDraw.Draw(b); rnd = random.Random(seed)
    for y in range(int(y0), int(y1)): d.line([(0, y), (b.width, y)], fill=mix(deep, col, (y - y0) / max(1, y1 - y0)))
    for _ in range(int(b.width * (y1 - y0) / 900)):
        x, y = rnd.randint(0, b.width), rnd.randint(int(y0) + 2, int(y1) - 2); d.line([(x, y), (x + rnd.randint(6, 16), y)], fill=sh(col, 1.25))

def fortress(b, x0, x1, y_top, h=52, col=(178, 172, 158), crenel=True):
    """성벽 (돌 쌓기 + 여장)"""
    d = ImageDraw.Draw(b)
    d.rectangle([x0, y_top, x1, y_top + h], fill=col)
    rnd = random.Random(x0 + y_top)
    for y in range(int(y_top) + 4, int(y_top + h), 10):
        off = rnd.randint(0, 16)
        for x in range(int(x0) - off, int(x1), 22): d.rectangle([max(x, x0), y, min(x + 20, x1), y + 9], outline=sh(col, 0.8))
    if crenel:
        for x in range(int(x0), int(x1), 30):
            d.rectangle([x, y_top - 16, x + 24, y_top], fill=sh(col, 1.05)); d.rectangle([x + 9, y_top - 10, x + 14, y_top - 5], fill=(50, 46, 42))
            d.line([(x, y_top - 16), (x + 24, y_top - 16)], fill=sh(col, 1.2))

def us_ship(b, x, y, s=1.0, smoke=True, col=(40, 40, 46)):
    """19세기 증기 군함 (옆모습: 돛대 셋 + 굴뚝)"""
    d = ImageDraw.Draw(b)
    d.polygon([(x - 90 * s, y), (x + 100 * s, y), (x + 80 * s, y + 22 * s), (x - 76 * s, y + 22 * s)], fill=col)
    d.line([(x - 86 * s, y + 6 * s), (x + 96 * s, y + 6 * s)], fill=(220, 220, 220), width=max(1, int(2 * s)))
    for k in range(6): d.rectangle([x - 60 * s + k * 26 * s, y + 9 * s, x - 55 * s + k * 26 * s, y + 13 * s], fill=(20, 20, 24))
    for mx in (-56, 6, 64):
        d.line([(x + mx * s, y), (x + mx * s, y - 70 * s)], fill=(60, 50, 40), width=max(1, int(2 * s)))
        for yy in (-58, -40, -22): d.line([(x + (mx - 16) * s, y + yy * s), (x + (mx + 16) * s, y + yy * s)], fill=(60, 50, 40))
    d.rectangle([x - 18 * s, y - 34 * s, x - 6 * s, y], fill=(30, 30, 30))
    if smoke:
        for k in range(5): d.ellipse([x - 26 * s - k * 14 * s, y - 52 * s - k * 6 * s, x - 2 * s - k * 12 * s, y - 36 * s - k * 6 * s], fill=(90 + k * 12, 90 + k * 12, 96 + k * 12))

def steamship(b, x, y, s=1.0, name=None):
    """여객 증기선 (제물포 · 메이지마루)"""
    d = ImageDraw.Draw(b)
    d.polygon([(x - 150 * s, y - 6 * s), (x + 160 * s, y - 6 * s), (x + 130 * s, y + 34 * s), (x - 130 * s, y + 34 * s)], fill=(36, 36, 42))
    d.rectangle([x - 140 * s, y - 6 * s, x + 150 * s, y + 2 * s], fill=(160, 40, 36))
    d.rectangle([x - 90 * s, y - 34 * s, x + 90 * s, y - 6 * s], fill=(236, 232, 220))
    for k in range(10): d.ellipse([x - 82 * s + k * 17 * s, y - 26 * s, x - 74 * s + k * 17 * s, y - 18 * s], fill=(60, 70, 90))
    d.rectangle([x - 14 * s, y - 80 * s, x + 6 * s, y - 34 * s], fill=(30, 30, 30)); d.rectangle([x - 14 * s, y - 70 * s, x + 6 * s, y - 62 * s], fill=(200, 200, 200))
    for mx in (-110, 110): d.line([(x + mx * s, y - 6 * s), (x + mx * s, y - 96 * s)], fill=(70, 56, 40), width=max(2, int(3 * s)))
    for k in range(6): d.ellipse([x - 20 * s - k * 22 * s, y - 104 * s - k * 8 * s, x + 6 * s - k * 18 * s, y - 84 * s - k * 8 * s], fill=(110 + k * 14, 110 + k * 14, 116 + k * 14))
    if name: d.text((x + 100 * s, y + 18 * s), name, font=F(int(11 * s) + 4), fill=(236, 230, 210), anchor='mm')

def jangpan(b, x0, y0, x1, y1, col=(214, 170, 96)):
    """장판 (기름 먹인 종이 바닥)"""
    d = ImageDraw.Draw(b)
    d.rectangle([x0, y0, x1, y1], fill=col)
    for y in range(int(y0), int(y1), 48):
        for x in range(int(x0) + ((y // 48) % 2) * 32, int(x1), 64):
            d.rectangle([x, y, x + 63, y + 47], outline=sh(col, 0.9))
            d.line([(x + 4, y + 3), (x + 30, y + 3)], fill=sh(col, 1.08))

def goods(d, x, y, kind):
    """가게 앞 물건"""
    if kind == 'rice':
        for k in range(3): d.rounded_rectangle([x + k * 16, y - 18, x + k * 16 + 15, y], 5, fill=(214, 190, 130), outline=(160, 130, 80))
        d.rounded_rectangle([x + 8, y - 32, x + 23, y - 16], 5, fill=(214, 190, 130), outline=(160, 130, 80))
    elif kind == 'cloth':
        for k in range(4): d.rectangle([x + k * 12, y - 26 + (k % 2) * 4, x + k * 12 + 10, y], fill=[(240, 236, 226), (200, 70, 60), (60, 90, 150), (226, 214, 180)][k], outline=(120, 110, 90))
    elif kind == 'pot':
        for k in range(3): d.ellipse([x + k * 15, y - 20, x + k * 15 + 14, y], fill=(110, 70, 44)); d.ellipse([x + k * 15 + 3, y - 22, x + k * 15 + 11, y - 17], fill=(80, 50, 32))
    elif kind == 'fish':
        d.rectangle([x, y - 10, x + 48, y], fill=(150, 110, 70))
        for k in range(5): d.ellipse([x + 2 + k * 9, y - 16, x + 10 + k * 9, y - 10], fill=(170, 180, 186))
    elif kind == 'paper':
        for k in range(5): d.rectangle([x + k * 3, y - 20 - k * 2, x + 34 + k * 3, y - 16 - k * 2], fill=(246, 242, 228), outline=(200, 190, 170))
    elif kind == 'kerosene':
        for k in range(3): d.rectangle([x + k * 15, y - 22, x + k * 15 + 12, y], fill=(170, 60, 50)); d.rectangle([x + k * 15 + 3, y - 26, x + k * 15 + 8, y - 22], fill=(150, 150, 156))
    elif kind == 'matches':
        for k in range(3):
            for j in range(2): d.rectangle([x + k * 14, y - 10 - j * 10, x + k * 14 + 12, y - j * 10], fill=(230, 200, 120), outline=(150, 110, 60))
    elif kind == 'calico':      # 옥양목 (하얀 면직물 두루마리)
        for k in range(4): d.rounded_rectangle([x + k * 4, y - 12 - k * 7, x + 46 + k * 4, y - k * 7], 3, fill=(250, 250, 246), outline=(180, 180, 176))

def shop_row(b, x0, x1, y_base, signs, era='1867'):
    """시전 행랑: 기와 가게들이 길게 이어진 정면 + 간판 + 물건"""
    d = ImageDraw.Draw(b)
    n = len(signs); w = (x1 - x0) / n
    for k, (sg, kind) in enumerate(signs):
        a = x0 + k * w + 4; c = x0 + (k + 1) * w - 4
        hall(b, a, c, y_base, wall_h=54, roof_h=34, doors='shop', wall=(230, 222, 200))
        d = ImageDraw.Draw(b)
        if sg:
            jp = sg.startswith('日')
            f = F(13, 'serif'); tw = d.textlength(sg, font=f)
            sx = (a + c) / 2; sy = y_base - 70
            bc = (240, 236, 226) if jp else (40, 34, 30)
            d.rectangle([sx - tw / 2 - 6, sy - 10, sx + tw / 2 + 6, sy + 10], fill=bc, outline=(160, 130, 80))
            d.text((sx, sy), sg, font=f, fill=(30, 30, 40) if jp else (240, 220, 160), anchor='mm')
            if jp:      # 노렌 (가게 앞 천)
                for j in range(4): d.rectangle([a + 6 + j * (c - a - 12) / 4, y_base - 58, a + 4 + (j + 1) * (c - a - 12) / 4, y_base - 36], fill=(50, 60, 100))
        if kind: goods(d, int(a + 8), y_base - 12, kind)

def straw_mat(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(206, 184, 130))
    for x in range(int(x0), int(x1), 4): d.line([(x, y0), (x, y1)], fill=(186, 160, 106))

# ==================================================================== 01 역관 집 사랑방 (1882 밤)
def sarang(root):
    g = [list('B' * 29) for _ in range(13)]
    for y in range(3, 12):
        for x in range(8, 21): g[y][x] = 'o'
    g[12][14] = 'o'
    g[3][19] = 'x'; g[3][20] = 'x'                     # 책장
    g[4][9] = 'x'                                     # 반닫이
    g[5][14] = 'x'                                    # 서안
    g[3][11] = 'x'; g[3][12] = 'x'; g[3][17] = 'x'     # 문갑 · 사방탁자
    m = Map('sarang', 1, [''.join(r) for r in g], 'seoul', 1882)
    b = m.big; d = ImageDraw.Draw(b)
    dark_out(b, 0, 8, col=(26, 22, 20)); dark_out(b, 21, 29, col=(26, 22, 20))
    jangpan(b, 8 * TS, 3 * TS, 21 * TS - 1, 12 * TS - 1)
    d.rectangle([14 * TS, 12 * TS, 15 * TS - 1, 13 * TS - 1], fill=(120, 90, 60))
    # 뒷벽: 흰 벽 · 나무 기둥 · 창호 · 책가도 병풍
    d.rectangle([8 * TS, 0, 21 * TS - 1, 3 * TS - 1], fill=(232, 224, 204))
    for x in (8 * TS, 12 * TS, 17 * TS, 21 * TS - 8): d.rectangle([x, 0, x + 8, 3 * TS], fill=WOOD)
    d.rectangle([8 * TS, 3 * TS - 10, 21 * TS - 1, 3 * TS - 1], fill=WOOD_D)
    d.rectangle([8 * TS, 0, 21 * TS - 1, 12], fill=WOOD_D)
    # 책가도 병풍 (왼쪽)
    bx = 8 * TS + 14
    for k in range(4):
        x = bx + k * 40
        d.rectangle([x, 26, x + 38, 3 * TS - 16], fill=(236, 226, 196), outline=(120, 80, 50))
        for j, (yy, c) in enumerate(((40, (60, 80, 120)), (66, (150, 60, 50)), (92, (90, 120, 80)))):
            d.rectangle([x + 6, yy, x + 32, yy + 6], fill=c); d.rectangle([x + 10, yy + 8, x + 28, yy + 12], fill=sh(c, 1.3))
        if k == 1: d.ellipse([x + 12, 106, x + 26, 118], outline=(60, 60, 60), width=2)      # 안경
        if k == 2: d.ellipse([x + 12, 104, x + 26, 118], fill=(220, 200, 120), outline=(120, 100, 60))   # 회중시계
    # 창 (오른쪽 · 달빛)
    wx = 17 * TS + 20
    d.rectangle([wx, 20, wx + 150, 3 * TS - 18], fill=(70, 90, 130))
    d.ellipse([wx + 96, 30, wx + 130, 64], fill=(250, 240, 200))
    d.rectangle([wx, 20, wx + 150, 3 * TS - 18], outline=WOOD_D, width=4)
    for x in range(wx + 15, wx + 150, 15): d.line([(x, 20), (x, 3 * TS - 18)], fill=(220, 210, 180))
    for y in range(32, 3 * TS - 18, 15): d.line([(wx, y), (wx + 150, y)], fill=(220, 210, 180))
    # 가운데 벽: 족자 (글씨)
    d.rectangle([13 * TS + 10, 18, 16 * TS - 10, 3 * TS - 20], fill=(244, 238, 222), outline=(140, 110, 70), width=2)
    d.text((14 * TS + 24, 72), '溫故知新', font=F(22, 'serif'), fill=(40, 30, 26), anchor='mm')
    # 옆벽
    d.rectangle([8 * TS - 10, 0, 8 * TS, 12 * TS], fill=WOOD_D); d.rectangle([21 * TS, 0, 21 * TS + 10, 12 * TS], fill=WOOD_D)
    # 보료 · 방석 · 문지방
    d.rounded_rectangle([12 * TS + 4, 6 * TS + 6, 17 * TS - 4, 6 * TS + 40], 6, fill=(150, 60, 60), outline=(110, 40, 40))
    for x in (13 * TS, 15 * TS): d.rounded_rectangle([x + 8, 7 * TS + 8, x + 40, 7 * TS + 36], 8, fill=(80, 100, 150))
    d.rectangle([8 * TS, 12 * TS - 6, 21 * TS - 1, 12 * TS + 2], fill=WOOD)
    # 문갑 (낮은 장) · 화로 · 담뱃대 걸이 · 사방탁자
    with Prop(b, 11 * TS, 3 * TS - 4, 2 * TS, 44) as dd:
        dd.rectangle([2, 8, 2 * TS - 2, 40], fill=(120, 80, 48)); dd.rectangle([2, 4, 2 * TS - 2, 10], fill=(150, 104, 64))
        for k in range(4): dd.rectangle([6 + k * 22, 14, 24 + k * 22, 34], outline=(206, 170, 90)); dd.ellipse([13 + k * 22, 22, 17 + k * 22, 26], fill=(206, 170, 90))
    with Prop(b, 17 * TS + 2, 3 * TS - 30, 44, 74) as dd:
        dd.rectangle([4, 4, 40, 70], outline=(110, 72, 44), width=3)
        for y in (24, 46): dd.line([(4, y), (40, y)], fill=(110, 72, 44), width=3)
        dd.ellipse([12, 8, 30, 22], fill=(220, 220, 214)); dd.rectangle([10, 30, 34, 42], fill=(150, 60, 50)); dd.ellipse([14, 52, 28, 66], fill=(90, 120, 110))
    with Prop(b, 10 * TS + 4, 8 * TS + 4, 40, 40) as dd:
        dd.polygon([(4, 14), (36, 14), (32, 36), (8, 36)], fill=(150, 120, 90)); dd.ellipse([4, 10, 36, 20], fill=(60, 50, 46))
        for k in range(3): dd.ellipse([9 + k * 8, 11, 15 + k * 8, 17], fill=(230, 120, 50))
    glow(b, 16 * TS + 24, 5 * TS + 14, 120, (255, 220, 150), 60)
    m.ev('door', 14, 12, trigger=1)
    m.ev('desk', 14, 5, '!$k_seoan')
    m.ev('chest', 9, 4, '!$k_bandaji')
    m.ev('bookcase', 19, 3, '!$k_bookcase')
    m.ev('lamp', 16, 5, '!$k_lamp_oil', anime=True)
    m.ev('mother', 11, 8, '$k_mother', dir='right')
    m.ev('yunhee', 18, 8, '$k_yunhee23', dir='left')
    m.ev('screen', 9, 2)
    m.ev('window', 19, 2)
    G.finish(b, m.grid, vignette=0.2, ao=0.25, warm=0.1)
    d = ImageDraw.Draw(b)
    d.rectangle([0, 0, 8 * TS - 11, b.height], fill=(26, 22, 20)); d.rectangle([21 * TS + 11, 0, b.width, b.height], fill=(26, 22, 20))
    d.rectangle([0, 12 * TS, 14 * TS - 1, b.height], fill=(26, 22, 20)); d.rectangle([15 * TS, 12 * TS, b.width, b.height], fill=(26, 22, 20))
    note_label(b, '역관 집 사랑방 · 1882년 9월 밤')
    m.save(root, parallax_name='!k_sarang', finish=False)

# ==================================================================== 02 경복궁 중건 공사장 (1867)
def palace(root):
    g = grid_open('.', 5)
    for x in range(7, 22): g[4][x] = 'B'
    for (x, y) in ((8, 6), (20, 6), (9, 11), (19, 11)): g[y][x] = 'x'        # 목재 더미
    g[10][20] = 'x'                                                          # 수레
    m = Map('palace', 2, [''.join(r) for r in g], 'seoul', 1867)
    b = m.big; d = ImageDraw.Draw(b)
    skyk(b, 5 * TS)
    granite_mts(b, 3 * TS + 10, seed=7, height=120, peaks=((0.5, 1.0), (0.2, 0.5)))
    # 멀리 근정전 지붕 (공사 중)
    giwa_roof(d, 10 * TS, 19 * TS, 2 * TS - 50, 2 * TS - 10, GIWA_L)
    for x in range(10 * TS, 19 * TS, 24): d.line([(x, 2 * TS - 10), (x, 2 * TS - 60)], fill=(150, 110, 70), width=2)
    # 궁궐 담 + 광화문
    d.rectangle([0, 3 * TS + 20, b.width, 5 * TS], fill=(210, 160, 120))
    giwa_roof(d, -20, b.width + 20, 3 * TS + 4, 3 * TS + 24, GIWA, flare=0, ridge=False)
    gwanghwamun(b, 14 * TS + 24, 5 * TS, scaffold=True)
    d = ImageDraw.Draw(b)
    # 바깥 마당 (양옆)
    for x in (1, 3, 25, 27): G.tree(b, x, 7, 'pine', 1.0)
    # 공사장 땅 · 주춧돌 자리 (노란 표시)
    for tx in (11, 14, 17):
        X, Y = tx * TS, 5 * TS
        d.rectangle([X + 4, Y + 4, X + TS - 5, Y + TS - 5], outline=(240, 200, 70), width=3)
        d.line([(X + 10, Y + 10), (X + TS - 11, Y + TS - 11)], fill=(240, 200, 70), width=2); d.line([(X + TS - 11, Y + 10), (X + 10, Y + TS - 11)], fill=(240, 200, 70), width=2)
    for (tx, ty) in ((8, 6), (20, 6), (9, 11), (19, 11)):
        with Prop(b, tx * TS - 2, ty * TS + 6, 52, 40) as dd:
            for k in range(4): dd.rounded_rectangle([2, 26 - k * 8, 48, 34 - k * 8], 3, fill=(170, 120, 74) if k % 2 else (150, 104, 62), outline=(100, 66, 40))
    exit_path(b, 14, 14, 11 * TS + 30, '운종가로')
    note_label(b, '경복궁 중건 공사장 · 1867년 봄', y=12 * TS + 12)
    m.ev('exit', 14, 12, trigger=1)
    m.ev('father', 8, 9, '$k_father', dir='right')
    m.ev('overseer', 20, 5, '$k_overseer', dir='left')
    m.ev('corvee', 8, 7, '$k_corvee', dir='right')
    m.ev('carpenter', 20, 8, '$k_carpenter', dir='left')
    m.ev('rich', 10, 10, '$k_rich', dir='up')
    m.ev('daewongun', 14, 4, '$k_daewongun')
    m.ev('stone1', 12, 8, '!$k_stone')
    m.ev('stone2', 14, 8, '!$k_stone')
    m.ev('stone3', 16, 7, '!$k_stone')
    m.ev('cart', 20, 10, '!$k_cart')
    m.ev('gate', 14, 2)
    G.finish(b, m.grid, vignette=0.12, ao=0.25, warm=0.06)
    m.save(root, parallax_name='!k_palace', finish=False)

# ==================================================================== 03 운종가 장터 (1867 · 1871 · 1882)
def market(root):
    g = grid_open('.', 4)
    for x in range(7, 22): g[3][x] = 'B'
    m = Map('market', 3, [''.join(r) for r in g], 'seoul', 1871)
    base = m.big.copy()
    def draw(b, era):
        d = ImageDraw.Draw(b)
        skyk(b, 3 * TS)
        granite_mts(b, 2 * TS + 10, seed=11, height=100, peaks=((0.4, 1.0), (0.75, 0.7)))
        d = ImageDraw.Draw(b)
        if era == '1882':
            signs = [('米廛', 'rice'), ('洋布 · 玉洋木', 'calico'), ('紙廛', 'paper'), ('日本商會', 'matches'), ('石油', 'kerosene'), ('魚物廛', 'fish')]
        else:
            signs = [('米廛', 'rice'), ('綿布廛', 'cloth'), ('紙廛', 'paper'), ('甕器', 'pot'), ('綿紬廛', 'cloth'), ('魚物廛', 'fish')]
        shop_row(b, 6 * TS - 20, 19 * TS, 4 * TS - 4, signs, era)
        # 종루 (보신각) · 오른쪽
        hall(b, 19 * TS + 10, 22 * TS + 30, 4 * TS - 4, wall_h=70, roof_h=40, doors='wall', dan=True, wall=(170, 60, 50), sign='普信閣' if era == '1882' else '鐘樓')
        d = ImageDraw.Draw(b)
        d.ellipse([20 * TS + 34, 2 * TS + 22, 21 * TS + 22, 3 * TS + 22], fill=(90, 110, 100))
        for tx in (0, 25):
            d.rectangle([tx * TS, 2 * TS, (tx + 4) * TS, 4 * TS], fill=(214, 196, 160))
            giwa_roof(d, tx * TS + 10, (tx + 4) * TS - 10, 2 * TS - 30, 2 * TS + 6)
        # 길 (돌 깔린 큰길)
        if era == '1882':
            d.line([(6 * TS, 4 * TS + 6), (23 * TS, 4 * TS + 6)], fill=(110, 100, 90), width=2)
            for x in (7 * TS + 10, 21 * TS + 30): d.line([(x, 4 * TS + 6), (x, 1 * TS)], fill=(110, 90, 70), width=3)    # 깃대 · 장대
        # 길가 난전 (돗자리 위 물건)
        for (tx, ty, kind) in ((6, 9, 'pot'), (22, 7, 'fish'), (22, 10, 'cloth'), (6, 6, 'rice')):
            straw_mat(d, tx * TS - 30, ty * TS + 14, tx * TS + 40, ty * TS + 44); goods(d, tx * TS - 22, ty * TS + 38, kind)
        if era == '1882':
            straw_mat(d, 22 * TS - 30, 4 * TS + 30, 22 * TS + 40, 5 * TS + 12); goods(d, 22 * TS - 24, 5 * TS + 8, 'kerosene')
        note_label(b, '운종가 장터 · %s년' % era)
        G.finish(b, m.grid, vignette=0.12, ao=0.25, warm=0.06)
    for era in ('1867', '1871', '1882'):
        b = base.copy(); draw(b, era)
        exit_path(b, 14, 14, 11 * TS + 30, '큰길')
        save_variant(root, '!k_market' + era, b)
        if era == '1871': m.big = b
    m.ev('exit', 14, 12, trigger=1)
    m.ev('yunhee', 13, 9, '$k_yunhee12', dir='up')
    m.ev('rice_seller', 8, 5, '$k_rice_seller', dir='down')
    m.ev('notice', 11, 4, '!$k_notice')
    m.ev('hmap', 12, 4, '!$k_hmap')
    m.ev('commoner', 16, 7, '$k_commoner', dir='left')
    m.ev('scholar_y', 18, 5, '$k_scholar_y', dir='down')
    m.ev('peddler', 10, 8, '$k_peddler', dir='right')
    m.ev('market_w', 19, 9, '$k_market_w', dir='left')
    m.ev('poor_m', 12, 7, '$k_poor_m', dir='down')
    m.ev('kid', 17, 9, '$k_kid_m', dir='left')
    m.ev('stele', 20, 5, '!$k_stele')
    m.ev('father', 19, 6, '$k_father', dir='left')
    m.ev('father82', 7, 11, '$k_father_old', dir='down')
    m.ev('jpshop', 15, 4, '!$k_jpsign')
    m.ev('kerosene', 17, 4, '!$k_kerosene')
    m.ev('cloth', 9, 4, '!$k_cloth')
    m.ev('qing1', 7, 10, '$k_qing_soldier')
    m.ev('qing2', 21, 10, '$k_qing_soldier')
    m.ev('qmerchant', 21, 9, '$k_qing_merchant')
    m.ev('bell', 20, 2)
    m.save(root, parallax_name='!k_market1871', finish=False, image=False)

# ==================================================================== 04 강화도 정족산성 아래 (1866 · 밤)
GANG_ROCKS = [(9, 10), (19, 10), (11, 8), (16, 8), (8, 6), (13, 6), (20, 6), (10, 4), (17, 4)]
def ganghwa(root):
    g = grid_open(',', 3)
    for (x, y) in GANG_ROCKS: g[y][x] = 'k'
    for x in range(7, 22):
        if x != 14: g[3][x] = 'B'
    m = Map('ganghwa', 4, [''.join(r) for r in g], 'seoul', 1866)
    b = m.big; d = ImageDraw.Draw(b)
    skyk(b, 3 * TS, (24, 30, 54), (52, 58, 82))
    for _ in range(60):
        x, y = random.randint(0, b.width), random.randint(0, 2 * TS); d.point((x, y), fill=(220, 220, 240))
    d.ellipse([22 * TS, 16, 22 * TS + 34, 50], fill=(240, 236, 210))
    granite_mts(b, 3 * TS, seed=21, col=(80, 84, 96), height=90, peaks=((0.5, 1.0),))
    fortress(b, 0, b.width, 2 * TS + 20, 3 * TS + 10 - (2 * TS + 20), col=(120, 118, 112))
    d = ImageDraw.Draw(b)
    # 동문 (가운데 홍예)
    X = 14 * TS
    d.rectangle([X - 30, 2 * TS + 4, X + TS + 30, 4 * TS], fill=(130, 126, 118))
    d.chord([X - 4, 2 * TS + 40, X + TS + 4, 4 * TS + 40], 180, 360, fill=(26, 22, 20)); d.rectangle([X - 4, 3 * TS + 40, X + TS + 4, 4 * TS], fill=(26, 22, 20))
    giwa_roof(d, X - 40, X + TS + 40, 2 * TS - 26, 2 * TS + 6, (60, 62, 70))
    label(b, '정족산성 동문', X + 24, 2 * TS - 36, 11, back=(40, 40, 60, 220))
    for (tx, ty) in GANG_ROCKS:
        with Prop(b, tx * TS - 6, ty * TS + 4, 60, 46) as dd:
            dd.ellipse([2, 14, 58, 44], fill=(96, 94, 90)); dd.ellipse([8, 4, 44, 36], fill=(122, 120, 114)); dd.ellipse([26, 12, 54, 38], fill=(108, 106, 100))
            dd.ellipse([14, 8, 30, 18], fill=(150, 148, 140)); dd.line([(20, 26), (34, 32)], fill=(80, 78, 74), width=2)
            for k in range(4): dd.line([(4 + k * 14, 44), (8 + k * 14, 36)], fill=(70, 100, 60), width=2)
    for (tx, ty) in ((7, 9), (21, 9), (7, 5), (21, 4)): G.tree(b, tx, ty, 'pine', 0.9)
    for tx in (1, 3, 25, 27): G.tree(b, tx, 8, 'pine', 1.0)
    note_label(b, '강화도 정족산성 아래 · 1866년 가을 밤')
    m.ev('gate', 14, 3, trigger=1)
    m.ev('yanghs', 17, 11, '$k_yanghs', dir='left')
    m.ev('hunter', 19, 11, '$k_tiger_hunter', dir='left')
    m.ev('father', 11, 11, '$k_father', dir='right')
    m.ev('fr1', 8, 9, '$k_french', dir='left')
    m.ev('fr2', 20, 7, '$k_french', dir='left')
    m.ev('fr3', 10, 5, '$k_french', dir='right')
    m.ev('rock', 16, 8)
    G.finish(b, m.grid, vignette=0.22, ao=0.25, warm=0.0)
    m.save(root, parallax_name='!k_ganghwa', finish=False)

# ==================================================================== 05 광성보 (1871)
def gwangseong(root):
    g = grid_open('.', 4)
    for x in range(7, 22): g[3][x] = 'B'
    for (x, y) in ((9, 5), (17, 5), (21, 4)): g[y][x] = 'x'
    m = Map('gwangseong', 5, [''.join(r) for r in g], 'seoul', 1871)
    b = m.big; d = ImageDraw.Draw(b)
    skyk(b, 2 * TS, (150, 186, 214), (226, 230, 226))
    sea(b, 2 * TS - 30, 3 * TS + 20, (90, 130, 150), (60, 100, 126))
    d.polygon([(0, 2 * TS - 30), (4 * TS, 2 * TS - 60), (8 * TS, 2 * TS - 36), (9 * TS, 2 * TS - 30)], fill=(110, 126, 100))     # 건너편 김포
    for k, x in enumerate((10, 15, 19)): us_ship(b, x * TS + 20, 2 * TS + 4 - k * 6, 0.55 - k * 0.06)
    fortress(b, 0, b.width, 3 * TS + 6, 30, col=(170, 164, 150))
    d = ImageDraw.Draw(b)
    # 돈대 (둥근 포대) 오른쪽
    d.rounded_rectangle([21 * TS - 10, 2 * TS + 6, 25 * TS, 4 * TS], 40, fill=(170, 164, 150), outline=(130, 124, 110), width=3)
    for y in range(2 * TS + 16, 4 * TS, 11): d.line([(21 * TS, y), (25 * TS - 10, y)], fill=(146, 140, 126))
    for x in range(21 * TS, 25 * TS - 10, 26): d.rectangle([x, 2 * TS - 8, x + 20, 2 * TS + 6], fill=(180, 174, 160)); d.rectangle([x + 8, 2 * TS - 4, x + 12, 2 * TS], fill=(50, 46, 42))
    label(b, '광성 돈대', 23 * TS, 3 * TS + 10, 11, back=(60, 50, 40, 220))
    for (tx, ty) in ((24, 6), (26, 8), (2, 6), (4, 8)): G.tree(b, tx, ty, 'pine', 1.0)
    label(b, '손돌목', 14 * TS, 2 * TS + 34, 11, back=(40, 60, 80, 220))
    note_label(b, '강화도 광성보 · 1871년 6월')
    m.ev('father', 9, 9, '$k_father', dir='right')
    m.ev('eojaeyeon', 14, 5, '$k_eojaeyeon', dir='down')
    m.ev('hunter2', 18, 7, '$k_tiger_hunter', dir='left')
    m.ev('beacon_m', 20, 5, '$k_beacon_m', dir='left')
    m.ev('bongsu', 21, 4, '!$k_bongsu', anime=True)
    m.ev('soldier2', 11, 6, '$k_soldier_k', dir='down')
    m.ev('cannon1', 9, 5, '!$k_cannon')
    m.ev('cannon2', 17, 5, '!$k_cannon')
    m.ev('sujagi', 15, 4, '!$k_sujagi', anime=True)
    m.ev('sea', 14, 2)
    G.finish(b, m.grid, vignette=0.12, ao=0.25, warm=0.05)
    m.save(root, parallax_name='!k_gwangseong', finish=False)

# ==================================================================== 06 강화부 연무당 (1876)
def yeonmudang(root):
    g = grid_open('#', 4)
    for x in range(7, 22): g[3][x] = 'B'
    g[6][14] = 'x'; g[6][13] = 'x'; g[6][15] = 'x'
    m = Map('yeonmudang', 6, [''.join(r) for r in g], 'seoul', 1876)
    b = m.big; d = ImageDraw.Draw(b)
    skyk(b, 3 * TS, (160, 184, 206), (226, 228, 222))
    sea(b, 2 * TS - 10, 3 * TS, (100, 130, 150), (70, 100, 126))
    us_ship(b, 21 * TS, 2 * TS + 6, 0.5, col=(50, 50, 56)); us_ship(b, 25 * TS, 2 * TS + 10, 0.45, col=(50, 50, 56))
    # 연무당 (열린 마루 건물)
    d = ImageDraw.Draw(b)
    x0, x1, yb = 8 * TS, 20 * TS, 4 * TS - 6
    d.rectangle([x0 - 10, yb - 12, x1 + 10, yb], fill=STONE_K)
    for k in range(9):
        x = x0 + (x1 - x0) * k / 8; d.rectangle([x - 4, yb - 92, x + 4, yb - 12], fill=(160, 60, 50)); d.line([(x - 4, yb - 92), (x - 4, yb - 12)], fill=(190, 90, 70))
    d.rectangle([x0, yb - 100, x1, yb - 88], fill=WOOD)
    for x in range(int(x0), int(x1), 16): d.rectangle([x, yb - 100, x + 7, yb - 92], fill=DAN_G); d.rectangle([x + 8, yb - 100, x + 15, yb - 92], fill=DAN_B)
    giwa_roof(d, x0, x1, yb - 150, yb - 96)
    d.rectangle([x0, yb - 88, x1, yb - 12], fill=(186, 150, 110))
    for x in range(int(x0), int(x1), 12): d.line([(x, yb - 40), (x, yb - 12)], fill=(160, 124, 86))
    d.rectangle([x0 + 6, yb - 84, x1 - 6, yb - 44], fill=(236, 228, 206))
    for x in range(int(x0) + 10, int(x1) - 6, 10): d.line([(x, yb - 84), (x, yb - 44)], fill=(190, 160, 120))
    d.line([(x0, yb - 40), (x1, yb - 40)], fill=(120, 86, 56), width=3)
    d.text(((x0 + x1) / 2, yb - 124), '鍊武堂', font=F(16, 'serif'), fill=(240, 220, 160), anchor='mm')
    # 깃발 · 천막 (양쪽 진영)
    for x in (2, 4): d.line([(x * TS, 4 * TS), (x * TS, 1 * TS)], fill=WOOD_D, width=3); d.rectangle([x * TS + 2, 1 * TS, x * TS + 40, 1 * TS + 26], fill=(200, 50, 50))
    for x in (24, 26): d.polygon([(x * TS, 4 * TS), (x * TS + 50, 2 * TS + 20), (x * TS + 100, 4 * TS)], fill=(220, 214, 200), outline=(150, 140, 120))
    # 붉은 깔개
    d.rectangle([11 * TS, 5 * TS + 8, 18 * TS - 1, 8 * TS - 8], fill=(150, 50, 50), outline=(220, 180, 100), width=3)
    note_label(b, '강화부 연무당 · 1876년 2월')
    m.ev('treaty', 14, 6, '!$k_treaty')
    m.ev('sinheon', 12, 6, '$k_sinheon', dir='right')
    m.ev('kuroda', 16, 6, '$k_kuroda', dir='left')
    m.ev('ogyeongseok', 10, 7, '$k_ogyeongseok', dir='right')
    m.ev('father', 11, 8, '$k_father', dir='right')
    m.ev('jp1', 19, 7, '$k_jp_soldier', dir='left')
    m.ev('jp2', 20, 8, '$k_jp_soldier', dir='left')
    m.ev('kr1', 8, 6, '$k_kyujanggak', dir='right')
    m.ev('ships', 20, 2)
    G.finish(b, m.grid, vignette=0.12, ao=0.25, warm=0.05)
    m.save(root, parallax_name='!k_yeonmudang', finish=False)

# ==================================================================== 07 하도감 훈련장 · 궐 앞 (1881)
def hadogam(root):
    g = grid_open('.', 4)
    for x in range(7, 22): g[3][x] = 'B'
    for (x, y) in ((8, 4), (12, 4), (17, 4)): g[y][x] = 'x'
    m = Map('hadogam', 7, [''.join(r) for r in g], 'seoul', 1881)
    b = m.big; d = ImageDraw.Draw(b)
    skyk(b, 3 * TS)
    granite_mts(b, 2 * TS + 20, seed=33, height=90, peaks=((0.7, 1.0), (0.25, 0.6)))
    d = ImageDraw.Draw(b)
    # 왼쪽: 하도감 담장 + 훈련장 (울타리 · 깃발)
    d.rectangle([0, 3 * TS - 10, 15 * TS, 4 * TS], fill=(200, 170, 130))
    giwa_roof(d, -10, 15 * TS, 3 * TS - 22, 3 * TS - 6, GIWA, flare=0, ridge=False)
    for x in range(1, 14, 3):
        d.line([(x * TS + 24, 4 * TS), (x * TS + 24, 2 * TS - 10)], fill=WOOD_D, width=3)
        d.polygon([(x * TS + 26, 2 * TS - 10), (x * TS + 60, 2 * TS), (x * TS + 26, 2 * TS + 12)], fill=[(200, 50, 50), (60, 90, 170), (230, 200, 60), (240, 240, 236), (40, 40, 44)][x % 5])
    # 오른쪽: 창덕궁 돈화문 (2층 문루) + 궁궐 담
    d.rectangle([15 * TS, 3 * TS - 4, b.width, 4 * TS], fill=(214, 150, 110))
    hall(b, 17 * TS, 22 * TS, 4 * TS - 4, wall_h=66, roof_h=30, doors='wall', dan=True, wall=(170, 60, 50), sign='敦化門')
    d = ImageDraw.Draw(b)
    giwa_roof(d, 17 * TS + 20, 22 * TS - 20, 1 * TS - 30, 1 * TS + 6)
    # 유생들의 돗자리
    straw_mat(d, 16 * TS + 8, 8 * TS + 10, 21 * TS - 8, 10 * TS - 6)
    # 훈련장 바닥 (다진 흙 · 줄)
    for y in (6, 8): d.line([(7 * TS, y * TS), (14 * TS, y * TS)], fill=(150, 130, 100))
    exit_path(b, 14, 14, 11 * TS + 30, '사역원으로')
    note_label(b, '하도감 훈련장 · 궐 앞 · 1881년 봄')
    m.ev('horimoto', 10, 5, '$k_horimoto', dir='down')
    m.ev('byeol1', 8, 7, '$k_byeolgigun', dir='up')
    m.ev('byeol2', 10, 7, '$k_byeolgigun', dir='up')
    m.ev('byeol3', 12, 7, '$k_byeolgigun', dir='up')
    m.ev('old_soldier', 8, 10, '$k_old_soldier', dir='right')
    m.ev('drum', 12, 4, '!$k_drum')
    m.ev('rifles', 8, 4, '!$k_rifles')
    m.ev('kimhongjip', 16, 6, '$k_kimhongjip', dir='down')
    m.ev('chmap', 17, 4, '!$k_hmap')
    m.ev('young_off', 18, 6, '$k_young_off', dir='down')
    m.ev('imansun', 19, 8, '$k_imansun', dir='up')
    m.ev('confucian', 17, 9, '$k_confucian', dir='up')
    m.ev('confucian2', 20, 9, '$k_confucian2', dir='up')
    m.ev('palace_gate', 19, 2)
    G.finish(b, m.grid, vignette=0.12, ao=0.25, warm=0.06)
    m.save(root, parallax_name='!k_hadogam', finish=False)

# ==================================================================== 08 선혜청 도봉소 (1882)
def seonhye(root):
    g = grid_open('#', 4)
    for x in range(7, 22): g[3][x] = 'B'
    for (x, y) in ((13, 5), (17, 5), (16, 4)): g[y][x] = 'x'
    m = Map('seonhye', 8, [''.join(r) for r in g], 'seoul', 1882)
    b = m.big; d = ImageDraw.Draw(b)
    skyk(b, 2 * TS, (190, 196, 200), (226, 222, 210))
    hall(b, 5 * TS, 24 * TS, 4 * TS - 4, wall_h=74, roof_h=44, doors='store', wall=(220, 210, 190), sign='宣惠廳 都捧所')
    d = ImageDraw.Draw(b)
    for (tx, ty) in ((8, 5), (20, 5)):
        with Prop(b, tx * TS - 30, ty * TS - 10, 110, 60) as dd:
            for k, (x, y) in enumerate(((4, 30), (36, 30), (68, 30), (20, 10), (52, 10))):
                dd.rounded_rectangle([x, y, x + 34, y + 22], 7, fill=(214, 190, 130), outline=(150, 120, 80))
    exit_path(b, 14, 14, 11 * TS + 30, '종로로')
    note_label(b, '선혜청 도봉소 · 1882년 6월')
    m.ev('kimchunyoung', 11, 7, '$k_kimchunyoung', dir='right')
    m.ev('clerk', 15, 5, '$k_clerk', dir='down')
    m.ev('yunhee', 18, 8, '$k_yunhee23', dir='left')
    m.ev('scale', 13, 5, '!$k_scale')
    m.ev('rice', 17, 5, '!$k_rice')
    m.ev('ledger', 16, 4, '!$k_ledger')
    m.ev('soldier3', 9, 8, '$k_old_soldier', dir='right')
    m.ev('poor2', 20, 7, '$k_poor_m', dir='left')
    m.ev('granary', 14, 2)
    G.finish(b, m.grid, vignette=0.12, ao=0.25, warm=0.05)
    m.save(root, parallax_name='!k_seonhye', finish=False)

# ==================================================================== 09 제물포 (1882 가을 · 에필로그)
def jemulpo(root):
    g = grid_open('P', 5)
    for x in range(7, 22):
        g[4][x] = 'B'; g[3][x] = 'B'; g[5][x] = 'H'
    g[4][14] = 'H'
    g[6][8] = 'x'
    m = Map('jemulpo', 9, [''.join(r) for r in g], 'seoul', 1882)
    b = m.big; d = ImageDraw.Draw(b)
    skyk(b, 2 * TS, (200, 200, 196), (232, 226, 214))
    sea(b, 2 * TS - 40, 5 * TS, (90, 120, 136), (60, 90, 110))
    steamship(b, 14 * TS + 24, 4 * TS - 20, 1.25, '明治丸')
    us_ship(b, 4 * TS, 2 * TS + 10, 0.4, col=(60, 60, 64)); us_ship(b, 25 * TS, 2 * TS + 4, 0.38, col=(60, 60, 64))
    d = ImageDraw.Draw(b)
    d.rectangle([13 * TS + 12, 4 * TS - 10, 15 * TS - 12, 5 * TS], fill=(150, 110, 70))     # 건널판
    for x in range(13 * TS + 12, 15 * TS - 12, 8): d.line([(x, 4 * TS - 10), (x, 5 * TS)], fill=(120, 86, 52))
    # 양옆 창고 (일본 · 청 조계 건물)
    for (x0, x1, c) in ((0, 6 * TS, (200, 190, 170)), (23 * TS, b.width, (190, 170, 160))):
        d.rectangle([x0, 4 * TS, x1, 6 * TS], fill=c); d.rectangle([x0, 4 * TS - 14, x1, 4 * TS], fill=sh(c, 0.7))
        for x in range(int(x0) + 14, int(x1) - 20, 40): d.rectangle([x, 4 * TS + 20, x + 20, 5 * TS + 20], fill=(70, 60, 54))
    note_label(b, '제물포 항구 · 1882년 9월')
    m.ev('ship', 14, 4)
    m.ev('father', 12, 9, '$k_father_old', dir='right')
    m.ev('mother', 11, 9, '$k_mother', dir='right')
    m.ev('yunhee', 10, 9, '$k_yunhee23', dir='right')
    m.ev('parkyounghyo', 15, 6, '$k_parkyounghyo', dir='down')
    m.ev('kimokgyun', 17, 6, '$k_kimokgyun', dir='down')
    m.ev('sailor', 13, 5, '$k_sailor_jp', dir='down')
    m.ev('qing3', 20, 8, '$k_qing_soldier', dir='left')
    m.ev('crates', 8, 6, '!$k_rice')
    G.finish(b, m.grid, vignette=0.14, ao=0.25, warm=0.05)
    m.save(root, parallax_name='!k_jemulpo', finish=False)

def build(root, only=None):
    fns = [sarang, palace, market, ganghwa, gwangseong, yeonmudang, hadogam, seonhye, jemulpo]
    for f in fns:
        if only and f.__name__ not in only: continue
        f(root); print('map', f.__name__)
    write_mapinfos(root, MAP_NAMES)

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2:] or None)
