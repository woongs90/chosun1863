"""전보 소년 지도 공통 (29 x 13칸, 가운데 17칸이 실제 방)"""
import os, sys, math, random, json
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import numpy as np
import k_gfx as G
from k_gfx import TS, F, sh, mix, Prop, soft_shadow, label, glow
from k_common import write_map, write_mapinfos, blank, fill, save_layout, out
MW, MH = 29, 13
PW, PH = MW * TS, MH * TS

class Map:
    def __init__(self, key, mid, rows, pal='seoul', seed=1):
        self.key, self.mid = key, mid
        self.grid = [list(r) for r in rows]
        assert len(self.grid) == MH and all(len(r) == MW for r in self.grid), key
        self.big = G.render(self.grid, pal, seed)
        self.top = Image.new('RGBA', self.big.size, (0, 0, 0, 0))
        self.events = []
        self.pal = pal
        self.variants = {}
    def ev(self, name, x, y, sprite='', **kw):
        e = dict(name=name, x=x, y=y, sprite=sprite); e.update(kw); self.events.append(e); return e
    def tree(self, tx, ty, kind='mulberry', s=1.0, ox=24):
        tmp = Image.new('RGBA', self.big.size, (0, 0, 0, 0))
        G.tree(tmp, tx, ty, kind, s, ox)
        self.big.alpha_composite(tmp)
        cut = ty * TS + 4
        self.top.alpha_composite(tmp.crop((0, 0, tmp.width, cut)), (0, 0))
    def to_top(self, fn, cut_y, *a, **k):
        """그림 일부(cut_y 위쪽)를 인물보다 위 층에도 그림"""
        tmp = Image.new('RGBA', self.big.size, (0, 0, 0, 0))
        fn(tmp, *a, **k)
        self.big.alpha_composite(tmp)
        self.top.alpha_composite(tmp.crop((0, 0, tmp.width, cut_y)), (0, 0))
    def regions(self):
        reg = []
        for row in self.grid:
            reg.append([1 if ch in G.WALL else (5 if ch == 'u' else 0) for ch in row])
        return reg
    def save(self, root, parallax_name=None, finish=True, image=True, **fk):
        if finish and image: G.finish(self.big, self.grid, **fk)
        name = parallax_name or ('!c_' + self.key)
        if image: out(root, name, self.big.convert('RGB'))
        if self.top.getbbox():
            self.top.save(os.path.join(root, 'img/parallaxes', name + '_top.png'), optimize=True)
        write_map(root, self.mid, MW, MH, self.regions(), self.events, name)
        save_layout(self.key, {'map': self.mid, 'events': {e['name']: [e['x'], e['y']] for e in self.events}})
        return self.big

def sky(big, y1, seed=1, mountain=True, top=(150, 186, 214), bot=(214, 222, 222), night=False):
    """맨 위 하늘 + 먼 산 (건물 뒤)"""
    d = ImageDraw.Draw(big)
    if night: top, bot = (30, 36, 58), (60, 66, 84)
    for y in range(0, y1):
        t = y / max(1, y1 - 1)
        d.line([(0, y), (big.width, y)], fill=mix(top, bot, t))
    if mountain:
        rnd = random.Random(seed)
        pts = [(0, y1)]
        x = 0
        while x < big.width:
            pts.append((x, y1 - 30 - rnd.randint(0, 50) - (60 if abs(x - big.width / 2) < 260 else 0) * math.cos((x - big.width / 2) / 260 * math.pi / 2)))
            x += 40
        pts.append((big.width, y1))
        d.polygon(pts, fill=mix((96, 116, 110), bot, 0.35) if not night else (40, 46, 60))
        pts2 = [(p[0], p[1] + 26 + (i % 3) * 6) for i, p in enumerate(pts[1:-1])]
        d.polygon([(0, y1)] + pts2 + [(big.width, y1)], fill=mix((80, 100, 90), bot, 0.2) if not night else (34, 40, 52))

def dark_out(big, x0, x1, y0=0, y1=MH, col=(26, 22, 20)):
    d = ImageDraw.Draw(big)
    d.rectangle([x0 * TS, y0 * TS, x1 * TS - 1, y1 * TS - 1], fill=col)

def save_variant(root, name, big, top=None):
    out(root, name, big.convert('RGB'))
    if top is not None and top.getbbox():
        top.save(os.path.join(root, 'img/parallaxes', name + '_top.png'), optimize=True)

def exit_path(big, x0, x1, y0, text, col=(150, 132, 104), edge=(96, 82, 64)):
    """아래쪽 나가는 길: x0~x1칸, y0(px)부터 맨 아래까지 흙길 + 테두리 + 아래 화살표 + 팻말"""
    d = ImageDraw.Draw(big); PH_ = MH * TS
    X0, X1 = x0 * TS + 4, (x1 + 1) * TS - 4
    rnd = random.Random(x0 * 7 + y0)
    d.rectangle([X0, y0, X1, PH_], fill=col)
    for _ in range(120):
        px_, py_ = rnd.randint(X0, X1), rnd.randint(y0, PH_ - 1)
        d.point((px_, py_), fill=sh(col, rnd.choice([0.86, 0.92, 1.08])))
    for xx in (X0, X1 - 5): d.rectangle([xx, y0, xx + 5, PH_], fill=edge)
    cx = (X0 + X1) // 2
    for k, yy in enumerate(range(y0 + 26, PH_ - 10, 34)):
        d.polygon([(cx - 14, yy), (cx + 14, yy), (cx, yy + 14)], fill=(250, 240, 210) if k % 2 == 0 else (236, 222, 186))
    label(big, text, cx, y0 - 2, 12, back=(40, 50, 60, 230))

