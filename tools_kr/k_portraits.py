"""종로 사진관 2 표정 초상화 (대화창 위 상반신, 240x264 도트)
 크게(4배) 매끈하게 그린 뒤 줄이고 색을 줄여 도트 느낌으로 만듭니다.
 실존 인물은 사진으로 남은 특징(얼굴형·머리·안경·수염·옷)을 살려 그렸습니다.
   김구: 둥글고 넓은 얼굴, 짧게 깎은 머리, 굵은 검은 둥근 안경, 흰 두루마기, 활짝 웃는 입
   이승만: 갸름한 얼굴, 뒤로 넘긴 흰머리, 가는 눈과 주름, 짙은 양복·은회색 넥타이
   여운형: 각진 얼굴, 뒤로 넘긴 회색 머리, 짙은 눈썹, 흰 콧수염, 밝은 회색 양복·줄무늬 넥타이
   김규식: 둥근 얼굴, 뒤로 빗어 넘긴 검은 머리(넓은 이마), 수염 없음, 회갈색 두루마기
 그림 이름: pt_<사람>_<표정>.png   표정 n smile surprise sad angry resolve worry think
"""
import os, sys, math
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'tools'))
from hd_art import sh, mix, outline

U = 4                      # 그릴 때 배율
PW, PH = 120, 132          # 도트 크기 (최종 x2 = 240x264)

Z = 1.34                   # 머리를 크게 보이게 (60, 62)를 중심으로 확대
def P(x, y): return (((x - 60) * Z + 60) * U, ((y - 62) * Z + 64) * U)
def B(x0, y0, x1, y1):
    a, b = P(x0, y0); c, e = P(x1, y1)
    return [a, b, c, e]
def poly(pts): return [P(x, y) for x, y in pts]

def bez(p0, p1, p2, n=12):
    out = []
    for i in range(n + 1):
        t = i / n
        out.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1]))
    return out

def curve(d, p0, p1, p2, col, w):
    pts = [P(*q) for q in bez(p0, p1, p2, 16)]
    d.line(pts, fill=col, width=max(1, int(w * U * Z)), joint='curve')

EXPR = {
    #          눈썹(안쪽 올림, 바깥 올림, 찌푸림), 눈 뜨기, 입, 눈 모양
    'n':        dict(bi=0, bo=0, eye=1.0, mouth='neutral'),
    'smile':    dict(bi=0.8, bo=0.4, eye=0.75, mouth='smile', happy=True),
    'surprise': dict(bi=3.0, bo=2.6, eye=1.35, mouth='open'),
    'sad':      dict(bi=3.2, bo=-1.2, eye=0.78, mouth='frown', down=True),
    'angry':    dict(bi=-3.0, bo=1.2, eye=0.85, mouth='grit'),
    'resolve':  dict(bi=-1.8, bo=0.6, eye=0.92, mouth='tight'),
    'worry':    dict(bi=2.6, bo=-0.4, eye=1.0, mouth='wavy'),
    'think':    dict(bi=0.5, bo=1.6, eye=0.9, mouth='side', side=True),
}

def draw_eye(d, cx, cy, p, ex, side):
    """cx: 눈 가운데, side: -1 왼쪽(보는 사람 기준) / 1 오른쪽"""
    w = p.get('eye_w', 6.2) * 1.08; h = p.get('eye_h', 3.4) * ex['eye'] * 1.1
    narrow = p.get('narrow', 0)
    h = max(0.8, h - narrow)
    lid = p.get('lid', (40, 28, 26))
    if ex.get('happy'):
        curve(d, (cx - w, cy + 0.6), (cx, cy - 3.0), (cx + w, cy + 0.6), lid, 1.5)
        return
    sclera = (248, 244, 238)
    tilt = p.get('eye_tilt', 0.6) * side
    pts = bez((cx - w, cy + tilt * -0.3), (cx, cy - h * 1.25), (cx + w, cy - tilt * 0.3), 10) + bez((cx + w, cy - tilt * 0.3), (cx, cy + h * 1.05), (cx - w, cy + tilt * -0.3), 10)[1:]
    d.polygon(poly(pts), fill=sclera)
    # 눈동자
    ir = p.get('iris', 3.0) * (0.8 if ex['eye'] > 1.2 else 1.0)
    ix = cx + (1.2 * side * 0 + (1.6 if ex.get('side') else 0))
    iy = cy + (0.9 if ex.get('down') else 0) - 0.2
    d.ellipse(B(ix - ir, iy - ir, ix + ir, iy + ir), fill=p.get('iris_c', (66, 44, 34)))
    d.ellipse(B(ix - ir * 0.5, iy - ir * 0.5, ix + ir * 0.5, iy + ir * 0.5), fill=(20, 14, 14))
    d.ellipse(B(ix - ir * 0.75, iy - ir * 0.85, ix - ir * 0.05, iy - ir * 0.15), fill=(255, 255, 255))
    # 눈꺼풀 (위 굵게) - 가는 눈은 위에서 덮음
    skin = p['skin']
    if narrow > 0:
        cover = bez((cx - w - 0.5, cy - 0.2), (cx, cy - h * 1.25 - 2.6), (cx + w + 0.5, cy - 0.2), 10) + [(cx + w + 0.5, cy - h * 0.2), (cx - w - 0.5, cy - h * 0.2)]
        d.polygon(poly([(x, y - 3) for x, y in cover[:11]] + list(reversed(cover[:11]))), fill=skin)
    curve(d, (cx - w - 0.4, cy + 0.2 - tilt * 0.3), (cx, cy - h * 1.3), (cx + w + 0.4, cy - 0.2 + tilt * 0.3), lid, 2.0)
    if p.get('double_lid', True) and narrow < 1.5:
        curve(d, (cx - w * 0.6, cy - h * 1.05 - 1.2), (cx, cy - h * 1.3 - 1.8), (cx + w * 0.8, cy - h * 0.9 - 1.0), sh(skin, 0.78), 0.6)
    curve(d, (cx - w * 0.8, cy + h * 0.55), (cx, cy + h * 1.0), (cx + w * 0.8, cy + h * 0.5), sh(skin, 0.8), 0.5)
    if p.get('bags'):
        curve(d, (cx - w * 0.7, cy + h + 1.6), (cx, cy + h + 3.0), (cx + w * 0.8, cy + h + 1.4), sh(skin, 0.82), 0.6)

def draw_brow(d, cx, cy, p, ex, side):
    bw = p.get('brow_w', 8.2); th = p.get('brow_t', 1.8) * 1.3
    col = p.get('brow_c', p.get('hair_c', (40, 34, 30)))
    inner = (cx - bw * side * -1 * 0 + (-bw * 0.5 if side > 0 else bw * 0.5), cy - ex['bi'] * 0.7)
    inner = (cx + (-bw * 0.55 if side > 0 else bw * 0.55), cy - ex['bi'] * 0.7)
    outer = (cx + (bw * 0.6 if side > 0 else -bw * 0.6), cy - ex['bo'] * 0.6 + p.get('brow_slope', 0.6))
    mid = ((inner[0] + outer[0]) / 2, min(inner[1], outer[1]) - p.get('brow_arch', 1.2))
    if ex.get('side') and side > 0: mid = (mid[0], mid[1] - 1.5); outer = (outer[0], outer[1] - 1.2)
    pts_top = bez(inner, mid, outer, 10)
    pts_bot = [(x, y + th * (1 - 0.5 * i / 10)) for i, (x, y) in enumerate(pts_top)]
    d.polygon(poly(pts_top + list(reversed(pts_bot))), fill=col)

def draw_mouth(d, cx, cy, p, ex):
    mw = p.get('mouth_w', 6.5)
    lip = p.get('lip', (178, 96, 88))
    dark = (90, 40, 40)
    k = ex['mouth']
    if k == 'neutral' and p.get('talk'):
        d.polygon(poly(bez((cx - mw * 0.7, cy), (cx, cy - 0.8), (cx + mw * 0.7, cy), 8) + bez((cx + mw * 0.7, cy), (cx, cy + 3.2), (cx - mw * 0.7, cy), 8)[1:]), fill=(110, 50, 48))
        d.polygon(poly(bez((cx - mw * 0.6, cy - 0.1), (cx, cy - 0.5), (cx + mw * 0.6, cy - 0.1), 8) + [(cx + mw * 0.5, cy + 0.8), (cx - mw * 0.5, cy + 0.8)]), fill=(236, 230, 218))
        return
    if k == 'neutral':
        curve(d, (cx - mw * 0.75, cy), (cx, cy + 0.6 + p.get('smirk', 0)), (cx + mw * 0.75, cy - p.get('smirk', 0) * 0.5), sh(lip, 0.55), 1.4)
        d.polygon(poly(bez((cx - mw * 0.5, cy + 0.9), (cx, cy + 2.6), (cx + mw * 0.5, cy + 0.9), 8)), fill=sh(lip, 0.95))
        if p.get('lower_lip', True): curve(d, (cx - mw * 0.4, cy + 1.8), (cx, cy + 2.6), (cx + mw * 0.4, cy + 1.8), sh(p['skin'], 0.86), 0.6)
    elif k == 'smile':
        if p.get('grin', True):
            top = bez((cx - mw, cy - 0.8), (cx, cy + 0.4), (cx + mw, cy - 0.8), 10)
            bot = bez((cx + mw, cy - 0.8), (cx, cy + p.get('grin_h', 5.6)), (cx - mw, cy - 0.8), 10)
            d.polygon(poly(top + bot[1:]), fill=dark)
            tb = bez((cx - mw * 0.82, cy - 0.3), (cx, cy + 0.9), (cx + mw * 0.82, cy - 0.3), 10)
            d.polygon(poly(tb + [(cx + mw * 0.7, cy + 1.5), (cx - mw * 0.7, cy + 1.5)]), fill=(246, 242, 232))
            if p.get('tooth_gap'):
                d.polygon(poly([(cx - 0.7, cy - 0.2), (cx + 0.7, cy - 0.2), (cx + 0.5, cy + 1.8), (cx - 0.5, cy + 1.8)]), fill=dark)
                for tx in (-4.2, -2.2, 2.2, 4.2): d.line([P(cx + tx, cy - 0.1), P(cx + tx, cy + 1.3)], fill=(214, 206, 192), width=max(1, U // 2))
            d.ellipse(B(cx - mw * 0.45, cy + 2.4, cx + mw * 0.45, cy + 4.6), fill=(196, 96, 96))
        else:
            curve(d, (cx - mw, cy - 0.8), (cx, cy + 2.4), (cx + mw, cy - 0.8), sh(lip, 0.65), 1.2)
        if p.get('cheek_lines', True):
            curve(d, (cx - mw - 1.2, cy - 2.4), (cx - mw - 2.4, cy - 0.4), (cx - mw - 0.8, cy + 1.2), sh(p['skin'], 0.82), 0.6)
            curve(d, (cx + mw + 1.2, cy - 2.4), (cx + mw + 2.4, cy - 0.4), (cx + mw + 0.8, cy + 1.2), sh(p['skin'], 0.82), 0.6)
    elif k == 'open':
        d.ellipse(B(cx - mw * 0.42, cy - 1.4, cx + mw * 0.42, cy + 3.6), fill=dark)
        d.ellipse(B(cx - mw * 0.3, cy + 1.4, cx + mw * 0.3, cy + 3.4), fill=(190, 92, 92))
    elif k == 'frown':
        curve(d, (cx - mw * 0.7, cy + 1.2), (cx, cy - 1.0), (cx + mw * 0.7, cy + 1.2), sh(lip, 0.65), 1.1)
    elif k == 'grit':
        d.rounded_rectangle(B(cx - mw * 0.7, cy - 1.0, cx + mw * 0.7, cy + 1.8), radius=U, fill=(246, 242, 232), outline=dark, width=U)
        d.line([P(cx - mw * 0.7, cy + 0.4), P(cx + mw * 0.7, cy + 0.4)], fill=sh(dark, 1.6), width=max(1, U // 2))
    elif k == 'tight':
        d.line([P(cx - mw * 0.65, cy + 0.3), P(cx + mw * 0.65, cy + 0.3)], fill=sh(lip, 0.6), width=int(1.2 * U * Z))
    elif k == 'wavy':
        pts = [(cx - mw * 0.6 + i * mw * 0.12, cy + 0.6 + math.sin(i * 1.4) * 0.6) for i in range(11)]
        d.line(poly(pts), fill=sh(lip, 0.65), width=int(1.0 * U * Z))
    elif k == 'side':
        curve(d, (cx - mw * 0.4, cy + 0.6), (cx + mw * 0.2, cy + 0.8), (cx + mw * 0.8, cy - 0.6), sh(lip, 0.65), 1.1)

def soft_spot(im, boxes, col, alpha, blur):
    """부드러운 색 얼룩 (투명한 둘레가 검게 번지지 않게 알파만 흐림)"""
    m = Image.new('L', im.size, 0); md = ImageDraw.Draw(m)
    for b in boxes: md.ellipse(b, fill=alpha)
    m = m.filter(ImageFilter.GaussianBlur(blur))
    lay = Image.new('RGBA', im.size, col + (0,)); lay.putalpha(m)
    im.alpha_composite(lay)

def face_outline(p):
    """얼굴 테두리 점들 (위 이마 → 오른쪽 볼 → 턱 → 왼쪽)"""
    cx, top, fw = 60, p.get('top', 30), p.get('fw', 24)
    cheek_y = p.get('cheek_y', 66); jaw = p.get('jaw', 0.8); chin_y = p.get('chin', 88); chin_w = p.get('chin_w', 7)
    pts = []
    pts += bez((cx - fw * 0.92, cheek_y - 14), (cx - fw * 1.0, top - 1), (cx, top), 10)
    pts += bez((cx, top), (cx + fw * 1.0, top - 1), (cx + fw * 0.92, cheek_y - 14), 10)[1:]
    pts += bez((cx + fw * 0.92, cheek_y - 14), (cx + fw * 1.02, cheek_y + 2), (cx + fw * jaw, cheek_y + 12), 8)[1:]
    pts += bez((cx + fw * jaw, cheek_y + 12), (cx + chin_w + 4, chin_y), (cx, chin_y), 8)[1:]
    pts += bez((cx, chin_y), (cx - chin_w - 4, chin_y), (cx - fw * jaw, cheek_y + 12), 8)[1:]
    pts += bez((cx - fw * jaw, cheek_y + 12), (cx - fw * 1.02, cheek_y + 2), (cx - fw * 0.92, cheek_y - 14), 8)[1:]
    return pts

def draw_badges(d, p):
    sh_y = p.get('shoulder_y', 102)
    if p.get('flag_pin'):        # 옷깃의 작은 성조기 배지
        x, y = 41, sh_y + 3
        d.rectangle(B(x, y, x + 6, y + 4), fill=(240, 240, 240))
        for k in range(3): d.line([P(x, y + 0.6 + k * 1.4), P(x + 6, y + 0.6 + k * 1.4)], fill=(190, 40, 50), width=max(1, int(0.7 * U * Z)))
        d.rectangle(B(x, y, x + 2.6, y + 2.2), fill=(40, 60, 140))
    if p.get('hero_star'):       # 옷깃의 금별 훈장 (붉은 띠 + 금색 별)
        x, y = 42, sh_y + 1
        d.rectangle(B(x - 2, y, x + 2, y + 3), fill=(200, 40, 40))
        pts = []
        for k in range(10):
            a = -math.pi / 2 + k * math.pi / 5; r = 3.4 if k % 2 == 0 else 1.4
            pts.append((x + math.cos(a) * r, y + 7 + math.sin(a) * r))
        d.polygon(poly(pts), fill=(240, 196, 60))

def draw_clothes(d, p):
    kind = p.get('clothes', 'shirt')
    if kind in NEW_CLOTHES: return draw_clothes2(d, p)
    c = p.get('cloth', (240, 238, 230)); cs = sh(c, 0.82); cd = sh(c, 0.66)
    neck_c = sh(p['skin'], 0.9)
    # 목
    d.polygon(poly([(50, 82), (70, 82), (72, 100), (48, 100)]), fill=neck_c)
    d.polygon(poly([(50, 86), (70, 86), (70, 92), (50, 92)]), fill=sh(p['skin'], 0.82))
    sh_y = p.get('shoulder_y', 102)
    body = [(4, PH), (6, sh_y + 12), (20, sh_y + 2), (44, sh_y - 4), (60, sh_y - 2), (76, sh_y - 4), (100, sh_y + 2), (114, sh_y + 12), (116, PH)]
    if kind in ('durumagi', 'jeogori', 'chima'):
        d.polygon(poly(body), fill=c)
        # 그늘
        d.polygon(poly([(4, PH), (6, sh_y + 12), (20, sh_y + 2), (30, sh_y + 6), (24, PH)]), fill=cs)
        d.polygon(poly([(116, PH), (114, sh_y + 12), (100, sh_y + 2), (92, sh_y + 8), (98, PH)]), fill=cs)
        # 깃(동정 포함): 왼쪽 깃이 오른쪽 위로 덮는 한복 여밈
        dong = (252, 252, 248)
        d.polygon(poly([(44, sh_y - 5), (52, sh_y - 6), (76, PH), (64, PH)]), fill=sh(c, 0.92))
        d.line([P(45, sh_y - 5), P(70, PH)], fill=dong, width=int(3.2 * U * Z))          # 오른쪽→아래 동정
        d.polygon(poly([(76, sh_y - 5), (68, sh_y - 6), (46, PH), (58, PH)]), fill=c)
        d.line([P(75, sh_y - 5), P(52, PH)], fill=dong, width=int(3.2 * U * Z))
        d.line([P(77, sh_y - 4), P(53, PH + 1)], fill=cd, width=U)
        if kind == 'chima' and p.get('goreum'):
            g = p['goreum']
            d.polygon(poly([(62, 120), (66, 118), (72, PH), (66, PH)]), fill=g)
            d.polygon(poly([(62, 120), (58, 122), (54, PH), (60, PH)]), fill=sh(g, 0.85))
            d.ellipse(B(59, 116, 67, 123), fill=g)
    elif kind in ('suit', 'gakuran', 'vest', 'jacket', 'shirt', 'padded'):
        shirt = p.get('shirt', (244, 244, 240))
        if kind == 'gakuran':
            d.polygon(poly(body), fill=c)
            d.polygon(poly([(48, sh_y - 8), (72, sh_y - 8), (74, sh_y + 2), (60, sh_y + 4), (46, sh_y + 2)]), fill=sh(c, 1.15))   # 세운 깃
            d.line([P(60, sh_y + 4), P(60, PH)], fill=cd, width=U)
            for yy in (sh_y + 10, sh_y + 20): d.ellipse(B(58.5, yy - 1.6, 61.5, yy + 1.6), fill=(232, 200, 110))
            d.polygon(poly([(4, PH), (6, sh_y + 12), (20, sh_y + 2), (28, sh_y + 8), (22, PH)]), fill=cs)
        elif kind == 'shirt':
            d.polygon(poly(body), fill=shirt)
            d.polygon(poly([(50, sh_y - 7), (60, sh_y + 4), (70, sh_y - 7), (74, sh_y), (60, sh_y + 8), (46, sh_y)]), fill=sh(shirt, 0.9))
            d.line([P(60, sh_y + 6), P(60, PH)], fill=sh(shirt, 0.8), width=U)
        else:
            d.polygon(poly(body), fill=c)
            d.polygon(poly([(4, PH), (6, sh_y + 12), (20, sh_y + 2), (28, sh_y + 8), (22, PH)]), fill=cs)
            d.polygon(poly([(116, PH), (114, sh_y + 12), (100, sh_y + 2), (94, sh_y + 8), (98, PH)]), fill=cs)
            # 셔츠 V
            if kind != 'padded':
                d.polygon(poly([(48, sh_y - 7), (72, sh_y - 7), (66, PH - (0 if kind == 'vest' else 8)), (54, PH - (0 if kind == 'vest' else 8))]), fill=shirt)
                d.polygon(poly([(48, sh_y - 7), (60, sh_y + 3), (72, sh_y - 7), (74, sh_y - 1), (60, sh_y + 7), (46, sh_y - 1)]), fill=sh(shirt, 0.9))
            else:
                d.polygon(poly([(46, sh_y - 7), (74, sh_y - 7), (74, sh_y + 2), (46, sh_y + 2)]), fill=sh(c, 1.12))
                for yy in range(int(sh_y + 8), PH, 6): d.line([P(10, yy), P(110, yy)], fill=cs, width=U)
            tie = p.get('tie')
            if p.get('bowtie'):
                bt = p['bowtie']
                d.polygon(poly([(60, sh_y + 5), (53, sh_y + 1), (53, sh_y + 9)]), fill=bt); d.polygon(poly([(60, sh_y + 5), (67, sh_y + 1), (67, sh_y + 9)]), fill=bt)
                d.ellipse(B(58.5, sh_y + 3.5, 61.5, sh_y + 6.5), fill=sh(bt, 0.8))
                if p.get('tie_pattern') == 'dots':
                    for (tx, ty) in ((55, sh_y + 4), (65, sh_y + 6), (55.5, sh_y + 7), (64.5, sh_y + 3)): d.ellipse(B(tx - 0.7, ty - 0.7, tx + 0.7, ty + 0.7), fill=(240, 240, 240))
                tie = None
            if tie and kind != 'padded':
                d.polygon(poly([(57.5, sh_y + 3), (62.5, sh_y + 3), (61.5, sh_y + 7)]), fill=sh(tie, 0.8))
                d.polygon(poly([(58, sh_y + 7), (62, sh_y + 7), (64, PH - 2), (60, PH), (56, PH - 2)]), fill=tie)
                if p.get('tie_pattern') == 'dots':
                    for (tx, ty) in ((59, sh_y + 12), (61.5, sh_y + 17), (59.5, sh_y + 22), (61, sh_y + 27)):
                        d.ellipse(B(tx - 0.8, ty - 0.8, tx + 0.8, ty + 0.8), fill=sh(tie, 0.6))
                if p.get('tie_pattern') == 'stripe':
                    for k in range(5):
                        y0 = sh_y + 10 + k * 5
                        d.line([P(57, y0 + 2), P(63, y0 - 1)], fill=sh(tie, 1.6), width=U)
            if kind == 'suit':
                # 옷깃(라펠)
                d.polygon(poly([(46, sh_y - 6), (54, sh_y - 5), (58, sh_y + 20), (52, sh_y + 8), (44, sh_y + 4)]), fill=sh(c, 1.1))
                d.polygon(poly([(74, sh_y - 6), (66, sh_y - 5), (62, sh_y + 20), (68, sh_y + 8), (76, sh_y + 4)]), fill=sh(c, 0.92))
                d.line([P(54, sh_y - 5), P(58, sh_y + 21)], fill=cd, width=U); d.line([P(66, sh_y - 5), P(62, sh_y + 21)], fill=cd, width=U)
            if kind == 'vest':
                vc = p.get('vest', (80, 76, 84))
                d.polygon(poly([(30, sh_y + 4), (52, sh_y + 6), (58, PH), (26, PH)]), fill=vc)
                d.polygon(poly([(90, sh_y + 4), (68, sh_y + 6), (62, PH), (94, PH)]), fill=sh(vc, 0.9))
                for yy in (sh_y + 18, sh_y + 25): d.ellipse(B(54.5, yy - 1, 56.5, yy + 1), fill=sh(vc, 0.55))
            if kind == 'jacket':
                d.polygon(poly([(46, sh_y - 7), (56, sh_y - 4), (54, sh_y + 6), (44, sh_y + 2)]), fill=sh(c, 1.12))
                d.polygon(poly([(74, sh_y - 7), (64, sh_y - 4), (66, sh_y + 6), (76, sh_y + 2)]), fill=sh(c, 1.0))
        if p.get('stars'):     # 군복 어깨 계급장
            for sd in (-1, 1):
                for k in range(p['stars']):
                    x = 60 + sd * (30 + k * 4.2); y = p.get('shoulder_y', 102) - 3
                    d.polygon(poly([(x, y - 2.2), (x + 1.8, y), (x, y + 2.2), (x - 1.8, y)]), fill=(250, 220, 90))
        if p.get('scarf'):
            sc = p['scarf']
            d.polygon(poly([(42, sh_y - 8), (78, sh_y - 8), (80, sh_y + 2), (60, sh_y + 6), (40, sh_y + 2)]), fill=sc)
            d.polygon(poly([(64, sh_y), (72, sh_y + 2), (70, PH), (62, PH)]), fill=sh(sc, 0.85))
        if p.get('strap'):
            d.line([P(24, sh_y + 2), P(86, PH)], fill=(70, 50, 36), width=int(2.4 * U * Z))
    if p.get('apron'):
        ap = p['apron']
        d.polygon(poly([(34, PH - 10), (86, PH - 10), (90, PH), (30, PH)]), fill=ap)

def draw_hair_back(d, p):
    hc = p.get('hair_c', (36, 30, 28)); st = p.get('hair', 'short')
    if p.get('hat') in ('eth_crown', 'headscarf', 'nursecap'):
        cx, top, fw = 60, p.get('top', 30), p.get('fw', 24)
        dc = {'eth_crown': (248, 246, 238), 'nursecap': (250, 250, 250)}.get(p['hat'], p.get('hat_c', (236, 230, 214)))
        if p['hat'] == 'headscarf':     # 머릿수건: 턱 아래로 묶은 짧은 수건
            d.polygon(poly([(cx - fw * 1.2, top + 6), (cx - fw * 1.05, top - 12), (cx + fw * 1.05, top - 12), (cx + fw * 1.2, top + 6), (cx + fw * 1.15, 84), (cx - fw * 1.15, 84)]), fill=sh(dc, 0.8))
        else:
            d.polygon(poly([(cx - fw * 1.25, top + 6), (cx - fw * 1.1, top - 12), (cx + fw * 1.1, top - 12), (cx + fw * 1.25, top + 6), (cx + fw * 1.4, 106), (cx - fw * 1.4, 106)]), fill=sh(dc, 0.94))
    if st == 'updo':
        cx, top, fw = 60, p.get('top', 30), p.get('fw', 24)
        d.ellipse(B(cx - fw * 1.12, top - 12, cx + fw * 1.12, top + 30), fill=hc)
    if st == 'queue':
        cx, top, fw = 60, p.get('top', 30), p.get('fw', 24)
        for k in range(7):
            yy = 88 + k * 6
            d.ellipse(B(76 - k * 0.3, yy, 84 - k * 0.3, yy + 7), fill=hc)
            d.arc(B(76 - k * 0.3, yy, 84 - k * 0.3, yy + 7), 200, 340, fill=sh(hc, 1.6), width=U)
    cx, top, fw = 60, p.get('top', 30), p.get('fw', 24)
    if st == 'bob':           # 턱까지 오는 단발
        d.rounded_rectangle(B(cx - fw * 1.14, top - 5, cx + fw * 1.14, p.get('chin', 86) - 2), radius=int(14 * U * Z), fill=hc)
    if st == 'long':          # 어깨 아래까지 긴 머리
        d.polygon(poly([(cx - fw * 1.1, top + 8), (cx - fw * 1.25, 100), (cx - fw * 1.3, PH), (cx + fw * 1.3, PH), (cx + fw * 1.25, 100), (cx + fw * 1.1, top + 8)]), fill=hc)
        d.ellipse(B(cx - fw * 1.12, top - 5, cx + fw * 1.12, top + 40), fill=hc)
    if st == 'perm':          # 둥글게 부푼 파마머리
        for k in range(14):
            a = math.pi * (0.9 + k / 13 * 1.2)
            x = cx + math.cos(a) * fw * 1.12; y = top + 22 + math.sin(a) * 30
            d.ellipse(B(x - 8, y - 8, x + 8, y + 8), fill=hc)
        for (x, y) in ((cx - fw * 1.12, 70), (cx + fw * 1.12, 70), (cx - fw * 1.05, 80), (cx + fw * 1.05, 80)):
            d.ellipse(B(x - 7, y - 7, x + 7, y + 7), fill=hc)
    if st == 'bun':
        d.ellipse(B(cx - fw * 1.02, top - 4, cx + fw * 1.02, top + 34), fill=hc)
    if st == 'braid':
        d.ellipse(B(cx - fw * 1.04, top - 4, cx + fw * 1.04, top + 36), fill=hc)
        # 어깨 위로 넘어온 땋은 머리
        for k in range(6):
            yy = 86 + k * 7
            d.ellipse(B(80 - k * 0.6, yy, 90 - k * 0.6, yy + 8), fill=hc)
            d.arc(B(80 - k * 0.6, yy, 90 - k * 0.6, yy + 8), 200, 340, fill=sh(hc, 1.6), width=U)
        d.polygon(poly([(80, 128), (88, 128), (90, PH), (78, PH)]), fill=p.get('daenggi', (170, 40, 50)))

def draw_hair_front(d, p):
    hc = p.get('hair_c', (36, 30, 28)); st = p.get('hair', 'short')
    if st in NEW_HAIR: return draw_hair2(d, p)
    hl = sh(hc, 1.35) if sum(hc) < 300 else sh(hc, 1.08)
    hs = sh(hc, 0.72)
    cx, top, fw = 60, p.get('top', 30), p.get('fw', 24)
    line_y = p.get('hairline', top + 9)
    if st == 'crop':          # 아주 짧게 깎은 머리 (김구)
        pts = bez((cx - fw * 0.98, line_y + 8), (cx - fw * 1.02, top - 3), (cx, top - 2.5), 10) + bez((cx, top - 2.5), (cx + fw * 1.02, top - 3), (cx + fw * 0.98, line_y + 8), 10)[1:]
        pts += bez((cx + fw * 0.98, line_y + 8), (cx + fw * 0.5, line_y - 1), (cx, line_y - 1.5), 8)[1:] + bez((cx, line_y - 1.5), (cx - fw * 0.5, line_y - 1), (cx - fw * 0.98, line_y + 8), 8)[1:]
        d.polygon(poly(pts), fill=mix(hc, p['skin'], 0.28))
        for i in range(70):         # 짧은 머리카락 점
            a = i * 2.39996; r = (i / 70) ** 0.5
            x = cx + math.cos(a) * fw * 0.85 * r; y = top + 2 + abs(math.sin(a)) * (line_y - top) * r * 0.9
            d.rectangle(B(x, y, x + 0.8, y + 0.8), fill=hs)
        # 옆머리
        d.polygon(poly([(cx - fw * 0.99, line_y + 3), (cx - fw * 0.9, line_y + 3), (cx - fw * 0.93, line_y + 16), (cx - fw * 1.0, line_y + 14)]), fill=mix(hc, p['skin'], 0.2))
        d.polygon(poly([(cx + fw * 0.99, line_y + 3), (cx + fw * 0.9, line_y + 3), (cx + fw * 0.93, line_y + 16), (cx + fw * 1.0, line_y + 14)]), fill=mix(hc, p['skin'], 0.2))
        return
    if st == 'slick_white':   # 이승만: 뒤로 넘긴 흰머리, 위로 부풀고 관자놀이가 들어감
        pts = bez((cx - fw * 1.0, line_y + 12), (cx - fw * 1.18, top - 12), (cx - 2, top - 13), 12) + bez((cx - 2, top - 13), (cx + fw * 1.2, top - 11), (cx + fw * 1.0, line_y + 12), 12)[1:]
        pts += [(cx + fw * 0.9, line_y + 12), (cx + fw * 0.78, line_y + 1)] + bez((cx + fw * 0.78, line_y + 1), (cx, line_y - 6), (cx - fw * 0.78, line_y + 1), 10)[1:] + [(cx - fw * 0.9, line_y + 12)]
        d.polygon(poly(pts), fill=hc)
        # 뒤로 빗어 넘긴 결: 이마선과 나란한 곡선 몇 줄 + 윗부분 광택
        for k in range(4):
            yy = line_y - 3 - k * 3.4
            curve(d, (cx - fw * (0.86 - k * 0.04), yy + 4), (cx, yy - 4.5), (cx + fw * (0.86 - k * 0.04), yy + 4), sh(hc, 0.78), 0.55)
        curve(d, (cx - fw * 0.6, top - 5), (cx - fw * 0.05, top - 10.5), (cx + fw * 0.5, top - 6), (255, 255, 255), 1.3)
        # 관자놀이 들어간 곳 + 옆머리 짧게
        d.polygon(poly([(cx - fw * 0.98, line_y + 12), (cx - fw * 0.9, line_y + 4), (cx - fw * 0.84, line_y + 14)]), fill=sh(hc, 0.86))
        d.polygon(poly([(cx + fw * 0.98, line_y + 12), (cx + fw * 0.9, line_y + 4), (cx + fw * 0.84, line_y + 14)]), fill=sh(hc, 0.86))
        return
    if st == 'wavy_gray':     # 여운형: 회색 머리를 뒤로 넘김, 위가 풍성
        pts = bez((cx - fw * 1.02, line_y + 13), (cx - fw * 1.16, top - 9), (cx + 2, top - 11), 12) + bez((cx + 2, top - 11), (cx + fw * 1.18, top - 9), (cx + fw * 1.02, line_y + 13), 12)[1:]
        pts += [(cx + fw * 0.92, line_y + 13), (cx + fw * 0.82, line_y + 2)] + bez((cx + fw * 0.82, line_y + 2), (cx, line_y - 4), (cx - fw * 0.82, line_y + 2), 10)[1:] + [(cx - fw * 0.92, line_y + 13)]
        d.polygon(poly(pts), fill=hc)
        # 왼쪽 가르마에서 오른쪽 뒤로 물결치며 넘긴 결
        d.line([P(cx - fw * 0.45, line_y - 2), P(cx - fw * 0.5, top - 8)], fill=sh(hc, 0.66), width=int(U * Z))
        for k in range(5):
            y0 = top - 7 + k * 3.2
            curve(d, (cx - fw * 0.42, y0), (cx + fw * 0.2, y0 - 3 + (k % 2) * 2), (cx + fw * 0.95, y0 + 3), sh(hc, 0.78) if k % 2 else sh(hc, 1.12), 0.8)
        curve(d, (cx - fw * 0.95, top + 2), (cx - fw * 0.8, top - 8), (cx - fw * 0.5, top - 9), sh(hc, 1.15), 1.0)
        return
    if st == 'slick_back':    # 김규식: 넓은 이마, 뒤로 빗어 넘긴 짙은 머리
        pts = bez((cx - fw * 1.0, line_y + 14), (cx - fw * 1.08, top - 5), (cx, top - 6), 12) + bez((cx, top - 6), (cx + fw * 1.08, top - 5), (cx + fw * 1.0, line_y + 14), 12)[1:]
        pts += [(cx + fw * 0.9, line_y + 14), (cx + fw * 0.72, line_y)] + bez((cx + fw * 0.72, line_y), (cx, line_y - 7), (cx - fw * 0.72, line_y), 10)[1:] + [(cx - fw * 0.9, line_y + 14)]
        d.polygon(poly(pts), fill=hc)
        # 기름 발라 매끈하게 넘긴 머리: 넓은 광택 띠 + 가는 결 몇 줄
        curve(d, (cx - fw * 0.7, top + 1), (cx, top - 6), (cx + fw * 0.7, top + 1), sh(hc, 1.9), 1.8)
        for k in range(4):
            x0 = cx - fw * 0.45 + k * fw * 0.3
            curve(d, (x0, line_y - 4.5), (x0 + (x0 - cx) * 0.1, top + 1), (x0 + (x0 - cx) * 0.2, top - 3), sh(hc, 1.35), 0.5)
        return
    if st == 'bald':          # 머리가 거의 없음 (귀 위 옆머리만 조금)
        ey = p.get('eye_y', 61)
        for sd in (-1, 1):
            d.polygon(poly([(cx + sd * fw * 1.0, ey + 2), (cx + sd * fw * 1.01, ey - 12), (cx + sd * fw * 0.9, ey - 14), (cx + sd * fw * 0.86, ey + 1)]), fill=mix(hc, p['skin'], 0.45))
        curve(d, (cx - fw * 0.45, top + 4), (cx - fw * 0.1, top - 1), (cx + fw * 0.35, top + 2), sh(p['skin'], 1.1), 1.6)
        return
    if st == 'bob':
        pts = bez((cx - fw * 1.1, line_y + 22), (cx - fw * 1.16, top - 7), (cx, top - 7), 12) + bez((cx, top - 7), (cx + fw * 1.16, top - 7), (cx + fw * 1.1, line_y + 22), 12)[1:]
        pts += [(cx + fw * 0.92, line_y + 22), (cx + fw * 0.9, line_y + 4), (cx + fw * 0.4, line_y + 5), (cx, line_y + 6), (cx - fw * 0.4, line_y + 5), (cx - fw * 0.9, line_y + 4), (cx - fw * 0.92, line_y + 22)]
        d.polygon(poly(pts), fill=hc)
        curve(d, (cx - fw * 0.7, top + 1), (cx - fw * 0.1, top - 6), (cx + fw * 0.6, top - 1), hl, 1.6)
        for k in range(6):
            x0 = cx - fw * 0.7 + k * fw * 0.28
            d.line([P(x0, line_y - 2), P(x0 + 0.5, line_y + 5)], fill=hs, width=U)
        return
    if st in ('long', 'perm'):     # 옆 가르마로 얼굴 옆을 덮는 머리
        pts = bez((cx - fw * 1.12, line_y + 26), (cx - fw * 1.2, top - 7), (cx, top - 7), 12) + bez((cx, top - 7), (cx + fw * 1.2, top - 7), (cx + fw * 1.12, line_y + 26), 12)[1:]
        pts += [(cx + fw * 0.94, line_y + 26), (cx + fw * 0.9, line_y + 6)] + bez((cx + fw * 0.9, line_y + 6), (cx + fw * 0.2, line_y - 5), (cx - fw * 0.35, line_y - 2), 8)[1:]
        pts += bez((cx - fw * 0.35, line_y - 2), (cx - fw * 0.8, line_y + 2), (cx - fw * 0.92, line_y + 14), 6)[1:] + [(cx - fw * 0.94, line_y + 26)]
        d.polygon(poly(pts), fill=hc)
        curve(d, (cx - fw * 0.7, top + 1), (cx - fw * 0.1, top - 6), (cx + fw * 0.6, top - 1), hl, 1.6)
        d.line([P(cx - fw * 0.35, top - 5), P(cx - fw * 0.35, line_y - 2)], fill=hs, width=U)
        if st == 'perm':      # 곱슬곱슬한 결: 머리 둘레에 작은 원을 겹침
            for k in range(12):
                a = math.pi * (1.0 + k / 11 * 1.0)
                x = cx + math.cos(a) * fw * 1.08; y = top + 12 + math.sin(a) * 18
                d.ellipse(B(x - 5, y - 5, x + 5, y + 5), fill=hc)
                d.arc(B(x - 3.5, y - 3.5, x + 3.5, y + 3.5), 180, 330, fill=hl, width=U)
        return
    if st == 'bun' or st == 'braid' or st == 'center':   # 가운데 가르마, 뒤로 묶음
        pts = bez((cx - fw * 1.02, line_y + 18), (cx - fw * 1.1, top - 4), (cx, top - 3), 12) + bez((cx, top - 3), (cx + fw * 1.1, top - 4), (cx + fw * 1.02, line_y + 18), 12)[1:]
        pts += [(cx + fw * 0.9, line_y + 18)] + bez((cx + fw * 0.9, line_y + 18), (cx + fw * 0.7, line_y - 2), (cx, line_y - 1), 10)[1:] + bez((cx, line_y - 1), (cx - fw * 0.7, line_y - 2), (cx - fw * 0.9, line_y + 18), 10)[1:]
        d.polygon(poly(pts), fill=hc)
        d.line([P(cx, top - 3), P(cx, line_y - 1)], fill=sh(p['skin'], 0.95), width=U)
        curve(d, (cx - fw * 0.8, top + 2), (cx - fw * 0.5, top - 2), (cx - 2, top - 2), hl, 1.0)
        curve(d, (cx + fw * 0.8, top + 2), (cx + fw * 0.5, top - 2), (cx + 2, top - 2), hl, 1.0)
        return
    # 소년·청년 머리 (short: 앞머리 / part: 옆 가르마 / messy)
    pts = bez((cx - fw * 1.04, line_y + 13), (cx - fw * 1.14, top - 6), (cx, top - 6), 12) + bez((cx, top - 6), (cx + fw * 1.14, top - 6), (cx + fw * 1.04, line_y + 13), 12)[1:]
    if st == 'short':
        fr = [(cx + fw * 0.96, line_y + 13), (cx + fw * 0.8, line_y + 2), (cx + fw * 0.5, line_y + 6), (cx + fw * 0.3, line_y + 1), (cx + 2, line_y + 7), (cx - fw * 0.22, line_y + 1),
              (cx - fw * 0.5, line_y + 6), (cx - fw * 0.75, line_y + 1), (cx - fw * 0.96, line_y + 13)]
    elif st == 'part':
        fr = [(cx + fw * 0.96, line_y + 12), (cx + fw * 0.85, line_y + 1)] + bez((cx + fw * 0.85, line_y + 1), (cx - fw * 0.1, line_y - 6), (cx - fw * 0.4, line_y + 4), 8)[1:] + [(cx - fw * 0.5, line_y - 3), (cx - fw * 0.85, line_y + 3), (cx - fw * 0.96, line_y + 12)]
    elif st == 'messy':
        fr = [(cx + fw * 0.98, line_y + 13), (cx + fw * 0.86, line_y + 1), (cx + fw * 0.66, line_y + 7), (cx + fw * 0.4, line_y), (cx + fw * 0.12, line_y + 8), (cx - fw * 0.15, line_y + 1),
              (cx - fw * 0.42, line_y + 8), (cx - fw * 0.62, line_y), (cx - fw * 0.85, line_y + 6), (cx - fw * 0.98, line_y + 13)]
    else:   # slick (아버지)
        fr = [(cx + fw * 0.95, line_y + 10), (cx + fw * 0.8, line_y)] + bez((cx + fw * 0.8, line_y), (cx, line_y - 6), (cx - fw * 0.8, line_y), 10)[1:] + [(cx - fw * 0.95, line_y + 10)]
    d.polygon(poly(pts + fr), fill=hc)
    curve(d, (cx - fw * 0.7, top + 1), (cx - fw * 0.1, top - 6), (cx + fw * 0.6, top - 1), hl, 1.6)
    if st == 'part': d.line([P(cx - fw * 0.42, top - 4), P(cx - fw * 0.45, line_y - 2)], fill=hs, width=U)
    if st in ('short', 'messy'):
        for k in range(5):
            x0 = cx - fw * 0.6 + k * fw * 0.3
            curve(d, (x0, top + 3), (x0 + 1, line_y - 1), (x0 + 2.5, line_y + 4), hs, 0.6)
    if st == 'slick':
        for k in range(6):
            x0 = cx - fw * 0.6 + k * fw * 0.24
            curve(d, (x0, line_y - 2), (x0 + 2, top), (x0 + 6, top - 4), hs, 0.6)

def draw_hat(d, p):
    hat = p.get('hat'); cx, top, fw = 60, p.get('top', 30), p.get('fw', 24)
    if hat in NEW_HATS: return draw_hat2(d, p)
    if hat == 'student':
        hc = p.get('hat_c', (30, 30, 40))
        d.polygon(poly([(cx - fw * 1.1, top + 8), (cx - fw * 1.0, top - 9), (cx, top - 12), (cx + fw * 1.0, top - 9), (cx + fw * 1.1, top + 8)]), fill=hc)
        d.rectangle(B(cx - fw * 1.1, top + 3, cx + fw * 1.1, top + 8), fill=sh(hc, 0.7))
        d.polygon(poly([(cx - fw * 0.95, top + 8), (cx + fw * 0.95, top + 8), (cx + fw * 0.8, top + 13), (cx - fw * 0.8, top + 13)]), fill=(16, 16, 20))   # 챙
        d.line([P(cx - fw * 0.8, top + 8.5), P(cx + fw * 0.8, top + 8.5)], fill=(70, 70, 80), width=U)
        d.ellipse(B(cx - 3, top - 4, cx + 3, top + 2), fill=(228, 196, 100))
        curve(d, (cx - fw * 0.8, top - 6), (cx, top - 10), (cx + fw * 0.6, top - 6), sh(hc, 1.5), 0.8)
    elif hat == 'towel':
        tc = p.get('hat_c', (236, 234, 226))
        d.polygon(poly(bez((cx - fw * 1.1, top + 10), (cx, top - 16), (cx + fw * 1.1, top + 10), 14) + [(cx + fw * 1.0, top + 12), (cx - fw * 1.0, top + 12)]), fill=tc)
        curve(d, (cx - fw * 1.0, top + 9), (cx, top + 2), (cx + fw * 1.0, top + 9), sh(tc, 0.82), 0.8)
        d.polygon(poly([(cx + fw * 0.9, top + 2), (cx + fw * 1.2, top - 2), (cx + fw * 1.25, top + 6), (cx + fw * 1.02, top + 8)]), fill=sh(tc, 0.92))
    elif hat == 'beanie':
        hc = p.get('hat_c', (70, 70, 76))
        d.polygon(poly(bez((cx - fw * 1.08, top + 9), (cx, top - 22), (cx + fw * 1.08, top + 9), 14)), fill=hc)
        d.rectangle(B(cx - fw * 1.08, top + 3, cx + fw * 1.08, top + 10), fill=sh(hc, 0.82))
        for k in range(10): d.line([P(cx - fw + k * fw * 0.22, top + 3), P(cx - fw + k * fw * 0.22, top + 10)], fill=sh(hc, 0.68), width=U // 2 + 1)
    elif hat == 'fedora':
        hc = p.get('hat_c', (80, 74, 66))
        d.ellipse(B(cx - fw * 1.5, top + 3, cx + fw * 1.5, top + 11), fill=sh(hc, 0.85))
        d.polygon(poly([(cx - fw * 0.95, top + 7), (cx - fw * 0.85, top - 12), (cx, top - 9), (cx + fw * 0.85, top - 12), (cx + fw * 0.95, top + 7)]), fill=hc)
        d.rectangle(B(cx - fw * 0.95, top + 1, cx + fw * 0.95, top + 6), fill=sh(hc, 0.5))

def draw_glasses(d, p, lx, rx, ey):
    kind = p.get('glasses')
    if not kind: return
    col = p.get('glass_c', (20, 18, 18))
    r = p.get('glass_r', 8.4); t = p.get('glass_t', 2.4)
    if kind == 'sun':     # 짙은 선글라스 (각진 알)
        for x in (lx, rx):
            d.rounded_rectangle(B(x - r, ey - r * 0.62, x + r, ey + r * 0.72), radius=int(2.5 * U * Z), fill=(18, 18, 22), outline=col, width=int(t * U * Z))
            d.line([P(x - r + 2, ey - r * 0.4), P(x - r + 5, ey - r * 0.4)], fill=(120, 130, 140), width=U)
        d.line([P(lx + r, ey - 1.5), P(rx - r, ey - 1.5)], fill=col, width=int(t * U * Z))
        d.line([P(lx - r, ey - 1), P(lx - r - 5, ey - 2)], fill=col, width=int(t * 0.8 * U * Z))
        d.line([P(rx + r, ey - 1), P(rx + r + 5, ey - 2)], fill=col, width=int(t * 0.8 * U * Z))
        return
    for x in (lx, rx):
        d.ellipse(B(x - r, ey - r + 0.4, x + r, ey + r + 0.4), outline=col, width=int(t * U * Z))
        d.arc(B(x - r + 2, ey - r + 2.4, x + r - 2, ey + r - 1.6), 200, 250, fill=(255, 255, 255), width=U)
    curve(d, (lx + r - 0.6, ey - 0.6), (60, ey - 2.4), (rx - r + 0.6, ey - 0.6), col, t * 0.8)
    d.line([P(lx - r, ey - 1), P(lx - r - 5, ey - 2)], fill=col, width=int(t * 0.8 * U * Z))
    d.line([P(rx + r, ey - 1), P(rx + r + 5, ey - 2)], fill=col, width=int(t * 0.8 * U * Z))

def render(p, expr='n'):
    ex = EXPR[expr]
    im = Image.new('RGBA', (PW * U, PH * U), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    skin = p['skin']; p = dict(p)
    cx = 60
    draw_hair_back(d, p)
    draw_clothes(d, p)
    draw_badges(d, p)
    # 귀
    ey = p.get('eye_y', 61)
    fw = p.get('fw', 24)
    ear = p.get('ear', 1.0)
    for side in (-1, 1):
        ex0 = cx + side * (fw * 0.98)
        d.ellipse(B(ex0 - 3.4 * ear, ey - 2, ex0 + 3.4 * ear, ey + 9 * ear), fill=sh(skin, 0.92))
        d.ellipse(B(ex0 - 1.6 * ear + side * 0.6, ey, ex0 + 1.6 * ear + side * 0.6, ey + 6 * ear), fill=sh(skin, 0.78))
    # 얼굴
    pts = face_outline(p)
    d.polygon(poly(pts), fill=skin)
    # 얼굴 그늘 (오른쪽 아래)
    shade = Image.new('L', im.size, 0); sd = ImageDraw.Draw(shade)
    sd.polygon(poly(pts), fill=255)
    m = Image.new('L', im.size, 0); md = ImageDraw.Draw(m)
    md.ellipse(B(cx - fw * 0.9, p.get('top', 30) - 4, cx + fw * 0.7, p.get('chin', 88) - 3), fill=255)
    m = m.filter(ImageFilter.GaussianBlur(5 * U))
    sh_mask = Image.fromarray((np.array(shade).astype(float) * (1 - np.array(m) / 255.0) * 0.7).astype(np.uint8))
    im.paste(Image.new('RGBA', im.size, sh(skin, 0.76) + (255,)), (0, 0), sh_mask)
    # 머리카락 아래 이마 그늘
    fsh = Image.new('L', im.size, 0); ImageDraw.Draw(fsh).rectangle(B(0, p.get('hairline', 40) - 2, PW, p.get('hairline', 40) + 3), fill=90)
    fsh = Image.fromarray(np.minimum(np.array(fsh.filter(ImageFilter.GaussianBlur(U * 1.5))), np.array(shade)))
    im.paste(Image.new('RGBA', im.size, sh(skin, 0.8) + (255,)), (0, 0), fsh)
    # 광대 밝은 빛
    soft_spot(im, [B(cx - fw * 0.72, ey + 3, cx - fw * 0.28, ey + 10)], sh(skin, 1.1), 120, U * 1.6)
    d = ImageDraw.Draw(im)
    # 볼 홍조
    if p.get('blush') or (ex.get('happy') and p.get('young')):
        soft_spot(im, [B(x - 5, ey + 5.5, x + 5, ey + 10) for x in (cx - fw * 0.55, cx + fw * 0.55)], (236, 130, 120), 95, U * 1.3)
        d = ImageDraw.Draw(im)
    # 주름 (나이)
    age = p.get('age_lines', 0)
    wc = sh(skin, 0.8)
    if age >= 1:
        curve(d, (cx - 9, ey + 9), (cx - 12, ey + 15), (cx - 10.5, ey + 21), wc, 0.7)
        curve(d, (cx + 9, ey + 9), (cx + 12, ey + 15), (cx + 10.5, ey + 21), wc, 0.7)
    if age >= 2:
        for k in range(3):
            yy = p.get('top', 30) + 7 + k * 2.6
            curve(d, (cx - 11 + k, yy), (cx, yy - 1.2), (cx + 11 - k, yy), wc, 0.55)
        for side in (-1, 1):
            x0 = cx + side * 18
            d.line([P(x0, ey), P(x0 + side * 3, ey - 1.5)], fill=wc, width=U // 2 + 1)
            d.line([P(x0, ey + 1.5), P(x0 + side * 3, ey + 2.5)], fill=wc, width=U // 2 + 1)
    if age >= 3:
        curve(d, (cx - 5, p.get('chin', 88) - 1), (cx, p.get('chin', 88) + 1.5), (cx + 5, p.get('chin', 88) - 1), wc, 0.6)
        curve(d, (cx - 14, ey + 18), (cx - 15, ey + 22), (cx - 12, ey + 25), wc, 0.6)
        curve(d, (cx + 14, ey + 18), (cx + 15, ey + 22), (cx + 12, ey + 25), wc, 0.6)
    draw_hair_front(d, p)
    # 눈썹·눈
    gap = p.get('eye_gap', 11)
    lx, rx = cx - gap, cx + gap
    draw_brow(d, lx, ey - p.get('brow_dy', 7.5), p, ex, -1)
    draw_brow(d, rx, ey - p.get('brow_dy', 7.5), p, ex, 1)
    draw_eye(d, lx, ey, p, ex, -1)
    draw_eye(d, rx, ey, p, ex, 1)
    # 코
    nw = p.get('nose_w', 3.6); ny = p.get('nose_y', ey + 12)
    nc = sh(skin, 0.62)
    curve(d, (cx - 1.5, ey + 2), (cx - 2.4, ny - 4), (cx - 1.8, ny - 1), sh(skin, 0.88), 0.7)
    d.arc(B(cx - nw - 1.4, ny - 2.4, cx - nw + 2.2, ny + 1.6), 90, 270, fill=nc, width=U)
    d.arc(B(cx + nw - 2.2, ny - 2.4, cx + nw + 1.4, ny + 1.6), 270, 450, fill=nc, width=U)
    d.line([P(cx - nw * 0.4, ny + 1.2), P(cx + nw * 0.4, ny + 1.2)], fill=nc, width=U)
    d.ellipse(B(cx - 1.2, ny - 3.4, cx + 1.8, ny - 1.0), fill=sh(skin, 1.06))
    # 수염
    if p.get('mustache'):
        mc = p['mustache']; my = ny + 2.2; mw = p.get('must_w', 7.5)
        pts = [(cx - mw, my + 3.4), (cx - mw * 0.7, my + 0.2), (cx - 1, my - 0.5), (cx, my + 0.3), (cx + 1, my - 0.5), (cx + mw * 0.7, my + 0.2), (cx + mw, my + 3.4),
               (cx + mw * 0.5, my + 3.0), (cx, my + 2.6), (cx - mw * 0.5, my + 3.0)]
        d.polygon(poly(pts), fill=mc)
        curve(d, (cx - mw * 0.8, my + 2.2), (cx, my + 1.0), (cx + mw * 0.8, my + 2.2), sh(mc, 0.8), 0.5)
    if p.get('stubble'):
        st_ = Image.new('RGBA', im.size, (0, 0, 0, 0)); sd2 = ImageDraw.Draw(st_)
        sd2.polygon(poly(bez((cx - fw * 0.8, ey + 14), (cx, p.get('chin', 88) + 8), (cx + fw * 0.8, ey + 14), 12)), fill=p['stubble'] + (70,))
        sd2.ellipse(B(cx - 10, ny + 4, cx + 10, ny + 12), fill=(0, 0, 0, 0))
        im.alpha_composite(st_)
        d = ImageDraw.Draw(im)
    face_hair_pre(d, p, cx, ny, ey, fw)
    draw_mouth(d, cx, p.get('mouth_y', ny + 7.5), p, ex)
    face_hair_post(d, p, cx, ny, ey, fw)
    draw_glasses(d, p, lx, rx, ey)
    if p.get('tear') and expr == 'sad':
        d.ellipse(B(rx + 3, ey + 4, rx + 5.4, ey + 8), fill=(170, 210, 240))
    draw_hat(d, p)
    # 줄여서 도트로
    small = im.resize((PW, PH), Image.LANCZOS)
    a = np.array(small)
    a[..., 3] = np.where(a[..., 3] > 110, 255, 0)
    small = Image.fromarray(a)
    rgb = small.convert('RGB').quantize(colors=p.get('colors', 64), method=Image.Quantize.MEDIANCUT, dither=Image.Dither.NONE).convert('RGB')
    out = Image.new('RGBA', (PW, PH), (0, 0, 0, 0)); out.paste(rgb, (0, 0), small.split()[3])
    out = outline(out, 0.42)
    # 외곽선이 아래 끝(몸통)에서 위로 넘어와 생기는 맨 윗줄 선 지우기
    oa = np.array(out); before = np.array(small)[..., 3]
    for y in range(2):
        row = (before[y] == 0) & (before[y + 1] == 0)
        oa[y][row] = 0
    out = Image.fromarray(oa)
    return out.resize((PW * 2, PH * 2), Image.NEAREST)


# ==================================================================== 전보 소년 편에서 더한 것: 옷 · 모자 · 머리 · 수염
NEW_CLOTHES = {'tunic', 'messenger', 'frock', 'shamma', 'robe', 'kurta', 'blouse', 'overall', 'sari', 'wrap'}
NEW_HATS = {'kepi', 'garrison', 'cloche', 'beret', 'm1', 'warden', 'headset', 'pillbox', 'boater', 'bowler', 'tophat', 'pickel', 'svcap', 'brodie', 'turban', 'fez', 'feltbrim', 'topee', 'cocked', 'mobcap', 'nursecap',
            'flatcap', 'eth_crown', 'qingcap', 'stahl', 'headscarf', 'peaked', 'wreath', 'corinth_up', 'tiara', 'kausia', 'diadem', 'nemes', 'petasos'}
NEW_HAIR = {'curly', 'updo', 'queue'}

def _neck(d, p):
    neck_c = sh(p['skin'], 0.9)
    d.polygon(poly([(50, 82), (70, 82), (72, 100), (48, 100)]), fill=neck_c)
    d.polygon(poly([(50, 86), (70, 86), (70, 92), (50, 92)]), fill=sh(p['skin'], 0.82))

def _body(p):
    sh_y = p.get('shoulder_y', 102)
    return sh_y, [(4, PH), (6, sh_y + 12), (20, sh_y + 2), (44, sh_y - 4), (60, sh_y - 2), (76, sh_y - 4), (100, sh_y + 2), (114, sh_y + 12), (116, PH)]

def draw_clothes2(d, p):
    kind = p['clothes']
    c = p.get('cloth', (70, 70, 80)); cs = sh(c, 0.82); cd = sh(c, 0.62)
    _neck(d, p)
    sh_y, body = _body(p)
    shade_l = [(4, PH), (6, sh_y + 12), (20, sh_y + 2), (28, sh_y + 8), (22, PH)]
    shade_r = [(116, PH), (114, sh_y + 12), (100, sh_y + 2), (94, sh_y + 8), (98, PH)]
    if kind in ('tunic', 'messenger'):
        d.polygon(poly(body), fill=c); d.polygon(poly(shade_l), fill=cs); d.polygon(poly(shade_r), fill=cs)
        col = p.get('collar_c', sh(c, 0.9))
        d.polygon(poly([(46, sh_y - 9), (74, sh_y - 9), (75, sh_y + 1), (60, sh_y + 3), (45, sh_y + 1)]), fill=col)   # 세운 깃
        if p.get('collar_tab'):
            for sd in (-1, 1): d.polygon(poly([(60 + sd * 6, sh_y - 7), (60 + sd * 13, sh_y - 7), (60 + sd * 13, sh_y - 1), (60 + sd * 6, sh_y + 1)]), fill=p['collar_tab'])
        d.line([P(60, sh_y + 3), P(60, PH)], fill=cd, width=U)
        btn = p.get('buttons', (226, 196, 110))
        for yy in range(int(sh_y + 8), PH, 8): d.ellipse(B(58.4, yy - 1.6, 61.6, yy + 1.6), fill=btn)
        if kind == 'messenger':
            pc = p.get('piping', (190, 40, 40))
            d.line([P(46, sh_y + 1), P(60, sh_y + 3), P(74, sh_y + 1)], fill=pc, width=int(1.2 * U * Z))
            d.line([P(62.5, sh_y + 4), P(62.5, PH)], fill=pc, width=U)
            d.line([P(24, sh_y + 2), P(86, PH)], fill=(70, 50, 36), width=int(2.4 * U * Z))   # 가방끈
        elif not p.get('nopockets'):
            for sd in (-1, 1):
                x0 = 60 + sd * 22
                d.rectangle(B(min(x0, x0 + sd * 14), sh_y + 10, max(x0, x0 + sd * 14), sh_y + 22), fill=sh(c, 0.92))
                d.rectangle(B(min(x0, x0 + sd * 14), sh_y + 10, max(x0, x0 + sd * 14), sh_y + 13), fill=cs)
        if p.get('epaulet'):
            for sd in (-1, 1): d.polygon(poly([(60 + sd * 22, sh_y - 3), (60 + sd * 40, sh_y + 3), (60 + sd * 40, sh_y + 8), (60 + sd * 22, sh_y + 2)]), fill=p['epaulet'])
        if p.get('medals'):
            for k, mc in enumerate(p['medals']):
                x = 36 + k * 5
                d.rectangle(B(x, sh_y + 8, x + 4, sh_y + 11), fill=mc); d.ellipse(B(x + 0.5, sh_y + 12, x + 3.5, sh_y + 15), fill=(220, 190, 100))
        if p.get('order_star'):
            x, y = 80, sh_y + 20
            for k in range(8):
                a = k * math.pi / 4
                d.line([P(x, y), P(x + math.cos(a) * 5, y + math.sin(a) * 5)], fill=(230, 220, 200), width=int(1.4 * U * Z))
    elif kind == 'frock':
        shirt = p.get('shirt', (246, 246, 242))
        d.polygon(poly(body), fill=c); d.polygon(poly(shade_l), fill=cs); d.polygon(poly(shade_r), fill=cs)
        d.polygon(poly([(47, sh_y - 9), (73, sh_y - 9), (68, PH - 6), (52, PH - 6)]), fill=shirt)
        d.polygon(poly([(47, sh_y - 9), (53, sh_y - 8), (56, sh_y - 2), (49, sh_y - 1)]), fill=sh(shirt, 0.92))     # 날개 깃
        d.polygon(poly([(73, sh_y - 9), (67, sh_y - 8), (64, sh_y - 2), (71, sh_y - 1)]), fill=sh(shirt, 0.92))
        tie = p.get('tie', (40, 40, 46))
        if p.get('cravat'):
            d.polygon(poly([(54, sh_y - 4), (66, sh_y - 4), (64, sh_y + 10), (60, sh_y + 13), (56, sh_y + 10)]), fill=tie)
        else:
            d.polygon(poly([(56, sh_y - 4), (64, sh_y - 4), (62, sh_y), (58, sh_y)]), fill=tie)
            d.polygon(poly([(58.5, sh_y), (61.5, sh_y), (63, PH - 8), (60, PH - 6), (57, PH - 8)]), fill=tie)
        if p.get('vest'):
            d.polygon(poly([(50, sh_y + 6), (58, sh_y + 10), (58, PH), (46, PH)]), fill=p['vest']); d.polygon(poly([(70, sh_y + 6), (62, sh_y + 10), (62, PH), (74, PH)]), fill=sh(p['vest'], 0.9))
        d.polygon(poly([(44, sh_y - 6), (52, sh_y - 5), (56, sh_y + 24), (48, sh_y + 10)]), fill=sh(c, 1.15))
        d.polygon(poly([(76, sh_y - 6), (68, sh_y - 5), (64, sh_y + 24), (72, sh_y + 10)]), fill=sh(c, 0.92))
        if p.get('sash'):
            d.polygon(poly([(20, sh_y + 2), (30, sh_y - 2), (104, PH), (90, PH)]), fill=p['sash'])
        if p.get('order_star'):
            x, y = 36, sh_y + 20
            for k in range(8):
                a = k * math.pi / 4
                d.line([P(x, y), P(x + math.cos(a) * 5, y + math.sin(a) * 5)], fill=(230, 220, 200), width=int(1.4 * U * Z))
    elif kind == 'shamma':        # 에티오피아: 흰 셔츠 위에 흰 샴마를 왼쪽 어깨로 둘러 걸침 (테두리 띠)
        shirt = p.get('shirt', (244, 242, 234)); bc = p.get('border', (180, 40, 40))
        d.polygon(poly(body), fill=shirt)
        if p.get('cape'):
            d.polygon(poly(body), fill=p['cape']); d.polygon(poly(shade_l), fill=sh(p['cape'], 0.8)); d.polygon(poly(shade_r), fill=sh(p['cape'], 0.8))
            d.polygon(poly([(50, sh_y - 7), (70, sh_y - 7), (66, PH), (54, PH)]), fill=shirt)
            d.line([P(52, sh_y - 6), P(56, PH)], fill=(220, 190, 100), width=int(1.4 * U * Z)); d.line([P(68, sh_y - 6), P(64, PH)], fill=(220, 190, 100), width=int(1.4 * U * Z))
        else:
            sc = c
            d.polygon(poly([(4, PH), (6, sh_y + 12), (20, sh_y + 2), (44, sh_y - 5), (58, sh_y + 6), (96, PH)]), fill=sc)
            d.polygon(poly([(116, PH), (114, sh_y + 12), (100, sh_y + 2), (84, sh_y + 2), (98, PH)]), fill=sh(sc, 0.9))
            d.line([P(44, sh_y - 5), P(96, PH)], fill=bc, width=int(3.0 * U * Z))
            d.line([P(46, sh_y + 2), P(84, PH)], fill=sh(sc, 0.82), width=U)
    elif kind == 'robe':          # 청나라 창파오: 세운 깃 + 오른쪽으로 비스듬히 여밈 + 매듭 단추
        d.polygon(poly(body), fill=c); d.polygon(poly(shade_l), fill=cs); d.polygon(poly(shade_r), fill=cs)
        d.polygon(poly([(48, sh_y - 8), (72, sh_y - 8), (73, sh_y - 1), (47, sh_y - 1)]), fill=sh(c, 1.1))
        d.line([P(60, sh_y - 1), P(64, sh_y + 6), P(86, sh_y + 10)], fill=cd, width=U)
        for (x, y) in ((60, sh_y - 1), (66, sh_y + 7), (76, sh_y + 9), (84, sh_y + 10)): d.ellipse(B(x - 1.4, y - 1.4, x + 1.4, y + 1.4), fill=p.get('knot', (40, 30, 26)))
        if p.get('vest'):
            vc = p['vest']
            d.polygon(poly([(26, sh_y + 6), (46, sh_y - 1), (74, sh_y - 1), (94, sh_y + 6), (96, PH), (24, PH)]), fill=vc)
            d.line([P(60, sh_y - 1), P(60, PH)], fill=sh(vc, 0.6), width=U)
        if p.get('court_badge'):
            d.rectangle(B(44, sh_y + 14, 76, PH), fill=p['court_badge']); d.rectangle(B(48, sh_y + 18, 72, PH), fill=sh(p['court_badge'], 1.2))
        if p.get('beads'):
            pts = bez((40, sh_y), (60, PH + 18), (80, sh_y), 18)
            for (x, y) in pts: d.ellipse(B(x - 1.3, y - 1.3, x + 1.3, y + 1.3), fill=p['beads'])
    elif kind == 'kurta':
        d.polygon(poly(body), fill=c); d.polygon(poly(shade_l), fill=cs); d.polygon(poly(shade_r), fill=cs)
        d.polygon(poly([(52, sh_y - 6), (68, sh_y - 6), (66, sh_y - 2), (54, sh_y - 2)]), fill=sh(c, 0.9))
        d.line([P(60, sh_y - 3), P(60, sh_y + 18)], fill=cd, width=U)
        for yy in (sh_y + 4, sh_y + 10): d.ellipse(B(61, yy - 1, 63, yy + 1), fill=sh(c, 0.6))
        if p.get('shawl'):
            d.polygon(poly([(4, PH), (6, sh_y + 12), (20, sh_y + 2), (40, sh_y - 4), (52, sh_y + 4), (40, PH)]), fill=p['shawl'])
            d.polygon(poly([(116, PH), (114, sh_y + 12), (100, sh_y + 2), (80, sh_y - 4), (68, sh_y + 4), (80, PH)]), fill=sh(p['shawl'], 0.9))
    elif kind == 'blouse':        # 1900년대 여성: 목까지 올라오는 높은 깃 + 브로치 + 볼록한 소매
        d.polygon(poly(body), fill=c)
        for sd in (-1, 1): d.ellipse(B(60 + sd * 46 - 14, sh_y - 2, 60 + sd * 46 + 14, sh_y + 22), fill=c)
        d.polygon(poly(shade_l), fill=cs); d.polygon(poly(shade_r), fill=cs)
        d.polygon(poly([(50, 80), (70, 80), (71, sh_y - 2), (49, sh_y - 2)]), fill=sh(c, 0.97))
        for yy in (84, 88, 92, 96): d.line([P(50, yy), P(70, yy)], fill=sh(c, 0.88), width=max(1, U // 2))
        d.ellipse(B(57.5, sh_y - 3, 62.5, sh_y + 2), fill=p.get('brooch', (220, 190, 100)))
        for k in range(4): d.line([P(52 + k * 5, sh_y + 6), P(53 + k * 5, sh_y + 22)], fill=sh(c, 0.9), width=U)
        if p.get('skirt_band'): d.rectangle(B(20, PH - 6, 100, PH), fill=p['skirt_band'])
        if p.get('apron'): d.polygon(poly([(36, sh_y + 6), (84, sh_y + 6), (88, PH), (32, PH)]), fill=p['apron']); d.rectangle(B(36, sh_y + 4, 40, sh_y + 10), fill=p['apron']); d.rectangle(B(80, sh_y + 4, 84, sh_y + 10), fill=p['apron'])
        if p.get('redcross'):
            d.rectangle(B(56, sh_y + 12, 64, sh_y + 24), fill=(210, 30, 30)); d.rectangle(B(54, sh_y + 15, 66, sh_y + 21), fill=(210, 30, 30))
        if p.get('sash'): d.polygon(poly([(20, sh_y + 2), (30, sh_y - 2), (104, PH), (90, PH)]), fill=p['sash'])
    elif kind == 'overall':
        d.polygon(poly(body), fill=c); d.polygon(poly(shade_l), fill=cs); d.polygon(poly(shade_r), fill=cs)
        d.polygon(poly([(44, sh_y - 6), (60, sh_y + 6), (76, sh_y - 6), (78, sh_y), (60, sh_y + 12), (42, sh_y)]), fill=sh(c, 1.08))
        for yy in range(int(sh_y + 14), PH, 9): d.ellipse(B(58.6, yy - 1.4, 61.4, yy + 1.4), fill=sh(c, 0.6))
        if p.get('badge'): d.ellipse(B(74, sh_y + 10, 82, sh_y + 18), fill=p['badge'])
    elif kind == 'sari':
        bl = p.get('blouse', (200, 60, 50))
        d.polygon(poly(body), fill=bl)
        d.polygon(poly([(4, PH), (6, sh_y + 12), (20, sh_y + 2), (44, sh_y - 4), (60, sh_y), (100, PH)]), fill=c)
        d.line([P(44, sh_y - 4), P(100, PH)], fill=p.get('border', (200, 40, 40)), width=int(3.0 * U * Z))
        d.line([P(30, sh_y + 4), P(78, PH)], fill=sh(c, 0.85), width=U)
    elif kind == 'wrap':
        d.polygon(poly(body), fill=c)
        pc = p.get('pattern', sh(c, 0.6))
        for yy in range(int(sh_y + 4), PH, 7):
            for xx in range(10, 112, 8): d.rectangle(B(xx, yy, xx + 3, yy + 3), fill=pc)
        d.line([P(30, sh_y), P(90, PH)], fill=sh(c, 0.8), width=U)

def draw_hair2(d, p):
    hc = p.get('hair_c', (30, 26, 24)); st = p['hair']
    cx, top, fw = 60, p.get('top', 30), p.get('fw', 24)
    line_y = p.get('hairline', top + 9)
    hl = sh(hc, 1.5) if sum(hc) < 300 else sh(hc, 1.08); hs = sh(hc, 0.7)
    if st == 'curly':      # 짧고 촘촘한 곱슬머리
        pts = bez((cx - fw * 1.0, line_y + 9), (cx - fw * 1.06, top - 6), (cx, top - 6.5), 10) + bez((cx, top - 6.5), (cx + fw * 1.06, top - 6), (cx + fw * 1.0, line_y + 9), 10)[1:]
        pts += bez((cx + fw * 1.0, line_y + 9), (cx + fw * 0.5, line_y - 2), (cx, line_y - 2), 8)[1:] + bez((cx, line_y - 2), (cx - fw * 0.5, line_y - 2), (cx - fw * 1.0, line_y + 9), 8)[1:]
        d.polygon(poly(pts), fill=hc)
        for i in range(90):
            a = i * 2.39996; r = (i / 90) ** 0.5
            x = cx + math.cos(a) * fw * 0.9 * r; y = top - 3 + abs(math.sin(a)) * (line_y - top + 2) * r * 0.9
            d.ellipse(B(x - 1.1, y - 1.1, x + 1.1, y + 1.1), fill=hl if i % 3 == 0 else hs)
        return
    if st == 'updo':       # 깁슨 걸 머리: 앞을 부풀려 올리고 뒤에서 틀어 묶음
        pts = bez((cx - fw * 1.02, line_y + 16), (cx - fw * 1.3, top - 14), (cx, top - 15), 12) + bez((cx, top - 15), (cx + fw * 1.3, top - 14), (cx + fw * 1.02, line_y + 16), 12)[1:]
        pts += [(cx + fw * 0.9, line_y + 16)] + bez((cx + fw * 0.9, line_y + 16), (cx + fw * 0.8, line_y - 4), (cx, line_y - 2), 10)[1:] + bez((cx, line_y - 2), (cx - fw * 0.8, line_y - 4), (cx - fw * 0.9, line_y + 16), 10)[1:]
        d.polygon(poly(pts), fill=hc)
        for k in range(4):
            curve(d, (cx - fw * (0.9 - k * 0.1), line_y + 6), (cx - fw * 0.3, top - 12 + k * 3), (cx + fw * 0.2, top - 6 + k * 3), hs, 0.6)
        curve(d, (cx - fw * 0.7, top - 6), (cx, top - 13), (cx + fw * 0.7, top - 6), hl, 1.4)
        return
    if st == 'queue':      # 변발: 이마부터 정수리 앞쪽은 밀고, 뒤쪽 머리만 길러 땋음
        shaved = mix(p['skin'], (160, 170, 190), 0.12)
        pts = bez((cx - fw * 1.0, line_y + 10), (cx - fw * 1.06, top - 5), (cx, top - 5.5), 10) + bez((cx, top - 5.5), (cx + fw * 1.06, top - 5), (cx + fw * 1.0, line_y + 10), 10)[1:]
        d.polygon(poly(pts + [(cx + fw * 0.95, line_y + 10), (cx - fw * 0.95, line_y + 10)]), fill=shaved)
        d.polygon(poly(bez((cx - fw * 1.0, top + 2), (cx, top - 9), (cx + fw * 1.0, top + 2), 10) + [(cx + fw * 1.0, top - 2), (cx - fw * 1.0, top - 2)]), fill=hc)
        for sd in (-1, 1): d.polygon(poly([(cx + sd * fw * 0.99, line_y + 3), (cx + sd * fw * 0.9, line_y + 3), (cx + sd * fw * 0.93, line_y + 12), (cx + sd * fw * 1.0, line_y + 10)]), fill=hc)
        return

def draw_hat2(d, p):
    hat = p['hat']; cx, top, fw = 60, p.get('top', 30), p.get('fw', 24)
    hc = p.get('hat_c', (40, 36, 34)); hs = sh(hc, 0.7); hl = sh(hc, 1.3)
    if hat == 'wreath':           # 올리브 · 월계관 (머리 둘레 잎)
        wc = p.get('hat_c', (110, 150, 70))
        for side in (-1, 1):
            for k in range(7):
                a = math.radians(200 + k * 20) if side < 0 else math.radians(340 - k * 20)
                x, y = cx + math.cos(a) * fw * 1.02, top + 12 + math.sin(a) * 12
                d.ellipse(B(x - 3.4, y - 1.8, x + 3.4, y + 1.8), fill=wc if k % 2 else sh(wc, 1.25))
        return
    if hat == 'corinth_up':       # 이마 위로 올려 쓴 코린토스식 청동 투구 + 말총 볏 (페리클레스 흉상)
        bz = p.get('hat_c', (176, 136, 70)); crest = p.get('crest', (170, 40, 36))
        d.polygon(poly(bez((cx - fw * 1.0, top - 8), (cx, top - 30), (cx + fw * 1.0, top - 8), 14)), fill=crest)     # 볏 (뒤)
        d.chord(B(cx - fw * 1.12, top - 14, cx + fw * 1.12, top + 30), 180, 360, fill=bz)                          # 투구 둥근 부분
        d.arc(B(cx - fw * 1.0, top - 10, cx + fw * 1.0, top + 26), 200, 340, fill=sh(bz, 1.25), width=int(1.4 * U * Z))
        d.rectangle(B(cx - fw * 1.12, top + 6, cx + fw * 1.12, top + 13), fill=sh(bz, 0.82))                        # 위로 올린 얼굴 가리개
        for sd in (-1, 1): d.ellipse(B(cx + sd * fw * 0.45 - 6, top + 7, cx + sd * fw * 0.45 + 6, top + 12), fill=(40, 30, 24))
        d.rectangle(B(cx - 1.5, top + 6, cx + 1.5, top + 16), fill=sh(bz, 0.7))                                     # 코 가리개
        return
    if hat == 'tiara':            # 페르시아 부드러운 모자 (머리 · 귀 · 턱을 감싸는 천)
        tc = p.get('hat_c', (206, 180, 110))
        d.polygon(poly(bez((cx - fw * 1.15, top + 14), (cx - fw * 0.2, top - 34), (cx + fw * 1.15, top + 14), 16)), fill=tc)
        d.polygon(poly([(cx + 2, top - 14), (cx + 14, top - 22), (cx + 10, top - 8)]), fill=sh(tc, 0.85))
        for sd in (-1, 1): d.polygon(poly([(cx + sd * fw * 1.15, top + 10), (cx + sd * fw * 0.96, top + 10), (cx + sd * fw * 0.98, 88), (cx + sd * fw * 1.2, 88)]), fill=sh(tc, 0.92))
        return
    if hat == 'kausia':           # 마케도니아 넓적한 펠트 모자
        kc = p.get('hat_c', (220, 214, 200))
        d.chord(B(cx - fw * 1.02, top - 4, cx + fw * 1.02, top + 22), 180, 360, fill=sh(kc, 0.92))
        d.ellipse(B(cx - fw * 1.32, top + 2, cx + fw * 1.32, top + 14), fill=kc)
        d.line([P(cx - fw * 1.25, top + 10), P(cx + fw * 1.25, top + 10)], fill=sh(kc, 0.75), width=int(1.2 * U * Z))
        return
    if hat == 'diadem':           # 흰 머리띠 (헬레니즘 왕)
        d.line([P(cx - fw * 1.05, top + 10), P(cx + fw * 1.05, top + 10)], fill=(246, 242, 232), width=int(2.6 * U * Z))
        d.line([P(cx + fw * 1.0, top + 11), P(cx + fw * 1.25, top + 30)], fill=(246, 242, 232), width=int(1.6 * U * Z))
        return
    if hat == 'nemes':            # 이집트 줄무늬 두건
        nc = p.get('hat_c', (226, 206, 130))
        d.polygon(poly(bez((cx - fw * 1.2, top + 16), (cx, top - 26), (cx + fw * 1.2, top + 16), 16) + [(cx + fw * 1.35, 104), (cx + fw * 0.95, 104), (cx + fw * 0.98, top + 16), (cx - fw * 0.98, top + 16), (cx - fw * 0.95, 104), (cx - fw * 1.35, 104)]), fill=nc)
        for k in range(8):
            y = top + 2 + k * 9
            for sd in (-1, 1): d.line([P(cx + sd * fw * 1.0, y), P(cx + sd * fw * 1.3, y)], fill=(40, 70, 130), width=int(1.6 * U * Z))
        d.rectangle(B(cx - fw * 1.0, top + 8, cx + fw * 1.0, top + 12), fill=(40, 70, 130))
        return
    if hat == 'petasos':          # 넓은 챙 여행 모자
        pc = p.get('hat_c', (200, 170, 110))
        d.ellipse(B(cx - fw * 1.8, top + 2, cx + fw * 1.8, top + 12), fill=sh(pc, 0.85))
        d.chord(B(cx - fw * 0.9, top - 16, cx + fw * 0.9, top + 14), 180, 360, fill=pc)
        return
    if hat == 'pillbox_x':
        pass
    elif hat == 'kepi':          # 프랑스 케피 (드골)
        kc = p.get('hat_c', (140, 126, 84))
        d.polygon(poly([(cx - fw * 0.95, top + 4), (cx - fw * 0.85, top - 20), (cx + fw * 0.85, top - 20), (cx + fw * 0.95, top + 4)]), fill=kc)
        d.rectangle(B(cx - fw * 0.95, top - 4, cx + fw * 0.95, top + 4), fill=p.get('band', (30, 30, 36)))
        d.ellipse(B(cx - fw * 0.85, top - 23, cx + fw * 0.85, top - 17), fill=sh(kc, 1.1))
        d.chord(B(cx - fw * 1.0, top - 1, cx + fw * 1.0, top + 14), 0, 180, fill=(30, 28, 26))
        for k in (1, 2): d.line([P(cx - fw * 0.9, top - 4 - k * 5), P(cx + fw * 0.9, top - 4 - k * 5)], fill=(210, 180, 90), width=max(1, U))
    elif hat == 'garrison':      # 접는 군모
        gc = p.get('hat_c', (140, 126, 84))
        d.polygon(poly([(cx - fw * 0.95, top + 2), (cx + fw * 0.85, top + 2), (cx + fw * 0.7, top - 12), (cx - fw * 0.8, top - 8)]), fill=gc)
        d.line([P(cx - fw * 0.95, top + 2), P(cx + fw * 0.85, top + 2)], fill=sh(gc, 0.65), width=int(1.4 * U * Z))
        d.line([P(cx - fw * 0.85, top - 4), P(cx + fw * 0.75, top - 6)], fill=sh(gc, 0.8), width=max(1, U))
    elif hat == 'cloche':
        cc = p.get('hat_c', (110, 50, 70))
        d.chord(B(cx - fw * 1.12, top - 18, cx + fw * 1.12, top + 30), 180, 360, fill=cc)
        d.polygon(poly([(cx - fw * 1.12, top + 6), (cx + fw * 1.12, top + 6), (cx + fw * 1.2, top + 14), (cx - fw * 1.2, top + 14)]), fill=sh(cc, 0.9))
        d.rectangle(B(cx - fw * 1.1, top, cx + fw * 1.1, top + 5), fill=p.get('band', (230, 200, 120)))
    elif hat == 'beret':
        bc = p.get('hat_c', (40, 60, 90))
        d.ellipse(B(cx - fw * 1.15, top - 14, cx + fw * 1.25, top + 6), fill=bc)
        d.line([P(cx - fw * 1.0, top + 2), P(cx + fw * 1.05, top + 2)], fill=sh(bc, 0.7), width=int(1.6 * U * Z))
        d.ellipse(B(cx - 2, top - 17, cx + 2, top - 13), fill=sh(bc, 0.7))
    elif hat in ('m1', 'warden'):
        mc = (30, 30, 32) if hat == 'warden' else p.get('hat_c', (92, 98, 66))
        if hat == 'm1':
            d.chord(B(cx - fw * 1.18, top - 20, cx + fw * 1.18, top + 30), 180, 360, fill=mc)
            d.ellipse(B(cx - fw * 1.3, top + 2, cx + fw * 1.3, top + 10), fill=sh(mc, 0.85))
        else:
            d.chord(B(cx - fw * 0.95, top - 16, cx + fw * 0.95, top + 14), 180, 360, fill=mc)
            d.ellipse(B(cx - fw * 1.55, top - 3, cx + fw * 1.55, top + 6), fill=sh(mc, 1.1))
            d.text(P(cx - 4, top - 13), 'W', fill=(250, 250, 250), font=None)
    elif hat == 'headset':
        d.arc(B(cx - fw * 1.15, top - 14, cx + fw * 1.15, top + 40), 180, 360, fill=(40, 40, 44), width=int(3 * U * Z))
        for sd in (-1, 1): d.rounded_rectangle(B(cx + sd * fw * 1.15 - 5, top + 18, cx + sd * fw * 1.15 + 5, top + 34), radius=int(3 * U * Z), fill=(40, 40, 44))
    elif hat == 'pillbox':
        d.rounded_rectangle(B(cx - fw * 0.75, top - 12, cx + fw * 0.75, top + 2), radius=int(3 * U * Z), fill=hc)
        d.rectangle(B(cx - fw * 0.75, top - 3, cx + fw * 0.75, top + 0.5), fill=p.get('band', (190, 40, 40)))
        d.ellipse(B(cx - 2.5, top - 10, cx + 2.5, top - 5), fill=(226, 196, 110))
    elif hat == 'boater':
        sc = p.get('hat_c', (226, 204, 150))
        d.ellipse(B(cx - fw * 1.55, top - 3, cx + fw * 1.55, top + 6), fill=sh(sc, 0.9))
        d.rectangle(B(cx - fw * 0.95, top - 13, cx + fw * 0.95, top + 2), fill=sc)
        d.ellipse(B(cx - fw * 0.95, top - 16, cx + fw * 0.95, top - 10), fill=sh(sc, 1.08))
        d.rectangle(B(cx - fw * 0.95, top - 5, cx + fw * 0.95, top), fill=p.get('band', (120, 40, 40)))
        for k in range(8): d.line([P(cx - fw * 0.9 + k * fw * 0.25, top - 12), P(cx - fw * 0.9 + k * fw * 0.25, top - 6)], fill=sh(sc, 0.88), width=max(1, U // 2))
    elif hat == 'bowler':
        d.ellipse(B(cx - fw * 1.35, top - 1, cx + fw * 1.35, top + 7), fill=sh(hc, 0.85))
        d.chord(B(cx - fw * 0.98, top - 22, cx + fw * 0.98, top + 12), 180, 360, fill=hc)
        d.rectangle(B(cx - fw * 0.98, top - 2, cx + fw * 0.98, top + 2), fill=sh(hc, 0.6))
        curve(d, (cx - fw * 0.6, top - 12), (cx - fw * 0.2, top - 17), (cx + fw * 0.2, top - 16), sh(hc, 2.2), 1.2)
    elif hat == 'tophat':
        d.ellipse(B(cx - fw * 1.4, top - 1, cx + fw * 1.4, top + 7), fill=sh(hc, 0.85))
        d.polygon(poly([(cx - fw * 0.92, top + 2), (cx - fw * 0.98, top - 30), (cx + fw * 0.98, top - 30), (cx + fw * 0.92, top + 2)]), fill=hc)
        d.ellipse(B(cx - fw * 0.98, top - 33, cx + fw * 0.98, top - 27), fill=sh(hc, 1.15))
        d.rectangle(B(cx - fw * 0.93, top - 5, cx + fw * 0.93, top), fill=sh(hc, 0.55))
        d.line([P(cx - fw * 0.6, top - 28), P(cx - fw * 0.55, top - 7)], fill=sh(hc, 2.4), width=int(1.4 * U * Z))
    elif hat in ('pickel', 'stahl', 'brodie'):
        if hat == 'pickel':
            pc = p.get('hat_c', (30, 28, 30)); cover = p.get('cover')
            base = cover or pc
            d.chord(B(cx - fw * 1.05, top - 20, cx + fw * 1.05, top + 14), 180, 360, fill=base)
            d.polygon(poly([(cx - fw * 1.2, top + 2), (cx + fw * 1.2, top + 2), (cx + fw * 0.9, top + 7), (cx - fw * 0.9, top + 7)]), fill=sh(base, 0.7))
            sp_c = p.get('spike', (214, 190, 110)) if not cover else sh(base, 0.9)
            d.rectangle(B(cx - 3, top - 22, cx + 3, top - 17), fill=sp_c)
            d.polygon(poly([(cx - 3, top - 22), (cx + 3, top - 22), (cx, top - 36)]), fill=sp_c)
            if not cover:
                d.polygon(poly([(cx - 8, top - 10), (cx + 8, top - 10), (cx + 5, top + 1), (cx, top + 4), (cx - 5, top + 1)]), fill=p.get('plate', (224, 194, 104)))
                d.polygon(poly([(cx - 4, top - 7), (cx + 4, top - 7), (cx, top - 1)]), fill=sh(p.get('plate', (224, 194, 104)), 0.75))
            else:
                d.rectangle(B(cx - 3, top - 6, cx + 3, top - 1), fill=(180, 40, 40))
            curve(d, (cx - fw * 0.7, top - 6), (cx - fw * 0.4, top - 15), (cx, top - 17), sh(base, 1.8), 1.2)
        elif hat == 'stahl':
            sc = p.get('hat_c', (100, 104, 92))
            d.chord(B(cx - fw * 1.12, top - 18, cx + fw * 1.12, top + 26), 180, 360, fill=sc)
            d.polygon(poly([(cx - fw * 1.12, top + 4), (cx + fw * 1.12, top + 4), (cx + fw * 1.3, top + 18), (cx + fw * 1.05, top + 18), (cx - fw * 1.05, top + 18), (cx - fw * 1.3, top + 18)]), fill=sc)
            d.line([P(cx - fw * 1.1, top + 4), P(cx + fw * 1.1, top + 4)], fill=sh(sc, 0.7), width=int(1.4 * U * Z))
            for sd in (-1, 1): d.ellipse(B(cx + sd * fw * 0.9 - 2, top - 2, cx + sd * fw * 0.9 + 2, top + 2), fill=sh(sc, 0.6))
            curve(d, (cx - fw * 0.8, top - 4), (cx - fw * 0.3, top - 16), (cx + fw * 0.2, top - 17), sh(sc, 1.4), 1.2)
        else:
            bc = p.get('hat_c', (112, 106, 78))
            d.ellipse(B(cx - fw * 1.6, top - 4, cx + fw * 1.6, top + 8), fill=sh(bc, 0.88))
            d.chord(B(cx - fw * 0.95, top - 18, cx + fw * 0.95, top + 10), 180, 360, fill=bc)
            d.ellipse(B(cx - fw * 1.6, top - 4, cx + fw * 1.6, top + 8), outline=sh(bc, 0.65), width=int(1.2 * U * Z))
            curve(d, (cx - fw * 0.6, top - 6), (cx - fw * 0.2, top - 13), (cx + fw * 0.3, top - 12), sh(bc, 1.35), 1.0)
    elif hat in ('svcap', 'peaked'):
        sc = p.get('hat_c', (140, 126, 84))
        d.ellipse(B(cx - fw * 1.2, top - 15, cx + fw * 1.2, top + 1), fill=sc)
        d.rectangle(B(cx - fw * 0.98, top - 6, cx + fw * 0.98, top + 2), fill=p.get('band', sh(sc, 0.82)))
        d.polygon(poly([(cx - fw * 0.95, top + 2), (cx + fw * 0.95, top + 2), (cx + fw * 0.75, top + 9), (cx - fw * 0.75, top + 9)]), fill=p.get('visor', (50, 40, 30)))
        d.ellipse(B(cx - 3, top - 8, cx + 3, top - 2), fill=p.get('badge', (210, 186, 110)))
    elif hat == 'turban':
        tc = p.get('hat_c', (236, 232, 220))
        d.ellipse(B(cx - fw * 1.15, top - 20, cx + fw * 1.15, top + 10), fill=tc)
        for k in range(5):
            y0 = top - 14 + k * 5
            curve(d, (cx - fw * 1.1, y0 + 6), (cx - fw * 0.1, y0 - 4), (cx + fw * 1.05, y0 + 2 - k), sh(tc, 0.82), 0.9)
        if p.get('kulla'):
            d.polygon(poly([(cx - 6, top - 16), (cx + 6, top - 16), (cx, top - 30)]), fill=p['kulla'])
        if p.get('fan'):
            d.polygon(poly([(cx + 6, top - 16), (cx + 18, top - 30), (cx + 22, top - 22)]), fill=tc)
        if p.get('turban_badge'): d.ellipse(B(cx - 3, top - 9, cx + 3, top - 3), fill=p['turban_badge'])
    elif hat == 'fez':
        fc = p.get('hat_c', (180, 30, 36))
        d.polygon(poly([(cx - fw * 0.85, top + 4), (cx - fw * 0.72, top - 20), (cx + fw * 0.72, top - 20), (cx + fw * 0.85, top + 4)]), fill=fc)
        d.ellipse(B(cx - fw * 0.72, top - 23, cx + fw * 0.72, top - 17), fill=sh(fc, 1.15))
        d.line([P(cx, top - 20), P(cx + fw * 0.9, top - 4)], fill=(24, 22, 24), width=int(1.4 * U * Z))
        d.line([P(cx - fw * 0.5, top - 15), P(cx - fw * 0.55, top)], fill=sh(fc, 1.3), width=U)
    elif hat == 'feltbrim':
        fc = p.get('hat_c', (46, 40, 36))
        d.ellipse(B(cx - fw * 1.75, top - 4, cx + fw * 1.75, top + 8), fill=sh(fc, 0.85))
        d.polygon(poly([(cx - fw * 0.95, top + 2), (cx - fw * 0.85, top - 20), (cx, top - 16), (cx + fw * 0.85, top - 20), (cx + fw * 0.95, top + 2)]), fill=fc)
        d.rectangle(B(cx - fw * 0.95, top - 4, cx + fw * 0.95, top + 1), fill=sh(fc, 0.55))
    elif hat == 'topee':
        tc = p.get('hat_c', (240, 236, 222))
        d.ellipse(B(cx - fw * 1.5, top - 2, cx + fw * 1.5, top + 10), fill=sh(tc, 0.9))
        d.chord(B(cx - fw * 1.05, top - 22, cx + fw * 1.05, top + 14), 180, 360, fill=tc)
        d.rectangle(B(cx - fw * 1.05, top - 4, cx + fw * 1.05, top + 1), fill=p.get('band', sh(tc, 0.8)))
        d.ellipse(B(cx - 2.5, top - 24, cx + 2.5, top - 19), fill=sh(tc, 0.8))
    elif hat == 'cocked':
        d.polygon(poly([(cx - fw * 1.6, top + 2), (cx - fw * 1.1, top - 10), (cx + fw * 1.1, top - 10), (cx + fw * 1.6, top + 2), (cx, top + 4)]), fill=(28, 28, 32))
        d.line([P(cx - fw * 1.5, top + 1), P(cx + fw * 1.5, top + 1)], fill=(220, 190, 100), width=int(1.4 * U * Z))
        for k in range(22):
            a = math.pi * (1.0 + k / 21)
            r = 26 + (k % 3) * 3
            curve(d, (cx, top - 8), (cx + math.cos(a) * r * 0.5, top - 8 + math.sin(a) * r * 0.9 - 6), (cx + math.cos(a) * r, top - 6 + math.sin(a) * r * 0.65),
                  (60, 150, 70) if k % 2 else (110, 196, 104), 1.6)
    elif hat == 'mobcap':
        mc = p.get('hat_c', (240, 236, 226))
        d.ellipse(B(cx - fw * 1.25, top - 18, cx + fw * 1.25, top + 10), fill=mc)
        curve(d, (cx - fw * 1.2, top + 4), (cx, top + 9), (cx + fw * 1.2, top + 4), sh(mc, 0.8), 1.0)
        for k in range(6): d.line([P(cx - fw * 0.8 + k * fw * 0.32, top - 12), P(cx - fw * 0.85 + k * fw * 0.34, top + 3)], fill=sh(mc, 0.9), width=U)
    elif hat == 'nursecap':
        d.polygon(poly(bez((cx - fw * 1.15, top + 8), (cx, top - 22), (cx + fw * 1.15, top + 8), 14) + bez((cx + fw * 1.15, top + 8), (cx, top - 2), (cx - fw * 1.15, top + 8), 10)[1:]), fill=(250, 250, 250))
        d.rectangle(B(cx - 2, top - 8, cx + 2, top + 2), fill=(210, 30, 30)); d.rectangle(B(cx - 5, top - 5, cx + 5, top - 1), fill=(210, 30, 30))
    elif hat == 'flatcap':
        fc = p.get('hat_c', (90, 84, 76))
        d.ellipse(B(cx - fw * 1.2, top - 15, cx + fw * 1.3, top + 3), fill=fc)
        d.polygon(poly([(cx - fw * 0.9, top - 1), (cx + fw * 0.95, top - 1), (cx + fw * 0.7, top + 7), (cx - fw * 0.7, top + 7)]), fill=sh(fc, 0.75))
        for k in range(6): d.line([P(cx - fw + k * fw * 0.4, top - 12), P(cx - fw * 0.9 + k * fw * 0.4, top)], fill=sh(fc, 0.88), width=max(1, U // 2))
    elif hat == 'eth_crown':      # 흰 머릿수건 + 작은 금관 (타이투 황후)
        d.polygon(poly(bez((cx - fw * 1.2, top + 12), (cx, top - 22), (cx + fw * 1.2, top + 12), 14) + bez((cx + fw * 1.2, top + 12), (cx, top - 4), (cx - fw * 1.2, top + 12), 10)[1:]), fill=(248, 246, 238))
        d.polygon(poly([(cx - fw * 0.8, top - 6), (cx - fw * 0.8, top - 20), (cx - fw * 0.4, top - 12), (cx, top - 24), (cx + fw * 0.4, top - 12), (cx + fw * 0.8, top - 20), (cx + fw * 0.8, top - 6)]), fill=(226, 184, 70))
        for x in (cx - fw * 0.4, cx, cx + fw * 0.4): d.ellipse(B(x - 2, top - 11, x + 2, top - 7), fill=(190, 40, 50))
    elif hat == 'qingcap':
        d.polygon(poly([(cx - fw * 1.3, top + 4), (cx, top - 18), (cx + fw * 1.3, top + 4)]), fill=(232, 222, 192))
        d.polygon(poly([(cx - fw * 1.0, top + 0), (cx, top - 16), (cx + fw * 1.0, top + 0)]), fill=(186, 40, 40))
        d.ellipse(B(cx - 4, top - 24, cx + 4, top - 16), fill=p.get('knob', (60, 90, 170)))
    elif hat == 'headscarf':
        sc = p.get('hat_c', (236, 230, 214))
        d.polygon(poly(bez((cx - fw * 1.2, top + 14), (cx, top - 22), (cx + fw * 1.2, top + 14), 14) + bez((cx + fw * 1.2, top + 14), (cx, top - 4), (cx - fw * 1.2, top + 14), 10)[1:]), fill=sc)
        curve(d, (cx - fw * 1.0, top - 2), (cx, top - 8), (cx + fw * 1.0, top - 2), sh(sc, 0.85), 0.8)

def face_hair_pre(d, p, cx, ny, ey, fw):
    chin = p.get('chin', 88)
    if p.get('whiskers'):
        wc = p['whiskers']
        for sd in (-1, 1):
            d.polygon(poly([(cx + sd * fw * 0.98, ey - 4), (cx + sd * fw * 0.98, ey + 18), (cx + sd * fw * 0.72, ey + 24), (cx + sd * fw * 0.6, ey + 14), (cx + sd * fw * 0.84, ey - 4)]), fill=wc)
    if p.get('beard'):
        bc = p['beard']; L = p.get('beard_long', 0)
        pts = [(cx - fw * 0.98, ey - 2)] + bez((cx - fw * 0.98, ey + 6), (cx - fw * 0.8, chin + 4 + L), (cx, chin + 6 + L), 10) + bez((cx, chin + 6 + L), (cx + fw * 0.8, chin + 4 + L), (cx + fw * 0.98, ey + 6), 10)[1:] + [(cx + fw * 0.98, ey - 2), (cx + fw * 0.8, ey + 8)]
        pts += bez((cx + fw * 0.8, ey + 8), (cx, ny + 8), (cx - fw * 0.8, ey + 8), 10)[1:]
        d.polygon(poly(pts), fill=bc)
        for k in range(10):
            x = cx - fw * 0.7 + k * fw * 0.15
            curve(d, (x, ny + 8), (x + 0.5, chin), (x * 0.9 + cx * 0.1, chin + 4 + L), sh(bc, 1.3 if sum(bc) < 300 else 0.85), 0.5)
    if p.get('goatee'):
        gc = p['goatee']
        d.polygon(poly([(cx - 5, ny + 11), (cx + 5, ny + 11), (cx + 3, chin + 6), (cx, chin + 9), (cx - 3, chin + 6)]), fill=gc)

def face_hair_post(d, p, cx, ny, ey, fw):
    my = ny + 2.2
    if p.get('kaiser'):      # 끝을 위로 꼬아 올린 콧수염 (빌헬름 2세 · 프란츠 페르디난트)
        k = p['kaiser']; w = p.get('kaiser_w', 1.0)
        for sd in (-1, 1):
            pts = [(cx, my), (cx + sd * 6 * w, my + 1.2), (cx + sd * 11 * w, my - 1.5), (cx + sd * 14 * w, my - 6), (cx + sd * 12.5 * w, my - 3.5), (cx + sd * 9 * w, my + 3.2), (cx + sd * 3, my + 3.2), (cx, my + 2.2)]
            d.polygon(poly(pts), fill=k)
    if p.get('walrus'):      # 입을 덮는 덥수룩한 콧수염 (비스마르크 · 클레망소)
        wc = p['walrus']; w = p.get('walrus_w', 10)
        pts = [(cx - w, my + 9), (cx - w * 0.9, my + 1), (cx - 2, my - 1), (cx, my), (cx + 2, my - 1), (cx + w * 0.9, my + 1), (cx + w, my + 9), (cx + w * 0.6, my + 6.5), (cx, my + 5.5), (cx - w * 0.6, my + 6.5)]
        d.polygon(poly(pts), fill=wc)
        for k in range(7): curve(d, (cx - w * 0.75 + k * w * 0.25, my + 1), (cx - w * 0.8 + k * w * 0.26, my + 4), (cx - w * 0.85 + k * w * 0.28, my + 7), sh(wc, 0.82), 0.5)
    if p.get('mustache2'):   # 짧고 단정한 콧수염 (레닌·로이드 조지)
        mc = p['mustache2']
        d.polygon(poly([(cx - 8, my + 3.4), (cx - 6, my + 0.4), (cx, my), (cx + 6, my + 0.4), (cx + 8, my + 3.4), (cx, my + 2.6)]), fill=mc)

EU = (246, 212, 186); EU2 = (238, 198, 170); MED = (226, 184, 150); SA = (184, 130, 94); SA2 = (160, 110, 78); EA = (238, 204, 170)
AF = (124, 84, 60); AF2 = (98, 64, 46); ETH = (146, 98, 70)
KH = (140, 126, 84)
KH = (140, 126, 84); OLIVE = (98, 100, 70); OLD = (232, 198, 168)
# 사람마다 '보통' 얼굴을 살짝 다르게
BASE_EXPR = {'pericles': 'resolve'}
class _BE(dict):
    def get(self, k, d=None): return dict.get(self, k, d)
BASE_EXPR = _BE(BASE_EXPR)
ALL_E = ['n', 'smile', 'sad', 'worry', 'resolve', 'surprise', 'angry', 'think']
ANNA = dict(skin=EU, fw=22, top=31, cheek_y=66, jaw=0.72, chin=86, chin_w=5.8, eye_y=62, eye_w=6.6, eye_h=3.8, iris=3.2, iris_c=(90, 120, 150),
            hair_c=(196, 150, 80), hairline=40, lip=(196, 100, 96), brow_t=1.4, mouth_w=5.2, brow_c=(160, 116, 60))
LOTTE = dict(skin=EU, fw=21.5, top=31, cheek_y=66, jaw=0.7, chin=86, chin_w=5.6, eye_y=62, eye_w=6.6, eye_h=3.8, iris=3.2, iris_c=(80, 110, 90),
             hair_c=(226, 190, 116), hairline=40, lip=(200, 104, 100), brow_t=1.3, mouth_w=5.0, brow_c=(190, 150, 90))
KID = dict(fw=21, top=33, cheek_y=67, jaw=0.68, chin=84, chin_w=5, eye_y=63, eye_w=7.2, eye_h=4.4, iris=3.5, young=True, blush=True, hairline=42, brow_t=1.1, mouth_w=4.4)
def _w(base, **kw):
    d = dict(base); d.update(kw); return d
def M(skin=EU, **kw):     # 보통 어른 남자 얼굴
    d = dict(skin=skin, fw=23, top=31, cheek_y=66, jaw=0.8, chin=87, chin_w=7, eye_y=62, eye_w=5.8, eye_h=3.0, iris=2.9, iris_c=(80, 90, 110), hairline=39, brow_t=1.7, mouth_w=6)
    d.update(kw); return d
def W(skin=EU, **kw):     # 보통 어른 여자 얼굴
    d = dict(skin=skin, fw=22, top=31, cheek_y=66, jaw=0.74, chin=86, chin_w=6, eye_y=62, eye_w=6.2, eye_h=3.4, iris=3.0, iris_c=(80, 90, 110), hairline=40, brow_t=1.4, mouth_w=5.4, lip=(190, 100, 96))
    d.update(kw); return d
GR_H = (52, 38, 28); GR_H2 = (80, 58, 40); GREYH = (168, 164, 158); WHITEH = (222, 220, 214)
def CHT(shirt, drape=None, border=(170, 60, 40)):
    """키톤 + 히마티온 (어깨에 비스듬히 두른 겉옷, 테두리 무늬)"""
    return dict(clothes='shamma', shirt=shirt, cloth=drape or shirt, border=border)

# ==================================================================== 조선 (1863~1882): 갓 · 사모 · 익선관 · 전립 · 와룡관 · 탕건 · 단령 · 군복
KR_P_HATS = {'gat', 'samo', 'ikseon', 'jeolip', 'waryong', 'tanggeon', 'paeraengi', 'headband', 'bachi', 'skullcap', 'jobawi', 'mangeon'}
_orig_draw_hat = draw_hat
def draw_hat(d, p):
    if p.get('hat') in KR_P_HATS: return draw_kr_hat(d, p)
    return _orig_draw_hat(d, p)
def draw_kr_hat(d, p):
    hat = p['hat']; cx, top, fw = 60, p.get('top', 30), p.get('fw', 24)
    hc = p.get('hat_c', (34, 30, 30)); hl = sh(hc, 1.9) if sum(hc) < 200 else sh(hc, 1.12); hs = sh(hc, 0.7)
    W_ = int(1.2 * U * Z)
    def mangeon():
        d.polygon(poly(bez((cx - fw * 1.0, top + 12), (cx, top + 6), (cx + fw * 1.0, top + 12), 12) + bez((cx + fw * 1.0, top + 16), (cx, top + 10), (cx - fw * 1.0, top + 16), 12)), fill=(28, 26, 26))
        for k in range(9): d.line([P(cx - fw * 0.85 + k * fw * 0.21, top + 9), P(cx - fw * 0.85 + k * fw * 0.21, top + 14)], fill=(70, 66, 64), width=U // 2 + 1)
    if hat == 'mangeon':
        mangeon(); d.ellipse(B(cx - 6, top - 12, cx + 6, top), fill=p.get('hair_c', (30, 26, 26))); return
    if hat in ('gat', 'paeraengi'):
        gc = hc if hat == 'gat' else p.get('hat_c', (206, 182, 126))
        if hat == 'gat': mangeon()
        kk = p.get('gatkkeun', (50, 40, 34))
        if hat == 'gat':
            # 갓끈: 얼굴 안쪽(눈 · 볼)을 가로지르지 않도록 얼굴 테두리 바깥선을 따라 턱 아래에서 모인다
            cy_ = p.get('cheek_y', 66); jw_ = p.get('jaw', 0.8); chn = p.get('chin', 88); cw_ = p.get('chin_w', 7)
            for sd in (-1, 1):
                d.line([P(cx + sd * (fw * 1.0 + 1.2), top + 12), P(cx + sd * (fw * 1.03 + 1.2), cy_ + 2), P(cx + sd * (fw * jw_ + 1.6), cy_ + 13),
                        P(cx + sd * (cw_ + 4), chn + 1.5), P(cx + sd * 3, chn + 4)], fill=kk, width=int(0.9 * U * Z))
            d.line([P(cx - 2, p.get('chin', 88) + 4), P(cx - 4, 112)], fill=kk, width=int(1.0 * U * Z)); d.line([P(cx + 2, p.get('chin', 88) + 4), P(cx + 4, 112)], fill=kk, width=int(1.0 * U * Z))
        ch = 17 if hat == 'gat' else 12
        d.ellipse(B(cx - fw * 2.0, top + 3, cx + fw * 2.0, top + 13), fill=gc)
        d.ellipse(B(cx - fw * 1.85, top + 4.5, cx + fw * 1.85, top + 11.5), outline=hl, width=W_ // 2 + 1)
        d.rounded_rectangle(B(cx - fw * 0.66, top - ch + 2, cx + fw * 0.66, top + 8), radius=int(4 * U), fill=gc)
        d.line([P(cx - fw * 0.5, top - ch + 6), P(cx - fw * 0.5, top + 4)], fill=hl, width=W_)
        d.rectangle(B(cx - fw * 0.66, top + 3, cx + fw * 0.66, top + 7), fill=sh(gc, 0.6) if hat == 'gat' else (40, 34, 30))
        return
    if hat in ('samo', 'ikseon'):
        if hat == 'ikseon':
            for sd in (-1, 1):
                d.ellipse(B(cx + sd * fw * 0.62 - 6.5, top - 23, cx + sd * fw * 0.62 + 6.5, top - 2), fill=hc)
                d.ellipse(B(cx + sd * fw * 0.62 - 4.5, top - 20, cx + sd * fw * 0.62 + 4.5, top - 5), outline=hl, width=W_ // 2 + 1)
        d.chord(B(cx - fw * 0.66, top - 15, cx + fw * 0.66, top + 8), 180, 360, fill=hc)
        d.polygon(poly(bez((cx - fw * 1.04, top + 14), (cx - fw * 1.1, top - 8), (cx, top - 8), 10) + bez((cx, top - 8), (cx + fw * 1.1, top - 8), (cx + fw * 1.04, top + 14), 10)[1:]), fill=hc)
        d.line([P(cx - fw * 0.9, top - 2), P(cx + fw * 0.9, top - 2)], fill=hl if hat == 'samo' else (210, 176, 90), width=W_)
        if hat == 'samo':
            for sd in (-1, 1):
                d.ellipse(B(cx + sd * fw * 1.0 - (fw * 1.0 if sd < 0 else 0), top - 6, cx + sd * fw * 1.0 + (fw * 1.0 if sd > 0 else 0), top + 3), fill=hc)
                d.ellipse(B(cx + sd * fw * 1.15 - (fw * 0.75 if sd < 0 else 0), top - 4, cx + sd * fw * 1.15 + (fw * 0.75 if sd > 0 else 0), top + 1), outline=hl, width=W_ // 2 + 1)
        return
    if hat == 'jeolip':
        d.ellipse(B(cx - fw * 1.5, top + 3, cx + fw * 1.5, top + 13), fill=sh(hc, 0.92))
        d.chord(B(cx - fw * 1.0, top - 12, cx + fw * 1.0, top + 22), 180, 360, fill=hc)
        d.line([P(cx - fw * 0.95, top + 2), P(cx + fw * 0.95, top + 2)], fill=p.get('band', (150, 40, 40)), width=int(1.6 * U * Z))
        tc = p.get('tassel', (200, 40, 40))
        for k in (-6, -3, 0, 3, 6): curve(d, (cx, top - 12), (cx + k * 0.6, top - 9), (cx + k, top - 4), tc, 1.2)
        d.ellipse(B(cx - 3.4, top - 16, cx + 3.4, top - 10), fill=tc)
        if p.get('feather'):
            curve(d, (cx + 6, top - 10), (cx + 16, top - 16), (cx + 28, top - 18), p['feather'], 1.6)
            d.ellipse(B(cx + 24, top - 22, cx + 32, top - 14), fill=(50, 120, 150)); d.ellipse(B(cx + 26.5, top - 19.5, cx + 29.5, top - 16.5), fill=(230, 200, 90))
        return
    if hat == 'waryong':
        pts = [(cx - fw * 1.0, top + 12), (cx - fw * 0.92, top - 6), (cx - fw * 0.42, top - 15), (cx + fw * 0.42, top - 15), (cx + fw * 0.92, top - 6), (cx + fw * 1.0, top + 12)]
        d.polygon(poly(pts), fill=hc)
        for y in (top - 9, top - 1, top + 6): d.line([P(cx - fw * 0.85, y), P(cx + fw * 0.85, y)], fill=hl, width=W_ // 2 + 1)
        d.line([P(cx, top - 15), P(cx, top + 10)], fill=hl, width=W_ // 2 + 1)
        return
    if hat == 'tanggeon':
        mangeon()
        d.polygon(poly([(cx - fw * 1.0, top + 10), (cx - fw * 0.98, top - 4), (cx - fw * 0.45, top - 4), (cx - fw * 0.45, top - 11), (cx + fw * 0.45, top - 11), (cx + fw * 0.45, top - 4), (cx + fw * 0.98, top - 4), (cx + fw * 1.0, top + 10)]), fill=hc)
        d.line([P(cx - fw * 0.9, top + 2), P(cx + fw * 0.9, top + 2)], fill=hl, width=W_ // 2 + 1)
        return
    if hat == 'headband':
        bc = p.get('hat_c', (242, 240, 232))
        d.polygon(poly(bez((cx - fw * 1.05, top + 11), (cx, top + 3), (cx + fw * 1.05, top + 11), 12) + bez((cx + fw * 1.05, top + 17), (cx, top + 9), (cx - fw * 1.05, top + 17), 12)), fill=bc)
        d.polygon(poly([(cx + fw * 0.95, top + 10), (cx + fw * 1.35, top + 6), (cx + fw * 1.3, top + 14)]), fill=sh(bc, 0.9))
        return
    if hat == 'bachi':
        bc = p.get('hat_c', (30, 40, 70))
        d.ellipse(B(cx - fw * 1.2, top - 6, cx + fw * 1.2, top + 8), fill=bc); d.rectangle(B(cx - fw * 1.0, top + 3, cx + fw * 1.0, top + 9), fill=sh(bc, 0.7))
        d.ellipse(B(cx - 4, top - 12, cx + 4, top - 4), fill=(210, 40, 40)); return
    if hat == 'skullcap':
        d.chord(B(cx - fw * 1.0, top - 8, cx + fw * 1.0, top + 26), 180, 360, fill=hc); d.ellipse(B(cx - 2.5, top - 11, cx + 2.5, top - 6), fill=(200, 40, 40)); return
    if hat == 'jobawi':
        jc = p.get('hat_c', (90, 50, 90))
        d.polygon(poly(bez((cx - fw * 1.1, top + 26), (cx - fw * 1.2, top - 8), (cx, top - 6), 10) + bez((cx, top - 6), (cx + fw * 1.2, top - 8), (cx + fw * 1.1, top + 26), 10)[1:] + [(cx + fw * 0.85, top + 26)] + bez((cx + fw * 0.85, top + 20), (cx, top + 2), (cx - fw * 0.85, top + 20), 10) + [(cx - fw * 0.85, top + 26)]), fill=jc)
        d.ellipse(B(cx - 3, top + 1, cx + 3, top + 7), fill=(200, 60, 60)); return

KR_P_CLOTHES = {'danryeong', 'gunbok', 'po_kr'}
_orig_draw_clothes = draw_clothes
def draw_clothes(d, p):
    kind = p.get('clothes')
    if kind not in KR_P_CLOTHES: return _orig_draw_clothes(d, p)
    c = p.get('cloth', (60, 80, 110)); cs = sh(c, 0.8)
    _neck(d, p); sh_y, body = _body(p)
    if kind == 'gunbok':                # 동달이(붉은 소매) + 전복(조끼)
        d.polygon(poly(body), fill=p.get('sleeve', (190, 50, 50)))
        v = p.get('vest', (40, 44, 60))
        d.polygon(poly([(24, PH), (26, sh_y + 4), (44, sh_y - 4), (60, sh_y - 2), (76, sh_y - 4), (94, sh_y + 4), (96, PH)]), fill=v)
        d.polygon(poly([(44, sh_y - 5), (52, sh_y - 6), (66, PH), (56, PH)]), fill=c)
        d.line([P(45, sh_y - 5), P(62, PH)], fill=(250, 250, 244), width=int(2.2 * U * Z))
        d.rectangle(B(26, 122, 94, 127), fill=p.get('jeondae', (200, 60, 50)))
        return
    d.polygon(poly(body), fill=c)
    d.polygon(poly([(4, PH), (6, sh_y + 12), (20, sh_y + 2), (30, sh_y + 6), (24, PH)]), fill=cs)
    d.polygon(poly([(116, PH), (114, sh_y + 12), (100, sh_y + 2), (92, sh_y + 8), (98, PH)]), fill=cs)
    if kind == 'danryeong':             # 둥근 깃 + 흉배
        d.chord(B(42, sh_y - 14, 78, sh_y + 10), 0, 180, fill=sh(c, 0.6))
        d.chord(B(46, sh_y - 12, 74, sh_y + 6), 0, 180, fill=(250, 250, 244))
        d.chord(B(48, sh_y - 12, 72, sh_y + 4), 0, 180, fill=sh(p['skin'], 0.86))
        hb = p.get('hyungbae')
        if hb:
            d.rectangle(B(48, sh_y + 12, 72, PH), fill=hb); d.rectangle(B(50, sh_y + 14, 70, PH), outline=sh(hb, 0.7), width=U)
            d.ellipse(B(54, sh_y + 17, 66, sh_y + 27), outline=(240, 220, 150), width=U)
        if p.get('dragon'):
            gd = (232, 196, 90)
            d.ellipse(B(46, sh_y + 10, 74, PH + 8), fill=gd); d.ellipse(B(50, sh_y + 14, 70, PH + 4), outline=(190, 60, 40), width=U)
            for sd in (-1, 1): d.ellipse(B(60 + sd * 40 - 9, sh_y - 2, 60 + sd * 40 + 9, sh_y + 14), fill=gd)
        return
    # po_kr: 단순한 포 (일본 · 청 사람 옷 등) — 깃만
    d.polygon(poly([(44, sh_y - 5), (52, sh_y - 6), (76, PH), (64, PH)]), fill=sh(c, 0.85))
    d.line([P(45, sh_y - 5), P(70, PH)], fill=p.get('collar', sh(c, 0.6)), width=int(3 * U * Z))
    if p.get('obi'): d.rectangle(B(10, 124, 110, PH), fill=p['obi'])

def KRM(skin=(236, 202, 168), **kw):
    base = dict(iris_c=(54, 40, 32), hair_c=(28, 24, 24), brow_c=(30, 26, 24), eye_h=2.7, eye_w=5.6); base.update(kw)
    return M(skin, **base)
def KRW(skin=(240, 208, 176), **kw):
    base = dict(iris_c=(54, 40, 32), hair_c=(28, 24, 24), brow_c=(40, 32, 28), eye_h=3.0); base.update(kw)
    return W(skin, **base)
def KRK(skin=(240, 206, 172), **kw):
    d = _w(KID, skin=skin, iris_c=(54, 40, 32), hair_c=(28, 24, 24), brow_c=(40, 32, 28), lip=(200, 110, 100)); d.update(kw); return d
HK = (28, 24, 24); GRK = (150, 146, 140); WHK = (226, 224, 218)
WHITE_P = (244, 242, 234)
PEOPLE = {
    # 주인공 집안 (만든 인물)
    'yunjae10': KRK(hair='braid', clothes='jeogori', cloth=(236, 230, 214)),
    'yunjae15': KRK(hair='braid', clothes='jeogori', cloth=(214, 224, 236), fw=21.5, chin=85),
    'yunjae20': KRM(young=True, hair='slick', hat='gat', clothes='durumagi', cloth=(222, 232, 240)),
    'yunjae26': KRM(hair='slick', hat='gat', clothes='durumagi', cloth=(206, 222, 236)),
    'father': KRM(hair='slick', hat='gat', clothes='durumagi', cloth=(236, 234, 226), beard=(40, 34, 30), mustache=(40, 34, 30)),
    'mother': KRW(hair='center', clothes='jeogori', cloth=(236, 222, 200)),
    'yunhee12': KRK(hair='braid', clothes='chima', cloth=(240, 200, 120), goreum=(190, 40, 60)),
    'yunhee17': KRW(young=True, hair='braid', clothes='chima', cloth=(226, 196, 160), goreum=(190, 40, 60)),
    'yunhee23': KRW(hair='center', clothes='chima', cloth=(214, 200, 170), goreum=(120, 60, 90)),
    # 실존 인물 · 시대 인물
    'daewongun': KRM(fw=22.5, chin=88, hair='slick', hat='waryong', clothes='durumagi', cloth=WHITE_P, beard=(70, 60, 54), mustache=(70, 60, 54), beard_long=2, age_lines=2, narrow=0.4),
    'overseer': KRM(hair='slick', hat='samo', clothes='danryeong', cloth=(70, 110, 90), hyungbae=(200, 170, 100), mustache=HK),
    'corvee': KRM(skin=(214, 172, 136), hair='slick', hat='headband', clothes='jeogori', cloth=(214, 204, 180), stubble=(60, 50, 40), age_lines=1),
    'rich': KRM(fw=25, hair='slick', hat='gat', clothes='durumagi', cloth=(150, 130, 170), beard=HK, mustache=HK),
    'rice_seller': KRM(skin=(214, 172, 136), hair='slick', hat='paeraengi', clothes='jeogori', cloth=(220, 210, 190), age_lines=1),
    'commoner': KRM(skin=(214, 172, 136), hair='slick', hat='headband', clothes='jeogori', cloth=(226, 220, 200)),
    'scholar_y': KRM(hair='slick', hat='gat', clothes='durumagi', cloth=WHITE_P, beard=HK, mustache=HK, beard_long=1),
    'peddler': KRM(skin=(214, 172, 136), hair='slick', hat='paeraengi', clothes='jeogori', cloth=(200, 190, 160)),
    'market_w': KRW(skin=(230, 192, 160), hair='center', clothes='chima', cloth=(230, 220, 200), goreum=(110, 70, 60), age_lines=1),
    'yanghs': KRM(hair='slick', hat='jeolip', feather=(120, 90, 50), clothes='gunbok', cloth=(60, 80, 130), vest=(30, 34, 50), beard=HK, mustache=HK, brow_t=2.1),
    'soldier_k': KRM(skin=(214, 172, 136), hair='slick', hat='jeolip', clothes='gunbok', cloth=(70, 90, 140), vest=(40, 44, 60)),
    'tiger_hunter': KRM(skin=(206, 164, 128), hair='slick', hat='jeolip', hat_c=(60, 50, 44), clothes='jeogori', cloth=(180, 160, 120), stubble=(50, 44, 40), brow_t=2.0),
    'kyujanggak': KRM(hair='slick', hat='samo', clothes='danryeong', cloth=(60, 80, 110), hyungbae=(200, 170, 100), age_lines=1),
    'french_off': M(EU, hat='kepi', hat_c=(30, 40, 80), band=(200, 170, 80), hair='short', hair_c=(80, 60, 40), mustache=(80, 60, 40), clothes='tunic', cloth=(30, 40, 80)),
    'eojaeyeon': KRM(hair='slick', hat='jeolip', feather=(120, 90, 50), clothes='gunbok', cloth=(70, 70, 120), vest=(30, 30, 40), beard=HK, mustache=HK, beard_long=2, brow_t=2.2, age_lines=1),
    'us_marine': M(EU, hat='kepi', hat_c=(30, 40, 70), band=(30, 40, 70), hair='short', hair_c=(120, 90, 60), clothes='tunic', cloth=(30, 40, 70)),
    'park_gyusu': KRM(skin=(232, 198, 166), hair='slick', hat='samo', clothes='danryeong', cloth=(50, 70, 90), hyungbae=(200, 170, 100), beard=GRK, mustache=GRK, beard_long=3, age_lines=3),
    'sinheon': KRM(hair='slick', hat='samo', clothes='danryeong', cloth=(40, 60, 80), hyungbae=(200, 160, 80), beard=(60, 54, 50), mustache=(60, 54, 50), beard_long=3, age_lines=2),
    'kuroda': KRM(fw=24, hat='peaked', hat_c=(30, 34, 50), band=(200, 170, 80), hair='short', clothes='tunic', cloth=(30, 34, 50), mustache=HK, brow_t=2.0),
    'ogyeongseok': KRM(hair='slick', hat='gat', clothes='durumagi', cloth=(214, 226, 234), beard=HK, mustache=HK),
    'jp_merchant': KRM(hair='short', clothes='po_kr', cloth=(110, 100, 110), obi=(60, 50, 60)),
    'choi_ik': KRM(skin=(232, 198, 166), hair='slick', hat='gat', clothes='durumagi', cloth=WHITE_P, beard=WHK, mustache=WHK, beard_long=4, age_lines=2, brow_c=(150, 146, 140), brow_t=2.0),
    'horimoto': KRM(hat='kepi', hat_c=(30, 34, 60), band=(200, 50, 50), hair='short', mustache=HK, clothes='tunic', cloth=(30, 34, 60)),
    'byeolgigun': KRM(skin=(220, 180, 146), hair='slick', hat='jeolip', hat_c=(30, 30, 30), clothes='tunic', cloth=(46, 74, 60)),
    'old_soldier': KRM(skin=(206, 164, 128), hair='slick', hat='jeolip', clothes='gunbok', cloth=(90, 100, 120), sleeve=(160, 70, 60), vest=(60, 60, 64), stubble=(60, 50, 40), age_lines=2),
    'kimhongjip': KRM(hair='slick', hat='samo', clothes='danryeong', cloth=(60, 90, 110), hyungbae=(200, 170, 100), beard=HK, mustache=HK),
    'young_off': KRM(young=True, hair='slick', hat='samo', clothes='danryeong', cloth=(70, 120, 120), hyungbae=(200, 170, 100)),
    'imansun': KRM(hair='slick', hat='gat', clothes='durumagi', cloth=WHITE_P, beard=(50, 44, 40), mustache=(50, 44, 40), beard_long=2, brow_t=2.0),
    'kimyunsik': KRM(hair='slick', hat='samo', clothes='danryeong', cloth=(50, 70, 100), hyungbae=(200, 170, 100), beard=HK, mustache=HK, beard_long=1),
    'kimchunyoung': KRM(skin=(206, 164, 128), hair='slick', hat='jeolip', clothes='gunbok', cloth=(90, 100, 120), sleeve=(160, 70, 60), vest=(60, 60, 64), stubble=(60, 50, 40), brow_t=2.1),
    'poor_m': KRM(skin=(206, 164, 128), hair='slick', hat='headband', clothes='jeogori', cloth=(196, 186, 164), stubble=(60, 50, 40), age_lines=1),
    'clerk': KRM(hair='slick', hat='samo', clothes='danryeong', cloth=(90, 100, 80), mustache=HK),
    'qing_soldier': KRM(hair='queue', hat='turban', hat_c=(40, 40, 50), clothes='kurta', cloth=(60, 80, 140)),
    'parkyounghyo': KRM(young=True, hair='slick', hat='gat', clothes='durumagi', cloth=(214, 222, 236)),
    'kimokgyun': KRM(hair='slick', hat='gat', clothes='durumagi', cloth=(230, 226, 214), mustache=HK),
    'carpenter': KRM(skin=(214, 172, 136), hair='slick', hat='headband', clothes='jeogori', cloth=(190, 170, 140), mustache=HK, age_lines=1),
    'beacon_m': KRM(skin=(206, 164, 128), hair='slick', hat='jeolip', hat_c=(60, 50, 44), clothes='jeogori', cloth=(200, 190, 170), stubble=(60, 50, 40)),
    'confucian2': KRM(skin=(232, 198, 166), hair='slick', hat='gat', clothes='durumagi', cloth=WHITE_P, beard=GRK, mustache=GRK, beard_long=3, age_lines=3, brow_c=(150, 146, 140)),
    'qing_merchant': KRM(hair='queue', hat='skullcap', hat_c=(30, 30, 34), clothes='robe', cloth=(70, 90, 110), mustache=HK),
    'gojong': KRM(fw=23.5, hair='slick', hat='ikseon', clothes='danryeong', cloth=(190, 40, 40), dragon=True, beard=HK, mustache=HK),
}
E5 = ['n', 'smile', 'sad', 'worry', 'surprise']
SETS = {k: ALL_E for k in PEOPLE}

def build(out):
    os.makedirs(out, exist_ok=True)
    files = []
    for who, exprs in SETS.items():
        for e in exprs:
            ee = BASE_EXPR.get(who, e) if e == 'n' else e
            im = render(PEOPLE[who], ee)
            name = 'kp_%s_%s' % (who, e)
            im.save(os.path.join(out, name + '.png'))
            files.append(name)
    print('portraits', len(files))
    return files

if __name__ == '__main__':
    files = build(sys.argv[1])
    if len(sys.argv) > 2:
        whos = list(SETS)
        cols = 8
        prev = Image.new('RGBA', (240 * cols, 264 * len(whos)), (60, 56, 52, 255))
        for r, who in enumerate(whos):
            for c, e in enumerate(SETS[who][:cols]):
                im = Image.open(os.path.join(sys.argv[1], 'kp_%s_%s.png' % (who, e)))
                prev.alpha_composite(im, (c * 240, r * 264))
        prev = prev.resize((prev.width // 2, prev.height // 2), Image.NEAREST)
        prev.save(sys.argv[2])
