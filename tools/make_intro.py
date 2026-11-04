"""인트로 영상 (movies/intro_goryeo.webm / .mp4) 생성"""
import os, sys, math, random, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from make_title import night_scene, draw_gate, glow_layer, logo, sprite_frame, outlined, sans, serif
import make_music as MM

ROOT = sys.argv[1]
TMP = sys.argv[2]
os.makedirs(TMP, exist_ok=True)
os.makedirs(os.path.join(ROOT, 'movies'), exist_ok=True)
FPS = 24
WIDTH, HEIGHT = 816, 624
DUR = 55.0
CH = os.path.join(ROOT, 'img/characters')
PIC = os.path.join(ROOT, 'img/pictures')
PAR = os.path.join(ROOT, 'img/parallaxes')

def ease(x): return 0 if x <= 0 else 1 if x >= 1 else x * x * (3 - 2 * x)
def seg(t, a, b): return 0 if t < a else 1 if t > b else (t - a) / (b - a)
def fade_in_out(t, a, b, f=0.5): return ease(seg(t, a, a + f)) * (1 - ease(seg(t, b - f, b)))

# ------------------------------------------------------------------ 박물관 배경 (도트)
def museum_bg():
    im = Image.new('RGB', (272, 208)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, 272, 80], fill=(214, 208, 196))
    for x in range(0, 272, 34):
        d.rectangle([x, 0, x + 1, 80], fill=(196, 190, 178))
    d.rectangle([0, 76, 272, 80], fill=(150, 120, 90))
    for y in range(80, 208, 6):
        d.rectangle([0, y, 272, y + 5], fill=(150, 108, 70) if (y // 6) % 2 else (142, 102, 66))
        d.line([(0, y + 5), (272, y + 5)], fill=(120, 86, 56))
    # 천장 조명
    for x in (60, 136, 212):
        d.ellipse([x - 4, 2, x + 4, 6], fill=(255, 250, 220))
    # 벽 안내판 / 액자
    for x in (14, 228):
        d.rectangle([x, 22, x + 30, 52], fill=(70, 60, 54)); d.rectangle([x + 2, 24, x + 28, 50], fill=(220, 210, 180))
        for j in range(28, 48, 4): d.line([(x + 5, j), (x + 25, j)], fill=(120, 110, 100))
    d.rectangle([100, 14, 172, 26], fill=(90, 40, 36));
    # 진열장 3개
    def case(x, y, w, h, item):
        d.rectangle([x, y + h - 14, x + w, y + h + 6], fill=(60, 50, 46))
        d.rectangle([x + 1, y, x + w - 1, y + h - 14], fill=(176, 206, 214))
        d.rectangle([x + 3, y + 2, x + w - 3, y + h - 16], fill=(120, 150, 160))
        d.line([(x + 4, y + 3), (x + 10, y + h - 18)], fill=(220, 240, 245))
        cx = x + w // 2
        if item == 'vase':
            d.ellipse([cx - 7, y + 10, cx + 7, y + 30], fill=(124, 172, 152)); d.rectangle([cx - 3, y + 6, cx + 3, y + 12], fill=(124, 172, 152))
            d.point((cx - 2, y + 18), fill=(250, 250, 250)); d.point((cx + 2, y + 22), fill=(30, 30, 30))
        elif item == 'book':
            d.rectangle([cx - 9, y + 18, cx + 9, y + 28], fill=(220, 206, 170)); d.line([(cx, y + 18), (cx, y + 28)], fill=(120, 90, 60))
        else:
            d.rectangle([cx - 10, y + 14, cx + 10, y + 30], fill=(150, 112, 70));
            for j in range(16, 30, 3): d.line([(cx - 8, j + y), (cx + 8, j + y)], fill=(110, 80, 50))
    case(30, 60, 40, 46, 'board'); case(116, 52, 40, 56, 'vase'); case(202, 60, 40, 46, 'book')
    for x in (20, 252):
        d.rectangle([x, 120, x + 2, 140], fill=(200, 170, 80))
    d.line([(22, 124), (252, 124)], fill=(150, 30, 40), width=1)
    big = im.resize((816, 624), Image.NEAREST).convert('RGBA')
    for x in (180, 408, 636):
        big.alpha_composite(glow_layer(big.size, x, 120, 120, (255, 240, 200), 0.6))
    return big

def big_vase():
    im = Image.new('RGBA', (816, 624), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    cx, top = 408, 120
    vase = [(cx - 30, top), (cx + 30, top), (cx + 34, top + 20), (cx + 100, top + 80), (cx + 108, top + 150), (cx + 78, top + 250),
            (cx + 52, top + 340), (cx - 52, top + 340), (cx - 78, top + 250), (cx - 108, top + 150), (cx - 100, top + 80), (cx - 34, top + 20)]
    d.polygon(vase, fill=(124, 172, 152, 255), outline=(60, 96, 84, 255))
    d.ellipse([cx - 32, top - 10, cx + 32, top + 10], fill=(108, 152, 134, 255), outline=(60, 96, 84, 255))
    def crane(x, y, s):
        d.ellipse([x - 30 * s, y - 30 * s, x + 30 * s, y + 30 * s], outline=(250, 250, 246, 255), width=3)
        d.line([(x - 18 * s, y + 4 * s), (x, y - 6 * s), (x + 18 * s, y + 4 * s)], fill=(250, 250, 246, 255), width=4)
        d.line([(x, y - 6 * s), (x + 6 * s, y - 16 * s)], fill=(250, 250, 246, 255), width=3)
    def cloud(x, y):
        for k in range(3):
            d.arc([x + k * 12 - 10, y - 8, x + k * 12 + 6, y + 8], 180, 360, fill=(36, 40, 40, 255), width=4)
    crane(cx - 40, top + 110, 1); crane(cx + 45, top + 190, 0.9); crane(cx - 25, top + 260, 0.75)
    cloud(cx + 20, top + 90); cloud(cx - 70, top + 180); cloud(cx + 25, top + 270); cloud(cx - 5, top + 160)
    d.polygon([(cx - 70, top + 60), (cx - 50, top + 60), (cx - 90, top + 230), (cx - 100, top + 200)], fill=(255, 255, 255, 40))
    return im

def caption(frame, text, alpha, speaker=None):
    if alpha <= 0: return
    lay = Image.new('RGBA', frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    f = sans(26)
    lines = []
    for para in text.split('\n'):
        line = ''
        for ch in para:
            if d.textlength(line + ch, font=f) > 700 and line:
                lines.append(line); line = ch
            else:
                line += ch
        lines.append(line)
    h = 30 + len(lines) * 38 + (30 if speaker else 0)
    y0 = 600 - h
    d.rounded_rectangle([40, y0, 776, 600], 14, fill=(10, 8, 6, 200), outline=(255, 214, 120, 220), width=2)
    y = y0 + 16
    if speaker:
        d.text((62, y), speaker, font=sans(20), fill=(255, 210, 120, 255)); y += 30
    for ln in lines:
        d.text((408, y + 16), ln, font=f, fill=(255, 255, 255, 255), anchor='mm'); y += 38
    a = lay.split()[3].point(lambda v: int(v * alpha))
    lay.putalpha(a)
    frame.alpha_composite(lay)

def skip_hint(frame):
    return   # 영상은 건너뛸 수 없게 바뀌어 안내 문구를 표시하지 않음
    d = ImageDraw.Draw(frame)
    d.text((800, 14), 'Enter · 클릭: 건너뛰기', font=sans(14), fill=(255, 255, 255, 150), anchor='ra')

def overlay(frame, color, alpha):
    if alpha <= 0: return
    lay = Image.new('RGBA', frame.size, color + (int(255 * min(1, alpha)),))
    frame.alpha_composite(lay)

# ------------------------------------------------------------------ 미리 준비
import hd_title
MUSEUM = hd_title.museum()
VASE = big_vase()
def core816(im):
    """넓은 화면용 그림(1392px)이면 가운데 816px만 사용"""
    if im.width > 816:
        x = (im.width - 816) // 2
        im = im.crop((x, 0, x + 816, 624))
    return im

PALACE = core816(Image.open(os.path.join(PAR, '!bg_palace.png')).convert('RGBA'))
NIGHT = hd_title.night()
TITLE_IMG = core816(Image.open(os.path.join(ROOT, 'img/titles1/TimeGate_Title.png')).convert('RGBA'))
SM = os.path.join(CH, '$student_m.png'); SF = os.path.join(CH, '$student_f.png')
THUMBS = [core816(Image.open(os.path.join(PAR, n + '.png')).convert('RGBA')).resize((160, 122), Image.LANCZOS) for n in
          ['!bg_palace', '!bg_workshop', '!bg_mansion', '!bg_ganghwa', '!bg_dojang', '!bg_yuan', '!bg_temple', '!bg_ending']]
ERA = ['고려 건국', '청자 공방', '무신 집권기', '몽골과의 전쟁', '팔만대장경', '원 간섭기', '직지', '여말선초']
ICONS = {k: Image.open(os.path.join(PIC, k + '.png')).convert('RGBA') for k in ['item_celadon', 'item_takbon', 'item_type']}
rnd = random.Random(11)
STARS = [(rnd.uniform(0, 6.28), rnd.uniform(10, 420), rnd.uniform(0.6, 1.6)) for _ in range(160)]
GATE_GLOW = glow_layer((816, 624), 408, 280, 260, (255, 226, 150), 1.5)

def students(frame, x, y, row, step, scale=2):
    for i, path in enumerate([SM, SF]):
        fr = sprite_frame(path, row, step, scale)
        frame.alpha_composite(fr, (int(x + i * 70), int(y)))

def card(frame, x, y, w, h, title, body, icon_fn, alpha, red=False):
    lay = Image.new('RGBA', frame.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(lay)
    d.rounded_rectangle([x, y, x + w, y + h], 16, fill=(236, 222, 188, 255), outline=(120, 84, 50, 255), width=4)
    icon_fn(lay, d, x + w // 2, y + 70)
    d.text((x + w // 2, y + 150), title, font=sans(24), fill=(170, 40, 36, 255) if red else (60, 40, 26, 255), anchor='mm')
    d.text((x + w // 2, y + 190), body, font=sans(17), fill=(60, 40, 26, 255), anchor='mm')
    lay.putalpha(lay.split()[3].point(lambda v: int(v * alpha)))
    frame.alpha_composite(lay, (0, int((1 - alpha) * 30)))

def icon_lock(lay, d, cx, cy):
    for i, s in enumerate(['↑', '비', '7']):
        x = cx - 75 + i * 52
        d.rounded_rectangle([x, cy - 24, x + 44, cy + 24], 6, fill=(30, 28, 40, 255), outline=(255, 214, 120, 255), width=2)
        d.text((x + 22, cy), s, font=sans(24), fill=(255, 255, 255, 255), anchor='mm')
        d.polygon([(x + 22, cy - 40), (x + 14, cy - 30), (x + 30, cy - 30)], fill=(200, 150, 60, 255))
def icon_treasure(lay, d, cx, cy):
    for i, k in enumerate(['item_celadon', 'item_takbon', 'item_type']):
        ic = ICONS[k].resize((64, 64), Image.NEAREST)
        lay.alpha_composite(ic, (cx - 100 + i * 68, cy - 32))
def icon_time(lay, d, cx, cy):
    d.polygon([(cx - 60, cy - 36), (cx - 20, cy - 36), (cx - 40, cy), ], fill=(214, 176, 90, 255))
    d.polygon([(cx - 40, cy), (cx - 60, cy + 36), (cx - 20, cy + 36)], fill=(214, 176, 90, 255))
    d.rectangle([cx - 64, cy - 40, cx - 16, cy - 36], fill=(110, 70, 40, 255)); d.rectangle([cx - 64, cy + 36, cx - 16, cy + 40], fill=(110, 70, 40, 255))
    d.ellipse([cx + 4, cy - 34, cx + 72, cy + 34], fill=(196, 140, 52, 255))
    d.text((cx + 38, cy), '3', font=sans(40), fill=(255, 255, 255, 255), anchor='mm')

def render(t):
    f = Image.new('RGBA', (WIDTH, HEIGHT), (0, 0, 0, 255))
    # S1 박물관
    if t < 7.0:
        f.alpha_composite(MUSEUM)
        walk = ease(seg(t, 0.3, 4.4))
        x = -150 + walk * 420
        moving = 0.3 < t < 4.4
        step = [0, 1, 2, 1][int(t * 8) % 4] if moving else 1
        row = 2 if moving else 3
        students(f, x, 470, row, step)
        caption(f, '국립박물관 고려실, 역사 수업 견학 날.', fade_in_out(t, 0.6, 3.6))
        caption(f, '우리는 푸른 청자 앞에서 걸음을 멈췄다.', fade_in_out(t, 3.9, 6.9))
        overlay(f, (0, 0, 0), 1 - seg(t, 0, 0.8))
    # S2 청자 클로즈업
    elif t < 12.5:
        k = seg(t, 7.0, 12.5)
        bg = Image.new('RGBA', (WIDTH, HEIGHT), (24, 30, 40, 255))
        f.alpha_composite(bg)
        for _ in range(1 + int(k * 3)):
            f.alpha_composite(glow_layer(f.size, 408, 300, int(170 + 140 * k), (255, 236, 170), 0.6 + 2.4 * k))
        sc = 1.0 + 0.12 * k
        v = VASE.resize((int(816 * sc), int(624 * sc)), Image.BILINEAR)
        f.alpha_composite(v, (int(408 - 408 * sc), int(312 - 312 * sc)))
        if k > 0.4:
            r = random.Random(int(t * 24))
            d = ImageDraw.Draw(f)
            for _ in range(int(30 * k)):
                a = r.uniform(0, 6.28); rr = r.uniform(80, 260)
                x, y = 408 + math.cos(a) * rr, 300 + math.sin(a) * rr
                d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=(255, 244, 200, 255))
        caption(f, '그때, 진열장 속 청자가 빛나기 시작했다...', fade_in_out(t, 7.4, 12.2))
        overlay(f, (0, 0, 0), 1 - seg(t, 7.0, 7.5))
    # S3 시간 터널
    elif t < 15.5:
        k = seg(t, 12.5, 15.5)
        f.alpha_composite(Image.new('RGBA', f.size, (14, 16, 44, 255)))
        lay = Image.new('RGBA', f.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
        for i in range(18):
            a = i * math.pi / 9 + t * 2.4
            L = 600
            d.polygon([(408, 312), (408 + math.cos(a - 0.06) * L, 312 + math.sin(a - 0.06) * L), (408 + math.cos(a + 0.06) * L, 312 + math.sin(a + 0.06) * L)],
                      fill=(255, 226, 150, 70) if i % 2 else (160, 200, 255, 60))
        for (ang, dist, sp) in STARS:
            rr = (dist + (t - 12.5) * 260 * sp) % 520
            x, y = 408 + math.cos(ang + t * 0.8) * rr, 312 + math.sin(ang + t * 0.8) * rr
            s = 1 + rr / 160
            d.ellipse([x - s, y - s, x + s, y + s], fill=(255, 250, 230, 230))
        f.alpha_composite(lay)
        f.alpha_composite(glow_layer(f.size, 408, 312, 200, (255, 250, 230), 1.4))
        overlay(f, (255, 252, 240), max(1 - seg(t, 12.5, 13.3), seg(t, 14.7, 15.5)))
    # S4 고려 궁궐
    elif t < 21.5:
        f.alpha_composite(PALACE)
        step = 1
        bob = 0
        students(f, 408 - 72, 380, 0, step)
        caption(f, '눈을 떠 보니... 그곳은 천 년도 더 된 고려의 궁궐이었다.', fade_in_out(t, 16.2, 21.2))
        overlay(f, (255, 252, 240), 1 - seg(t, 15.5, 16.4))
    # S5 수수께끼의 목소리
    elif t < 28.5:
        f.alpha_composite(PALACE)
        students(f, 408 - 72, 380, 3, 1)
        overlay(f, (0, 0, 10), 0.72 * ease(seg(t, 21.5, 22.5)))
        a = ease(seg(t, 22.0, 23.2))
        if a > 0:
            g = Image.new('RGBA', f.size, (0, 0, 0, 0))
            draw_gate(g, 408, 220, 0.75, t=t * 0.6)
            g.putalpha(g.split()[3].point(lambda v: int(v * a)))
            f.alpha_composite(g)
        caption(f, "집으로 돌아가려면 고려의 시간을 끝까지 건너,\n'시간의 문'을 열어야 한다.", fade_in_out(t, 22.6, 28.2), speaker='수수께끼의 목소리')
    # S6 8개의 시대
    elif t < 40.5:
        f.alpha_composite(NIGHT)
        overlay(f, (10, 8, 30), 0.55)
        d = ImageDraw.Draw(f)
        d.text((408, 40), '건너야 할 8개의 시대', font=serif(34), fill=(255, 226, 150), anchor='mm')
        pos = []
        for i in range(8):
            row = i // 4
            col = i % 4 if row == 0 else 3 - i % 4
            pos.append((40 + col * 190, 86 + row * 196))
        shown = int(max(0, (t - 29.0) / 1.15)) + 1
        for i in range(min(8, shown)):
            x, y = pos[i]
            k = ease(seg(t, 29.0 + i * 1.15, 29.5 + i * 1.15))
            if i > 0:
                px, py = pos[i - 1]
                d.line([(px + 80, py + 61), (x + 80, y + 61)], fill=(255, 214, 120), width=4)
            th = THUMBS[i].copy()
            th.putalpha(int(255 * k))
            f.alpha_composite(th, (x, y + int((1 - k) * 20)))
            d = ImageDraw.Draw(f)
            d.rounded_rectangle([x - 2, y - 2, x + 161, y + 123], 6, outline=(255, 214, 120), width=3)
            d.ellipse([x - 14, y - 14, x + 18, y + 18], fill=(170, 40, 36), outline=(255, 230, 170), width=2)
            d.text((x + 2, y + 2), str(i + 1), font=sans(18), fill=(255, 255, 255), anchor='mm')
            d.text((x + 80, y + 140), ERA[i], font=sans(20), fill=(255, 255, 255), anchor='mm')
        caption(f, '고려가 세워진 때부터 문을 닫을 때까지,\n8개의 시대를 차례로 지나야 한다.', fade_in_out(t, 29.2, 40.2))
        overlay(f, (0, 0, 0), 1 - seg(t, 28.5, 29.0))
    # S7 탈출 방법
    elif t < 48.5:
        f.alpha_composite(NIGHT)
        overlay(f, (10, 8, 30), 0.6)
        d = ImageDraw.Draw(f)
        d.text((408, 60), '이렇게 탈출한다', font=serif(38), fill=(255, 226, 150), anchor='mm')
        card(f, 40, 150, 230, 230, '잠긴 문을 열어라', '흩어진 단서를 이어 푼다', icon_lock, ease(seg(t, 41.0, 41.6)))
        card(f, 293, 150, 230, 230, '세 보물을 모아라', '청자 · 탁본 · 금속활자', icon_treasure, ease(seg(t, 43.0, 43.6)))
        card(f, 546, 150, 230, 230, '40분 · 힌트 3번', '힌트는 게임 전체에서 단 3번!', icon_time, ease(seg(t, 45.0, 45.6)), red=True)
        caption(f, '마지막 방의 시간의 문을 열면 집으로 돌아갈 수 있다.', fade_in_out(t, 46.0, 48.3))
        overlay(f, (0, 0, 0), 1 - seg(t, 40.5, 41.0))
    # S8 로고
    else:
        k = seg(t, 48.5, 50.0)
        f.alpha_composite(TITLE_IMG)
        d = ImageDraw.Draw(f)
        if t > 51.0:
            a = fade_in_out(t, 51.0, 54.2, 0.6)
            box = Image.new('RGBA', f.size, (0, 0, 0, 0)); bd = ImageDraw.Draw(box)
            bd.rounded_rectangle([288, 446, 528, 494], 24, fill=(10, 8, 20, int(190 * a)), outline=(255, 214, 120, int(220 * a)), width=2)
            bd.text((408, 470), '준비됐나요?', font=sans(30), fill=(255, 255, 255, int(255 * a)), anchor='mm')
            f.alpha_composite(box)
        overlay(f, (0, 0, 0), max(1 - ease(k), seg(t, 54.2, 55.0)))
    if t < 54.0:
        skip_hint(f)
    return f.convert('RGB')

# ------------------------------------------------------------------ 소리
def make_audio(path):
    music = MM.title(seconds=DUR + 1, loop=False)[:int(MM.SR * DUR)]
    music = music * 0.75
    fx = np.zeros_like(music)
    def put(sig, at, g=1.0):
        i = int(at * MM.SR); j = min(len(fx), i + len(sig)); fx[i:j] += sig[:j - i] * g
    put(MM.bell(MM.midi(MM.nm('E5')), 6, 0.7), 7.3, 0.9)
    put(MM.bell(MM.midi(MM.nm('A5')), 6, 0.5), 9.8, 0.7)
    put(MM.whoosh(3.2, 0.9), 12.2, 1.0)
    put(MM.bell(MM.midi(MM.nm('C4')), 8, 0.8), 15.6, 0.8)
    for i in range(8):
        put(MM.gayageum(MM.midi(MM.PYEONG[2 + i % 8]), 0.6, 0.6), 29.0 + i * 1.15, 0.8)
    for at in (41.0, 43.0, 45.0):
        put(MM.janggu('deong', 0.7), at, 1.0)
    put(MM.buk(0.9), 48.6, 1.0)
    put(MM.bell(MM.midi(MM.nm('C5')), 6, 0.8), 48.7, 0.9)
    mix = music + fx
    mix = np.tanh(mix * 1.2) / np.tanh(1.2)
    fade = np.ones(len(mix)); n = int(MM.SR * 1.2); fade[-n:] = np.linspace(1, 0, n)
    mix = mix * fade
    mix = mix / max(1e-9, np.max(np.abs(mix))) * 0.9
    st = (np.stack([mix, mix], 1) * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(MM.SR); w.writeframes(st.tobytes())

if __name__ == '__main__':
    only = sys.argv[3] if len(sys.argv) > 3 else None
    if only == 'preview':
        for i, tt in enumerate([2.5, 5.5, 10.5, 13.8, 18.5, 25.0, 38.5, 46.5, 52.0]):
            render(tt).save(os.path.join(TMP, 'intro_prev_%d.png' % i))
        sys.exit(0)
    wav = os.path.join(TMP, 'intro.wav')
    make_audio(wav)
    raw = os.path.join(TMP, 'intro_video.mp4')
    p = subprocess.Popen(['ffmpeg', '-loglevel', 'error', '-y', '-f', 'rawvideo', '-pix_fmt', 'rgb24', '-s', '%dx%d' % (WIDTH, HEIGHT),
                          '-r', str(FPS), '-i', '-', '-c:v', 'libx264', '-crf', '12', '-preset', 'veryfast', '-pix_fmt', 'yuv420p', raw],
                         stdin=subprocess.PIPE)
    n = int(DUR * FPS)
    for i in range(n):
        p.stdin.write(render(i / FPS).tobytes())
        if i % 120 == 0:
            print('frame', i, '/', n, flush=True)
    p.stdin.close(); p.wait()
    mv = os.path.join(ROOT, 'movies')
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', raw, '-i', wav, '-c:v', 'libx264', '-crf', '24', '-preset', 'slow',
                    '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', os.path.join(mv, 'intro_goryeo.mp4')], check=True)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', raw, '-i', wav, '-c:v', 'libvpx-vp9', '-b:v', '0', '-crf', '36', '-row-mt', '1',
                    '-deadline', 'good', '-cpu-used', '4', '-c:a', 'libopus', '-b:a', '112k', '-shortest', os.path.join(mv, 'intro_goryeo.webm')], check=True)
    print('done')
