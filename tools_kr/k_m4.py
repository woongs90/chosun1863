"""금지된 주파수 지도 8장 (29 x 13칸, 가운데 6~22칸이 실제로 걷는 곳)
 01 런던 방송국 (1923 사보이 힐 / 1933 · 1938 · 1939 방송회관 / 1940 등화관제 / 1944 / 1945)
 02 베를린 거리 (1923 / 1933 / 1938)     03 뉴욕 월가 (1929 / 1932)     04 제네바 국제 연맹 회의장 (1936)
 05 런던 거리 (1940 공습 밤)     06 블레츨리 파크 (1941)     07 노르망디 해변 (1944)     08 베르겐-벨젠 (1945 해방 뒤)
 '!' 표시가 그림과 정확히 맞도록: 조사할 물건은 (가) 그 물건 그림을 이벤트 자체(스프라이트)로 쓰거나
 (나) 지도에 그린 물건의 가운데 칸에 이벤트를 두고, 높은 물건은 이야기 쪽에서 markAt 으로 표시 칸을 정한다.
"""
from k_mapbase import *
import k_flags as FL
from k_m1 import panel_wall, side_walls
from k_m2 import facade
from k_m3 import sandbag_row, barbed, crater

WOOD = (120, 80, 50); WOOD_D = (84, 56, 36); BRASS = (206, 170, 90)

def interior_grid(floor='o'):
    g = [list('BBBBBB' + 'f' * 17 + 'BBBBBB') for _ in range(13)]
    for y in range(3, 12):
        for x in range(7, 22): g[y][x] = floor
    return g

def desk(b, tx0, tx1, ty, col=(110, 76, 48), top=None, legs=True, items=()):
    """tx0~tx1 칸, ty 칸에 놓인 책상 (칸 경계에 딱 맞게)"""
    d = ImageDraw.Draw(b)
    x0, x1, y = tx0 * TS + 2, (tx1 + 1) * TS - 2, ty * TS
    soft_shadow(b, [x0 + 4, y + 36, x1 + 4, y + 46], 80, 4)
    d.rectangle([x0, y + 8, x1, y + 34], fill=col); d.rectangle([x0, y + 6, x1, y + 10], fill=top or sh(col, 1.25))
    if legs:
        for xx in (x0 + 3, x1 - 8): d.rectangle([xx, y + 34, xx + 5, y + 46], fill=sh(col, 0.7))

# ==================================================================== 01 런던 방송국
def studio(root):
    g = interior_grid('o')
    for x in (13, 14, 15): g[5][x] = 'x'            # 마이크 책상
    g[4][8] = g[4][9] = 'x'                          # 수신기 탁자
    g[7][18] = g[7][19] = 'x'                        # 국장 책상
    g[3][21] = 'x'                                   # 화분 / 모래주머니 자리
    m = Map('studio', 1, [''.join(r) for r in g], 'paris', 23)
    base = m.big.copy()
    dark_out(base, 0, 6, col=(30, 26, 24)); dark_out(base, 23, 29, col=(30, 26, 24))

    def warmap(b, era):
        """벽의 전황 지도 (17~21칸, 위 벽) - 장마다 바뀜"""
        import k_geo as GEO
        yr = {'39': 1938, '40': 1938, '41': 1938, '44': 1945, '45': 1945}[era]
        box = (-12, 45, 33, 62)
        mp, pj = GEO.render(yr, box, (226, 118), line_w=0.5, seed=yr)
        md = ImageDraw.Draw(mp)
        axis = (110, 110, 116)
        def shade_axis(polys):
            pass
        # 전선 / 화살표
        if era == '39':
            GEO.polyline(md, pj, [(14.0, 54.0), (19.0, 52.5), (21.0, 52.2)], (180, 20, 20), 3)
            GEO.polyline(md, pj, [(23.0, 54.0), (22.0, 52.0), (21.5, 51.0)], (180, 20, 20), 3)
        elif era in ('40', '41'):
            for pts in ([(7.0, 50.5), (4.0, 50.0), (2.3, 48.9)], [(10.0, 55.0), (10.5, 59.9)], [(5.0, 52.0), (4.5, 52.4)]):
                GEO.polyline(md, pj, pts, (180, 20, 20), 3)
        elif era == '44':
            GEO.polyline(md, pj, [(-1.0, 50.5), (-0.5, 49.4)], (30, 60, 170), 3)
            GEO.polyline(md, pj, [(32.0, 52.0), (26.0, 52.5)], (30, 60, 170), 3)
        X0, Y0 = 17 * TS - 6, 6
        dd = ImageDraw.Draw(b)
        dd.rectangle([X0 - 6, Y0 - 4, X0 + 232, Y0 + 124], fill=(90, 66, 40)); dd.rectangle([X0 - 3, Y0 - 1, X0 + 229, Y0 + 121], fill=(214, 190, 130))
        b.paste(mp, (X0, Y0))
        label(b, {'39': '전황 지도 · 1939', '40': '전황 지도 · 1940', '41': '전황 지도 · 1941', '44': '전황 지도 · 1944', '45': '전황 지도 · 1945'}[era], X0 + 113, Y0 + 132, 11, back=(60, 40, 24, 230))

    def draw(b, era):
        d = ImageDraw.Draw(b)
        old = era == '23'
        if old:      # 사보이 힐: 소리를 줄이려고 벽마다 두꺼운 휘장
            panel_wall(b, 6 * TS, 23 * TS - 1, 3 * TS - 1, upper=(140, 60, 60), lower=(90, 60, 40), rail=(160, 120, 70), stripe=False)
            for xx in range(6 * TS, 23 * TS, 24):
                d.rectangle([xx, 0, xx + 11, 2 * TS + 40], fill=(124, 50, 52)); d.line([(xx + 11, 0), (xx + 11, 2 * TS + 40)], fill=(100, 40, 42), width=2)
        else:        # 방송회관(1932~): 매끈한 벽과 둥근 시계
            panel_wall(b, 6 * TS, 23 * TS - 1, 3 * TS - 1, upper=(214, 204, 180), lower=(70, 80, 96), rail=(190, 160, 90), stripe=False)
            for xx in range(6 * TS + 20, 23 * TS, 96): d.rectangle([xx, 10, xx + 4, 2 * TS + 10], fill=(200, 188, 160))
        side_walls(b, (100, 80, 64) if old else (70, 80, 96))
        # 왼쪽 창문 (1940~ 테이프 · 가림막)
        for xx in (7 * TS + 6, 10 * TS + 6):
            d.rectangle([xx, 14, xx + 70, 2 * TS + 16], fill=(150, 170, 186) if era not in ('40', '41') else (24, 26, 32))
            d.rectangle([xx + 33, 14, xx + 37, 2 * TS + 16], fill=(230, 226, 214)); d.rectangle([xx, 2 * TS - 18, xx + 70, 2 * TS - 14], fill=(230, 226, 214))
            if era in ('39', '40', '41', '44'):
                d.line([(xx, 14), (xx + 70, 2 * TS + 16)], fill=(236, 230, 200), width=3); d.line([(xx + 70, 14), (xx, 2 * TS + 16)], fill=(236, 230, 200), width=3)
        # 가운데: 방송 중 표시등 + 시계
        cx_, cy_ = 14 * TS + 24, 40
        d.ellipse([cx_ - 24, cy_ - 24, cx_ + 24, cy_ + 24], fill=(40, 40, 44)); d.ellipse([cx_ - 20, cy_ - 20, cx_ + 20, cy_ + 20], fill=(246, 242, 228))
        for k in range(12):
            a = k * math.pi / 6; d.line([(cx_ + math.cos(a) * 15, cy_ + math.sin(a) * 15), (cx_ + math.cos(a) * 18, cy_ + math.sin(a) * 18)], fill=(30, 30, 30), width=2)
        d.line([(cx_, cy_), (cx_ + 9, cy_ - 5)], fill=(20, 20, 20), width=3); d.line([(cx_, cy_), (cx_ - 2, cy_ - 14)], fill=(20, 20, 20), width=2)
        d.rounded_rectangle([cx_ - 44, 72, cx_ + 44, 92], 6, fill=(120, 20, 20)); d.text((cx_, 82), '방송 중  ON AIR', font=F(11), fill=(255, 230, 200), anchor='mm')
        if era in ('39', '40', '41', '44', '45'): warmap(b, era)
        else:
            with Prop(b, 17 * TS + 10, 14, 4 * TS - 20, 2 * TS) as dd:
                dd.rectangle([0, 0, 4 * TS - 21, 2 * TS - 1], fill=(236, 226, 200), outline=(120, 90, 60), width=3)
                dd.text((2 * TS - 10, 22), '오늘의 방송 순서', font=F(13), fill=(80, 40, 30), anchor='mm')
                for k in range(5): dd.line([(16, 40 + k * 10), (4 * TS - 40, 40 + k * 10)], fill=(150, 130, 110), width=2)
        # 마이크 책상 (13~15칸, 5칸)
        desk(b, 13, 15, 5, col=(90, 64, 44) if old else (60, 66, 80))
        with Prop(b, 13 * TS + 6, 5 * TS + 2, 3 * TS - 12, 20) as dd:
            dd.rectangle([10, 0, 60, 10], fill=(240, 236, 220)); dd.line([(14, 4), (54, 4)], fill=(120, 120, 120))
            dd.rectangle([96, 0, 124, 12], fill=(40, 40, 44))
        # 수신기 탁자 (8~9칸, 4칸)
        desk(b, 8, 9, 4, col=(110, 76, 48))
        # 국장 책상 (18~19칸, 7칸)
        desk(b, 18, 19, 7, col=(100, 64, 40))
        with Prop(b, 18 * TS + 8, 7 * TS - 4, 2 * TS - 16, 14) as dd:
            dd.rectangle([4, 2, 30, 12], fill=(244, 236, 214)); dd.rectangle([46, 0, 62, 12], fill=(30, 30, 30))
        # 오른쪽 위 모퉁이 (21,3)
        if era in ('39', '40', '41', '44'):
            sandbag_row(d, 21 * TS + 2, 22 * TS - 2, 4 * TS - 8, 3, seed=3)
        else:
            G.bush(b, 21, 3, 24, 40, 0.8)
        if era in ('40', '41'):     # 직원들이 방송국에서 잠을 잤다
            for xx in (8, 10):
                with Prop(b, xx * TS + 2, 10 * TS + 10, 2 * TS - 8, 30) as dd:
                    dd.rectangle([0, 6, 2 * TS - 9, 22], fill=(120, 126, 100)); dd.rectangle([2, 4, 18, 14], fill=(236, 232, 220))
                    dd.rectangle([2, 22, 6, 29], fill=(80, 80, 80)); dd.rectangle([2 * TS - 15, 22, 2 * TS - 11, 29], fill=(80, 80, 80))
        if era == '45':
            for k, c in enumerate(['uk', 'us48', 'su', 'fr', 'roc28']):
                fl = FL.waving(c, 40, 24, 0.06, k); b.alpha_composite(fl, (8 * TS + k * 52, 2 * TS + 10))
        cap = {'23': '영국 방송 회사 · 사보이 힐 스튜디오', '33': 'BBC 방송회관', '38': 'BBC 방송회관', '39': 'BBC 방송회관 · 1939', '40': 'BBC 방송회관 · 등화관제',
               '41': 'BBC 방송회관', '44': 'BBC 방송회관 · 1944', '45': 'BBC 방송회관 · 1945'}[era]
        label(b, cap, 14 * TS + 24, 12 * TS + 12, 12, back=(40, 30, 24, 230))
    for era in ('23', '33', '38', '39', '40', '41', '44', '45'):
        b = base.copy(); draw(b, era)
        G.finish(b, m.grid, vignette=0.14, ao=0.25, warm={'23': 0.1, '40': -0.04}.get(era, 0.04))
        save_variant(root, '!c_studio' + era, b)
    m.ev('door', 14, 12, trigger=1)
    m.ev('mic', 14, 5, '!$c_mic', anime=True)
    m.ev('radio', 8, 4, '!$c_radio')
    m.ev('warmap', 19, 2)
    m.ev('board', 19, 2)
    m.ev('gray', 18, 6, '$c_gray', dir='down')
    m.ev('tom', 10, 4, '$c_tom', dir='left')
    m.ev('annc', 12, 6, '$c_annc', dir='down')
    m.ev('secy', 20, 9, '$c_secy', dir='left')
    m.ev('secy2', 9, 8, '$c_secy2', dir='right')
    m.ev('paul16', 16, 9, '$c_paul16', dir='left')
    m.ev('elsa_s', 17, 9, '$c_elsa42', dir='left')
    m.ev('degaulle', 16, 6, '$c_degaulle', dir='down')
    m.ev('bed', 9, 10)
    m.save(root, parallax_name='!c_studio23', image=False)

# ==================================================================== 02 베를린 거리 (1923 / 1933 / 1938)
BLDG = {'bakery': (6, 3), 'radio_st': (9, 5), 'rosen': (14, 3), 'shop': (17, 3), 'station': (20, 3)}     # (시작 칸, 칸 수) → 문은 가운데 칸
def door_tile(key):
    x0, w = BLDG[key]; return x0 + w // 2

def street_grid(sidewalk='P', road='q'):
    g = [list('B' * 29) for _ in range(13)]
    for y in range(3, 11):
        for x in range(6, 23): g[y][x] = sidewalk
    for y in range(6, 9):
        for x in range(0, 29): g[y][x] = road
    for x in range(13, 16):
        g[11][x] = sidewalk; g[12][x] = sidewalk
    for y in range(6, 9):
        for x in list(range(0, 6)) + list(range(23, 29)): g[y][x] = 'B'
    return g

def berlin(root):
    g = street_grid()
    g[4][10] = 'x'                       # 지폐 손수레 / 확성기 자리
    g[4][18] = 'x'                       # 라디오 진열대
    m = Map('berlin', 2, [''.join(r) for r in g], 'paris', 1923)
    base = m.big.copy()

    def draw(b, era):
        d = ImageDraw.Draw(b)
        for y in range(0, 20): d.line([(0, y), (PW, y)], fill=mix((150, 160, 176), (196, 196, 192), y / 20))
        names = {'23': {'bakery': '빵집', 'radio_st': '복스하우스 · 라디오 방송국', 'rosen': '로젠 서점', 'shop': '전기 상회', 'station': '여관'},
                 '33': {'bakery': '빵집', 'radio_st': '베를린 방송국', 'rosen': '로젠 서점', 'shop': '라디오 상점', 'station': '여관'},
                 '38': {'bakery': '빵집', 'radio_st': '엘자의 아파트', 'rosen': '로젠 서점', 'shop': '라디오 상점', 'station': '프리드리히 거리 역'}}[era]
        walls = {'bakery': (214, 196, 160), 'radio_st': (190, 178, 160), 'rosen': (200, 186, 150), 'shop': (186, 180, 170), 'station': (170, 150, 130)}
        # 양옆 장식 건물
        for (tx, tw) in ((0, 3), (3, 3), (23, 3), (26, 3)):
            facade(b, tx * TS, 0, tw * TS, 3 * TS + 6, 'stone', (196 - tx, 184, 166), seed=tx, floors=3)
        for k, (x0, w) in BLDG.items():
            st = 'stone' if k != 'radio_st' else 'austro'
            if k == 'station' and era == '38':
                with Prop(b, x0 * TS - 4, -10, w * TS + 8, 3 * TS + 18) as dd:
                    dd.rectangle([4, 10, w * TS + 4, 3 * TS + 16], fill=(150, 120, 100))
                    dd.chord([14, 20, w * TS - 6, 3 * TS * 2 - 40], 180, 360, fill=(120, 140, 150))
                    for xx in range(24, w * TS - 10, 16): dd.line([(xx, 30), (xx, 3 * TS - 20)], fill=(90, 100, 110))
                    dd.rectangle([w * TS / 2 - 26, 3 * TS - 38, w * TS / 2 + 34, 3 * TS + 16], fill=(50, 40, 34))
                    dd.rectangle([8, 3 * TS - 56, w * TS, 3 * TS - 40], fill=(40, 40, 50))
                    dd.text((w * TS / 2 + 4, 3 * TS - 48), names[k], font=F(11), fill=(250, 240, 210), anchor='mm')
                continue
            facade(b, x0 * TS, 0, w * TS, 3 * TS + 6, st, walls[k], seed=x0 + 3, shop=names[k], shop_c=(50, 50, 60), floors=3,
                   awning=(120, 40, 40) if k == 'bakery' else None)
        if era == '23':
            # 복스하우스 지붕 위 안테나
            ax = (BLDG['radio_st'][0] + BLDG['radio_st'][1] / 2) * TS
            d.line([(ax - 40, 4), (ax + 40, 4)], fill=(40, 40, 40), width=2); d.line([(ax - 40, 0), (ax - 40, 14)], fill=(40, 40, 40), width=2); d.line([(ax + 40, 0), (ax + 40, 14)], fill=(40, 40, 40), width=2)
            # 빵집 앞 가격표 (하루에 두 번 바뀜)
            with Prop(b, 6 * TS + 4, 2 * TS + 2, 40, 26) as dd:
                dd.rectangle([0, 0, 39, 25], fill=(30, 30, 30)); dd.text((20, 7), '빵 1개', font=F(9), fill=(255, 255, 255), anchor='mm'); dd.text((20, 18), '2000억', font=F(10), fill=(255, 210, 120), anchor='mm')
        if era == '33':
            # 붉은 휘장 (나치 깃발은 지도에 그리지 않고 사료 카드에서만) · 상점 불매 표시
            for xx in (9 * TS + 20, 13 * TS - 14):
                d.rectangle([xx, 10, xx + 22, 2 * TS + 10], fill=(190, 30, 30)); d.ellipse([xx + 3, 40, xx + 19, 56], fill=(240, 236, 230))
            with Prop(b, 14 * TS + 6, 2 * TS + 6, 3 * TS - 12, 24) as dd:
                dd.rectangle([0, 0, 3 * TS - 13, 23], fill=(246, 240, 220), outline=(120, 30, 30), width=2)
                dd.text((3 * TS / 2 - 6, 12), '"유대인 상점에서 사지 마라"', font=F(10), fill=(150, 20, 20), anchor='mm')
            with Prop(b, 17 * TS + 6, 2 * TS + 4, 3 * TS - 12, 22) as dd:
                dd.rectangle([0, 0, 3 * TS - 13, 21], fill=(250, 230, 120)); dd.text((3 * TS / 2 - 6, 11), '국민 라디오 76마르크!', font=F(10), fill=(40, 30, 20), anchor='mm')
        if era == '38':
            # 수정의 밤 뒤: 깨진 유리 · 판자로 막은 창
            rnd = random.Random(38)
            for k in range(60):
                x = rnd.randint(14 * TS, 17 * TS - 4); y = rnd.randint(3 * TS + 4, 5 * TS)
                d.polygon([(x, y), (x + rnd.randint(3, 8), y + rnd.randint(-2, 3)), (x + rnd.randint(0, 5), y + rnd.randint(3, 7))], fill=(200, 220, 230))
            for xx in (14 * TS + 6, 15 * TS + 30):
                for k in range(3): d.rectangle([xx, 2 * TS + 4 + k * 12, xx + 40, 2 * TS + 12 + k * 12], fill=(150, 116, 76), outline=(100, 76, 50))
            d.text((15 * TS + 24, 2 * TS - 4), '1938.11.10', font=F(10), fill=(90, 30, 30), anchor='mm')
        # 길
        for xx in range(0, PW, 64): d.rectangle([xx, 7 * TS + 22, xx + 30, 7 * TS + 26], fill=(214, 206, 190))
        for yy in (6 * TS - 3, 9 * TS): d.rectangle([0, yy, PW, yy + 4], fill=(170, 164, 150))
        if era != '38':
            for xx in (7, 21): A_pole(b, xx * TS + 24, 10 * TS + 40, 130)
        else:
            for xx in (7, 21): A_pole(b, xx * TS + 24, 10 * TS + 40, 130)
        exit_path(b, 13, 15, 11 * TS + 2, '↓ 런던으로', col=(150, 146, 136), edge=(110, 106, 100))
        label(b, {'23': '베를린 · 1923년 11월', '33': '베를린 · 1933년 가을', '38': '베를린 · 1938년 12월'}[era], 14 * TS + 24, 10 * TS + 30, 12, back=(50, 40, 34, 230))
    for era in ('23', '33', '38'):
        b = base.copy(); draw(b, era)
        G.finish(b, m.grid, vignette=0.14, warm={'23': 0.06, '33': 0.0, '38': -0.06}[era])
        save_variant(root, '!c_berlin' + era, b)
    # 문 (건물 문은 벽 칸(2줄)에, 앞 칸(3줄)에서 위를 보고 조사)
    m.ev('bakery', door_tile('bakery'), 2)
    m.ev('voxhaus', door_tile('radio_st'), 2)
    m.ev('rosen_door', door_tile('rosen'), 2)
    m.ev('shopdoor', door_tile('shop'), 2)
    m.ev('station', door_tile('station'), 2)
    m.ev('exit', 14, 12, trigger=1)
    # 1923
    m.ev('barrow', 10, 4, '!$c_barrow')
    m.ev('baker', 7, 3, '$c_baker', dir='down')
    m.ev('wage_man', 12, 5, '$c_de_man23', dir='left')
    m.ev('vet', 20, 9, '$c_de_vet23', dir='left')
    m.ev('kid23', 16, 9, '$c_de_kid23', dir='up')
    m.ev('elsa23', 12, 3, '$c_elsa20', dir='down')
    m.ev('radiotech', 10, 3, '$c_radio_tech', dir='down')
    for (x, y, sp) in ((8, 4, '$c_de_wom23'), (9, 5, '$c_de_man23b'), (8, 5, '$c_de_wom23')):
        m.ev('queue23', x, y, sp, dir='left')
    # 1933
    m.ev('speaker', 10, 4, '!$c_speaker', anime=True)
    m.ev('radio_ve', 18, 4, '!$c_radio_ve')
    m.ev('shopkeep', 19, 3, '$c_radio_shop', dir='down')
    m.ev('rosen', 15, 3, '$c_jew_shop', dir='down')
    m.ev('sa1', 14, 4, '$c_sa', dir='right')
    m.ev('sa2', 16, 4, '$c_sa2', dir='left')
    m.ev('newsboy', 8, 9, '$c_newsboy_de', dir='right')
    m.ev('elsa33', 12, 3, '$c_elsa30', dir='down')
    m.ev('paul4', 13, 3, '$c_paul4', dir='down')
    for (x, y, sp) in ((9, 5, '$c_de_man33'), (11, 5, '$c_de_wom33'), (10, 5, '$c_de_old33')):
        m.ev('listen33', x, y, sp, dir='up')
    # 1938
    m.ev('glazier', 16, 4, '$c_glazier', dir='up')
    m.ev('rosen38', 14, 4, '$c_jew_shop', dir='down')
    m.ev('elsa38', 12, 3, '$c_elsa35', dir='down')
    m.ev('paul9', 13, 3, '$c_paul9', dir='down')
    m.ev('quaker', 20, 4, '$c_quaker', dir='left')
    m.ev('rail', 22, 3, '$c_rail', dir='down')
    for (x, y, sp) in ((19, 5, '$c_kt_kid'), (21, 5, '$c_kt_kid2'), (22, 5, '$c_kt_kid3'), (18, 5, '$c_kt_mom'), (19, 4, '$c_kt_dad')):
        m.ev('kt_crowd', x, y, sp, dir='up')
    m.ev('patrol1', 9, 7, '$c_sa', dir='right')
    m.ev('patrol2', 18, 9, '$c_schupo', dir='left')
    m.save(root, parallax_name='!c_berlin23', image=False)

def A_pole(b, x, y, h):
    import k_arch
    g_arch.pole(b, x, y, h, lamp=True)

# ==================================================================== 03 뉴욕 월가 (1929 / 1932)
def newyork(root):
    g = street_grid()
    g[4][12] = 'x'                          # 시세 테이프 기계
    m = Map('ny', 3, [''.join(r) for r in g], 'versailles', 1929)
    base = m.big.copy()

    def draw(b, era):
        d = ImageDraw.Draw(b)
        for y in range(0, 16): d.line([(0, y), (PW, y)], fill=mix((160, 176, 196), (200, 200, 196), y / 16))
        for (tx, tw) in ((0, 3), (3, 3), (23, 3), (26, 3)):
            facade(b, tx * TS, 0, tw * TS, 3 * TS + 6, 'stone', (180 + tx, 176, 170), seed=tx + 9, floors=3)
        # 증권 거래소 (7~13칸): 기둥 여섯 개
        with Prop(b, 7 * TS - 6, -6, 7 * TS + 12, 3 * TS + 14) as dd:
            W_ = 7 * TS + 11
            dd.rectangle([6, 6, W_ - 6, 3 * TS + 12], fill=(222, 216, 200))
            dd.polygon([(0, 30), (W_, 30), (W_ - 30, 6), (30, 6)], fill=(232, 226, 210)); dd.rectangle([0, 30, W_, 38], fill=(206, 198, 180))
            for k in range(6):
                xx = 24 + k * (W_ - 48) / 5
                dd.rectangle([xx - 9, 40, xx + 9, 3 * TS + 2], fill=(240, 236, 224)); dd.line([(xx - 4, 42), (xx - 4, 3 * TS)], fill=(214, 208, 196))
                dd.rectangle([xx - 12, 3 * TS + 2, xx + 12, 3 * TS + 10], fill=(214, 208, 196))
            dd.text((W_ / 2, 20), '뉴욕 증권 거래소', font=F(12), fill=(80, 70, 60), anchor='mm')
            if era == '29':
                for k in range(3): dd.rectangle([60 + k * 110, 50, 80 + k * 110, 70], fill=(70, 90, 140))
        # 은행 (15~19칸)
        facade(b, 15 * TS, 0, 5 * TS, 3 * TS + 6, 'stone', (200, 190, 170), seed=15, shop='시민 은행' if era == '29' else '시민 은행 · 문 닫음', shop_c=(40, 60, 50) if era == '29' else (120, 30, 30), floors=3)
        if era == '32':
            with Prop(b, 17 * TS - 2, 2 * TS + 14, 52, 26) as dd:
                dd.rectangle([0, 0, 51, 25], fill=(246, 240, 220), outline=(40, 40, 40)); dd.text((26, 7), 'CLOSED', font=F(10), fill=(160, 20, 20), anchor='mm'); dd.text((26, 18), '임시 휴업', font=F(9), fill=(40, 40, 40), anchor='mm')
        # 무료 급식소 (20~22칸)
        facade(b, 20 * TS, 0, 3 * TS, 3 * TS + 6, 'london', (150, 96, 76), seed=20, shop='무료 급식소' if era == '32' else '식당', shop_c=(60, 60, 60), floors=3)
        for xx in range(0, PW, 64): d.rectangle([xx, 7 * TS + 22, xx + 30, 7 * TS + 26], fill=(230, 220, 120))
        for yy in (6 * TS - 3, 9 * TS): d.rectangle([0, yy, PW, yy + 4], fill=(170, 164, 150))
        if era == '29':
            rnd = random.Random(29)
            for k in range(140):                              # 흩날리는 시세 테이프 종이
                x, y = rnd.randint(6 * TS, 23 * TS), rnd.randint(3 * TS, 11 * TS)
                d.line([(x, y), (x + rnd.randint(-6, 6), y + rnd.randint(2, 7))], fill=(246, 242, 228), width=2)
        exit_path(b, 13, 15, 11 * TS + 2, '↓ 부두 · 런던으로', col=(150, 146, 136), edge=(110, 106, 100))
        label(b, {'29': '뉴욕 월가 · 1929년 10월 29일 「검은 화요일」', '32': '뉴욕 월가 · 1932년 겨울'}[era], 14 * TS + 24, 10 * TS + 30, 12, back=(40, 40, 50, 230))
    for era in ('29', '32'):
        b = base.copy(); draw(b, era)
        G.finish(b, m.grid, vignette=0.14, warm=0.02 if era == '29' else -0.05)
        save_variant(root, '!c_ny' + era, b)
    m.ev('exchange', 10, 2)
    m.ev('bank', 17, 2)
    m.ev('soup', 21, 2)
    m.ev('ticker', 12, 4, '!$c_ticker', anime=True)
    m.ev('exit', 14, 12, trigger=1)
    m.ev('broker', 11, 4, '$c_broker', dir='right')
    m.ev('broker2', 9, 5, '$c_broker2', dir='up')
    m.ev('newsboy', 16, 9, '$c_newsboy_us', dir='left')
    m.ev('nypd', 19, 5, '$c_nypd', dir='down')
    for (x, y, sp) in ((8, 4, '$c_broker'), (13, 5, '$c_broker2'), (10, 9, '$c_depositor'), (7, 5, '$c_broker')):
        m.ev('crowd29', x, y, sp, dir='up')
    m.ev('apple', 8, 9, '$c_apple_man', dir='right')
    m.ev('depositor', 17, 4, '$c_depositor2', dir='up')
    m.ev('jobless', 21, 4, '$c_jobless', dir='up')
    m.ev('souplady', 21, 3, '$c_soup_lady', dir='down')
    for (x, y, sp) in ((16, 4, '$c_depositor'), (16, 5, '$c_depositor3'), (18, 4, '$c_depositor')):
        m.ev('bankq', x, y, sp, dir='up')
    for (x, y, sp) in ((22, 4, '$c_jobless2'), (22, 5, '$c_jobless3'), (20, 5, '$c_jobless'), (19, 4, '$c_jobless2')):
        m.ev('breadq', x, y, sp, dir='left')
    m.ev('shine', 12, 9, '$c_shoeshine', dir='up')
    m.save(root, parallax_name='!c_ny29', image=False)

# ==================================================================== 04 제네바 국제 연맹 회의장 (1936년 6월 30일)
def geneva(root):
    g = interior_grid('z')
    for x in (13, 14, 15): g[4][x] = 'x'                 # 연단
    for y in (6, 9):
        for x in (8, 9, 10, 11): g[y][x] = 'x'           # 대표석
        for x in (17, 18, 19, 20): g[y][x] = 'x'
    g[3][7] = g[3][8] = 'x'                              # 기자석
    m = Map('geneva', 4, [''.join(r) for r in g], 'versailles', 1936)
    b = m.big; d = ImageDraw.Draw(b)
    dark_out(b, 0, 6, col=(34, 30, 28)); dark_out(b, 23, 29, col=(34, 30, 28))
    panel_wall(b, 6 * TS, 23 * TS - 1, 3 * TS - 1, upper=(200, 190, 166), lower=(110, 80, 56), rail=(180, 150, 90), stripe=False)
    for xx in range(7 * TS, 22 * TS, 3 * TS):
        d.rectangle([xx, 10, xx + 50, 2 * TS + 14], fill=(170, 186, 200)); d.chord([xx, -14, xx + 50, 30], 180, 360, fill=(170, 186, 200))
        d.line([(xx + 25, 10), (xx + 25, 2 * TS + 14)], fill=(220, 214, 196), width=3)
    with Prop(b, 12 * TS + 10, 14, 5 * TS - 20, 56) as dd:
        dd.rectangle([0, 0, 5 * TS - 21, 55], fill=(40, 60, 90), outline=(200, 180, 110), width=3)
        dd.text((5 * TS / 2 - 10, 18), '국제 연맹 총회', font=F(15), fill=(250, 240, 210), anchor='mm')
        dd.text((5 * TS / 2 - 10, 40), 'SOCIÉTÉ DES NATIONS', font=F(10), fill=(220, 210, 180), anchor='mm')
    side_walls(b, (110, 90, 70))
    desk(b, 13, 15, 4, col=(90, 60, 40))
    with Prop(b, 14 * TS + 4, 4 * TS - 6, 40, 16) as dd:
        dd.rectangle([14, 0, 26, 10], fill=(60, 60, 64))
    for y in (6, 9):
        for (a_, b_) in ((8, 11), (17, 20)):
            desk(b, a_, b_, y, col=(110, 76, 48))
            with Prop(b, a_ * TS + 6, y * TS + 2, (b_ - a_ + 1) * TS - 12, 12) as dd:
                for k in range(b_ - a_ + 1): dd.rectangle([k * TS + 4, 0, k * TS + 30, 9], fill=(240, 236, 220))
    desk(b, 7, 8, 3, col=(80, 70, 60))
    label(b, '기자석', 8 * TS, 3 * TS - 6, 10, back=(50, 40, 34, 220))
    for nm, (x, y) in (('영국', (9, 6)), ('프랑스', (11, 6)), ('중국', (18, 6)), ('소련', (20, 6))):
        label(b, nm, x * TS + 24, y * TS + 34, 9, back=(40, 40, 50, 210))
    label(b, '제네바 · 국제 연맹 총회 · 1936년 6월 30일', 14 * TS + 24, 12 * TS + 12, 11, back=(40, 50, 70, 230))
    m.ev('door', 14, 12, trigger=1)
    m.ev('selassie', 14, 3, '$c_selassie', dir='down')
    m.ev('aide', 12, 3, '$c_eth_aide', dir='down')
    m.ev('uk_dlg', 9, 5, '$c_dlg36', dir='down')
    m.ev('fr_dlg', 11, 5, '$c_dlg36b', dir='down')
    m.ev('cn_dlg', 18, 5, '$c_cn_dlg', dir='down')
    m.ev('su_dlg', 20, 5, '$c_su_dlg', dir='down')
    m.ev('journo1', 7, 4, '$c_it_journo', dir='up')
    m.ev('journo2', 8, 4, '$c_it_journo', dir='up')
    m.ev('usher', 16, 11, '$c_usher', dir='up')
    for (x, y, sp) in ((9, 8, '$c_dlg36'), (11, 8, '$c_dlg36c'), (17, 8, '$c_dlg36b'), (19, 8, '$c_dlg36c'), (8, 10, '$c_dlg36b'), (20, 10, '$c_dlg36')):
        m.ev('delegates', x, y, sp, dir='up')
    m.save(root, vignette=0.14, warm=0.04)

# ==================================================================== 05 런던 거리 (1940년 공습 밤)
def london(root):
    g = street_grid()
    g[4][7] = g[4][8] = 'x'                         # 공습 경비 초소 (모래주머니)
    # (21,3)은 지하철역 문 앞 — 비워 둠
    m = Map('london', 5, [''.join(r) for r in g], 'paris', 1940)
    b = m.big; d = ImageDraw.Draw(b)
    for y in range(0, 24): d.line([(0, y), (PW, y)], fill=mix((20, 24, 44), (50, 40, 50), y / 24))
    for (tx, tw, wc) in ((0, 3, (110, 70, 60)), (3, 3, (120, 76, 64)), (6, 3, (110, 72, 62)), (9, 3, (124, 80, 66)), (12, 3, (112, 70, 58)), (15, 3, (118, 76, 64)),
                         (18, 3, (106, 70, 60)), (23, 3, (114, 74, 62)), (26, 3, (110, 70, 60))):
        facade(b, tx * TS, 0, tw * TS, 3 * TS + 6, 'london', wc, seed=tx, floors=3, night=False)
    # 지하철역 (20~22칸)
    with Prop(b, 20 * TS - 2, -4, 3 * TS + 4, 3 * TS + 12) as dd:
        dd.rectangle([2, 4, 3 * TS + 2, 3 * TS + 10], fill=(130, 60, 50))
        dd.rectangle([20, 3 * TS - 50, 3 * TS - 16, 3 * TS + 10], fill=(30, 26, 26))
        dd.ellipse([3 * TS / 2 - 26, 16, 3 * TS / 2 + 30, 56], fill=(200, 30, 30)); dd.ellipse([3 * TS / 2 - 16, 26, 3 * TS / 2 + 20, 46], fill=(250, 250, 250))
        dd.rectangle([3 * TS / 2 - 34, 31, 3 * TS / 2 + 38, 41], fill=(30, 40, 120)); dd.text((3 * TS / 2 + 2, 36), 'UNDERGROUND', font=F(7), fill=(255, 255, 255), anchor='mm')
    label(b, '지하철역 · 공습 대피소', 21 * TS + 24, 3 * TS + 14, 10, back=(140, 30, 30, 230))
    # 테이프 붙인 창문 (불빛 없는 등화관제)
    for k in range(40):
        rnd = random.Random(k)
        x, y = rnd.randint(6 * TS, 20 * TS), rnd.randint(18, 2 * TS + 10)
    # 탐조등 불빛
    for (x0, a) in ((4 * TS, -0.5), (25 * TS, 0.6)):
        lay = Image.new('RGBA', b.size, (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
        ld.polygon([(x0, 20), (x0 + a * 300 - 30, -200), (x0 + a * 300 + 30, -200)], fill=(230, 230, 200, 70))
        b.alpha_composite(lay)
    # 초소 (모래주머니)
    sandbag_row(d, 7 * TS, 9 * TS, 4 * TS + 20, 3, seed=40)
    with Prop(b, 7 * TS + 10, 3 * TS + 2, 2 * TS - 20, 20) as dd:
        dd.rectangle([0, 0, 2 * TS - 21, 19], fill=(30, 30, 34)); dd.text((2 * TS / 2 - 10, 10), '경비 초소 ARP', font=F(9), fill=(250, 230, 120), anchor='mm')
    for xx in range(0, PW, 64): d.rectangle([xx, 7 * TS + 22, xx + 30, 7 * TS + 26], fill=(220, 220, 220))
    for yy in (6 * TS - 3, 9 * TS): d.rectangle([0, yy, PW, yy + 4], fill=(120, 116, 110))
    for xx in range(0, PW, 96): d.rectangle([xx, 6 * TS - 3, xx + 48, 6 * TS + 1], fill=(240, 240, 240))     # 등화관제 흰 연석 표시
    crater(d, 16 * TS, 7 * TS + 20, 30, (70, 64, 60))
    exit_path(b, 13, 15, 11 * TS + 2, '↓ 방송국으로', col=(110, 106, 100), edge=(80, 76, 70))
    label(b, '런던 · 1940년 9월 밤 · 공습', 14 * TS + 24, 10 * TS + 30, 12, back=(40, 30, 40, 230))
    m.ev('tube', 21, 2)
    m.ev('post', 7, 4)
    m.ev('exit', 14, 12, trigger=1)
    m.ev('warden', 9, 4, '$c_warden', dir='down')
    m.ev('lon_mom', 12, 9, '$c_lon_mom', dir='up')
    m.ev('lon_kid', 17, 10, '$c_lon_kid', dir='up')
    m.ev('lon_old', 19, 5, '$c_lon_old', dir='left')
    m.ev('fireman', 16, 4, '$c_fireman', dir='down')
    m.ev('fire1', 15, 3, '!$c_fire', anime=True, through=True)
    m.ev('fire2', 10, 9, '!$c_fire', anime=True, through=True)
    m.ev('tubestaff', 22, 3, '$c_tube_staff', dir='down')
    m.ev('wvs', 20, 4, '$c_wvs', dir='left')
    m.ev('pilot', 11, 4, '$c_pol_air', dir='down')
    m.ev('sailor', 13, 4, '$c_fr_sailor', dir='down')
    m.ev('balloon', 4, 1, '!$c_balloon', anime=True, through=True, priority=2)
    m.ev('balloon2', 25, 1, '!$c_balloon', anime=True, through=True, priority=2)
    m.ev('searchl', 2, 2, '!$c_searchlight', anime=True)
    m.save(root, vignette=0.24, warm=-0.08)

# ==================================================================== 06 블레츨리 파크 8호 막사 (1941)
def bletchley(root):
    g = interior_grid('o')
    for x in (8, 9, 10, 11): g[5][x] = 'x'
    for x in (8, 9, 10, 11): g[8][x] = 'x'
    g[5][15] = g[5][16] = 'x'                         # 튜링의 책상
    for x in (18, 19): g[3][x] = 'x'; g[4][x] = 'x'   # 봄브 기계
    m = Map('bletchley', 6, [''.join(r) for r in g], 'paris', 1941)
    b = m.big; d = ImageDraw.Draw(b)
    dark_out(b, 0, 6, col=(30, 30, 28)); dark_out(b, 23, 29, col=(30, 30, 28))
    panel_wall(b, 6 * TS, 23 * TS - 1, 3 * TS - 1, upper=(200, 206, 186), lower=(110, 100, 80), rail=(150, 140, 110), stripe=False)
    side_walls(b, (120, 110, 90))
    # 칠판 (9~11칸 위 벽)
    with Prop(b, 9 * TS - 10, 10, 3 * TS + 20, 2 * TS) as dd:
        dd.rectangle([0, 0, 3 * TS + 19, 2 * TS - 1], fill=(40, 60, 50), outline=(120, 90, 60), width=4)
        for k, t in enumerate(['WETTER = 날씨?', 'ZHWWHU', '←3 →3 ?']): dd.text((16, 16 + k * 24), t, font=F(13), fill=(236, 236, 226))
    for xx in (14 * TS, 20 * TS + 20):
        d.rectangle([xx, 14, xx + 60, 2 * TS + 10], fill=(28, 30, 36))
    label(b, '극비 · 8호 막사', 14 * TS + 30, 2 * TS + 26, 10, back=(120, 30, 30, 230))
    for y in (5, 8): desk(b, 8, 11, y, col=(110, 86, 60))
    for y in (5, 8):
        with Prop(b, 8 * TS + 6, y * TS + 2, 4 * TS - 12, 12) as dd:
            for k in range(4): dd.rectangle([k * TS + 4, 0, k * TS + 28, 9], fill=(240, 236, 220))
    desk(b, 15, 16, 5, col=(100, 70, 46))
    with Prop(b, 15 * TS + 6, 5 * TS - 2, 2 * TS - 12, 14) as dd:
        dd.rectangle([2, 2, 28, 12], fill=(244, 236, 214)); dd.rectangle([40, 0, 56, 12], fill=(60, 60, 60)); dd.ellipse([62, 2, 72, 12], fill=(240, 240, 230))
    label(b, '블레츨리 파크 · 1941년', 14 * TS + 24, 12 * TS + 12, 12, back=(40, 40, 34, 230))
    m.ev('door', 14, 12, trigger=1)
    m.ev('bombe', 19, 4, '!$c_bombe', anime=True)
    m.ev('chalk', 10, 2)
    m.ev('tdesk', 15, 5)
    m.ev('turing', 16, 6, '$c_turing', dir='down')
    m.ev('wren', 17, 5, '$c_wren', dir='right')
    m.ev('wren2', 20, 5, '$c_wren2', dir='left')
    m.ev('codebrk', 9, 6, '$c_codebrk', dir='up')
    m.ev('codebrk2', 11, 9, '$c_codebrk', dir='up')
    m.ev('guard', 16, 11, '$c_guard_uk', dir='up')
    m.save(root, vignette=0.14, warm=0.02)

# ==================================================================== 07 노르망디 해변 (1944년 6월 7일)
def normandy(root):
    g = [list(';' * 29) for _ in range(13)]
    for y in range(0, 3):
        for x in range(29): g[y][x] = 'T'
    for x in (13, 14, 15): g[2][x] = '.'
    for y in range(3, 10):
        for x in range(29): g[y][x] = 's'
    for y in range(10, 13):
        for x in range(29): g[y][x] = 'W'
    for y in range(3, 10):
        for x in list(range(0, 6)) + list(range(23, 29)): g[y][x] = 'B'
    for (x, y) in ((8, 8), (20, 8), (11, 9), (17, 9)): g[y][x] = 'x'      # 해안 장애물
    for x in (8, 9, 10, 17, 18, 19): g[4][x] = 'x'                      # 녹음 차 · 전차
    m = Map('normandy', 7, [''.join(r) for r in g], 'busan', 1944)
    b = m.big; d = ImageDraw.Draw(b)
    for (x, y) in ((1, 1), (4, 0), (7, 1), (10, 0), (18, 0), (21, 1), (24, 0), (27, 1)): m.tree(x, y, 'mulberry', 1.0)
    for (x, y) in ((2, 4), (25, 5), (3, 8), (26, 8)): G.bush(b, x, y, 24, 40, 1.0)
    d.rectangle([13 * TS + 4, 0, 16 * TS - 4, 3 * TS], fill=(170, 150, 110))
    label(b, '↑ 마을로 가는 길', 14 * TS + 24, 3 * TS + 6, 10, back=(40, 50, 60, 220))
    G.scatter(b, m.grid, seed=44, density=0.5, flowers=False, pal='busan')
    for k in range(10):
        rnd = random.Random(k)
        crater(d, rnd.randint(6 * TS, 22 * TS), rnd.randint(4 * TS, 9 * TS), rnd.randint(14, 26), (170, 150, 110))
    label(b, '노르망디 · 1944년 6월 7일', 14 * TS + 24, 9 * TS + 30, 12, back=(40, 50, 60, 230))
    m.ev('path', 14, 2, trigger=1)
    m.ev('recvan', 9, 4, '!$c_jeep', dir='right')
    m.ev('sherman', 18, 4, '!$c_sherman', dir='left')
    m.ev('lcvp', 10, 11, '!$c_lcvp', dir='right', through=True)
    m.ev('lcvp2', 19, 11, '!$c_lcvp', dir='left', through=True)
    for (x, y) in ((8, 8), (20, 8), (11, 9), (17, 9)): m.ev('hedgehog', x, y, '!$c_hedgehog')
    m.ev('gi', 12, 6, '$c_gi', dir='down')
    m.ev('gi2', 13, 8, '$c_gi2', dir='up')
    m.ev('tommy', 16, 6, '$c_tommy44', dir='down')
    m.ev('canuck', 21, 6, '$c_canuck44', dir='left')
    m.ev('ff44', 7, 6, '$c_ff44', dir='right')
    m.ev('medic', 10, 7, '$c_gi_medic', dir='right')
    m.ev('pow', 21, 4, '$c_de_pow', dir='down')
    m.ev('powguard', 20, 4, '$c_tommy44', dir='right')
    m.ev('villager', 15, 3, '$c_fr_vill', dir='down')
    m.ev('frwom', 16, 3, '$c_fr_wom', dir='down')
    m.ev('frkid', 12, 3, '$c_fr_kid', dir='down')
    m.ev('photog', 7, 4, '$c_correspondent', dir='right')
    m.save(root, vignette=0.12, warm=0.04)

# ==================================================================== 08 베르겐-벨젠 수용소 해방 뒤 (1945년 4월)
def belsen(root):
    g = [list('.' * 29) for _ in range(13)]
    for y in range(0, 3):
        for x in range(29): g[y][x] = 'B'
    for y in range(3, 13):
        for x in list(range(0, 6)) + list(range(23, 29)): g[y][x] = 'B'
    for y in (11, 12):
        for x in range(29): g[y][x] = 'B' if x not in (13, 14, 15) else '.'
    for x in (8, 9, 10): g[4][x] = 'x'               # 의무 천막
    g[3][21] = 'x'                                   # 경고 표지
    for x in (17, 18, 19): g[4][x] = 'x'             # 구급차
    m = Map('belsen', 8, [''.join(r) for r in g], 'seoul_w', 1945)
    b = m.big; d = ImageDraw.Draw(b)
    for y in range(0, 30): d.line([(0, y), (PW, y)], fill=mix((170, 178, 186), (200, 200, 196), y / 30))
    for (x, y) in ((1, 1), (3, 0), (5, 1), (23, 1), (25, 0), (27, 1)): m.tree(x, y, 'pine', 1.0)
    # 철조망 울타리 + 닫힌 문 (안쪽은 그리지 않음)
    d.rectangle([6 * TS, 2 * TS + 10, 23 * TS, 3 * TS], fill=(150, 140, 120))
    barbed(d, 6 * TS, 23 * TS, 2 * TS + 20, 45, col=(60, 56, 52))
    with Prop(b, 13 * TS, TS + 10, 3 * TS, 2 * TS) as dd:
        dd.rectangle([4, 0, 12, 2 * TS - 1], fill=(90, 70, 50)); dd.rectangle([3 * TS - 12, 0, 3 * TS - 4, 2 * TS - 1], fill=(90, 70, 50))
        for xx in range(16, 3 * TS - 16, 10): dd.line([(xx, 14), (xx, 2 * TS - 4)], fill=(70, 66, 60), width=2)
        dd.line([(12, 14), (3 * TS - 12, 14)], fill=(70, 66, 60), width=3)
    # 영국군 의무 천막 (8~10칸)
    with Prop(b, 8 * TS - 6, 2 * TS + 20, 3 * TS + 12, 2 * TS) as dd:
        dd.polygon([(0, 2 * TS - 6), (3 * TS / 2 + 6, 4), (3 * TS + 12, 2 * TS - 6)], fill=(176, 170, 140))
        dd.polygon([(3 * TS / 2 + 6, 4), (3 * TS + 12, 2 * TS - 6), (3 * TS / 2 + 30, 2 * TS - 6)], fill=(156, 150, 120))
        dd.rectangle([3 * TS / 2 - 8, 2 * TS - 40, 3 * TS / 2 + 20, 2 * TS - 6], fill=(60, 54, 44))
        dd.rectangle([3 * TS / 2 - 2, 26, 3 * TS / 2 + 14, 42], fill=(250, 250, 250)); dd.rectangle([3 * TS / 2 + 3, 28, 3 * TS / 2 + 9, 40], fill=(200, 30, 30)); dd.rectangle([3 * TS / 2 - 0, 31, 3 * TS / 2 + 12, 37], fill=(200, 30, 30))
    # 경고 표지 (21칸)
    with Prop(b, 21 * TS - 6, 2 * TS + 8, 60, 60) as dd:
        dd.line([(30, 58), (30, 30)], fill=(90, 70, 50), width=3)
        dd.rectangle([0, 0, 59, 32], fill=(246, 240, 220), outline=(40, 40, 40)); dd.text((30, 9), '위험', font=F(11), fill=(170, 20, 20), anchor='mm'); dd.text((30, 23), '티푸스 전염병', font=F(9), fill=(40, 40, 40), anchor='mm')
    for (x, y) in ((12, 7), (17, 7), (19, 9)):
        with Prop(b, x * TS - 4, y * TS + 30, TS + 8, 18) as dd:
            dd.rectangle([0, 4, TS + 7, 12], fill=(120, 96, 70)); dd.rectangle([2, 12, 6, 17], fill=(90, 70, 50)); dd.rectangle([TS, 12, TS + 4, 17], fill=(90, 70, 50))
    exit_path(b, 13, 15, 11 * TS + 2, '↓ 돌아가는 길', col=(170, 160, 140), edge=(130, 120, 100))
    label(b, '베르겐-벨젠 · 1945년 4월 · 해방 직후', 14 * TS + 24, 10 * TS + 30, 12, back=(50, 50, 50, 230))
    m.ev('gate', 14, 2)
    m.ev('tent', 9, 4)
    m.ev('sign', 21, 3)
    m.ev('exit', 14, 12, trigger=1)
    m.ev('ambulance', 18, 4, '!$c_ambulance', dir='left')
    m.ev('officer', 14, 5, '$c_br_officer', dir='down')
    m.ev('nurse', 11, 5, '$c_nurse45', dir='down')
    m.ev('ramc', 8, 6, '$c_ramc', dir='right')
    m.ev('surv1', 12, 7, '$c_survivor', dir='down')
    m.ev('surv2', 17, 7, '$c_survivor2', dir='down')
    m.ev('surv3', 20, 9, '$c_survivor3', dir='left')
    m.ev('elsa45', 16, 9, '$c_elsa42', dir='down')
    m.ev('soldier', 21, 5, '$c_br_sold', dir='left')
    m.ev('soldier2', 7, 9, '$c_br_sold', dir='right')
    m.save(root, vignette=0.14, warm=-0.04)

ALL4 = [studio, berlin, newyork, geneva, london, bletchley, normandy, belsen]
MAP_NAMES = ['01 런던 방송국', '02 베를린 거리', '03 뉴욕 월가', '04 제네바 국제 연맹', '05 런던 공습', '06 블레츨리 파크', '07 노르망디 해변', '08 베르겐-벨젠']

def build(root, only=None):
    from k_common import write_mapinfos
    p = os.path.join(HERE, 'layout.json')
    if only is None and os.path.exists(p): os.remove(p)
    for fn in ALL4:
        if only and fn.__name__ not in only: continue
        fn(root); print('map', fn.__name__)
    write_mapinfos(root, MAP_NAMES)

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2:] or None)
