"""척화비 아래에서 타이틀 화면 (img/titles1/Kr_Title.png, 1392x624 + 화면 너비에 맞춰 놓는 조각들)
 노을 진 한양 기와지붕과 바다 건너 증기선, 가운데 제목 판, 왼쪽 척화비 · 오른쪽 일기책, 아래 그 시대 사람들
"""
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from k_common import F
from hd_art import sh, mix
import k_mg as MG

def outlined(d, xy, text, font, fill, ol=(30, 18, 8), w=5, anchor='mm'):
    d.text(xy, text, font=font, fill=fill, anchor=anchor, stroke_width=w, stroke_fill=ol)

def title_image(root, W=1392, H=624):
    bg = Image.new('RGBA', (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(bg)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=mix((60, 50, 90), (236, 150, 90), min(1, t * 1.4)) if t < 0.7 else mix((236, 150, 90), (90, 60, 50), (t - 0.7) / 0.3))
    d.ellipse([W * 0.68, H * 0.36, W * 0.68 + 90, H * 0.36 + 90], fill=(255, 210, 140))
    MG.granite_mts(bg, int(H * 0.62), seed=5, col=(90, 70, 80), height=150, peaks=((0.25, 1.0), (0.5, 0.6)))
    d = ImageDraw.Draw(bg)
    MG.sea(bg, int(H * 0.6), int(H * 0.72), (150, 110, 110), (110, 80, 90))
    MG.us_ship(bg, int(W * 0.84), int(H * 0.6) + 6, 0.8, col=(40, 30, 36))
    rnd = random.Random(3)
    for k in range(9):                       # 기와지붕 실루엣
        x0 = -40 + k * 170 + rnd.randint(-20, 20); w_ = rnd.randint(150, 220); yb = int(H * 0.86) + rnd.randint(-10, 20)
        dd = ImageDraw.Draw(bg)
        dd.rectangle([x0 + 10, yb - 10, x0 + w_ - 10, H], fill=(40, 26, 30))
        MG.giwa_roof(dd, x0 + 10, x0 + w_ - 10, yb - 60, yb - 14, (34, 24, 30))
    vig = Image.new('L', (W, H), 0); ImageDraw.Draw(vig).ellipse([-200, -160, W + 200, H + 220], fill=255)
    vig = ImageOps.invert(vig.filter(ImageFilter.GaussianBlur(120)))
    bg.paste(Image.new('RGBA', (W, H), (10, 8, 6, 255)), (0, 0), vig.point(lambda v: int(v * 0.8)))
    d = ImageDraw.Draw(bg)
    # 제목 판 (한지 · 단청 띠)
    d.rounded_rectangle([W / 2 - 360, 56, W / 2 + 360, 296], 18, fill=(34, 26, 22, 220), outline=(222, 190, 120), width=3)
    for k, x in enumerate(range(int(W / 2 - 340), int(W / 2 + 340), 20)):
        for y0 in (66, 280):
            d.rectangle([x, y0, x + 9, y0 + 6], fill=(60, 130, 110)); d.rectangle([x + 10, y0, x + 19, y0 + 6], fill=(170, 60, 50) if k % 2 else (60, 90, 150))
    tsz = 72
    while d.textlength('척화비 아래에서', font=F(tsz, 'serif')) + 12 > 600: tsz -= 2
    outlined(d, (W / 2, 146), '척화비 아래에서', F(tsz, 'serif'), (250, 238, 210), w=6)
    outlined(d, (W / 2, 214), '흥선대원군에서 임오군란까지 · 1863 – 1882', F(27, 'serif'), (230, 200, 140), w=4)
    outlined(d, (W / 2, 254), '역관 윤재가 읽은 아버지의 일기 · 개항기 1편', F(19), (240, 232, 214), w=3)
    os.makedirs(os.path.join(root, 'img/titles1'), exist_ok=True)
    # ---- 화면 너비에 맞춰 놓는 조각들
    st = Image.new('RGBA', (120, 300), (0, 0, 0, 0)); sd = ImageDraw.Draw(st)      # 척화비
    sd.rectangle([10, 262, 110, 296], fill=(150, 146, 136)); sd.rectangle([22, 60, 98, 266], fill=(184, 180, 170))
    sd.polygon([(8, 62), (112, 62), (96, 34), (24, 34)], fill=(130, 126, 118)); sd.rectangle([40, 20, 80, 36], fill=(120, 116, 108))
    for j, col in enumerate(('洋夷侵犯', '非戰則和', '主和賣國')):
        for k, ch in enumerate(col): sd.text((82 - j * 22, 84 + k * 44), ch, font=F(20, 'serif'), fill=(70, 66, 60), anchor='mm')
    st.save(os.path.join(root, 'img/titles1/Kr_TitleStele.png'))
    bk = Image.new('RGBA', (150, 190), (0, 0, 0, 0)); bd = ImageDraw.Draw(bk)          # 일기책
    for k in range(3):
        x = 10 + k * 12; y = 30 - k * 10
        bd.rectangle([x, y, x + 110, y + 150], fill=[(70, 60, 90), (60, 80, 120), (140, 60, 50)][k], outline=(30, 24, 20), width=2)
        for yy in (y + 20, y + 60, y + 100, y + 140): bd.line([(x + 4, yy), (x + 8, yy)], fill=(230, 220, 200), width=3)
    bd.rectangle([60, 30, 120, 120], fill=(244, 236, 214)); bd.text((90, 56), '譯官', font=F(16, 'serif'), fill=(40, 30, 26), anchor='mm'); bd.text((90, 86), '日記', font=F(16, 'serif'), fill=(40, 30, 26), anchor='mm')
    bk.save(os.path.join(root, 'img/titles1/Kr_TitleBook.png'))
    people = ['$k_yunjae10', '$k_father', '$k_daewongun', '$k_overseer', '$k_yanghs', '$k_eojaeyeon', '$k_sinheon', '$k_kuroda', '$k_choi_ik', '$k_kimhongjip',
              '$k_byeolgigun', '$k_imansun', '$k_kimchunyoung', '$k_yunhee23', '$k_parkyounghyo', '$k_yunjae26']
    n = len(people); gap = 76
    strip = Image.new('RGBA', (gap * n + 66, 58 * 3), (0, 0, 0, 0))
    for k, p in enumerate(people):
        sh_ = Image.open(os.path.join(root, 'img/characters', p + '.png')).convert('RGBA')
        fw, fh = sh_.width // 3, sh_.height // 4
        fr = sh_.crop((fw, 0, fw * 2, fh)).resize((fw * 3, fh * 3), Image.NEAREST)
        strip.alpha_composite(fr, (int(33 + gap * k + gap / 2 - fw * 1.5), 0))
    strip = strip.crop(strip.getbbox())
    strip.save(os.path.join(root, 'img/titles1/Kr_TitlePeople.png'))
    bg.convert('RGB').save(os.path.join(root, 'img/titles1/Kr_Title.png'))

if __name__ == '__main__':
    title_image(sys.argv[1]); print('title ok')
