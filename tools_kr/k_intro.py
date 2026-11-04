"""척화비 아래에서 인트로 영상 (movies/Kr_Intro.webm · .mp4, 1280x720, 약 44초, 건너뛸 수 없음)
 0~6   검은 화면 글씨: 1882년 가을, 일본으로 떠나는 젊은 역관
 6~14  1880년 무렵 동아시아 지도 위로 조선을 찾아온 배들 (프랑스 1866 · 미국 1871 · 일본 1875)
 14~21 역관 집 사랑방, 일기를 펼친 윤재
 21~35 일기 속 장면들 (1867 경복궁 · 1866 강화도 · 1871 광성보 · 1876 연무당 · 1881 하도감 · 1882 선혜청)
 35~44 "문을 닫을 것인가, 열 것인가" → 제목
"""
import os, sys, math, subprocess, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from k_common import F
import k_music as MU
import k_geo as GEO

W, H, FPS, DUR = 1280, 720, 30, 44.0
def ease(x): return 0 if x <= 0 else 1 if x >= 1 else x * x * (3 - 2 * x)
def seg(t, a, b): return 0 if t < a else 1 if t > b else (t - a) / (b - a)
def fio(t, a, b, f=0.6): return ease(seg(t, a, a + f)) * (1 - ease(seg(t, b - f, b)))

def sepia(im):
    g = ImageOps.grayscale(im.convert('RGB'))
    return ImageOps.colorize(g, (36, 24, 14), (250, 236, 206)).convert('RGBA')

def text(frame, s, y, size, a, col=(250, 236, 206), kind='serif'):
    if a <= 0: return
    lay = Image.new('RGBA', frame.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((W / 2, y), s, font=F(size, kind), fill=col + (int(255 * a),), anchor='mm', stroke_width=3, stroke_fill=(20, 12, 6, int(200 * a)))
    frame.alpha_composite(lay)

def compose(root, mid, par, keep):
    """지도 원경 위에 그 장면의 인물들을 세운 그림 (가운데 17칸)"""
    import json
    mp = json.load(open(os.path.join(root, 'data', 'Map%03d.json' % mid), encoding='utf-8'))
    im = Image.open(os.path.join(root, 'img/parallaxes', par + '.png')).convert('RGBA')
    DIR = {2: 0, 4: 1, 6: 2, 8: 3}
    for e in sorted([e for e in mp['events'] if e], key=lambda e: e['y']):
        if e['name'] not in keep: continue
        pg = e['pages'][0]; img = pg['image']['characterName']
        if not img: continue
        sh_ = Image.open(os.path.join(root, 'img/characters', img + '.png')).convert('RGBA')
        fw, fh = sh_.width // 3, sh_.height // 4
        r = DIR[pg['image']['direction']]
        im.alpha_composite(sh_.crop((fw, r * fh, fw * 2, r * fh + fh)), (e['x'] * 48 + 24 - fw // 2, e['y'] * 48 + 48 - fh))
    top = os.path.join(root, 'img/parallaxes', par + '_top.png')
    if os.path.exists(top): im.alpha_composite(Image.open(top).convert('RGBA'))
    return im.crop((288, 0, 1104, 624))

SHOT_KEEP = {
    '!k_palace': (2, {'father', 'overseer', 'corvee', 'carpenter', 'rich', 'stone1', 'stone2', 'stone3', 'cart'}),
    '!k_ganghwa': (4, {'yanghs', 'hunter', 'father', 'fr1', 'fr2', 'fr3'}),
    '!k_gwangseong': (5, {'eojaeyeon', 'hunter2', 'beacon_m', 'bongsu', 'soldier2', 'cannon1', 'cannon2', 'sujagi'}),
    '!k_yeonmudang': (6, {'sinheon', 'kuroda', 'ogyeongseok', 'father', 'treaty', 'jp1', 'jp2', 'kr1'}),
    '!k_hadogam': (7, {'horimoto', 'byeol1', 'byeol2', 'byeol3', 'old_soldier', 'drum', 'rifles', 'kimhongjip', 'young_off', 'imansun', 'confucian', 'confucian2', 'chmap'}),
    '!k_seonhye': (8, {'kimchunyoung', 'clerk', 'scale', 'rice', 'ledger', 'soldier3', 'poor2'}),
}
def tone(im, dark=(14, 20, 34), light=(214, 230, 244)):
    g = ImageOps.grayscale(im.convert('RGB'))
    return ImageOps.colorize(g, dark, light).convert('RGBA')

def build(root):
    pars = os.path.join(root, 'img', 'parallaxes')
    lib = Image.open(os.path.join(pars, '!k_sarang.png')).convert('RGBA').crop((288, 0, 1104, 624))
    st_big = lib.resize((int(816 * 1.7), int(624 * 1.7)), Image.NEAREST)
    hero = Image.open(os.path.join(root, 'img/characters/$k_yunjae26.png')).convert('RGBA')
    fw, fh = hero.width // 3, hero.height // 4
    hero = hero.crop((fw, 0, fw * 2, fh)).resize((fw * 4, fh * 4), Image.NEAREST)
    shots = [('!k_palace', '1867  경복궁 중건 공사장'), ('!k_ganghwa', '1866  강화도 · 프랑스 함대'), ('!k_gwangseong', '1871  광성보 · 미국 함대'),
             ('!k_yeonmudang', '1876  강화부 연무당 · 일본과의 조약'), ('!k_hadogam', '1881  별기군과 유생들'), ('!k_seonhye', '1882  선혜청 도봉소')]
    shot_imgs = []
    for n, cap in shots:
        mid, keep = SHOT_KEEP[n]
        im = compose(root, mid, n, keep).resize((780, 596), Image.LANCZOS)
        shot_imgs.append((tone(im, (40, 26, 16), (250, 236, 206)), cap))
    SHIPS = [((120.5, 34.0), (125.9, 37.6), '프랑스 함대 1866', (210, 210, 240)), ((122.0, 31.5), (126.2, 37.4), '미국 함대 1871', (200, 220, 250)),
             ((131.5, 33.5), (126.6, 37.5), '일본 군함 1875', (250, 220, 200))]
    base = GEO.render(1880, (112, 146, 26, 46), (W, H), colors=lambda p, o: (176, 160, 120) if 'Korea' in (p.get('NAME') or '') else (100, 92, 84),
                      line_w=0.6, seed=1880, paper=False, sea=(18, 30, 50), line=(40, 34, 30))
    world, pj = base[0].convert('RGBA'), base[1]
    grain = [Image.effect_noise((W // 2, H // 2), 40).resize((W, H)).convert('L') for _ in range(4)]
    tmp = os.path.join(root, '_intro_frames'); os.makedirs(tmp, exist_ok=True)
    N_ = int(DUR * FPS)
    for i in range(N_):
        t = i / FPS
        fr = Image.new('RGBA', (W, H), (8, 6, 4, 255))
        if t < 6.2:
            text(fr, '1882년 가을, 한양.', H / 2 - 40, 34, fio(t, 0.6, 6.0))
            text(fr, '내일 일본으로 떠나는 젊은 역관 윤재.', H / 2 + 20, 26, fio(t, 2.0, 6.0), col=(230, 214, 180))
            text(fr, '그는 아버지가 스무 해 동안 쓴 통역 일기를 펼친다.', H / 2 + 62, 24, fio(t, 3.0, 6.0), col=(210, 196, 166))
        elif t < 14.2:
            fr.alpha_composite(world)
            d = ImageDraw.Draw(fr)
            x, y = pj(127.0, 37.0); d.text((x - 20, y + 40), '조선', font=F(30, 'serif'), fill=(250, 236, 200), stroke_width=3, stroke_fill=(30, 20, 10), anchor='mm')
            for j, (a0, a1, lb, col) in enumerate(SHIPS):
                kj = seg(t, 6.8 + j * 2.0, 8.8 + j * 2.0)
                if kj <= 0: continue
                x0, y0 = pj(*a0); x1, y1 = pj(*a1); xx = x0 + (x1 - x0) * ease(kj) * 0.85; yy = y0 + (y1 - y0) * ease(kj) * 0.85
                d.line([(x0, y0), (xx, yy)], fill=col, width=3)
                d.polygon([(xx - 14, yy - 4), (xx + 14, yy - 4), (xx + 9, yy + 6), (xx - 9, yy + 6)], fill=(30, 30, 36)); d.line([(xx, yy - 4), (xx, yy - 22)], fill=(200, 200, 200), width=2)
                d.text((x0 + 10, y0 + 14), lb, font=F(20), fill=col, stroke_width=2, stroke_fill=(10, 10, 20))
            text(fr, '바다 건너 낯선 배들이 조선의 문을 두드렸다', 70, 34, fio(t, 6.6, 14.0))
            text(fr, '문을 닫을 것인가, 열 것인가. 조선은 갈림길에 섰다.', H - 70, 22, fio(t, 8.0, 14.0), col=(230, 214, 180), kind='sans')
            a = fio(t, 6.2, 14.2, 0.6)
            fr.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * (1 - a)))))
        elif t < 21.2:
            k = seg(t, 14.2, 21.2)
            x = int(-60 - k * 260); y = int(-180 + k * 40)
            fr.alpha_composite(st_big, (x, y))
            fr.alpha_composite(Image.new('RGBA', (W, H), (30, 20, 10, int(70 * (1 - k * 0.5)))))
            fr.alpha_composite(hero, (W // 2 - 90, 330))
            a = fio(t, 14.2, 21.2, 0.6)
            fr.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * (1 - a)))))
            text(fr, '역관 집안의 아들, 스물여섯 살 윤재', 90, 32, fio(t, 14.6, 20.8))
        elif t < 35.2:
            k = (t - 21.2) / (14.0 / 6)
            idx = min(5, int(k)); kk = k - idx
            im, cap = shot_imgs[idx]
            sc = 0.82 + kk * 0.05
            im2 = im.resize((int(780 * sc), int(596 * sc)), Image.LANCZOS)
            frame = Image.new('RGBA', (im2.width + 24, im2.height + 64), (240, 228, 200, 255)); frame.alpha_composite(im2, (12, 12))
            d = ImageDraw.Draw(frame); d.text((frame.width / 2, im2.height + 38), cap, font=F(24, 'serif'), fill=(60, 40, 24), anchor='mm')
            rot = frame.rotate(-2 + idx * 0.9, expand=True, resample=Image.BICUBIC)
            a = min(1, kk / 0.18) * (1 if kk < 0.85 else (1 - (kk - 0.85) / 0.15))
            rot.putalpha(rot.split()[3].point(lambda v: int(v * a)))
            fr.alpha_composite(rot, ((W - rot.width) // 2, (H - rot.height) // 2))
        else:
            text(fr, '일기 한 권을 펼칠 때마다,', H / 2 - 150, 30, fio(t, 35.4, 39.4))
            text(fr, '그날의 조선이 눈앞에 살아난다.', H / 2 - 104, 30, fio(t, 36.2, 39.4))
            a = ease(seg(t, 39.0, 40.5))
            text(fr, '척화비 아래에서', H / 2 + 10, 76, a, col=(250, 236, 200))
            text(fr, '흥선대원군에서 임오군란까지 · 1863 – 1882', H / 2 + 92, 32, a, col=(220, 196, 150))
            fr.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * ease(seg(t, 42.6, 44.0))))))
        g = grain[i % 4]
        fr.paste(Image.new('RGBA', (W, H), (140, 110, 80, 255)), (0, 0), g.point(lambda v: max(0, v - 128) // 7))
        fr.convert('RGB').save(os.path.join(tmp, 'f%05d.png' % i))
    trk = MU.Track(DUR)
    music = MU.kr_title()
    fade = np.clip(np.minimum(np.arange(len(music)) / (MU.SR * 3), 1), 0, 1)
    m = music[:int(MU.SR * DUR)] * 0.85
    m[:len(fade)] *= fade[:len(m)]
    trk.add(m, 0.0)
    for k in range(6): trk.add(MU.se_paper() * 0.5, 21.2 + k * 14.0 / 6)
    out = trk.render(0.2, loop=False)
    end = int(MU.SR * (DUR - 1.5)); out[end:] *= np.linspace(1, 0, len(out) - end)
    wav = os.path.join(tmp, 'a.wav'); MU.save(wav, out)
    md = os.path.join(root, 'movies'); os.makedirs(md, exist_ok=True)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(tmp, 'f%05d.png'), '-i', wav,
                    '-c:v', 'libvpx', '-b:v', '2.2M', '-crf', '10', '-c:a', 'libvorbis', '-q:a', '4', '-shortest', os.path.join(md, 'Kr_Intro.webm')], check=True)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(tmp, 'f%05d.png'), '-i', wav,
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-shortest',
                    os.path.join(md, 'Kr_Intro.mp4')], check=True)
    shutil.rmtree(tmp)
    print('intro ok')

if __name__ == '__main__':
    build(sys.argv[1])
