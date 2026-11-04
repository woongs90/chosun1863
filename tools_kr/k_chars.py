"""금지된 주파수 캐릭터 (48x58, 3프레임 x 4방향) - 1923~1945 여러 나라 사람들
 피부 skin: 사람마다 (유럽·지중해·남아시아·동아시아·아프리카 여러 빛깔)
 윗옷 top : suit(양복) frock(긴 프록코트) tunic(군복 상의) greatcoat(군용 외투) messenger(전보 배달 소년 제복) shirt vest jacket
            dress(긴 원피스) blouse(블라우스+긴 치마) overall(군수 공장 작업복) shamma(에티오피아 흰 겉옷) robe(긴 두루마기형: 중국 창파오·아랍)
            kurta(인도 긴 셔츠) sari(사리) wrap(아프리카 천 두르기) sailor(수병)
 다리 legs: trousers skirt(긴 치마) dhoti(도티) shorts robe(발목까지)  + puttee(각반)
 머리 hair: short part slick crop bald curly(짧은 곱슬) queue(변발) updo(틀어 올린 머리) bun long
 수염: mustache(콧수염) kaiser(위로 올린 콧수염) beard(턱수염) whiskers(구레나룻) goatee
 모자 hat: pillbox(전보 배달 모자) bowler(중산모) tophat(실크 모자) boater(밀짚 보터) flatcap(헌팅캡) pickel(뾰족 투구) stahl(독일 철모)
          brodie(영국 철모) adrian(프랑스 철모) kepi(케피) svcap(영국 군모) topee(햇빛 가리개 모자) turban(터번) fez(페즈) chechia(세네갈 저격병 모자)
          campaign(미군 챙모자) bersagl(이탈리아 깃털 모자) russcap(러시아 군모) jpcap(일본 군모) cocked(깃털 이각모) bonnet(여자 모자) mobcap(작업모)
          nursecap(간호사 머릿수건) bobby(영국 경찰 헬멧) mane(에티오피아 사자 갈기 머리 장식) feltbrim(넓은 챙 펠트 모자) coolie(삿갓) qingcap(청 관모)
          headscarf(머릿수건) plume(공화국 근위대 깃털 투구) peaked(챙 모자)
 손 hold: telegram rifle paper book flag:<코드> spool(전선 감개) shield_eth spear basket candle football bag cane lantern umbrella cup pen bottle
"""
import os, sys, math
from PIL import Image, ImageDraw
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'tools'))
sys.path.insert(0, HERE)
from hd_art import sh, outline, mix

# 피부색
EU = (246, 214, 186); EU2 = (238, 196, 168); MED = (226, 184, 148); SA = (186, 132, 94); SA2 = (160, 110, 76)
EA = (238, 204, 168); AF = (128, 86, 60); AF2 = (98, 64, 46); ETH = (150, 100, 70); OLD = (232, 198, 168)
WHITE = (242, 240, 232)
KHAKI = (150, 134, 92); KHAKI_D = (132, 116, 78); FGRAU = (118, 122, 104); HBLUE = (120, 146, 176); NAVY = (36, 42, 66)
RED_T = (170, 40, 40)

OFF = 10          # 모자·깃털이 잘리지 않게 칸을 위로 10px 늘림 (48x58)
FH = 48 + OFF

def tone(c): return sh(c, 1.2), c, sh(c, 0.78), sh(c, 0.58)
def px(d, x, y, c): d.point((x, y), fill=c)
def lum(c): return 0.3 * c[0] + 0.59 * c[1] + 0.11 * c[2]

def mini_flag(code, w, h):
    import k_flags
    return g_flags.flag(code, w, h)

def draw(sp, D, step):
    S = 48
    lay = Image.new('RGBA', (S, FH), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    cx = 24
    bob = 0 if step == 1 else 1
    kid = sp.get('kid', False)
    hy = (10 if kid else 5) + bob + OFF
    ny = hy + 17
    sway = {0: -1, 1: 0, 2: 1}[step]
    lift = {0: (0, 2), 1: (0, 0), 2: (2, 0)}[step]
    top = sp.get('top', 'suit')
    cloth = sp.get('cloth', (70, 70, 80))
    cL, cM, cS, cD = tone(cloth)
    hair = sp.get('hair_c', (60, 44, 34))
    hL, hM, hS, hD = tone(hair)
    shoe = sp.get('shoes', (34, 28, 26))
    skin = sp.get('skin', EU); skin_s = sh(skin, 0.84)
    legs = sp.get('legs', 'trousers')
    if top in ('dress', 'blouse', 'sari', 'overall_f'): legs = sp.get('legs', 'skirt') if top != 'overall_f' else 'trousers'
    if top in ('robe', 'po', 'dan'): legs = 'robe'
    foot = 45 + OFF
    wide = 1 if sp.get('stout') else 0
    pack = sp.get('pack')

    # ---------------- 등에 멘 것 (뒤쪽)
    if pack == 'rifle_back' and D in (0, 1, 2):
        rx = cx + (5 if D == 0 else -1)
        d.line([(rx - 4, ny + 14), (rx + 5, ny - 9)], fill=(70, 52, 36), width=2)
    if pack == 'spool' and D in (1, 2, 3):
        bx = cx + (6 if D == 1 else -12 if D == 2 else -6)
        d.ellipse([bx, ny, bx + 11, ny + 11], fill=(110, 80, 50)); d.ellipse([bx + 3, ny + 3, bx + 8, ny + 8], fill=(60, 60, 64))

    # ---------------- 다리
    if legs in ('skirt', 'robe', 'long'):
        sc = sp.get('skirt', cloth) if legs != 'robe' else cloth
        sL, sM, sS, sD = tone(sc)
        tp = ny + 3 if legs == 'skirt' else ny + 8
        wb = (12 if legs == 'skirt' else 10) + wide
        d.polygon([(cx - 8, tp), (cx + 7, tp), (cx + wb - 1 + sway, foot), (cx - wb + sway, foot)], fill=sM)
        d.polygon([(cx - 8, tp), (cx - 5, tp), (cx - wb + 4 + sway, foot), (cx - wb + sway, foot)], fill=sL if D != 2 else sS)
        d.polygon([(cx + 4, tp), (cx + 7, tp), (cx + wb - 1 + sway, foot), (cx + wb - 5 + sway, foot)], fill=sS if D != 2 else sL)
        for k in (-5, -1, 3):
            d.line([(cx + k, tp + 4), (cx + int(k * 1.5) + sway, foot - 1)], fill=sS)
        if sp.get('hem'): d.line([(cx - wb + sway, foot - 2), (cx + wb - 1 + sway, foot - 2)], fill=sp['hem'], width=2)
        if sp.get('apron') and D != 3:
            ap = sp['apron']
            d.polygon([(cx - 6, tp + 2), (cx + 5, tp + 2), (cx + 7 + sway, foot - 4), (cx - 8 + sway, foot - 4)], fill=ap)
        for i, fx in enumerate((cx - 6, cx + 1)):
            d.rectangle([fx + sway, foot - lift[i] // 2, fx + 5 + sway, foot + 1 - lift[i] // 2], fill=shoe if not sp.get('barefoot') else skin_s)
    else:
        pc = sp.get('pants', (60, 56, 54))
        pL, pM, pS, pD = tone(pc)
        for i, lx in enumerate((cx - 6 - wide, cx + 1 + wide)):
            ly = 33 + OFF - lift[i] + (5 if kid else 0); fy = foot - lift[i]
            if legs == 'dhoti':
                d.rectangle([lx - 1, ly, lx + 5, fy - 2], fill=pM); d.line([(lx + 5, ly), (lx + 5, fy - 2)], fill=pS)
                d.line([(lx + 2, ly + 2), (lx + 1, fy - 3)], fill=pS)
                d.rectangle([lx, fy - 2, lx + 4, fy], fill=skin)
                d.rectangle([lx - 1, fy, lx + 5, fy + 1], fill=shoe if not sp.get('barefoot') else skin_s)
            elif legs == 'shorts':
                d.rectangle([lx, ly, lx + 4, ly + 5], fill=pM)
                d.rectangle([lx + 1, ly + 6, lx + 3, fy], fill=sp.get('socks', skin))
                d.rectangle([lx - 1, fy, lx + 5, fy + 1], fill=shoe if not sp.get('barefoot') else skin_s)
            elif legs == 'jodh':      # 에티오피아 흰 바지 (아래가 좁음)
                d.rectangle([lx - 1, ly, lx + 5, fy - 6], fill=pM); d.rectangle([lx, fy - 6, lx + 4, fy - 1], fill=pS)
                d.rectangle([lx, fy - 1, lx + 4, fy], fill=skin)
                d.rectangle([lx - 1, fy, lx + 5, fy + 1], fill=skin_s if sp.get('barefoot', True) else shoe)
            else:
                d.rectangle([lx, ly, lx + 4, fy], fill=pM); d.line([(lx + 4, ly), (lx + 4, fy)], fill=pS)
                if sp.get('stripe'): d.line([(lx + 2, ly), (lx + 2, fy - 1)], fill=sp['stripe'])
                if sp.get('puttee'):
                    pt = sp['puttee'] if isinstance(sp['puttee'], tuple) else sh(pc, 0.86)
                    d.rectangle([lx, fy - 7, lx + 4, fy], fill=pt)
                    for yy in range(fy - 6, fy, 2): d.line([(lx, yy), (lx + 4, yy + 1)], fill=sh(pt, 0.8))
                if sp.get('boots'): d.rectangle([lx, fy - 6, lx + 4, fy], fill=sp['boots'])
                d.rectangle([lx - 1, fy, lx + 5, fy + 1], fill=shoe if not sp.get('barefoot') else skin_s)

    # ---------------- 몸통
    by = ny
    bx0, bx1 = cx - 9 - wide, cx + 8 + wide
    def side_shade(y0, y1):
        d.rectangle([bx0, y0, bx0 + 2, y1], fill=cL if D != 2 else cS)
        d.rectangle([bx1 - 2, y0, bx1, y1], fill=cS if D != 2 else cL)
    if top in ('suit', 'frock', 'tunic', 'greatcoat', 'messenger', 'jacket', 'shirt', 'vest', 'sailor', 'kurta', 'overall', 'overall_f', 'shamma', 'jeo'):
        tail = {'jeo': 14, 'frock': 21, 'greatcoat': 22, 'suit': 13, 'tunic': 13, 'kurta': 19, 'overall': 19, 'shamma': 15, 'messenger': 11}.get(top, 11)
        if top == 'overall_f': tail = 13
        d.polygon([(bx0, by + 6), (bx1, by + 6), (bx1 + (2 if tail > 15 else 0) + sway, by + tail), (bx0 - (2 if tail > 15 else 0) + sway, by + tail)], fill=cM)
        if tail > 15:
            d.polygon([(bx0, by + 6), (bx0 + 3, by + 6), (bx0 + 1 + sway, by + tail), (bx0 - 2 + sway, by + tail)], fill=cL if D != 2 else cS)
            d.polygon([(bx1 - 3, by + 6), (bx1, by + 6), (bx1 + 2 + sway, by + tail), (bx1 - 1 + sway, by + tail)], fill=cS if D != 2 else cL)
        d.rounded_rectangle([bx0, by, bx1, by + 11], 3, fill=cM)
        side_shade(by + 1, by + 10)
        if D == 0:
            if top in ('suit', 'frock', 'greatcoat'):
                shirt = sp.get('shirt', WHITE)
                d.polygon([(cx - 4, by), (cx + 3, by), (cx, by + 7)], fill=shirt)
                d.line([(cx - 4, by), (cx, by + 7)], fill=cD); d.line([(cx + 3, by), (cx, by + 7)], fill=cD)
                if sp.get('tie'): d.line([(cx, by + 1), (cx, by + 6)], fill=sp['tie'], width=2)
                if sp.get('bowtie'): d.rectangle([cx - 2, by, cx + 1, by + 1], fill=sp['bowtie'])
                if top == 'greatcoat':
                    for yy in (by + 4, by + 8, by + 12, by + 16): px(d, cx - 3, yy, (200, 190, 140)); px(d, cx + 2, yy, (200, 190, 140))
                else:
                    px(d, cx - 1, by + 9, cD); px(d, cx - 1, by + 12, cD)
                if sp.get('vest') and top != 'greatcoat':
                    d.rectangle([cx - 3, by + 4, cx + 2, by + 9], fill=sp['vest'])
                    if sp.get('chain'): d.line([(cx - 3, by + 7), (cx + 1, by + 8)], fill=(230, 200, 100))
            elif top in ('tunic', 'messenger'):
                col = sp.get('collar', sh(cloth, 0.8))
                d.rectangle([cx - 4, by - 1, cx + 3, by + 1], fill=col)
                d.line([(cx, by + 1), (cx, by + tail - 1)], fill=cD)
                btn = sp.get('buttons', (210, 190, 120))
                for yy in range(by + 2, by + tail - 1, 3): px(d, cx, yy, btn)
                if top == 'tunic' and not sp.get('nopockets'):
                    d.rectangle([cx - 7, by + 2, cx - 3, by + 5], fill=cS); d.rectangle([cx + 2, by + 2, cx + 6, by + 5], fill=cS)
                if top == 'messenger':
                    d.line([(bx0, by + 1), (bx0, by + 10)], fill=sp.get('piping', (190, 40, 40)))
                    d.line([(bx1, by + 1), (bx1, by + 10)], fill=sp.get('piping', (190, 40, 40)))
            elif top in ('shirt', 'jacket'):
                d.line([(cx, by + 1), (cx, by + 12)], fill=cS if top == 'shirt' else cD)
                d.polygon([(cx - 4, by - 1), (cx, by + 2), (cx + 3, by - 1)], fill=cL)
                if sp.get('tie'): d.line([(cx, by + 1), (cx, by + 6)], fill=sp['tie'], width=2)
                if sp.get('braces'): d.line([(cx - 5, by), (cx - 4, by + 11)], fill=sp['braces']); d.line([(cx + 4, by), (cx + 3, by + 11)], fill=sp['braces'])
                if sp.get('scarf'): d.rectangle([cx - 5, by - 1, cx + 4, by + 2], fill=sp['scarf'])
            elif top == 'vest':
                vc = sp.get('vest', (90, 80, 70))
                d.rectangle([cx - 5, by + 1, cx + 4, by + 12], fill=vc)
                d.polygon([(cx - 2, by), (cx + 1, by), (cx, by + 4)], fill=cloth)
                for yy in range(by + 3, by + 12, 3): px(d, cx, yy, sh(vc, 0.55))
                if sp.get('tie'): d.line([(cx, by + 1), (cx, by + 5)], fill=sp['tie'], width=2)
                if sp.get('chain'): d.line([(cx - 4, by + 7), (cx, by + 8)], fill=(230, 200, 100))
            elif top == 'sailor':
                d.polygon([(cx - 6, by), (cx + 5, by), (cx, by + 7)], fill=(250, 250, 250))
                d.polygon([(cx - 4, by), (cx + 3, by), (cx, by + 5)], fill=sh(cloth, 0.7))
            elif top == 'kurta':
                d.line([(cx, by), (cx, by + 6)], fill=cS)
                for yy in (by + 2, by + 4): px(d, cx - 1, yy, sh(cloth, 0.6))
            elif top in ('overall', 'overall_f'):
                d.rectangle([cx - 4, by - 1, cx + 3, by + 1], fill=sh(cloth, 0.85))
                for yy in range(by + 3, by + 12, 3): px(d, cx, yy, sh(cloth, 0.6))
            elif top == 'shamma':
                bc = sp.get('border', (170, 40, 40))
                d.line([(cx - 6, by), (cx + 4, by + 12)], fill=sh(cloth, 0.86))
                d.line([(bx0 + 1, by + tail - 2), (bx1 - 1, by + tail - 2)], fill=bc, width=2)
        elif D == 3:
            if top in ('frock', 'greatcoat'): d.line([(cx, by + 10), (cx + sway, by + tail)], fill=cD)
            if top == 'sailor': d.rectangle([cx - 6, by - 1, cx + 5, by + 6], fill=(36, 50, 90)); d.line([(cx - 6, by + 5), (cx + 5, by + 5)], fill=(250, 250, 250))
            if top == 'shamma': d.line([(bx0 + 1, by + tail - 2), (bx1 - 1, by + tail - 2)], fill=sp.get('border', (170, 40, 40)), width=2)
            if top == 'messenger' or sp.get('pouch'): pass
        if sp.get('belt') and D != 3: d.rectangle([bx0, by + 10, bx1, by + 11], fill=sp['belt'])
        elif sp.get('belt'): d.rectangle([bx0, by + 10, bx1, by + 11], fill=sp['belt'])
        if sp.get('sash'):
            sc = sp['sash']
            if D in (0, 3): d.line([(bx0 + 2, by + 1), (bx1 - 2, by + 10)], fill=sc, width=2)
        if sp.get('webbing') and D in (0, 3):
            wc = sp['webbing']
            d.line([(cx - 6, by), (cx - 6, by + 10)], fill=wc); d.line([(cx + 5, by), (cx + 5, by + 10)], fill=wc)
            d.rectangle([bx0, by + 9, bx1, by + 11], fill=wc)
            if D == 0:
                for xx in (cx - 8, cx - 5, cx + 3, cx + 6): d.rectangle([xx, by + 8, xx + 1, by + 10], fill=sh(wc, 0.8))
        if sp.get('medals') and D == 0:
            for k, mc in enumerate(sp['medals']): d.rectangle([cx - 7 + k * 2, by + 3, cx - 6 + k * 2, by + 5], fill=mc)
        if sp.get('epaulet') and D in (0, 3):
            ep = sp['epaulet']
            d.rectangle([bx0 - 1, by, bx0 + 3, by + 1], fill=ep); d.rectangle([bx1 - 3, by, bx1 + 1, by + 1], fill=ep)
        if sp.get('cross') and D == 0: d.rectangle([cx - 7, by + 4, cx - 5, by + 6], fill=sp['cross'])
        if sp.get('cuirass'):      # 청동 흉갑 (그리스 중장 보병)
            cu = sp['cuirass']; cuL, cuM, cuS, cuD = tone(cu)
            d.rounded_rectangle([bx0 + 1, by, bx1 - 1, by + 12], 3, fill=cuM)
            d.line([(bx0 + 2, by + 1), (bx1 - 2, by + 1)], fill=cuL)
            if D == 0: d.arc([cx - 6, by + 1, cx - 1, by + 7], 200, 340, fill=cuS); d.arc([cx, by + 1, cx + 5, by + 7], 200, 340, fill=cuS)
            for xx in range(bx0 + 1, bx1, 3): d.line([(xx, by + 12), (xx, by + 15)], fill=cuS)     # 가죽 띠(프테루게스)
        if sp.get('drape') and D in (0, 3):      # 히마티온: 왼쪽 어깨에서 비스듬히 두른 겉옷
            dc = sp['drape']; dL, dM, dS, dD = tone(dc)
            d.polygon([(bx0, by), (bx0 + 6, by), (bx1, by + 12), (bx1, by + 17), (bx1 - 5, by + 17)], fill=dM)
            d.line([(bx0 + 6, by), (bx1, by + 12)], fill=dS)
    elif top in ('dress', 'blouse', 'sari'):
        jc = sp.get('blouse', cloth)
        jL, jM, jS, jD = tone(jc)
        d.rounded_rectangle([cx - 8, by - 1, cx + 7, by + 8], 3, fill=jM)
        d.rectangle([cx - 8, by, cx - 6, by + 7], fill=jL if D != 2 else jS)
        d.rectangle([cx + 5, by, cx + 7, by + 7], fill=jS if D != 2 else jL)
        if top == 'blouse':
            d.rectangle([cx - 8, by + 7, cx + 7, by + 9], fill=sp.get('skirt', (50, 50, 70)))
            if D == 0: d.rectangle([cx - 2, by - 1, cx + 1, by + 1], fill=sh(jc, 1.1)); px(d, cx, by + 3, sh(jc, 0.7))
        elif top == 'dress':
            if sp.get('belt'): d.rectangle([cx - 8, by + 7, cx + 7, by + 8], fill=sp['belt'])
            if D == 0 and sp.get('collar'): d.rectangle([cx - 3, by - 1, cx + 2, by + 1], fill=sp['collar'])
        elif top == 'sari':
            pc = sp.get('pallu', sh(cloth, 0.8))
            if D in (0, 1): d.polygon([(cx - 8, by - 1), (cx - 4, by - 1), (cx + 8, by + 10), (cx + 4, by + 12)], fill=pc)
            elif D == 3: d.polygon([(cx - 8, by - 2), (cx + 7, by - 2), (cx + 7, by + 12), (cx - 8, by + 9)], fill=pc)
            if sp.get('border'): d.line([(cx - 4, by - 1), (cx + 8, by + 10)], fill=sp['border'])
    elif top == 'wrap':
        wc = cloth; pat = sp.get('pattern', sh(wc, 0.6))
        d.rounded_rectangle([bx0 + 1, by, bx1 - 1, by + 12], 3, fill=wc)
        d.polygon([(bx0, by + 9), (bx1, by + 9), (bx1 + 1 + sway, by + 18), (bx0 - 1 + sway, by + 18)], fill=sh(wc, 0.9))
        for k in range(bx0 + 1, bx1, 3): px(d, k, by + 3 + (k % 2) * 3, pat); px(d, k + 1, by + 13, pat)
        if sp.get('bare_arms'): pass
    # 완장
    if sp.get('armband') and D != 2:
        ax = cx - 12 - wide if D in (0, 3, 1) else cx + 8
        d.rectangle([ax, ny + 3, ax + 3, ny + 5], fill=sp['armband'])
        if sp.get('armband_cross'): px(d, ax + 1, ny + 4, sp['armband_cross']); px(d, ax + 2, ny + 4, sp['armband_cross'])

    # 팔
    armc = sp.get('sleeve', sp.get('blouse', cloth) if top in ('dress', 'blouse', 'sari') else cloth)
    if top == 'vest': armc = cloth
    bare = sp.get('bare_arms') or top == 'wrap'
    aL, aM, aS, aD = tone(armc)
    swing = {0: 2, 1: 0, 2: -2}[step]
    hold = sp.get('hold')
    ay = by
    if sp.get('salute') and D == 0: hold = None
    if D in (0, 3):
        for side, sg in ((-1, swing), (1, -swing)):
            ax = cx - 12 - wide if side < 0 else cx + 8 + wide
            hh = 0 if (hold and side > 0 and D == 0) else sg
            if top in ('shamma', 'robe', 'kurta', 'po', 'dan') and not bare:
                d.rounded_rectangle([ax - 1, ay + 1 + max(0, -hh), ax + 4, ay + 11 + max(0, hh)], 2, fill=aM)
            else:
                d.rounded_rectangle([ax, ay + 1 + max(0, -hh), ax + 3, ay + 11 + max(0, hh)], 2, fill=(skin if bare else aM))
                if sp.get('cuff') and not bare: d.line([(ax, ay + 10 + max(0, hh)), (ax + 3, ay + 10 + max(0, hh))], fill=sp['cuff'])
            d.rectangle([ax, ay + 11 + max(0, hh), ax + 3, ay + 13 + max(0, hh)], fill=sp.get('gloves', skin))
    else:
        ax = cx - 2
        d.rounded_rectangle([ax, ay + 1, ax + 4, ay + 12], 2, fill=(skin_s if bare else aS))
        d.rectangle([ax, ay + 12, ax + 4, ay + 14], fill=sp.get('gloves', skin))
    if top in ('robe', 'po', 'dan'):
        d.rounded_rectangle([bx0, by, bx1, by + 11], 3, fill=cM); side_shade(by + 1, by + 10)
        if D == 0:
            d.line([(cx - 3, by), (cx + 3, by + 6)], fill=cD)
            d.rectangle([cx - 3, by - 1, cx + 2, by], fill=sh(cloth, 0.8))
            if sp.get('vest'): d.rectangle([cx - 7, by, cx + 6, by + 9], fill=sp['vest'])
        if sp.get('belt'): d.rectangle([bx0, by + 9, bx1, by + 10], fill=sp['belt'])

    kr_body(d, sp, D, cx, by, bx0, bx1, cloth, sway, foot, ny, top)
    # ---------------- 머리
    hx0, hx1 = cx - 8, cx + 7
    hs = sp.get('hair', 'short')
    kr_hair = hs
    if hs == 'jjok': hs = 'bun'
    elif hs == 'daenggi': hs = 'braid'
    elif hs == 'sangtu': hs = 'slick'
    if hs == 'updo' and D != 3:
        d.ellipse([cx - 6, hy - 4, cx + 5, hy + 3], fill=hM)
    d.rounded_rectangle([hx0, hy + 2, hx1, hy + 16], 6, fill=skin)
    d.rectangle([cx - 3, hy + 15, cx + 2, ny], fill=skin_s)
    if D == 3:
        if hs == 'bald':
            d.rounded_rectangle([hx0, hy + 2, hx1, hy + 15], 6, fill=skin); d.rectangle([hx0, hy + 8, hx1, hy + 13], fill=hM)
        elif hs in ('crop', 'curly'):
            d.rounded_rectangle([hx0, hy + 1, hx1, hy + 14], 6, fill=hS)
            if hs == 'curly':
                for qx in range(hx0 + 1, hx1, 3):
                    for qy in range(hy + 2, hy + 13, 3): px(d, qx, qy, hD)
        elif hs == 'queue':
            d.rounded_rectangle([hx0, hy + 4, hx1, hy + 15], 6, fill=hM); d.rounded_rectangle([hx0 + 1, hy + 1, hx1 - 1, hy + 6], 5, fill=sh(skin, 0.9))
            d.rectangle([cx - 1, hy + 13, cx + 1, hy + 30], fill=hS)
            for yy in range(hy + 15, hy + 30, 3): px(d, cx, yy, hD)
        else:
            d.rounded_rectangle([hx0, hy + 1, hx1, hy + 15], 6, fill=hM)
        if hs in ('bun', 'updo'): d.ellipse([cx - 4, hy + 2 if hs == 'updo' else hy + 11, cx + 3, hy + 9 if hs == 'updo' else hy + 17], fill=hD)
        if hs == 'long': d.rounded_rectangle([hx0 - 1, hy + 4, hx1 + 1, hy + 22], 4, fill=hM)
        if hs == 'braid': d.rectangle([cx - 1, hy + 13, cx + 1, hy + 26], fill=hS)
        if sp.get('beard'): pass
    else:
        if hs == 'bald':
            d.rectangle([hx0, hy + 7, hx0 + 2, hy + 12], fill=hM); d.rectangle([hx1 - 2, hy + 7, hx1, hy + 12], fill=hM)
        elif hs == 'crop':
            d.rounded_rectangle([hx0, hy + 1, hx1, hy + 6], 5, fill=hS)
            d.rectangle([hx0, hy + 3, hx0 + 1, hy + 9], fill=hS); d.rectangle([hx1 - 1, hy + 3, hx1, hy + 9], fill=hS)
        elif hs == 'curly':
            d.rounded_rectangle([hx0 - 1, hy, hx1 + 1, hy + 6], 5, fill=hM)
            d.rectangle([hx0 - 1, hy + 3, hx0 + 1, hy + 9], fill=hM); d.rectangle([hx1 - 1, hy + 3, hx1 + 1, hy + 9], fill=hM)
            for qx in range(hx0, hx1 + 1, 2): px(d, qx, hy + 1 + (qx % 4 == 0), hD); px(d, qx + 1, hy + 4, hS)
        elif hs == 'queue':
            d.rounded_rectangle([hx0, hy + 2, hx1, hy + 6], 4, fill=sh(skin, 0.9))     # 앞머리를 민 자리
            d.rectangle([hx0 - 1, hy + 5, hx0 + 1, hy + 9], fill=hM); d.rectangle([hx1 - 1, hy + 5, hx1 + 1, hy + 9], fill=hM)
            if D in (1, 2):
                qx = hx1 if D == 1 else hx0 - 2
                d.rectangle([qx, hy + 8, qx + 2, hy + 28], fill=hS)
        else:
            d.rounded_rectangle([hx0 - 1, hy, hx1 + 1, hy + 7], 5, fill=hM)
            if hs in ('short', 'part', 'slick', 'bob', 'braid', 'bun', 'long', 'updo'):
                d.rectangle([hx0 - 1, hy + 4, hx0 + 1, hy + 10], fill=hM); d.rectangle([hx1 - 1, hy + 4, hx1 + 1, hy + 10], fill=hM)
            d.line([(hx0 + 2, hy + 2), (hx1 - 3, hy + 2)], fill=hL)
            if hs == 'part' and D == 0: d.line([(cx - 3, hy), (cx - 3, hy + 4)], fill=hS)
            if hs == 'short' and D == 0: d.rectangle([hx0 + 1, hy + 4, hx0 + 6, hy + 6], fill=hM)
            if hs == 'slick' and D == 0: d.line([(hx0 + 1, hy + 5), (hx1 - 1, hy + 5)], fill=hS)
            if hs == 'updo' and D == 0: d.line([(cx, hy), (cx, hy + 3)], fill=hS)
            if hs == 'long':
                d.rectangle([hx0 - 2, hy + 3, hx0 + 1, hy + 21], fill=hM); d.rectangle([hx1 - 1, hy + 3, hx1 + 2, hy + 21], fill=hM)
            if hs in ('bun', 'updo') and D in (1, 2):
                bx = hx1 - 1 if D == 1 else hx0 - 4
                d.ellipse([bx, hy + (2 if hs == 'updo' else 9), bx + 5, hy + (8 if hs == 'updo' else 15)], fill=hD)
            if hs == 'braid' and D in (1, 2):
                bx = hx1 if D == 1 else hx0 - 2
                d.rectangle([bx, hy + 9, bx + 2, hy + 24], fill=hS)
        # 구레나룻·턱수염 (얼굴 아래)
        bc = sp.get('beard') or sp.get('whiskers') or sp.get('goatee')
        if sp.get('beard'):
            bcol = sp['beard']; long_ = sp.get('beard_long', 0)
            if D == 0:
                d.rounded_rectangle([hx0 + 1, hy + 10, hx1 - 1, hy + 17 + long_], 4, fill=bcol)
                d.rectangle([cx - 2, hy + 12, cx + 1, hy + 13], fill=sh(skin, 0.7))
            elif D in (1, 2):      # 옆모습: 턱 앞쪽만 (뒤통수 쪽 · 등 쪽에는 그리지 않음)
                bx = hx0 if D == 1 else hx1 - 6
                d.rounded_rectangle([bx, hy + 11, bx + 6, hy + 16 + long_], 2, fill=bcol)
                sx_ = bx + 5 if D == 1 else bx
                d.line([(sx_, hy + 7), (sx_, hy + 12)], fill=bcol)
        if sp.get('whiskers'):
            wc = sp['whiskers']
            if D == 0: d.rectangle([hx0, hy + 8, hx0 + 2, hy + 15], fill=wc); d.rectangle([hx1 - 2, hy + 8, hx1, hy + 15], fill=wc)
            else:
                wx = hx1 - 4 if D == 1 else hx0 + 1
                d.rectangle([wx, hy + 8, wx + 3, hy + 15], fill=wc)
        if sp.get('goatee') and D != 3:
            gx = cx - 1 if D == 0 else (cx - 5 if D == 1 else cx + 3)
            d.rectangle([gx, hy + 14, gx + 2, hy + 18], fill=sp['goatee'])
        # 얼굴
        dark = lum(skin) < 150
        eye = (14, 10, 12) if dark else (36, 28, 40)
        if D == 0:
            for ex in (cx - 4, cx + 3):
                px(d, ex, hy + 10, eye); px(d, ex, hy + 9, eye)
                if dark: px(d, ex + (1 if ex < cx else -1), hy + 10, (226, 218, 206))
            if sp.get('blush', not sp.get('old') and not dark and lum(skin) > 200):
                d.rectangle([cx - 6, hy + 12, cx - 5, hy + 12], fill=mix(skin, (240, 140, 130), 0.5)); d.rectangle([cx + 4, hy + 12, cx + 5, hy + 12], fill=mix(skin, (240, 140, 130), 0.5))
            if not (sp.get('mustache') or sp.get('kaiser') or sp.get('beard')):
                d.line([(cx - 1, hy + 13), (cx, hy + 13)], fill=sh(skin, 0.7))
            if sp.get('smile'): d.line([(cx - 2, hy + 13), (cx + 1, hy + 13)], fill=sh(skin, 0.6)); px(d, cx - 2, hy + 12, sh(skin, 0.6)); px(d, cx + 1, hy + 12, sh(skin, 0.6))
            if sp.get('glasses'):
                gc = sp.get('glass_c', (30, 26, 26))
                if sp.get('glasses') == 'pince':
                    px(d, cx - 4, hy + 8, gc); px(d, cx + 3, hy + 8, gc); d.point([(cx - 5, hy + 9), (cx - 3, hy + 9), (cx + 2, hy + 9), (cx + 4, hy + 9)], fill=gc); px(d, cx - 1, hy + 9, gc); px(d, cx, hy + 9, gc)
                else:
                    d.ellipse([cx - 7, hy + 7, cx - 1, hy + 12], outline=gc); d.ellipse([cx + 1, hy + 7, cx + 7, hy + 12], outline=gc)
                    d.line([(cx - 1, hy + 9), (cx + 1, hy + 9)], fill=gc)
            if sp.get('mustache'): d.line([(cx - 3, hy + 12), (cx + 2, hy + 12)], fill=sp['mustache']); px(d, cx - 4, hy + 13, sp['mustache']); px(d, cx + 3, hy + 13, sp['mustache'])
            if sp.get('kaiser'):
                k = sp['kaiser']; d.line([(cx - 3, hy + 12), (cx + 2, hy + 12)], fill=k); px(d, cx - 4, hy + 11, k); px(d, cx - 5, hy + 10, k); px(d, cx + 3, hy + 11, k); px(d, cx + 4, hy + 10, k)
            if sp.get('wrinkle'): px(d, cx - 6, hy + 10, skin_s); px(d, cx + 5, hy + 10, skin_s)
            if sp.get('monocle'): d.ellipse([cx + 1, hy + 7, cx + 6, hy + 12], outline=(200, 190, 150))
            if sp.get('tilak'): px(d, cx, hy + 7, sp['tilak'])
        else:
            ex = cx - 5 if D == 1 else cx + 4
            px(d, ex, hy + 10, eye); px(d, ex, hy + 9, eye)
            if sp.get('glasses') and sp.get('glasses') != 'pince':
                gc = sp.get('glass_c', (30, 26, 26))
                d.ellipse([ex - 3, hy + 7, ex + 3, hy + 12], outline=gc)
                d.line([(ex + (3 if D == 1 else -3), hy + 9), (cx + (6 if D == 1 else -7), hy + 8)], fill=gc)
            mc = sp.get('mustache') or sp.get('kaiser')
            if mc: d.line([(ex - 1 if D == 1 else ex - 2, hy + 12), (ex + 2 if D == 1 else ex + 1, hy + 12)], fill=mc)
            if sp.get('kaiser'): px(d, ex + (3 if D == 2 else -2), hy + 11, sp['kaiser'])
            nx = hx0 - 1 if D == 1 else hx1 + 1
            px(d, nx, hy + 11, skin_s)
    kr_hair_extra(d, sp, D, cx, hy, hx0, hx1, kr_hair, tone(hair))
    # 모자
    hat = sp.get('hat')
    hc = sp.get('hat_c', (40, 36, 34))
    hcL, hcM, hcS, hcD = tone(hc)
    if hat == 'pillbox':        # 전보 배달 소년: 작고 납작한 둥근 모자 + 턱끈
        d.rounded_rectangle([cx - 6, hy - 3, cx + 5, hy + 2], 2, fill=hc); d.line([(cx - 6, hy + 1), (cx + 5, hy + 1)], fill=sp.get('band', (190, 40, 40)))
        if D == 0: d.line([(hx0 + 1, hy + 3), (hx0 + 1, hy + 12)], fill=sh(hc, 0.6)); px(d, cx, hy - 1, (230, 200, 110))
    elif hat == 'bowler':
        d.chord([cx - 7, hy - 6, cx + 6, hy + 5], 180, 360, fill=hc); d.ellipse([cx - 10, hy - 1, cx + 9, hy + 3], fill=hc)
        d.line([(cx - 7, hy - 1), (cx + 6, hy - 1)], fill=sh(hc, 0.6)); px(d, cx - 3, hy - 4, sh(hc, 1.6))
    elif hat == 'tophat':
        d.rectangle([cx - 6, hy - 10, cx + 5, hy + 1], fill=hc); d.ellipse([cx - 10, hy - 1, cx + 9, hy + 3], fill=hc)
        d.rectangle([cx - 6, hy - 2, cx + 5, hy - 1], fill=sh(hc, 1.6)); d.line([(cx - 5, hy - 9), (cx - 5, hy - 3)], fill=sh(hc, 1.5))
    elif hat == 'boater':
        sc = sp.get('hat_c', (226, 204, 150))
        d.rectangle([cx - 6, hy - 4, cx + 5, hy + 1], fill=sc); d.ellipse([cx - 11, hy - 1, cx + 10, hy + 3], fill=sc)
        d.rectangle([cx - 6, hy - 2, cx + 5, hy], fill=sp.get('band', (40, 40, 60)))
    elif hat == 'flatcap':
        d.ellipse([hx0 - 2, hy - 3, hx1 + 1, hy + 4], fill=hc)
        if D == 0: d.rectangle([hx0 + 1, hy + 2, hx1 - 2, hy + 4], fill=sh(hc, 0.7))
        elif D in (1, 2):
            vx = hx0 - 4 if D == 1 else hx1 - 2
            d.rectangle([vx, hy + 2, vx + 6, hy + 3], fill=sh(hc, 0.7))
    elif hat == 'pickel':       # 프로이센 뾰족 투구 (높은 가죽 투구 + 금빛 독수리판 + 긴 뾰족 끝)
        pc = sp.get('cover') or sp.get('hat_c', (30, 28, 30))
        d.rounded_rectangle([hx0, hy - 6, hx1, hy + 3], 5, fill=pc)
        d.polygon([(hx0 - 2, hy + 2), (hx1 + 2, hy + 2), (hx1 + 1, hy + 4), (hx0 - 1, hy + 4)], fill=sh(pc, 0.7))
        spk = sp.get('spike', (210, 186, 110)) if not sp.get('cover') else sh(pc, 0.92)
        d.rectangle([cx - 2, hy - 8, cx + 1, hy - 6], fill=spk)
        d.polygon([(cx - 2, hy - 8), (cx + 1, hy - 8), (cx, hy - 14)], fill=spk)
        if D == 0 and not sp.get('cover'): d.polygon([(cx - 3, hy - 3), (cx + 2, hy - 3), (cx, hy + 2)], fill=sp.get('plate', (220, 190, 100)))
        if D == 0 and sp.get('cover'): d.rectangle([cx - 2, hy - 2, cx + 1, hy], fill=(170, 40, 40))
    elif hat == 'stahl':        # 독일 철모 (1916~): 깊은 투구 + 옆으로 벌어진 귀막이
        sc = sp.get('hat_c', (100, 104, 92))
        d.chord([hx0 - 2, hy - 5, hx1 + 2, hy + 12], 180, 360, fill=sc)
        d.polygon([(hx0 - 2, hy + 3), (hx1 + 2, hy + 3), (hx1 + 4, hy + 8), (hx0 - 4, hy + 8)], fill=sc)
        d.line([(hx0 - 3, hy + 7), (hx1 + 3, hy + 7)], fill=sh(sc, 0.7)); px(d, hx0 + 1, hy, sh(sc, 0.6)); px(d, hx1 - 1, hy, sh(sc, 0.6))
    elif hat == 'brodie':       # 영국 철모: 넓은 접시 모양
        bc_ = sp.get('hat_c', (110, 104, 76))
        d.chord([cx - 6, hy - 5, cx + 5, hy + 6], 180, 360, fill=bc_)
        d.ellipse([cx - 12, hy - 1, cx + 11, hy + 4], fill=sh(bc_, 0.92)); d.ellipse([cx - 11, hy, cx + 10, hy + 3], outline=sh(bc_, 0.7))
    elif hat == 'adrian':       # 프랑스 철모: 위에 볏 + 앞뒤 챙
        ac = sp.get('hat_c', (110, 130, 150))
        d.chord([hx0 - 1, hy - 5, hx1 + 1, hy + 9], 180, 360, fill=ac)
        d.rectangle([cx - 1, hy - 8, cx, hy - 3], fill=sh(ac, 1.15)); d.line([(cx - 4, hy - 6), (cx + 3, hy - 6)], fill=sh(ac, 1.15))
        d.ellipse([hx0 - 3, hy + 1, hx1 + 3, hy + 5], fill=sh(ac, 0.9))
        if D == 0: px(d, cx, hy - 1, sh(ac, 0.6))
    elif hat == 'kepi':
        kc = sp.get('hat_c', (180, 40, 40)); band = sp.get('band', (40, 50, 90))
        d.polygon([(hx0, hy + 3), (hx1, hy + 3), (hx1 - 1, hy - 5), (hx0 + 2, hy - 4)], fill=kc)
        d.rectangle([hx0, hy, hx1, hy + 3], fill=band)
        if D == 0: d.rectangle([hx0 + 1, hy + 3, hx1 - 1, hy + 5], fill=(24, 24, 28))
        elif D in (1, 2):
            vx = hx0 - 3 if D == 1 else hx1 - 3
            d.rectangle([vx, hy + 3, vx + 6, hy + 4], fill=(24, 24, 28))
    elif hat == 'svcap':        # 영국 군모(챙 달린 천 모자)
        sc = sp.get('hat_c', KHAKI)
        d.ellipse([hx0 - 2, hy - 4, hx1 + 2, hy + 3], fill=sc); d.rectangle([hx0, hy, hx1, hy + 3], fill=sh(sc, 0.82))
        if D == 0: d.rectangle([hx0 + 1, hy + 3, hx1 - 1, hy + 5], fill=sh(sc, 0.5)); px(d, cx, hy - 1, (200, 180, 110))
        elif D in (1, 2):
            vx = hx0 - 4 if D == 1 else hx1 - 2
            d.rectangle([vx, hy + 3, vx + 6, hy + 4], fill=sh(sc, 0.5))
    elif hat == 'peaked':
        d.ellipse([hx0 - 2, hy - 5, hx1 + 2, hy + 2], fill=hc); d.rectangle([hx0, hy, hx1, hy + 3], fill=sp.get('band', sh(hc, 0.6)))
        if D == 0: d.rectangle([hx0 + 1, hy + 3, hx1 - 1, hy + 5], fill=(20, 20, 24)); px(d, cx, hy - 2, sp.get('badge', (230, 200, 110)))
        elif D in (1, 2):
            vx = hx0 - 4 if D == 1 else hx1 - 2
            d.rectangle([vx, hy + 3, vx + 6, hy + 4], fill=(20, 20, 24))
    elif hat == 'russcap':
        rc = sp.get('hat_c', (236, 234, 224))
        d.ellipse([hx0 - 2, hy - 5, hx1 + 2, hy + 2], fill=rc); d.rectangle([hx0, hy, hx1, hy + 3], fill=sp.get('band', (180, 40, 40)))
        if D == 0: d.rectangle([hx0 + 1, hy + 3, hx1 - 1, hy + 5], fill=(20, 20, 24)); px(d, cx, hy - 1, (230, 120, 40))
    elif hat == 'jpcap':
        jc = sp.get('hat_c', (40, 46, 70))
        d.polygon([(hx0, hy + 3), (hx1, hy + 3), (hx1 - 1, hy - 4), (hx0 + 1, hy - 4)], fill=jc)
        d.rectangle([hx0, hy, hx1, hy + 2], fill=sp.get('band', (200, 50, 50)))
        if D == 0: d.rectangle([hx0 + 1, hy + 3, hx1 - 1, hy + 5], fill=(20, 20, 24)); px(d, cx, hy - 2, (240, 210, 90))
    elif hat == 'topee':
        tc = sp.get('hat_c', (240, 236, 222))
        d.chord([hx0 - 2, hy - 6, hx1 + 2, hy + 8], 180, 360, fill=tc)
        d.ellipse([hx0 - 4, hy + 0, hx1 + 4, hy + 5], fill=sh(tc, 0.92))
        d.line([(hx0, hy + 1), (hx1, hy + 1)], fill=sp.get('band', sh(tc, 0.75))); px(d, cx, hy - 6, sh(tc, 0.8))
    elif hat == 'turban':
        tc = sp.get('hat_c', (236, 232, 220))
        d.ellipse([hx0 - 2, hy - 5, hx1 + 2, hy + 6], fill=tc)
        d.line([(hx0 - 1, hy + 1), (cx + 3, hy - 4)], fill=sh(tc, 0.8)); d.line([(hx0, hy + 4), (hx1, hy - 1)], fill=sh(tc, 0.85))
        if sp.get('kulla') and D == 0: d.polygon([(cx - 2, hy - 4), (cx + 1, hy - 4), (cx, hy - 8)], fill=sp['kulla'])
        if sp.get('turban_tail') and D in (1, 2, 3):
            tx = hx0 - 1 if D == 1 else hx1 - 1 if D == 2 else cx - 1
            d.rectangle([tx, hy + 4, tx + 2, hy + 14], fill=tc)
    elif hat == 'fez':
        fc = sp.get('hat_c', (180, 30, 36))
        d.polygon([(cx - 6, hy + 3), (cx + 5, hy + 3), (cx + 4, hy - 6), (cx - 5, hy - 6)], fill=fc)
        d.line([(cx - 5, hy - 6), (cx + 4, hy - 6)], fill=sh(fc, 1.2)); d.line([(cx, hy - 6), (cx + (5 if D != 1 else -6), hy + 1)], fill=(20, 20, 24))
    elif hat == 'chechia':
        fc = sp.get('hat_c', (196, 30, 36))
        d.polygon([(cx - 7, hy + 3), (cx + 6, hy + 3), (cx + 5, hy - 3), (cx - 6, hy - 3)], fill=fc)
        d.line([(cx, hy - 3), (cx + (6 if D != 1 else -7), hy + 2)], fill=(30, 40, 90))
    elif hat == 'campaign':
        cc = sp.get('hat_c', (150, 130, 90))
        d.polygon([(cx - 6, hy + 1), (cx - 4, hy - 6), (cx - 1, hy - 4), (cx, hy - 7), (cx + 1, hy - 4), (cx + 3, hy - 6), (cx + 5, hy + 1)], fill=cc)
        d.ellipse([cx - 13, hy - 1, cx + 12, hy + 4], fill=sh(cc, 0.9)); d.line([(cx - 6, hy), (cx + 5, hy)], fill=sp.get('band', (60, 50, 40)))
    elif hat == 'bersagl':      # 베르살리에리: 검은 둥근 모자에 수탉 깃털 다발
        d.ellipse([cx - 11, hy - 1, cx + 10, hy + 4], fill=(30, 30, 34)); d.chord([cx - 6, hy - 5, cx + 5, hy + 4], 180, 360, fill=(30, 30, 34))
        fx = cx + (4 if D != 1 else -5)
        for k in range(6): d.line([(fx, hy - 3), (fx + (8 if D != 1 else -8) - k, hy + 2 + k * 2)], fill=(20, 40, 30) if k % 2 else (40, 70, 50))
    elif hat == 'cocked':       # 프란츠 페르디난트: 녹색 깃털이 풍성한 이각모
        d.polygon([(cx - 10, hy + 2), (cx + 9, hy + 2), (cx + 6, hy - 3), (cx - 7, hy - 3)], fill=(30, 30, 34))
        d.line([(cx - 9, hy + 1), (cx + 8, hy + 1)], fill=(220, 190, 100))
        for k in range(11):
            a = math.pi * (1.0 + k * 0.1)
            d.line([(cx, hy - 2), (cx + math.cos(a) * 11, hy - 3 + math.sin(a) * 9)], fill=(50, 140, 60) if k % 2 else (100, 190, 100), width=2)
    elif hat == 'bonnet':
        bc_ = sp.get('hat_c', (150, 90, 110))
        d.ellipse([cx - 12, hy - 2, cx + 11, hy + 4], fill=bc_); d.rounded_rectangle([cx - 6, hy - 6, cx + 5, hy + 1], 3, fill=bc_)
        d.line([(cx - 6, hy - 1), (cx + 5, hy - 1)], fill=sp.get('band', (240, 230, 220)))
        if sp.get('flower'): d.ellipse([cx + 3, hy - 4, cx + 7, hy], fill=sp['flower'])
    elif hat == 'mobcap':
        mc = sp.get('hat_c', (240, 236, 226))
        d.ellipse([hx0 - 2, hy - 4, hx1 + 2, hy + 6], fill=mc); d.line([(hx0 - 1, hy + 4), (hx1 + 1, hy + 4)], fill=sh(mc, 0.8))
    elif hat == 'nursecap':
        nc = (250, 250, 250)
        d.rounded_rectangle([hx0 - 1, hy - 2, hx1 + 1, hy + 4], 3, fill=nc)
        if D in (1, 2, 3): d.rectangle([hx0 if D != 2 else cx, hy + 2, hx1 if D != 1 else cx, hy + 14], fill=nc)
        if D == 0: d.rectangle([cx - 1, hy - 1, cx, hy + 2], fill=(210, 30, 30)); d.rectangle([cx - 2, hy, cx + 1, hy + 1], fill=(210, 30, 30))
    elif hat == 'bobby':        # 영국 경찰 헬멧
        bc_ = (30, 34, 50)
        d.rounded_rectangle([cx - 6, hy - 9, cx + 5, hy + 3], 5, fill=bc_); d.ellipse([cx - 8, hy, cx + 7, hy + 4], fill=bc_)
        if D == 0: d.ellipse([cx - 2, hy - 4, cx + 1, hy - 1], fill=(210, 210, 216)); px(d, cx, hy - 10, (200, 200, 206))
    elif hat == 'mane':         # 에티오피아 장수의 사자 갈기 머리 장식
        mc = (150, 100, 46)
        d.ellipse([hx0 - 5, hy - 7, hx1 + 5, hy + 8], fill=mc)
        for k in range(14):
            a = math.pi * (0.95 + k / 13 * 1.1)
            d.line([(cx, hy + 2), (cx + math.cos(a) * 12, hy + 2 + math.sin(a) * 10)], fill=sh(mc, 1.2 if k % 2 else 0.85))
        d.rounded_rectangle([hx0, hy + 2, hx1, hy + 16], 6, fill=skin)
        if D == 0:
            for ex in (cx - 4, cx + 3): px(d, ex, hy + 10, (14, 10, 12)); px(d, ex, hy + 9, (14, 10, 12))
            if sp.get('beard'): d.rounded_rectangle([hx0 + 1, hy + 11, hx1 - 1, hy + 17], 4, fill=sp['beard'])
    elif hat == 'feltbrim':     # 메넬리크 2세: 넓은 챙의 펠트 모자
        fc = sp.get('hat_c', (46, 40, 36))
        d.rounded_rectangle([cx - 6, hy - 7, cx + 5, hy + 2], 3, fill=fc); d.ellipse([cx - 13, hy - 1, cx + 12, hy + 4], fill=fc)
        d.rectangle([cx - 6, hy - 1, cx + 5, hy], fill=sh(fc, 1.5))
    elif hat == 'headscarf':
        sc = sp.get('hat_c', (240, 236, 226))
        d.rounded_rectangle([hx0 - 2, hy - 2, hx1 + 2, hy + 8], 5, fill=sc)
        if D in (1, 2, 3): d.rectangle([hx0 - 2, hy + 4, hx1 + 2, hy + 16], fill=sc)
        if D == 0: d.rectangle([hx0 - 2, hy + 5, hx0, hy + 15], fill=sc); d.rectangle([hx1, hy + 5, hx1 + 2, hy + 15], fill=sc)
    elif hat == 'coolie':
        cc = sp.get('hat_c', (210, 180, 120))
        d.polygon([(cx - 13, hy + 3), (cx, hy - 7), (cx + 12, hy + 3)], fill=cc); d.line([(cx - 13, hy + 3), (cx + 12, hy + 3)], fill=sh(cc, 0.7))
    elif hat == 'qingcap':      # 청나라 관모(여름): 원뿔꼴 + 붉은 술 + 꼭지 구슬
        d.polygon([(cx - 10, hy + 3), (cx, hy - 6), (cx + 9, hy + 3)], fill=(236, 226, 196))
        d.polygon([(cx - 7, hy + 2), (cx, hy - 5), (cx + 6, hy + 2)], fill=(190, 40, 40))
        d.ellipse([cx - 2, hy - 8, cx + 1, hy - 5], fill=sp.get('knob', (60, 90, 170)))
    elif hat == 'plume':        # 공화국 근위대: 은빛 투구 + 뒤로 늘어진 검은 말총 + 붉은 깃털
        if D != 0:
            hx_ = hx1 - 2 if D == 1 else (hx0 - 2 if D == 2 else cx - 2)
            d.rectangle([hx_, hy - 2, hx_ + 4, hy + 14], fill=(20, 20, 24))
        d.rounded_rectangle([hx0, hy - 5, hx1, hy + 3], 5, fill=(214, 214, 222)); d.line([(hx0 - 1, hy + 3), (hx1 + 1, hy + 3)], fill=(200, 170, 80))
        d.rectangle([cx - 1, hy - 8, cx, hy - 5], fill=(230, 200, 100))
        d.line([(cx - 4, hy - 3), (cx - 4, hy - 12)], fill=(220, 30, 40), width=2)
    elif hat == 'm1':           # 미군 M1 철모 (1941~): 둥글고 깊은 투구 + 둘레 챙
        mc = sp.get('hat_c', (92, 98, 66))
        d.chord([hx0 - 2, hy - 6, hx1 + 2, hy + 12], 180, 360, fill=mc)
        d.ellipse([hx0 - 3, hy + 1, hx1 + 3, hy + 6], fill=sh(mc, 0.85)); d.line([(hx0 - 2, hy + 3), (hx1 + 2, hy + 3)], fill=sh(mc, 0.65))
        px(d, cx - 3, hy - 3, sh(mc, 1.3)); px(d, cx - 2, hy - 4, sh(mc, 1.3))
        if sp.get('medic'): d.rectangle([cx - 2, hy - 3, cx + 1, hy + 1], fill=(250, 250, 250)); d.line([(cx - 1, hy - 3), (cx - 1, hy + 1)], fill=(200, 30, 30)); d.line([(cx - 2, hy - 1), (cx + 1, hy - 1)], fill=(200, 30, 30))
    elif hat == 'garrison':     # 접는 군모(사이드캡)
        gc_ = sp.get('hat_c', (100, 96, 70))
        d.polygon([(hx0 + 1, hy + 1), (hx1 - 1, hy + 1), (hx1 - 2, hy - 3), (hx0 + 3, hy - 4)], fill=gc_); d.line([(hx0 + 1, hy + 1), (hx1 - 1, hy + 1)], fill=sh(gc_, 0.7))
    elif hat == 'beret':
        bc2 = sp.get('hat_c', (40, 40, 50))
        d.ellipse([hx0 - 2, hy - 4, hx1 + 3, hy + 3], fill=bc2); px(d, cx, hy - 5, sh(bc2, 0.7)); d.line([(hx0, hy + 1), (hx1 - 1, hy + 1)], fill=sh(bc2, 0.7))
    elif hat == 'cloche':       # 1920년대 종 모양 여자 모자
        cc = sp.get('hat_c', (120, 60, 80))
        d.chord([hx0 - 2, hy - 5, hx1 + 2, hy + 14], 180, 360, fill=cc); d.rectangle([hx0 - 2, hy + 3, hx1 + 2, hy + 6], fill=cc)
        d.line([(hx0 - 1, hy + 2), (hx1 + 1, hy + 2)], fill=sp.get('band', sh(cc, 0.6)))
    elif hat == 'fedora':
        fc = sp.get('hat_c', (70, 64, 60))
        d.polygon([(cx - 6, hy + 1), (cx - 5, hy - 6), (cx - 1, hy - 4), (cx + 4, hy - 6), (cx + 5, hy + 1)], fill=fc)
        d.ellipse([cx - 10, hy - 1, cx + 9, hy + 3], fill=sh(fc, 0.9)); d.line([(cx - 6, hy - 1), (cx + 5, hy - 1)], fill=sp.get('band', sh(fc, 0.55)))
    elif hat == 'shako':        # 독일 경찰 모자 (원통형 + 챙)
        sc2 = sp.get('hat_c', (40, 70, 50))
        d.rectangle([cx - 6, hy - 8, cx + 5, hy + 2], fill=sc2); d.rectangle([cx - 6, hy - 8, cx + 5, hy - 7], fill=(20, 20, 20))
        d.ellipse([cx - 8, hy, cx + 7, hy + 4], fill=(20, 20, 22)); px(d, cx, hy - 4, (220, 210, 170))
    elif hat == 'warden':       # 영국 공습 경비원 철모 (검정 + 흰 W)
        d.chord([cx - 6, hy - 5, cx + 5, hy + 6], 180, 360, fill=(30, 30, 32))
        d.ellipse([cx - 12, hy - 1, cx + 11, hy + 4], fill=(36, 36, 38))
        if D in (0, 1, 2): d.line([(cx - 3, hy - 3), (cx - 2, hy), (cx, hy - 2), (cx + 1, hy), (cx + 2, hy - 3)], fill=(250, 250, 250))
    elif hat == 'headset':      # 방송 기술자 헤드폰
        d.arc([hx0 - 2, hy - 4, hx1 + 2, hy + 12], 180, 360, fill=(40, 40, 44), width=2)
        d.rectangle([hx0 - 3, hy + 5, hx0, hy + 11], fill=(40, 40, 44)); d.rectangle([hx1, hy + 5, hx1 + 3, hy + 11], fill=(40, 40, 44))
    elif hat == 'ushanka':      # 소련 털모자 (귀덮개)
        uc = sp.get('hat_c', (110, 90, 70))
        d.rounded_rectangle([hx0 - 3, hy - 6, hx1 + 3, hy + 3], 4, fill=uc); d.line([(hx0 - 2, hy + 2), (hx1 + 2, hy + 2)], fill=sh(uc, 0.7))
        if D in (0, 1, 2): d.rectangle([hx0 - 3, hy + 2, hx0, hy + 10], fill=sh(uc, 0.9)); d.rectangle([hx1, hy + 2, hx1 + 3, hy + 10], fill=sh(uc, 0.9))
        for k in range(hx0 - 2, hx1 + 2, 2): px(d, k, hy - 6, sh(uc, 1.25))
        if sp.get('badge'): d.rectangle([cx - 1, hy - 4, cx + 1, hy - 2], fill=sp['badge'])
    elif hat == 'beanie':
        d.chord([hx0 - 1, hy - 4, hx1 + 1, hy + 9], 180, 360, fill=hc); d.rectangle([hx0 - 1, hy + 1, hx1 + 1, hy + 3], fill=sh(hc, 0.75))
    elif hat == 'crown_eth':    # 타이투 황후: 흰 머릿수건 위 작은 금관
        d.rounded_rectangle([hx0 - 2, hy - 2, hx1 + 2, hy + 8], 5, fill=(246, 244, 236))
        if D in (1, 2, 3): d.rectangle([hx0 - 2, hy + 4, hx1 + 2, hy + 18], fill=(246, 244, 236))
        d.rectangle([cx - 5, hy - 5, cx + 4, hy - 1], fill=(230, 190, 80)); px(d, cx, hy - 7, (230, 190, 80)); px(d, cx - 4, hy - 6, (230, 190, 80)); px(d, cx + 3, hy - 6, (230, 190, 80))

    # ---- 고대 그리스 · 페르시아 · 마케도니아 머리 장식
    if hat == 'wreath':         # 올리브 · 월계관
        wc = sp.get('hat_c', (110, 150, 70))
        for k, qx in enumerate(range(hx0 - 1, hx1 + 2, 2)):
            px(d, qx, hy + 2 + (k % 2), wc); px(d, qx, hy + 1 + ((k + 1) % 2), sh(wc, 1.3))
    elif hat == 'corinth':      # 코린토스식 청동 투구 + 말총 볏
        bz = sp.get('hat_c', (176, 136, 70)); crest = sp.get('crest', (170, 40, 36))
        d.rounded_rectangle([hx0 - 1, hy - 2, hx1 + 1, hy + 12], 5, fill=bz)
        d.line([(hx0, hy - 1), (hx1, hy - 1)], fill=sh(bz, 1.3))
        if D == 0:
            d.rectangle([cx - 4, hy + 5, cx - 2, hy + 7], fill=(30, 24, 20)); d.rectangle([cx + 1, hy + 5, cx + 3, hy + 7], fill=(30, 24, 20))
            d.rectangle([cx - 1, hy + 5, cx, hy + 11], fill=sh(bz, 0.75)); d.rectangle([cx - 4, hy + 9, cx + 3, hy + 12], fill=skin)
        elif D in (1, 2):
            ex2 = hx0 + 1 if D == 1 else hx1 - 4
            d.rectangle([ex2, hy + 5, ex2 + 3, hy + 7], fill=(30, 24, 20))
        d.rectangle([cx - 2, hy - 8, cx + 1, hy - 2], fill=crest)
        if D in (1, 2): d.polygon([(cx - 7, hy - 6), (cx + 6, hy - 6), (cx + 8, hy + 2) if D == 1 else (cx - 9, hy + 2), (cx + 2, hy - 2)], fill=crest)
        else: d.rectangle([cx - 7, hy - 8, cx + 6, hy - 5], fill=crest)
    elif hat == 'tiara':        # 페르시아 부드러운 모자 (턱 아래까지 감싸는 천)
        tc = sp.get('hat_c', (200, 170, 90))
        d.rounded_rectangle([hx0 - 2, hy - 4, hx1 + 2, hy + 6], 4, fill=tc); d.polygon([(cx - 3, hy - 4), (cx + 2, hy - 4), (cx + 4, hy - 8)], fill=sh(tc, 0.85))
        d.rectangle([hx0 - 2, hy + 4, hx0 + 1, hy + 15], fill=tc); d.rectangle([hx1 - 1, hy + 4, hx1 + 2, hy + 15], fill=tc)
        if D == 0: d.line([(hx0 + 1, hy + 14), (hx1 - 1, hy + 14)], fill=sh(tc, 0.8))
    elif hat == 'kausia':       # 마케도니아 넓적한 펠트 모자
        kc = sp.get('hat_c', (200, 190, 170))
        d.ellipse([hx0 - 3, hy - 3, hx1 + 3, hy + 3], fill=kc); d.line([(hx0 - 2, hy + 1), (hx1 + 2, hy + 1)], fill=sh(kc, 0.7))
    elif hat == 'petasos':      # 넓은 챙 여행 모자
        pc2 = sp.get('hat_c', (200, 170, 110))
        d.ellipse([cx - 12, hy - 1, cx + 11, hy + 4], fill=pc2); d.chord([cx - 6, hy - 6, cx + 5, hy + 4], 180, 360, fill=sh(pc2, 0.9))
    elif hat == 'diadem':       # 흰 머리띠 (알렉산드로스 · 헬레니즘 왕)
        d.line([(hx0 - 1, hy + 3), (hx1 + 1, hy + 3)], fill=(244, 240, 228), width=2)
        if D in (1, 2, 3):
            tx = hx0 - 1 if D == 1 else hx1 + 1 if D == 2 else cx
            d.line([(tx, hy + 4), (tx + (-1 if D == 2 else 1), hy + 12)], fill=(244, 240, 228))
    elif hat == 'nemes':        # 이집트 줄무늬 두건
        nc = sp.get('hat_c', (220, 200, 120))
        d.rounded_rectangle([hx0 - 2, hy - 2, hx1 + 2, hy + 8], 3, fill=nc)
        d.polygon([(hx0 - 2, hy + 6), (hx0 + 2, hy + 6), (hx0 + 1, hy + 18), (hx0 - 3, hy + 18)], fill=nc); d.polygon([(hx1 - 2, hy + 6), (hx1 + 2, hy + 6), (hx1 + 3, hy + 18), (hx1 - 1, hy + 18)], fill=nc)
        for yy in range(hy - 1, hy + 18, 3): d.line([(hx0 - 2, yy), (hx0 + 1, yy)], fill=(40, 70, 130)); d.line([(hx1 - 1, yy), (hx1 + 2, yy)], fill=(40, 70, 130))

    kr_hat(d, sp, D, cx, hy, hx0, hx1, skin)
    # 손에 든 것
    if sp.get('salute') and D == 0:
        d.rounded_rectangle([cx + 8, by - 8, cx + 11, by + 2], 2, fill=aM); d.rectangle([cx + 6, hy + 4, cx + 10, hy + 7], fill=skin)
    if hold and D != 3:
        hxp = cx + 9 + wide if D in (0, 2) else cx - 12 - wide
        hyp = by + 11
        if hold == 'scroll':        # 두루마리
            d.rectangle([hxp - 3, hyp - 1, hxp + 6, hyp + 3], fill=(236, 222, 180)); d.ellipse([hxp - 4, hyp - 2, hxp - 1, hyp + 4], fill=(200, 180, 130)); d.ellipse([hxp + 4, hyp - 2, hxp + 7, hyp + 4], fill=(200, 180, 130))
        elif hold == 'amphora':     # 항아리
            ac = sp.get('pot_c', (190, 100, 50))
            d.ellipse([hxp - 3, hyp - 2, hxp + 6, hyp + 9], fill=ac); d.rectangle([hxp, hyp - 5, hxp + 3, hyp - 1], fill=ac)
            d.line([(hxp - 3, hyp + 3), (hxp + 6, hyp + 3)], fill=(30, 24, 20)); d.arc([hxp - 3, hyp - 5, hxp + 1, hyp + 1], 90, 270, fill=sh(ac, 0.7))
        elif hold == 'hoplon':      # 둥근 청동 방패
            sx = hxp - 6 if D != 1 else hxp - 3
            d.ellipse([sx - 2, hyp - 10, sx + 13, hyp + 6], fill=sp.get('shield_c', (176, 136, 70)), outline=(110, 80, 40))
            d.ellipse([sx + 3, hyp - 5, sx + 8, hyp + 1], fill=sp.get('emblem', (170, 40, 36)))
        elif hold == 'oar':         # 노
            d.line([(hxp + 1, hyp + 8), (hxp + 1, hy - 6)], fill=(150, 110, 70), width=2); d.rectangle([hxp - 1, hyp + 8, hxp + 3, hyp + 14], fill=(150, 110, 70))
        elif hold == 'ostrakon':    # 도자기 조각
            d.polygon([(hxp - 2, hyp), (hxp + 4, hyp - 2), (hxp + 5, hyp + 4), (hxp - 1, hyp + 5)], fill=(196, 110, 70)); d.line([(hxp - 1, hyp + 2), (hxp + 3, hyp + 1)], fill=(40, 30, 26))
        elif hold == 'tablet':      # 밀랍 서판
            d.rectangle([hxp - 3, hyp - 2, hxp + 5, hyp + 6], fill=(150, 110, 70)); d.rectangle([hxp - 2, hyp - 1, hxp + 4, hyp + 5], fill=(110, 90, 60))
        elif hold == 'gnomon':      # 해시계 막대 · 측량 막대
            d.line([(hxp + 1, hyp + 8), (hxp + 1, hy - 10)], fill=(230, 220, 190), width=2)
        if hold == 'telegram':
            d.rectangle([hxp - 2, hyp - 1, hxp + 5, hyp + 4], fill=(246, 226, 160)); d.line([(hxp - 2, hyp - 1), (hxp + 1, hyp + 2), (hxp + 5, hyp - 1)], fill=(170, 130, 60))
        elif hold == 'mic':
            d.rectangle([hxp, hyp - 8, hxp + 4, hyp - 1], fill=(40, 40, 46)); d.rectangle([hxp + 1, hyp - 1, hxp + 3, hyp + 6], fill=(150, 150, 156))
            d.line([(hxp + 1, hyp - 6), (hxp + 3, hyp - 6)], fill=(180, 180, 190)); d.line([(hxp + 1, hyp - 4), (hxp + 3, hyp - 4)], fill=(180, 180, 190))
        elif hold == 'suitcase':
            d.rectangle([hxp - 4, hyp + 1, hxp + 6, hyp + 8], fill=(120, 80, 50)); d.line([(hxp - 1, hyp), (hxp + 3, hyp)], fill=(60, 40, 30)); d.line([(hxp - 4, hyp + 4), (hxp + 6, hyp + 4)], fill=(90, 60, 36))
        elif hold == 'money':       # 지폐 다발
            for k in range(3): d.rectangle([hxp - 3 + k, hyp - 3 - k * 2, hxp + 6 + k, hyp + 1 - k * 2], fill=(186, 196, 150) if k % 2 else (166, 176, 130), outline=(110, 120, 90))
        elif hold == 'apple':
            d.rectangle([hxp - 4, hyp, hxp + 6, hyp + 6], fill=(140, 100, 60)); d.ellipse([hxp - 3, hyp - 3, hxp + 1, hyp + 1], fill=(200, 40, 40)); d.ellipse([hxp + 1, hyp - 3, hxp + 5, hyp + 1], fill=(210, 50, 40))
        elif hold == 'clip':
            d.rectangle([hxp - 2, hyp - 3, hxp + 5, hyp + 6], fill=(150, 110, 70)); d.rectangle([hxp - 1, hyp - 1, hxp + 4, hyp + 5], fill=(240, 236, 220)); d.rectangle([hxp, hyp - 4, hxp + 3, hyp - 2], fill=(160, 160, 166))
        elif hold == 'camera':
            d.rectangle([hxp - 3, hyp - 2, hxp + 5, hyp + 4], fill=(30, 30, 32)); d.ellipse([hxp - 1, hyp - 1, hxp + 3, hyp + 3], fill=(90, 110, 130))
        elif hold == 'blanket':
            d.rectangle([hxp - 4, hyp - 6, hxp + 4, hyp + 4], fill=(150, 120, 100)); d.line([(hxp - 4, hyp - 2), (hxp + 4, hyp - 2)], fill=(110, 80, 60))
        elif hold == 'paper':
            d.rectangle([hxp - 2, hyp - 2, hxp + 5, hyp + 6], fill=(240, 234, 214)); d.line([(hxp - 1, hyp), (hxp + 4, hyp)], fill=(80, 80, 80)); d.line([(hxp - 1, hyp + 2), (hxp + 3, hyp + 2)], fill=(80, 80, 80))
        elif hold == 'news':
            d.rectangle([hxp - 3, hyp - 4, hxp + 6, hyp + 6], fill=(236, 232, 214)); d.rectangle([hxp - 2, hyp - 3, hxp + 5, hyp - 1], fill=(40, 40, 40))
            for yy in (hyp + 1, hyp + 3): d.line([(hxp - 2, yy), (hxp + 5, yy)], fill=(130, 130, 130))
        elif hold.startswith('flag:'):
            code = hold.split(':')[1]
            d.line([(hxp + 1, hyp + 3), (hxp + 1, hy - 4)], fill=(150, 120, 80))
            fl = mini_flag(code, 11, 7); lay.alpha_composite(fl, (hxp + 2, hy - 4))
        elif hold == 'rifle':
            d.line([(hxp + 1, hyp + 6), (hxp + 1, hy - 4)], fill=(80, 60, 44), width=2); d.line([(hxp + 1, hy - 4), (hxp + 1, hy - 8)], fill=(150, 150, 156))
        elif hold == 'spear':
            d.line([(hxp + 1, hyp + 6), (hxp + 1, hy - 8)], fill=(120, 90, 60)); d.polygon([(hxp, hy - 8), (hxp + 2, hy - 8), (hxp + 1, hy - 13)], fill=(190, 190, 196))
        elif hold == 'shield_eth':
            sx = hxp - 3 if D != 1 else hxp - 2
            d.ellipse([sx - 2, hyp - 8, sx + 8, hyp + 4], fill=(110, 70, 40), outline=(60, 40, 24)); px(d, sx + 3, hyp - 2, (220, 190, 110))
        elif hold == 'spool':
            d.ellipse([hxp - 3, hyp - 2, hxp + 6, hyp + 7], fill=(110, 80, 50)); d.ellipse([hxp, hyp + 1, hxp + 3, hyp + 4], fill=(60, 60, 64))
        elif hold == 'book':
            d.rectangle([hxp - 2, hyp - 1, hxp + 4, hyp + 6], fill=(60, 70, 110)); d.line([(hxp + 4, hyp - 1), (hxp + 4, hyp + 6)], fill=(230, 220, 190))
        elif hold == 'basket':
            d.ellipse([hxp - 4, hyp, hxp + 6, hyp + 7], fill=(170, 130, 80)); d.arc([hxp - 3, hyp - 5, hxp + 5, hyp + 3], 180, 360, fill=(140, 100, 60))
        elif hold == 'candle':
            d.rectangle([hxp, hyp - 4, hxp + 2, hyp + 2], fill=(246, 240, 220)); px(d, hxp + 1, hyp - 6, (255, 210, 80)); px(d, hxp + 1, hyp - 5, (255, 160, 60))
        elif hold == 'football':
            d.ellipse([hxp - 2, hyp, hxp + 5, hyp + 6], fill=(150, 96, 56)); d.line([(hxp - 1, hyp + 3), (hxp + 4, hyp + 3)], fill=(240, 230, 210))
        elif hold == 'bag':
            d.rounded_rectangle([hxp - 3, hyp, hxp + 6, hyp + 8], 2, fill=sp.get('bundle_c', (90, 60, 40)))
        elif hold == 'cane':
            d.line([(hxp + 1, hyp - 2), (hxp + 1, foot)], fill=(70, 50, 34)); d.line([(hxp + 1, hyp - 2), (hxp - 2, hyp - 3)], fill=(70, 50, 34))
        elif hold == 'lantern':
            d.line([(hxp + 1, hyp), (hxp + 1, hyp + 3)], fill=(60, 60, 60)); d.rectangle([hxp - 2, hyp + 3, hxp + 4, hyp + 9], fill=(250, 210, 110), outline=(60, 50, 40))
        elif hold == 'umbrella':
            d.line([(hxp + 1, hyp - 6), (hxp + 1, foot - 2)], fill=(30, 30, 34))
        elif hold == 'cup':
            d.rectangle([hxp - 1, hyp - 2, hxp + 3, hyp + 3], fill=(240, 240, 240))
        elif hold == 'pen':
            d.line([(hxp, hyp + 2), (hxp + 4, hyp - 3)], fill=(30, 30, 30))
        elif hold == 'shell':
            d.rounded_rectangle([hxp - 2, hyp - 5, hxp + 3, hyp + 6], 2, fill=(200, 160, 80)); d.rectangle([hxp - 2, hyp + 4, hxp + 3, hyp + 6], fill=(170, 120, 60))
        elif hold == 'phone':
            d.rectangle([hxp - 3, hyp, hxp + 6, hyp + 6], fill=(70, 60, 44)); d.line([(hxp - 2, hyp - 2), (hxp + 5, hyp - 2)], fill=(30, 30, 30), width=2)
        elif hold == 'bucket':
            d.polygon([(hxp - 3, hyp), (hxp + 6, hyp), (hxp + 5, hyp + 7), (hxp - 2, hyp + 7)], fill=(130, 136, 140)); d.arc([hxp - 3, hyp - 4, hxp + 6, hyp + 4], 180, 360, fill=(80, 80, 80))
        elif hold == 'sign':
            d.line([(hxp + 1, hyp + 4), (hxp + 1, hy + 2)], fill=(150, 120, 80))
            d.rectangle([hxp - 4, hy - 4, hxp + 7, hy + 6], fill=(244, 240, 228), outline=(80, 70, 60))
            d.line([(hxp - 2, hy - 1), (hxp + 5, hy - 1)], fill=(170, 40, 40)); d.line([(hxp - 2, hy + 2), (hxp + 4, hy + 2)], fill=(40, 40, 40))
        elif hold == 'bottle':
            d.rectangle([hxp, hyp - 3, hxp + 3, hyp + 4], fill=(60, 90, 60)); d.rectangle([hxp + 1, hyp - 6, hxp + 2, hyp - 3], fill=(60, 90, 60))
        elif hold == 'sack':        # 석탄 · 밀가루 자루
            sc_ = sp.get('sack_c', (70, 66, 60))
            d.rounded_rectangle([hxp - 5, hyp - 4, hxp + 7, hyp + 8], 3, fill=sc_); d.line([(hxp - 3, hyp - 2), (hxp + 5, hyp - 2)], fill=sh(sc_, 0.7))
        elif hold == 'parachute':   # 손수건 낙하산 사탕
            d.chord([hxp - 5, hyp - 10, hxp + 7, hyp + 2], 180, 360, fill=(250, 250, 250)); d.line([(hxp - 5, hyp - 4), (hxp + 1, hyp + 3)], fill=(150, 150, 150)); d.line([(hxp + 7, hyp - 4), (hxp + 1, hyp + 3)], fill=(150, 150, 150))
            d.rectangle([hxp, hyp + 2, hxp + 3, hyp + 5], fill=(220, 60, 60))
        elif hold == 'hammer':      # 장벽 조각을 쪼는 망치
            d.line([(hxp + 1, hyp + 6), (hxp + 1, hyp - 5)], fill=(150, 110, 70), width=2); d.rectangle([hxp - 3, hyp - 7, hxp + 5, hyp - 4], fill=(110, 110, 116))
        elif hold == 'flower':
            d.line([(hxp + 1, hyp + 5), (hxp + 1, hyp - 4)], fill=(60, 120, 60)); d.ellipse([hxp - 2, hyp - 8, hxp + 4, hyp - 2], fill=sp.get('flower_c', (230, 60, 80)))
        elif hold == 'folder':
            d.rectangle([hxp - 3, hyp - 2, hxp + 6, hyp + 7], fill=sp.get('folder_c', (200, 170, 90))); d.line([(hxp - 3, hyp), (hxp + 6, hyp)], fill=(150, 120, 60))
        elif hold == 'tray':
            d.rectangle([hxp - 5, hyp - 1, hxp + 7, hyp + 1], fill=(200, 200, 200)); d.rectangle([hxp - 3, hyp - 4, hxp, hyp - 1], fill=(250, 250, 250)); d.rectangle([hxp + 2, hyp - 4, hxp + 5, hyp - 1], fill=(250, 250, 250))
    # 머리에 인 것
    if pack == 'head':
        bc_ = sp.get('bundle_c', (170, 130, 80))
        d.ellipse([cx - 9, hy - 8, cx + 8, hy + 1], fill=bc_); d.line([(cx - 7, hy - 5), (cx + 6, hy - 5)], fill=sh(bc_, 0.75))
        if sp.get('load'): d.ellipse([cx - 6, hy - 11, cx + 5, hy - 5], fill=sp['load'])
    if pack == 'bundle' and D in (1, 2, 3):
        bx = cx + (6 if D == 1 else -13 if D == 2 else -7)
        d.rounded_rectangle([bx, ny - 1, bx + 13 if D == 3 else bx + 8, ny + 11], 3, fill=sp.get('bundle_c', (110, 130, 170)))
    if pack == 'satchel' and D in (0, 1, 2):     # 전보 가방 (어깨끈 + 옆구리 가방)
        if D == 0: d.line([(cx - 7, ny), (cx + 7, ny + 11)], fill=(60, 40, 28))
        bx = cx + (6 if D in (0, 2) else -12)
        d.rounded_rectangle([bx, ny + 9, bx + 6, ny + 15], 1, fill=(90, 62, 40)); d.line([(bx, ny + 11), (bx + 6, ny + 11)], fill=(60, 40, 28))
    if pack == 'gasbag' and D in (0, 1, 2):
        bx = cx + (-11 if D in (0, 1) else 5)
        d.rounded_rectangle([bx, ny + 7, bx + 6, ny + 14], 2, fill=sh(cloth, 0.9))
    if sp.get('gasmask') and D != 3:
        mc = (110, 106, 86)
        if D == 0:
            d.rounded_rectangle([hx0 + 1, hy + 6, hx1 - 1, hy + 16], 3, fill=mc)
            d.ellipse([cx - 6, hy + 7, cx - 2, hy + 11], fill=(200, 210, 200)); d.ellipse([cx + 1, hy + 7, cx + 5, hy + 11], fill=(200, 210, 200))
            d.rectangle([cx - 1, hy + 13, cx, hy + 20], fill=(70, 70, 66))
        else:
            gx = hx0 if D == 1 else cx - 2
            d.rounded_rectangle([gx, hy + 6, gx + 10, hy + 16], 3, fill=mc)
            d.ellipse([gx + (1 if D == 1 else 5), hy + 7, gx + (5 if D == 1 else 9), hy + 11], fill=(200, 210, 200))
    if sp.get('canary'):    # 군수 공장 노동자: 화약(TNT) 때문에 노랗게 물든 피부를 살짝 표현
        pass
    kr_hold(d, sp, D, cx, hy, by, foot, wide, hold, lay)
    return lay

def sheet(sp, path):
    out = Image.new('RGBA', (144, FH * 4), (0, 0, 0, 0))
    for D in range(4):
        for st in range(3):
            out.alpha_composite(outline(draw(sp, D, st), 0.5), (st * 48, D * FH))
    out.save(path)


# ================================================================== 조선 (1863~1882) 옷 · 머리 · 갓 · 소품
DONG = (252, 252, 246)          # 동정 (흰 깃)
def kr_body(d, sp, D, cx, by, bx0, bx1, cloth, sway, foot, ny, top):
    """한복 깃 · 고름 · 흉배 · 전복(조끼) · 띠"""
    cS = sh(cloth, 0.78); cD = sh(cloth, 0.6)
    hanbok = top in ('po', 'jeo') or sp.get('hanbok')
    if sp.get('jeonbok'):           # 전복 · 쾌자 (소매 없는 긴 조끼, 군복)
        jc = sp['jeonbok']; jL, jM, jS, jD = tone(jc)
        if D in (0, 3):
            d.rectangle([bx0 + 1, by, bx1 - 1, by + 11], fill=jM)
            d.polygon([(bx0 + 1, by + 10), (bx1 - 1, by + 10), (bx1 + 1 + sway, foot - 6), (bx0 - 1 + sway, foot - 6)], fill=jM)
            if D == 0:
                d.line([(cx, by + 2), (cx + sway, foot - 6)], fill=jD)
                d.polygon([(cx - 4, by - 1), (cx + 3, by - 1), (cx, by + 4)], fill=sh(cloth, 1.0))
            else:
                d.line([(cx, by + 12), (cx + sway, foot - 6)], fill=jD)      # 뒤트임
        else:
            d.rectangle([cx - 6, by, cx + 5, by + 11], fill=jM)
            d.polygon([(cx - 6, by + 10), (cx + 5, by + 10), (cx + 6 + sway, foot - 6), (cx - 7 + sway, foot - 6)], fill=jM)
    if D == 0 and hanbok and not sp.get('jeonbok'):
        gc = sp.get('git', cD)
        d.polygon([(cx - 5, by - 1), (cx - 2, by - 1), (cx + 4, by + 6), (cx + 1, by + 7)], fill=gc)      # 깃
        d.line([(cx - 5, by - 1), (cx + 2, by + 6)], fill=DONG)                                                # 동정
        d.line([(cx + 4, by - 1), (cx + 1, by + 2)], fill=DONG)
        g = sp.get('goreum', sh(cloth, 0.7) if top != 'dress' else (190, 50, 60))
        d.rectangle([cx + 1, by + 6, cx + 3, by + 7], fill=g)
        d.line([(cx + 2, by + 7), (cx + 1, by + 13)], fill=g); d.line([(cx + 3, by + 7), (cx + 4, by + 12)], fill=sh(g, 0.85))
    if D == 0 and top == 'dress' and sp.get('hanbok'):
        d.rectangle([cx - 8, by + 7, cx + 7, by + 8], fill=sh(sp.get('skirt', cloth), 0.8))   # 치마 말기
    if top == 'dan':                # 단령 (관복: 둥근 깃 · 흉배 · 각대)
        if D == 0:
            d.arc([cx - 5, by - 4, cx + 4, by + 4], 0, 180, fill=sh(cloth, 0.55), width=2)
            d.arc([cx - 4, by - 3, cx + 3, by + 2], 0, 180, fill=DONG)
            hb = sp.get('hyungbae')
            if hb: d.rectangle([cx - 4, by + 3, cx + 3, by + 9], fill=hb); d.rectangle([cx - 3, by + 4, cx + 2, by + 8], outline=sh(hb, 0.7))
            if sp.get('dragon'):        # 곤룡포: 가슴 · 어깨의 금빛 둥근 용 무늬
                gd = (232, 196, 90)
                d.ellipse([cx - 4, by + 2, cx + 3, by + 9], fill=gd); d.ellipse([bx0 - 1, by - 1, bx0 + 3, by + 3], fill=gd); d.ellipse([bx1 - 3, by - 1, bx1 + 1, by + 3], fill=gd)
        bt = sp.get('gakdae', (40, 34, 30))
        if D in (0, 3):
            d.polygon([(bx0, by + 10), (bx1, by + 10), (bx1 + 1, by + 12), (bx0 - 1, by + 12)], fill=bt)
            if D == 0:
                for xx in range(bx0 + 1, bx1, 3): d.point((xx, by + 11), fill=(220, 190, 100))
        if D == 3 and sp.get('hyungbae'): d.rectangle([cx - 4, by + 2, cx + 3, by + 8], fill=sp['hyungbae'])
    if sp.get('tti') and D in (0, 3):     # 세조대 (도포 가슴 띠)
        tc = sp['tti']
        d.line([(bx0, by + 7), (bx1, by + 7)], fill=tc)
        if D == 0: d.line([(cx + 3, by + 7), (cx + 3, by + 16)], fill=tc); d.line([(cx + 5, by + 7), (cx + 6, by + 15)], fill=tc)
    if sp.get('jeondae') and D in (0, 3):  # 전대 (군복 허리띠)
        d.rectangle([bx0, by + 9, bx1, by + 11], fill=sp['jeondae'])
        if D == 0: d.line([(cx - 3, by + 11), (cx - 4, by + 17)], fill=sp['jeondae'], width=2)
    if sp.get('daenim') and top == 'jeo':  # 바지 발목 대님
        for fx in (cx - 6, cx + 1):
            d.line([(fx, foot - 3), (fx + 4, foot - 3)], fill=sp['daenim'])
    if sp.get('obi') and D in (0, 3):      # 기모노 허리띠
        d.rectangle([bx0, by + 7, bx1, by + 11], fill=sp['obi'])
    if sp.get('badge_circle') and D in (0, 3):    # 청 군사 · 둥근 표 (勇)
        d.ellipse([cx - 4, by + 2, cx + 3, by + 9], fill=(244, 238, 220)); d.rectangle([cx - 2, by + 4, cx + 1, by + 7], outline=(30, 26, 24)); d.point((cx, by + 3), fill=(30, 26, 24))

def kr_hair_extra(d, sp, D, cx, hy, hx0, hx1, kind, hairtone):
    hL, hM, hS, hD = hairtone
    if kind == 'sangtu' and not sp.get('hat') in ('gat', 'samo', 'ikseon', 'jeolip', 'waryong', 'tanggeon', 'paeraengi', 'bachi'):
        d.ellipse([cx - 3, hy - 5, cx + 2, hy + 1], fill=hM); px(d, cx - 1, hy - 4, hL)            # 상투
    if kind == 'sangtu' and D != 3 and sp.get('hat') not in ('samo', 'ikseon', 'tanggeon'):
        d.line([(hx0, hy + 3), (hx1, hy + 3)], fill=(30, 26, 26))                                  # 망건
    if kind in ('jjok', 'daenggi', 'center') and D == 0:
        d.line([(cx, hy), (cx, hy + 4)], fill=hD)                                                  # 가운데 가르마
    if kind == 'jjok':
        if D == 3: d.line([(cx - 6, hy + 14), (cx + 5, hy + 14)], fill=(220, 190, 90))               # 비녀
        elif D in (1, 2):
            bx = hx1 - 1 if D == 1 else hx0 - 4
            d.line([(bx - 2, hy + 12), (bx + 7, hy + 12)], fill=(220, 190, 90))
    if kind == 'daenggi':
        rb = sp.get('ribbon', (190, 40, 50))
        if D == 3: d.rectangle([cx - 2, hy + 26, cx + 2, hy + 30], fill=rb)
        elif D in (1, 2):
            bx = hx1 if D == 1 else hx0 - 2
            d.rectangle([bx - 1, hy + 23, bx + 3, hy + 27], fill=rb)

KR_HATS = {'gat', 'samo', 'ikseon', 'jeolip', 'paeraengi', 'waryong', 'tanggeon', 'headband', 'bachi', 'skullcap', 'jobawi', 'gat_white', 'satgat'}
def kr_hat(d, sp, D, cx, hy, hx0, hx1, skin):
    hat = sp.get('hat')
    if hat not in KR_HATS: return
    hc = sp.get('hat_c', (34, 30, 30))
    if hat in ('gat', 'gat_white'):             # 갓 (흑립): 넓은 챙 + 높은 원통 대우 + 갓끈
        gc = hc if hat == 'gat' else (236, 234, 226)
        d.rounded_rectangle([cx - 5, hy - 10, cx + 4, hy + 1], 2, fill=gc)
        d.line([(cx - 4, hy - 9), (cx - 4, hy - 1)], fill=sh(gc, 1.6) if hat == 'gat' else sh(gc, 0.85))
        d.ellipse([cx - 14, hy - 1, cx + 13, hy + 4], fill=gc)
        d.ellipse([cx - 13, hy, cx + 12, hy + 3], outline=sh(gc, 1.5) if hat == 'gat' else sh(gc, 0.8))
        d.line([(cx - 5, hy - 1), (cx + 4, hy - 1)], fill=sh(gc, 0.6) if hat == 'gat' else (40, 40, 40))
        if D == 0:
            sc_ = sp.get('gatkkeun', (40, 34, 30))
            # 얼굴 양옆 가장자리를 따라 내려와 턱 아래에서 모이게 (눈 밑을 지나지 않게)
            d.line([(hx0 - 1, hy + 4), (hx0 - 1, hy + 11), (cx - 3, hy + 17), (cx - 3, hy + 22)], fill=sc_)
            d.line([(hx1 + 1, hy + 4), (hx1 + 1, hy + 11), (cx + 2, hy + 17), (cx + 2, hy + 22)], fill=sc_)
        # 옆모습에서는 갓끈을 그리지 않는다 (얼굴을 가로지르는 줄처럼 보여서)
    elif hat == 'satgat':                        # 삿갓 (넓은 대나무 갓)
        sc = sp.get('hat_c', (196, 170, 116))
        d.polygon([(cx - 14, hy + 4), (cx, hy - 8), (cx + 13, hy + 4)], fill=sc); d.line([(cx - 14, hy + 4), (cx + 13, hy + 4)], fill=sh(sc, 0.7))
    elif hat == 'samo':                         # 사모 (관리 모자: 두 단 + 양쪽 날개)
        d.rounded_rectangle([hx0, hy - 5, hx1, hy + 4], 4, fill=hc)
        d.ellipse([cx - 5, hy - 11, cx + 4, hy - 1], fill=hc)
        d.line([(hx0 + 1, hy - 3), (hx1 - 1, hy - 3)], fill=sh(hc, 1.8))
        if D in (0, 3):
            d.ellipse([hx0 - 9, hy - 6, hx0, hy - 1], fill=hc); d.ellipse([hx1, hy - 6, hx1 + 9, hy - 1], fill=hc)
            d.ellipse([hx0 - 8, hy - 5, hx0 - 2, hy - 2], outline=sh(hc, 1.8)); d.ellipse([hx1 + 2, hy - 5, hx1 + 8, hy - 2], outline=sh(hc, 1.8))
        else:
            wx = hx1 - 2 if D == 1 else hx0 - 6
            d.ellipse([wx, hy - 9, wx + 8, hy - 3], fill=hc)
    elif hat == 'ikseon':                       # 익선관 (임금: 위로 선 매미 날개)
        d.rounded_rectangle([hx0, hy - 5, hx1, hy + 4], 4, fill=hc); d.ellipse([cx - 5, hy - 11, cx + 4, hy - 1], fill=hc)
        d.line([(hx0 + 1, hy - 3), (hx1 - 1, hy - 3)], fill=(200, 170, 90))
        for wx in (cx - 9, cx + 4):
            d.ellipse([wx, hy - 17, wx + 5, hy - 7], fill=hc); d.ellipse([wx + 1, hy - 16, wx + 4, hy - 8], outline=sh(hc, 1.8))
    elif hat == 'jeolip':                       # 전립 · 벙거지 (군사): 둥근 꼭대기 + 붉은 상모
        d.chord([cx - 7, hy - 8, cx + 6, hy + 4], 180, 360, fill=hc); d.rectangle([cx - 7, hy - 2, cx + 6, hy + 1], fill=hc)
        d.ellipse([cx - 11, hy - 1, cx + 10, hy + 4], fill=sh(hc, 0.92))
        d.line([(cx - 6, hy - 1), (cx + 5, hy - 1)], fill=sp.get('band', (150, 40, 40)))
        tc = sp.get('tassel', (200, 40, 40))
        d.ellipse([cx - 2, hy - 11, cx + 1, hy - 7], fill=tc)
        for k in (-3, -1, 1, 3): d.line([(cx, hy - 8), (cx + k, hy - 3)], fill=tc)
        if sp.get('feather'):                   # 장수의 공작 깃
            fc = sp['feather']; fx = cx + (3 if D != 2 else -4)
            d.line([(fx, hy - 8), (fx + (5 if D != 2 else -5), hy - 18)], fill=fc, width=2); d.ellipse([fx + (3 if D != 2 else -7), hy - 21, fx + (7 if D != 2 else -3), hy - 16], fill=(60, 120, 150))
    elif hat == 'paeraengi':                    # 패랭이 (보부상 · 상민의 대나무 갓)
        pc = sp.get('hat_c', (206, 182, 126))
        d.rounded_rectangle([cx - 5, hy - 7, cx + 4, hy + 1], 2, fill=pc); d.ellipse([cx - 12, hy - 1, cx + 11, hy + 3], fill=pc)
        d.line([(cx - 5, hy - 1), (cx + 4, hy - 1)], fill=(40, 34, 30))
        if sp.get('cotton'):                    # 보부상의 목화송이
            d.ellipse([cx + 3, hy - 9, cx + 8, hy - 4], fill=(250, 250, 246)); d.ellipse([cx - 9, hy - 9, cx - 4, hy - 4], fill=(250, 250, 246))
    elif hat == 'waryong':                      # 와룡관 · 정자관 (높은 검은 관)
        d.polygon([(hx0 + 1, hy + 3), (hx1 - 1, hy + 3), (hx1 - 2, hy - 7), (cx + 2, hy - 12), (cx - 3, hy - 12), (hx0 + 2, hy - 7)], fill=hc)
        d.line([(cx - 5, hy - 8), (cx + 4, hy - 8)], fill=sh(hc, 1.9)); d.line([(cx, hy - 12), (cx, hy + 2)], fill=sh(hc, 1.6))
    elif hat == 'tanggeon':                     # 탕건 (집 안에서 쓰는 관)
        d.polygon([(hx0, hy + 4), (hx1, hy + 4), (hx1 - 1, hy - 4), (cx + 3, hy - 4), (cx + 3, hy - 7), (cx - 4, hy - 7), (cx - 4, hy - 4), (hx0 + 1, hy - 4)], fill=hc)
        d.line([(hx0, hy + 2), (hx1, hy + 2)], fill=sh(hc, 1.7))
    elif hat == 'headband':                     # 머리 수건 (일꾼)
        bc = sp.get('hat_c', (240, 236, 226))
        d.rectangle([hx0 - 1, hy + 2, hx1 + 1, hy + 4], fill=bc)
        if D in (1, 2, 3):
            kx = hx0 - 2 if D in (1, 3) else hx1
            d.line([(kx, hy + 3), (kx + (-2 if D == 1 else 2), hy + 7)], fill=bc)
    elif hat == 'bachi':                        # 프랑스 수병 모자 (붉은 방울)
        bc = sp.get('hat_c', (30, 40, 70))
        d.ellipse([hx0 - 2, hy - 3, hx1 + 2, hy + 3], fill=bc); d.rectangle([hx0, hy + 1, hx1, hy + 3], fill=sh(bc, 0.7))
        d.ellipse([cx - 2, hy - 6, cx + 1, hy - 2], fill=(210, 40, 40))
    elif hat == 'skullcap':                     # 청 상인의 둥근 비단 모자
        d.chord([hx0, hy - 4, hx1, hy + 8], 180, 360, fill=hc); px(d, cx, hy - 5, (200, 40, 40)); px(d, cx - 1, hy - 5, (200, 40, 40))
    elif hat == 'jobawi':                       # 조바위 (여자 겨울 쓰개)
        jc = sp.get('hat_c', (90, 50, 90))
        d.chord([hx0 - 2, hy - 2, hx1 + 2, hy + 12], 180, 360, fill=jc); d.ellipse([cx - 3, hy - 3, cx + 2, hy + 1], fill=sh(jc, 1.4))
        if D in (0, 1, 2): d.rectangle([hx0 - 2, hy + 4, hx0, hy + 12], fill=jc); d.rectangle([hx1, hy + 4, hx1 + 2, hy + 12], fill=jc)
        if D == 0: d.line([(cx, hy + 1), (cx, hy + 5)], fill=(200, 60, 60))

def kr_hold(d, sp, D, cx, hy, by, foot, wide, hold, lay):
    pack = sp.get('pack')
    if pack == 'jige' and D in (1, 2, 3):          # 지게
        jx = cx + (6 if D == 1 else -9 if D == 2 else -7)
        for k in (0, 6 if D == 3 else 4):
            d.line([(jx + k, by - 8), (jx + k, foot - 2)], fill=(130, 96, 60), width=2)
        for yy in (by, by + 8): d.line([(jx, yy), (jx + (6 if D == 3 else 4), yy)], fill=(130, 96, 60))
        if sp.get('load'): d.rounded_rectangle([jx - 2, by - 14, jx + (9 if D == 3 else 7), by - 2], 2, fill=sp['load'])
    if pack == 'jige' and D == 0:
        d.line([(cx - 6, by), (cx - 6, by + 8)], fill=(110, 80, 50)); d.line([(cx + 5, by), (cx + 5, by + 8)], fill=(110, 80, 50))
    if pack == 'pole_load' and D in (0, 1, 2):     # 어깨에 멘 짐
        d.line([(cx - 14, by - 1), (cx + 13, by - 1)], fill=(130, 96, 60), width=2)
    if not hold or D == 3: return
    hxp = cx + 9 + wide if D in (0, 2) else cx - 12 - wide
    hyp = by + 11
    if hold == 'hwando':            # 환도 (허리에 찬 칼)
        d.line([(hxp - 2, hyp - 2), (hxp + 4, hyp + 12)], fill=(40, 34, 30), width=2); d.line([(hxp - 3, hyp - 3), (hxp - 1, hyp - 5)], fill=(200, 170, 90), width=2)
    elif hold == 'fan':             # 합죽선
        d.polygon([(hxp, hyp + 3), (hxp - 4, hyp - 5), (hxp + 6, hyp - 5)], fill=(240, 232, 210)); d.line([(hxp, hyp + 3), (hxp, hyp + 7)], fill=(150, 110, 70))
    elif hold == 'pipe':            # 곰방대 (긴 담뱃대)
        d.line([(hxp + 1, hyp + 2), (hxp + 1, hy + 8)], fill=(110, 76, 48)); d.rectangle([hxp, hy + 6, hxp + 3, hy + 8], fill=(150, 150, 156))
    elif hold == 'brush':           # 붓
        d.line([(hxp, hyp + 3), (hxp + 4, hyp - 4)], fill=(120, 90, 60)); px(d, hxp - 1, hyp + 4, (20, 20, 20))
    elif hold == 'sangso':          # 상소문 (길게 펼친 두루마리)
        d.rectangle([hxp - 3, hyp - 6, hxp + 4, hyp + 9], fill=(240, 234, 214)); d.rectangle([hxp - 4, hyp - 7, hxp + 5, hyp - 5], fill=(150, 110, 70))
        for yy in range(hyp - 3, hyp + 8, 3): d.line([(hxp - 2, yy), (hxp + 3, yy)], fill=(70, 60, 50))
    elif hold == 'matchlock':       # 화승총 (조선 군사)
        d.line([(hxp + 1, hyp + 6), (hxp + 1, hy - 6)], fill=(110, 76, 48), width=2); d.line([(hxp + 1, hy - 6), (hxp + 1, hy - 10)], fill=(70, 70, 74))
    elif hold == 'spear_k':         # 창
        d.line([(hxp + 1, hyp + 6), (hxp + 1, hy - 9)], fill=(120, 90, 60)); d.polygon([(hxp - 1, hy - 9), (hxp + 3, hy - 9), (hxp + 1, hy - 15)], fill=(200, 200, 206))
        d.line([(hxp - 1, hy - 8), (hxp + 3, hy - 8)], fill=(200, 40, 40))
    elif hold == 'rice':            # 쌀자루
        d.rounded_rectangle([hxp - 4, hyp - 4, hxp + 6, hyp + 8], 3, fill=(226, 214, 180)); d.line([(hxp - 2, hyp - 2), (hxp + 4, hyp - 2)], fill=(150, 130, 90))
    elif hold == 'coin':            # 엽전 꾸러미
        for k in range(4): d.ellipse([hxp - 2, hyp - 4 + k * 3, hxp + 4, hyp - 1 + k * 3], fill=(150, 120, 60), outline=(90, 70, 40))
    elif hold == 'flag_suja':       # 수자기 (장수 깃발)
        d.line([(hxp + 1, hyp + 6), (hxp + 1, hy - 14)], fill=(110, 80, 50), width=2)
        d.rectangle([hxp + 2, hy - 14, hxp + 14, hy - 2], fill=(226, 200, 120)); d.text((hxp + 4, hy - 13), '帥', fill=(30, 26, 22))
    elif hold == 'telescope':       # 망원경
        d.line([(hxp - 2, hyp - 2), (hxp + 6, hyp - 6)], fill=(150, 120, 60), width=3)
    elif hold == 'tray_k':          # 소반
        d.ellipse([hxp - 6, hyp - 2, hxp + 8, hyp + 2], fill=(150, 100, 60)); d.ellipse([hxp - 2, hyp - 5, hxp + 3, hyp - 1], fill=(240, 240, 236))
    elif hold == 'ledger':          # 장부
        d.rectangle([hxp - 3, hyp - 2, hxp + 5, hyp + 7], fill=(200, 170, 110)); d.line([(hxp + 1, hyp - 2), (hxp + 1, hyp + 7)], fill=(120, 90, 50))
    elif hold == 'lamp_oil':        # 석유 남포등
        d.line([(hxp + 1, hyp - 2), (hxp + 1, hyp + 1)], fill=(80, 80, 80)); d.ellipse([hxp - 2, hyp + 1, hxp + 4, hyp + 9], fill=(250, 220, 120), outline=(90, 80, 60))
    elif hold == 'umbrella_k':      # 지우산
        d.line([(hxp + 1, hyp + 6), (hxp + 1, hy - 4)], fill=(110, 80, 50)); d.chord([hxp - 8, hy - 9, hxp + 10, hy + 3], 180, 360, fill=(200, 150, 80))

# ---------------------------------------------------------------- 옷 차림 빨리 만들기
SKIN_K = (236, 200, 164); SKIN_K2 = (224, 186, 150); SKIN_O = (226, 192, 160); SKIN_T = (206, 160, 120)
HAIR_K = (30, 26, 26); GREY_K = (150, 146, 140); WHITE_K = (226, 224, 218)
WHITE_C = (242, 240, 232); OFFW = (232, 226, 210)
def PO(cloth=WHITE_C, hat='gat', skin=SKIN_K, **kw):
    """두루마기 · 도포 + 갓 (양반 · 유생 · 역관)"""
    d_ = dict(top='po', cloth=cloth, hat=hat, hair='sangtu', hair_c=HAIR_K, skin=skin, shoes=(60, 50, 44))
    d_.update(kw); return d_
def JEO(cloth=OFFW, pants=OFFW, hat='headband', skin=SKIN_T, **kw):
    """저고리 + 바지 (상민 · 일꾼 · 장사꾼)"""
    d_ = dict(top='jeo', cloth=cloth, legs='trousers', pants=pants, hat=hat, hair='sangtu', hair_c=HAIR_K, skin=skin, shoes=(150, 120, 80), daenim=sh(pants, 0.7))
    d_.update(kw); return d_
def HAN(jeogori, chima, skin=SKIN_K, hair='jjok', **kw):
    """여자: 저고리 + 치마"""
    d_ = dict(top='dress', hanbok=True, cloth=jeogori, blouse=jeogori, skirt=chima, hair=hair, hair_c=HAIR_K, skin=skin, shoes=(200, 180, 150))
    d_.update(kw); return d_
def DAN(cloth, hyungbae=(60, 90, 140), skin=SKIN_K, hat='samo', **kw):
    """단령 관복 + 사모"""
    d_ = dict(top='dan', cloth=cloth, hyungbae=hyungbae, hat=hat, hair='sangtu', hair_c=HAIR_K, skin=skin, shoes=(30, 26, 26))
    d_.update(kw); return d_
def GUN(cloth=(70, 90, 140), sleeve=(190, 50, 50), vest=(40, 44, 60), skin=SKIN_T, **kw):
    """구식 군인: 동달이(붉은 소매) + 전복 + 전립"""
    d_ = dict(top='po', cloth=cloth, sleeve=sleeve, jeonbok=vest, jeondae=(200, 60, 50), hat='jeolip', hair='sangtu', hair_c=HAIR_K, skin=skin, shoes=(40, 36, 32))
    d_.update(kw); return d_
SPECS = {}
SPECS.update({
    # ---- 주인공 집안 (만든 인물)
    'yunjae10': JEO((236, 230, 214), (226, 220, 204), hat=None, hair='daenggi', kid=True, skin=SKIN_K, shoes=(200, 180, 150)),
    'yunjae15': JEO((214, 224, 236), (226, 220, 204), hat=None, hair='daenggi', kid=True, skin=SKIN_K, shoes=(200, 180, 150)),
    'yunjae20': PO((222, 232, 240), hat='gat'),
    'yunjae26': PO((206, 222, 236), hat='gat', hold='book'),
    'father': PO((236, 234, 226), hat='gat', beard=(40, 34, 30), hold='book'),
    'father_old': PO((228, 226, 218), hat='gat', beard=GREY_K, beard_long=1, hair_c=GREY_K),
    'mother': HAN((236, 222, 200), (90, 70, 110), hair='jjok'),
    'yunhee12': HAN((240, 200, 120), (180, 50, 70), hair='daenggi', kid=True, ribbon=(200, 40, 50)),
    'yunhee17': HAN((226, 196, 160), (110, 80, 60), hair='daenggi', ribbon=(200, 40, 50), hold='basket'),
    'yunhee23': HAN((214, 200, 170), (70, 60, 90), hair='jjok', hold='basket'),
    # ---- 1장 경복궁 · 장터
    'daewongun': PO((242, 240, 232), hat='waryong', beard=(60, 52, 46), beard_long=1, border=(30, 30, 34), tti=(70, 60, 90)),
    'overseer': DAN((70, 110, 90), hyungbae=(200, 170, 100)),
    'corvee': JEO((214, 204, 180), (200, 190, 168), hat='headband', hold='spear', skin=SKIN_T),
    'carpenter': JEO((190, 170, 140), (170, 150, 120), hat='headband', hold='hammer', skin=SKIN_T),
    'rich': PO((150, 130, 170), hat='gat', beard=(40, 34, 30), stout=True, hold='coin'),
    'rice_seller': JEO((220, 210, 190), (190, 180, 160), hat='paeraengi', skin=SKIN_T, hold='rice'),
    'commoner': JEO((226, 220, 200), (200, 194, 176), hat='headband', skin=SKIN_T),
    'scholar_y': PO((244, 242, 234), hat='gat', beard=(40, 34, 30), tti=(40, 40, 80), hold='fan'),
    'peddler': JEO((200, 190, 160), (180, 170, 140), hat='paeraengi', cotton=True, pack='jige', load=(170, 140, 100), skin=SKIN_T),
    'market_w': HAN((230, 220, 200), (120, 100, 80), hair='jjok', hold='basket', skin=SKIN_K2),
    'kid_m': JEO((236, 222, 160), (214, 200, 160), hat=None, hair='daenggi', kid=True, skin=SKIN_K, shoes=(200, 180, 150)),
    # ---- 2장 강화도 (1866 · 1871)
    'yanghs': GUN((60, 80, 130), (190, 50, 50), (30, 34, 50), feather=(120, 90, 50), hold='hwando', beard=(40, 34, 30), skin=SKIN_K),
    'soldier_k': GUN(hold='matchlock'),
    'soldier_k2': GUN((80, 100, 120), (170, 60, 50), (50, 50, 60), hold='spear_k'),
    'tiger_hunter': JEO((180, 160, 120), (150, 130, 100), hat='jeolip', hat_c=(60, 50, 44), hold='matchlock', skin=SKIN_T),
    'kyujanggak': DAN((60, 80, 110), hyungbae=(200, 170, 100), hold='book'),
    'french': dict(top='sailor', cloth=(30, 40, 80), legs='trousers', pants=(36, 46, 86), hat='bachi', hair='short', hair_c=(110, 80, 50), skin=(240, 210, 186), hold='rifle', beard=(110, 80, 50)),
    'french_off': dict(top='tunic', cloth=(30, 40, 80), legs='trousers', pants=(170, 40, 40), hat='kepi', hat_c=(30, 40, 80), band=(200, 170, 80), epaulet=(220, 190, 100), hair='short', hair_c=(80, 60, 40), skin=(240, 210, 186), mustache=(80, 60, 40)),
    'eojaeyeon': GUN((70, 70, 120), (190, 50, 50), (30, 30, 40), feather=(120, 90, 50), hold='flag_suja', beard=(40, 34, 30), beard_long=1, skin=SKIN_K),
    'us_marine': dict(top='tunic', cloth=(30, 40, 70), legs='trousers', pants=(110, 130, 160), hat='kepi', hat_c=(30, 40, 70), band=(30, 40, 70), hair='short', hair_c=(120, 90, 60), skin=(240, 210, 186), hold='rifle', belt=(240, 240, 240)),
    'us_sailor': dict(top='sailor', cloth=(30, 40, 70), legs='trousers', pants=(30, 40, 70), hat='beanie', hat_c=(240, 240, 240), hair='short', hair_c=(90, 70, 50), skin=(240, 210, 186), mustache=(90, 70, 50)),
    'park_gyusu': DAN((50, 70, 90), hyungbae=(200, 170, 100), beard=GREY_K, beard_long=2, hair_c=GREY_K),
    'beacon_m': JEO((200, 190, 170), (170, 160, 140), hat='jeolip', hat_c=(60, 50, 44), skin=SKIN_T, hold='lantern'),
    # ---- 3장 강화도 조약 (1876)
    'sinheon': DAN((40, 60, 80), hyungbae=(200, 160, 80), beard=(50, 44, 40), beard_long=2),
    'kuroda': dict(top='tunic', cloth=(30, 34, 50), legs='trousers', pants=(30, 34, 50), stripe=(200, 170, 80), hat='peaked', hat_c=(30, 34, 50), band=(200, 170, 80),
                   epaulet=(220, 190, 100), hair='short', hair_c=HAIR_K, skin=SKIN_K, mustache=HAIR_K, buttons=(220, 190, 100)),
    'jp_official': dict(top='frock', cloth=(30, 30, 34), legs='trousers', pants=(40, 40, 44), hat='tophat', hair='short', hair_c=HAIR_K, skin=SKIN_K, mustache=HAIR_K, tie=(40, 40, 40)),
    'jp_soldier': dict(top='tunic', cloth=(36, 40, 66), legs='trousers', pants=(36, 40, 66), stripe=(200, 50, 50), hat='jpcap', hair='short', hair_c=HAIR_K, skin=SKIN_K, hold='rifle', belt=(30, 26, 24)),
    'ogyeongseok': PO((214, 226, 234), hat='gat', beard=(40, 34, 30), hold='book'),
    'jp_merchant': dict(top='po', cloth=(110, 100, 110), obi=(60, 50, 60), hair='short', hair_c=HAIR_K, skin=SKIN_K, shoes=(150, 110, 70), hold='bag', bundle_c=(150, 120, 80)),
    'choi_ik': PO((244, 242, 234), hat='gat', beard=WHITE_K, beard_long=3, hair_c=GREY_K, hold='sangso'),
    # ---- 4장 개화 정책 · 위정척사 (1880~81)
    'byeolgigun': dict(top='tunic', cloth=(46, 74, 60), legs='trousers', pants=(46, 74, 60), hat='jeolip', hat_c=(30, 30, 30), hair='sangtu', hair_c=HAIR_K, skin=SKIN_T, hold='rifle', belt=(40, 30, 24), buttons=(220, 200, 120)),
    'horimoto': dict(top='tunic', cloth=(30, 34, 60), legs='trousers', pants=(30, 34, 60), stripe=(200, 50, 50), hat='jpcap', hair='short', hair_c=HAIR_K, skin=SKIN_K, mustache=HAIR_K, hold='hwando', epaulet=(220, 190, 100)),
    'old_soldier': GUN((90, 100, 120), (160, 70, 60), (60, 60, 64), skin=SKIN_T, hold='spear_k'),
    'kimhongjip': DAN((60, 90, 110), hyungbae=(200, 170, 100), beard=(40, 34, 30), hold='book'),
    'young_off': DAN((70, 120, 120), hyungbae=(200, 170, 100), hold='book'),
    'imansun': PO((244, 242, 234), hat='gat', beard=(50, 44, 40), beard_long=2, hold='sangso', tti=(60, 50, 80)),
    'confucian': PO((240, 238, 230), hat='gat', beard=(40, 34, 30), tti=(40, 40, 80), hold='sangso'),
    'confucian2': PO((236, 234, 224), hat='gat', beard=GREY_K, hair_c=GREY_K, tti=(80, 40, 40)),
    'kimyunsik': DAN((50, 70, 100), hyungbae=(200, 170, 100), beard=(40, 34, 30)),
    # ---- 5장 임오군란 (1882)
    'kimchunyoung': GUN((90, 100, 120), (160, 70, 60), (60, 60, 64), skin=SKIN_T),
    'poor_m': JEO((196, 186, 164), (176, 166, 146), hat='headband', skin=SKIN_T, barefoot=True),
    'clerk': DAN((90, 100, 80), hyungbae=None, hold='ledger'),
    'qing_soldier': dict(top='kurta', cloth=(60, 80, 140), legs='trousers', pants=(40, 40, 50), hat='turban', hat_c=(40, 40, 50), hair='queue', hair_c=HAIR_K, skin=SKIN_K, badge_circle=True, hold='rifle', belt=(170, 40, 40)),
    'qing_merchant': dict(top='robe', cloth=(70, 90, 110), hat='skullcap', hat_c=(30, 30, 34), hair='queue', hair_c=HAIR_K, skin=SKIN_K, hold='ledger'),
    'parkyounghyo': PO((214, 222, 236), hat='gat'),
    'kimokgyun': PO((230, 226, 214), hat='gat', mustache=(40, 34, 30)),
    'gojong': DAN((190, 40, 40), hyungbae=None, dragon=True, hat='ikseon', gakdae=(40, 40, 40), beard=(40, 34, 30)),
    'sailor_jp': dict(top='sailor', cloth=(30, 34, 60), legs='trousers', pants=(30, 34, 60), hat='beanie', hat_c=(30, 34, 60), hair='short', hair_c=HAIR_K, skin=SKIN_K),
})

# ---------------------------------------------------------------- 물건 그림 (!$k_*)
PAPY = (232, 216, 170); INKB = (40, 30, 26); WOODK = (130, 92, 58); WOODK_D = (96, 66, 40); BRASS = (206, 170, 90); STONE = (170, 166, 156)
def _stone(d, D, st):           # 주춧돌 (밀어서 옮기는 돌)
    d.ellipse([6, 30, 42, 46], fill=(120, 116, 108)); d.rounded_rectangle([7, 14, 41, 40], 8, fill=STONE)
    d.ellipse([9, 10, 39, 24], fill=(200, 196, 186)); d.ellipse([16, 13, 32, 21], fill=(186, 182, 172))
    for (x, y) in ((12, 28), (30, 32), (22, 36)): d.point((x, y), fill=(130, 126, 118))
def _stone_mark(d, D, st):      # 주춧돌 놓을 자리 표시
    d.rectangle([8, 18, 40, 44], outline=(230, 200, 90), width=2); d.line([(12, 22), (36, 40)], fill=(230, 200, 90)); d.line([(36, 22), (12, 40)], fill=(230, 200, 90))
def _bandaji(d, D, st):         # 반닫이 (일기 상자)
    d.rectangle([4, 16, 44, 44], fill=WOODK); d.rectangle([4, 16, 44, 26], fill=sh(WOODK, 1.1))
    for (x0, y0) in ((6, 18), (36, 18), (6, 34), (36, 34)): d.rectangle([x0, y0, x0 + 6, y0 + 8], fill=BRASS)
    d.ellipse([20, 22, 28, 30], fill=BRASS); d.rectangle([23, 28, 25, 36], fill=sh(BRASS, 0.7))
def _seoan(d, D, st):           # 서안 (낮은 책상) + 책 · 벼루 · 붓
    d.rectangle([4, 24, 44, 32], fill=WOODK); d.rectangle([6, 32, 9, 44], fill=WOODK_D); d.rectangle([39, 32, 42, 44], fill=WOODK_D)
    d.rectangle([8, 18, 22, 24], fill=(200, 170, 110)); d.line([(15, 18), (15, 24)], fill=(120, 90, 50))
    d.rectangle([26, 19, 36, 24], fill=(50, 50, 54)); d.line([(38, 16), (42, 23)], fill=(110, 80, 50))
def _bookcase(d, D, st):        # 책장 (족보 · 책)
    d.rectangle([6, 2, 42, 46], fill=WOODK_D); d.rectangle([8, 4, 40, 44], fill=(110, 76, 46))
    for y in (4, 18, 32):
        for k in range(5): d.rectangle([10 + k * 6, y + 2, 14 + k * 6, y + 12], fill=[(200, 170, 110), (150, 60, 50), (60, 70, 110), (220, 200, 160), (90, 110, 80)][(k + y) % 5])
        d.line([(8, y + 13), (40, y + 13)], fill=WOODK_D, width=2)
def _deungjan(d, D, st):        # 등잔걸이 (기름 등잔)
    d.line([(24, 46), (24, 14)], fill=WOODK_D, width=2); d.rectangle([16, 43, 32, 46], fill=WOODK_D)
    d.ellipse([18, 12, 30, 17], fill=(200, 196, 186)); d.polygon([(23, 12), (25, 12), (24, 6 - st % 2)], fill=(250, 200, 80))
def _lamp_oil(d, D, st):        # 남포등 (석유 등, 1880년대)
    d.rectangle([18, 40, 30, 46], fill=BRASS); d.ellipse([16, 26, 32, 42], fill=(190, 160, 90))
    d.rounded_rectangle([19, 8, 29, 28], 4, fill=(246, 236, 190)); d.polygon([(22, 22), (26, 22), (24, 14 - st % 2)], fill=(250, 190, 70))
def _hwaro(d, D, st):           # 화로
    d.polygon([(8, 26), (40, 26), (36, 44), (12, 44)], fill=(150, 120, 90)); d.ellipse([8, 22, 40, 30], fill=(60, 50, 46))
    for k in range(3): d.ellipse([14 + k * 7, 23, 20 + k * 7, 27], fill=(230, 110 + st * 20, 50))
def _stele(d, D, st):           # 척화비 (작은 그림)
    d.rectangle([10, 40, 38, 47], fill=(150, 146, 138)); d.rectangle([15, 10, 33, 41], fill=(176, 172, 164))
    d.polygon([(11, 10), (37, 10), (33, 3), (15, 3)], fill=(130, 126, 118))
    for y in range(14, 38, 5): d.line([(21, y), (23, y)], fill=(80, 76, 70)); d.line([(26, y + 1), (28, y + 1)], fill=(80, 76, 70))
def _bongsu(d, D, st):          # 봉수대 굴뚝
    d.rectangle([12, 18, 36, 46], fill=(150, 140, 126)); d.rectangle([10, 14, 38, 20], fill=(120, 112, 100))
    for y in range(24, 46, 7): d.line([(12, y), (36, y)], fill=(120, 112, 100))
    if st != 1: d.polygon([(16, 14), (32, 14), (24, 2 + st)], fill=(250, 150, 50))
def _cannon_k(d, D, st):        # 조선 대포 (불랑기 · 바퀴 없는 받침)
    d.rectangle([6, 34, 42, 40], fill=WOODK_D); d.rectangle([8, 40, 12, 46], fill=WOODK_D); d.rectangle([36, 40, 40, 46], fill=WOODK_D)
    d.rounded_rectangle([4, 24, 44, 34], 4, fill=(70, 66, 60)); d.ellipse([38, 23, 46, 35], fill=(50, 46, 42))
    for x in (12, 22, 32): d.line([(x, 24), (x, 34)], fill=(110, 104, 96))
def _rice_bags(d, D, st):       # 쌀가마니 더미
    for (x, y) in ((4, 30), (24, 30), (14, 16)):
        d.rounded_rectangle([x, y, x + 20, y + 15], 5, fill=(214, 190, 130)); d.line([(x + 2, y + 4), (x + 18, y + 4)], fill=(170, 140, 90)); d.line([(x + 2, y + 11), (x + 18, y + 11)], fill=(170, 140, 90))
def _scale_k(d, D, st):         # 대저울 (녹봉 저울)
    d.line([(24, 46), (24, 6)], fill=WOODK_D, width=3); d.line([(6, 10), (42, 10)], fill=WOODK, width=3)
    for x in (8, 40):
        d.line([(x, 10), (x - 4, 26)], fill=(90, 80, 70)); d.line([(x, 10), (x + 4, 26)], fill=(90, 80, 70)); d.chord([x - 8, 22, x + 8, 32], 0, 180, fill=BRASS)
    d.rectangle([16, 42, 32, 46], fill=WOODK_D)
def _ledger_desk(d, D, st):     # 장부 책상 (선혜청)
    d.rectangle([2, 22, 46, 30], fill=WOODK); d.rectangle([4, 30, 7, 44], fill=WOODK_D); d.rectangle([41, 30, 44, 44], fill=WOODK_D)
    for k in range(3): d.rectangle([6 + k * 13, 14 - k, 17 + k * 13, 22], fill=(210, 180, 120), outline=(120, 90, 50))
def _treaty_table(d, D, st):    # 협상 탁자 (조약문)
    d.rectangle([2, 20, 46, 30], fill=(150, 40, 40)); d.rectangle([4, 30, 7, 46], fill=WOODK_D); d.rectangle([41, 30, 44, 46], fill=WOODK_D)
    d.rectangle([8, 14, 22, 24], fill=(244, 240, 228)); d.rectangle([26, 14, 40, 24], fill=(244, 240, 228))
    for y in (17, 20): d.line([(10, y), (20, y)], fill=INKB); d.line([(28, y), (38, y)], fill=INKB)
    d.ellipse([20, 22, 26, 27], fill=(200, 40, 40))
def _hanyang_map(d, D, st):     # 한양 지도판 (소문 지도)
    d.rectangle([4, 30, 7, 46], fill=WOODK_D); d.rectangle([41, 30, 44, 46], fill=WOODK_D)
    d.rectangle([2, 4, 46, 34], fill=(232, 220, 186), outline=WOODK_D, width=2)
    d.ellipse([10, 8, 38, 30], outline=(120, 100, 70)); d.line([(14, 22), (36, 18)], fill=(80, 120, 160), width=2)
    for (x, y) in ((16, 12), (30, 13), (22, 25)): d.rectangle([x, y, x + 4, y + 3], fill=(170, 50, 40))
def _drum_k(d, D, st):          # 북 (훈련장)
    d.line([(10, 46), (16, 30)], fill=WOODK_D, width=2); d.line([(38, 46), (32, 30)], fill=WOODK_D, width=2)
    d.ellipse([10, 10, 38, 38], fill=(150, 40, 40)); d.ellipse([14, 14, 34, 34], fill=(232, 220, 190))
    d.ellipse([20, 20, 28, 28], outline=(60, 90, 150), width=2)
def _rifle_rack(d, D, st):      # 총가 (서양식 소총)
    d.rectangle([4, 40, 44, 44], fill=WOODK_D); d.rectangle([4, 12, 44, 16], fill=WOODK_D)
    for x in range(8, 42, 7): d.line([(x, 42), (x + 2, 6)], fill=(90, 70, 50), width=2); d.line([(x + 2, 6), (x + 2, 2)], fill=(150, 150, 156))
def _banner_o(d, D, st):        # 오방기 깃발
    d.line([(12, 46), (12, 2)], fill=WOODK_D, width=2)
    col = [(200, 40, 40), (40, 80, 170), (230, 200, 60)][st % 3]
    d.polygon([(13, 4), (40, 6 + st), (38, 22), (13, 20)], fill=col); d.polygon([(13, 20), (38, 22), (34, 26), (13, 24)], fill=(240, 240, 236))
def _sujagi(d, D, st):          # 수자기 (帥字旗)
    d.line([(8, 47), (8, 1)], fill=WOODK_D, width=2)
    d.polygon([(9, 3), (44, 4 + st % 2), (44, 36), (9, 34)], fill=(222, 196, 120)); d.rectangle([9, 3, 44, 6], fill=(170, 40, 40))
    from PIL import ImageFont
    try:
        f = ImageFont.truetype('/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc', 22, index=1)
        d.text((26, 20), '帥', font=f, fill=(30, 26, 22), anchor='mm')
    except Exception: pass
def _notice(d, D, st):          # 방(榜) · 알림판
    d.rectangle([6, 30, 9, 46], fill=WOODK_D); d.rectangle([39, 30, 42, 46], fill=WOODK_D)
    d.rectangle([2, 4, 46, 32], fill=(236, 230, 210), outline=WOODK_D, width=2)
    for x in range(36, 6, -6): d.line([(x, 8), (x, 28)], fill=(50, 44, 40))
def _jp_sign(d, D, st):         # 일본 상점 간판 · 노렌 (1880년대 장터)
    d.rectangle([4, 4, 44, 14], fill=(40, 40, 60)); d.text((10, 4), '日本', fill=(240, 236, 226))
    for k in range(4): d.rectangle([5 + k * 10, 15, 13 + k * 10, 34], fill=(60, 70, 110))
    d.text((10, 18), '商', fill=(240, 236, 226))
def _kerosene(d, D, st):        # 석유통 · 성냥 상자 (새 물건)
    d.rectangle([4, 18, 22, 46], fill=(170, 60, 50)); d.rectangle([8, 12, 18, 18], fill=(150, 150, 156)); d.rectangle([6, 24, 20, 32], fill=(240, 220, 160))
    for k in range(3): d.rectangle([26, 34 - k * 8, 44, 41 - k * 8], fill=(230, 200, 120), outline=(150, 110, 60))
def _cloth_bolts(d, D, st):     # 옥양목 (영국산 면직물) 더미
    for k, c in enumerate(((244, 242, 236), (230, 228, 222), (250, 250, 246))):
        d.rounded_rectangle([4 + k * 2, 36 - k * 9, 44 - k * 2, 46 - k * 9], 3, fill=c, outline=(170, 170, 160))
def _onggi(d, D, st):           # 장독 · 항아리
    for k, (x, s_) in enumerate(((4, 1.0), (20, 0.8), (32, 0.9))):
        w = int(14 * s_); h = int(26 * s_)
        d.ellipse([x, 46 - h, x + w, 46], fill=(110, 70, 44)); d.ellipse([x + 2, 46 - h - 2, x + w - 2, 46 - h + 4], fill=(90, 56, 36))
def _jige(d, D, st):            # 지게 (세워 둔 것)
    d.line([(16, 46), (20, 4)], fill=WOODK, width=3); d.line([(32, 46), (28, 4)], fill=WOODK, width=3)
    for y in (12, 22, 32): d.line([(18, y), (30, y)], fill=WOODK, width=2)
    d.line([(20, 28), (10, 34)], fill=WOODK, width=2); d.line([(28, 28), (38, 34)], fill=WOODK, width=2)
def _well_k(d, D, st):          # 우물
    d.rectangle([6, 22, 42, 44], fill=(160, 156, 146)); d.ellipse([6, 16, 42, 28], fill=(60, 80, 100)); d.ellipse([6, 16, 42, 28], outline=(130, 126, 118), width=3)
    d.line([(10, 22), (10, 2)], fill=WOODK_D, width=2); d.line([(38, 22), (38, 2)], fill=WOODK_D, width=2); d.line([(8, 4), (40, 4)], fill=WOODK_D, width=3)
def _cart(d, D, st):            # 달구지 (돌 나르는 수레)
    d.rectangle([4, 18, 44, 30], fill=WOODK); d.ellipse([6, 26, 22, 42], outline=WOODK_D, width=3); d.ellipse([26, 26, 42, 42], outline=WOODK_D, width=3)
    d.rectangle([10, 10, 26, 18], fill=STONE)
def _jangseung(d, D, st):       # 장승
    d.rectangle([18, 6, 30, 46], fill=(150, 116, 80)); d.ellipse([16, 2, 32, 16], fill=(160, 124, 86))
    d.ellipse([19, 9, 23, 13], fill=INKB); d.ellipse([25, 9, 29, 13], fill=INKB); d.rectangle([21, 18, 27, 21], fill=(200, 50, 40))
    for y in range(26, 44, 4): d.line([(22, y), (26, y)], fill=INKB)
def _brazier_sig(d, D, st):     # 횃불 (밤 산성)
    d.line([(24, 46), (24, 16)], fill=WOODK_D, width=3); d.polygon([(18, 16), (30, 16), (24, 4 - st % 2)], fill=(250, 160, 50)); d.polygon([(21, 16), (27, 16), (24, 9)], fill=(255, 230, 120))
def _ship_far(d, D, st):        # 멀리 보이는 배 (망루에서)
    d.polygon([(4, 30), (44, 30), (38, 38), (10, 38)], fill=(60, 56, 54)); d.line([(24, 30), (24, 6)], fill=(60, 56, 54), width=2)
    d.polygon([(25, 8), (38, 26), (25, 26)], fill=(236, 232, 220)); d.rectangle([14, 18, 18, 30], fill=(40, 40, 40))
def _gate_k(d, D, st):          # 산성 문 (정족산성 동문)
    d.rectangle([0, 6, 47, 47], fill=(150, 146, 136)); d.chord([10, 14, 38, 60], 180, 360, fill=(30, 26, 24)); d.rectangle([10, 36, 38, 47], fill=(30, 26, 24))
    for y in range(8, 30, 6):
        for x in range(0, 48, 12): d.rectangle([x + (y // 6 % 2) * 6, y, x + 10 + (y // 6 % 2) * 6, y + 5], outline=(120, 116, 106))
OBJS = {'!$k_stone': _stone, '!$k_mark': _stone_mark, '!$k_bandaji': _bandaji, '!$k_seoan': _seoan, '!$k_bookcase': _bookcase, '!$k_deungjan': _deungjan,
        '!$k_lamp_oil': _lamp_oil, '!$k_hwaro': _hwaro, '!$k_stele': _stele, '!$k_bongsu': _bongsu, '!$k_cannon': _cannon_k, '!$k_rice': _rice_bags,
        '!$k_scale': _scale_k, '!$k_ledger': _ledger_desk, '!$k_treaty': _treaty_table, '!$k_hmap': _hanyang_map, '!$k_drum': _drum_k, '!$k_rifles': _rifle_rack,
        '!$k_banner': _banner_o, '!$k_sujagi': _sujagi, '!$k_notice': _notice, '!$k_jpsign': _jp_sign, '!$k_kerosene': _kerosene, '!$k_cloth': _cloth_bolts,
        '!$k_onggi': _onggi, '!$k_jige': _jige, '!$k_well': _well_k, '!$k_cart': _cart, '!$k_jangseung': _jangseung, '!$k_torch': _brazier_sig,
        '!$k_shipfar': _ship_far, '!$k_gate': _gate_k}
BIG = {}

def _obj(fn, fw=48, fh=48):
    out = Image.new('RGBA', (fw * 3, fh * 4), (0, 0, 0, 0))
    for D in range(4):
        for st in range(3):
            lay = Image.new('RGBA', (fw, fh), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            fn(d, D, st)
            out.alpha_composite(outline(lay, 0.5), (st * fw, D * fh))
    return out

def build(out):
    os.makedirs(out, exist_ok=True)
    for k, v in SPECS.items(): sheet(v, os.path.join(out, '$k_' + k + '.png'))
    for k, fn in OBJS.items(): _obj(fn).save(os.path.join(out, k + '.png'))
    for k, (fn, fw, fh) in BIG.items(): _obj(fn, fw, fh).save(os.path.join(out, k + '.png'))
    print('chars', len(SPECS), 'objs', len(OBJS) + len(BIG))

if __name__ == "__main__":
    build(sys.argv[1])
    if len(sys.argv) > 2:
        names = list(SPECS)
        cols = 12
        rows = (len(names) + cols - 1) // cols
        prev = Image.new('RGBA', (96 * cols, 96 * 2 * rows + 96 * 3), (200, 196, 180, 255))
        for i, n in enumerate(names):
            s_ = Image.open(os.path.join(sys.argv[1], '$k_' + n + '.png'))
            prev.alpha_composite(s_.crop((48, OFF, 96, FH)).resize((96, 96), Image.NEAREST), ((i % cols) * 96, (i // cols) * 192))
            prev.alpha_composite(s_.crop((48, FH * 1 + OFF, 96, FH * 2)).resize((96, 96), Image.NEAREST), ((i % cols) * 96, (i // cols) * 192 + 96))
        for i, k in enumerate(OBJS):
            s_ = Image.open(os.path.join(sys.argv[1], k + '.png'))
            prev.alpha_composite(s_.crop((48, 0, 96, 48)).resize((72, 72), Image.NEAREST), ((i % 16) * 72, 96 * 2 * rows + (i // 16) * 72))
        prev.save(sys.argv[2])
