"""고화질(48px 원본) 캐릭터 시트 17종 ($이름.png, 3프레임 x 4방향)"""
import os, sys
from PIL import Image, ImageDraw
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from hd_art import sh, outline

SKIN, SKIN_D = (250, 214, 182), (226, 178, 146)
EYE = (40, 30, 40)

def draw(spec, d_, step):
    S = 48
    lay = Image.new('RGBA', (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    hair = spec.get('hair', (40, 32, 40)); hair_l = sh(hair, 1.9) if sum(hair) < 200 else sh(hair, 1.25); hair_d = sh(hair, 0.7)
    top = spec['top']; top_l = sh(top, 1.3); top_d = sh(top, 0.72)
    lower = spec.get('lower', 'pants'); bottom = spec.get('bottom', (90, 90, 100)); shoes = spec.get('shoes', (50, 40, 40))
    hs = spec.get('hairstyle', 'short'); hat = spec.get('hat')
    bob = 1 if step != 1 else 0
    cx = 24; hy = 3 + bob; by = 25 + bob
    lift = {0: (0, 2), 1: (0, 0), 2: (2, 0)}[step]

    # 뒷머리 (몸 뒤)
    if hs == 'long' and d_ != 3:
        if d_ == 0: d.rounded_rectangle([cx - 12, hy + 8, cx + 11, hy + 29], 5, fill=hair_d)
        elif d_ == 1: d.rounded_rectangle([cx - 2, hy + 8, cx + 12, hy + 30], 5, fill=hair_d)
        else: d.rounded_rectangle([cx - 13, hy + 8, cx + 1, hy + 30], 5, fill=hair_d)

    # 다리 / 아랫도리
    if lower == 'robe':
        d.polygon([(cx - 10, by + 9), (cx + 9, by + 9), (cx + 11, 44), (cx - 12, 44)], fill=top)
        d.line([(cx - 10, by + 10), (cx - 12, 44)], fill=top_l)
        d.line([(cx - 1, by + 12), (cx - 1, 44)], fill=top_d)
        for i, fx in enumerate((cx - 7, cx + 1)):
            d.rectangle([fx, 44 - lift[i], fx + 6, 46 - lift[i]], fill=shoes)
    else:
        legc = SKIN if lower == 'skirt' else bottom
        sock = spec.get('socks', (246, 246, 246))
        for i, lx in enumerate((cx - 6, cx + 1)):
            ly = 37 - lift[i]
            d.rectangle([lx, ly, lx + 4, 43 - lift[i]], fill=legc)
            if lower == 'skirt': d.rectangle([lx, ly + 3, lx + 4, 43 - lift[i]], fill=sock)
            else: d.line([(lx, ly), (lx, 43 - lift[i])], fill=sh(legc, 1.2))
            d.rectangle([lx - 1, 44 - lift[i], lx + 5, 46 - lift[i]], fill=shoes)

    # 몸통
    d.rounded_rectangle([cx - 9, by, cx + 8, by + 12], 3, fill=top)
    d.line([(cx - 9, by + 1), (cx - 9, by + 11)], fill=top_l)
    if lower == 'skirt':
        d.polygon([(cx - 10, by + 10), (cx + 9, by + 10), (cx + 11, by + 15), (cx - 12, by + 15)], fill=bottom)
        for px in range(cx - 9, cx + 9, 4): d.line([(px, by + 11), (px - 1, by + 15)], fill=sh(bottom, 0.7))
    elif lower == 'pants':
        d.rectangle([cx - 8, by + 11, cx + 7, by + 13], fill=sh(bottom, 0.9))

    acc = spec.get('accent'); style = spec.get('accent_style')
    if d_ == 0:
        if style in ('collar', 'ribbon'):
            d.polygon([(cx - 3, by), (cx + 2, by), (cx - 1, by + 5)], fill=(248, 248, 248))
            d.line([(cx - 4, by), (cx - 1, by + 6)], fill=top_d); d.line([(cx + 3, by), (cx, by + 6)], fill=top_d)
            if style == 'collar':
                d.polygon([(cx - 2, by + 2), (cx + 1, by + 2), (cx + 1, by + 9), (cx - 1, by + 11), (cx - 2, by + 9)], fill=acc)
                d.point((cx - 1, by + 3), fill=sh(acc, 1.4))
            else:
                d.polygon([(cx - 4, by + 2), (cx - 1, by + 3), (cx - 4, by + 5)], fill=acc); d.polygon([(cx + 3, by + 2), (cx, by + 3), (cx + 3, by + 5)], fill=acc)
                d.rectangle([cx - 2, by + 2, cx + 1, by + 4], fill=sh(acc, 0.8))
            d.point((cx - 1, by + 8), fill=(220, 200, 120)); d.point((cx - 1, by + 10), fill=(220, 200, 120))
        elif style == 'vneck':
            d.line([(cx - 6, by), (cx, by + 7)], fill=(244, 240, 228), width=2); d.line([(cx + 5, by), (cx, by + 7)], fill=top_d)
            d.line([(cx + 1, by + 6), (cx + 5, by + 11)], fill=acc, width=2); d.line([(cx + 1, by + 6), (cx + 3, by + 12)], fill=sh(acc, 0.85))
        elif style == 'emblem':
            d.rectangle([cx - 5, by + 2, cx + 4, by + 9], fill=acc); d.rectangle([cx - 3, by + 4, cx + 2, by + 7], fill=sh(acc, 1.2))
            d.point((cx - 1, by + 5), fill=sh(top, 0.6))
            d.rectangle([cx - 9, by + 10, cx + 8, by + 11], fill=(40, 34, 30))
        elif style == 'belt':
            d.rectangle([cx - 9, by + 8, cx + 8, by + 10], fill=acc)
    if style == 'belt' and d_ != 0:
        d.rectangle([cx - 9, by + 8, cx + 8, by + 10], fill=acc)
    if style == 'emblem' and d_ != 0:
        d.rectangle([cx - 9, by + 10, cx + 8, by + 11], fill=(40, 34, 30))

    # 팔
    sw = {0: (2, -2), 1: (0, 0), 2: (-2, 2)}[step]
    if d_ in (0, 3):
        for i, ax in enumerate((cx - 12, cx + 9)):
            ay = by + 1 + (sw[i] if d_ == 0 else -sw[i]) // 2
            wide = 4 if lower == 'robe' else 3
            d.rounded_rectangle([ax - (1 if i == 0 and wide == 4 else 0), ay, ax + wide - (1 if i == 0 and wide == 4 else 0), ay + 10], 1, fill=top_d)
            d.rectangle([ax, ay + 10, ax + 3, ay + 12], fill=SKIN if d_ == 0 else SKIN_D)
    else:
        ax = cx - 2 + (sw[0] if d_ == 1 else -sw[0])
        d.rounded_rectangle([ax, by + 1, ax + 4, by + 11], 1, fill=top_d)
        d.rectangle([ax, by + 11, ax + 4, by + 13], fill=SKIN)

    # 머리
    if hs == 'bald':
        d.ellipse([cx - 11, hy + 1, cx + 10, hy + 22], fill=SKIN)
        d.arc([cx - 8, hy + 3, cx + 4, hy + 12], 200, 300, fill=(255, 236, 214), width=2)
        d.ellipse([cx - 11, hy + 1, cx + 10, hy + 22], outline=None)
        if d_ == 3:
            d.ellipse([cx - 11, hy + 1, cx + 10, hy + 22], fill=SKIN_D); d.arc([cx - 8, hy + 3, cx + 4, hy + 12], 200, 300, fill=SKIN, width=2)
        elif d_ == 0:
            for ex in (cx - 6, cx + 3):
                d.rectangle([ex, hy + 12, ex + 2, hy + 15], fill=EYE); d.point((ex, hy + 12), fill=(255, 255, 255))
            d.line([(cx - 7, hy + 10), (cx - 4, hy + 10)], fill=(150, 110, 90)); d.line([(cx + 2, hy + 10), (cx + 5, hy + 10)], fill=(150, 110, 90))
            d.line([(cx - 2, hy + 19), (cx + 1, hy + 19)], fill=(200, 120, 100))
        else:
            ex = cx - 8 if d_ == 1 else cx + 5
            d.rectangle([ex, hy + 12, ex + 2, hy + 15], fill=EYE); d.point((ex if d_ == 1 else ex + 2, hy + 12), fill=(255, 255, 255))
            d.line([(ex - 1, hy + 10), (ex + 3, hy + 10)], fill=(150, 110, 90))
    elif d_ == 3:
        d.ellipse([cx - 12, hy, cx + 11, hy + 22], fill=hair)
        if hs == 'long': d.rounded_rectangle([cx - 12, hy + 10, cx + 11, hy + 30], 5, fill=hair)
        d.arc([cx - 9, hy + 2, cx + 6, hy + 14], 200, 300, fill=hair_l, width=2)
        for k in range(4): d.line([(cx - 6 + k * 4, hy + 12), (cx - 7 + k * 4, hy + (28 if hs == 'long' else 20))], fill=hair_d)
        if spec.get('hair_ribbon'):
            r = spec['hair_ribbon']
            d.polygon([(cx - 5, hy + 15), (cx - 1, hy + 17), (cx - 5, hy + 19)], fill=r); d.polygon([(cx + 4, hy + 15), (cx, hy + 17), (cx + 4, hy + 19)], fill=r)
    else:
        d.ellipse([cx - 11, hy + 2, cx + 10, hy + 22], fill=SKIN)
        d.ellipse([cx - 12, hy, cx + 11, hy + (13 if d_ == 0 else 10)], fill=hair)
        if d_ == 0:
            if hs in ('long', 'short'):
                for fx in range(cx - 10, cx + 10, 4):
                    d.polygon([(fx, hy + 9), (fx + 4, hy + 9), (fx + 2, hy + 12 + (fx % 3) + (1 if hs == 'long' else 0))], fill=hair)
            else:   # 상투·쪽머리: 가운데 가르마
                d.polygon([(cx - 11, hy + 10), (cx - 1, hy + 4), (cx - 1, hy + 8), (cx - 8, hy + 12)], fill=hair)
                d.polygon([(cx + 10, hy + 10), (cx, hy + 4), (cx, hy + 8), (cx + 7, hy + 12)], fill=hair)
                d.line([(cx - 1, hy + 1), (cx - 1, hy + 7)], fill=hair_l)
            side_len = 18 if hs != 'short' else 14
            d.rectangle([cx - 12, hy + 6, cx - 10, hy + side_len], fill=hair); d.rectangle([cx + 9, hy + 6, cx + 11, hy + side_len], fill=hair)
            for ex in (cx - 6, cx + 3):
                d.rectangle([ex, hy + 13, ex + 2, hy + 17], fill=EYE); d.point((ex, hy + 13), fill=(255, 255, 255)); d.point((ex + 2, hy + 17), fill=(90, 70, 110))
            if spec.get('blush', True):
                d.rectangle([cx - 9, hy + 18, cx - 7, hy + 19], fill=(246, 166, 160)); d.rectangle([cx + 6, hy + 18, cx + 8, hy + 19], fill=(246, 166, 160))
            d.line([(cx - 1, hy + 20), (cx, hy + 20)], fill=(200, 110, 100))
        elif d_ == 1:
            d.ellipse([cx - 1, hy, cx + 12, hy + (21 if hs != 'short' else 17)], fill=hair)
            d.polygon([(cx - 12, hy + 5), (cx - 2, hy + 3), (cx - 7, hy + 9)], fill=hair)
            d.rectangle([cx - 8, hy + 13, cx - 6, hy + 17], fill=EYE); d.point((cx - 8, hy + 13), fill=(255, 255, 255))
            if spec.get('blush', True): d.rectangle([cx - 10, hy + 18, cx - 8, hy + 19], fill=(246, 166, 160))
        else:
            d.ellipse([cx - 13, hy, cx, hy + (21 if hs != 'short' else 17)], fill=hair)
            d.polygon([(cx + 11, hy + 5), (cx + 1, hy + 3), (cx + 6, hy + 9)], fill=hair)
            d.rectangle([cx + 5, hy + 13, cx + 7, hy + 17], fill=EYE); d.point((cx + 7, hy + 13), fill=(255, 255, 255))
            if spec.get('blush', True): d.rectangle([cx + 7, hy + 18, cx + 9, hy + 19], fill=(246, 166, 160))
        d.arc([cx - 9, hy + 1, cx + 6, hy + 10], 200, 320, fill=hair_l, width=2)
        if spec.get('hair_ribbon') and d_ != 0:
            rx = cx + 9 if d_ == 1 else cx - 12
            d.polygon([(rx, hy + 4), (rx + 4, hy + 2), (rx + 4, hy + 8)], fill=spec['hair_ribbon'])
    # 상투 / 쪽머리
    if hs == 'topknot' and not hat:
        d.ellipse([cx - 4, hy - 4, cx + 3, hy + 3], fill=hair); d.point((cx - 2, hy - 2), fill=hair_l)
        d.rectangle([cx - 2, hy + 1, cx + 1, hy + 2], fill=(200, 170, 90))
    if hs == 'bun':
        bx = cx if d_ in (0, 3) else (cx + 8 if d_ == 1 else cx - 9)
        d.ellipse([bx - 6, hy - 6, bx + 6, hy + 4], fill=hair); d.arc([bx - 4, hy - 5, bx + 3, hy + 1], 180, 300, fill=hair_l)
        d.line([(bx - 9, hy - 1), (bx + 9, hy - 1)], fill=spec.get('pin', (220, 180, 60)), width=2)

    # 모자
    BLK = (28, 26, 34)
    if hat == 'bokdu':
        d.rounded_rectangle([cx - 11, hy - 3, cx + 10, hy + 9], 4, fill=BLK)
        d.rectangle([cx - 6, hy - 7, cx + 5, hy - 2], fill=BLK)
        d.line([(cx - 9, hy - 2), (cx + 6, hy - 2)], fill=(70, 70, 86))
        if d_ in (0, 3):
            d.rectangle([cx - 22, hy + 4, cx - 11, hy + 6], fill=BLK); d.rectangle([cx + 10, hy + 4, cx + 21, hy + 6], fill=BLK)
        elif d_ == 1:
            d.rectangle([cx + 9, hy + 3, cx + 21, hy + 5], fill=BLK)
        else:
            d.rectangle([cx - 22, hy + 3, cx - 10, hy + 5], fill=BLK)
    elif hat == 'crown':
        d.rounded_rectangle([cx - 11, hy - 2, cx + 10, hy + 9], 4, fill=BLK)
        for hx in (cx - 8, cx + 2):
            d.ellipse([hx, hy - 9, hx + 7, hy - 1], fill=BLK)
        d.rectangle([cx - 11, hy + 5, cx + 10, hy + 7], fill=(206, 168, 70))
        d.point((cx - 1, hy + 2), fill=(240, 210, 120))
    elif hat == 'helmet':
        HM = (130, 136, 150)
        d.chord([cx - 12, hy - 4, cx + 11, hy + 16], 180, 360, fill=HM)
        d.rectangle([cx - 13, hy + 5, cx + 12, hy + 8], fill=sh(HM, 0.75))
        d.arc([cx - 9, hy - 2, cx + 4, hy + 10], 200, 290, fill=sh(HM, 1.35), width=2)
        d.polygon([(cx - 2, hy - 4), (cx + 1, hy - 4), (cx - 1, hy - 10)], fill=sh(HM, 1.2))
        if spec.get('plume'):
            d.polygon([(cx - 1, hy - 10), (cx + 6, hy - 13), (cx + 3, hy - 7)], fill=spec['plume'])
        if d_ != 3:
            for ex in ((cx - 13, cx - 10) if d_ != 2 else ()) + (() if d_ == 1 else ()):
                pass
            d.rectangle([cx - 13, hy + 8, cx - 11, hy + 15], fill=sh(HM, 0.8)); d.rectangle([cx + 10, hy + 8, cx + 12, hy + 15], fill=sh(HM, 0.8))
    elif hat == 'band':
        B = spec.get('band', (236, 230, 214))
        if d_ != 3:
            d.rectangle([cx - 12, hy + 7, cx + 11, hy + 9], fill=B)
        else:
            d.rectangle([cx - 12, hy + 7, cx + 11, hy + 9], fill=B)
            d.line([(cx - 1, hy + 9), (cx - 4, hy + 16)], fill=B, width=2); d.line([(cx, hy + 9), (cx + 3, hy + 15)], fill=B, width=2)
    return outline(lay, 0.4)

def sheet(spec, path):
    out = Image.new('RGBA', (144, 192), (0, 0, 0, 0))
    for d_ in range(4):
        for st in range(3):
            out.alpha_composite(draw(spec, d_, st), (st * 48, d_ * 48))
    out.save(path)

NAVY = (44, 58, 108)
SPECS = {
    'student_m':  dict(hair=(36, 30, 36), hairstyle='short', top=NAVY, accent=(196, 48, 56), accent_style='collar', bottom=(104, 106, 118), shoes=(40, 34, 34), blush=False),
    'student_f':  dict(hair=(40, 32, 40), hairstyle='long', hair_ribbon=(214, 52, 66), top=NAVY, accent=(214, 52, 66), accent_style='ribbon', lower='skirt', bottom=(54, 62, 110), shoes=(40, 34, 34)),
    'npc_minister': dict(hairstyle='short', hat='bokdu', top=(150, 46, 46), accent=(220, 184, 90), accent_style='emblem', lower='robe', shoes=(40, 30, 30), blush=False),
    'npc_potter':   dict(hairstyle='topknot', hair=(46, 38, 34), top=(140, 104, 70), accent=(150, 60, 50), accent_style='vneck', bottom=(206, 192, 160), shoes=(110, 84, 60), blush=False),
    'npc_apprentice': dict(hairstyle='short', hair=(54, 42, 36), top=(214, 198, 160), accent=(140, 110, 80), accent_style='vneck', bottom=(184, 168, 134), shoes=(120, 92, 66)),
    'npc_slave_a':  dict(hairstyle='topknot', hat='band', top=(176, 156, 122), accent=(120, 100, 76), accent_style='belt', bottom=(156, 138, 108), shoes=(100, 80, 58), blush=False),
    'npc_slave_b':  dict(hairstyle='short', top=(132, 124, 108), accent=(92, 82, 72), accent_style='belt', bottom=(124, 114, 100), shoes=(86, 70, 54), blush=False),
    'npc_slave_c':  dict(hairstyle='topknot', hat='band', band=(204, 174, 124), top=(156, 116, 82), accent=(104, 80, 56), accent_style='belt', bottom=(146, 126, 100), shoes=(96, 74, 54), blush=False),
    'npc_slave_d':  dict(hairstyle='bun', top=(184, 168, 140), accent=(150, 80, 60), accent_style='vneck', lower='skirt', bottom=(146, 126, 104), socks=(224, 214, 194), shoes=(104, 84, 62)),
    'npc_soldier':  dict(hairstyle='short', hat='helmet', top=(96, 110, 138), accent=(176, 56, 50), accent_style='belt', bottom=(72, 72, 86), shoes=(52, 42, 38), blush=False),
    'npc_monk':     dict(hairstyle='bald', top=(136, 132, 128), accent=(156, 100, 62), accent_style='belt', lower='robe', shoes=(84, 72, 62), blush=False),
    'npc_monk2':    dict(hairstyle='bald', top=(100, 96, 96), accent=(176, 84, 52), accent_style='belt', lower='robe', shoes=(72, 62, 52), blush=False),
    'npc_king':     dict(hairstyle='short', hat='crown', top=(192, 38, 42), accent=(230, 194, 84), accent_style='emblem', lower='robe', shoes=(40, 30, 30), blush=False),
    'npc_lady':     dict(hairstyle='bun', top=(100, 156, 104), accent=(196, 60, 70), accent_style='vneck', lower='skirt', bottom=(180, 52, 62), socks=(244, 240, 230), shoes=(180, 52, 62)),
    'npc_scholar_a': dict(hairstyle='short', hat='bokdu', top=(60, 88, 146), accent=(224, 204, 152), accent_style='emblem', lower='robe', shoes=(40, 30, 30), blush=False),
    'npc_scholar_b': dict(hairstyle='short', hat='bokdu', top=(60, 122, 88), accent=(224, 204, 152), accent_style='emblem', lower='robe', shoes=(40, 30, 30), blush=False),
    'npc_general':  dict(hairstyle='short', hat='helmet', plume=(210, 40, 40), top=(164, 46, 42), accent=(218, 184, 84), accent_style='belt', bottom=(74, 52, 46), shoes=(52, 42, 38), blush=False),
}

if __name__ == '__main__':
    out = sys.argv[1]
    os.makedirs(out, exist_ok=True)
    for k, v in SPECS.items():
        sheet(v, os.path.join(out, '$' + k + '.png'))
    prev = Image.new('RGBA', (48 * len(SPECS), 48 * 4), (210, 200, 180, 255))
    for i, k in enumerate(SPECS):
        sh_ = Image.open(os.path.join(out, '$' + k + '.png'))
        for r in range(4):
            prev.alpha_composite(sh_.crop((48, r * 48, 96, r * 48 + 48)), (i * 48, r * 48))
    prev.resize((prev.width * 2, prev.height * 2), Image.NEAREST).save(os.path.join(sys.argv[2], 'hd_chars_all.png'))
    print('sheets', len(SPECS))
