"""전보 소년 지도 1: 01 런던 국제 전신국 · 02 베를린 회의장 · 03 아드와 · 04 콩고 고무 채취소"""
from k_mapbase import *
import k_arch as A
import k_flags as FL
import k_geo as GEO

WOOD = (120, 80, 50); WOOD_D = (84, 56, 36); BRASS = (206, 170, 90)

def panel_wall(b, x0, x1, y1, upper=(226, 214, 186), lower=(110, 72, 46), rail=(150, 106, 64), stripe=True):
    d = ImageDraw.Draw(b)
    d.rectangle([x0, 0, x1, y1], fill=upper)
    if stripe:
        for xx in range(x0, x1, 14): d.line([(xx, 0), (xx, y1 - 50)], fill=sh(upper, 0.96))
    d.rectangle([x0, y1 - 48, x1, y1], fill=lower)
    for xx in range(x0 + 6, x1 - 30, 54):
        d.rectangle([xx, y1 - 42, xx + 44, y1 - 8], outline=sh(lower, 0.8), width=2)
        d.line([(xx + 2, y1 - 40), (xx + 42, y1 - 40)], fill=sh(lower, 1.2))
    d.rectangle([x0, y1 - 52, x1, y1 - 46], fill=rail)
    d.rectangle([x0, y1 - 4, x1, y1], fill=sh(lower, 0.7))

def side_walls(b, col=(110, 76, 50), x_left=6, x_right=22, bottom=True, door_x=14):
    d = ImageDraw.Draw(b)
    for x in (x_left, x_right):
        d.rectangle([x * TS, 0, x * TS + TS - 1, PH - 1], fill=col)
        edge = x * TS + (TS - 10 if x == x_left else 0)
        d.rectangle([edge, 0, edge + 9, PH - 1], fill=sh(col, 1.25))
    if bottom:
        d.rectangle([x_left * TS, 12 * TS, (x_right + 1) * TS - 1, PH - 1], fill=col)
        d.rectangle([(door_x - 1) * TS + 6, 12 * TS, (door_x + 2) * TS - 6, PH - 1], fill=sh(col, 0.7))
        d.rectangle([(door_x - 1) * TS + 10, 12 * TS + 4, (door_x + 2) * TS - 10, PH - 1], fill=(200, 210, 210))
        d.line([(door_x * TS + 24, 12 * TS + 4), (door_x * TS + 24, PH)], fill=sh(col, 0.7), width=3)

def world_cable_map(w, h, year=1900, cables=True):
    """세계 지도 + 영국 해저 전신선 (붉은 선)"""
    box = (-140, 160, -45, 72)
    im, pj = GEO.render(year, box, (w, h), line_w=0.6, paper=True, seed=year)
    d = ImageDraw.Draw(im)
    if cables:
        routes = [[(-0.1, 51.5), (-5.7, 50.1), (-9.2, 38.7), (-5.4, 36.1), (14.5, 35.9), (29.9, 31.2), (32.5, 29.9), (45.0, 12.8), (72.8, 19.0)],
                  [(72.8, 19.0), (80.2, 13.1), (103.8, 1.3), (114.2, 22.3), (121.5, 31.2)],
                  [(-10.3, 51.9), (-30, 52), (-53.0, 47.6)], [(-53.0, 47.6), (-70.0, 42.0), (-74.0, 40.7)],
                  [(-9.2, 38.7), (-17.0, 14.7), (-13.2, 8.5), (3.4, 6.4), (9.7, 4.0), (12.3, -6.0), (13.2, -8.8), (18.4, -33.9)],
                  [(45.0, 12.8), (39.3, -6.8), (32.6, -25.9), (31.0, -29.9), (18.4, -33.9)], [(103.8, 1.3), (106.8, -6.2), (130.8, -12.4), (151.2, -33.9)]]
        for r in routes: GEO.polyline(d, pj, r, col=(180, 30, 30), w=1)
        for (lo, la) in ((-0.1, 51.5), (72.8, 19.0), (121.5, 31.2), (-74.0, 40.7), (18.4, -33.9), (151.2, -33.9), (29.9, 31.2)):
            x, y = pj(lo, la); d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(150, 20, 20))
    return im

def morse_desk(d, x, y, w, era):
    """전신 책상: 나무 책상 + 송신 키 + 수신기(사운더) + 종이 테이프"""
    d.rectangle([x, y + 10, x + w, y + 34], fill=WOOD); d.rectangle([x, y + 8, x + w, y + 12], fill=sh(WOOD, 1.25))
    d.rectangle([x, y + 34, x + w, y + 38], fill=WOOD_D)
    for k in range(int(w // 56)):
        kx = x + 14 + k * 56
        d.rectangle([kx, y - 2, kx + 18, y + 8], fill=(60, 50, 40)); d.rectangle([kx + 2, y - 8, kx + 16, y - 2], fill=BRASS)   # 사운더
        d.line([(kx + 24, y + 4), (kx + 40, y + 2)], fill=BRASS, width=2); d.ellipse([kx + 36, y - 2, kx + 44, y + 4], fill=(30, 30, 30))   # 키
        d.rectangle([kx + 22, y + 14, kx + 46, y + 18], fill=(244, 238, 220))   # 테이프
        if era in ('14', '17'):
            d.rectangle([kx - 4, y + 16, kx + 14, y + 28], fill=(40, 40, 44)); d.rectangle([kx - 2, y + 12, kx + 12, y + 16], fill=(230, 226, 214))   # 타자기
    d.rectangle([x + 4, y + 38, x + 10, y + 46], fill=WOOD_D); d.rectangle([x + w - 10, y + 38, x + w - 4, y + 46], fill=WOOD_D)

def office(root):
    g = [list('BBBBBB' + 'f' * 17 + 'BBBBBB') for _ in range(13)]
    for y in range(3, 12):
        for x in range(7, 22): g[y][x] = 'o'
    for x in range(8, 13): g[5][x] = 'x'             # 전신 책상
    g[5][13] = 'x'                                     # 연습용 키
    g[7][17] = g[7][18] = 'x'                          # 국장 책상
    g[3][20] = g[3][21] = 'x'                          # 전보철 장
    g[10][7] = g[10][8] = 'x'                          # 배달 소년 걸상
    g[11][21] = 'x'
    m = Map('office', 1, [''.join(r) for r in g], 'paris', 3)
    base = m.big.copy()
    dark_out(base, 0, 6, col=(30, 26, 24)); dark_out(base, 23, 29, col=(30, 26, 24))
    maps = {yr: world_cable_map(250, 112, yr) for yr in (1880, 1900, 1914)}

    def draw(b, era):
        d = ImageDraw.Draw(b)
        panel_wall(b, 6 * TS, 23 * TS - 1, 3 * TS - 1, upper={'84': (214, 200, 168), '00': (222, 210, 180), '14': (214, 210, 196), '17': (206, 200, 186)}[era])
        side_walls(b, (110, 76, 50))
        # 세계 해저 전신선 지도
        mp = maps[{'84': 1880, '00': 1900, '14': 1914, '17': 1914}[era]]
        X0, Y0 = 7 * TS - 6, 8
        d.rectangle([X0 - 6, Y0 - 6, X0 + mp.width + 5, Y0 + mp.height + 5], fill=(110, 76, 40)); d.rectangle([X0 - 3, Y0 - 3, X0 + mp.width + 2, Y0 + mp.height + 2], fill=(200, 160, 90))
        b.paste(mp, (X0, Y0))
        label(b, '대영 제국 해저 전신망', X0 + mp.width // 2, Y0 + mp.height + 14, 11, back=(60, 40, 24, 230))
        # 시계
        cx_, cy_ = 15 * TS + 24, 52
        d.ellipse([cx_ - 26, cy_ - 26, cx_ + 26, cy_ + 26], fill=(90, 60, 36)); d.ellipse([cx_ - 21, cy_ - 21, cx_ + 21, cy_ + 21], fill=(246, 242, 228))
        for k in range(12):
            a = k * math.pi / 6; d.line([(cx_ + math.cos(a) * 17, cy_ + math.sin(a) * 17), (cx_ + math.cos(a) * 20, cy_ + math.sin(a) * 20)], fill=(40, 40, 40), width=2)
        d.line([(cx_, cy_), (cx_ + 10, cy_ - 6)], fill=(20, 20, 20), width=3); d.line([(cx_, cy_), (cx_ - 3, cy_ - 16)], fill=(20, 20, 20), width=2)
        d.text((cx_, cy_ + 34), 'G.M.T.', font=F(10), fill=(60, 40, 30), anchor='mm')
        # 압축 공기 관 (기송관)
        for k, xx in enumerate((17 * TS + 30, 18 * TS + 6, 18 * TS + 26)):
            d.rectangle([xx, 0, xx + 9, 2 * TS + 20], fill=BRASS); d.line([(xx + 2, 0), (xx + 2, 2 * TS + 20)], fill=sh(BRASS, 1.3))
            d.rectangle([xx - 3, 2 * TS + 14, xx + 12, 2 * TS + 30], fill=sh(BRASS, 0.75))
        d.rectangle([17 * TS + 20, 2 * TS + 30, 19 * TS + 4, 2 * TS + 40], fill=WOOD)
        # 전보철 장 (칸칸이 꽂힌 전보)
        with Prop(b, 20 * TS - 2, TS + 6, 2 * TS + 4, 2 * TS + 34) as dd:
            dd.rectangle([0, 0, 2 * TS + 3, 2 * TS + 33], fill=WOOD_D); dd.rectangle([3, 3, 2 * TS, 2 * TS + 30], fill=(70, 46, 30))
            for r in range(5):
                for c in range(4):
                    x0, y0 = 6 + c * 22, 6 + r * 23
                    dd.rectangle([x0, y0, x0 + 18, y0 + 19], fill=(56, 36, 24))
                    if (r * 4 + c) % 3 != 1: dd.rectangle([x0 + 2, y0 + 6, x0 + 16, y0 + 18], fill=(246, 228, 170))
            dd.text((TS + 1, 2 * TS + 26), '전보철', font=F(11), fill=(250, 230, 180), anchor='mm')
        # 등
        if era == '84':
            for xx in (9 * TS, 13 * TS, 19 * TS):
                d.line([(xx, 2 * TS - 6), (xx + 10, 2 * TS - 20)], fill=BRASS, width=2); d.ellipse([xx + 4, 2 * TS - 34, xx + 18, 2 * TS - 18], fill=(250, 220, 150))
                glow(b, xx + 11, 2 * TS - 26, 40, (255, 200, 120), 70)
        else:
            for xx in (10 * TS, 14 * TS, 18 * TS):
                d.line([(xx, 0), (xx, 3 * TS + 10)], fill=(50, 50, 50)); d.polygon([(xx - 12, 3 * TS + 10), (xx + 12, 3 * TS + 10), (xx + 6, 3 * TS + 2), (xx - 6, 3 * TS + 2)], fill=(40, 90, 60))
        # 책상들
        morse_desk(d, 8 * TS + 2, 5 * TS - 4, 5 * TS - 4, era)
        with Prop(b, 13 * TS + 4, 5 * TS + 4, 40, 36) as dd:
            dd.rectangle([0, 8, 39, 30], fill=WOOD); dd.rectangle([0, 6, 39, 10], fill=sh(WOOD, 1.25))
            dd.line([(8, 4), (26, 2)], fill=BRASS, width=2); dd.ellipse([22, -2, 30, 6], fill=(20, 20, 20))
            dd.text((20, 20), '연습', font=F(9), fill=(250, 230, 190), anchor='mm')
        with Prop(b, 17 * TS - 2, 7 * TS - 2, 2 * TS + 4, 44) as dd:
            dd.rectangle([0, 8, 2 * TS + 3, 34], fill=(100, 64, 40)); dd.rectangle([0, 6, 2 * TS + 3, 10], fill=(150, 104, 66))
            dd.rectangle([6, 36, 12, 43], fill=WOOD_D); dd.rectangle([2 * TS - 8, 36, 2 * TS - 2, 43], fill=WOOD_D)
            dd.rectangle([10, 0, 34, 8], fill=(244, 236, 214)); dd.rectangle([52, -4, 58, 8], fill=(40, 90, 60))
            dd.ellipse([46, -10, 64, 0], fill=(60, 110, 70) if era != '84' else (250, 220, 150))
            if era in ('14', '17'):
                dd.rectangle([70, -2, 80, 8], fill=(30, 30, 30)); dd.line([(72, -6), (78, -6)], fill=(30, 30, 30), width=3)   # 전화기
        with Prop(b, 7 * TS - 2, 10 * TS + 8, 2 * TS + 4, 34) as dd:
            dd.rectangle([0, 4, 2 * TS + 3, 16], fill=WOOD); dd.rectangle([0, 0, 2 * TS + 3, 4], fill=sh(WOOD, 1.3))
            dd.rectangle([4, 16, 10, 30], fill=WOOD_D); dd.rectangle([2 * TS - 6, 16, 2 * TS, 30], fill=WOOD_D)
        label(b, '배달 소년 대기석', 8 * TS, 10 * TS + 2, 10, back=(60, 40, 24, 220))
        G.bush(b, 21, 11, 24, 40, 0.8)
        # 시대 표시
        if era in ('14', '17'):
            with Prop(b, 15 * TS + 10, 10, 2 * TS - 10, 76) as dd:
                dd.rectangle([0, 0, 2 * TS - 11, 75], fill=(236, 226, 196), outline=(80, 70, 60))
                if era == '14':
                    dd.ellipse([22, 10, 46, 34], fill=(220, 180, 150)); dd.rectangle([20, 6, 48, 14], fill=(70, 60, 50)); dd.line([(26, 26), (42, 26)], fill=(70, 40, 30), width=3)
                    dd.rectangle([14, 36, 54, 52], fill=(130, 110, 80)); dd.text((34, 62), 'YOUR COUNTRY', font=F(7), fill=(150, 20, 20), anchor='mm'); dd.text((34, 70), 'NEEDS YOU', font=F(7), fill=(20, 20, 20), anchor='mm')
                else:
                    dd.rectangle([0, 0, 2 * TS - 11, 18], fill=(40, 70, 130)); dd.text((34, 9), 'WOMEN', font=F(9), fill=(255, 255, 255), anchor='mm')
                    dd.ellipse([24, 22, 42, 40], fill=(236, 200, 170)); dd.rectangle([20, 40, 46, 66], fill=(190, 170, 120))
            if era == '17':
                fl = FL.flag('uk', 50, 25)
                for xx in (8 * TS, 12 * TS): b.alpha_composite(fl, (xx, 2 * TS + 8))
        cal = {'84': '1884', '00': '1900', '14': '1914', '17': '1917'}[era]
        with Prop(b, 14 * TS - 18, 2 * TS + 8, 30, 34) as dd:
            dd.rectangle([0, 0, 29, 33], fill=(246, 244, 236)); dd.rectangle([0, 0, 29, 10], fill=(150, 30, 30))
            dd.text((15, 5), cal, font=F(8), fill=(255, 255, 255), anchor='mm')
            for yy in range(14, 31, 5): dd.line([(4, yy), (25, yy)], fill=(150, 150, 150))
        label(b, '런던 국제 전신국', 14 * TS, 12 * TS + 12, 12, back=(60, 40, 24, 230))
    for era in ('84', '00', '14', '17'):
        b = base.copy(); draw(b, era)
        G.finish(b, m.grid, vignette=0.12, ao=0.25, warm={'84': 0.1, '00': 0.06, '14': 0.03, '17': 0.0}[era])
        save_variant(root, '!c_office' + era, b)
    m.ev('door', 14, 12, trigger=1)
    m.ev('file', 20, 3)
    m.ev('wallmap', 10, 2)
    m.ev('clock', 15, 2)
    m.ev('tube', 18, 2)
    m.ev('key', 13, 5)
    m.ev('desk', 17, 7)
    m.ev('hardy', 17, 6, '$c_hardy', dir='down')
    m.ev('editor', 16, 9, '$c_editor', dir='left')
    m.ev('clerk1', 9, 4, '$c_clerk_f', dir='down')
    m.ev('clerk2', 11, 4, '$c_clerk_m', dir='down')
    m.ev('clerk3', 12, 4, '$c_clerk_f2', dir='down')
    m.ev('boy1', 8, 9, '$c_boy_m', dir='down')
    m.ev('sam', 12, 9, '$c_sam13', dir='down')
    m.ev('sam17', 12, 9, '$c_sam16', dir='down')
    m.ev('mary', 11, 9, '$c_mary', dir='right')
    m.ev('will_npc', 15, 6, '$c_will47', dir='down')
    m.save(root, parallax_name='!c_office84', image=False)

# ==================================================================== 02 베를린 회의장 (1884년 11월 15일, 빌헬름 거리 77번지 총리 관저)
def berlin(root):
    g = [list('BBBBBB' + 'f' * 17 + 'BBBBBB') for _ in range(13)]
    for y in range(3, 12):
        for x in range(7, 22): g[y][x] = 'z'
    for x in range(10, 19):
        g[6][x] = 'x'; g[7][x] = 'x'                     # 긴 회의 탁자
    for (x, y) in ((7, 3), (21, 3)): g[y][x] = 'x'      # 화분 · 난로
    m = Map('berlin', 2, [''.join(r) for r in g], 'versailles', 7)
    b = m.big; d = ImageDraw.Draw(b)
    dark_out(b, 0, 6, col=(34, 28, 26)); dark_out(b, 23, 29, col=(34, 28, 26))
    panel_wall(b, 6 * TS, 23 * TS - 1, 3 * TS - 1, upper=(150, 40, 46), lower=(220, 210, 186), rail=(214, 182, 100), stripe=False)
    for xx in range(6 * TS, 23 * TS, 18): d.line([(xx, 0), (xx, 2 * TS - 4)], fill=(140, 34, 40))
    side_walls(b, (210, 196, 170))
    # 큰 아프리카 지도 (1884년 무렵: 해안만 차지하고 안쪽은 '빈 땅'처럼 그려진 지도)
    am, pj = GEO.render(1880, (-20, 55, -37, 38), (176, 128), line_w=0.5, seed=84)
    X0, Y0 = 14 * TS + 24 - 88, 6
    d.rectangle([X0 - 8, Y0 - 4, X0 + 184, Y0 + 134], fill=(150, 110, 50)); d.rectangle([X0 - 4, Y0 - 1, X0 + 180, Y0 + 131], fill=(214, 184, 110))
    b.paste(am, (X0, Y0))
    label(b, '아프리카 지도', 14 * TS + 24, Y0 + 140, 11, back=(70, 40, 24, 230))
    # 창문 + 커튼
    for xx in (7 * TS + 8, 18 * TS + 34):
        d.rectangle([xx, 14, xx + 60, 2 * TS + 20], fill=(170, 190, 200)); d.rectangle([xx + 28, 14, xx + 32, 2 * TS + 20], fill=(230, 220, 200))
        d.line([(xx, 2 * TS - 20), (xx + 60, 2 * TS - 20)], fill=(230, 220, 200), width=3)
        d.polygon([(xx - 10, 6), (xx + 10, 6), (xx + 4, 2 * TS + 30), (xx - 12, 2 * TS + 30)], fill=(120, 30, 36))
        d.polygon([(xx + 50, 6), (xx + 70, 6), (xx + 72, 2 * TS + 30), (xx + 56, 2 * TS + 30)], fill=(120, 30, 36))
    # 회의 탁자 (초록 천)
    soft_shadow(b, [10 * TS, 8 * TS - 6, 19 * TS + 6, 8 * TS + 6], 100, 5)
    with Prop(b, 10 * TS - 4, 6 * TS - 6, 9 * TS + 8, 2 * TS + 14) as dd:
        dd.rounded_rectangle([0, 0, 9 * TS + 7, 2 * TS + 4], 8, fill=(40, 96, 66)); dd.rounded_rectangle([4, 4, 9 * TS + 3, 2 * TS], 6, fill=(54, 120, 80))
        dd.rectangle([0, 2 * TS + 4, 9 * TS + 7, 2 * TS + 13], fill=(90, 60, 36))
        rnd = random.Random(84)
        for k in range(14):
            x0 = 20 + k * 30
            dd.rectangle([x0, 14 + (k % 2) * 40, x0 + 18, 30 + (k % 2) * 40], fill=(246, 240, 224)); dd.line([(x0 + 3, 20 + (k % 2) * 40), (x0 + 14, 20 + (k % 2) * 40)], fill=(90, 90, 90))
            if k % 4 == 0: dd.rectangle([x0 + 22, 18 + (k % 2) * 40, x0 + 26, 28 + (k % 2) * 40], fill=(30, 30, 40))
        # 탁자 위에 펼친 아프리카 지도
        sm, _ = GEO.render(1880, (-20, 55, -37, 38), (64, 64), line_w=0.4, paper=False)
        dd._image.paste(sm, (4 * TS + 8, 18))
    # 14개 나라 깃발 (벽을 따라)
    codes = ['de', 'ah', 'be', 'dk', 'es', 'us38', 'fr', 'uk', 'it', 'nl', 'pt', 'ru', 'se', 'ot']
    for i, c in enumerate(codes):
        x = 6 * TS + 18 + i * 54 + (90 if i >= 7 else 0)
        if 11 * TS < x < 18 * TS: x += 0
        if i < 7: x = 7 * TS + 2 + i * 29
        else: x = 17 * TS + 26 + (i - 7) * 29
        fl = FL.flag(c, 26, 17)
        d.line([(x - 2, 2 * TS + 20), (x - 2, 2 * TS + 44)], fill=(150, 120, 60), width=2)
        b.alpha_composite(fl, (x, 2 * TS + 24))
    # 샹들리에 (인물 위 층)
    top = m.top; td = ImageDraw.Draw(top)
    for xx in (11 * TS, 17 * TS + 24):
        td.line([(xx, 0), (xx, 40)], fill=(200, 170, 90), width=2)
        td.ellipse([xx - 34, 34, xx + 34, 54], fill=(214, 182, 100, 255)); td.ellipse([xx - 28, 38, xx + 28, 50], fill=(240, 220, 160, 255))
        for k in range(7):
            cx_ = xx - 30 + k * 10; td.rectangle([cx_, 26, cx_ + 2, 36], fill=(250, 246, 230, 255)); td.ellipse([cx_ - 1, 20, cx_ + 3, 26], fill=(255, 220, 120, 255))
        glow(b, xx, 40, 70, (255, 220, 150), 60)
    b.alpha_composite(top)
    for (x, y) in ((7, 3),):
        G.bush(b, x, y, 24, 40, 0.9)
    with Prop(b, 21 * TS + 6, 2 * TS + 20, 36, 70) as dd:            # 사기 난로
        dd.rounded_rectangle([2, 0, 34, 66], 6, fill=(236, 232, 220)); dd.rectangle([8, 40, 28, 58], fill=(60, 50, 40))
        for yy in range(8, 38, 8): dd.line([(4, yy), (32, yy)], fill=(200, 196, 186))
    label(b, '베를린 · 독일 제국 총리 관저', 14 * TS, 12 * TS + 12, 12, back=(60, 30, 30, 230))
    side_walls(b, (210, 196, 170), bottom=True)
    m.ev('door', 14, 12, trigger=1)
    m.ev('mapwall', 14, 2)
    m.ev('table', 14, 7)
    m.ev('bismarck', 14, 5, '$c_bismarck', dir='down')
    for (n, x, y, sp, dr) in (('dlg_uk', 10, 5, '$c_dlg_uk', 'down'), ('dlg_fr', 12, 5, '$c_dlg_fr', 'down'), ('dlg_pt', 16, 5, '$c_dlg_pt', 'down'),
                              ('dlg_be', 18, 5, '$c_dlg_be', 'down'), ('dlg_us', 11, 8, '$c_dlg_us', 'up'), ('dlg_ot', 13, 8, '$c_dlg_ot', 'up'),
                              ('dlg_ru', 15, 8, '$c_dlg_ru', 'up'), ('dlg_x', 17, 8, '$c_dlg_x', 'up'), ('dlg_de', 19, 7, '$c_dlg_de', 'left')):
        m.ev(n, x, y, sp, dir=dr)
    m.ev('footman', 8, 9, '$c_footman', dir='right')
    m.ev('guard1', 12, 11, '$c_guard_de', dir='up'); m.ev('guard2', 16, 11, '$c_guard_de', dir='up')
    m.ev('stove', 21, 3)
    m.save(root, vignette=0.14, warm=0.06)

# ==================================================================== 03 아드와 (1896년 3월, 에티오피아군 진영)
def eth_tent(b, x, y, w=120, h=78, col=(244, 240, 226), band=(180, 40, 40), royal=False):
    soft_shadow(b, [x + 4, y + h - 8, x + w + 8, y + h + 6], 90, 5)
    with Prop(b, x, y, w, h + 4) as d:
        d.polygon([(0, h), (w / 2, 4), (w, h)], fill=col)
        d.polygon([(w / 2, 4), (w, h), (w * 0.62, h)], fill=sh(col, 0.85))
        for k in range(1, 4):
            t = k / 4
            d.line([(w / 2 - w / 2 * t, 4 + (h - 4) * t), (w / 2 + w / 2 * t, 4 + (h - 4) * t)], fill=band, width=3 if royal else 2)
        d.polygon([(w / 2 - 10, h), (w / 2, h - 30), (w / 2 + 10, h)], fill=(60, 40, 30))
        d.line([(w / 2, 4), (w / 2, 0)], fill=(120, 90, 50), width=2)
        if royal:
            d.ellipse([w / 2 - 5, -2, w / 2 + 5, 8], fill=(230, 190, 70))

def mountains_adwa(b, y1):
    """아드와의 뾰족한 화산암 봉우리들"""
    d = ImageDraw.Draw(b)
    for y in range(y1):
        t = y / y1; d.line([(0, y), (PW, y)], fill=mix((150, 186, 220), (232, 222, 196), t))
    peaks = [(80, 40), (210, 10), (330, 50), (470, 16), (600, 60), (760, 6), (900, 46), (1040, 20), (1180, 54), (1320, 24)]
    pts = [(0, y1)]
    for (x, h) in peaks: pts += [(x - 50, y1 - 20 - h * 0.3), (x, y1 - 96 + h), (x + 40, y1 - 30 - h * 0.2)]
    pts.append((PW, y1))
    d.polygon(pts, fill=(140, 120, 100))
    pts2 = [(x, y + 30) for (x, y) in pts[1:-1]]
    d.polygon([(0, y1)] + pts2 + [(PW, y1)], fill=(120, 110, 80))

def adwa(root):
    g = [list(';' * 29) for _ in range(13)]
    for y in range(0, 3):
        for x in range(29): g[y][x] = 'B'
    for x in range(12, 17): g[3][x] = 'x'               # 황제 천막
    for (x0, y0) in ((7, 3), (8, 3), (19, 3), (20, 3), (21, 3)): g[y0][x0] = 'x'   # 다른 천막
    for (x, y) in ((19, 7), (20, 8), (8, 9)): g[y][x] = 'x'     # 대포 · 모닥불
    for y in range(3, 13):
        for x in list(range(0, 6)) + list(range(23, 29)): g[y][x] = 'T' if (x + y) % 3 else 'k'
    for x in (13, 14, 15): g[12][x] = '.'
    m = Map('adwa', 3, [''.join(r) for r in g], 'desert', 96)
    b = m.big; d = ImageDraw.Draw(b)
    mountains_adwa(b, 2 * TS + 30)
    d.rectangle([0, 2 * TS + 30, PW, 3 * TS], fill=(170, 160, 100))
    # 흙길
    for y in range(4, 13):
        d.rectangle([13 * TS + 4, y * TS, 16 * TS - 4, y * TS + TS], fill=(196, 170, 120))
    G.scatter(b, m.grid, seed=96, density=0.8, flowers=False, pal='desert')
    # 천막들
    eth_tent(b, 11 * TS + 10, TS + 10, 5 * TS - 20, 2 * TS + 20, col=(200, 40, 46), band=(250, 210, 60), royal=True)
    eth_tent(b, 6 * TS + 30, 2 * TS - 10, 2 * TS + 10, 2 * TS + 4, band=(40, 130, 70))
    eth_tent(b, 18 * TS + 30, 2 * TS - 10, 3 * TS + 10, 2 * TS + 6, band=(220, 180, 50))
    # 초록·노랑·빨강 삼색 깃발 (장대)
    for (x, y) in ((11 * TS + 4, 2 * TS + 40), (17 * TS + 40, 2 * TS + 40), (10 * TS, 9 * TS), (19 * TS, 10 * TS)):
        d.line([(x, y + 60), (x, y)], fill=(120, 90, 50), width=3)
        fl = FL.waving('eth', 40, 26, 0.07, x * 0.01); b.alpha_composite(fl, (x + 2, y))
    # 모닥불 · 솥
    with Prop(b, 8 * TS - 2, 9 * TS + 10, 52, 40) as dd:
        dd.ellipse([4, 24, 48, 38], fill=(80, 70, 60)); dd.polygon([(12, 30), (26, 6), (40, 30)], fill=(240, 150, 60)); dd.polygon([(18, 30), (26, 14), (34, 30)], fill=(255, 220, 120))
    glow(b, 8 * TS + 24, 9 * TS + 30, 60, (255, 170, 80), 70)
    # 나무 (아카시아)
    for (x, y) in ((1, 4), (4, 7), (2, 10), (25, 4), (27, 8), (24, 11)): m.tree(x, y, 'dry', 0.9)
    exit_path(b, 13, 15, 12 * TS - 4, '↓ 해안으로 (다음 취재지)', col=(196, 170, 120), edge=(150, 126, 90))
    label(b, '아드와 · 에티오피아군 진영', 14 * TS, 11 * TS + 16, 12, back=(70, 40, 24, 230))
    m.ev('exit', 14, 12, trigger=1)
    m.ev('menelik', 14, 4, '$c_menelik', dir='down')
    m.ev('taytu', 16, 4, '$c_taytu', dir='down')
    m.ev('priest', 9, 5, '$c_eth_priest', dir='down')
    m.ev('war1', 11, 6, '$c_eth_war2', dir='right')
    m.ev('war2', 17, 8, '$c_eth_war', dir='left')
    m.ev('war3', 10, 10, '$c_eth_war3', dir='up')
    m.ev('woman', 7, 9, '$c_eth_woman', dir='right')
    m.ev('cannon1', 19, 7, '!$c_cannon'); m.ev('cannon2', 20, 8, '!$c_cannon')
    m.ev('pow', 21, 10, '$c_it_pow', dir='left')
    m.ev('guard', 20, 10, '$c_eth_war3', dir='right')
    for (x, y, sp) in ((8, 6, '$c_eth_war'), (18, 5, '$c_eth_war3'), (12, 9, '$c_eth_war'), (16, 10, '$c_eth_war2'), (10, 7, '$c_eth_woman')):
        m.ev('crowd', x, y, sp, dir='down')
    m.ev('fire', 8, 9)
    m.save(root, vignette=0.14, warm=0.08)

# ==================================================================== 04 콩고 고무 채취소 (1897년, 콩고 자유국)
def hut(b, x, y, w=96, h=80, wall=(160, 110, 70), roof=(176, 150, 90)):
    soft_shadow(b, [x + 6, y + h - 8, x + w + 6, y + h + 6], 90, 5)
    with Prop(b, x, y, w, h) as d:
        d.rectangle([10, h * 0.45, w - 10, h - 2], fill=wall)
        for xx in range(12, w - 10, 6): d.line([(xx, h * 0.45), (xx, h - 2)], fill=sh(wall, 0.85))
        d.polygon([(0, h * 0.5), (w / 2, 2), (w, h * 0.5)], fill=roof)
        for k in range(12): d.line([(w / 2, 4), (k * w / 11, h * 0.5)], fill=sh(roof, 0.82))
        d.rectangle([w / 2 - 9, h * 0.6, w / 2 + 9, h - 2], fill=(50, 34, 24))

def congo(root):
    g = [list(',' * 29) for _ in range(13)]
    for y in range(0, 2):
        for x in range(29): g[y][x] = 'T'
    for x in range(29):
        g[11][x] = 'W'; g[12][x] = 'W'
    for x in range(12, 17): g[11][x] = 'H'              # 부두
    g[12][13] = g[12][14] = g[12][15] = 'H'
    for y in range(2, 11):
        for x in list(range(0, 6)) + list(range(23, 29)): g[y][x] = 'T'
    for y in range(2, 11):
        for x in range(6, 23):
            if g[y][x] == ',' and 7 <= x <= 21 and 3 <= y <= 10: g[y][x] = '.'
    for x in range(15, 19): g[3][x] = 'x'                 # 무게 다는 헛간
    g[3][7] = g[3][8] = 'x'; g[6][7] = g[6][8] = 'x'      # 마을 오두막
    g[3][20] = g[3][21] = 'x'                             # 선교소
    g[9][20] = g[9][21] = 'x'                             # 전신 오두막
    m = Map('congo', 4, [''.join(r) for r in g], 'busan', 97)
    b = m.big; d = ImageDraw.Draw(b)
    # 강 위 증기선
    with Prop(b, 17 * TS, 10 * TS + 4, 5 * TS, 2 * TS + 10) as dd:
        dd.polygon([(0, 40), (5 * TS - 1, 40), (5 * TS - 20, 70), (20, 70)], fill=(236, 232, 220)); dd.rectangle([20, 20, 5 * TS - 40, 40], fill=(226, 220, 200))
        for xx in range(28, 5 * TS - 44, 14): dd.rectangle([xx, 24, xx + 8, 32], fill=(70, 90, 100))
        dd.rectangle([5 * TS - 80, 0, 5 * TS - 70, 22], fill=(40, 40, 40)); dd.rectangle([0, 34, 5 * TS - 1, 40], fill=(40, 60, 120))
        dd.ellipse([14, 30, 50, 66], outline=(150, 60, 40), width=4)
        fl = FL.flag('cfs', 22, 14); dd._image.paste(fl, (5 * TS - 24, 4), fl)
    # 정글 가장자리
    for (x, y) in ((1, 1), (4, 1), (8, 1), (11, 1), (19, 1), (23, 1), (26, 1), (0, 4), (3, 6), (1, 9), (25, 4), (27, 7), (24, 9), (14, 1), (17, 1)):
        m.tree(x, y, 'bamboo' if (x + y) % 4 == 0 else 'mulberry', 1.1)
    for (x, y) in ((2, 3), (5, 8), (26, 3), (23, 6), (27, 10)): G.bush(b, x, y, 24, 40, 1.0)
    G.scatter(b, m.grid, seed=97, density=0.9, flowers=False, pal='busan')
    # 오두막 · 헛간
    hut(b, 6 * TS + 6, 2 * TS - 4, 2 * TS + 4, 2 * TS + 4)
    hut(b, 6 * TS + 6, 5 * TS - 4, 2 * TS + 4, 2 * TS + 4, wall=(150, 100, 60))
    with Prop(b, 15 * TS - 6, TS + 30, 4 * TS + 12, 2 * TS + 22) as dd:      # 고무 무게 다는 헛간
        dd.polygon([(0, 30), (4 * TS + 11, 30), (4 * TS - 10, 0), (20, 0)], fill=(150, 130, 80))
        for xx in range(20, 4 * TS, 8): dd.line([(xx, 2), (xx - 10, 30)], fill=(120, 104, 64))
        for xx in (8, 4 * TS + 2): dd.rectangle([xx, 30, xx + 6, 2 * TS + 20], fill=(100, 70, 44))
        dd.rectangle([30, 46, 120, 66], fill=(110, 80, 50))
        dd.text((2 * TS + 6, 18), '고무 계량소', font=F(11), fill=(60, 30, 20), anchor='mm')
    # 고무 바구니 더미
    for (x, y) in ((16 * TS + 10, 3 * TS + 20), (18 * TS + 6, 3 * TS + 24)):
        with Prop(b, x, y, 50, 30) as dd:
            for k in range(4): dd.ellipse([k * 10, 10 - (k % 2) * 6, k * 10 + 18, 26 - (k % 2) * 6], fill=(140, 100, 60))
    hut(b, 20 * TS - 6, 2 * TS - 4, 2 * TS + 12, 2 * TS + 4, wall=(226, 216, 190), roof=(150, 130, 100))
    d.line([(21 * TS, 2 * TS - 8), (21 * TS, 2 * TS - 30)], fill=(90, 70, 50), width=3); d.line([(21 * TS - 8, 2 * TS - 22), (21 * TS + 8, 2 * TS - 22)], fill=(90, 70, 50), width=3)
    label(b, '선교소', 21 * TS, 4 * TS + 8, 11, back=(60, 40, 24, 220))
    with Prop(b, 20 * TS - 4, 8 * TS + 6, 2 * TS + 8, 2 * TS) as dd:    # 전신 오두막
        dd.rectangle([6, 30, 2 * TS + 2, 2 * TS - 2], fill=(200, 190, 160)); dd.polygon([(0, 32), (TS + 4, 6), (2 * TS + 8, 32)], fill=(120, 110, 100))
        dd.rectangle([40, 50, 60, 2 * TS - 2], fill=(60, 44, 30))
    d.line([(22 * TS + 10, 9 * TS + 40), (22 * TS + 10, 6 * TS)], fill=(110, 80, 50), width=3); d.line([(22 * TS + 10, 6 * TS + 4), (29 * TS, 5 * TS + 30)], fill=(40, 40, 40))
    label(b, '보마행 전신선', 21 * TS, 10 * TS + 30, 10, back=(40, 50, 60, 220))
    label(b, '콩고강 · 고무 채취소', 9 * TS, 10 * TS + 20, 12, back=(60, 40, 24, 230))
    m.ev('dock', 14, 11)
    m.ev('scale', 16, 4, '!$c_scale')
    m.ev('baskets', 18, 4, '!$c_rubber')
    m.ev('officer', 17, 5, '$c_be_officer', dir='down')
    m.ev('sold1', 11, 7, '$c_fp_sold', dir='right')
    m.ev('sold2', 19, 6, '$c_fp_sold', dir='left')
    m.ev('elder', 9, 4, '$c_kuba_old', dir='down')
    m.ev('woman', 9, 7, '$c_kuba_f', dir='left')
    m.ev('man', 12, 9, '$c_kuba_m', dir='up')
    m.ev('kid', 8, 8, '$c_kuba_kid', dir='right')
    m.ev('sheppard', 20, 5, '$c_sheppard', dir='down')
    m.ev('telegraph', 20, 9)
    for (x, y, sp) in ((14, 6, '$c_kuba_m'), (15, 7, '$c_kuba_m2'), (16, 6, '$c_kuba_f')):
        m.ev('line', x, y, sp, dir='up')
    m.save(root, vignette=0.16, warm=0.04)

ALL1 = [office, berlin, adwa, congo]
