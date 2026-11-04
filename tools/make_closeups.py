"""단서 확대 그림(img/pictures/cu_*.png)과 아이템 아이콘(item_*.png)"""
import os, sys, random, math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
SANS_B = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
SANS_R = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
SERIF_B = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'

def F(sz, kind='r'):
    path = {'r': SANS_R, 'b': SANS_B, 's': SERIF_B}[kind]
    return ImageFont.truetype(path, sz, index=1)

CW, CH = 640, 360
INK = (52, 36, 26)
RED = (170, 40, 36)

def parchment(title=None, w=CW, h=CH, base=(236, 222, 188)):
    im = Image.new('RGB', (w, h), base)
    d = ImageDraw.Draw(im)
    rnd = random.Random(w * h + len(title or ''))
    for _ in range(2500):
        x, y = rnd.randrange(w), rnd.randrange(h)
        c = tuple(max(0, v - rnd.randint(0, 18)) for v in base)
        d.point((x, y), fill=c)
    d.rectangle([6, 6, w - 7, h - 7], outline=(120, 84, 50), width=4)
    d.rectangle([14, 14, w - 15, h - 15], outline=(170, 130, 90), width=1)
    if title:
        d.text((w // 2, 40), title, font=F(28, 's'), fill=INK, anchor='mm')
        d.line([w // 2 - 120, 62, w // 2 + 120, 62], fill=(150, 110, 70), width=2)
    return im, d

def wrap(d, text, font, maxw):
    lines = []
    for para in text.split('\n'):
        line = ''
        for ch in para:
            if d.textlength(line + ch, font=font) > maxw and line:
                lines.append(line); line = ch
            else:
                line += ch
        lines.append(line)
    return lines

def text_block(d, x, y, text, size=20, maxw=560, gap=8, color=INK, kind='r'):
    f = F(size, kind)
    for ln in wrap(d, text, f, maxw):
        d.text((x, y), ln, font=f, fill=color)
        y += size + gap
    return y

def save(im, name):
    im.save(os.path.join(OUT, name + '.png'))

# ------------------------------------------------------------------ 규칙 카드
im, d = parchment('방탈출 규칙')
rules = [('8', '방은 모두 8개, 제한 시간 40분'), ('3', '힌트는 게임 전체에서 단 3번!'), ('?', '단서는 서로 이어 맞춰야 풀린다'),
         ('ESC', '가방: 모은 단서 다시 보기 · 힌트')]
y = 92
for k, t in rules:
    d.rounded_rectangle([60, y, 140, y + 50], 10, fill=(170, 40, 36) if k == '3' else (120, 84, 50))
    d.text((100, y + 25), k, font=F(26 if len(k) < 3 else 18, 'b'), fill=(255, 245, 225), anchor='mm')
    d.text((165, y + 25), t, font=F(24, 'b' if k == '3' else 'r'), fill=RED if k == '3' else INK, anchor='lm')
    y += 64
save(im, 'cu_rules')

# ------------------------------------------------------------------ 1. 훈요 10조 병풍
im, d = parchment(None, base=(232, 220, 190))
items = ["나라의 큰일은 부처님의 보살핌 덕분이니, 절을 세우고 불교를 받들어라.",
         "절은 도선이 정한 자리에만 세우고 함부로 더 짓지 말라.",
         "왕위는 맏아들에게 잇게 하되, 어질지 못하면 다른 아들에게 잇게 하라.",
         "중국의 제도를 꼭 따를 필요는 없다. 거란은 짐승 같은 나라이니 그 옷과 제도를 본받지 말라.",
         "서경은 우리나라 땅의 뿌리가 되는 곳이니, 해마다 100일 넘게 머물러라.",
         "연등회와 팔관회를 소홀히 하지 말라.",
         "신하의 바른말을 따르고, 백성의 세금과 부역을 가볍게 하라.",
         None,
         "관리의 녹봉은 나라 형편에 맞게 정하라.",
         "경전과 역사책을 널리 읽어 지난 일을 거울로 삼으라."]
d.text((CW // 2, 30), '훈요 10조', font=F(26, 's'), fill=INK, anchor='mm')
y = 56
for i, t in enumerate(items):
    d.text((34, y), f'{i + 1}.', font=F(16, 'b'), fill=RED)
    if t is None:
        d.rectangle([64, y + 4, 560, y + 18], fill=(200, 188, 160)); d.text((330, y + 11), '(글자가 지워져 읽을 수 없다)', font=F(14), fill=(120, 100, 80), anchor='mm')
        y += 28
    else:
        for ln in wrap(d, t, F(16), 556):
            d.text((64, y), ln, font=F(16), fill=INK); y += 22
        y += 5
save(im, 'cu_hunyo')

# ------------------------------------------------------------------ 1. 태조의 쪽지
im, d = parchment('태조의 쪽지')
y = text_block(d, 50, 90, "보물함은 나의 가르침 세 가지로 열린다.", 22)
y = text_block(d, 70, y + 10, "하나. 북쪽으로 나아갈 발판이 될 도시를 아끼라는 가르침\n둘. 부처의 힘에 기대라는 가르침\n셋. 북쪽 오랑캐의 풍속을 따르지 말라는 가르침", 20, 520, 12)
text_block(d, 50, y + 14, "각 가르침이 몇 번째 조항인지 이 차례대로 맞추어라.", 20, 540, 8, RED)
save(im, 'cu_desk_note')

# ------------------------------------------------------------------ 1. 북방 지도
im, d = parchment('북방 지도', base=(228, 216, 180))
d.polygon([(200, 330), (180, 260), (210, 200), (190, 150), (240, 110), (330, 95), (420, 80), (470, 110), (430, 170), (440, 230), (400, 290), (360, 340)], fill=(186, 200, 150), outline=(110, 120, 80))
d.line([(240, 112), (300, 98), (360, 92), (430, 82)], fill=(80, 120, 190), width=4)
d.text((470, 72), '압록강', font=F(16, 'b'), fill=(60, 90, 160))
d.rectangle([80, 70, 600, 76], fill=None)
d.text((450, 100), '북쪽: 거란', font=F(20, 'b'), fill=(120, 60, 40))
for (x, y, name, sub, c) in [(268, 196, '서경(평양)', '고구려의 옛 도읍\n북쪽으로 나아갈 발판', RED), (330, 280, '개경', '고려의 도읍', INK)]:
    d.ellipse([x - 7, y - 7, x + 7, y + 7], fill=c)
    d.text((x + 14, y - 12), name, font=F(20, 'b'), fill=c)
    d.text((x + 14, y + 12), sub, font=F(15), fill=INK)
d.line([(330, 270), (285, 210)], fill=RED, width=3)
d.polygon([(285, 210), (284, 224), (296, 218)], fill=RED)
d.text((110, 300), '↑ 북진', font=F(18, 'b'), fill=RED)
save(im, 'cu_map_north')

# ------------------------------------------------------------------ 1. 서경 가는 길 (격자)
im, d = parchment('서경 가는 길')
G, ox, oy = 52, 190, 80
mount = {(2, 3), (3, 1), (2, 1)}
for r in range(5):
    for c in range(5):
        x, y = ox + c * G, oy + r * G
        d.rectangle([x, y, x + G, y + G], outline=(150, 120, 80), width=1, fill=(226, 214, 176))
        if (c, r) in mount:
            d.polygon([(x + 8, y + G - 8), (x + G // 2, y + 8), (x + G - 8, y + G - 8)], fill=(120, 110, 90), outline=INK)
            d.polygon([(x + G // 2 - 6, y + 18), (x + G // 2, y + 8), (x + G // 2 + 6, y + 18)], fill=(240, 240, 240))
def mark(c, r, label, col):
    x, y = ox + c * G + G // 2, oy + r * G + G // 2
    d.ellipse([x - 13, y - 13, x + 13, y + 13], fill=col, outline=INK)
    d.text((x, y), label, font=F(15, 'b'), fill=(255, 250, 240), anchor='mm')
mark(3, 3, '개경', (60, 90, 150)); mark(1, 1, '서경', RED)
d.text((ox + 5 * G + 30, oy + 10), '↑ 북', font=F(22, 'b'), fill=INK)
d.polygon([(ox + 5 * G + 40, oy + 50), (ox + 5 * G + 52, oy + 74), (ox + 5 * G + 28, oy + 74)], fill=INK)
text_block(d, 34, 100, "▲ = 산\n지날 수 없다", 18, 140)
text_block(d, 34, 250, "개경에서 서경까지\n한 칸씩 네 번\n움직여라.", 18, 150)
save(im, 'cu_route')

# ------------------------------------------------------------------ 2. 한자 공부 표
im, d = parchment('한자 공부 표')
hanja = [('陶', '질그릇 도'), ('器', '그릇 기'), ('色', '빛 색'), ('之', '~의 / ~을 지'), ('靑', '푸를 청'),
         ('者', '것 자'), ('麗', '고울 려 (고려)'), ('人', '사람 인'), ('謂', '이를(부를) 위'), ('翡', '물총새·비취 비')]
for i, (h, m) in enumerate(hanja):
    col, row = i % 2, i // 2
    x, y = 70 + col * 270, 86 + row * 52
    d.text((x, y), h, font=F(34, 's'), fill=INK)
    d.text((x + 52, y + 8), m, font=F(20), fill=INK)
save(im, 'cu_hanja')

# ------------------------------------------------------------------ 2. 고려도경
im, d = parchment(None, base=(222, 206, 166))
d.rectangle([20, 20, CW - 21, CH - 21], outline=(140, 100, 60), width=2)
cols = ['陶器色之靑者', '麗人謂之翡色']
for i, c in enumerate(cols):
    x = 440 - i * 90
    for j, ch in enumerate(c):
        d.text((x, 50 + j * 46), ch, font=F(38, 's'), fill=INK)
d.rectangle([340, 40, 500, 330], outline=RED, width=2)
text_block(d, 50, 70, "『고려도경』\n송나라 사신 서긍이\n1123년 고려에 다녀와서\n쓴 책", 20, 240)
text_block(d, 50, 230, "(세로로, 오른쪽 줄부터\n위에서 아래로 읽는다)", 16, 260, 6, (120, 80, 50))
save(im, 'cu_song_book')

# ------------------------------------------------------------------ 2. 견본 청자
im, d = parchment(None, base=(230, 220, 196))
cx = CW // 2
vase = [(cx - 30, 40), (cx + 30, 40), (cx + 34, 60), (cx + 95, 110), (cx + 100, 170), (cx + 70, 250), (cx + 48, 320), (cx - 48, 320), (cx - 70, 250), (cx - 100, 170), (cx - 95, 110), (cx - 34, 60)]
d.polygon(vase, fill=(124, 170, 150), outline=(60, 90, 80))
d.ellipse([cx - 32, 32, cx + 32, 48], fill=(108, 150, 132), outline=(60, 90, 80))
def crane(x, y, s=1.0):
    d.ellipse([x - 30 * s, y - 30 * s, x + 30 * s, y + 30 * s], outline=(250, 250, 246), width=3)
    d.line([(x - 18 * s, y + 4 * s), (x, y - 6 * s), (x + 18 * s, y + 4 * s)], fill=(250, 250, 246), width=4)
    d.line([(x, y - 6 * s), (x + 6 * s, y - 16 * s)], fill=(250, 250, 246), width=3)
def cloud(x, y):
    for k in range(3):
        d.arc([x + k * 12 - 10, y - 8, x + k * 12 + 6, y + 8], 180, 360, fill=(36, 40, 40), width=4)
crane(cx - 40, 140); crane(cx + 45, 210, 0.9); crane(cx - 25, 265, 0.75)
cloud(cx + 20, 120); cloud(cx - 70, 205); cloud(cx + 25, 280); cloud(cx - 5, 190)
d.text((40, 40), '견본', font=F(26, 's'), fill=INK)
text_block(d, 40, 80, "청자 상감\n운학문 매병\n\n(구름 운 雲\n학 학 鶴)", 18, 170)
text_block(d, 450, 120, "흰 동그라미 안에\n흰 학이 날고,\n그 사이로\n까만 구름이\n흐른다.", 18, 170)
save(im, 'cu_sample')

# ------------------------------------------------------------------ 3. 보현원 그림
im, d = parchment('경인년(1170) 보현원의 일', base=(226, 212, 176))
d.rectangle([60, 80, 580, 300], fill=(210, 200, 168), outline=(120, 90, 60), width=2)
d.polygon([(200, 160), (320, 110), (440, 160)], fill=(120, 60, 50), outline=INK)
d.rectangle([220, 160, 420, 230], fill=(190, 150, 100), outline=INK)
for i, (x, c) in enumerate([(150, (90, 90, 110)), (190, (90, 90, 110)), (460, (60, 60, 140)), (500, (60, 60, 140)), (530, (140, 40, 40))]):
    d.ellipse([x - 8, 232, x + 8, 248], fill=(230, 196, 160), outline=INK)
    d.rectangle([x - 10, 248, x + 10, 284], fill=c, outline=INK)
d.text((170, 292), '무신들', font=F(16, 'b'), fill=INK, anchor='mm'); d.text((495, 292), '문신들', font=F(16, 'b'), fill=INK, anchor='mm')
text_block(d, 60, 312, "1170년 경인년, 의종이 보현원에 행차했을 때 무신정변이 일어났다.", 17, 540)
save(im, 'cu_painting')

# ------------------------------------------------------------------ 3. 무신 집권자
im, d = parchment('무신 집권자들', base=(226, 212, 176))
for i, (n, c) in enumerate([('정중부', (120, 70, 60)), ('경대승', (70, 90, 120)), ('이의민', (90, 110, 70)), ('최충헌', (150, 40, 40))]):
    x = 80 + i * 130
    d.rectangle([x, 90, x + 100, 240], fill=(214, 200, 164), outline=(100, 66, 40), width=4)
    d.ellipse([x + 32, 104, x + 68, 140], fill=(232, 198, 160), outline=INK)
    d.rectangle([x + 22, 138, x + 78, 226], fill=c, outline=INK)
    d.text((x + 50, 262), n, font=F(22, 'b'), fill=INK, anchor='mm')
    if i < 3:
        d.text((x + 115, 165), '→', font=F(22, 'b'), fill=RED, anchor='mm')
text_block(d, 60, 290, "무신들은 서로 권력을 빼앗고 빼앗겼다. 1196년부터 최씨 집안이 60여 년 동안 권력을 쥐었다.", 17, 520)
save(im, 'cu_rulers')

# ------------------------------------------------------------------ 4. 성곽 지도
im, d = parchment('고려의 성들', base=(228, 216, 180))
land = [(250, 340), (220, 270), (240, 220), (210, 170), (250, 120), (330, 90), (430, 76), (470, 110), (430, 170), (460, 230), (430, 300), (380, 345)]
d.polygon(land, fill=(186, 200, 150), outline=(110, 120, 80))
d.line([(250, 120), (330, 92), (430, 78)], fill=(80, 120, 190), width=4)
d.text((440, 62), '북쪽 국경', font=F(15, 'b'), fill=(60, 90, 160))
d.ellipse([196, 236, 214, 252], fill=(150, 170, 120), outline=(90, 100, 70)); d.text((130, 238), '강화도', font=F(15, 'b'), fill=INK)
for (x, y, n) in [(268, 132, '귀주성'), (300, 262, '처인성'), (350, 300, '충주성')]:
    d.rectangle([x - 8, y - 8, x + 8, y + 8], fill=RED, outline=INK)
    d.text((x + 14, y - 11), n, font=F(18, 'b'), fill=INK)
d.line([(500, 120), (500, 300)], fill=RED, width=4); d.polygon([(490, 290), (510, 290), (500, 310)], fill=RED)
text_block(d, 515, 150, "몽골군은\n북쪽 국경을\n넘어,\n해가 갈수록\n더 남쪽\n깊숙이\n쳐들어왔다.", 16, 110, 5, RED)
save(im, 'cu_castle_map')

# ------------------------------------------------------------------ 4. 전투 기록
im, d = parchment(None, base=(222, 210, 178))
recs = [('ㄱ', "1253년, 김윤후는 노비 문서를 불태우고 신분을 가리지 않고 상을 주겠다 약속했다. 모두 한마음으로 싸워 □□성을 지켰다."),
        ('ㄴ', "1231년 겨울, 몽골군이 처음 쳐들어왔다. 박서 장군과 군사들은 한 달 넘게 □□성을 지켜 냈다."),
        ('ㄷ', "1232년, 승려 김윤후가 이끄는 백성들이 □□성을 지켰다. 화살 한 대가 몽골 장수 살리타를 쓰러뜨렸다.")]
for i, (k, t) in enumerate(recs):
    x = 24 + i * 202
    d.rectangle([x, 26, x + 188, 334], fill=(236, 226, 196), outline=(120, 90, 60), width=2)
    d.ellipse([x + 74, 36, x + 114, 76], fill=RED)
    d.text((x + 94, 56), k, font=F(24, 'b'), fill=(255, 248, 236), anchor='mm')
    text_block(d, x + 12, 92, t, 16, 166, 7)
    for j in range(4):
        d.ellipse([x + 20 + j * 40, 300 - (j % 2) * 10, x + 50 + j * 40, 318], fill=(200, 196, 180))
save(im, 'cu_records')

# ------------------------------------------------------------------ 5. 경판(좌우 뒤집힘) / 탁본 / 천자문
def board_text(img_d, x, y, color, size=30):
    lines = ['玄', '부처님의 힘을 빌려', '몽골의 군사가', '물러가기를 비옵니다']
    img_d.text((x, y), lines[0], font=F(40, 's'), fill=color)
    yy = y + 6
    for ln in lines[1:]:
        img_d.text((x + 90, yy), ln, font=F(size, 's'), fill=color); yy += size + 22
board = Image.new('RGB', (CW, CH), (156, 112, 70))
bd = ImageDraw.Draw(board)
rnd = random.Random(5)
for y in range(0, CH, 3):
    bd.line([(0, y), (CW, y + rnd.randint(-2, 2))], fill=(146 + rnd.randint(-8, 8), 104, 64))
txt = Image.new('RGB', (CW, CH), (0, 0, 0)); td = ImageDraw.Draw(txt)
board_text(td, 70, 70, (255, 255, 255))
mask = txt.convert('L').transpose(Image.FLIP_LEFT_RIGHT)
carved = Image.new('RGB', (CW, CH), (96, 64, 38))
board = Image.composite(carved, board, mask)
bd = ImageDraw.Draw(board)
bd.rectangle([6, 6, CW - 7, CH - 7], outline=(80, 52, 30), width=8)
board.save(os.path.join(OUT, 'cu_board_mirror.png'))

im, d = parchment(None, base=(242, 238, 226))
board_text(d, 70, 70, (30, 28, 28))
d.rectangle([56, 62, 128, 124], outline=(60, 60, 60), width=2)
d.text((92, 140), '(함 이름)', font=F(14), fill=(100, 90, 80), anchor='mm')
save(im, 'cu_takbon')

im, d = parchment('천자문 (첫 여섯 글자)')
for i, (h, m) in enumerate([('天', '하늘 천'), ('地', '땅 지'), ('玄', '검을 현'), ('黃', '누를 황'), ('宇', '집 우'), ('宙', '집 주')]):
    x = 56 + i * 92
    d.rectangle([x, 96, x + 80, 196], fill=(244, 236, 214), outline=(140, 100, 60), width=2)
    d.text((x + 40, 140), h, font=F(46, 's'), fill=INK, anchor='mm')
    d.text((x + 40, 218), m, font=F(17), fill=INK, anchor='mm')
text_block(d, 60, 262, "대장경판을 담는 함(상자)에는 천자문 글자 차례대로 이름을 붙였다.", 19, 520)
save(im, 'cu_cheonja')

# ------------------------------------------------------------------ 6. 족보 / 지도 / 보고서
im, d = parchment('원 간섭기의 왕들')
kings = ['충렬왕', '충선왕', '충숙왕', '충혜왕', '충목왕', '충정왕']
for i, k in enumerate(kings):
    x = 70 + (i % 3) * 180; y = 96 + (i // 3) * 70
    d.text((x, y), k[0], font=F(30, 's'), fill=RED); d.text((x + 34, y + 2), k[1:], font=F(28, 's'), fill=INK)
text_block(d, 60, 260, "원에 충성한다는 뜻의 '충(忠)' 자를 왕의 이름에 붙여야 했다.", 19, 520)
save(im, 'cu_jokbo')

im, d = parchment('동북면 지도', base=(228, 216, 180))
G, ox, oy = 56, 200, 74
cols = 'ABCDE'
# 바다(동쪽)
for r in range(5):
    for c in range(5):
        x, y = ox + c * G, oy + r * G
        sea = (c == 4 and r <= 2)
        d.rectangle([x, y, x + G, y + G], fill=(150, 180, 210) if sea else (196, 206, 160), outline=(140, 120, 90))
for c in range(5): d.text((ox + c * G + G // 2, oy - 14), cols[c], font=F(18, 'b'), fill=INK, anchor='mm')
for r in range(5): d.text((ox - 16, oy + r * G + G // 2), str(r + 1), font=F(18, 'b'), fill=INK, anchor='mm')
d.text((ox + 4 * G + G // 2, oy + G + 6), '바다', font=F(14, 'b'), fill=(40, 70, 120), anchor='mm')
# 고개(산줄기): C2~D3 사이
for (x, y) in [(ox + 2 * G + 40, oy + 1 * G + 44), (ox + 3 * G + 6, oy + 2 * G + 8), (ox + 3 * G + 30, oy + 2 * G + 30), (ox + 2 * G + 10, oy + 1 * G + 10)]:
    d.polygon([(x - 12, y + 10), (x, y - 10), (x + 12, y + 10)], fill=(120, 110, 90), outline=INK)
d.text((ox + 2 * G + 6, oy + 2 * G + 34), '높은 고개', font=F(13, 'b'), fill=INK)
def town(c, r, name=None, col=INK):
    x, y = ox + c * G + G // 2, oy + r * G + G // 2
    if name:
        d.ellipse([x - 8, y - 8, x + 8, y + 8], fill=col, outline=INK); d.text((x, y + 16), name, font=F(14, 'b'), fill=INK, anchor='mm')
    else:
        d.polygon([(x, y - 10), (x + 10, y), (x, y + 10), (x - 10, y)], fill=(80, 70, 70), outline=INK)
town(2, 3, '개경', (60, 90, 150)); town(1, 2, '서경', (60, 90, 150))
for c, r in [(3, 1), (0, 1), (4, 3), (1, 4), (3, 4)]: town(c, r)
text_block(d, 34, 100, "◆ = 이름이\n지워진 곳", 16, 150)
save(im, 'cu_grid_map')

im, d = parchment('동북면 장수의 보고서')
y = text_block(d, 60, 96, "전하, 쌍성총관부(화주)의 위치를 아뢰옵니다.", 21, 520)
text_block(d, 80, y + 16, "하나. 개경에서 보아 동북쪽에 있습니다.\n둘. 가는 길에 높은 고개를 넘어야 합니다.\n셋. 동쪽 바닷가에 닿아 있습니다.", 21, 500, 14)
save(im, 'cu_report')

# ------------------------------------------------------------------ 7. 간기 / 연호
im, d = parchment(None, base=(226, 212, 176))
cols = ['宣光七年丁巳七月 日', '淸州牧外興德寺鑄字印施']
for i, c in enumerate(cols):
    x = 560 - i * 70
    for j, ch in enumerate(c):
        if ch == ' ':
            continue
        d.text((x, 26 + j * 29), ch, font=F(26, 's'), fill=INK)
text_block(d, 40, 60, "간기 (책 끝에 적는 글)", 22, 400, 8, RED, 's')
text_block(d, 40, 110, "오른쪽 줄: 선광 7년 정사 7월 일\n왼쪽 줄: 청주목 바깥 흥덕사에서\n쇠로 부어 만든 글자로 찍어 널리 폄", 19, 400, 12)
text_block(d, 40, 270, "※ '선광(宣光)'은 해의 이름(연호)이다.", 17, 400, 8, (120, 80, 50))
save(im, 'cu_colophon')

im, d = parchment('연호 표')
rows = [('至正', '지정', '1년 = 1341년'), ('洪武', '홍무', '1년 = 1368년'), ('宣光', '선광', '1년 = 1371년')]
y = 100
for h, k, v in rows:
    d.text((100, y), h, font=F(34, 's'), fill=INK); d.text((190, y + 6), f'({k})', font=F(22), fill=INK)
    d.text((300, y + 6), v, font=F(24, 'b'), fill=INK); y += 64
text_block(d, 80, 300, "연호의 1년이 시작하는 해를 적었다.", 18, 480, 8, (120, 80, 50))
save(im, 'cu_era')

# ------------------------------------------------------------------ 8. 두루마리
im, d = parchment(None, base=(228, 216, 184))
scrolls = [('㉠', "고려 왕실을 지키면서 잘못된 제도만 바로잡아 나가야 한다."),
           ('㉡', "썩은 나무는 고쳐 쓸 수 없다. 새 왕조를 세워 백성을 근본으로 삼는 나라를 만들자."),
           ('㉢', "이 몸이 죽고 죽어 일백 번 고쳐 죽어도, 임 향한 일편단심은 변하지 않으리라."),
           ('㉣', "새 나라의 법과 제도는 내가 설계하겠다. 도읍도 새로 정해야 한다.")]
for i, (k, t) in enumerate(scrolls):
    x = 22 + (i % 2) * 302; y = 22 + (i // 2) * 166
    d.rectangle([x, y, x + 292, y + 152], fill=(240, 232, 208), outline=(130, 96, 60), width=2)
    d.rectangle([x, y, x + 8, y + 152], fill=(130, 80, 50)); d.rectangle([x + 284, y, x + 292, y + 152], fill=(130, 80, 50))
    d.text((x + 22, y + 10), k, font=F(26, 'b'), fill=RED)
    text_block(d, x + 22, y + 48, t, 17, 254, 6)
save(im, 'cu_scrolls')

# ================================================================== 아이템 아이콘 (32px x3)
def icon(name, fn):
    im = Image.new('RGBA', (32, 32), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    fn(d)
    # 윤곽선
    out = im.copy()
    for y in range(32):
        for x in range(32):
            if im.getpixel((x, y))[3] == 0:
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < 32 and 0 <= ny < 32 and im.getpixel((nx, ny))[3] > 0:
                        out.putpixel((x, y), (40, 28, 26, 255)); break
    out.resize((96, 96), Image.NEAREST).save(os.path.join(OUT, name + '.png'))

icon('item_map', lambda d: (d.rectangle([4, 7, 27, 24], fill=(228, 214, 172)), d.rectangle([4, 7, 6, 24], fill=(150, 100, 60)), d.rectangle([25, 7, 27, 24], fill=(150, 100, 60)),
                            d.line([(9, 20), (12, 14), (17, 15), (21, 10)], fill=(200, 40, 40), width=2), d.polygon([(14, 19), (17, 15), (20, 19)], fill=(110, 100, 90))))
icon('item_knife', lambda d: (d.rectangle([14, 16, 17, 28], fill=(120, 80, 50)), d.polygon([(14, 16), (17, 16), (16, 3), (15, 3)], fill=(200, 204, 214))))
icon('item_baekto', lambda d: (d.ellipse([5, 14, 26, 27], fill=(150, 110, 70)), d.ellipse([8, 9, 23, 20], fill=(246, 244, 236))))
icon('item_jato', lambda d: (d.ellipse([5, 14, 26, 27], fill=(150, 110, 70)), d.ellipse([8, 9, 23, 20], fill=(180, 78, 54))))
icon('item_celadon', lambda d: (d.ellipse([7, 9, 24, 28], fill=(124, 172, 152)), d.rectangle([13, 3, 18, 10], fill=(124, 172, 152)),
                                d.ellipse([10, 13, 16, 19], outline=(250, 250, 246)), d.point((19, 22), fill=(30, 30, 30)), d.point((20, 22), fill=(30, 30, 30))))
icon('item_paper', lambda d: (d.rectangle([5, 5, 26, 26], fill=(236, 204, 80)), d.rectangle([9, 9, 22, 12], fill=(160, 120, 40)), d.rectangle([15, 12, 17, 22], fill=(160, 120, 40)), d.rectangle([12, 21, 16, 22], fill=(160, 120, 40))))
icon('item_ink', lambda d: (d.rectangle([11, 4, 20, 27], fill=(40, 40, 48)), d.rectangle([12, 8, 19, 13], fill=(200, 170, 80))))
icon('item_hanji', lambda d: (d.rectangle([5, 8, 26, 24], fill=(246, 242, 228)), d.ellipse([22, 8, 28, 24], fill=(226, 220, 204))))
icon('item_takbon', lambda d: (d.rectangle([5, 4, 26, 28], fill=(244, 240, 228)), [d.rectangle([9, 8 + i * 5, 22 - (i % 2) * 4, 10 + i * 5], fill=(30, 30, 30)) for i in range(4)]))
icon('item_report', lambda d: (d.rectangle([5, 7, 26, 25], fill=(236, 224, 192)), d.line([(5, 7), (16, 17), (26, 7)], fill=(150, 120, 80)), d.ellipse([13, 14, 19, 20], fill=(180, 40, 40))))
icon('item_type', lambda d: (d.rectangle([9, 9, 22, 24], fill=(150, 146, 130)), d.rectangle([9, 9, 22, 12], fill=(186, 182, 166)), d.rectangle([12, 14, 19, 15], fill=(60, 56, 50)), d.rectangle([15, 14, 16, 21], fill=(60, 56, 50))))
print('done', len(os.listdir(OUT)))
