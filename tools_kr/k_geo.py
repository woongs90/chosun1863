"""전보 소년 · 옛 국경 지도 그리기
 지도 자료: historical-basemaps (Ourednik, GPL-3.0) 1880 · 1900 · 1914 · 1920 년 국경 (geo 폴더)
 render(year, box, size, ...) -> RGB 그림.  나라를 '지배하는 나라' 기준으로 칠함 (영국 식민지는 영국 색).
"""
import json, os, math, random
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
GEO = os.path.join(HERE, 'geo')

# ------------------------------------------------------------------ 지배하는 나라 묶기
P = {}
def _set(key, *names):
    for n in names: P[n] = key
_set('uk', 'United Kingdom', 'United Kingdom of Great Britain and Ireland', 'Great Britain', 'Cape Colony', 'Natal', 'Canada', 'Australia', 'New Zealand', 'Ceylon',
     'British Guiana', 'Gambia', 'Gambia, The', 'Sierra Leone', 'Lagos', 'Basutoland', 'Lesotho', 'Malaya', 'Brunei', 'Belize', 'Malta', 'Uganda', 'Swaziland', 'Accra',
     'Union of South Africa', 'Kenya', 'Nigeria', 'Ghana', 'Sudan', 'Zambia', 'Zimbabwe', 'Malawi', 'Tanzania, United Republic of', 'Botswana', 'Trinidad', 'Jamaica',
     'Malaysia', 'Trucial Oman', 'Kuwait', 'India', 'Griqualand West', 'New South Wales (UK)', 'Northern Territory (UK)', 'Queensland (UK)', 'South Australia (UK)',
     'Victoria (UK)', 'Western Australia (UK)', 'Guyana', 'Barbados', 'Grenada', 'Saint Lucia', 'Saint Vincent and the Grenadines', 'Montserrat', 'Anguilla',
     'Antigua and Barbuda', 'Dominica', 'Saint Kitts and Nevis', 'Fiji', 'Niue', 'Tonga', 'Opobo', 'Calabar', 'Iceland_x')
_set('fr', 'France', 'Algeria', 'Senegal', 'Tunisia', 'Gabon', 'Ivory Coast', 'Madagascar (France)', 'French Indo-China', 'French Indochina', 'Annam', 'Cochin China',
     'French Guiana', 'Guadeloupe', 'Martinique', 'Cotonou', 'Togo', 'Wallis and Futuna Islands', 'Saint Barthelemy', 'Saint Martin')
_set('de', 'Germany', 'German Empire', 'German South-West Africa', 'Kamerun', 'Togoland', 'East Prussia')
_set('be', 'Belgium', 'Zaire (Belgium)', 'Rwanda (Belgium)', 'Burundi_1920')
_set('cfs', 'Congo')
_set('pt', 'Portugal', 'Angola', 'Portuguese East Africa', 'Portuguese Guinea', 'Mozambique', 'Guinea-Bissau')
_set('es', 'Spain', 'Spanish Guinea', 'Rio De Oro', 'Spanish Morocco', 'Equatorial Guinea', 'Spanish Sahara')
_set('it', 'Italy', 'Eritrea')
_set('nl', 'Netherlands', 'Netherlands Indies', 'Dutch East Indies', 'Dutch Guiana', 'Suriname', 'Netherlands Antilles')
_set('ot', 'Ottoman Empire', 'Ottoman Sultanate')
_set('ru', 'Russian Empire', 'Russia', 'USSR', 'Far Eastern SSR', 'South Russia', 'White Russia', 'Ukraine', 'central Asian khanates_x', 'Bokhara Khanate_x')
_set('jp', 'Imperial Japan', 'Empire of Japan')
_set('ah', 'Austria Hungary', 'Austro-Hungarian Empire', 'Bosnia-Herzegovina')
_set('us', 'United States of America', 'United States', 'Puerto Rico', 'American Samoa', 'United States Virgin Islands')
_set('qing', 'Manchu Empire', 'Chinese Warlords', 'Manchuria', 'Xinjiang', 'Tibet', 'Mongolia')
_set('dk', 'Denmark', 'Greenland', 'Iceland')

YEAR_FIX = {
    1880: {'Egypt': 'ot', 'Harer (Egypt)': 'ot', 'Taiwan': 'qing', 'Korea': 'ind', 'Finland': 'ru', 'Kingdom of Hawaii': 'ind', 'Philippines': 'es', 'Morocco': 'ind', 'Tunisia': 'ind'},
    1900: {'Egypt': 'uk', 'Harer (Egypt)': 'eth', 'Taiwan': 'jp', 'Korea': 'ind', 'Finland': 'ru', 'Kingdom of Hawaii': 'us', 'Philippines': 'us', 'Morocco': 'ind', 'Tunisia': 'fr'},
    1914: {'Taiwan': 'jp', 'Korea': 'jp', 'Finland': 'ru', 'Philippines': 'us', 'Morocco': 'fr', 'Armenia': 'ru', 'Azerbaijan': 'ru', 'Georgia': 'ru', 'Abyssinia': 'eth',
           'Kuwait': 'uk', 'Qatar': 'ind', 'Albania': 'ind'},
    1920: {'Philippines': 'us', 'Morocco': 'fr', 'Hejaz': 'ind', 'Ethiopia': 'eth', 'Burundi': 'be', 'Annam': 'fr', 'Cochin China': 'fr'},
}
LIBERIA = {'Liberia'}

def owner(props, year):
    sub = props.get('SUBJECTO') or props.get('NAME') or ''
    name = props.get('NAME') or ''
    fx = YEAR_FIX.get(year, {})
    for k in (name, sub):
        if k in fx: return fx[k]
    if sub in ('Ethiopia', 'Abyssinia') or name in ('Ethiopia', 'Abyssinia'): return 'eth'
    if sub in LIBERIA: return 'lib'
    if name in P: return P[name]
    if sub in P: return P[sub]
    return 'ind'

_cache = {}
def load(year):
    if year in _cache: return _cache[year]
    d = json.load(open(os.path.join(GEO, 'world_%s.geojson' % (year if isinstance(year, str) else '%d' % year)), encoding='utf-8'))
    feats = []
    for f in d['features']:
        g = f.get('geometry')
        if not g: continue
        polys = g['coordinates'] if g['type'] == 'MultiPolygon' else [g['coordinates']] if g['type'] == 'Polygon' else []
        feats.append((f['properties'], polys))
    _cache[year] = feats
    return feats

# ------------------------------------------------------------------ 색
COL = {'uk': (222, 112, 112), 'fr': (110, 146, 206), 'de': (128, 124, 120), 'be': (178, 126, 196), 'cfs': (178, 126, 196), 'pt': (120, 176, 98),
       'es': (236, 196, 110), 'it': (98, 182, 160), 'nl': (238, 150, 70), 'ot': (204, 150, 96), 'ru': (150, 186, 120), 'jp': (236, 170, 186),
       'ah': (226, 204, 104), 'us': (140, 120, 186), 'qing': (238, 222, 150), 'eth': (246, 242, 226), 'lib': (246, 242, 226), 'ind': (226, 216, 190), 'dk': (200, 200, 200)}
SEA = (176, 202, 214)
LINE = (92, 76, 60)

class Proj:
    def __init__(self, box, size, pad=0, kind='eq'):
        self.lon0, self.lon1, self.lat0, self.lat1 = box
        self.w, self.h = size; self.kind = kind
        self.k = math.cos(math.radians((self.lat0 + self.lat1) / 2)) if kind == 'eq' else 1.0
    def y_of(self, la):
        if self.kind == 'merc':
            return math.log(math.tan(math.pi / 4 + math.radians(max(-80, min(80, la))) / 2))
        return la
    def __call__(self, lo, la):
        if self.kind == 'merc':
            y0, y1 = self.y_of(self.lat0), self.y_of(self.lat1)
            return ((lo - self.lon0) / (self.lon1 - self.lon0) * self.w, (y1 - self.y_of(la)) / (y1 - y0) * self.h)
        return ((lo - self.lon0) / (self.lon1 - self.lon0) * self.w, (self.lat1 - la) / (self.lat1 - self.lat0) * self.h)

def fit_box(clon, clat, lat_span, size):
    """가운데·세로 폭(위도)과 그림 크기로 가로 폭을 맞춘 상자 (모양이 찌그러지지 않게)"""
    W, H = size
    lon_span = lat_span * (W / H) / math.cos(math.radians(clat))
    return (clon - lon_span / 2, clon + lon_span / 2, clat - lat_span / 2, clat + lat_span / 2)

def render(year, box, size, colors=None, default=None, sea=SEA, line=LINE, line_w=1.0, coast=(70, 60, 50), S=3, proj='eq', paper=True, seed=3,
           only=None, fade=None, hatch=None):
    """colors: {지배국키: 색} 또는 함수(props, owner) -> 색/None.  only: 이 키들만 색칠(나머지는 default).
       fade: 함수(props, owner) -> True면 연하게.  hatch: {키: 색} 빗금"""
    W, H = size
    pj = Proj(box, (W * S, H * S), kind=proj)
    im = Image.new('RGB', (W * S, H * S), sea)
    d = ImageDraw.Draw(im)
    cols = dict(COL); cols.update(colors or {} if not callable(colors) else {})
    feats = load(year)
    lon0, lon1, lat0, lat1 = box
    def visible(polys):
        for poly in polys:
            for (lo, la) in poly[0][::max(1, len(poly[0]) // 20)]:
                if lon0 - 20 <= lo <= lon1 + 20 and lat0 - 20 <= la <= lat1 + 20: return True
        return False
    hatch_jobs = []
    for props, polys in feats:
        if not visible(polys): continue
        ow = owner(props, year)
        if callable(colors): c = colors(props, ow)
        else: c = cols.get(ow, cols['ind'])
        if only is not None and ow not in only and not callable(colors): c = default or cols['ind']
        if c is None: c = default or cols['ind']
        if fade and fade(props, ow): c = tuple(int(v * 0.55 + 240 * 0.45) for v in c)
        for poly in polys:
            ring = [pj(lo, la) for lo, la in poly[0]]
            if len(ring) > 2: d.polygon(ring, fill=c)
        if hatch and ow in hatch:
            hatch_jobs.append((polys, hatch[ow]))
    for polys, hc in hatch_jobs:
        m = Image.new('L', im.size, 0); md = ImageDraw.Draw(m)
        for poly in polys:
            ring = [pj(lo, la) for lo, la in poly[0]]
            if len(ring) > 2: md.polygon(ring, fill=255)
        hl = Image.new('L', im.size, 0); hd = ImageDraw.Draw(hl)
        for x in range(-im.height, im.width, 7 * S): hd.line([(x, 0), (x + im.height, im.height)], fill=255, width=S)
        from PIL import ImageChops
        im.paste(hc, (0, 0), ImageChops.multiply(m, hl))
    # 국경선
    for props, polys in feats:
        if not visible(polys): continue
        for poly in polys:
            ring = [pj(lo, la) for lo, la in poly[0]]
            if len(ring) > 2: d.line(ring + [ring[0]], fill=line, width=max(1, int(line_w * S)))
    im = im.resize((W, H), Image.LANCZOS)
    if paper:
        im = age_paper(im, seed)
    return im, Proj(box, size, kind=proj)

def age_paper(im, seed=3, amt=0.16):
    """옛 지도 느낌: 누런 종이색을 살짝 섞고 얼룩·가장자리 어둡게"""
    W, H = im.size
    rnd = random.Random(seed)
    tint = Image.new('RGB', (W, H), (236, 220, 180))
    im = Image.blend(im, tint, amt)
    spots = Image.new('L', (W, H), 0); sd = ImageDraw.Draw(spots)
    for _ in range(max(6, W * H // 30000)):
        x, y, r = rnd.randint(0, W), rnd.randint(0, H), rnd.randint(10, 60)
        sd.ellipse([x - r, y - r, x + r, y + r], fill=rnd.randint(10, 30))
    spots = spots.filter(ImageFilter.GaussianBlur(14))
    im.paste((150, 120, 80), (0, 0), spots)
    v = Image.new('L', (W, H), 0); vd = ImageDraw.Draw(v)
    for k in range(20):
        vd.rectangle([k, k, W - 1 - k, H - 1 - k], outline=int(60 * (1 - k / 20) ** 2))
    im.paste((90, 70, 50), (0, 0), v)
    return im

def number_badge(d, x, y, n, r=11, col=(40, 34, 30), fg=(255, 250, 236), font=None):
    d.ellipse([x - r, y - r, x + r, y + r], fill=col, outline=fg, width=2)
    if font: d.text((x, y), str(n), font=font, fill=fg, anchor='mm')

def polyline(d, pj, pts, col=(160, 30, 30), w=3, dash=None):
    xy = [pj(lo, la) for lo, la in pts]
    if not dash:
        d.line(xy, fill=col, width=w, joint='curve'); return
    on, off = dash
    acc = 0; draw_on = True
    for (x0, y0), (x1, y1) in zip(xy, xy[1:]):
        L = math.hypot(x1 - x0, y1 - y0); t = 0
        while t < L:
            seg = (on if draw_on else off) - acc
            t1 = min(L, t + seg)
            if draw_on: d.line([(x0 + (x1 - x0) * t / L, y0 + (y1 - y0) * t / L), (x0 + (x1 - x0) * t1 / L, y0 + (y1 - y0) * t1 / L)], fill=col, width=w)
            acc += t1 - t; t = t1
            if acc >= (on if draw_on else off) - 1e-6: acc = 0; draw_on = not draw_on

# 서부 전선 참호선 (1914년 말 ~ 1917년, 대략)
WESTERN_FRONT = [(2.75, 51.13), (2.88, 50.85), (2.95, 50.6), (2.78, 50.29), (2.85, 50.0), (3.0, 49.58), (3.32, 49.38), (3.75, 49.35), (4.03, 49.26),
                 (4.6, 49.2), (5.0, 49.18), (5.38, 49.16), (5.54, 48.89), (6.05, 48.9), (6.5, 48.75), (6.9, 48.5), (7.05, 48.1), (7.1, 47.8), (7.17, 47.5)]
EASTERN_FRONT_1915 = [(21.2, 57.3), (23.5, 56.6), (25.5, 55.5), (26.5, 54.3), (25.8, 53.0), (25.6, 51.9), (25.3, 50.6), (25.7, 49.4), (25.9, 48.4)]

if __name__ == '__main__':
    import sys
    out = sys.argv[1]
    im, pj = render(1914, (-20, 55, -37, 38), (600, 600))
    im.save(out + '/geo_africa1914.png')
    im, pj = render(1880, (-20, 55, -37, 38), (600, 600))
    im.save(out + '/geo_africa1880.png')
    im, pj = render(1914, fit_box(16, 48, 26, (800, 450)), (800, 450))
    d = ImageDraw.Draw(im); polyline(d, pj, WESTERN_FRONT, w=3)
    im.save(out + '/geo_europe1914.png')
    im, pj = render(1920, fit_box(16, 48, 26, (800, 450)), (800, 450))
    im.save(out + '/geo_europe1920.png')
    im, pj = render(1914, (60, 150, -12, 50), (800, 450))
    im.save(out + '/geo_asia1914.png')
    im, pj = render(1914, (-170, 180, -56, 78), (1000, 450), proj='eq')
    im.save(out + '/geo_world1914.png')
