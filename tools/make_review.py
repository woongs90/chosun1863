"""후기 안내 그림 (QR 포함) -> img/pictures/cu_review.png"""
import sys, io
import segno
from PIL import Image, ImageDraw
sys.path.insert(0, '/home/claude/tools')
from make_closeups import parchment, F, INK, RED
url, out = sys.argv[1], sys.argv[2]
im, d = parchment('후기를 남겨 주세요!')
buf = io.BytesIO()
segno.make(url, error='m').save(buf, kind='png', scale=7, border=2, dark='#2a1a10', light='#fffaf0')
qr = Image.open(io.BytesIO(buf.getvalue())).convert('RGB')
side = 236
qr = qr.resize((side, side), Image.NEAREST)
im.paste(qr, (380, 82))
d.rectangle([376, 78, 380 + side + 3, 82 + side + 3], outline=(120, 84, 50), width=3)
y = 96
for line, col, sz in [("끝까지 함께해 줘서", INK, 24), ("고마워요!", INK, 24), ("", INK, 10),
                      ("휴대폰으로 QR을 찍거나,", INK, 19), ("Enter·클릭을 누르면", RED, 19), ("후기 페이지가 열려요.", RED, 19)]:
    if line:
        d.text((60, y), line, font=F(sz, 'b' if sz > 20 else 'r'), fill=col)
    y += sz + 14
short = url.replace('https://', '')
d.text((498, 336), short, font=F(15), fill=(110, 80, 50), anchor='mm')
im.save(out)
print(out)
