"""척화비 아래에서 · 확대 그림(카드) 만들기 -> img/pictures
 python k_cards.py <프로젝트 폴더>
 지도: historical-basemaps (Ourednik, GPL-3.0) 1880년 국경 자료
 '실제 사진 자리' 그림(kc_photo_*)은 tools_kr/photos/<이름>.png 가 있으면 그 사진으로, 없으면 예시 그림으로 만든다.
"""
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import k_cards_base as B
from k_cards_base import paper, wrap, text_block, title, tag, footnote, card, CW, CH, INK, RED, BLUE, F, sh, mix, outline
import k_geo as GEO

def S(im, name): B.S(im, name)
HANJI = (240, 230, 206)

# ==================================================================== 안내
def cards_intro():
    card('kc_rules', '『척화비 아래에서』를 시작하기 전에', [
        '주인공 윤재와 아버지(역관) · 어머니 · 누이 윤희, 공사장과 장터 사람들은 이야기를 위해 꾸민 인물이에요.',
        '흥선대원군 · 양헌수 · 어재연 · 박규수 · 신헌 · 구로다 · 오경석 · 최익현 · 김홍집 · 호리모토 · 이만손 · 김춘영 · 박영효 · 김옥균은 실존 인물이고, 말은 기록을 바탕으로 쉽게 풀었어요.',
        '아버지의 일기는 주제별로 묶여 있어서, 1장(1867년)보다 2장 첫머리(1866년)가 한 해 앞선 일이에요.',
        '같은 일을 여러 사람의 눈으로 보여 줘요. 전투 장면은 잔인하게 그리지 않았어요.'], label='알림', size=17)
    card('kc_controls', '이렇게 해요', [
        '방향키 · 화면 누르기: 걷기    Enter · Space · 클릭: 앞에 있는 사람 · 물건 조사',
        '머리 위 노란 \'!\': 지금 목표에서 찾아갈 곳',
        '오른쪽 위 [가방]: 모은 사료 카드 다시 보기    [힌트]: 막힐 때',
        '퍼즐 창: 틀려도 괜찮아요. 두 번 틀리면 힌트, 세 번 틀리면 정답을 알려 줘요. Esc 로 나중에 하기',
        '처음 시작할 때 1장~5장 가운데 골라 그 장부터 할 수도 있어요.'], label='조작', size=17)

# ==================================================================== 프롤로그
def jokbo():
    im = paper(seed=3); d = ImageDraw.Draw(im)
    tag(d, 24, 18, '족보 사이의 쪽지')
    d.rectangle([60, 70, 470, 400], fill=(246, 238, 216), outline=(150, 120, 80), width=2)
    text_block(d, 84, 96, 360, ['반닫이 번호는', '지금 임금께서', '왕위에 오르신 해다.', '계해년이니라.'], size=28, kind='serif', gap=12)
    d.text((440, 380), '— 아비 씀', font=F(16, 'serif'), fill=(90, 70, 50), anchor='rm')
    x0 = 510
    d.text((x0 + 120, 86), '간지와 서기 (책 뒤쪽 표)', font=F(17), fill=RED, anchor='mm')
    rows = [('신유년', '1861'), ('임술년', '1862'), ('계해년', '?'), ('갑자년', '1864'), ('을축년', '1865'), ('병인년', '1866'), ('정묘년', '1867')]
    for k, (a, b_) in enumerate(rows):
        y = 112 + k * 38
        d.rectangle([x0, y, x0 + 240, y + 32], fill=(250, 246, 232) if b_ != '?' else (255, 236, 190), outline=(170, 140, 100))
        d.text((x0 + 60, y + 16), a, font=F(18, 'serif'), fill=INK, anchor='mm'); d.text((x0 + 180, y + 16), b_, font=F(18), fill=RED if b_ == '?' else INK, anchor='mm')
    footnote(d, '60년마다 돌아오는 간지(갑자 · 을축 …)로 해를 셌어요')
    S(im, 'kc_jokbo')

def diary():
    im = paper(seed=5); d = ImageDraw.Draw(im)
    title(d, '아버지의 통역 일기', sub='스무 해 동안 쓴 다섯 권')
    labels = [('一', '1867', '경복궁 · 장터'), ('二', '1866 ~ 1871', '강화도'), ('三', '1876', '연무당'), ('四', '1881', '하도감'), ('五', '1882', '도봉소')]
    for k, (n, yr, where) in enumerate(labels):
        x = 70 + k * 136; y = 120
        d.rectangle([x, y, x + 112, y + 230], fill=[(140, 60, 50), (60, 80, 120), (90, 110, 80), (120, 90, 60), (70, 60, 90)][k], outline=(40, 30, 24), width=2)
        for yy in (y + 30, y + 80, y + 150, y + 200): d.line([(x + 6, yy), (x + 10, yy)], fill=(230, 220, 200), width=3)
        d.rectangle([x + 24, y + 20, x + 88, y + 140], fill=(244, 236, 214))
        d.text((x + 56, y + 50), n, font=F(30, 'serif'), fill=INK, anchor='mm')
        d.text((x + 56, y + 92), '譯官', font=F(14, 'serif'), fill=INK, anchor='mm'); d.text((x + 56, y + 112), '日記', font=F(14, 'serif'), fill=INK, anchor='mm')
        d.text((x + 56, y + 172), yr, font=F(13), fill=(250, 244, 226), anchor='mm'); d.text((x + 56, y + 196), where, font=F(13), fill=(250, 244, 226), anchor='mm')
    footnote(d, '실로 꿰맨 옛 책(선장본) 모양')
    S(im, 'kc_diary')

# ==================================================================== 1장
def prices():
    im = paper(seed=7); d = ImageDraw.Draw(im)
    tag(d, 24, 18, '장터 물가판 (방)')
    title(d, '쌀 한 말 값 (상평통보 닢)', sub='게임 속 숫자는 흐름을 보여 주려고 꾸민 것')
    data = [('을축년 가을\n(1865)', 15), ('병인년 가을\n(1866)', 22), ('병인년 섣달\n당백전 나옴', 34), ('정묘년 정월\n(1867)', 52), ('정묘년 봄\n(지금)', 70)]
    x0, y0, w, h = 110, 120, 600, 250
    d.line([(x0, y0 + h), (x0 + w, y0 + h)], fill=INK, width=2); d.line([(x0, y0), (x0, y0 + h)], fill=INK, width=2)
    for k, (lb, v) in enumerate(data):
        bx = x0 + 30 + k * 116; bh = v / 75 * (h - 20)
        d.rectangle([bx, y0 + h - bh, bx + 70, y0 + h], fill=(190, 150, 80) if k < 2 else (190, 70, 60), outline=(90, 60, 30))
        d.text((bx + 35, y0 + h - bh - 14), '%d닢' % v, font=F(16), fill=INK, anchor='mm')
        for j, ln in enumerate(lb.split('\n')): d.text((bx + 35, y0 + h + 16 + j * 18), ln, font=F(13), fill=INK, anchor='mm')
    d.line([(x0 + 30 + 2 * 116 - 14, y0), (x0 + 30 + 2 * 116 - 14, y0 + h)], fill=RED, width=2)
    d.text((x0 + 30 + 2 * 116 - 10, y0 + 6), '← 당백전', font=F(14), fill=RED)
    S(im, 'kc_prices')

# ==================================================================== 2장: 척화비 탁본 · 편지
STELE_COLS = ['洋夷侵犯', '非戰則和', '主和賣國']
def stele_rub(w=640, h=360, ink=True):
    """탁본: 먹이 묻은 검은 바탕 + 흰 글자 (오른쪽부터 세로쓰기)"""
    rnd = random.Random(1871)
    im = Image.new('RGB', (w, h), (26, 24, 24) if ink else HANJI)
    d = ImageDraw.Draw(im)
    for _ in range(4000):
        x, y = rnd.randint(0, w - 1), rnd.randint(0, h - 1); c = rnd.randint(18, 52)
        d.point((x, y), fill=(c, c, c))
    f = F(64, 'serif'); fs = F(22, 'serif')
    xs = [w - 120, w - 230, w - 340]
    for x, col in zip(xs, STELE_COLS):
        for k, ch in enumerate(col): d.text((x, 44 + k * 72), ch, font=f, fill=(238, 234, 222), anchor='mm')
    for k, ch in enumerate('戒我萬年子孫'): d.text((w - 440, 40 + k * 32), ch, font=fs, fill=(220, 216, 204), anchor='mm')
    for k, ch in enumerate('丙寅作辛未立'): d.text((w - 480, 40 + k * 32), ch, font=fs, fill=(220, 216, 204), anchor='mm')
    d.rectangle([8, 8, w - 9, h - 9], outline=(60, 58, 56), width=4)
    im = im.filter(ImageFilter.GaussianBlur(0.6))
    return im

def rub_cards():
    S(stele_rub(), 'kc_rub_stele')
    im = paper(seed=9); d = ImageDraw.Draw(im)
    tag(d, 24, 18, '척화비 탁본')
    r = stele_rub(520, 300); im.paste(r, (24, 70))
    text_block(d, 566, 84, 214, ['洋夷侵犯', '서양 오랑캐가 침범하는데', '非戰則和', '싸우지 않으면 화친하는 것이요', '主和賣國', '화친을 주장함은 나라를 파는 것이다'], size=15, gap=4)
    footnote(d, '戒我萬年子孫 우리 만대 자손에게 경계한다 · 丙寅作 辛未立 병인년에 짓고 신미년(1871)에 세운다')
    S(im, 'kc_rub_done')

def letter():
    B.letter('kc_letter', '오라버니께', ['오라버니, 연무당 일은 잘 끝났어요? 장터에서는 일본 배가 들어온다는 소문으로 시끄러워요.',
                                       '쌀을 마음대로 실어 간다던데 정말이에요? 그러면 쌀값이 또 오를 텐데요.',
                                       '어머니는 걱정 말라 하시지만, 저는 당백전 때 생각이 나서 무서워요.'], '누이 윤희 올림', '병자년(1876) 이월')

# ==================================================================== 3장: 조약문
TREATY_BOX = [
    ('제1관', '조선국은 자주의 나라로서 일본국과 평등한 권리를 가진다.', (0.5, 0.235), False),
    ('제7관', '조선의 바다와 섬, 바위를 일본 배가 자유롭게 측량할 수 있다.', (0.27, 0.44), True),
    ('제10관', '개항장에서 일본인이 조선 사람에게 죄를 지으면 일본 관원이 재판한다.', (0.73, 0.44), True),
    ('부록', '개항장에서 일본인은 일본 돈을 쓸 수 있고, 조선 사람도 이를 쓸 수 있다.', (0.27, 0.74), True),
    ('무역 규칙', '쌀과 잡곡을 실어 내가고 들여올 수 있다. (몇 해 동안 관세를 매기지 않음)', (0.73, 0.74), True),
]
def treaty():
    im = paper(seed=11, kind='letter'); d = ImageDraw.Draw(im)
    d.text((CW / 2, 30), '朝日修好條規 · 조일 수호 조규 (강화도 조약, 1876)', font=F(22, 'serif'), fill=INK, anchor='mm')
    d.line([(40, 50), (CW - 40, 50)], fill=(150, 120, 80), width=2)
    for (h, t, (cx, cy), _) in TREATY_BOX:
        bw = 680 if h == '제1관' else 360; bh = 80 if h == '제1관' else 104
        x0 = cx * CW - bw / 2; y0 = cy * CH - bh / 2
        d.rectangle([x0, y0, x0 + bw, y0 + bh], fill=(250, 246, 234), outline=(140, 110, 80), width=2)
        d.text((x0 + 12, y0 + 10), h, font=F(18, 'serif'), fill=RED)
        text_block(d, x0 + 12, y0 + 34, bw - 24, t, size=17, gap=3)
    d.text((CW - 46, CH - 26), '(쉽게 풀어 옮김)', font=F(13, 'reg'), fill=(120, 100, 80), anchor='rm')
    S(im, 'kc_treaty')

# ==================================================================== 4장: 『조선책략』 지도
CH_MARKS = None
def chmap():
    global CH_MARKS
    W_, H_ = 800, 450
    box = (100, 160, 18, 60)
    def col(p, o):
        n = (p.get('NAME') or '')
        if o == 'ru': return (196, 196, 204)
        if o == 'jp': return (236, 214, 190)
        if o == 'qing': return (236, 222, 170)
        if 'Korea' in n: return (210, 236, 200)
        if o == 'us': return (200, 214, 236)
        return (226, 220, 206)
    mp, pj = GEO.render(1880, box, (W_, H_), colors=col, line_w=0.6, seed=5, paper=False)
    mp = mp.convert('RGBA'); d = ImageDraw.Draw(mp)
    for (lo, la, t, sz) in ((127.3, 37.8, '조선', 20), (113, 40, '청', 22), (141.2, 39.6, '일본', 20), (128, 54, '러시아', 22)):
        x, y = pj(lo, la); d.text((x, y), t, font=F(sz), fill=(40, 30, 24), anchor='mm', stroke_width=3, stroke_fill=(250, 244, 226))
    d.rounded_rectangle([W_ - 150, H_ - 122, W_ - 10, H_ - 20], 10, fill=(214, 226, 244), outline=(80, 100, 140), width=2)
    d.text((W_ - 80, H_ - 104), '미국', font=F(20), fill=(30, 40, 70), anchor='mm'); d.text((W_ - 80, H_ - 82), '(태평양 건너)', font=F(13), fill=(30, 40, 70), anchor='mm')
    d.line([(W_ - 200, H_ - 70), (W_ - 155, H_ - 70)], fill=(80, 100, 140), width=3); d.polygon([(W_ - 155, H_ - 76), (W_ - 155, H_ - 64), (W_ - 146, H_ - 70)], fill=(80, 100, 140))
    d.text((20, H_ - 20), '1880년 무렵 · 황준헌 『조선책략』의 생각', font=F(14), fill=(60, 50, 40), stroke_width=2, stroke_fill=(250, 244, 226))
    marks = {}
    for k, (lo, la) in (('청', (113, 36.5)), ('일본', (138.0, 35.0)), ('러시아', (128, 50.5))):
        x, y = pj(lo, la); marks[k] = (round(x / W_, 3), round(y / H_, 3))
    marks['미국'] = (round((W_ - 80) / W_, 3), round((H_ - 40) / H_, 3))
    CH_MARKS = marks
    S(mp, 'kc_chmap')
    print('  조선책략 지도 표시 자리:', marks)

# ==================================================================== 5장: 한양 지도 (소문 지도)
HY_PLACES = {'선혜청': (0.48, 0.80), '운현궁': (0.42, 0.42), '일본 공사관': (0.13, 0.55), '창덕궁': (0.70, 0.28)}
def hanyang():
    W_ = H_ = 600
    im = Image.new('RGBA', (W_, H_), (232, 222, 190, 255)); d = ImageDraw.Draw(im)
    rnd = random.Random(1882)
    for _ in range(3000):
        x, y = rnd.randint(0, W_ - 1), rnd.randint(0, H_ - 1); d.point((x, y), fill=sh((232, 222, 190), 0.94 + rnd.random() * 0.08))
    # 산
    for (cx, cy, r, nm) in ((300, 70, 70, '북악산'), (110, 200, 60, '인왕산'), (320, 560, 70, '남산'), (520, 230, 50, '낙산')):
        for k in range(5): d.polygon([(cx - r + k * r / 2.5, cy + 20), (cx - r * 0.6 + k * r / 2.5, cy - 24), (cx - r * 0.2 + k * r / 2.5, cy + 20)], fill=(150, 170, 130), outline=(110, 130, 96))
        d.text((cx, cy + 34), nm, font=F(14), fill=(80, 90, 70), anchor='mm')
    # 도성 (성곽 고리)
    ring = [(300, 110), (420, 140), (500, 240), (510, 380), (430, 500), (300, 520), (170, 480), (110, 360), (130, 230), (200, 140)]
    d.line(ring + [ring[0]], fill=(120, 110, 96), width=6)
    for (x, y, nm) in ((500, 300, '흥인지문'), (300, 520, '숭례문'), (122, 300, '돈의문(서대문)'), (300, 112, '숙정문')):
        d.rectangle([x - 10, y - 10, x + 10, y + 10], fill=(170, 60, 50)); d.text((x, y + 22), nm, font=F(12), fill=INK, anchor='mm')
    # 청계천 · 종로
    d.line([(140, 330), (260, 340), (380, 330), (500, 340)], fill=(110, 150, 190), width=5); d.text((450, 356), '청계천', font=F(12), fill=(60, 90, 130), anchor='mm')
    d.line([(150, 290), (500, 290)], fill=(190, 170, 130), width=8); d.text((330, 280), '종로', font=F(13), fill=INK, anchor='mm')
    # 궁궐 · 장소
    d.rectangle([220, 140, 300, 220], fill=(214, 180, 140), outline=(140, 100, 60), width=2); d.text((260, 180), '경복궁', font=F(14), fill=INK, anchor='mm')
    for nm, (rx, ry) in HY_PLACES.items():
        x, y = rx * W_, ry * H_
        d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(190, 50, 40), outline=(255, 250, 240), width=2)
    d.text((14, H_ - 22), '1882년 한양 (간략한 그림)', font=F(13), fill=(90, 80, 60))
    S(im, 'kc_hanyang')

# ==================================================================== 사진 자리
def photo_slot(name, head, what, draw, desc=None):
    ph = os.path.join(HERE, 'photos', name.replace('kc_photo_', '') + '.png')
    if os.path.exists(ph):
        src = Image.open(ph).convert('RGB'); AH = CH - 40
        if src.height > src.width * 1.1:          # 세로로 긴 사진: 왼쪽에 크게, 오른쪽에 설명
            im = Image.new('RGB', (CW, CH), (30, 26, 24))
            bg = ImageEnhance.Brightness(ImageOps.fit(src, (CW, CH)).filter(ImageFilter.GaussianBlur(22))).enhance(0.3); im.paste(bg, (0, 0))
            k = (CH - 20) / src.height; fg = src.resize((max(1, int(src.width * k)), CH - 20), Image.LANCZOS)
            px = 40; im.paste(fg, (px, 10))
            d = ImageDraw.Draw(im); x0 = px + fg.width + 30; tw = CW - x0 - 30
            d.rectangle([x0 - 12, 0, CW, CH], fill=(30, 26, 24))
            lines, cur = [], ''
            for w in head.replace(' (', '\n(').split('\n'):
                lines.append(w)
            fs = 26
            while fs > 14 and max(d.textlength(l, font=F(fs)) for l in lines) > tw: fs -= 1
            y = (60 if desc else CH / 2 - (len(lines) * (fs + 12)) / 2)
            for i, l in enumerate(lines):
                d.text((x0, y), l, font=F(fs if i == 0 else max(14, fs - 6)), fill=(250, 240, 220) if i == 0 else (214, 200, 176)); y += fs + 14
            if desc:
                y += 10; d.line([(x0, y), (x0 + 60, y)], fill=(200, 160, 90), width=2); y += 18
                for para in desc:
                    cur = ''
                    for wd in para.split(' '):
                        t_ = (cur + ' ' + wd) if cur else wd
                        if cur and d.textlength(t_, font=F(17)) > tw: d.text((x0, y), cur, font=F(17), fill=(232, 222, 204)); y += 26; cur = wd
                        else: cur = t_
                    if cur: d.text((x0, y), cur, font=F(17), fill=(232, 222, 204)); y += 26
                    y += 8
            S(im, name); return
        bg = ImageEnhance.Brightness(ImageOps.fit(src, (CW, AH)).filter(ImageFilter.GaussianBlur(18))).enhance(0.35)
        im = Image.new('RGB', (CW, CH), (24, 20, 18)); im.paste(bg, (0, 0))
        k = min((CW - 16) / src.width, (AH - 12) / src.height); fg = src.resize((max(1, int(src.width * k)), max(1, int(src.height * k))), Image.LANCZOS)
        im.paste(fg, ((CW - fg.width) // 2, (AH - fg.height) // 2))
        d = ImageDraw.Draw(im); d.rectangle([0, AH, CW, CH], fill=(30, 26, 24))
        d.text((CW / 2, AH + 20), head, font=F(20), fill=(250, 240, 220), anchor='mm')
        S(im, name); return
    im = Image.new('RGB', (CW, CH), (60, 56, 52)); d = ImageDraw.Draw(im)
    draw(im, d)
    d.rectangle([0, CH - 52, CW, CH], fill=(30, 26, 24))
    d.text((CW / 2, CH - 36), head, font=F(18), fill=(250, 240, 220), anchor='mm')
    d.text((CW / 2, CH - 14), '예시 그림 · 실제 사진을 img/pictures/%s.png 로 넣으면 바뀌어요 (%s)' % (name, what), font=F(12), fill=(200, 190, 170), anchor='mm')
    S(im, name)

# ==================================================================== 오페르트 도굴 사건 (1868) · 어두운 밤 그림
def oppert():
    W_, H_ = CW, CH; rnd = random.Random(1868)
    im = Image.new('RGB', (W_, H_), (14, 18, 34)); d = ImageDraw.Draw(im)
    for y in range(H_):                                   # 밤하늘
        t = y / H_; d.line([(0, y), (W_, y)], fill=mix((10, 14, 30), (34, 40, 62), t))
    for _ in range(70):
        x, y = rnd.randrange(W_), rnd.randrange(0, 200); c = rnd.choice([(200, 206, 230), (150, 160, 190)])
        d.point((x, y), fill=c)
    d.ellipse([640, 36, 692, 88], fill=(236, 230, 200)); d.ellipse([652, 32, 702, 82], fill=(18, 22, 40))   # 초승달
    d.polygon([(0, 250), (120, 150), (210, 200), (330, 110), (450, 190), (560, 140), (680, 210), (800, 170), (800, 450), (0, 450)], fill=(26, 32, 44))  # 가야산
    d.polygon([(0, 300), (180, 250), (380, 280), (560, 240), (800, 280), (800, 450), (0, 450)], fill=(32, 40, 40))
    d.rectangle([0, 360, 800, 450], fill=(24, 30, 30))
    d.polygon([(470, 340), (800, 322), (800, 372), (520, 372)], fill=(30, 46, 66))                       # 삽교천 물줄기
    for k in range(7): d.line([(540 + k * 36, 350 + (k % 2) * 8), (566 + k * 36, 350 + (k % 2) * 8)], fill=(70, 96, 120))
    sx, sy = 640, 322                                       # 강에 숨겨 둔 증기선 그림자
    d.polygon([(sx, sy + 12), (sx + 120, sy + 12), (sx + 108, sy + 26), (sx + 10, sy + 26)], fill=(10, 12, 16))
    d.rectangle([sx + 50, sy - 14, sx + 60, sy + 12], fill=(10, 12, 16)); d.line([(sx + 30, sy - 40), (sx + 30, sy + 12)], fill=(10, 12, 16), width=2)
    d.line([(sx + 90, sy - 34), (sx + 90, sy + 12)], fill=(10, 12, 16), width=2)
    for k in range(5): d.ellipse([sx + 44 - k * 9, sy - 30 - k * 12, sx + 64 - k * 7, sy - 16 - k * 12], fill=(54, 58, 70))
    # 무덤 (봉분) + 망주석 · 상석
    d.ellipse([170, 250, 410, 380], fill=(52, 70, 44)); d.ellipse([180, 256, 400, 372], outline=(70, 92, 58), width=2)
    d.chord([170, 250, 410, 380], 180, 360, fill=(58, 78, 48))
    d.rectangle([250, 352, 330, 372], fill=(120, 120, 112)); d.rectangle([254, 348, 326, 354], fill=(140, 140, 130))
    for x in (150, 430):
        d.rectangle([x - 5, 300, x + 5, 380], fill=(130, 130, 122)); d.ellipse([x - 9, 286, x + 9, 304], fill=(140, 140, 132))
    # 파다 만 자리 (단단한 석회층) - 흰빛 덩어리
    d.polygon([(232, 300), (300, 290), (346, 306), (330, 330), (250, 328)], fill=(40, 34, 28))
    d.polygon([(256, 312), (310, 304), (330, 316), (300, 324), (262, 322)], fill=(206, 204, 190))
    # 등불을 든 그림자들 (얼굴 없이 실루엣만)
    def man(x, y, tool=None, lamp=False):
        d.ellipse([x - 7, y - 46, x + 7, y - 32], fill=(8, 10, 14)); d.polygon([(x - 10, y - 32), (x + 10, y - 32), (x + 12, y), (x - 12, y)], fill=(8, 10, 14))
        d.ellipse([x - 9, y - 52, x + 9, y - 42], fill=(8, 10, 14))
        if tool: d.line([(x + 8, y - 26), (x + 26, y + 2)], fill=(8, 10, 14), width=3); d.polygon([(x + 22, y), (x + 32, y - 2), (x + 30, y + 8)], fill=(8, 10, 14))
        if lamp:
            for r, a in ((34, 40), (22, 80), (12, 140)):
                g = Image.new('L', (W_, H_), 0); ImageDraw.Draw(g).ellipse([x - 22 - r, y - 30 - r, x - 22 + r, y - 30 + r], fill=a)
                g = g.filter(ImageFilter.GaussianBlur(10)); im.paste((255, 196, 110), (0, 0), g)
            d.line([(x - 8, y - 28), (x - 22, y - 36)], fill=(8, 10, 14), width=2); d.rectangle([x - 26, y - 36, x - 18, y - 24], fill=(255, 210, 130))
    man(220, 320, tool=True); man(360, 316, tool=True); man(460, 340, lamp=True)
    d = ImageDraw.Draw(im)
    d.rectangle([0, H_ - 40, W_, H_], fill=(14, 12, 12))
    d.text((W_ / 2, H_ - 20), '1868년 · 남연군 묘 도굴 미수 (오페르트 도굴 사건) · 이해를 돕는 그림', font=F(17), fill=(236, 226, 206), anchor='mm')
    S(im, 'kc_oppert')

def photos():
    def uigwe(im, d):
        d.rectangle([0, 0, CW, CH - 52], fill=(222, 210, 180))
        d.rectangle([60, 30, 740, 370], fill=(244, 236, 214), outline=(150, 120, 80), width=3)
        for k in range(14):                      # 반차도 행렬
            x = 90 + k * 46
            d.ellipse([x, 160, x + 20, 180], fill=(236, 210, 170)); d.rectangle([x + 2, 180, x + 18, 220], fill=[(170, 50, 50), (60, 90, 150), (90, 120, 80)][k % 3])
            d.ellipse([x - 2, 150, x + 22, 162], fill=(40, 34, 30))
        d.rectangle([380, 240, 460, 300], fill=(190, 60, 50), outline=(110, 40, 30), width=2)
        d.text((400, 70), '儀軌 · 의궤 (왕실 행사 기록 · 반차도)', font=F(22, 'serif'), fill=INK, anchor='mm')
    def sujagi(im, d):
        d.rectangle([0, 0, CW, CH - 52], fill=(70, 70, 76))
        d.polygon([(220, 40), (600, 50), (590, 360), (230, 350)], fill=(214, 190, 120))
        d.rectangle([220, 40, 600, 70], fill=(170, 40, 40))
        d.text((410, 210), '帥', font=F(180, 'serif'), fill=(30, 26, 22), anchor='mm')
    def stele(im, d):
        d.rectangle([0, 0, CW, CH - 52], fill=(170, 196, 214))
        d.rectangle([0, 300, CW, CH - 52], fill=(150, 140, 120))
        d.rectangle([340, 300, 460, 330], fill=(140, 136, 128)); d.rectangle([350, 90, 450, 304], fill=(176, 172, 164))
        d.polygon([(330, 92), (470, 92), (450, 66), (350, 66)], fill=(130, 126, 118))
        for j, col in enumerate(STELE_COLS):
            for k, ch in enumerate(col): d.text((430 - j * 30, 120 + k * 42), ch, font=F(26, 'serif'), fill=(70, 66, 60), anchor='mm')
    def byeol(im, d):
        d.rectangle([0, 0, CW, CH - 52], fill=(200, 196, 186))
        for k in range(8):
            x = 80 + k * 84
            d.ellipse([x + 10, 120, x + 40, 150], fill=(220, 190, 160)); d.ellipse([x, 104, x + 50, 124], fill=(30, 30, 30)); d.rectangle([x + 18, 92, x + 32, 112], fill=(30, 30, 30))
            d.rectangle([x + 6, 150, x + 44, 260], fill=(60, 80, 66)); d.rectangle([x + 10, 260, x + 40, 340], fill=(60, 80, 66))
            d.line([(x + 46, 330), (x + 46, 140)], fill=(80, 60, 40), width=3)
        d.text((400, 50), '별기군 (1881)', font=F(26), fill=INK, anchor='mm')
    photo_slot('kc_photo_uigwe', '외규장각 의궤 속 행렬 그림(반차도) · 2011년 우리나라로 돌아옴', '의궤 사진', uigwe)
    photo_slot('kc_photo_sujagi', '어재연 장군의 수자기 (2007년 장기 대여로 돌아옴)', '수자기 사진', sujagi)
    photo_slot('kc_photo_cheokhwabi', '척화비 (1871)', '척화비 사진', stele,
               ['洋夷侵犯 非戰則和 主和賣國', '서양 오랑캐가 침범하는데 싸우지 않으면 화친하는 것이요, 화친을 주장하는 것은 나라를 파는 것이다.',
                '戒我萬年子孫 丙寅作 辛未立 (우리 만대 자손에게 경계한다. 병인년에 짓고 신미년에 세운다)'])
    photo_slot('kc_photo_byeolgigun', '별기군 (1881 · 신식 군대)', '별기군 사진', byeol,
               ['1881년, 개화 정책으로 만든 신식 군대.', '일본인 교관 호리모토에게 근대식 훈련을 받았다.',
                '구식 군인보다 대우가 좋아 불만이 쌓였고, 이듬해 임오군란(1882)의 한 원인이 되었다.'])

# ==================================================================== 사료 카드 · 정리
def cards_src():
    card('kc_src_daewon', '흥선대원군의 개혁 정치 (1863~1873)', [
        '배경: 세도 정치로 왕권이 약해지고, 삼정(전정 · 군정 · 환곡)이 문란해 백성이 고통받음',
        '왕권 강화: 비변사 폐지 · 의정부와 삼군부 부활 · 『대전회통』 편찬 · 경복궁 중건 · 인재 고루 등용',
        '민생 안정: 호포제(양반에게도 군포) · 사창제 · 양전 사업 · 서원 정리(47곳만 남김)',
        '한계: 경복궁 공사로 원납전 · 당백전 · 부역 → 물가가 오르고 원망이 커짐'], label='사료 카드', size=17)
    card('kc_src_yangyo', '병인양요와 신미양요 (1866 · 1871)', [
        '병인박해(1866) → 병인양요: 프랑스 함대가 강화도 침략 → 한성근(문수산성) · 양헌수(정족산성)가 물리침, 외규장각 도서 약탈',
        '제너럴셔먼호 사건(1866, 평양) · 오페르트 도굴 사건(1868)',
        '신미양요(1871): 미국 함대가 강화도 침략 → 어재연이 광성보에서 항전, 미군 철수',
        '척화비 건립(1871): 통상 수교 거부 의지를 알림'], label='사료 카드', size=17)
    card('kc_src_treaty', '강화도 조약 (1876 · 조일 수호 조규)', [
        '배경: 대원군이 물러남(1873) · 운요호 사건(1875) · 박규수 등 통상 개화론',
        '내용: 부산 · 원산 · 인천 개항, 해안 측량권, 영사 재판권(치외 법권)',
        '부록 · 무역 규칙: 일본 화폐 사용, 양곡 무제한 유출, 무관세',
        '성격: 우리나라 첫 근대적 조약이자 불평등 조약 · 최익현의 왜양일체론(개항 반대)'], label='사료 카드', size=17)
    card('kc_src_gaehwa', '개화 정책과 위정척사 운동 (1876~1882)', [
        '사절단: 수신사(김기수 1876 · 김홍집 1880, 『조선책략』) · 조사 시찰단(1881) · 영선사(김윤식, 1881 청 톈진)',
        '기구 · 군대: 통리기무아문(1880, 12사) · 별기군(1881) · 5군영을 2영으로',
        '위정척사: 통상 반대(1860년대 이항로 · 기정진) → 개항 반대(1870년대 최익현) → 개화 반대(1880년대 영남 만인소 이만손)',
        '조미 수호 통상 조약(1882): 서양과 맺은 첫 조약 · 거중 조정 · 최혜국 대우'], label='사료 카드', size=16)
    card('kc_src_imo', '임오군란 (1882)', [
        '원인: 구식 군인 차별 · 13개월 밀린 녹봉 · 겨와 모래 섞인 쌀 · 일본으로 곡식이 빠져나가 쌀값 상승',
        '전개: 선혜청 습격 → 도시 빈민 합세 → 일본 공사관 습격 · 궁궐 습격 → 흥선대원군 재집권(별기군 · 통리기무아문 폐지)',
        '결과: 청군 개입 · 대원군 청으로 압송 → 제물포 조약(일본: 배상금 · 공사관 경비병) · 조청 상민 수륙 무역 장정(청: 속방 · 내지 통상)',
        '청의 내정 간섭: 마젠창 · 묄렌도르프 고문 · 군대 주둔'], label='사료 카드', size=16)

def summaries():
    data = [
        ('kc_sum1', '1장 정리 · 흥선대원군의 개혁', ['세도 정치 → 흥선대원군 집권 (1863)', '왕권 강화: 비변사 폐지 · 대전회통 · 경복궁 중건', '민생 안정: 호포제 · 사창제 · 서원 정리 · 한계: 원납전 · 당백전']),
        ('kc_sum2', '2장 정리 · 통상 수교 거부', ['병인박해 → 병인양요(1866): 정족산성 · 외규장각 약탈', '제너럴셔먼호(1866) · 오페르트 도굴(1868)', '신미양요(1871): 광성보 · 척화비 건립']),
        ('kc_sum3', '3장 정리 · 강화도 조약', ['운요호 사건(1875) → 강화도 조약(1876)', '3개 항구 개항 · 해안 측량권 · 영사 재판권', '일본 화폐 · 양곡 유출 · 무관세 → 불평등 조약']),
        ('kc_sum4', '4장 정리 · 개화와 위정척사', ['수신사 · 조사 시찰단 · 영선사 · 『조선책략』', '통리기무아문 · 별기군 · 조미 수호 통상 조약(1882)', '위정척사: 통상 반대 → 개항 반대 → 개화 반대']),
        ('kc_sum5', '5장 정리 · 임오군란', ['구식 군인 차별 · 밀린 녹봉 → 봉기 (1882)', '대원군 재집권 → 청군 개입 · 대원군 압송', '제물포 조약(일본) · 무역 장정(청) → 청의 내정 간섭']),
    ]
    for (n, h, ls) in data: card(n, h, ls, label='정리', size=20)
    im = paper(seed=91); d = ImageDraw.Draw(im)
    title(d, '척화비 아래에서 한눈에 보기')
    steps = [('1863', '고종 즉위 · 흥선대원군 집권'), ('1865~68', '경복궁 중건 · 당백전'), ('1866', '병인박해 · 병인양요'),
             ('1871', '신미양요 · 척화비'), ('1873 · 1875', '고종 친정 · 운요호 사건'), ('1876', '강화도 조약'),
             ('1880~81', '통리기무아문 · 별기군 · 만인소'), ('1882 봄', '조미 수호 통상 조약'), ('1882 여름', '임오군란 → 청의 간섭')]
    for k, (yr, ev) in enumerate(steps):
        x = 60 + (k % 3) * 236; y = 96 + (k // 3) * 102
        d.rounded_rectangle([x, y, x + 214, y + 80], 10, fill=(250, 244, 228), outline=(150, 120, 80), width=2)
        d.text((x + 14, y + 18), yr, font=F(17), fill=RED, anchor='lm')
        text_block(d, x + 14, y + 34, 190, ev, size=14)
    footnote(d, '→ 2편 「갑신정변」 (1884)으로 이어집니다')
    S(im, 'kc_summary')

def bead():
    im = paper(seed=13); d = ImageDraw.Draw(im)
    tag(d, 24, 18, '아버지의 선물')
    for k in range(9):
        x = 200 + k * 46; y = 220 + int(30 * math.sin(k / 8 * math.pi))
        d.ellipse([x, y, x + 40, y + 40], fill=(214, 140, 50), outline=(140, 80, 30), width=2); d.ellipse([x + 8, y + 6, x + 18, y + 14], fill=(250, 210, 140))
    d.line([(160, 200), (200, 236)], fill=(40, 34, 30), width=3); d.line([(614, 236), (650, 200)], fill=(40, 34, 30), width=3)
    text_block(d, 120, 320, 560, '갓끈에 꿰던 호박 구슬. "보태지도 빼지도 말고, 우리 말을 똑바로 전하거라."', size=18)
    S(im, 'kc_bead')

def icons():
    def ic(name, fn):
        im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im); fn(d, im); S(outline(im, 0.5), name)
    def book(d, im):
        d.rectangle([14, 8, 50, 56], fill=(140, 60, 50)); d.rectangle([22, 14, 42, 40], fill=(244, 236, 214))
        for yy in (14, 26, 38, 50): d.line([(14, yy), (18, yy)], fill=(240, 230, 210), width=2)
    def rub(d, im):
        d.rectangle([10, 8, 54, 56], fill=(30, 28, 28))
        for k, x in enumerate((44, 32, 20)):
            for j in range(4): d.rectangle([x - 3, 14 + j * 10, x + 3, 20 + j * 10], fill=(236, 232, 220))
    def beadi(d, im):
        for k in range(5): d.ellipse([6 + k * 10, 24 + int(6 * math.sin(k)), 18 + k * 10, 36 + int(6 * math.sin(k))], fill=(214, 140, 50), outline=(140, 80, 30))
    def cardi(d, im):
        d.rectangle([10, 12, 54, 52], fill=(240, 230, 204)); d.rectangle([10, 12, 54, 20], fill=(150, 40, 40))
        for yy in range(26, 48, 6): d.line([(16, yy), (48, yy)], fill=(100, 80, 60))
    for n, fn in (('ki_diary', book), ('ki_takbon', rub), ('ki_bead', beadi), ('ki_card', cardi)): ic(n, fn)

def build(root):
    B.ROOT = root; B.OUT = os.path.join(root, 'img', 'pictures'); os.makedirs(B.OUT, exist_ok=True)
    cards_intro(); jokbo(); diary(); prices(); rub_cards(); letter(); treaty(); chmap(); hanyang(); oppert(); photos(); cards_src(); summaries(); bead(); icons()
    B.review_card(name='kc_review')
    print('cards', len([f for f in os.listdir(B.OUT) if f.startswith(('kc_', 'ki_'))]))

if __name__ == '__main__':
    build(sys.argv[1])
