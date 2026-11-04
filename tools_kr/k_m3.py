"""전보 소년 지도 3: 09 플랑드르 참호 · 10 무인 지대 · 11 군수 공장 · 12 브라이턴 인도군 병원 · 13 파리 케도르세 · 14 베르사유 거울의 방"""
from k_mapbase import *
import k_arch as A
import k_flags as FL
from k_m2 import facade

SAND = (176, 158, 112)
def sandbag_row(d, x0, x1, y, rows=2, col=SAND, seed=0):
    rnd = random.Random(seed)
    for r in range(rows):
        yy = y - r * 11
        off = (r % 2) * 12
        for xx in range(int(x0) - off, int(x1), 24):
            c = sh(col, rnd.choice([0.9, 0.96, 1.0, 1.06]))
            d.rounded_rectangle([xx, yy, xx + 22, yy + 12], 4, fill=c); d.line([(xx + 3, yy + 3), (xx + 19, yy + 3)], fill=sh(c, 1.12))
            d.line([(xx + 11, yy + 2), (xx + 11, yy + 10)], fill=sh(c, 0.82))

def barbed(d, x0, x1, y, seed=0, col=(70, 66, 60)):
    rnd = random.Random(seed)
    for xx in range(int(x0), int(x1), 40): d.line([(xx, y + 18), (xx + rnd.randint(-4, 4), y - 10)], fill=(80, 64, 46), width=3)
    for k in range(4):
        pts = [(xx, y - 6 + k * 6 + math.sin(xx * 0.11 + k) * 4) for xx in range(int(x0), int(x1), 6)]
        d.line(pts, fill=col)
        for (px_, py_) in pts[::3]: d.line([(px_ - 2, py_ - 2), (px_ + 2, py_ + 2)], fill=sh(col, 1.3))

def crater(d, cx, cy, r, mud=(96, 76, 54), water=None):
    d.ellipse([cx - r, cy - r * 0.6, cx + r, cy + r * 0.6], fill=sh(mud, 1.15))
    d.ellipse([cx - r * 0.8, cy - r * 0.45, cx + r * 0.8, cy + r * 0.5], fill=sh(mud, 0.75))
    if water: d.ellipse([cx - r * 0.5, cy - r * 0.2, cx + r * 0.5, cy + r * 0.35], fill=water)

def stump(d, x, y, h=60):
    d.polygon([(x - 6, y), (x + 6, y), (x + 3, y - h), (x - 1, y - h - 8), (x - 4, y - h + 4)], fill=(60, 52, 44))
    d.line([(x, y - h * 0.6), (x + 14, y - h * 0.8)], fill=(60, 52, 44), width=3)

# ==================================================================== 09 플랑드르 참호 (1914년 12월 / 1915년 4월)
def trench(root):
    g = [list('u' * 29) for _ in range(13)]
    for y in range(0, 3):
        for x in range(29): g[y][x] = 'B'
    for y in range(10, 13):
        for x in range(29): g[y][x] = 'B'
    for y in range(3, 10):
        for x in list(range(0, 6)) + list(range(23, 29)): g[y][x] = 'B'
    for y in range(3, 10):
        for x in range(6, 23): g[y][x] = 'H'          # 참호 바닥 널판
    for (x, y) in ((10, 3), (10, 4), (16, 3), (16, 4), (21, 3), (21, 4)): g[y][x] = 'x'     # 지그재그 방벽(횡장)
    for x in (7, 8): g[9][x] = 'u'
    g[10][18] = 'H'; g[10][8] = 'H'                 # 엄폐호 입구 · 연락호
    g[7][12] = 'x'                                  # 화로
    m = Map('trench', 9, [''.join(r) for r in g], 'flanders', 1914)
    base = m.big.copy()

    def draw(b, era):
        d = ImageDraw.Draw(b)
        mud = (96, 76, 54) if era != '14' else (110, 98, 86)
        # 참호 너머 (무인 지대)
        for y in range(0, 2 * TS):
            d.line([(0, y), (PW, y)], fill=mix((170, 176, 180) if era == '14' else (176, 190, 196), (120, 110, 90), y / (2 * TS)))
        d.rectangle([0, TS + 4, PW, 2 * TS + 10], fill=sh(mud, 0.95))
        for xx in range(30, PW, 140): stump(d, xx + random.Random(xx).randint(-20, 20), TS + 26, 40)
        barbed(d, 0, PW, TS + 16, 3)
        # 흉벽 (모래주머니)
        d.rectangle([0, 2 * TS + 6, PW, 3 * TS + 4], fill=(120, 104, 74))
        sandbag_row(d, 0, PW, 3 * TS - 8, 3, seed=7)
        if era == '14':     # 서리
            for _ in range(500):
                rx, ry = random.randint(0, PW), random.randint(2 * TS, 3 * TS + 4); d.point((rx, ry), fill=(236, 240, 244))
        # 바닥 진흙 + 널판
        d.rectangle([0, 3 * TS + 4, PW, 10 * TS], fill=mud)
        for y in range(3, 10):
            for x in range(6, 23):
                X = x * TS
                d.rectangle([X + 2, y * TS + 14, X + TS - 2, y * TS + 34], fill=(140, 110, 72))
                for k in range(4): d.line([(X + 4 + k * 11, y * TS + 14), (X + 4 + k * 11, y * TS + 34)], fill=(110, 84, 54))
        for (x, y) in ((7, 9), (8, 9)): A.G.rock if False else None
        d.ellipse([7 * TS - 10, 9 * TS + 4, 9 * TS + 10, 10 * TS - 2], fill=(80, 70, 56))
        # 횡장 (모래주머니 기둥)
        for x in (10, 16, 21):
            with Prop(b, x * TS - 4, 3 * TS - 10, TS + 8, 2 * TS + 20) as dd:
                for r in range(9):
                    yy = 2 * TS + 8 - r * 10; off = (r % 2) * 8
                    dd.rounded_rectangle([2 + off, yy, 26 + off, yy + 12], 4, fill=sh(SAND, 0.92 + (r % 3) * 0.05)); dd.rounded_rectangle([24 - off, yy, TS + 4 - off, yy + 12], 4, fill=sh(SAND, 1.0))
        # 사격 발판 + 잠망경
        d.rectangle([6 * TS, 3 * TS + 4, 23 * TS, 3 * TS + 14], fill=(130, 100, 66))
        with Prop(b, 13 * TS + 14, 2 * TS - 10, 20, 70) as dd:
            dd.rectangle([6, 0, 14, 64], fill=(90, 80, 60)); dd.rectangle([4, 0, 16, 10], fill=(60, 56, 50)); dd.rectangle([6, 2, 14, 7], fill=(150, 190, 210))
        # 뒷벽 (파라도) + 엄폐호
        d.rectangle([0, 10 * TS, PW, PH], fill=(104, 88, 62))
        sandbag_row(d, 0, PW, 10 * TS + 6, 2, col=(160, 142, 100), seed=11)
        with Prop(b, 17 * TS - 6, 10 * TS - 4, 3 * TS + 12, 2 * TS + 24) as dd:
            dd.rectangle([0, 6, 3 * TS + 11, 2 * TS + 23], fill=(90, 74, 52))
            dd.rectangle([30, 14, 3 * TS - 18, 2 * TS + 23], fill=(30, 24, 20))
            for k in range(3): dd.rectangle([22 + k * 2, 8 + k * 2, 3 * TS - 10 - k * 2, 14 + k * 2], fill=(110, 84, 54))
            dd.rectangle([40, 30, 70, 46], fill=(80, 60, 40)); dd.ellipse([46, 24, 56, 34], fill=(30, 30, 30))
        glow(b, 18 * TS + 24, 11 * TS, 50, (255, 200, 120), 60)
        label(b, '통신 엄폐호', 18 * TS + 24, 12 * TS + 28, 10, back=(50, 40, 30, 230))
        with Prop(b, 7 * TS - 6, 10 * TS - 4, 3 * TS, 2 * TS + 24) as dd:
            dd.rectangle([0, 6, 3 * TS - 1, 2 * TS + 23], fill=(96, 80, 56)); dd.rectangle([30, 6, 3 * TS - 30, 2 * TS + 23], fill=(130, 104, 70))
            for yy in range(10, 2 * TS + 20, 12): dd.line([(32, yy), (3 * TS - 32, yy)], fill=(100, 80, 54), width=2)
        label(b, '연락호 (후방)', 8 * TS + 18, 12 * TS + 28, 10, back=(50, 40, 30, 230))
        # 화로
        with Prop(b, 12 * TS + 2, 7 * TS + 4, 44, 44) as dd:
            dd.rectangle([8, 10, 36, 40], fill=(70, 66, 60))
            for xx in range(10, 36, 5): dd.rectangle([xx, 12, xx + 2, 38], fill=(40, 38, 36))
            dd.polygon([(10, 12), (18, 0), (24, 10), (30, 2), (34, 12)], fill=(250, 150, 60))
        glow(b, 12 * TS + 24, 7 * TS + 16, 50, (255, 170, 80), 70)
        # 사다리 (참호 밖으로)
        with Prop(b, 14 * TS + 8, 2 * TS - 20, 34, 2 * TS + 4) as dd:
            for xx in (2, 28): dd.rectangle([xx, 0, xx + 4, 2 * TS + 3], fill=(140, 110, 70))
            for yy in range(6, 2 * TS, 12): dd.rectangle([2, yy, 32, yy + 3], fill=(150, 120, 80))
        if era == '14':
            label(b, '플랑드르 · 1914년 12월 24일', 14 * TS, 9 * TS + 30, 12, back=(50, 40, 30, 230))
        else:
            label(b, '이프르 · 1915년 4월', 14 * TS, 9 * TS + 30, 12, back=(50, 40, 30, 230))
    for era in ('14', '15'):
        b = base.copy(); draw(b, era)
        G.finish(b, m.grid, vignette=0.2, ao=0.3, warm=(-0.04 if era == '14' else 0.0))
        save_variant(root, '!c_trench' + era, b)
    m.ev('ladder', 14, 2)
    m.ev('periscope', 13, 3)
    m.ev('dugout', 18, 10, trigger=1)
    m.ev('back', 8, 10, trigger=1)
    m.ev('brazier', 12, 7)
    m.ev('officer', 19, 5, '$c_officer_uk', dir='left')
    m.ev('alfie', 9, 6, '$c_tommy14', dir='right')
    m.ev('sepoy', 22, 6, '$c_sepoy', dir='left')
    m.ev('sepoy2', 22, 8, '$c_sepoy2', dir='left')
    m.ev('scot', 13, 8, '$c_scot', dir='up')
    m.ev('tommy1', 7, 4, '$c_tommy14b', dir='up')
    m.ev('tommy2', 17, 4, '$c_tommy14', dir='up')
    m.ev('medic', 15, 9, '$c_medic', dir='left')
    for (x, y) in ((8, 2), (19, 2), (24, 1), (4, 1)): m.ev('xtree', x, y, '!$c_xtree', priority=2, through=True, anime=True)
    m.ev('alfie15', 9, 6, '$c_tommy16', dir='right')
    for k, (x, y) in enumerate(((7, 3), (12, 3), (18, 3))): m.ev('gas%d' % (k + 1), x, y, '!$c_gas', through=True, anime=True, priority=2)
    for k, (x, y) in enumerate(((11, 6), (20, 6), (15, 5))): m.ev('cough%d' % (k + 1), x, y, '$c_tommy16', dir='up')
    m.save(root, parallax_name='!c_trench14', image=False)

# ==================================================================== 10 무인 지대 (크리스마스 낮 / 1916 밤 / 1916 새벽)
def nomans(root):
    g = [list('u' * 29) for _ in range(13)]
    for y in range(0, 2):
        for x in range(29): g[y][x] = 'B'
    for y in range(11, 13):
        for x in range(29): g[y][x] = 'B'
    g[11][14] = 'u'
    for y in range(2, 11):
        for x in list(range(0, 6)) + list(range(23, 29)): g[y][x] = 'B'
    for y in range(2, 11):
        for x in range(6, 23): g[y][x] = ',' if (x * 7 + y * 3) % 5 else 'u'
    wire = [(7, 4), (8, 4), (11, 4), (12, 4), (17, 4), (18, 4), (21, 4), (6, 8), (9, 8), (10, 8), (15, 8), (16, 8), (19, 8), (20, 8)]
    for (x, y) in wire: g[y][x] = 'x'
    for (x, y) in ((13, 6), (20, 6), (8, 6)): g[y][x] = 'k'          # 부러진 나무 둥치
    m = Map('nomans', 10, [''.join(r) for r in g], 'flanders', 1916)
    base = m.big.copy()

    def draw(b, era):
        d = ImageDraw.Draw(b)
        mud = (110, 98, 86) if era == 'xmas' else (96, 76, 54)
        d.rectangle([0, 0, PW, PH], fill=mud)
        rr = random.Random(16)
        for _ in range(26):
            crater(d, rr.randint(0, PW), rr.randint(2 * TS, 11 * TS), rr.randint(26, 54), mud, (90, 100, 96) if rr.random() < 0.4 else None)
        if era == 'xmas':
            for _ in range(2500):
                x, y = rr.randint(0, PW), rr.randint(0, PH); d.point((x, y), fill=(232, 236, 240))
        # 독일군 참호 (위)
        d.rectangle([0, 0, PW, TS + 30], fill=(90, 84, 70))
        sandbag_row(d, 0, PW, TS + 18, 3, col=(150, 150, 130), seed=3)
        # 영국군 참호 (아래)
        d.rectangle([0, 11 * TS - 6, PW, PH], fill=(90, 76, 56))
        sandbag_row(d, 0, PW, 11 * TS + 4, 2, seed=5)
        d.rectangle([14 * TS + 6, 11 * TS - 6, 15 * TS - 6, PH], fill=(70, 58, 44))
        label(b, '↓ 우리 참호', 14 * TS + 24, 12 * TS + 24, 10, back=(50, 40, 30, 230))
        # 철조망
        for (x, y) in wire:
            barbed(d, x * TS, x * TS + TS, y * TS + 30, x + y)
        for (x, y) in ((13, 6), (20, 6), (8, 6)): stump(d, x * TS + 24, y * TS + 44, 70)
        if era != 'xmas':
            # 끊어진 전화선 (영국 참호 → 전방 관측소)
            pts = [(14 * TS + 24, 11 * TS), (12 * TS, 9 * TS + 30), (9 * TS + 24, 7 * TS + 30), (11 * TS, 5 * TS + 30), (16 * TS, 6 * TS + 40), (19 * TS, 5 * TS + 20), (21 * TS + 30, 3 * TS + 30)]
            d.line(pts, fill=(30, 30, 30), width=2)
            with Prop(b, 21 * TS, 2 * TS + 8, 60, 46) as dd:      # 전방 관측소
                dd.rectangle([4, 14, 56, 44], fill=(110, 96, 70)); sandbag_row(dd, 0, 60, 30, 2, seed=9)
                dd.rectangle([20, 22, 40, 34], fill=(30, 26, 22))
            label(b, '전방 관측소', 21 * TS + 30, 3 * TS + 46, 10, back=(50, 40, 30, 230))
    for era in ('xmas', 'night', 'dawn'):
        b = base.copy(); draw(b, era)
        G.finish(b, m.grid, vignette=0.24 if era != 'xmas' else 0.16, ao=0.3, warm=-0.06 if era == 'xmas' else 0.0)
        save_variant(root, '!c_nomans_' + era, b)
    # 크리스마스
    for (x, y) in ((8, 1), (12, 1), (17, 1), (21, 1)): m.ev('xtree', x, y, '!$c_xtree', priority=2, through=True, anime=True)
    m.ev('fritz', 14, 5, '$c_fritz14', dir='down')
    m.ev('fritz2', 16, 6, '$c_fritz14b', dir='left')
    m.ev('alfie', 12, 7, '$c_tommy14', dir='right')
    m.ev('scot', 15, 7, '$c_scot', dir='up')
    m.ev('ball', 11, 9, '!$c_ball', anime=True)
    m.ev('chaplain', 10, 6, '$c_officer_uk', dir='right')
    for (x, y, sp) in ((9, 9, '$c_tommy14b'), (13, 9, '$c_fritz14'), (17, 9, '$c_tommy14'), (19, 7, '$c_fritz14b'), (7, 7, '$c_sepoy2'), (18, 5, '$c_fritz14')):
        m.ev('mingle', x, y, sp, dir='down')
    # 1916 밤: 끊어진 곳 3군데 + 탐조등 + 기관총 + 보초
    for i, (x, y) in enumerate(((12, 9), (9, 7), (19, 5))): m.ev('break%d' % (i + 1), x, y, '!$c_spark', anime=True)
    m.ev('op', 21, 3)
    m.ev('light1', 9, 1, '!$c_searchlight', anime=True)
    m.ev('light2', 18, 1, '!$c_searchlight', anime=True)
    m.ev('mgnest', 13, 1, '!$c_mg')
    m.ev('sentry1', 11, 3, '$c_fritz16', dir='down')
    m.ev('sentry2', 16, 3, '$c_fritz16', dir='down')
    m.ev('home', 14, 11, trigger=1)
    # 1916 새벽: 전차 · 비행기
    m.ev('tank', 2, 7, '!$c_tank', dir='right', through=True)
    m.ev('plane', 26, 3, '!$c_plane', dir='left', through=True, priority=2)
    for (x, y, sp) in ((5, 9, '$c_tommy16'), (6, 10, '$c_tommy16'), (4, 10, '$c_canuck'), (3, 9, '$c_tommy16')):
        m.ev('advance', x, y, sp, dir='right', through=True)
    m.ev('officer', 15, 10, '$c_officer_uk', dir='up')
    m.save(root, parallax_name='!c_nomans_night', image=False)

# ==================================================================== 11 울리치 군수 공장 (1916년)
def factory(root):
    g = [list('BBBBBB' + 'f' * 17 + 'BBBBBB') for _ in range(13)]
    for y in range(3, 12):
        for x in range(7, 22): g[y][x] = 'P'
    for y in (5, 8):
        for x in range(8, 13): g[y][x] = 'x'
        for x in range(16, 21): g[y][x] = 'x'
    g[3][21] = g[3][20] = 'x'
    m = Map('factory', 11, [''.join(r) for r in g], 'paris', 1916)
    b = m.big; d = ImageDraw.Draw(b)
    dark_out(b, 0, 6, col=(30, 28, 26)); dark_out(b, 23, 29, col=(30, 28, 26))
    d.rectangle([6 * TS, 0, 23 * TS - 1, 3 * TS - 1], fill=(150, 140, 120))
    for xx in range(6 * TS, 23 * TS, 24): d.line([(xx, 0), (xx, 3 * TS)], fill=(140, 130, 110))
    # 높은 창 + 굴뚝 보임 + 천장 들보
    for k in range(5):
        xx = 7 * TS + k * 3 * TS
        d.rectangle([xx, 10, xx + 2 * TS, 2 * TS - 4], fill=(170, 180, 186));
        for j in range(4): d.line([(xx + j * 24, 10), (xx + j * 24, 2 * TS - 4)], fill=(80, 76, 70), width=2)
        d.line([(xx, 50), (xx + 2 * TS, 50)], fill=(80, 76, 70), width=2)
    from k_m1 import side_walls
    side_walls(b, (100, 96, 90))
    # 작업대 (포탄 껍데기 · 상자)
    for y in (5, 8):
        for x0 in (8, 16):
            with Prop(b, x0 * TS - 4, y * TS - 14, 5 * TS + 8, TS + 22) as dd:
                dd.rectangle([0, 14, 5 * TS + 7, 40], fill=(120, 100, 76)); dd.rectangle([0, 12, 5 * TS + 7, 16], fill=(150, 126, 96))
                for k in range(13):
                    sx = 10 + k * 18
                    dd.rounded_rectangle([sx, 0, sx + 10, 20], 3, fill=(196, 160, 80)); dd.rectangle([sx, 16, sx + 10, 20], fill=(170, 120, 60))
                dd.rectangle([4, 40, 10, 58], fill=(80, 66, 50)); dd.rectangle([5 * TS - 4, 40, 5 * TS + 2, 58], fill=(80, 66, 50))
    # 상자 더미
    for (x, y) in ((20, 3), (21, 3)):
        with Prop(b, x * TS, y * TS - 20, TS, TS + 20) as dd:
            for r in range(3): dd.rectangle([4, 4 + r * 18, TS - 4, 20 + r * 18], fill=(150, 116, 76), outline=(110, 84, 54))
    # 포스터
    for (x, t, c) in ((9 * TS, '여성들이여, 군수 공장으로!', (40, 70, 130)), (15 * TS, '병사들의 목숨이 여러분 손에', (150, 30, 30))):
        with Prop(b, x, 2 * TS - 10, 3 * TS, 46) as dd:
            dd.rectangle([0, 0, 3 * TS - 1, 45], fill=(236, 226, 196), outline=(80, 70, 60)); dd.rectangle([0, 0, 3 * TS - 1, 12], fill=c)
            dd.text((3 * TS // 2, 28), t, font=F(10), fill=(40, 30, 20), anchor='mm')
    label(b, '울리치 왕립 병기창 · 포탄 충전 작업장 (1916)', 14 * TS, 12 * TS + 12, 11, back=(60, 40, 24, 230))
    top = m.top; td = ImageDraw.Draw(top)
    for xx in range(7 * TS, 22 * TS, 4 * TS):
        td.line([(xx, 0), (xx, 30)], fill=(60, 60, 60, 255), width=2); td.polygon([(xx - 16, 30), (xx + 16, 30), (xx + 8, 22), (xx - 8, 22)], fill=(50, 80, 60, 255))
    b.alpha_composite(top)
    m.ev('door', 14, 12, trigger=1)
    m.ev('bench', 10, 8)
    m.ev('crates', 20, 3)
    m.ev('peel', 14, 4, '$c_forewoman', dir='down')
    m.ev('mary', 11, 9, '$c_mary_w', dir='up')
    for (x, y, sp, dr) in ((9, 4, '$c_muni_w', 'down'), (11, 4, '$c_muni_w2', 'down'), (17, 4, '$c_muni_w3', 'down'), (19, 4, '$c_muni_w', 'down'),
                           (9, 9, '$c_muni_w2', 'up'), (17, 9, '$c_muni_w3', 'up'), (19, 9, '$c_muni_w', 'up')):
        m.ev('worker', x, y, sp, dir=dr)
    m.ev('foreman', 21, 10, '$c_foreman', dir='left')
    m.ev('carrier', 8, 6, '$c_muni_w2', dir='right')
    m.save(root, vignette=0.14, warm=0.02)

# ==================================================================== 12 브라이턴 로열 파빌리언 인도군 병원 (1915년)
def brighton(root):
    g = [list('BBBBBB' + 'f' * 17 + 'BBBBBB') for _ in range(13)]
    for y in range(3, 12):
        for x in range(7, 22): g[y][x] = 'z'
    for x in (8, 10, 18, 20):
        g[4][x] = 'x'; g[5][x] = 'x'
    for x in (8, 10, 18, 20):
        g[8][x] = 'x'; g[9][x] = 'x'
    m = Map('brighton', 12, [''.join(r) for r in g], 'versailles', 1915)
    b = m.big; d = ImageDraw.Draw(b)
    dark_out(b, 0, 6, col=(40, 30, 30)); dark_out(b, 23, 29, col=(40, 30, 30))
    # 붉은·금빛 벽 + 연꽃 장식 + 창 너머 양파 지붕
    d.rectangle([6 * TS, 0, 23 * TS - 1, 3 * TS - 1], fill=(150, 40, 40))
    for xx in range(6 * TS, 23 * TS, 32):
        d.line([(xx, 0), (xx, 3 * TS)], fill=(200, 150, 60), width=2)
        d.ellipse([xx + 10, 20, xx + 22, 32], fill=(220, 180, 80))
    for xx in (8 * TS, 13 * TS, 18 * TS):
        d.rectangle([xx, 12, xx + 2 * TS, 2 * TS + 20], fill=(170, 200, 220))
        d.chord([xx, -10, xx + 2 * TS, 40], 180, 360, fill=(150, 40, 40))
        d.ellipse([xx + 30, 40, xx + 66, 80], fill=(236, 230, 214)); d.polygon([(xx + 48, 30), (xx + 40, 46), (xx + 56, 46)], fill=(236, 230, 214))
        d.rectangle([xx + 34, 70, xx + 62, 2 * TS + 20], fill=(236, 230, 214))
    from k_m1 import side_walls
    side_walls(b, (170, 110, 60))
    # 침대 줄
    for y in (4, 8):
        for x in (8, 10, 18, 20):
            with Prop(b, x * TS - 4, y * TS - 8, TS + 8, 2 * TS + 8) as dd:
                dd.rectangle([4, 8, TS + 4, 2 * TS + 2], fill=(240, 240, 236)); dd.rectangle([6, 12, TS + 2, 30], fill=(250, 250, 250))
                dd.rectangle([6, 34, TS + 2, 2 * TS], fill=(110, 120, 170))
                dd.rectangle([2, 4, 6, 2 * TS + 6], fill=(90, 90, 96)); dd.rectangle([TS + 2, 4, TS + 6, 2 * TS + 6], fill=(90, 90, 96))
    # 바닥 깔개
    d.rectangle([12 * TS, 3 * TS + 10, 17 * TS, 11 * TS + 30], fill=(150, 50, 50)); d.rectangle([12 * TS + 8, 3 * TS + 18, 17 * TS - 8, 11 * TS + 22], fill=(180, 120, 60))
    d.rectangle([12 * TS + 16, 3 * TS + 26, 17 * TS - 16, 11 * TS + 14], fill=(130, 40, 40))
    label(b, '브라이턴 · 로열 파빌리언 인도군 병원 (1915)', 14 * TS, 12 * TS + 12, 11, back=(90, 30, 30, 230))
    top = m.top; td = ImageDraw.Draw(top)
    for xx in (10 * TS, 19 * TS):     # 연꽃 샹들리에
        td.line([(xx, 0), (xx, 28)], fill=(200, 160, 70, 255), width=2)
        for k in range(6):
            a = math.pi * (0.1 + k * 0.16); td.ellipse([xx + math.cos(a) * 26 - 7, 28 + math.sin(a) * 10 - 4, xx + math.cos(a) * 26 + 7, 28 + math.sin(a) * 10 + 10], fill=(240, 220, 180, 255))
        glow(b, xx, 36, 60, (255, 220, 150), 50)
    b.alpha_composite(top)
    m.ev('door', 14, 12, trigger=1)
    m.ev('p1', 8, 6, '$c_patient_sikh', dir='down')
    m.ev('p2', 18, 6, '$c_patient_pa', dir='down')
    m.ev('p3', 20, 10, '$c_patient_gk', dir='down')
    m.ev('p4', 10, 10, '$c_patient_pa', dir='down')
    m.ev('nurse', 13, 6, '$c_nurse', dir='down')
    m.ev('doctor', 16, 4, '$c_doctor', dir='down')
    m.ev('letterbox', 21, 3)
    m.ev('kitchen', 7, 3)
    m.save(root, vignette=0.12, warm=0.06)

# ==================================================================== 13 파리 케도르세 (1919년 봄, 강화 회의장 앞)
def paris(root):
    g = [list('P' * 29) for _ in range(13)]
    for y in range(0, 3):
        for x in range(29): g[y][x] = 'B'
    for y in range(3, 11):
        for x in list(range(0, 6)) + list(range(23, 29)): g[y][x] = 'B'
    for y in range(6, 9):
        for x in range(29): g[y][x] = 'q'
    for x in range(29):
        g[11][x] = 'C'; g[12][x] = 'C'
    for x in (13, 14, 15): g[10][x] = 'P'
    m = Map('paris', 13, [''.join(r) for r in g], 'versailles', 1919)
    b = m.big; d = ImageDraw.Draw(b)
    facade(b, 0, 0, PW, 3 * TS + 6, 'stone', (214, 206, 186), seed=19, floors=3, shop='프랑스 외무부 (케도르세) · 파리 강화 회의', shop_c=(40, 50, 90))
    for i, c in enumerate(['us48', 'uk', 'fr', 'it', 'jp']):
        fl = FL.waving(c, 46, 28, 0.06, i); x = 9 * TS + i * 2 * TS
        d.line([(x, 2 * TS + 10), (x, TS - 10)], fill=(150, 130, 90), width=2); b.alpha_composite(fl, (x + 1, TS - 10))
    d.rectangle([0, 6 * TS, PW, 9 * TS - 1], fill=(140, 136, 126))
    for xx in range(0, PW, 20): d.line([(xx, 6 * TS), (xx, 9 * TS)], fill=(130, 126, 116))
    d.rectangle([0, 10 * TS + 30, PW, 11 * TS + 2], fill=(200, 194, 180))
    for xx in range(0, PW, 18): d.rectangle([xx, 10 * TS + 20, xx + 6, 10 * TS + 30], fill=(200, 194, 180))
    for (x, y) in ((7, 10), (21, 10), (11, 10), (17, 10)): m.tree(x, y, 'mulberry', 0.8)
    label(b, '센강', 4 * TS, 12 * TS, 11, back=(40, 50, 70, 220))
    label(b, '파리 · 1919년 봄', 14 * TS, 10 * TS + 14, 12, back=(40, 40, 70, 230))
    m.ev('gate', 14, 2)
    m.ev('garde1', 12, 3, '$c_garde', dir='down'); m.ev('garde2', 16, 3, '$c_garde', dir='down')
    m.ev('nguyen', 9, 5, '$c_nguyen', dir='down')
    m.ev('kimks', 19, 5, '$c_kimks', dir='down')
    m.ev('egypt', 21, 4, '$c_egy_del', dir='left')
    m.ev('koo', 7, 4, '$c_koo', dir='right')
    m.ev('reporter', 11, 9, '$c_reporter', dir='up')
    m.ev('station', 14, 10)
    for (x, y, sp) in ((8, 7, '$c_paris_m'), (12, 8, '$c_paris_w'), (17, 7, '$c_paris_m'), (20, 8, '$c_paris_w'), (15, 6, '$c_doughboy'), (10, 6, '$c_poilu16')):
        m.ev('walker', x, y, sp, dir='left')
    m.ev('car', 25, 7, '!$c_car2', dir='left', through=True)
    m.save(root, vignette=0.12, warm=0.04)

# ==================================================================== 14 베르사유 궁전 거울의 방 (1919년 6월 28일)
def versailles(root):
    g = [list('BBBBBB' + 'f' * 17 + 'BBBBBB') for _ in range(13)]
    for y in range(3, 12):
        for x in range(7, 22): g[y][x] = 'o'
    for x in range(11, 18): g[6][x] = 'x'          # 서명 탁자
    m = Map('versailles', 14, [''.join(r) for r in g], 'versailles', 1919)
    b = m.big; d = ImageDraw.Draw(b)
    dark_out(b, 0, 6, col=(40, 34, 28)); dark_out(b, 23, 29, col=(40, 34, 28))
    d.rectangle([6 * TS, 0, 23 * TS - 1, 3 * TS - 1], fill=(220, 196, 140))
    for k in range(7):
        xx = 6 * TS + 18 + k * 2 * TS + 12
        d.rectangle([xx, 16, xx + 64, 3 * TS - 10], fill=(200, 176, 120)); d.chord([xx, 0, xx + 64, 40], 180, 360, fill=(200, 176, 120))
        d.rectangle([xx + 6, 22, xx + 58, 3 * TS - 16], fill=(190, 206, 214)); d.chord([xx + 6, 6, xx + 58, 40], 180, 360, fill=(190, 206, 214))
        for j in range(1, 4): d.line([(xx + 6 + j * 13, 22), (xx + 6 + j * 13, 3 * TS - 16)], fill=(220, 196, 140))
        for j in range(1, 4): d.line([(xx + 6, 22 + j * 22), (xx + 58, 22 + j * 22)], fill=(220, 196, 140))
    from k_m1 import side_walls
    side_walls(b, (210, 186, 130))
    # 쪽마루 (헤링본)
    for y in range(3 * TS, 12 * TS, 16):
        for x in range(7 * TS, 22 * TS, 32):
            d.line([(x, y), (x + 16, y + 16)], fill=(150, 104, 64)); d.line([(x + 16, y + 16), (x + 32, y)], fill=(150, 104, 64))
    # 서명 탁자 (말굽 모양 대신 긴 탁자)
    with Prop(b, 11 * TS - 8, 6 * TS - 14, 7 * TS + 16, TS + 30) as dd:
        dd.rounded_rectangle([0, 10, 7 * TS + 15, TS + 14], 6, fill=(160, 120, 70)); dd.rounded_rectangle([4, 8, 7 * TS + 11, TS + 6], 6, fill=(110, 40, 40))
        dd.rectangle([3 * TS + 16, 16, 4 * TS + 8, 36], fill=(246, 240, 224)); dd.line([(3 * TS + 30, 18), (3 * TS + 40, 30)], fill=(30, 30, 30))
        dd.text((3 * TS + 36, 44), '강화 조약', font=F(9), fill=(240, 230, 200), anchor='mm')
    label(b, '베르사유 궁전 · 거울의 방 · 1919년 6월 28일', 14 * TS, 12 * TS + 12, 11, back=(90, 60, 30, 230))
    top = m.top; td = ImageDraw.Draw(top)
    for xx in (9 * TS, 14 * TS + 24, 20 * TS):
        td.line([(xx, 0), (xx, 24)], fill=(214, 182, 100, 255), width=2)
        td.ellipse([xx - 30, 22, xx + 30, 50], fill=(240, 220, 160, 255)); td.ellipse([xx - 20, 28, xx + 20, 44], fill=(255, 246, 220, 255))
        for k in range(7): td.ellipse([xx - 30 + k * 10, 46, xx - 26 + k * 10, 56], fill=(250, 240, 210, 255))
        glow(b, xx, 40, 80, (255, 230, 170), 60)
    b.alpha_composite(top)
    m.ev('door', 14, 12, trigger=1)
    m.ev('treaty', 14, 6)
    m.ev('clemenceau', 14, 5, '$c_clemenceau', dir='down')
    m.ev('wilson', 12, 5, '$c_wilson', dir='down')
    m.ev('lloyd', 16, 5, '$c_lloyd', dir='down')
    m.ev('orlando', 17, 5, '$c_orlando', dir='down')
    m.ev('saionji', 11, 5, '$c_saionji', dir='down')
    m.ev('de1', 13, 8, '$c_de_del', dir='up'); m.ev('de2', 15, 8, '$c_de_del', dir='up')
    m.ev('garde1', 12, 11, '$c_garde', dir='up'); m.ev('garde2', 16, 11, '$c_garde', dir='up')
    for (x, y, sp) in ((8, 4, '$c_reporter'), (9, 4, '$c_paris_m'), (20, 4, '$c_reporter'), (21, 5, '$c_doughboy'), (8, 9, '$c_poilu16'), (21, 9, '$c_paris_w'), (20, 10, '$c_reporter'), (9, 10, '$c_paris_m')):
        m.ev('guest', x, y, sp, dir='down' if y < 7 else 'up')
    m.save(root, vignette=0.12, warm=0.08)

ALL3 = [trench, nomans, factory, brighton, paris, versailles]
