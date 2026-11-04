"""전보 소년 · 그 시절 나라 깃발 (1884~1919)
 flag(code, w, h=None) -> RGBA 그림.  4배로 크게 그린 뒤 줄여 테두리가 매끈함.
 연도에 따라 바뀌는 깃발은 코드에 연도를 붙임 (미국 별 수: us38 · us45 · us48 / 청 · 중화민국 등)
   uk 영국(유니언 잭)   fr 프랑스        de 독일 제국(검정·하양·빨강)   ah 오스트리아-헝가리(상선기)  hb 합스부르크 왕실기(검정·노랑)
   ru 러시아 제국(하양·파랑·빨강)  it 이탈리아 왕국(사보이 방패)  ot 오스만 제국   be 벨기에   pt 포르투갈 왕국(1910 전)
   es 에스파냐   nl 네덜란드   dk 덴마크   se 스웨덴-노르웨이 연합   us38/us45/us48 미국   jp 일본   qing 청(황룡기)
   eth 에티오피아   serb 세르비아   cfs 콩고 자유국   lib 라이베리아   ch 스위스   redcross 적십자
   pl 폴란드   cz 체코슬로바키아   yu 세르브·크로아트·슬로벤 왕국   fi 핀란드   at 오스트리아(1919)   hu 헝가리
   lt 리투아니아   lv 라트비아   ee 에스토니아   rsfsr 러시아 소비에트(1918)   roc 중화민국 오색기   egy 이집트 술탄국(1914)
"""
import math
from PIL import Image, ImageDraw

RED = (200, 32, 46); WHITE = (250, 250, 248); BLUE = (30, 52, 130); BLACK = (24, 22, 24)
YEL = (250, 206, 40); GREEN = (16, 130, 70); GOLD = (232, 186, 60)
UK_BLUE = (1, 33, 105); UK_RED = (200, 16, 46)
US_RED = (178, 34, 52); US_BLUE = (60, 59, 110)
NAMES = {'us50': '미국', 'frg': '서독', 'gdr': '동독', 'un': '국제 연합', 'prc': '중화 인민 공화국', 'malta': '몰타', 'weimar': '독일(바이마르 공화국)', 'nazi': '나치 독일', 'su': '소련', 'free_fr': '자유 프랑스', 'mk': '만주국', 'roc28': '중화민국', 'uk': '영국', 'fr': '프랑스', 'de': '독일', 'ah': '오스트리아-헝가리', 'hb': '합스부르크 왕실', 'ru': '러시아', 'it': '이탈리아', 'ot': '오스만 제국',
         'be': '벨기에', 'pt': '포르투갈', 'es': '에스파냐', 'nl': '네덜란드', 'dk': '덴마크', 'se': '스웨덴-노르웨이', 'us38': '미국', 'us45': '미국', 'us48': '미국',
         'jp': '일본', 'qing': '청', 'eth': '에티오피아', 'serb': '세르비아', 'cfs': '콩고 자유국', 'lib': '라이베리아', 'ch': '스위스', 'redcross': '적십자',
         'pl': '폴란드', 'cz': '체코슬로바키아', 'yu': '유고슬라비아', 'fi': '핀란드', 'at': '오스트리아', 'hu': '헝가리', 'lt': '리투아니아', 'lv': '라트비아',
         'ee': '에스토니아', 'rsfsr': '소비에트 러시아', 'roc': '중화민국', 'egy': '이집트'}
RATIO = {'us50': 10 / 19, 'frg': 3 / 5, 'gdr': 3 / 5, 'un': 2 / 3, 'prc': 2 / 3, 'malta': 2 / 3, 'uk': 0.5, 'us38': 10 / 19, 'us45': 10 / 19, 'us48': 10 / 19, 'jp': 2 / 3, 'ch': 1.0, 'dk': 28 / 37, 'fi': 11 / 18, 'lib': 10 / 19, 'de': 2 / 3,
         'ru': 2 / 3, 'it': 2 / 3, 'qing': 2 / 3, 'pl': 5 / 8}

def star(d, cx, cy, r, col, rot=-90, inner=0.382):
    pts = []
    for i in range(10):
        a = math.radians(rot + i * 36); rr = r if i % 2 == 0 else r * inner
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    d.polygon(pts, fill=col)

def hstripes(d, W, H, cols, weights=None):
    weights = weights or [1] * len(cols); tot = sum(weights); y = 0
    for c, w in zip(cols, weights):
        y1 = y + H * w / tot; d.rectangle([0, y, W, y1], fill=c); y = y1

def vstripes(d, W, H, cols):
    n = len(cols)
    for i, c in enumerate(cols): d.rectangle([W * i / n, 0, W * (i + 1) / n, H], fill=c)

def crown(d, cx, cy, s, col=GOLD):
    d.polygon([(cx - s, cy + s * 0.5), (cx - s, cy - s * 0.4), (cx - s * 0.5, cy), (cx, cy - s * 0.7), (cx + s * 0.5, cy), (cx + s, cy - s * 0.4), (cx + s, cy + s * 0.5)], fill=col)
    d.rectangle([cx - s, cy + s * 0.35, cx + s, cy + s * 0.65], fill=(200, 150, 40))

def shield(d, cx, cy, w, h, fill, outline=None, ow=0):
    pts = [(cx - w / 2, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2, cy + h * 0.15), (cx, cy + h / 2), (cx - w / 2, cy + h * 0.15)]
    d.polygon(pts, fill=fill)
    if outline: d.line(pts + [pts[0]], fill=outline, width=max(1, int(ow)))

def eagle(d, cx, cy, s, col=BLACK):
    """머리 둘 달린 독수리 / 한 머리 독수리를 아주 줄인 모양"""
    d.polygon([(cx - s, cy - s * 0.3), (cx - s * 0.3, cy - s * 0.1), (cx, cy - s * 0.5), (cx + s * 0.3, cy - s * 0.1), (cx + s, cy - s * 0.3),
               (cx + s * 0.6, cy + s * 0.3), (cx + s * 0.25, cy + s * 0.2), (cx + s * 0.2, cy + s * 0.8), (cx - s * 0.2, cy + s * 0.8), (cx - s * 0.25, cy + s * 0.2), (cx - s * 0.6, cy + s * 0.3)], fill=col)

def draw_uk(d, W, H):
    d.rectangle([0, 0, W, H], fill=UK_BLUE)
    u = W / 60.0
    def band(x0, y0, x1, y1, wdt, col):
        dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy); nx, ny = -dy / L * wdt / 2, dx / L * wdt / 2
        d.polygon([(x0 + nx, y0 + ny), (x1 + nx, y1 + ny), (x1 - nx, y1 - ny), (x0 - nx, y0 - ny)], fill=col)
    band(0, 0, W, H, 6 * u, WHITE); band(0, H, W, 0, 6 * u, WHITE)
    # 붉은 X (성 패트릭): 시계 방향으로 엇갈리게 (깃대 쪽 위에서는 아래로 치우침)
    o = 1.0 * u
    for (x0, y0, x1, y1, sx, sy) in ((0, 0, W / 2, H / 2, 1, -1), (W / 2, H / 2, W, H, -1, 1), (0, H, W / 2, H / 2, 1, 1), (W / 2, H / 2, W, 0, -1, -1)):
        pass
    def red_diag(x0, y0, x1, y1, off):
        dx, dy = x1 - x0, y1 - y0; L = math.hypot(dx, dy); nx, ny = -dy / L, dx / L
        cx0, cy0, cx1, cy1 = x0 + nx * off, y0 + ny * off, x1 + nx * off, y1 + ny * off
        band(cx0, cy0, cx1, cy1, 2 * u, UK_RED)
    red_diag(0, 0, W / 2, H / 2, 1.0 * u); red_diag(W, H, W / 2, H / 2, 1.0 * u)
    red_diag(0, H, W / 2, H / 2, -1.0 * u); red_diag(W, 0, W / 2, H / 2, -1.0 * u)
    d.rectangle([W / 2 - 5 * u, 0, W / 2 + 5 * u, H], fill=WHITE); d.rectangle([0, H / 2 - 5 * u, W, H / 2 + 5 * u], fill=WHITE)
    d.rectangle([W / 2 - 3 * u, 0, W / 2 + 3 * u, H], fill=UK_RED); d.rectangle([0, H / 2 - 3 * u, W, H / 2 + 3 * u], fill=UK_RED)

def draw_us(d, W, H, nstars):
    for i in range(13): d.rectangle([0, H * i / 13, W, H * (i + 1) / 13], fill=US_RED if i % 2 == 0 else WHITE)
    cw, ch = W * 0.4, H * 7 / 13
    d.rectangle([0, 0, cw, ch], fill=US_BLUE)
    rows = {38: [8, 7, 8, 7, 8], 45: [8, 7, 8, 7, 8, 7], 48: [8, 8, 8, 8, 8, 8]}[nstars]
    r = ch / (len(rows) + 1) * 0.42
    for ri, n in enumerate(rows):
        y = ch * (ri + 1) / (len(rows) + 1)
        off = 0 if n == max(rows) or nstars == 48 else cw / (max(rows) + 1) / 2
        for k in range(n):
            x = cw * (k + 1) / (max(rows) + 1) + off
            star(d, x, y, r, WHITE)

def draw_qing(d, W, H):
    d.rectangle([0, 0, W, H], fill=(250, 210, 40))
    # 파란 용: 꼬리(오른쪽 아래)에서 몸을 S자로 꼬아 올라와, 머리가 왼쪽 위 붉은 여의주를 바라봄
    DB, DD = (36, 84, 176), (20, 50, 120)
    pts = []
    for i in range(60):
        t = i / 59
        x = W * (0.88 - 0.6 * t)
        y = H * (0.78 - 0.32 * t) + math.sin(t * math.pi * 2.6) * H * 0.14
        pts.append((x, y))
    for i, (x, y) in enumerate(pts):
        r = H * (0.025 + 0.055 * (i / 59))
        d.ellipse([x - r, y - r, x + r, y + r], fill=DB)
    for i in range(6, 58, 4):      # 등지느러미
        x, y = pts[i]; r = H * (0.025 + 0.055 * (i / 59))
        d.polygon([(x - r * 0.5, y - r * 0.8), (x, y - r * 1.9), (x + r * 0.6, y - r * 0.8)], fill=DD)
    for i in (18, 34, 48):         # 발톱
        x, y = pts[i]
        d.line([(x, y), (x - H * 0.03, y + H * 0.12)], fill=DB, width=max(1, int(H * 0.03)))
        for k in (-1, 0, 1): d.line([(x - H * 0.03, y + H * 0.12), (x - H * 0.03 + k * H * 0.03, y + H * 0.16)], fill=DD, width=max(1, int(H * 0.015)))
    hx, hy = pts[-1]
    d.ellipse([hx - H * 0.1, hy - H * 0.08, hx + H * 0.06, hy + H * 0.08], fill=DB)
    d.polygon([(hx - H * 0.08, hy - H * 0.02), (hx - H * 0.2, hy + H * 0.0), (hx - H * 0.08, hy + H * 0.06)], fill=DB)   # 주둥이
    d.line([(hx, hy - H * 0.06), (hx + H * 0.06, hy - H * 0.18)], fill=DD, width=max(1, int(H * 0.02)))                    # 뿔
    d.line([(hx - H * 0.16, hy + H * 0.02), (hx - H * 0.26, hy + H * 0.1)], fill=DD, width=max(1, int(H * 0.012)))       # 수염
    d.ellipse([hx - H * 0.06, hy - H * 0.04, hx - H * 0.02, hy], fill=(250, 250, 240))
    d.ellipse([W * 0.08, H * 0.1, W * 0.2, H * 0.28], fill=(220, 40, 30))

def draw(code, W, H, d):
    if code == 'uk': draw_uk(d, W, H)
    elif code == 'fr': vstripes(d, W, H, [(0, 85, 164), WHITE, (239, 65, 53)])
    elif code == 'de': hstripes(d, W, H, [BLACK, WHITE, (220, 30, 40)])
    elif code == 'hb': hstripes(d, W, H, [BLACK, YEL])
    elif code == 'ah':
        # 왼쪽 오스트리아(빨강-하양-빨강), 오른쪽 헝가리(빨강-하양-초록) + 작은 문장 두 개
        for i, c in enumerate([RED, WHITE, RED]): d.rectangle([0, H * i / 3, W / 2, H * (i + 1) / 3], fill=c)
        for i, c in enumerate([RED, WHITE, (40, 140, 70)]): d.rectangle([W / 2, H * i / 3, W, H * (i + 1) / 3], fill=c)
        shield(d, W * 0.27, H * 0.5, H * 0.24, H * 0.28, RED, BLACK, H * 0.02); d.rectangle([W * 0.27 - H * 0.11, H * 0.47, W * 0.27 + H * 0.11, H * 0.53], fill=WHITE)
        crown(d, W * 0.27, H * 0.29, H * 0.07)
        shield(d, W * 0.73, H * 0.5, H * 0.24, H * 0.28, RED, BLACK, H * 0.02)
        for k in range(4): d.line([(W * 0.73 - H * 0.11, H * (0.4 + k * 0.05)), (W * 0.73, H * (0.4 + k * 0.05))], fill=WHITE, width=max(1, int(H * 0.015)))
        d.rectangle([W * 0.73 + H * 0.01, H * 0.38, W * 0.73 + H * 0.11, H * 0.6], fill=(40, 140, 70))
        d.line([(W * 0.78, H * 0.4), (W * 0.78, H * 0.58)], fill=WHITE, width=max(1, int(H * 0.025)))
        crown(d, W * 0.73, H * 0.29, H * 0.07)
    elif code == 'ru': hstripes(d, W, H, [WHITE, (0, 57, 166), (213, 43, 30)])
    elif code == 'it':
        vstripes(d, W, H, [(0, 140, 69), WHITE, (205, 33, 42)])
        shield(d, W / 2, H * 0.52, W * 0.15, H * 0.36, (0, 90, 170))
        shield(d, W / 2, H * 0.52, W * 0.12, H * 0.31, (205, 33, 42))
        d.rectangle([W / 2 - W * 0.012, H * 0.4, W / 2 + W * 0.012, H * 0.64], fill=WHITE)
        d.rectangle([W / 2 - W * 0.05, H * 0.47, W / 2 + W * 0.05, H * 0.51], fill=WHITE)
        crown(d, W / 2, H * 0.29, W * 0.04)
    elif code == 'ot':
        d.rectangle([0, 0, W, H], fill=(227, 10, 23))
        cx, cy, r = W * 0.42, H * 0.5, H * 0.26
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
        d.ellipse([cx - r * 0.55, cy - r * 0.82, cx + r * 1.08, cy + r * 0.82], fill=(227, 10, 23))
        star(d, W * 0.6, H * 0.5, H * 0.13, WHITE, rot=180)
    elif code == 'egy':
        d.rectangle([0, 0, W, H], fill=(206, 17, 38))
        for (cx, cy) in ((W * 0.33, H * 0.3), (W * 0.33, H * 0.7), (W * 0.6, H * 0.5)):
            r = H * 0.13
            d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE); d.ellipse([cx - r * 0.5, cy - r * 0.8, cx + r * 1.1, cy + r * 0.8], fill=(206, 17, 38))
            star(d, cx + r * 0.75, cy, r * 0.42, WHITE, rot=180)
    elif code == 'be': vstripes(d, W, H, [BLACK, (253, 218, 36), (239, 51, 64)])
    elif code == 'pt':
        d.rectangle([0, 0, W / 2, H], fill=(0, 56, 168)); d.rectangle([W / 2, 0, W, H], fill=WHITE)
        shield(d, W / 2, H * 0.55, W * 0.2, H * 0.42, WHITE, (200, 30, 40), W * 0.02)
        for (x, y) in ((0, -0.08), (-0.05, 0.02), (0.05, 0.02), (0, 0.12), (0, 0.02)):
            d.rectangle([W * (0.5 + x) - W * 0.016, H * (0.53 + y) - H * 0.03, W * (0.5 + x) + W * 0.016, H * (0.53 + y) + H * 0.03], fill=(0, 56, 168))
        crown(d, W / 2, H * 0.26, W * 0.06)
    elif code == 'es': hstripes(d, W, H, [(170, 21, 27), (241, 191, 0), (170, 21, 27)], [1, 2, 1])
    elif code == 'nl': hstripes(d, W, H, [(174, 28, 40), WHITE, (33, 70, 139)])
    elif code == 'dk':
        d.rectangle([0, 0, W, H], fill=(200, 16, 46)); d.rectangle([W * 12 / 37, 0, W * 16 / 37, H], fill=WHITE); d.rectangle([0, H * 12 / 28, W, H * 16 / 28], fill=WHITE)
    elif code == 'se':
        d.rectangle([0, 0, W, H], fill=(0, 82, 147)); d.rectangle([W * 0.31, 0, W * 0.43, H], fill=(254, 204, 0)); d.rectangle([0, H * 0.4, W, H * 0.6], fill=(254, 204, 0))
        # 연합 표시(깃대 쪽 위): 노르웨이 빨강·파랑과 스웨덴 노랑·파랑을 X자로 나눔
        cw, ch = W * 0.31, H * 0.4
        d.polygon([(0, 0), (cw, 0), (cw / 2, ch / 2)], fill=(186, 12, 47)); d.polygon([(0, ch), (cw, ch), (cw / 2, ch / 2)], fill=(186, 12, 47))
        d.line([(0, 0), (cw, ch)], fill=(254, 204, 0), width=max(1, int(H * 0.04))); d.line([(0, ch), (cw, 0)], fill=(254, 204, 0), width=max(1, int(H * 0.04)))
        d.line([(cw / 2, 0), (cw / 2, ch)], fill=WHITE, width=max(1, int(H * 0.05))); d.line([(0, ch / 2), (cw, ch / 2)], fill=WHITE, width=max(1, int(H * 0.05)))
    elif code in ('us38', 'us45', 'us48'): draw_us(d, W, H, int(code[2:]))
    elif code == 'jp':
        d.rectangle([0, 0, W, H], fill=WHITE); r = H * 0.3; d.ellipse([W / 2 - r, H / 2 - r, W / 2 + r, H / 2 + r], fill=(188, 0, 45))
    elif code == 'qing': draw_qing(d, W, H)
    elif code == 'eth': hstripes(d, W, H, [(7, 137, 48), (252, 221, 9), (218, 18, 26)])
    elif code == 'serb':
        hstripes(d, W, H, [(198, 54, 60), (12, 64, 118), WHITE])
        shield(d, W * 0.35, H * 0.5, H * 0.3, H * 0.4, (198, 54, 60), WHITE, H * 0.02); eagle(d, W * 0.35, H * 0.48, H * 0.11, WHITE); crown(d, W * 0.35, H * 0.22, H * 0.07)
    elif code == 'cfs':
        d.rectangle([0, 0, W, H], fill=(0, 64, 160)); star(d, W / 2, H / 2, H * 0.32, (250, 210, 40))
    elif code == 'lib':
        for i in range(11): d.rectangle([0, H * i / 11, W, H * (i + 1) / 11], fill=(191, 10, 48) if i % 2 == 0 else WHITE)
        s = H * 5 / 11; d.rectangle([0, 0, s, s], fill=(0, 40, 104)); star(d, s / 2, s / 2, s * 0.3, WHITE)
    elif code in ('ch', 'redcross'):
        bg, fg = ((218, 41, 28), WHITE) if code == 'ch' else (WHITE, (218, 41, 28))
        d.rectangle([0, 0, W, H], fill=bg); a = min(W, H)
        d.rectangle([W / 2 - a * 0.1, H / 2 - a * 0.3, W / 2 + a * 0.1, H / 2 + a * 0.3], fill=fg); d.rectangle([W / 2 - a * 0.3, H / 2 - a * 0.1, W / 2 + a * 0.3, H / 2 + a * 0.1], fill=fg)
    elif code == 'pl': hstripes(d, W, H, [WHITE, (220, 20, 60)])
    elif code == 'cz':
        hstripes(d, W, H, [WHITE, (215, 20, 26)]); d.polygon([(0, 0), (W / 2, H / 2), (0, H)], fill=(17, 69, 126))
    elif code == 'yu': hstripes(d, W, H, [(0, 56, 147), WHITE, (206, 17, 38)])
    elif code == 'fi':
        d.rectangle([0, 0, W, H], fill=WHITE); d.rectangle([W * 5 / 18, 0, W * 8 / 18, H], fill=(0, 47, 108)); d.rectangle([0, H * 4 / 11, W, H * 7 / 11], fill=(0, 47, 108))
    elif code == 'at': hstripes(d, W, H, [(200, 16, 46), WHITE, (200, 16, 46)])
    elif code == 'hu': hstripes(d, W, H, [(205, 42, 62), WHITE, (67, 111, 77)])
    elif code == 'lt': hstripes(d, W, H, [(253, 185, 19), (0, 106, 68), (193, 39, 45)])
    elif code == 'lv': hstripes(d, W, H, [(158, 48, 57), WHITE, (158, 48, 57)], [2, 1, 2])
    elif code == 'ee': hstripes(d, W, H, [(0, 114, 206), BLACK, WHITE])
    elif code == 'rsfsr':
        d.rectangle([0, 0, W, H], fill=(204, 0, 0))
        d.rectangle([W * 0.06, H * 0.08, W * 0.3, H * 0.34], outline=(250, 210, 60), width=max(1, int(H * 0.03)))
    elif code == 'roc': hstripes(d, W, H, [(222, 41, 16), (255, 222, 0), (24, 82, 168), WHITE, BLACK])
    elif code == 'weimar': hstripes(d, W, H, [BLACK, (221, 0, 0), (255, 206, 0)])
    elif code == 'nazi':       # 사료 카드에서만 사용 (교과서 사료 수준)
        d.rectangle([0, 0, W, H], fill=(204, 0, 0))
        cx, cy, r = W / 2, H / 2, H * 0.36
        d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=WHITE)
        a = r * 0.62; t = r * 0.15
        import math as _m
        pts = []
        def rot(x, y): c, s_ = _m.cos(_m.radians(45)), _m.sin(_m.radians(45)); return (cx + x * c - y * s_, cy + x * s_ + y * c)
        segs = [((-t, -a), (t, a)), ((-a, -t), (a, t)), ((-t, -a), (a, -a + 2 * t)), ((a - 2 * t, -t), (a, a)), ((-a, a - 2 * t), (t, a)), ((-a, -a), (-a + 2 * t, t))]
        for (x0, y0), (x1, y1) in segs:
            d.polygon([rot(x0, y0), rot(x1, y0), rot(x1, y1), rot(x0, y1)], fill=BLACK)
    elif code == 'su':
        d.rectangle([0, 0, W, H], fill=(204, 0, 0))
        g = (250, 210, 60); u = H / 10
        star(d, W * 0.13, H * 0.13, u * 0.6, g)
        d.arc([W * 0.06, H * 0.2, W * 0.06 + u * 2.4, H * 0.2 + u * 2.4], 200, 60, fill=g, width=max(1, int(u * 0.35)))
        d.line([(W * 0.07, H * 0.42), (W * 0.15, H * 0.3)], fill=g, width=max(1, int(u * 0.35)))
        d.rectangle([W * 0.12, H * 0.24, W * 0.17, H * 0.29], fill=g)
    elif code == 'free_fr':
        vstripes(d, W, H, [(0, 85, 164), WHITE, (239, 65, 53)])
        cx = W / 2; c = (220, 30, 40); w_ = max(1, int(W * 0.03))
        d.rectangle([cx - w_ / 2, H * 0.22, cx + w_ / 2, H * 0.8], fill=c)
        d.rectangle([cx - W * 0.06, H * 0.32, cx + W * 0.06, H * 0.32 + w_], fill=c); d.rectangle([cx - W * 0.09, H * 0.44, cx + W * 0.09, H * 0.44 + w_], fill=c)
    elif code == 'mk':
        d.rectangle([0, 0, W, H], fill=(255, 210, 0))
        for k, c in enumerate([(220, 30, 30), (20, 50, 160), WHITE, BLACK]): d.rectangle([0, H / 3 * k / 4 * 4 / 4 * 1, W / 3, H / 3 * (k + 1) / 4 * 4 / 4], fill=c) if False else d.rectangle([0, k * H / 12, W / 3, (k + 1) * H / 12], fill=c)
    elif code == 'roc28':
        d.rectangle([0, 0, W, H], fill=(254, 0, 0))
        d.rectangle([0, 0, W / 2, H / 2], fill=(0, 0, 149))
        cx, cy, r = W / 4, H / 4, H * 0.17
        for k in range(12):
            a = math.radians(k * 30)
            d.polygon([(cx + math.cos(a) * r, cy + math.sin(a) * r), (cx + math.cos(a + 0.26) * r * 0.55, cy + math.sin(a + 0.26) * r * 0.55), (cx + math.cos(a - 0.26) * r * 0.55, cy + math.sin(a - 0.26) * r * 0.55)], fill=WHITE)
        d.ellipse([cx - r * 0.5, cy - r * 0.5, cx + r * 0.5, cy + r * 0.5], fill=WHITE)
    elif code == 'us50':
        for i in range(13): d.rectangle([0, H * i / 13, W, H * (i + 1) / 13], fill=US_RED if i % 2 == 0 else WHITE)
        cw, ch = W * 0.4, H * 7 / 13
        d.rectangle([0, 0, cw, ch], fill=US_BLUE)
        r = ch / 10 * 0.42
        for ri in range(9):
            n = 6 if ri % 2 == 0 else 5
            for k in range(n):
                x = cw * (2 * k + 1 + (0 if n == 6 else 1)) / 12
                star(d, x, ch * (ri + 1) / 10, r, WHITE)
    elif code in ('frg', 'gdr'):
        hstripes(d, W, H, [BLACK, (221, 0, 0), (255, 206, 0)])
        if code == 'gdr':
            cx, cy, R = W / 2, H / 2, H * 0.3
            d.ellipse([cx - R, cy - R, cx + R, cy + R], fill=(200, 160, 40))
            d.ellipse([cx - R * 0.8, cy - R * 0.8, cx + R * 0.8, cy + R * 0.8], fill=(221, 0, 0))
            d.line([(cx - R * 0.45, cy + R * 0.5), (cx + R * 0.45, cy - R * 0.4)], fill=YEL, width=max(2, int(H * 0.03)))
            d.line([(cx - R * 0.4, cy - R * 0.35), (cx + R * 0.45, cy + R * 0.5)], fill=BLACK, width=max(2, int(H * 0.03)))
            d.arc([cx - R * 0.5, cy - R * 0.55, cx + R * 0.5, cy + R * 0.45], 200, 340, fill=YEL, width=max(2, int(H * 0.025)))
    elif code == 'un':
        d.rectangle([0, 0, W, H], fill=(74, 146, 219))
        cx, cy, R = W / 2, H * 0.47, H * 0.3
        for k in range(1, 5): d.ellipse([cx - R * k / 4, cy - R * k / 4, cx + R * k / 4, cy + R * k / 4], outline=WHITE, width=max(1, int(H * 0.015)))
        for k in range(8):
            a = math.radians(k * 45); d.line([(cx, cy), (cx + math.cos(a) * R, cy + math.sin(a) * R)], fill=WHITE, width=max(1, int(H * 0.012)))
        d.arc([cx - R * 1.35, cy - R * 1.3, cx + R * 1.35, cy + R * 1.35], 30, 150, fill=WHITE, width=max(2, int(H * 0.04)))
    elif code == 'prc':
        d.rectangle([0, 0, W, H], fill=(222, 41, 16))
        star(d, W * 5 / 30, H * 5 / 20, H * 3 / 20, YEL)
        for (x, y) in ((10, 2), (12, 4), (12, 7), (10, 9)):
            star(d, W * x / 30, H * y / 20, H * 1 / 20, YEL, rot=-90 + math.degrees(math.atan2(5 - y, 5 - x)))
    elif code == 'malta':
        d.rectangle([0, 0, W / 2, H], fill=WHITE); d.rectangle([W / 2, 0, W, H], fill=(207, 20, 43))
        d.rectangle([W * 0.06, H * 0.08, W * 0.18, H * 0.26], fill=(160, 160, 166), outline=(200, 30, 40))
    elif code == 'kr':
        import k_arch
        return 'kr'
    else: raise KeyError(code)

def flag(code, w, h=None, border=False):
    if h is None: h = int(round(w * RATIO.get(code, 2 / 3)))
    if code == 'kr':
        import k_arch
        return g_arch.taegeukgi(w, h).convert('RGBA')
    S = 4
    big = Image.new('RGBA', (w * S, h * S), (0, 0, 0, 0)); d = ImageDraw.Draw(big)
    draw(code, w * S, h * S, d)
    im = big.resize((w, h), Image.LANCZOS)
    if border:
        ImageDraw.Draw(im).rectangle([0, 0, w - 1, h - 1], outline=(60, 50, 40))
    return im

def waving(code, w, h=None, amp=0.06, phase=0.0, shade=True):
    """펄럭이는 깃발 (세로로 출렁이고 접힌 곳에 그늘)"""
    im = flag(code, w, h); h = im.height
    pad = int(h * amp) + 2
    out = Image.new('RGBA', (w, h + pad * 2), (0, 0, 0, 0))
    for x in range(w):
        t = x / max(1, w - 1)
        dy = math.sin(t * math.pi * 2.0 + phase) * h * amp * t
        col = im.crop((x, 0, x + 1, h))
        if shade:
            k = 0.86 + 0.14 * math.cos(t * math.pi * 2.0 + phase)
            col = Image.eval(col, lambda v, k=k: int(v * k)) if False else col.point(lambda v, k=k: int(v * k))
            col.putalpha(im.crop((x, 0, x + 1, h)).split()[3])
        out.alpha_composite(col, (x, int(pad + dy)))
    return out

if __name__ == '__main__':
    import sys, os
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    codes = list(NAMES)
    cols = 6
    sheet = Image.new('RGB', (cols * 170, ((len(codes) + cols - 1) // cols) * 120), (200, 196, 186))
    from k_common import F
    dd = ImageDraw.Draw(sheet)
    for i, c in enumerate(codes):
        x, y = (i % cols) * 170 + 15, (i // cols) * 120 + 10
        im = flag(c, 140, None, border=True)
        sheet.paste(im, (x, y), im)
        dd.text((x, y + 96), c + ' ' + NAMES[c], font=F(13), fill=(20, 20, 20))
    sheet.save(sys.argv[1])
