"""고화질 타이틀 화면 + 인트로용 밤하늘/박물관 배경"""
import os, sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hd_art import sh, mix, layer, outline, soft_shadow, vgrad, hgrad, floor_maru, noise_fill, DAN_GREEN, DAN_BLUE, DAN_RED, DAN_WHITE, PILLAR
from hd_world import vase_shape, MW_glow, wood_top
from make_title import draw_gate, glow_layer, logo, sprite_frame

W, H = 816, 624

def night(palace=True, seed=3, mx=0):
    img = Image.new('RGBA', (W, H))
    d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        c = mix((14, 14, 42), (70, 46, 96), t ** 1.2)
        d.line([(0, y), (W, y)], fill=c)
    rnd = random.Random(seed)
    for _ in range(int(260 * W / 816)):
        x, y = rnd.randrange(W), rnd.randrange(int(H * 0.62))
        b = rnd.randint(140, 255)
        d.point((x, y), fill=(b, b, min(255, b + 15)))
        if rnd.random() < 0.06:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)): d.point((x + dx, y + dy), fill=(b, b, b))
            for dx, dy in ((2, 0), (-2, 0), (0, 2), (0, -2)): d.point((x + dx, y + dy), fill=(b // 2, b // 2, b // 2))
    img.alpha_composite(glow_layer(img.size, 660 + mx, 90, 90, (250, 240, 200), 0.9))
    d = ImageDraw.Draw(img)
    d.ellipse([636 + mx, 66, 684 + mx, 114], fill=(252, 244, 210)); d.ellipse([650 + mx, 60, 698 + mx, 108], fill=mix((14, 14, 42), (70, 46, 96), 0.12))
    for (ox, oy, r) in [(646 + mx, 84, 4), (656 + mx, 98, 3)]:
        d.ellipse([ox - r, oy - r, ox + r, oy + r], fill=(232, 222, 186))
    # 산 (여러 겹)
    for layer_i, (base, col, amp, step) in enumerate([(360, (46, 44, 92), 70, 40), (400, (38, 36, 74), 50, 30), (430, (30, 28, 58), 34, 22)]):
        pts = [(0, H)]
        x = -20
        while x <= W + 40:
            pts.append((x, base - abs(math.sin(x / (90 + layer_i * 30) + layer_i)) * amp - rnd.randint(0, 10)))
            x += step
        pts.append((W, H))
        d.polygon(pts, fill=col)
        for i in range(1, len(pts) - 2):
            d.line([pts[i], pts[i + 1]], fill=sh(col, 1.35))
    # 안개
    fog = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fog)
    for i in range(int(W / 170) + 2):
        fd.ellipse([-100 + i * 170, 400, 160 + i * 170, 470], fill=(150, 140, 190, 40))
    img.alpha_composite(fog.filter(ImageFilter.GaussianBlur(14)))
    if palace:
        draw_palace(img)
    return img

def draw_palace(img):
    lay = layer(); d = ImageDraw.Draw(lay)
    # 기단
    d.polygon([(110, 520), (706, 520), (740, 560), (76, 560)], fill=(118, 110, 120))
    d.rectangle([76, 560, 740, 624], fill=(96, 90, 100))
    d.line([(110, 520), (706, 520)], fill=(160, 152, 160))
    for i in range(7):
        y = 520 + i * 15
        w = 70 + i * 8
        d.rectangle([408 - w, y, 408 + w, y + 14], fill=sh((128, 120, 130), 1.05 - i * 0.03))
        d.line([(408 - w, y), (408 + w, y)], fill=(176, 168, 176))
    # 기둥과 벽
    d.rectangle([150, 410, 666, 520], fill=(214, 200, 176))
    for x in range(150, 666, 32):
        d.rectangle([x + 6, 430, x + 26, 512], fill=(150, 92, 56))
        for k in range(x + 9, x + 25, 4): d.line([(k, 432), (k, 510)], fill=(196, 160, 110))
        d.line([(x + 8, 470), (x + 24, 470)], fill=(196, 160, 110))
    for x in range(140, 690, 64):
        hgrad(d, (x, 404, x + 14, 520), sh(PILLAR, 0.7), sh(PILLAR, 0.65), mid=sh(PILLAR, 1.35))
    # 창방 단청
    d.rectangle([130, 392, 686, 410], fill=DAN_GREEN)
    for x in range(132, 684, 22):
        d.rectangle([x, 395, x + 18, 407], fill=DAN_BLUE); d.rectangle([x + 3, 398, x + 15, 404], fill=DAN_WHITE); d.ellipse([x + 6, 397, x + 12, 405], fill=DAN_RED)
    # 서까래 끝
    for x in range(100, 716, 10):
        d.ellipse([x, 380, x + 9, 389], fill=DAN_GREEN); d.ellipse([x + 2, 382, x + 7, 387], fill=DAN_WHITE); d.point((x + 4, 384), fill=DAN_RED)
    # 지붕 (곡선 처마)
    eave = []
    for i in range(61):
        t = i / 60
        x = 60 + t * 696
        y = 378 - 30 * math.sin(math.pi * t) * 0.35 - 26 * (abs(t - 0.5) * 2) ** 4
        eave.append((x, y))
    ridge_y = 286
    roof = [(150, ridge_y), (666, ridge_y)] + eave[::-1]
    d.polygon(roof, fill=(54, 50, 66))
    for row in range(12):
        t = row / 12
        pts = []
        for (x, y) in eave:
            yy = y + (ridge_y - y) * t
            xx = 408 + (x - 408) * (1 - t * 0.26)
            pts.append((xx, yy))
        d.line(pts, fill=(74, 70, 88), width=2)
    for i in range(0, 61, 2):
        x, y = eave[i]
        tx = 408 + (x - 408) * 0.74
        d.line([(x, y), (tx, ridge_y)], fill=(44, 40, 54))
    d.line(eave, fill=(30, 28, 38), width=3)
    d.rectangle([140, ridge_y - 12, 676, ridge_y + 2], fill=(40, 36, 50))
    d.line([(140, ridge_y - 12), (676, ridge_y - 12)], fill=(90, 86, 104), width=2)
    for (x, s) in [(140, -1), (676, 1)]:
        d.polygon([(x, ridge_y - 12), (x + s * 20, ridge_y - 34), (x + s * 8, ridge_y + 2)], fill=(40, 36, 50))
    img.alpha_composite(outline(lay, 0.5))
    # 창 불빛
    for x in range(156, 660, 32):
        img.alpha_composite(MW_glow((x + 16, 470), 20, (255, 210, 140)))

def title_image(root, img=None):
    if img is None: img = night(palace=True)
    draw_gate(img, 408, 290, 1.0, t=0.2)
    pics = os.path.join(root, 'img/pictures')
    def icon(name, cx, cy, size, ang):
        ic = Image.open(os.path.join(pics, name + '.png')).convert('RGBA').resize((size, size), Image.NEAREST).rotate(ang, resample=Image.NEAREST, expand=True)
        img.alpha_composite(glow_layer(img.size, cx, cy, int(size * 0.85), (255, 236, 170), 0.8))
        img.alpha_composite(ic, (cx - ic.width // 2, cy - ic.height // 2))
    icon('item_celadon', 196, 300, 92, 8); icon('item_takbon', 620, 282, 88, -8); icon('item_type', 654, 404, 70, 10)
    ch = os.path.join(root, 'img/characters')
    m = sprite_frame(os.path.join(ch, '$student_m.png'), 3, 1, 2); f = sprite_frame(os.path.join(ch, '$student_f.png'), 3, 1, 2)
    soft_shadow(img, (300, 610, 520, 630), 120, 6)
    img.alpha_composite(m, (408 - 104, 530)); img.alpha_composite(f, (408 + 8, 530))
    logo(img, 408, 128, 1.0)
    return img.convert('RGB')

def museum():
    img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
    d = ImageDraw.Draw(img)
    noise_fill(img, (0, 0, W, 230), (222, 216, 204), 4, seed=21)
    d = ImageDraw.Draw(img)
    vgrad(d, (0, 0, W, 40), (190, 184, 172), (222, 216, 204))
    for x in range(0, W, 102):
        d.line([(x, 40), (x, 228)], fill=(206, 200, 188))
    d.rectangle([0, 222, W, 236], fill=(140, 104, 70)); d.line([(0, 222), (W, 222)], fill=(180, 140, 100))
    floor_maru(img, (0, 236, W, H), (166, 118, 74), seed=7)
    d = ImageDraw.Draw(img)
    # 현판
    d.rectangle([300, 44, 516, 84], fill=(96, 40, 36)); d.rectangle([304, 48, 512, 80], outline=(214, 176, 90), width=2)
    for i in range(6): d.rectangle([326 + i * 28, 56, 344 + i * 28, 72], fill=(230, 200, 120))
    # 설명판
    for x in (40, 690):
        d.rectangle([x, 70, x + 86, 160], fill=(70, 60, 54)); d.rectangle([x + 5, 75, x + 81, 155], fill=(236, 228, 206))
        for j in range(84, 150, 8): d.line([(x + 12, j), (x + 74 - (j % 3) * 6, j)], fill=(120, 110, 100))
    # 진열장 3개
    def case(x, y, w, h, kind):
        soft_shadow(img, (x - 6, y + h + 30, x + w + 10, y + h + 52), 110, 8)
        lay = layer(); dd = ImageDraw.Draw(lay)
        dd.rectangle([x - 6, y + h, x + w + 6, y + h + 46], fill=(64, 52, 48)); dd.line([(x - 6, y + h), (x + w + 6, y + h)], fill=(110, 96, 88))
        dd.rectangle([x, y, x + w, y + h], fill=(80, 70, 80, 255))
        dd.rectangle([x + 4, y + 4, x + w - 4, y + h - 2], fill=(56, 64, 86))
        if kind == 'vase':
            vase_shape(dd, x + w // 2, y + 22, 3.4)
        elif kind == 'board':
            dd.rectangle([x + 20, y + 40, x + w - 20, y + h - 20], fill=(176, 136, 90))
            for i in range(x + 26, x + w - 26, 8):
                for j in range(y + 48, y + h - 28, 10): dd.rectangle([i, j, i + 5, j + 6], fill=(120, 86, 54))
        else:
            dd.rectangle([x + 18, y + 60, x + w // 2 - 2, y + h - 30], fill=(232, 218, 182)); dd.rectangle([x + w // 2 + 2, y + 60, x + w - 18, y + h - 30], fill=(232, 218, 182))
            for j in range(y + 70, y + h - 36, 8):
                dd.line([(x + 24, j), (x + w // 2 - 8, j)], fill=(110, 100, 90)); dd.line([(x + w // 2 + 8, j), (x + w - 24, j)], fill=(110, 100, 90))
        img.alpha_composite(outline(lay, 0.5))
        glass = layer(); gd = ImageDraw.Draw(glass)
        gd.rectangle([x, y, x + w, y + h], fill=(190, 220, 240, 46), outline=(220, 240, 250, 200))
        gd.polygon([(x + 10, y + 6), (x + 26, y + 6), (x + 8, y + h - 10), (x - 4 + 10, y + h - 10)], fill=(255, 255, 255, 60))
        img.alpha_composite(glass)
    case(70, 120, 150, 150, 'board'); case(320, 90, 176, 196, 'vase'); case(596, 120, 150, 150, 'book')
    for x in (145, 408, 671):
        img.alpha_composite(glow_layer(img.size, x, 100, 140, (255, 244, 210), 0.55))
    # 줄 기둥
    lay = layer(); dd = ImageDraw.Draw(lay)
    for x in (40, 776):
        dd.rectangle([x - 3, 330, x + 3, 392], fill=(206, 168, 80)); dd.ellipse([x - 7, 322, x + 7, 336], fill=(230, 196, 100)); dd.ellipse([x - 12, 388, x + 12, 398], fill=(150, 120, 60))
    dd.arc([40, 300, 776, 380], 20, 160, fill=(160, 30, 40), width=4)
    img.alpha_composite(outline(lay, 0.5))
    return img

def side_silhouettes(img, ox):
    """넓은 화면 양옆: 소나무와 담장 실루엣"""
    d = ImageDraw.Draw(img)
    WW = img.width
    rnd = random.Random(11)
    for side in (0, 1):
        x0, x1 = (0, ox + 60) if side == 0 else (WW - ox - 60, WW)
        # 담장
        d.rectangle([x0, 548, x1, 624], fill=(28, 26, 44))
        for x in range(x0 - 12, x1, 12):
            d.chord([x, 540, x + 12, 552], 180, 360, fill=(40, 38, 60), outline=(22, 20, 34))
        d.line([(x0, 552), (x1, 552)], fill=(50, 48, 72))
        # 소나무
        for k in range(3):
            cx = (x0 + 40 + k * 90 + rnd.randint(-10, 10)) if side == 0 else (x1 - 40 - k * 90 + rnd.randint(-10, 10))
            if not (x0 <= cx <= x1): continue
            base = 552; hgt = rnd.randint(140, 200)
            d.polygon([(cx - 5, base), (cx + 5, base), (cx + 2, base - hgt), (cx - 2, base - hgt)], fill=(24, 22, 36))
            for j in range(6):
                yy = base - hgt * (0.45 + j * 0.1); r = 46 - j * 5
                ox2 = rnd.randint(-14, 14)
                d.ellipse([cx + ox2 - r, yy - r * 0.45, cx + ox2 + r, yy + r * 0.45], fill=(26 + j * 2, 30 + j * 2, 46 + j * 2))

def title_image_wide(root, WW=1392):
    global W
    ox = (WW - 816) // 2
    W0 = W; W = WW
    try:
        bg = night(palace=False, mx=ox)
    finally:
        W = W0
    side_silhouettes(bg, ox)
    core = night(palace=True)           # 가운데 816: 원래 그림 그대로
    core = title_image(root, core).convert('RGBA')
    # 가운데 그림의 하늘 부분은 넓은 배경과 자연스럽게 섞이도록 가장자리를 흐리게
    mask = Image.new('L', core.size, 255)
    md = ImageDraw.Draw(mask)
    for i in range(60):
        a = int(255 * i / 60)
        md.line([(i, 0), (i, 624)], fill=a); md.line([(815 - i, 0), (815 - i, 624)], fill=a)
    bg.paste(core, (ox, 0), mask)
    bg.paste(bg.crop((0, 1, bg.width, 2)), (0, 0))   # 맨 윗줄 얇은 선 지우기
    return bg.convert('RGB')

if __name__ == '__main__':
    root = sys.argv[1]
    os.makedirs(os.path.join(root, 'img/titles1'), exist_ok=True)
    title_image_wide(root).save(os.path.join(root, 'img/titles1/TimeGate_Title.png'))
    if len(sys.argv) > 2:
        museum().convert('RGB').save(os.path.join(sys.argv[2], 'hd_museum.png'))
        night().convert('RGB').save(os.path.join(sys.argv[2], 'hd_night.png'))
    print('title ok')
