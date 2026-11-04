"""후기 링크 바꾸기 (Windows · Mac · 리눅스 어디서나)
 하는 일: 1) img/pictures/cu_review.png 를 새 주소의 QR 그림으로 다시 만들고
          2) data/EscapeData.json 의 "review" → "url" 을 새 주소로 바꿉니다.

 쓰는 법 (명령 창에서):
   python make_review_qr.py "https://forms.gle/새주소" "C:\\경로\\내MV프로젝트"
 처음 한 번만:  pip install pillow segno
"""
import io, json, os, sys

def font(size):
    from PIL import ImageFont
    for p in (r'C:\Windows\Fonts\malgunbd.ttf', r'C:\Windows\Fonts\malgun.ttf',
              '/System/Library/Fonts/AppleSDGothicNeo.ttc', '/Library/Fonts/AppleGothic.ttf',
              '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc', '/usr/share/fonts/truetype/nanum/NanumGothicBold.ttf'):
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size, index=1 if p.endswith('NotoSansCJK-Bold.ttc') else 0)
            except Exception:
                pass
    return ImageFont.load_default()

def make_card(url, out):
    from PIL import Image, ImageDraw
    W, H = 800, 450
    im = Image.new('RGB', (W, H), (242, 232, 208)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W - 1, H - 1], outline=(150, 130, 100), width=3)
    d.text((W / 2, 40), '후기를 남겨 주세요!', font=font(30), fill=(44, 36, 30), anchor='mm')
    d.line([(60, 66), (W - 60, 66)], fill=(150, 120, 90), width=2)
    try:
        import segno
        buf = io.BytesIO()
        segno.make(url, error='m').save(buf, kind='png', scale=7, border=2, dark='#2a1a10', light='#fffaf0')
        qr = Image.open(io.BytesIO(buf.getvalue())).convert('RGB').resize((236, 236), Image.NEAREST)
        im.paste(qr, (500, 96))
        d.rectangle([496, 92, 739, 335], outline=(120, 84, 50), width=3)
    except ImportError:
        print('※ segno 가 없어 QR 없이 만들었어요. (pip install segno 후 다시 실행하면 QR이 들어가요)')
    y = 112
    for line, col, sz in (('끝까지 함께해 줘서', (44, 36, 30), 26), ('고마워요!', (44, 36, 30), 26), ('', None, 10),
                          ('휴대폰으로 QR을 찍거나,', (44, 36, 30), 20), ('Enter · 클릭을 누르면', (170, 40, 40), 20), ('후기 페이지가 열려요.', (170, 40, 40), 20)):
        if line: d.text((70, y), line, font=font(sz), fill=col)
        y += sz + 16
    d.text((618, 360), url.replace('https://', ''), font=font(15), fill=(110, 80, 50), anchor='mm')
    im.save(out)

def main():
    if len(sys.argv) < 3:
        print(__doc__); sys.exit(1)
    url, root = sys.argv[1].strip(), sys.argv[2]
    pic = os.path.join(root, 'img', 'pictures', 'cu_review.png')
    data = os.path.join(root, 'data', 'EscapeData.json')
    if not os.path.exists(data):
        print('EscapeData.json 을 찾지 못했어요. MV 프로젝트 폴더(안에 data, img 폴더가 있는 곳)를 적어 주세요:', root); sys.exit(1)
    os.makedirs(os.path.dirname(pic), exist_ok=True)
    make_card(url, pic)
    d = json.load(open(data, encoding='utf-8'))
    d.setdefault('review', {})['url'] = url
    d['review'].setdefault('picture', 'cu_review')
    json.dump(d, open(data, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)
    print('완료! 새 후기 주소:', url)
    print(' - 그림:', pic)
    print(' - 데이터:', data)

if __name__ == '__main__':
    main()
