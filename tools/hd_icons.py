"""고화질 아이템 아이콘 96x96 (img/pictures/item_*.png)"""
import os, sys, math
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hd_art import sh, outline, vgrad

S = 96
def canvas():
    im = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    return im, ImageDraw.Draw(im)

def save(im, out, name):
    outline(im, 0.42).save(os.path.join(out, name + '.png'))

def bowl(d, clay):
    d.ellipse([14, 44, 82, 84], fill=(150, 108, 70))
    d.chord([14, 44, 82, 84], 90, 270, fill=(176, 130, 88))
    d.ellipse([18, 40, 78, 60], fill=sh(clay, 0.8))
    d.ellipse([22, 26, 74, 56], fill=clay)
    d.chord([22, 26, 74, 56], 140, 260, fill=sh(clay, 1.12))
    for (x, y) in [(36, 38), (52, 34), (60, 44), (42, 48)]:
        d.ellipse([x, y, x + 6, y + 4], fill=sh(clay, 0.88))

def make(out):
    os.makedirs(out, exist_ok=True)
    # 지도
    im, d = canvas()
    d.rectangle([14, 20, 82, 76], fill=(232, 216, 176)); d.rectangle([14, 20, 82, 26], fill=(214, 196, 150))
    d.rectangle([8, 16, 16, 80], fill=(140, 86, 52)); d.rectangle([80, 16, 88, 80], fill=(140, 86, 52))
    d.line([(9, 18), (9, 78)], fill=(186, 130, 90)); d.line([(81, 18), (81, 78)], fill=(186, 130, 90))
    for gx in range(24, 76, 12): d.line([(gx, 28), (gx, 72)], fill=(200, 184, 146))
    for gy in range(32, 74, 12): d.line([(18, gy), (78, gy)], fill=(200, 184, 146))
    for (x, y) in [(46, 44), (56, 56), (46, 32)]:
        d.polygon([(x - 6, y + 5), (x, y - 6), (x + 6, y + 5)], fill=(120, 110, 96)); d.polygon([(x - 2, y - 2), (x, y - 6), (x + 2, y - 2)], fill=(240, 240, 240))
    d.line([(64, 62), (64, 50), (52, 50), (40, 50), (28, 50), (28, 38)], fill=(200, 40, 40), width=3)
    d.ellipse([60, 58, 70, 68], fill=(60, 90, 160)); d.ellipse([22, 32, 34, 44], fill=(200, 40, 40))
    save(im, out, 'item_map')
    # 조각칼
    im, d = canvas()
    d.polygon([(38, 84), (50, 84), (52, 46), (36, 46)], fill=(130, 84, 50)); d.line([(40, 84), (38, 46)], fill=(170, 120, 80))
    for y in (54, 64, 74): d.line([(37, y), (51, y)], fill=(100, 62, 36))
    d.rectangle([34, 40, 54, 46], fill=(200, 170, 80))
    d.polygon([(38, 40), (50, 40), (48, 14), (44, 8), (40, 14)], fill=(200, 206, 218)); d.line([(42, 38), (42, 14)], fill=(244, 248, 255), width=2)
    save(im, out, 'item_knife')
    # 백토 / 자토
    im, d = canvas(); bowl(d, (244, 242, 234)); save(im, out, 'item_baekto')
    im, d = canvas(); bowl(d, (184, 82, 58)); save(im, out, 'item_jato')
    # 상감청자
    im, d = canvas()
    cx = 48; c = (124, 172, 152)
    pts = [(cx - 8, 8), (cx + 8, 8), (cx + 10, 14), (cx + 26, 28), (cx + 26, 46), (cx + 18, 70), (cx + 14, 88), (cx - 14, 88), (cx - 18, 70), (cx - 26, 46), (cx - 26, 28), (cx - 10, 14)]
    d.polygon(pts, fill=c)
    d.polygon([(cx - 22, 30), (cx - 14, 24), (cx - 16, 60), (cx - 20, 56)], fill=sh(c, 1.22))
    d.ellipse([cx - 9, 4, cx + 9, 12], fill=sh(c, 0.85))
    for (ox, oy, r) in [(-8, 40, 9), (10, 58, 8)]:
        d.ellipse([cx + ox - r, oy - r, cx + ox + r, oy + r], outline=(250, 250, 246), width=2)
        d.line([(cx + ox - 5, oy + 2), (cx + ox, oy - 2), (cx + ox + 5, oy + 2)], fill=(250, 250, 246), width=2)
    for (ox, oy) in [(8, 34), (-10, 62), (2, 76)]:
        d.arc([cx + ox - 5, oy - 3, cx + ox + 5, oy + 3], 180, 360, fill=(36, 40, 40), width=2)
    save(im, out, 'item_celadon')
    # 丁 노란 종이
    im, d = canvas()
    d.polygon([(14, 18), (78, 12), (84, 78), (20, 84)], fill=(240, 206, 82)); d.polygon([(14, 18), (78, 12), (80, 22), (16, 28)], fill=(250, 222, 110))
    d.polygon([(28, 30), (68, 27), (68, 36), (52, 37), (54, 70), (46, 74), (40, 70), (46, 66), (44, 37), (28, 38)], fill=(150, 108, 34))
    save(im, out, 'item_paper')
    # 먹
    im, d = canvas()
    d.polygon([(34, 10), (62, 14), (58, 88), (30, 84)], fill=(42, 42, 50)); d.polygon([(34, 10), (40, 11), (36, 85), (30, 84)], fill=(80, 80, 92))
    d.rectangle([38, 30, 54, 50], fill=(206, 172, 82)); d.line([(42, 34), (50, 34)], fill=(120, 90, 40)); d.line([(46, 34), (46, 46)], fill=(120, 90, 40))
    save(im, out, 'item_ink')
    # 한지
    im, d = canvas()
    d.rectangle([12, 26, 74, 74], fill=(248, 244, 232)); d.line([(12, 26), (74, 26)], fill=(255, 255, 250))
    for y in range(30, 72, 5): d.line([(14, y), (72, y + 1)], fill=(236, 230, 214))
    d.ellipse([66, 22, 86, 78], fill=(232, 226, 208)); d.ellipse([71, 40, 81, 60], fill=(214, 206, 186))
    save(im, out, 'item_hanji')
    # 대장경판 탁본
    im, d = canvas()
    d.rectangle([16, 8, 80, 88], fill=(246, 242, 230)); d.rectangle([16, 8, 80, 14], fill=(226, 220, 204))
    d.rectangle([22, 18, 74, 82], outline=(40, 40, 40), width=2)
    for col in range(5):
        x = 66 - col * 10
        for row in range(7):
            y = 24 + row * 8
            d.rectangle([x, y, x + 6, y + 5], fill=(30, 30, 30))
    d.rectangle([26, 66, 38, 78], fill=(180, 40, 40))
    save(im, out, 'item_takbon')
    # 보고서
    im, d = canvas()
    d.rectangle([12, 22, 84, 76], fill=(236, 224, 192)); d.polygon([(12, 22), (48, 52), (84, 22)], fill=(214, 200, 162))
    d.line([(12, 22), (48, 52), (84, 22)], fill=(170, 150, 110), width=2)
    d.ellipse([38, 42, 58, 62], fill=(178, 36, 36)); d.ellipse([42, 46, 54, 58], outline=(220, 90, 80))
    save(im, out, 'item_report')
    # 금속활자
    im, d = canvas()
    d.polygon([(24, 34), (52, 22), (78, 34), (50, 46)], fill=(196, 192, 176))
    d.polygon([(24, 34), (50, 46), (50, 84), (24, 72)], fill=(150, 146, 130))
    d.polygon([(50, 46), (78, 34), (78, 72), (50, 84)], fill=(120, 116, 104))
    d.polygon([(38, 32), (60, 28), (60, 33), (52, 34), (53, 42), (48, 43), (47, 35), (38, 37)], fill=(70, 66, 58))
    d.line([(24, 34), (52, 22)], fill=(230, 226, 214))
    save(im, out, 'item_type')

if __name__ == '__main__':
    make(sys.argv[1])
    print('icons ok')
