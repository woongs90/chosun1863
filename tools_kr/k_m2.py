"""전보 소년 지도 2: 05 베이징 공사관 거리 · 06 콜카타 거리 · 07 사라예보 강변길 · 08 런던 거리"""
from k_mapbase import *
import k_arch as A
import k_flags as FL

def facade(b, x, y, w, h, style='london', wall=None, seed=0, shop=None, shop_c=(40, 60, 50), floors=3, flags=None, night=False, sign_t=(250, 240, 210), awning=None, door=True):
    """유럽·식민지 도시 건물 앞모습. style: london(벽돌·내리닫이창) austro(파스텔 회벽·장식 창) colonial(아치·베란다) stone(돌)"""
    rnd = random.Random(seed + x * 7)
    wall = wall or {'london': (150, 92, 72), 'austro': (226, 206, 160), 'colonial': (214, 196, 160), 'stone': (196, 188, 170)}[style]
    soft_shadow(b, [x + 4, y + h - 8, x + w + 8, y + h + 6], 90, 5)
    with Prop(b, x - 4, y - 14, w + 8, h + 14) as d:
        ox, oy = 4, 14
        d.rectangle([ox, oy, ox + w, oy + h], fill=wall)
        if style == 'london':
            for yy in range(oy + 4, oy + h, 6):
                d.line([(ox, yy), (ox + w, yy)], fill=sh(wall, 0.9))
                for xx in range(ox + (yy // 6 % 2) * 6, ox + w, 12): d.line([(xx, yy - 6), (xx, yy)], fill=sh(wall, 0.92))
        elif style == 'austro':
            for yy in range(oy + 10, oy + h, 30): d.line([(ox, yy), (ox + w, yy)], fill=sh(wall, 0.94))
        d.rectangle([ox - 3, oy - 4, ox + w + 3, oy + 6], fill=sh(wall, 1.12 if style != 'london' else 1.5))   # 처마 돌림띠
        if style == 'austro':
            for xx in range(ox, ox + w, 10): d.rectangle([xx, oy + 6, xx + 5, oy + 10], fill=sh(wall, 0.85))
        gy = oy + h - 46
        fl_h = (gy - oy - 10) / max(1, floors - 1)
        nwin = max(2, w // 30)
        for f in range(floors - 1):
            wy = oy + 12 + f * fl_h
            for k in range(nwin):
                wx = ox + (k + 0.5) * w / nwin - 8
                lit = night and rnd.random() < 0.5
                if style == 'colonial':
                    d.rectangle([wx - 2, wy, wx + 18, wy + fl_h - 8], fill=sh(wall, 0.8))
                    d.chord([wx - 2, wy - 8, wx + 18, wy + 10], 180, 360, fill=sh(wall, 0.8))
                    for jx in range(int(wx), int(wx + 16), 4): d.line([(jx, wy + 2), (jx, wy + fl_h - 10)], fill=(90, 110, 80))
                else:
                    d.rectangle([wx - 2, wy - 2, wx + 18, wy + fl_h - 8], fill=(236, 230, 214) if style != 'london' else (226, 220, 206))
                    d.rectangle([wx, wy, wx + 16, wy + fl_h - 10], fill=(250, 210, 130) if lit else (70, 86, 100))
                    d.line([(wx + 8, wy), (wx + 8, wy + fl_h - 10)], fill=(226, 220, 206)); d.line([(wx, wy + (fl_h - 10) / 2), (wx + 16, wy + (fl_h - 10) / 2)], fill=(226, 220, 206))
                    if style == 'austro':
                        d.polygon([(wx - 4, wy - 3), (wx + 8, wy - 9), (wx + 20, wy - 3)], fill=sh(wall, 1.1))
                        d.rectangle([wx - 3, wy + fl_h - 8, wx + 19, wy + fl_h - 6], fill=sh(wall, 0.8))
                if flags and f == 0 and k % 2 == 0:
                    fl = FL.waving(flags, 30, 20, 0.06, k)
                    d.line([(wx + 8, wy + fl_h - 8), (wx + 8, wy + fl_h + 14)], fill=(120, 100, 70), width=2)
                    d._image.alpha_composite(fl, (int(wx + 9), int(wy + fl_h - 10)))
        # 1층
        d.rectangle([ox, gy, ox + w, oy + h], fill=sh(wall, 0.88))
        if style == 'colonial':
            for k in range(max(2, w // 40)):
                ax_ = ox + 6 + k * 40
                d.rectangle([ax_, gy + 10, ax_ + 30, oy + h], fill=(60, 50, 40)); d.chord([ax_, gy, ax_ + 30, gy + 22], 180, 360, fill=(60, 50, 40))
        else:
            for k in range(max(2, w // 26)):
                gx0 = ox + 4 + k * 26
                if gx0 + 22 > ox + w: break
                d.rectangle([gx0, gy + 6, gx0 + 20, oy + h - 6], fill=(250, 212, 140) if night else (80, 96, 104))
                d.line([(gx0 + 2, gy + 8), (gx0 + 2, gy + 20)], fill=(140, 160, 170))
        if door:
            dx = ox + w / 2
            d.rectangle([dx - 10, gy + 4, dx + 10, oy + h], fill=(60, 44, 34)); d.rectangle([dx - 8, gy + 6, dx + 8, gy + 18], fill=(110, 130, 140))
        if shop:
            d.rectangle([ox + 4, gy - 16, ox + w - 4, gy - 1], fill=shop_c); d.rectangle([ox + 4, gy - 16, ox + w - 4, gy - 15], fill=sh(shop_c, 1.5))
            fs = 12 if len(shop) <= w // 13 else 10
            d.text((ox + w / 2, gy - 8), shop, font=F(fs), fill=sign_t, anchor='mm')
        if awning:
            d.polygon([(ox + 2, gy + 2), (ox + w - 2, gy + 2), (ox + w + 4, gy + 14), (ox - 4, gy + 14)], fill=awning)
            for xx in range(ox + 2, ox + w, 12): d.polygon([(xx, gy + 2), (xx + 6, gy + 2), (xx + 8, gy + 14), (xx + 2, gy + 14)], fill=sh(awning, 1.3))

# ==================================================================== 05 베이징 공사관 거리 (1900년 8월, 둥자오민샹)
def qing_gate(b, x, y, w, h, roof=(70, 80, 84), wall=(150, 50, 44)):
    soft_shadow(b, [x + 4, y + h - 8, x + w + 8, y + h + 6], 90, 5)
    with Prop(b, x - 14, y - 30, w + 28, h + 30) as d:
        ox, oy = 14, 30
        d.rectangle([ox, oy + 30, ox + w, oy + h], fill=wall)
        for xx in range(ox + 10, ox + w - 10, 26): d.rectangle([xx, oy + 34, xx + 6, oy + h], fill=sh(wall, 0.8))
        d.polygon([(ox - 14, oy + 34), (ox + w + 14, oy + 34), (ox + w - 6, oy + 4), (ox + 6, oy + 4)], fill=roof)
        for xx in range(ox - 10, ox + w + 12, 5): d.line([(xx, oy + 8), (xx - 3, oy + 34)], fill=sh(roof, 0.75))
        d.polygon([(ox - 18, oy + 30), (ox - 4, oy + 26), (ox + 2, oy + 36)], fill=sh(roof, 0.9)); d.polygon([(ox + w + 18, oy + 30), (ox + w + 4, oy + 26), (ox + w - 2, oy + 36)], fill=sh(roof, 0.9))
        d.rectangle([ox + 2, oy, ox + w - 2, oy + 6], fill=sh(roof, 0.6))
        d.rectangle([ox + w / 2 - 22, oy + 50, ox + w / 2 + 22, oy + h], fill=(60, 40, 30))
        for yy in range(int(oy + 56), int(oy + h), 10):
            for xx in (ox + w / 2 - 16, ox + w / 2 + 8): d.ellipse([xx, yy, xx + 4, yy + 4], fill=(210, 170, 80))

def gray_wall(b, x0, x1, y0, y1, col=(140, 138, 134), damaged=False, seed=0):
    d = ImageDraw.Draw(b); rnd = random.Random(seed)
    d.rectangle([x0, y0, x1, y1], fill=col)
    for yy in range(y0 + 4, y1, 8):
        d.line([(x0, yy), (x1, yy)], fill=sh(col, 0.86))
        for xx in range(x0 + (yy // 8 % 2) * 10, x1, 20): d.line([(xx, yy - 8), (xx, yy)], fill=sh(col, 0.9))
    d.rectangle([x0, y0 - 6, x1, y0 + 2], fill=(80, 84, 86))
    if damaged:
        for _ in range(int((x1 - x0) / 60)):
            hx, hy = rnd.randint(x0, x1), rnd.randint(y0 + 4, y1 - 10)
            d.ellipse([hx - 8, hy - 6, hx + 8, hy + 6], fill=sh(col, 0.6)); d.ellipse([hx - 4, hy - 3, hx + 4, hy + 3], fill=sh(col, 0.4))

def beijing(root):
    g = [list('q' * 29) for _ in range(13)]
    for y in range(0, 3):
        for x in range(29): g[y][x] = 'B'
    for y in range(3, 12):
        for x in list(range(0, 6)) + list(range(23, 29)): g[y][x] = 'B'
    for x in range(29): g[12][x] = 'B'
    for x in (13, 14, 15): g[12][x] = 'q'
    for (x, y) in ((8, 8), (20, 8), (7, 11)): g[y][x] = 'x'      # 무너진 벽돌 더미 · 수레
    g[10][21] = g[10][20] = 'x'                                    # 전신 천막
    m = Map('beijing', 5, [''.join(r) for r in g], 'seoul', 1900)
    b = m.big; d = ImageDraw.Draw(b)
    # 하늘 + 공사관 담장 (가운데) + 중국 성벽 (양옆)
    for y in range(0, 40): d.line([(0, y), (PW, y)], fill=mix((176, 186, 190), (214, 206, 186), y / 40))
    gray_wall(b, 0, PW, 30, 3 * TS - 2, damaged=True, seed=19)
    # 8개 공사관 문 + 깃발
    codes = ['uk', 'us45', 'fr', 'de', 'ru', 'jp', 'it', 'ah']
    for i, c in enumerate(codes):
        x = (7 + i * 2) * TS - 18
        with Prop(b, x, 40, 2 * TS - 12, 2 * TS + 6) as dd:
            W_ = 2 * TS - 13
            dd.rectangle([2, 20, W_ - 2, 2 * TS + 5], fill=[(200, 196, 186), (210, 200, 180), (196, 190, 176)][i % 3])
            dd.rectangle([W_ / 2 - 12, 40, W_ / 2 + 12, 2 * TS + 5], fill=(70, 50, 36))
            dd.polygon([(0, 22), (W_ / 2, 4), (W_, 22)], fill=(110, 96, 86) if i % 2 else (90, 96, 100))
            for k in range(4): dd.rectangle([8 + k * 18, 26, 14 + k * 18, 34], fill=(70, 84, 96))
    # 무너진 곳 · 탄흔
    for (x, y) in ((8, 8), (20, 8)):
        with Prop(b, x * TS - 10, y * TS + 6, 68, 44) as dd:
            for k in range(14):
                rx, ry = random.Random(x * 9 + k).randint(0, 54), random.Random(x + k * 7).randint(6, 34)
                dd.rectangle([rx, ry, rx + 12, ry + 8], fill=random.Random(k + y).choice([(150, 140, 134), (130, 126, 120), (170, 160, 150), (120, 70, 60)]))
    with Prop(b, 7 * TS - 20, 11 * TS - 6, 80, 50) as dd:      # 버려진 수레
        dd.rectangle([6, 14, 70, 30], fill=(130, 96, 60)); dd.ellipse([10, 22, 34, 46], outline=(80, 60, 40), width=4); dd.line([(70, 22), (80, 10)], fill=(110, 80, 50), width=3)
    # 전신 천막 (임시 야전 전신소)
    with Prop(b, 20 * TS - 10, 9 * TS + 6, 2 * TS + 20, 2 * TS) as dd:
        dd.polygon([(0, 50), (2 * TS + 10, 50), (2 * TS - 6, 8), (16, 8)], fill=(206, 196, 160)); dd.rectangle([20, 50, 2 * TS - 6, 2 * TS - 2], fill=(120, 100, 70))
        dd.rectangle([30, 56, 70, 70], fill=(80, 60, 40)); dd.line([(40, 54), (54, 50)], fill=(206, 170, 90), width=2)
    d.line([(22 * TS + 20, 10 * TS + 10), (22 * TS + 20, 7 * TS)], fill=(110, 80, 50), width=3); d.line([(22 * TS + 20, 7 * TS + 4), (29 * TS, 6 * TS + 20)], fill=(40, 40, 40))
    label(b, '야전 전신소', 21 * TS, 11 * TS + 34, 10, back=(40, 50, 60, 220))
    for (x, y) in ((6, 4), (22, 4), (6, 10), (22, 11)): m.tree(x, y, 'willow', 0.9)
    exit_path(b, 13, 15, 12 * TS + 2, '↓ 톈진 · 항구로', col=(150, 146, 136), edge=(110, 106, 100))
    qing_gate(b, 0 * TS, 3 * TS, 5 * TS, 3 * TS)
    qing_gate(b, 24 * TS, 3 * TS, 5 * TS, 3 * TS)
    label(b, '베이징 · 공사관 거리 (둥자오민샹)', 14 * TS, 11 * TS + 20, 12, back=(70, 30, 26, 230))
    flagx = {}
    for i, c in enumerate(codes):
        flagx[c] = 7 + i * 2
        m.ev('flag_' + c[:2], 7 + i * 2, 3, '!$c_flag_' + c)
    for (n, sp, dr), x in zip((('s_uk', '$c_sol_sikh', 'down'), ('s_us', '$c_sol_us00', 'down'), ('s_fr', '$c_sol_fr00', 'down'), ('s_de', '$c_sol_de00', 'down'),
                               ('s_ru', '$c_sol_ru00', 'down'), ('s_jp', '$c_sol_jp00', 'down'), ('s_it', '$c_sol_it00', 'down'), ('s_ah', '$c_sol_ah00', 'down')), range(8, 24, 2)):
        m.ev(n, x, 4, sp, dir=dr)
    m.ev('li', 10, 9, '$c_cn_m', dir='right')
    m.ev('scholar', 17, 10, '$c_cn_scholar', dir='left')
    m.ev('cnw', 9, 10, '$c_cn_w', dir='up')
    m.ev('cnkid', 11, 10, '$c_cn_kid', dir='left')
    m.ev('uk_sol', 15, 7, '$c_sol_uk00', dir='down')
    m.ev('looter', 18, 7, '$c_sol_de00', dir='right')
    m.ev('telegraph', 20, 10)
    m.ev('rubble', 8, 8)
    m.ev('exit', 14, 12, trigger=1)
    for (x, y, sp) in ((12, 6, '$c_sol_jp00'), (16, 9, '$c_sol_ru00'), (13, 8, '$c_cn_m2'), (19, 6, '$c_sol_us00')):
        m.ev('walker', x, y, sp, dir='down')
    m.save(root, vignette=0.14, warm=0.05)

# ==================================================================== 06 콜카타 거리 (1905년 10월 16일, 벵골 분할 날)
def calcutta(root):
    g = [list('P' * 29) for _ in range(13)]
    for y in range(0, 3):
        for x in range(29): g[y][x] = 'B'
    for y in range(6, 9):
        for x in range(29): g[y][x] = 'q'           # 길 (전차 선로)
    for y in range(3, 12):
        for x in list(range(0, 6)) + list(range(23, 29)): g[y][x] = 'B'
    for x in range(29): g[12][x] = 'B'
    for x in (13, 14, 15): g[12][x] = 'P'
    g[4][10] = 'x'                                  # 연설 단
    g[10][17] = g[10][18] = 'x'                     # 외국 옷감 태우는 불
    g[3][20] = 'x'; g[3][21] = 'x'                  # 신문 게시판
    m = Map('calcutta', 6, [''.join(r) for r in g], 'desert', 1905)
    b = m.big; d = ImageDraw.Draw(b)
    for y in range(0, 30): d.line([(0, y), (PW, y)], fill=mix((180, 196, 206), (232, 220, 196), y / 30))
    blds = [(0, 4, 'colonial', (214, 196, 160), None), (4, 3, 'colonial', (226, 206, 170), '면직물 상점'), (7, 4, 'colonial', (220, 180, 150), '스와데시 상점'),
            (11, 3, 'colonial', (230, 214, 180), None), (14, 4, 'colonial', (200, 170, 140), '서점'), (18, 6, 'london', (170, 70, 56), '중앙 전신국'), (24, 5, 'colonial', (220, 200, 166), None)]
    for (tx, tw, st, wc, shop) in blds:
        facade(b, tx * TS, 0, tw * TS, 3 * TS + 6, st, wc, seed=tx, shop=shop, shop_c=(60, 80, 40) if shop != '중앙 전신국' else (40, 40, 60), floors=3)
    # 길 · 전차 선로
    d.rectangle([0, 6 * TS, PW, 9 * TS - 1], fill=(170, 150, 120))
    for yy in (7 * TS + 6, 7 * TS + 30): d.line([(0, yy), (PW, yy)], fill=(110, 100, 90), width=3)
    for xx in range(0, PW, 18): d.line([(xx, 7 * TS + 2), (xx, 7 * TS + 34)], fill=(140, 120, 96), width=2)
    for yy in (6 * TS - 2, 9 * TS): d.rectangle([0, yy, PW, yy + 4], fill=(160, 150, 136))
    # 반얀나무
    for (x, y) in ((6, 10), (22, 10)): m.tree(x, y, 'mulberry', 1.3)
    # 연설 단 + 현수막
    with Prop(b, 9 * TS - 6, 4 * TS + 6, 2 * TS + 12, 40) as dd:
        dd.rectangle([0, 10, 2 * TS + 11, 34], fill=(150, 110, 70)); dd.rectangle([0, 8, 2 * TS + 11, 12], fill=(190, 150, 100))
    A.banner(b, 7 * TS, 13 * TS, 3 * TS + 18, '반데 마타람 (어머니 인도 만세)', col=(246, 236, 210), tcol=(150, 40, 30), size=13, poles=True, h=22)
    # 외국 옷감 태우는 불
    with Prop(b, 17 * TS - 4, 10 * TS - 10, 2 * TS + 8, 60) as dd:
        for k in range(8): dd.rectangle([6 + k * 10, 40 + (k % 2) * 4, 18 + k * 10, 52], fill=random.Random(k).choice([(240, 240, 236), (200, 60, 60), (60, 90, 160), (230, 210, 120)]))
        dd.polygon([(14, 46), (30, 4), (48, 40), (62, 10), (80, 46)], fill=(250, 150, 60)); dd.polygon([(26, 46), (36, 18), (46, 44), (60, 24), (70, 46)], fill=(255, 220, 120))
    glow(b, 18 * TS, 10 * TS + 10, 70, (255, 170, 80), 70)
    # 신문 게시판
    with Prop(b, 20 * TS - 4, 2 * TS + 22, 2 * TS + 8, 70) as dd:
        dd.rectangle([0, 0, 2 * TS + 7, 54], fill=(90, 66, 40)); dd.rectangle([4, 4, 2 * TS + 3, 50], fill=(236, 230, 210))
        dd.text((TS + 4, 12), '호외', font=F(12), fill=(170, 30, 30), anchor='mm')
        for yy in range(22, 48, 5): dd.line([(10, yy), (2 * TS - 2, yy)], fill=(100, 100, 100))
        dd.rectangle([8, 54, 12, 69], fill=(90, 66, 40)); dd.rectangle([2 * TS - 6, 54, 2 * TS - 2, 69], fill=(90, 66, 40))
    exit_path(b, 13, 15, 12 * TS + 2, '↓ 후글리강 부두', col=(170, 150, 120), edge=(130, 110, 86))
    label(b, '콜카타 · 1905년 10월 16일', 14 * TS, 11 * TS + 20, 12, back=(60, 40, 24, 230))
    m.ev('speaker', 9, 4, '$c_bn_stu', dir='down')
    m.ev('anand', 19, 4, '$c_anand', dir='down')
    m.ev('post', 20, 2, trigger=0)
    m.ev('board', 21, 3)
    m.ev('fire', 17, 10)
    m.ev('woman', 12, 10, '$c_bn_w', dir='left')
    m.ev('muslim', 15, 4, '$c_mus_m', dir='down')
    m.ev('official', 21, 9, '$c_raj_off', dir='left')
    m.ev('police', 20, 9, '$c_ind_pol', dir='left')
    m.ev('viet', 8, 10, '$c_viet', dir='right')
    m.ev('elder', 11, 4, '$c_bn_old', dir='down')
    for (x, y, sp) in ((8, 5, '$c_bn_m'), (10, 6, '$c_bn_m2'), (11, 5, '$c_bn_w2'), (12, 6, '$c_bn_m'), (8, 6, '$c_bn_stu'), (13, 5, '$c_bn_m2')):
        m.ev('crowd', x, y, sp, dir='up')
    for (x, y, sp) in ((16, 9, '$c_bn_m'), (13, 11, '$c_bn_w2')):
        m.ev('walker', x, y, sp, dir='left')
    m.ev('exit', 14, 12, trigger=1)
    m.save(root, vignette=0.12, warm=0.08)

# ==================================================================== 07 사라예보 아펠 강변길 (1914년 6월 28일)
def sarajevo(root):
    g = [list('P' * 29) for _ in range(13)]
    for y in range(0, 4):
        for x in range(29): g[y][x] = 'B'
    for y in range(6, 9):
        for x in range(29): g[y][x] = 'm'             # 차도
    for x in range(29):
        g[10][x] = 'W'; g[11][x] = 'W'; g[12][x] = 'W'
    for x in (16, 17): g[10][x] = 'P'; g[11][x] = 'P'; g[12][x] = 'P'     # 라틴 다리
    for y in range(4, 10):
        for x in list(range(0, 4)) + list(range(25, 29)): g[y][x] = 'B'
    g[4][21] = 'x'                                     # 우체국 앞 우체통
    m = Map('sarajevo', 7, [''.join(r) for r in g], 'versailles', 1914)
    b = m.big; d = ImageDraw.Draw(b)
    # 언덕과 첨탑 (멀리)
    for y in range(0, 50): d.line([(0, y), (PW, y)], fill=mix((160, 196, 226), (220, 226, 220), y / 50))
    d.polygon([(0, 50), (200, 10), (420, 40), (700, 8), (980, 36), (1200, 12), (PW, 40), (PW, 60), (0, 60)], fill=(120, 150, 110))
    for xx in (240, 1100):
        d.rectangle([xx, 4, xx + 8, 56], fill=(236, 232, 220)); d.polygon([(xx - 2, 6), (xx + 4, -10), (xx + 10, 6)], fill=(120, 130, 140))
    blds = [(0, 4, (226, 206, 160), None, 'hb'), (4, 3, (214, 196, 170), '카페', None), (7, 4, (236, 222, 186), None, 'hb'), (11, 3, (200, 210, 196), '시청 쪽', None),
            (14, 4, (230, 210, 170), '실러 식료품점', 'hb'), (18, 4, (220, 196, 160), '중앙 우체국', 'ah'), (22, 3, (236, 216, 180), None, 'hb'), (25, 4, (214, 200, 176), None, None)]
    for (tx, tw, wc, shop, fl) in blds:
        facade(b, tx * TS, 4, tw * TS, 4 * TS - 4, 'austro', wc, seed=tx, shop=shop, shop_c=(60, 50, 70), floors=3, flags=fl)
    d.rectangle([0, 6 * TS, PW, 9 * TS - 1], fill=(150, 146, 136))
    for xx in range(0, PW, 24): d.line([(xx, 6 * TS), (xx, 9 * TS)], fill=(140, 136, 126))
    for yy in (6 * TS - 3, 9 * TS): d.rectangle([0, yy, PW, yy + 4], fill=(200, 196, 186))
    # 강둑 난간
    d.rectangle([0, 9 * TS + 34, PW, 9 * TS + 44], fill=(206, 200, 186))
    for xx in range(0, PW, 16): d.rectangle([xx, 9 * TS + 26, xx + 4, 9 * TS + 34], fill=(206, 200, 186))
    # 라틴 다리 (돌 아치)
    with Prop(b, 15 * TS - 10, 10 * TS - 6, 4 * TS + 20, 3 * TS + 6) as dd:
        dd.rectangle([10, 0, 4 * TS + 10, 3 * TS + 5], fill=(196, 190, 176))
        for yy in range(6, 3 * TS, 10): dd.line([(10, yy), (4 * TS + 10, yy)], fill=(176, 170, 156))
        dd.rectangle([10, 0, 22, 3 * TS + 5], fill=(214, 208, 196)); dd.rectangle([4 * TS - 2, 0, 4 * TS + 10, 3 * TS + 5], fill=(214, 208, 196))
    label(b, '라틴 다리', 17 * TS, 12 * TS + 20, 11, back=(60, 50, 40, 220))
    label(b, '아펠 강변길 · 밀랴츠카강', 7 * TS, 9 * TS + 20, 11, back=(40, 50, 60, 220))
    for (x, y) in ((5, 9), (11, 9), (22, 9)): m.tree(x, y, 'poplar', 0.8)
    m.ev('post', 20, 3)
    m.ev('postbox', 21, 4)
    m.ev('milan', 13, 5, '$c_bos_stu', dir='down')
    m.ev('emina', 9, 5, '$c_bos_w', dir='down')
    m.ev('ahoff', 22, 5, '$c_ah_off', dir='down')
    m.ev('merchant', 6, 5, '$c_bos_mus', dir='down')
    m.ev('policeman', 16, 9, '$c_ah_pol', dir='up')
    for (x, y, sp) in ((5, 5, '$c_bos_cit'), (7, 5, '$c_bos_w'), (8, 5, '$c_bos_mus'), (11, 5, '$c_bos_cit'), (12, 5, '$c_bos_w'), (15, 5, '$c_bos_mus'), (17, 5, '$c_bos_cit'),
                       (19, 5, '$c_bos_w'), (21, 5, '$c_bos_mus'), (23, 5, '$c_bos_cit'), (6, 9, '$c_bos_cit'), (9, 9, '$c_bos_w'), (13, 9, '$c_bos_mus'), (20, 9, '$c_bos_w'), (23, 9, '$c_bos_cit')):
        m.ev('crowd', x, y, sp, dir='down' if y == 5 else 'up')
    m.ev('car', 4, 7, '!$c_car_ff', dir='right', through=True)
    m.ev('car0', 1, 7, '!$c_car2', dir='right', through=True)
    m.ev('smoke', 10, 7, '!$c_gas', priority=2, through=True, anime=True)
    m.save(root, vignette=0.12, warm=0.06)

# ==================================================================== 08 런던 거리 (1914년 8월 / 1917년 / 1918년 11월 11일)
def london(root):
    g = [list('P' * 29) for _ in range(13)]
    for y in range(0, 3):
        for x in range(29): g[y][x] = 'B'
    for y in range(6, 10):
        for x in range(29): g[y][x] = 'm'
    for y in range(3, 12):
        for x in list(range(0, 6)) + list(range(23, 29)): g[y][x] = 'B'
    for x in range(29): g[12][x] = 'B'
    for x in (13, 14, 15): g[12][x] = 'P'
    g[10][9] = 'x'; g[10][19] = 'x'                 # 가로등
    m = Map('london', 8, [''.join(r) for r in g], 'paris', 1914)
    base = m.big.copy()

    def draw(b, era):
        d = ImageDraw.Draw(b)
        for y in range(0, 30): d.line([(0, y), (PW, y)], fill=mix((150, 160, 176), (200, 200, 196), y / 30) if era != '18' else mix((170, 180, 196), (220, 214, 200), y / 30))
        # 멀리 빅벤
        d.rectangle([24 * TS + 20, -10, 24 * TS + 46, 40], fill=(170, 150, 110)); d.ellipse([24 * TS + 24, 4, 24 * TS + 42, 22], fill=(236, 230, 210))
        shops14 = [(0, 4, None), (4, 3, '신병 모집소'), (7, 3, '식료품점'), (10, 4, '은행'), (14, 3, '약국'), (17, 3, '찻집'), (20, 3, '신문사'), (23, 3, None), (26, 3, None)]
        shops17 = [(0, 4, None), (4, 3, '군수부 사무소'), (7, 3, '식료품점'), (10, 4, '은행'), (14, 3, '약국'), (17, 3, '찻집'), (20, 3, '신문사'), (23, 3, None), (26, 3, None)]
        for (tx, tw, shop) in (shops14 if era == '14' else shops17):
            wc = random.Random(tx + 3).choice([(150, 92, 72), (160, 100, 80), (196, 188, 170), (140, 86, 70)])
            facade(b, tx * TS, 0, tw * TS, 3 * TS + 8, 'london' if wc[0] < 180 else 'stone', wc, seed=tx, shop=shop,
                   shop_c=(150, 30, 30) if shop in ('신병 모집소',) else (40, 60, 50), floors=3, awning=(40, 90, 60) if shop == '식료품점' else None)
        # 길
        d.rectangle([0, 6 * TS, PW, 10 * TS - 1], fill=(90, 88, 86))
        rr = random.Random(5)
        for _ in range(900):
            x, y = rr.randint(0, PW - 1), rr.randint(6 * TS, 10 * TS - 2)
            d.point((x, y), fill=rr.choice([(80, 78, 76), (100, 98, 96)]))
        for yy in (6 * TS - 3, 10 * TS): d.rectangle([0, yy, PW, yy + 4], fill=(170, 166, 156))
        for xx in range(0, PW, 64): d.rectangle([xx, 8 * TS - 2, xx + 30, 8 * TS + 1], fill=(220, 214, 196))
        for (x, y) in ((9, 10), (19, 10)):
            A.pole(b, x * TS + 24, y * TS + 44, 140, lamp=True)
        # 포스터 · 시대 표시
        def poster(x, y, kind):
            with Prop(b, x, y, 34, 46) as dd:
                dd.rectangle([0, 0, 33, 45], fill=(236, 226, 196), outline=(80, 70, 60))
                if kind == 'k':
                    dd.ellipse([10, 4, 24, 18], fill=(220, 180, 150)); dd.rectangle([8, 2, 26, 7], fill=(70, 60, 50)); dd.line([(12, 14), (22, 14)], fill=(70, 40, 30), width=2)
                    dd.rectangle([6, 19, 28, 28], fill=(130, 110, 80)); dd.rectangle([4, 32, 30, 34], fill=(170, 30, 30)); dd.rectangle([6, 37, 28, 39], fill=(30, 30, 30))
                elif kind == 'w':
                    dd.rectangle([0, 0, 33, 10], fill=(40, 70, 130)); dd.ellipse([12, 13, 22, 23], fill=(236, 200, 170)); dd.rectangle([10, 23, 24, 40], fill=(190, 170, 120))
                elif kind == 'f':
                    dd.rectangle([0, 0, 33, 10], fill=(60, 110, 60)); dd.text((17, 26), '빵을\n아끼자', font=F(8), fill=(40, 40, 40), anchor='mm', align='center')
                elif kind == 'b':
                    dd.rectangle([0, 0, 33, 10], fill=(170, 30, 30)); dd.text((17, 26), '전쟁\n채권', font=F(8), fill=(40, 40, 40), anchor='mm', align='center')
        if era == '14':
            for x in (4 * TS + 6, 5 * TS + 40, 11 * TS + 8): poster(x, 2 * TS + 30, 'k')
            A.banner(b, 4 * TS, 7 * TS, 2 * TS + 10, '지원병 모집', col=(240, 236, 226), tcol=(150, 20, 20), size=12, poles=False, h=18)
        elif era == '17':
            for (x, k) in ((4 * TS + 6, 'w'), (5 * TS + 40, 'b'), (8 * TS + 30, 'f'), (11 * TS + 8, 'w'), (15 * TS, 'b')): poster(x, 2 * TS + 30, k)
            d.rectangle([20 * TS, 0, 23 * TS, 26], fill=(110, 100, 90))
            label(b, '공습 대피소 →', 21 * TS, 4 * TS + 30, 10, back=(140, 30, 30, 220))
        else:
            for k in range(29):
                x = k * TS + 24
                col = [(200, 30, 40), (250, 250, 250), (30, 50, 130)][k % 3]
                d.polygon([(x - 12, 3 * TS + 12), (x + 12, 3 * TS + 12), (x, 3 * TS + 30)], fill=col)
            d.line([(0, 3 * TS + 12), (PW, 3 * TS + 12)], fill=(80, 70, 60), width=2)
            for x in (8 * TS, 12 * TS, 16 * TS, 20 * TS):
                fl = FL.waving('uk', 40, 20, 0.08, x); b.alpha_composite(fl, (x, 2 * TS + 26))
        exit_path(b, 13, 15, 12 * TS + 2, '↓ 전신국으로', col=(150, 146, 136), edge=(110, 106, 100))
        label(b, {'14': '런던 · 1914년 8월', '17': '런던 · 1917년', '18': '런던 · 1918년 11월 11일'}[era], 14 * TS, 11 * TS + 20, 12, back=(60, 40, 24, 230))
    for era in ('14', '17', '18'):
        b = base.copy(); draw(b, era)
        G.finish(b, m.grid, vignette=0.12, warm={'14': 0.03, '17': -0.03, '18': 0.04}[era])
        save_variant(root, '!c_london' + era, b)
    m.ev('exit', 14, 12, trigger=1)
    m.ev('recruit_off', 5, 3)
    m.ev('sergeant', 6, 4, '$c_sergeant', dir='down')
    m.ev('mary', 12, 4, '$c_mary', dir='down')
    m.ev('sam', 13, 4, '$c_sam13', dir='down')
    m.ev('newsboy', 16, 10, '$c_newsboy', dir='left')
    m.ev('bobby', 21, 4, '$c_bobby', dir='down')
    m.ev('suffrage', 17, 4, '$c_suffrage', dir='down')
    for (x, y, sp) in ((7, 5, '$c_recruit'), (8, 5, '$c_recruit2'), (9, 5, '$c_recruit3'), (10, 5, '$c_recruit'), (11, 5, '$c_recruit2')):
        m.ev('queue14', x, y, sp, dir='left')
    for (x, y, sp) in ((6, 7, '$c_tommy14'), (7, 8, '$c_tommy14b'), (5, 7, '$c_tommy14'), (4, 8, '$c_tommy14b'), (3, 7, '$c_tommy14'), (2, 8, '$c_tommy14b')):
        m.ev('march', x, y, sp, dir='right', through=True)
    for (x, y, sp) in ((14, 5, '$c_lon_w'), (15, 5, '$c_lon_old'), (18, 5, '$c_lon_w2'), (20, 5, '$c_lon_kid')):
        m.ev('cheer14', x, y, sp, dir='down')
    # 1917
    m.ev('grocer', 8, 3, '$c_grocer', dir='down')
    for (x, y, sp) in ((9, 4, '$c_queue_w'), (10, 4, '$c_queue_old'), (11, 4, '$c_queue_w'), (12, 4, '$c_lon_kid'), (13, 4, '$c_queue_old')):
        m.ev('queue17', x, y, sp, dir='left')
    m.ev('house1', 18, 2); m.ev('house2', 21, 2); m.ev('house3', 15, 2)
    m.ev('widow', 18, 3, '$c_widow', dir='down')
    m.ev('tram_w', 17, 9, '$c_tram_w', dir='left')
    m.ev('clc', 11, 10, '$c_clc', dir='up')
    m.ev('wounded', 7, 10, '$c_tommy16', dir='right')
    # 1918
    for (x, y, sp) in ((8, 6, '$c_cheer_m'), (10, 7, '$c_cheer_w'), (12, 8, '$c_sailor'), (15, 7, '$c_cheer_k'), (17, 6, '$c_cheer_w'), (19, 8, '$c_cheer_m'), (9, 9, '$c_tommy16'),
                       (13, 6, '$c_lon_w'), (20, 7, '$c_sailor'), (16, 9, '$c_cheer_k')):
        m.ev('party', x, y, sp, dir='down', through=True)
    m.ev('bus', 26, 8, '!$c_bus', dir='left', through=True)
    m.ev('cart', 1, 7, '!$c_horse', dir='right', through=True)
    m.save(root, parallax_name='!c_london14', image=False)

ALL2 = [beijing, calcutta, sarajevo, london]
