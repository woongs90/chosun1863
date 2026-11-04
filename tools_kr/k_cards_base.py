"""전보 소년 확대 그림(카드) - img/pictures (800x450)
 cu_*  확대 카드(사료·지도·전보·정리)   cu_tel0~6 전보   cu_album + cu_album_ov0~6 전보철(겹치기)   it_* 가방 아이콘
 지도: historical-basemaps (Ourednik, GPL-3.0) 의 1880 · 1900 · 1914 · 1920년 국경 자료로 그림
"""
import numpy as np
import os, sys, json, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageOps
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'tools'))
from k_common import F, TS
from hd_art import sh, mix, outline
import k_arch as A

CW, CH = 800, 450
INK = (44, 36, 30)
RED = (170, 40, 40)
BLUE = (40, 70, 140)
OUT = None
ROOT = None

def S(im, name):
    im.save(os.path.join(OUT, name + '.png'))

def paper(w=CW, h=CH, kind='paper', seed=1):
    rnd = random.Random(seed)
    base = {'paper': (242, 232, 208), 'news': (232, 226, 210), 'letter': (246, 240, 224), 'dark': (40, 36, 34), 'blue': (226, 232, 238), 'white': (248, 246, 240)}[kind]
    im = Image.new('RGBA', (w, h), base + (255,))
    d = ImageDraw.Draw(im)
    for _ in range(int(w * h / 900)):
        x, y = rnd.randint(0, w - 1), rnd.randint(0, h - 1)
        c = sh(base, 0.94 + rnd.random() * 0.1)
        d.rectangle([x, y, x + rnd.randint(1, 3), y + rnd.randint(1, 3)], fill=c)
    if kind in ('paper', 'letter', 'news'):
        edge = Image.new('L', (w, h), 0); ed = ImageDraw.Draw(edge)
        ed.rectangle([0, 0, w - 1, h - 1], outline=255, width=14)
        edge = edge.filter(ImageFilter.GaussianBlur(10))
        im.paste(Image.new('RGBA', (w, h), sh(base, 0.82) + (255,)), (0, 0), edge)
    d = ImageDraw.Draw(im)
    d.rectangle([0, 0, w - 1, h - 1], outline=sh(base, 0.6), width=2)
    return im

def wrap(d, text, font, maxw):
    out = []
    for para in str(text).split('\n'):
        words = para.split(' '); line = ''
        for w_ in words:
            t = (line + ' ' + w_).strip()
            if d.textlength(t, font=font) <= maxw: line = t
            else:
                if line: out.append(line)
                line = w_
                while d.textlength(line, font=font) > maxw:
                    k = len(line)
                    while k > 1 and d.textlength(line[:k], font=font) > maxw: k -= 1
                    out.append(line[:k]); line = line[k:]
        out.append(line)
    return out

def text_block(d, x, y, w, text, size=21, col=INK, kind='sans', gap=7, bullet=None, max_h=None):
    f = F(size, kind)
    yy = y
    for para in (text if isinstance(text, list) else [text]):
        lines = wrap(d, para, f, w - (22 if bullet else 0))
        for i, ln in enumerate(lines):
            if bullet and i == 0:
                d.text((x, yy), bullet, font=f, fill=RED if bullet != '·' else col)
            d.text((x + (22 if bullet else 0), yy), ln, font=f, fill=col)
            yy += size + gap
        yy += 4
    return yy

def title(d, text, y=22, size=30, col=INK, sub=None, w=CW):
    d.text((w / 2, y + size / 2), text, font=F(size, 'serif'), fill=col, anchor='mm')
    yy = y + size + 8
    if sub:
        d.text((w / 2, yy + 9), sub, font=F(17), fill=sh(col, 1.6) if sum(col) < 300 else (110, 100, 90), anchor='mm')
        yy += 24
    d.line([(60, yy + 4), (w - 60, yy + 4)], fill=(170, 140, 100), width=2)
    return yy + 16

def tag(d, x, y, text, col=(150, 40, 40), size=15):
    f = F(size); tw = d.textlength(text, font=f)
    d.rounded_rectangle([x, y, x + tw + 18, y + size + 10], 6, fill=col)
    d.text((x + 9, y + 5), text, font=f, fill=(255, 250, 240))
    return x + tw + 24

def footnote(d, text, w=CW, h=CH, col=(120, 104, 86)):
    d.text((w / 2, h - 22), text, font=F(14, 'reg'), fill=col, anchor='mm')

def card(name, head, lines, sub=None, label=None, note=None, kind='paper', art=None, art_w=0, size=21, seed=1, bullet='•'):
    im = paper(kind=kind, seed=seed); d = ImageDraw.Draw(im)
    if label: tag(d, 24, 18, label)
    y = title(d, head, sub=sub)
    x0 = 48
    w = CW - 96 - (art_w + 20 if art is not None else 0)
    if art is not None:
        ax = CW - 48 - art_w
        im.alpha_composite(art, (ax, y + 6)); d = ImageDraw.Draw(im)
    text_block(d, x0, y + 4, w, lines, size=size, bullet=bullet)
    if note: footnote(d, note)
    S(im, name)
    return im

# ------------------------------------------------------------------ 지도 (실제 해안선: world-atlas 10m)
GEO = None
def geo_map(im, box, lon=(124.0, 130.8), lat=(33.0, 43.2), land=(226, 214, 176), sea=(150, 192, 220), line=(110, 92, 70)):
    global GEO
    if GEO is None: GEO = json.load(open(os.path.join(HERE, 'k_geo.json')))
    x0, y0, x1, y1 = box
    sx = (x1 - x0) / (lon[1] - lon[0]); sy = (y1 - y0) / (lat[1] - lat[0])
    s = min(sx, sy * 1.0)
    cxl = (lon[0] + lon[1]) / 2; cyl = (lat[0] + lat[1]) / 2
    kx = math.cos(math.radians(cyl))
    s = min((x1 - x0) / ((lon[1] - lon[0]) * kx), (y1 - y0) / (lat[1] - lat[0]))
    def P(lo, la): return (x0 + (x1 - x0) / 2 + (lo - cxl) * kx * s, y0 + (y1 - y0) / 2 - (la - cyl) * s)
    lay = Image.new('RGBA', im.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.rectangle(box, fill=sea)
    for ring in GEO:
        pts = [P(lo, la) for lo, la in ring]
        if len(pts) > 2: d.polygon(pts, fill=land, outline=line)
    mask = Image.new('L', im.size, 0); ImageDraw.Draw(mask).rectangle(box, fill=255)
    im.paste(lay, (0, 0), Image.composite(lay.split()[3], Image.new('L', im.size, 0), mask))
    ImageDraw.Draw(im).rectangle(box, outline=(120, 100, 80), width=2)
    return P

MDL = [(126.1, 37.72), (126.68, 37.95), (127.0, 38.12), (127.3, 38.3), (127.6, 38.3), (127.9, 38.32), (128.1, 38.45), (128.36, 38.62)]
CITIES = {'서울': (126.98, 37.57), '평양': (125.75, 39.03), '개성': (126.55, 37.97), '해주': (125.72, 38.04), '부산': (129.04, 35.1), '함흥': (127.53, 39.92),
          '흥남': (127.62, 39.83), '인천': (126.63, 37.46), '대구': (128.6, 35.87), '제주': (126.53, 33.5), '정읍': (126.86, 35.57), '판문점': (126.68, 37.96),
          '원산': (127.44, 39.15), '대전': (127.38, 36.35), '신의주': (124.4, 40.1), '혜산': (128.18, 41.4), '낙동강': (128.4, 35.6)}

def dot(d, P, name, dx=8, dy=-10, col=INK, size=15, r=4):
    x, y = P(*CITIES[name])
    d.ellipse([x - r, y - r, x + r, y + r], fill=col)
    d.text((x + dx, y + dy), name, font=F(size), fill=col)

def line38(d, P, col=(190, 40, 40), w=3, dash=True):
    a = P(124.0, 38.0); b = P(130.0, 38.0)
    if dash:
        n = 40
        for k in range(n):
            if k % 2 == 0:
                d.line([(a[0] + (b[0] - a[0]) * k / n, a[1]), (a[0] + (b[0] - a[0]) * (k + 1) / n, a[1])], fill=col, width=w)
    else: d.line([a, b], fill=col, width=w)

NK_BORDER = [(124.2, 39.85), (124.9, 40.35), (125.6, 40.75), (126.4, 41.35), (126.9, 41.8), (127.6, 41.45), (128.1, 41.4), (128.3, 42.0), (129.2, 42.2), (129.7, 42.45), (130.4, 42.6), (130.7, 42.3)]
def zone_tint(im, P, box, north=(232, 150, 196), south=(140, 182, 236), land=(226, 214, 176)):
    """사진처럼 38도선 북쪽(소련군)·남쪽(미군) 땅에 색 칠하기 (한반도만)"""
    a = np.array(im.convert('RGB')).astype(int)
    isl = (np.abs(a - np.array(land)).sum(axis=2) < 12)
    for poly, col in (([(123.8, 38.0), (123.8, 39.85)] + NK_BORDER + [(131.2, 42.3), (131.2, 38.0)], north),
                      ([(123.8, 38.0), (131.2, 38.0), (131.2, 35.6), (129.45, 35.05), (129.0, 34.6), (127.0, 32.9), (123.8, 32.9)], south)):
        m = Image.new('L', im.size, 0); ImageDraw.Draw(m).polygon([P(*q) for q in poly], fill=255)
        bm = Image.new('L', im.size, 0); ImageDraw.Draw(bm).rectangle(box, fill=255)
        sel = isl & (np.array(m) > 0) & (np.array(bm) > 0)
        t = Image.new('RGBA', im.size, col + (255,))
        im.paste(t, (0, 0), Image.fromarray((sel * 255).astype('uint8')))

def line38_land(d, P, col=(30, 26, 24), w=3):
    """한반도를 가로지르는 북위 38도선 (실선)"""
    d.line([P(124.3, 38.0), P(129.6, 38.0)], fill=col, width=w)

def mdl(d, P, col=(190, 40, 40), w=4):
    d.line([P(*p) for p in MDL], fill=col, width=w)

def arrow(d, pts, col=(190, 40, 40), w=5):
    d.line(pts, fill=col, width=w)
    (x1, y1), (x2, y2) = pts[-2], pts[-1]
    a = math.atan2(y2 - y1, x2 - x1)
    d.polygon([(x2 + math.cos(a) * 10, y2 + math.sin(a) * 10), (x2 + math.cos(a + 2.4) * 14, y2 + math.sin(a + 2.4) * 14), (x2 + math.cos(a - 2.4) * 14, y2 + math.sin(a - 2.4) * 14)], fill=col)

# ------------------------------------------------------------------ 사진 (게임 그림으로 다시 그린 장면)
def sprite(name, row=0, col=1):
    im = Image.open(os.path.join(ROOT, 'img/characters', name + '.png')).convert('RGBA')
    fw, fh = im.width // 3, im.height // 4
    return im.crop((col * fw, row * fh, col * fw + fw, row * fh + fh))

DIRROW = {'down': 0, 'left': 1, 'right': 2, 'up': 3}
def scene(par, cx, cy, people, w=480, h=270, top=True, scale=2, extra=None):
    """원경 그림의 (cx, cy) 둘레를 잘라 인물을 세우고 2배 확대 → 960x540 장면"""
    base = Image.open(os.path.join(ROOT, 'img/parallaxes', par + '.png')).convert('RGBA')
    tp = os.path.join(ROOT, 'img/parallaxes', par + '_top.png')
    x0 = int(cx - w / 2); y0 = int(cy - h / 2)
    lay = base.copy()
    for p in sorted(people, key=lambda q: q[2]):
        name, tx, ty = p[0], p[1], p[2]
        dr = p[3] if len(p) > 3 else 'down'
        fr = sprite(name, DIRROW[dr], 1 if len(p) <= 4 else p[4])
        ox = int(tx * TS) if isinstance(tx, float) else tx * TS
        oy = int(ty * TS) if isinstance(ty, float) else ty * TS
        sh_ = Image.new('RGBA', (48, 48), (0, 0, 0, 0)); ImageDraw.Draw(sh_).ellipse([12, 38, 36, 46], fill=(0, 0, 0, 70))
        lay.alpha_composite(sh_, (ox, oy))
        lay.alpha_composite(fr, (ox, oy))
    if top and os.path.exists(tp): lay.alpha_composite(Image.open(tp).convert('RGBA'))
    if extra: extra(lay)
    crop = lay.crop((x0, y0, x0 + w, y0 + h))
    return crop.resize((w * scale, h * scale), Image.NEAREST)

def sepia(im, amount=1.0):
    g = ImageOps.grayscale(im.convert('RGB'))
    sep = ImageOps.colorize(g, (40, 26, 16), (246, 232, 204))
    if amount < 1: sep = Image.blend(im.convert('RGB'), sep, amount)
    return sep.convert('RGBA')

def toned(im, tone):
    """bw: 흑백 / faded: 바랜 컬러(1970년대) / color: 컬러"""
    if tone == 'bw':
        g = ImageOps.grayscale(im.convert('RGB')); return ImageOps.colorize(g, (24, 22, 22), (240, 238, 232)).convert('RGBA')
    if tone == 'faded':
        from PIL import ImageEnhance
        c = ImageEnhance.Color(im.convert('RGB')).enhance(0.55)
        warm = Image.new('RGB', c.size, (240, 200, 140))
        return Image.blend(c, warm, 0.16).convert('RGBA')
    return im.convert('RGBA')

def print_card(name, src, caption, date, note='당시 사진을 바탕으로 게임 그림으로 다시 그렸어요', tone='bw'):
    """인화한 사진 카드 (흰 테두리 + 손글씨 메모)"""
    im = paper(kind='dark', seed=7)
    d = ImageDraw.Draw(im)
    ph = toned(src, tone).resize((560, 315), Image.LANCZOS)
    ph = ImageOps.expand(ph, border=12, fill=(246, 242, 230))
    ph = ImageOps.expand(ph, border=0)
    ph2 = Image.new('RGBA', (ph.width, ph.height + 44), (246, 242, 230, 255)); ph2.paste(ph, (0, 0))
    dd = ImageDraw.Draw(ph2)
    dd.text((ph2.width / 2, ph.height + 18), caption, font=F(18, 'serif'), fill=(60, 50, 40), anchor='mm')
    rot = ph2.rotate(-1.6, expand=True, resample=Image.BICUBIC, fillcolor=(0, 0, 0, 0))
    shadow = Image.new('RGBA', rot.size, (0, 0, 0, 0)); shadow.putalpha(rot.split()[3].point(lambda v: 110 if v > 0 else 0))
    shadow = shadow.filter(ImageFilter.GaussianBlur(6))
    px_ = (CW - rot.width) // 2; py_ = 8
    im.alpha_composite(shadow, (px_ + 6, py_ + 8)); im.alpha_composite(rot, (px_, py_))
    d = ImageDraw.Draw(im)
    d.text((CW - 30, CH - 18), date, font=F(15), fill=(230, 210, 170), anchor='rm')
    d.text((30, CH - 18), note, font=F(12, 'reg'), fill=(170, 160, 150), anchor='lm')
    S(im, name)
    return ph

# ------------------------------------------------------------------ 편지
def letter(name, head, lines, sign, date):
    im = paper(kind='letter', seed=len(name)); d = ImageDraw.Draw(im)
    for yy in range(70, CH - 30, 34): d.line([(50, yy), (CW - 50, yy)], fill=(206, 196, 176))
    d.text((60, 30), head, font=F(22, 'serif'), fill=(60, 50, 80))
    y = 74
    for ln in lines:
        for l2 in wrap(d, ln, F(20, 'serif'), CW - 130):
            d.text((70, y), l2, font=F(20, 'serif'), fill=(50, 44, 70)); y += 34
    d.text((CW - 70, CH - 56), sign, font=F(20, 'serif'), fill=(60, 50, 80), anchor='rm')
    d.text((CW - 70, CH - 28), date, font=F(15, 'serif'), fill=(110, 100, 120), anchor='rm')
    S(im, name)

# ------------------------------------------------------------------ 실존 인물 카드 (똑같은 틀)
def person_card(name, who, years, role, lines, pt):
    im = paper(kind='paper', seed=hash(name) % 99); d = ImageDraw.Draw(im)
    tag(d, 24, 18, '실존 인물')
    por = Image.open(os.path.join(OUT, pt + '.png')).convert('RGBA')
    frame = Image.new('RGBA', (por.width + 16, por.height + 16), (120, 90, 60, 255))
    frame.paste(Image.new('RGBA', (por.width + 8, por.height + 8), (220, 210, 190, 255)), (4, 4))
    frame.alpha_composite(por, (8, 8))
    im.alpha_composite(frame, (40, 70)); d = ImageDraw.Draw(im)
    x0 = 330
    d.text((x0, 64), who, font=F(34, 'serif'), fill=INK)
    d.text((x0 + d.textlength(who, font=F(34, 'serif')) + 14, 78), years, font=F(18), fill=(110, 96, 80))
    d.text((x0, 112), role, font=F(18), fill=RED)
    text_block(d, x0, 150, CW - x0 - 40, lines, size=19, bullet='·', gap=6)
    footnote(d, '게임 속 대사는 남긴 말과 기록을 바탕으로 쉽게 꾸민 것이에요', w=CW)
    S(im, name)

# ==================================================================== 카드 목록

def portrait_art(pt, w=150):
    im = Image.open(os.path.join(OUT, pt + '.png')).convert('RGBA')
    im = im.resize((w, int(w * im.height / im.width)), Image.NEAREST)
    fr = Image.new('RGBA', (im.width + 12, im.height + 12), (120, 90, 60, 255))
    fr.paste(Image.new('RGBA', (im.width + 4, im.height + 4), (220, 210, 190, 255)), (4, 4)); fr.alpha_composite(im, (6, 6))
    return fr

# ------------------------------------------------------------------ 후기 안내 (엔딩 뒤, QR 포함)
REVIEW_URL = 'https://forms.gle/9PfM9UU7hb5RcCwd6'
def review_card(url=REVIEW_URL, name='cu_review'):
    import io
    try:
        import segno
    except ImportError:
        print('  (segno 가 없어 QR 없이 만듭니다: pip install segno)'); segno = None
    im = paper(seed=44); d = ImageDraw.Draw(im)
    title(d, '후기를 남겨 주세요!')
    if segno:
        buf = io.BytesIO()
        segno.make(url, error='m').save(buf, kind='png', scale=7, border=2, dark='#2a1a10', light='#fffaf0')
        qr = Image.open(io.BytesIO(buf.getvalue())).convert('RGB').resize((236, 236), Image.NEAREST)
        im.paste(qr, (500, 96)); d = ImageDraw.Draw(im)
        d.rectangle([496, 92, 739, 335], outline=(120, 84, 50), width=3)
    y = 112
    for line, col, sz in (('끝까지 함께해 줘서', INK, 26), ('고마워요!', INK, 26), ('', INK, 10),
                          ('휴대폰으로 QR을 찍거나,', INK, 20), ('[후기 남기기] 단추를 누르면', RED, 20), ('새 창이 열려요.', RED, 20)):
        if line: d.text((70, y), line, font=F(sz), fill=col)
        y += sz + 16
    d.text((618, 360), url.replace('https://', ''), font=F(15), fill=(110, 80, 50), anchor='mm')
    S(im, name)

