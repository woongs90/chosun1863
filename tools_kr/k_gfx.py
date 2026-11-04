"""종로 사진관 편 그래픽 (프랑스·중국사 편 그래픽을 바탕으로)
 서울 1945~53 색: seoul(가을) seoul_w(겨울) busan(항구) hungnam(눈 부두) line38(38선 들판) 추가
 추가 땅 기호: q 파리 돌길(포석)  u 진흙(걷기, 리전 5)  z 바둑판 돌바닥  o 나무 마루
 - 도트 느낌 땅 그리기 + 빛·그늘 마무리 + 나무
 땅 기호 (모든 관 공통)
   .  흙길            ,  풀밭          ;  초원(누런 풀)    s  모래(사막)       M  조·기장 밭(벽)
   W  큰 강(벽)       w  얕은 물(걷기)  C  운하·바다(벽)    L  둑(걷기)         H  나무다리·부두(걷기)
   E  판축 기단(걷기)  #  다진 마당      S  계단(걷기)       P  돌판 포장(걷기)   K  벽돌 포장(걷기)
   m  흰 대리석(걷기)  r  붉은 칠 바닥    n  눈(걷기)
   B  건물(벽)        T  나무(벽)      f  담(벽)          x  물건(벽)         k  바위(벽)   c  절벽(벽)
"""
import os, sys, math, random
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from scipy import ndimage
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from k_common import TS, F
from hd_art import sh, mix, outline

PX = 2
K = TS // PX
WALL = set('MWCBTfxkc')
BAYER = (np.array([[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]) + 0.5) / 16.0

# ------------------------------------------------------------------ 시대별 색
PAL = {
    'loess': dict(dirt=(204, 168, 112), grass=(124, 152, 78), steppe=(176, 170, 96), sand=(222, 190, 128), field=(206, 180, 92),
                  river=(178, 136, 74), river_deep=(146, 106, 58), canal=(96, 132, 128), canal_deep=(66, 100, 104),
                  court=(196, 166, 118), earth=(182, 148, 102), stone=(170, 160, 142), brick=(150, 138, 124), marble=(228, 226, 216),
                  red=(150, 50, 40), snow=(236, 240, 246), cliff=(150, 120, 90)),
    'zhou': dict(dirt=(196, 168, 120), grass=(108, 148, 82), steppe=(170, 168, 100), sand=(220, 192, 136), field=(196, 176, 96),
                 river=(110, 140, 150), river_deep=(80, 110, 126), canal=(90, 130, 136), canal_deep=(60, 96, 110),
                 court=(184, 168, 136), earth=(172, 146, 110), stone=(166, 160, 146), brick=(146, 138, 128), marble=(228, 226, 218),
                 red=(150, 50, 40), snow=(236, 240, 246), cliff=(140, 118, 96)),
    'qin': dict(dirt=(176, 156, 120), grass=(100, 130, 80), steppe=(160, 156, 100), sand=(214, 186, 132), field=(186, 166, 96),
                river=(120, 136, 136), river_deep=(86, 104, 112), canal=(86, 118, 124), canal_deep=(56, 84, 96),
                court=(168, 156, 132), earth=(160, 140, 112), stone=(150, 146, 140), brick=(118, 114, 112), marble=(220, 218, 210),
                red=(120, 40, 34), snow=(236, 240, 246), cliff=(130, 112, 92)),
    'desert': dict(dirt=(214, 182, 128), grass=(140, 150, 86), steppe=(184, 170, 104), sand=(230, 196, 132), field=(206, 180, 92),
                   river=(120, 150, 150), river_deep=(80, 120, 126), canal=(90, 140, 140), canal_deep=(60, 104, 110),
                   court=(206, 178, 130), earth=(196, 160, 112), stone=(186, 166, 136), brick=(176, 150, 116), marble=(230, 224, 210),
                   red=(160, 70, 50), snow=(236, 240, 246), cliff=(196, 150, 104)),
    'tang': dict(dirt=(198, 172, 128), grass=(112, 154, 86), steppe=(176, 170, 100), sand=(222, 194, 140), field=(200, 180, 96),
                 river=(96, 140, 150), river_deep=(66, 108, 126), canal=(84, 136, 140), canal_deep=(56, 100, 116),
                 court=(192, 176, 146), earth=(178, 154, 118), stone=(178, 172, 160), brick=(150, 142, 134), marble=(232, 230, 222),
                 red=(170, 60, 44), snow=(236, 240, 246), cliff=(150, 126, 100)),
    'song': dict(dirt=(176, 160, 132), grass=(100, 142, 92), steppe=(170, 168, 104), sand=(214, 192, 146), field=(190, 176, 104),
                 river=(92, 132, 140), river_deep=(62, 100, 116), canal=(84, 128, 134), canal_deep=(56, 92, 108),
                 court=(176, 168, 150), earth=(166, 150, 122), stone=(164, 162, 156), brick=(132, 128, 124), marble=(226, 226, 220),
                 red=(150, 50, 40), snow=(236, 240, 246), cliff=(130, 120, 104)),
    'steppe': dict(dirt=(186, 166, 120), grass=(128, 156, 80), steppe=(168, 170, 88), sand=(216, 192, 136), field=(196, 180, 96),
                   river=(100, 150, 170), river_deep=(70, 120, 150), canal=(90, 140, 160), canal_deep=(60, 110, 140),
                   court=(186, 170, 136), earth=(170, 150, 112), stone=(168, 164, 150), brick=(150, 142, 130), marble=(230, 228, 220),
                   red=(160, 60, 44), snow=(236, 240, 246), cliff=(140, 124, 100)),
    'ming': dict(dirt=(184, 166, 132), grass=(100, 146, 88), steppe=(168, 166, 100), sand=(216, 196, 150), field=(196, 178, 100),
                 river=(84, 128, 150), river_deep=(56, 96, 128), canal=(70, 120, 150), canal_deep=(40, 84, 124),
                 court=(186, 176, 160), earth=(170, 154, 128), stone=(170, 168, 162), brick=(126, 124, 124), marble=(234, 232, 226),
                 red=(160, 46, 38), snow=(236, 240, 246), cliff=(134, 124, 110)),
}

FR = dict(dirt=(150, 132, 108), grass=(108, 140, 78), steppe=(176, 166, 104), sand=(214, 196, 150), field=(196, 170, 90),
          river=(92, 120, 120), river_deep=(62, 88, 96), canal=(84, 112, 120), canal_deep=(56, 80, 92),
          court=(176, 166, 146), earth=(160, 140, 112), stone=(196, 188, 170), brick=(150, 110, 90), marble=(232, 228, 216),
          red=(150, 40, 40), snow=(236, 240, 246), cliff=(140, 126, 106), cobble=(150, 146, 136), mud=(106, 84, 60),
          check_a=(226, 220, 204), check_b=(150, 140, 128), floor=(150, 104, 66))
PAL['paris'] = FR
PAL['versailles'] = dict(FR, stone=(214, 206, 186), cobble=(170, 164, 150), dirt=(196, 182, 150))
PAL['russia'] = dict(FR, dirt=(170, 168, 168), grass=(120, 132, 110), snow=(232, 238, 246), river=(150, 170, 186), river_deep=(110, 132, 150), mud=(120, 110, 104))
PAL['flanders'] = dict(FR, grass=(104, 136, 70), field=(196, 172, 92), dirt=(132, 110, 80), mud=(96, 76, 54))

def ramp(c, n=5, lo=0.78, hi=1.16):
    return np.array([sh(c, lo + (hi - lo) * i / (n - 1)) for i in range(n)], float)

def regions(grid):
    return [[1 if ch in WALL else (5 if ch == 'u' else 0) for ch in row] for row in grid]

def _up(m, blur=0.0, thr=0.5, noise=None, namt=0.0):
    up = np.kron(m, np.ones((K, K)))
    if blur > 0: up = ndimage.gaussian_filter(up, blur * K / 2.5)
    if noise is not None and namt: up = up + noise * namt
    return up >= thr

def tile_mask(grid, chars):
    return np.array([[1.0 if c in chars else 0.0 for c in row] for row in grid])

def quant(v, rp, bay, amt=1.0):
    n = len(rp)
    idx = np.clip(np.floor(v * n + (bay - 0.5) * amt), 0, n - 1).astype(int)
    return rp[idx]

def ground_of(grid, chars='xkTB'):
    """물건·나무·건물 칸은 둘레의 땅 재료로 바꿔서 칠함 (밑에 네모 자국이 안 생기게)"""
    g = [list(r) for r in grid]
    th, tw = len(g), len(g[0])
    for _ in range(12):
        changed = False
        new = [r[:] for r in g]
        for y in range(th):
            for x in range(tw):
                if g[y][x] not in chars: continue
                cnt = {}
                for dy in (-1, 0, 1):
                    for dx in (-1, 0, 1):
                        yy, xx = y + dy, x + dx
                        if 0 <= yy < th and 0 <= xx < tw and g[yy][xx] not in chars and g[yy][xx] not in 'fWCM':
                            cnt[g[yy][xx]] = cnt.get(g[yy][xx], 0) + 1
                if cnt:
                    new[y][x] = max(cnt.items(), key=lambda kv: kv[1])[0]; changed = True
        g = new
        if not changed: break
    return g

def render(grid, pal='loess', seed=1):
    """땅 전체를 도트 느낌으로 (2픽셀 단위, 색 계단 + 디더링)"""
    P = PAL[pal] if isinstance(pal, str) else pal
    grid = ground_of(grid)
    th, tw = len(grid), len(grid[0])
    gh, gw = th * K, tw * K
    rng = np.random.default_rng(seed)
    n1 = ndimage.gaussian_filter(rng.normal(0, 1, (gh, gw)), 2.0); n1 /= n1.std() + 1e-6
    n2 = ndimage.gaussian_filter(rng.normal(0, 1, (gh, gw)), 7.0); n2 /= n2.std() + 1e-6
    n3 = ndimage.gaussian_filter(rng.normal(0, 1, (gh, gw)), 18.0); n3 /= n3.std() + 1e-6
    wn = rng.random((gh, gw))
    yy, xx = np.mgrid[0:gh, 0:gw]
    bay = BAYER[yy % 4, xx % 4]
    def field(a=0.12, b=0.14, c=0.1, w=0.0):
        return np.clip(0.5 + n1 * a + n2 * b + n3 * c + (wn - 0.5) * w, 0, 1)

    # 재료별 바탕
    dirt = quant(field(0.10, 0.08, 0.06, 0.25), ramp(P['dirt'], 5, 0.86, 1.1), bay)
    grass_v = field(0.12, 0.08, 0.05, 0.3)
    grass = quant(grass_v, ramp(P['grass'], 6, 0.84, 1.13), bay)
    steppe = quant(field(0.12, 0.08, 0.06, 0.35), ramp(P['steppe'], 6, 0.84, 1.12), bay)
    ripple = (np.sin(xx * 0.32 + yy * 0.95 + n2 * 2.2 + n3 * 3) * 0.5 + 0.5)
    sand = quant(np.clip(0.35 + ripple * 0.35 + n3 * 0.12 + n1 * 0.05, 0, 1), ramp(P['sand'], 5, 0.84, 1.1), bay)
    fieldc = quant(field(0.08, 0.1, 0.06, 0.4), ramp(P['field'], 5, 0.8, 1.12), bay)
    court = quant(field(0.06, 0.08, 0.08, 0.2), ramp(P['court'], 4, 0.88, 1.08), bay)
    earth = quant(field(0.06, 0.08, 0.06, 0.2), ramp(P['earth'], 4, 0.86, 1.08), bay)
    snow = quant(field(0.05, 0.08, 0.08, 0.1), ramp(P['snow'], 4, 0.9, 1.03), bay)
    cliff = quant(field(0.12, 0.12, 0.08, 0.3), ramp(P['cliff'], 5, 0.7, 1.1), bay)

    # 돌판 (한 칸 = 한 장, 줄눈 + 판마다 색)
    slab_id = (yy // K) * 977 + ((xx + (yy // K % 2) * (K // 2)) // K) * 131
    srnd = (np.sin(slab_id * 12.9898) * 43758.5453) % 1.0
    stone_v = np.clip(0.5 + (srnd - 0.5) * 0.5 + n1 * 0.06, 0, 1)
    stone = quant(stone_v, ramp(P['stone'], 5, 0.86, 1.1), bay, 0.6)
    gx = ((xx + (yy // K % 2) * (K // 2)) % K == 0); gy = (yy % K == 0)
    stone[gx | gy] = stone[gx | gy] * 0.78
    marble = quant(np.clip(0.55 + (srnd - 0.5) * 0.25 + n1 * 0.05, 0, 1), ramp(P['marble'], 4, 0.9, 1.04), bay, 0.5)
    mg = ((xx % K) == 0) | ((yy % K) == 0)
    marble[mg] = marble[mg] * 0.86
    vein = (np.abs(np.sin(xx * 0.08 + n2 * 3.5 + yy * 0.03)) < 0.03)
    marble[vein] = marble[vein] * 0.92
    # 벽돌 (가로 엇갈림, 반 칸 높이)
    bh, bw = K // 4, K // 2
    brow = yy // bh
    bxid = (xx + (brow % 2) * (bw // 2)) // bw
    brnd = (np.sin((brow * 313 + bxid * 71) * 12.9898) * 43758.5453) % 1.0
    brick = quant(np.clip(0.5 + (brnd - 0.5) * 0.6 + n1 * 0.05, 0, 1), ramp(P['brick'], 5, 0.84, 1.12), bay, 0.5)
    bg = ((yy % bh) == 0) | (((xx + (brow % 2) * (bw // 2)) % bw) == 0)
    brick[bg] = brick[bg] * 0.72
    # 붉은 칠 바닥
    redf = quant(field(0.04, 0.05, 0.04, 0.1), ramp(P['red'], 4, 0.86, 1.1), bay)
    # 나무 판자 (부두·다리)
    plank = (yy // (K // 4))
    prnd = (np.sin(plank * 78.233) * 43758.5453) % 1.0
    wood = quant(np.clip(0.45 + (prnd - 0.5) * 0.5 + (np.sin(xx * 0.9 + plank * 3) * 0.04), 0, 1), ramp((150, 110, 72), 5, 0.8, 1.15), bay, 0.5)
    wood[(yy % (K // 4)) == 0] *= 0.62

    # 파리 포석: 작고 둥근 돌 (엇갈린 줄)
    P.setdefault('cobble', P['stone']); P.setdefault('mud', sh(P['dirt'], 0.7)); P.setdefault('check_a', (222, 216, 200)); P.setdefault('check_b', (70, 66, 64)); P.setdefault('floor', (150, 104, 66))
    ch_, cw_ = 5, 7
    crow = yy // ch_
    ccol = (xx + (crow % 2) * 3) // cw_
    crnd = (np.sin((crow * 157 + ccol * 311) * 12.9898) * 43758.5453) % 1.0
    cob = quant(np.clip(0.5 + (crnd - 0.5) * 0.7 + n2 * 0.05, 0, 1), ramp(P['cobble'], 5, 0.78, 1.14), bay, 0.4)
    cgap = ((yy % ch_) == 0) | (((xx + (crow % 2) * 3) % cw_) == 0)
    cob[cgap] = cob[cgap] * 0.62
    chl = ((yy % ch_) == 1) & (((xx + (crow % 2) * 3) % cw_) <= 2) & (((xx + (crow % 2) * 3) % cw_) >= 1)
    cob[chl] = np.minimum(cob[chl] * 1.18, 255)
    mud = quant(field(0.12, 0.14, 0.1, 0.25), ramp(P['mud'], 5, 0.78, 1.12), bay)
    pud = (n2 > 1.6) & (n1 > 0.5)
    mud[pud] = np.array(mix(P['mud'], (150, 160, 170), 0.45))
    tid = ((yy // (K // 2)) + (xx // (K // 2))) % 2
    chk = np.where(tid[..., None] == 0, np.array(P['check_a'], float), np.array(P['check_b'], float)) * (1 + n1[..., None] * 0.03)
    cgl = ((yy % (K // 2)) == 0) | ((xx % (K // 2)) == 0)
    chk[cgl] *= 0.8
    fpl = (xx // (K // 3))
    frnd = (np.sin(fpl * 41.7 + (yy // (K * 2) + fpl % 3) * 9.1) * 43758.5453) % 1.0
    flo = quant(np.clip(0.45 + (frnd - 0.5) * 0.4 + np.sin(yy * 0.7 + fpl * 2) * 0.03, 0, 1), ramp(P['floor'], 5, 0.8, 1.12), bay, 0.5)
    flo[(xx % (K // 3)) == 0] *= 0.7
    flo[((yy + (fpl % 2) * K) % (K * 2)) == 0] *= 0.8

    img = dirt.copy()
    nmask = n1 * 0.18
    layers = [(',T', grass, 0.9, 0.18), (';', steppe, 0.9, 0.2), ('s', sand, 1.1, 0.22), ('M', fieldc, 0.3, 0.05), ('#', court, 0.15, 0.03),
              ('E', earth, 0.0, 0), ('L', earth, 0.35, 0.05), ('n', snow, 0.8, 0.15), ('c', cliff, 0.0, 0),
              ('P', stone, 0.0, 0), ('K', brick, 0.0, 0), ('m', marble, 0.0, 0), ('r', redf, 0.0, 0), ('S', stone, 0.0, 0), ('H', wood, 0.0, 0),
              ('q', cob, 0.0, 0), ('u', mud, 0.9, 0.2), ('z', chk, 0.0, 0), ('o', flo, 0.0, 0)]
    masks = {}
    for chars, tex, blur, nz in layers:
        m = _up(tile_mask(grid, set(chars)), blur, 0.5, n1 if nz else None, nz)
        masks[chars] = m
        img[m] = tex[m]
    # 풀밭 가장자리: 풀이 흙 위로 삐죽 (밝은 테두리 + 아래 그늘)
    gm = masks[',T'] | masks[';']
    edge_dn = gm & ~np.roll(gm, -1, 0)
    img[np.roll(edge_dn, 1, 0) & ~gm] *= 0.82
    img[edge_dn] = img[edge_dn] * 1.12
    # 포장 가장자리 테두리 (돌판·벽돌·대리석·기단 아래쪽 턱)
    for key in ('P', 'K', 'm', 'E', '#', 'q'):
        m = masks[key]
        below = np.roll(m, K // 6, 0) & ~m
        img[below] *= 0.8
        for k in range(1, 3):
            b2 = np.roll(m, k, 0) & ~m
            img[b2] *= 0.86

    # ---- 물: 큰 강(W), 운하·바다(C), 얕은 물(w)
    for ch, base, deep, flowamt in (('W', P['river'], P['river_deep'], 1.0), ('C', P['canal'], P['canal_deep'], 0.5)):
        wm = _up(tile_mask(grid, {ch}), 0.7, 0.5, n1, 0.1)
        if not wm.any(): continue
        din = ndimage.distance_transform_edt(wm)
        t = np.clip(din / (K * 2.5), 0, 1)
        flow = np.sin(xx / 6.0 + yy * 1.2 + n1 * 2.6) * 0.5 + 0.5
        v = np.clip(0.62 - t * 0.45 + (flow - 0.5) * 0.22 * flowamt + n2 * 0.06, 0, 1)
        rp = np.array([mix(deep, base, i / 5) for i in range(6)], float)
        wat = quant(v, rp, bay, 0.8)
        img[wm] = wat[wm]
        foam = wm & (din <= 2.2)
        img[foam] = img[foam] * 0.4 + np.array([236, 230, 206]) * 0.6
        dw = ndimage.distance_transform_edt(~wm)
        wet = (~wm) & (dw <= 3) & ~masks['H']
        img[wet] *= 0.8
        masks[ch] = wm
    sm = _up(tile_mask(grid, {'w'}), 0.8, 0.5, n1, 0.1)
    if sm.any():
        shallow_c = mix(P['river'], (170, 170, 150), 0.4)
        flow = np.sin(xx / 5.0 + yy * 1.1 + n1 * 2) * 0.5 + 0.5
        sw = quant(np.clip(0.5 + (flow - 0.5) * 0.3 + n2 * 0.08, 0, 1), ramp(shallow_c, 4, 0.86, 1.12), bay)
        img[sm] = img[sm] * 0.3 + sw[sm] * 0.7
    masks['w'] = sm

    small = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8), 'RGB')
    big = small.resize((tw * TS, th * TS), Image.NEAREST).convert('RGBA')
    big._masks = masks
    _details(big, grid, P, seed, masks)
    return big

def _details(big, grid, P, seed, masks):
    d = ImageDraw.Draw(big)
    rnd = random.Random(seed)
    th, tw = len(grid), len(grid[0])
    for y in range(th):
        for x in range(tw):
            ch = grid[y][x]; X, Y = x * TS, y * TS
            if ch in ',;':
                base = P['grass'] if ch == ',' else P['steppe']
                for _ in range(5 if ch == ',' else 7):
                    sx, sy = X + rnd.randrange(2, 46, 2), Y + rnd.randrange(6, 46, 2)
                    c = rnd.choice([sh(base, 1.28), sh(base, 0.72), sh(base, 1.12)])
                    d.rectangle([sx, sy - 4, sx + 1, sy], fill=c); d.rectangle([sx + 2, sy - 2, sx + 3, sy], fill=sh(c, 0.9))
            elif ch == 'M':                                   # 조·기장: 고개 숙인 이삭
                for row in range(3):
                    for col in range(4):
                        sx = X + 4 + col * 11 + rnd.randint(-1, 1); sy = Y + 14 + row * 14
                        d.rectangle([sx, sy - 12, sx + 1, sy], fill=(140, 132, 66))
                        d.rectangle([sx + 2, sy - 14, sx + 5, sy - 12], fill=(232, 198, 92)); d.rectangle([sx + 4, sy - 12, sx + 7, sy - 8], fill=(214, 176, 74))
                        d.rectangle([sx + 2, sy - 14, sx + 3, sy - 13], fill=(250, 226, 130))
            elif ch == 'L':
                for yy in range(Y + 6, Y + TS, 10): d.rectangle([X, yy, X + TS - 1, yy + 1], fill=sh(P['earth'], 0.86))
            elif ch == 'E':                                   # 판축: 켜켜이 다진 흙
                for yy in range(Y + 4, Y + TS, 8):
                    d.rectangle([X, yy, X + TS - 1, yy + 1], fill=sh(P['earth'], 0.84))
                    d.rectangle([X, yy + 2, X + TS - 1, yy + 2], fill=sh(P['earth'], 1.08))
                if y + 1 < th and grid[y + 1][x] not in 'EBS':
                    d.rectangle([X, Y + TS - 12, X + TS - 1, Y + TS - 1], fill=sh(P['earth'], 0.7))
                    for yy in range(Y + TS - 10, Y + TS, 3): d.rectangle([X, yy, X + TS - 1, yy], fill=sh(P['earth'], 0.62))
                    for xx in range(X + 2, X + TS, 12): d.rectangle([xx, Y + TS - 12, xx + 1, Y + TS - 1], fill=sh(P['earth'], 0.56))   # 판축 나무틀 자국
            elif ch == 'S':
                for yy in range(Y + 2, Y + TS, 8):
                    d.rectangle([X + 2, yy, X + TS - 3, yy + 5], fill=sh(P['stone'], 1.08))
                    d.rectangle([X + 2, yy + 5, X + TS - 3, yy + 6], fill=sh(P['stone'], 0.7))
            elif ch == '.':
                r = rnd.random()
                if r < 0.3:
                    sx, sy = X + rnd.randrange(4, 40, 2), Y + rnd.randrange(4, 40, 2)
                    d.rectangle([sx, sy, sx + 3, sy + 1], fill=sh(P['dirt'], 0.82)); d.rectangle([sx, sy - 1, sx + 3, sy - 1], fill=sh(P['dirt'], 1.12))
                elif r < 0.4:
                    sx, sy = X + rnd.randrange(8, 36, 2), Y + rnd.randrange(8, 36, 2)
                    d.line([(sx, sy), (sx + 6, sy + 2), (sx + 10, sy + 1)], fill=sh(P['dirt'], 0.86))
            elif ch == 's':
                if rnd.random() < 0.12:
                    sx, sy = X + rnd.randrange(6, 40, 2), Y + rnd.randrange(6, 40, 2)
                    d.rectangle([sx, sy, sx + 3, sy + 1], fill=sh(P['sand'], 0.8))
            elif ch == 'P' and rnd.random() < 0.18:           # 돌판 금
                sx, sy = X + rnd.randrange(8, 36, 2), Y + rnd.randrange(8, 36, 2)
                d.line([(sx, sy), (sx + 4, sy + 4), (sx + 3, sy + 9)], fill=sh(P['stone'], 0.7))
            elif ch == 'K' and rnd.random() < 0.08:           # 이끼 낀 벽돌
                sx, sy = X + rnd.randrange(4, 40, 2), Y + rnd.randrange(4, 40, 2)
                d.rectangle([sx, sy, sx + 3, sy + 1], fill=(110, 130, 80))
    # 물결 무늬
    for ch, base in (('W', P['river']), ('C', P['canal'])):
        wm = masks.get(ch)
        if wm is None or not wm.any(): continue
        gh, gw = wm.shape
        for _ in range(int(tw * th * 1.1)):
            x, y = rnd.randrange(0, tw * TS - 24, 2), rnd.randrange(0, th * TS - 6, 2)
            if not wm[y // PX, x // PX] or not wm[min(gh - 1, (y + 6) // PX), min(gw - 1, (x + 22) // PX)]: continue
            r_ = rnd.random()
            c = sh(base, 1.25) if r_ < 0.6 else (sh(base, 0.78) if r_ < 0.9 else (244, 238, 214))
            L_ = rnd.randrange(6, 22, 2)
            d.rectangle([x, y, x + L_ // 2, y + 1], fill=c); d.rectangle([x + L_ // 2, y + 1, x + L_, y + 2], fill=c)
    sm = masks.get('w')
    if sm is not None and sm.any():
        for _ in range(int(tw * th * 0.9)):
            x, y = rnd.randrange(0, tw * TS - 14, 2), rnd.randrange(0, th * TS - 6, 2)
            if sm[y // PX, x // PX]:
                d.rectangle([x, y, x + 7, y + 1], fill=sh(P['river'], 1.3))
    # 물가 갈대
    for y in range(th):
        for x in range(tw):
            if grid[y][x] in ',.L;' and any(0 <= y + dy < th and grid[y + dy][x] in 'W' for dy in (-1, 1)) and rnd.random() < 0.55:
                X, Y = x * TS, y * TS
                lay = Image.new('RGBA', (TS, TS + 16), (0, 0, 0, 0)); ld = ImageDraw.Draw(lay)
                for _ in range(6):
                    sx = rnd.randrange(2, 44, 2); top = rnd.randrange(14, 22, 2)
                    yb = 30 if (y + 1 < th and grid[y + 1][x] == 'W') else 44
                    ld.rectangle([sx, yb - top, sx + 1, yb], fill=rnd.choice([(108, 136, 64), (130, 156, 76)]))
                    ld.rectangle([sx - 1, yb - top - 6, sx + 2, yb - top], fill=(150, 108, 66))
                big.alpha_composite(outline(lay, 0.6), (X, Y - 8))

def finish(big, grid, light=(1.0, 0.98, 0.94), vignette=0.18, ao=0.32, warm=0.06, night=False):
    """마무리: 벽·물건 둘레 그늘(AO) + 위에서 오는 빛 + 가장자리 어둡게"""
    th, tw = len(grid), len(grid[0])
    a = np.asarray(big.convert('RGB')).astype(float)
    H, W = a.shape[:2]
    wm = np.kron(np.array([[1.0 if c in 'fc' else 0.0 for c in row] for row in grid]), np.ones((TS, TS)))
    if ao > 0 and wm.any():
        dist = ndimage.distance_transform_edt(wm < 0.5)
        occ = np.clip(1 - dist / 22.0, 0, 1) ** 1.6
        # 아래쪽으로 더 길게 (빛이 위에서)
        occ2 = np.roll(np.clip(1 - dist / 30.0, 0, 1), 10, 0) * (wm < 0.5)
        f = 1 - ao * np.maximum(occ, occ2 * 0.7) * (wm < 0.5)
        a *= f[..., None]
    yy, xx = np.mgrid[0:H, 0:W]
    # 큰 빛 얼룩 (구름 그림자 느낌)
    rng = np.random.default_rng(len(grid) * 31 + len(grid[0]))
    cl = ndimage.gaussian_filter(rng.normal(0, 1, (H // 24 + 1, W // 24 + 1)), 3)
    cl = np.kron(cl / (cl.std() + 1e-6), np.ones((24, 24)))[:H, :W]
    a *= (1 + cl * 0.02)[..., None]
    a *= np.array(light)[None, None, :]
    if warm:
        a[..., 0] *= 1 + warm * 0.5; a[..., 2] *= 1 - warm * 0.5
    if vignette:
        cx, cy = W / 2, H / 2
        r = np.sqrt(((xx - cx) / (W / 2)) ** 2 + ((yy - cy) / (H / 2)) ** 2)
        a *= (1 - vignette * np.clip(r - 0.6, 0, 1) ** 1.5)[..., None]
    if night:
        lum = a.mean(axis=2, keepdims=True)
        a = a * 0.45 + lum * 0.15 + np.array([10, 16, 40])
    out = Image.fromarray(np.clip(a, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    big.paste(out, (0, 0))
    return big

def glow(big, x, y, r, col=(255, 190, 100), a=110, blur=None):
    """밤 등불 빛 (덧셈 느낌)"""
    b = blur or r / 3; pad = int(b * 2.5) + 2
    g = Image.new('RGBA', (int(r * 2 + pad * 2), int(r * 2 + pad * 2)), (0, 0, 0, 0))
    ImageDraw.Draw(g).ellipse([pad, pad, pad + r * 2, pad + r * 2], fill=col + (a,))
    g = g.filter(ImageFilter.GaussianBlur(b))
    _paste(big, g, int(x - r - pad), int(y - r - pad))

# ------------------------------------------------------------------ 소품을 작은 판에 그려서 붙이기 (빠름)
class Prop:
    def __init__(self, big, x0, y0, w, h, ol=0.5):
        self.big, self.x0, self.y0, self.ol = big, int(x0), int(y0), ol
        self.im = Image.new('RGBA', (int(w), int(h)), (0, 0, 0, 0))
        self.d = ImageDraw.Draw(self.im)
    def __enter__(self): return self.d
    def __exit__(self, *a):
        im = outline(self.im, self.ol) if self.ol else self.im
        self.big.alpha_composite(im, (self.x0, self.y0)) if self.x0 >= 0 and self.y0 >= 0 else _paste(self.big, im, self.x0, self.y0)

def _paste(big, im, x, y):
    lay = Image.new('RGBA', big.size, (0, 0, 0, 0)); lay.paste(im, (x, y), im); big.alpha_composite(lay)

def soft_shadow(big, box, a=90, blur=5, ellipse=False):
    x0, y0, x1, y1 = [int(v) for v in box]
    pad = blur * 3
    s = Image.new('RGBA', (x1 - x0 + pad * 2, y1 - y0 + pad * 2), (0, 0, 0, 0))
    dd = ImageDraw.Draw(s)
    (dd.ellipse if ellipse else dd.rectangle)([pad, pad, pad + x1 - x0, pad + y1 - y0], fill=(0, 0, 0, a))
    s = s.filter(ImageFilter.GaussianBlur(blur))
    _paste(big, s, x0 - pad, y0 - pad)

def label(big, text, x, y, size=15, col=(255, 248, 230), back=(52, 34, 22, 225), wood=True):
    """나무 팻말 모양 이름표"""
    f = F(size); tw = ImageDraw.Draw(big).textlength(text, font=f)
    w, h = int(tw + 20), int(size * 1.5)
    im = Image.new('RGBA', (w + 4, h + 6), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([2, 4, w + 1, h + 4], 5, fill=(0, 0, 0, 70))
    d.rounded_rectangle([1, 1, w, h], 5, fill=back)
    if wood:
        d.rounded_rectangle([1, 1, w, h], 5, outline=sh(back, 1.6) + (255,), width=1)
        d.line([(5, 3), (w - 5, 3)], fill=sh(back, 1.35) + (200,))
    d.text((w / 2 + 1, h / 2 + 1), text, font=f, fill=col, anchor='mm')
    _paste(big, im, int(x - w / 2), int(y - h / 2))

# ------------------------------------------------------------------ 나무·풀
LEAF = {
    'mulberry': [(46, 92, 52), (66, 118, 62), (92, 146, 76), (128, 174, 92)],
    'willow': [(70, 112, 58), (96, 140, 70), (128, 168, 88), (166, 196, 110)],
    'pine': [(30, 70, 56), (42, 92, 66), (60, 116, 78), (90, 142, 92)],
    'cypress': [(32, 74, 58), (46, 96, 70), (64, 120, 82), (92, 146, 96)],
    'poplar': [(84, 124, 60), (110, 150, 70), (140, 176, 86), (176, 200, 110)],
    'autumn': [(150, 70, 30), (190, 100, 40), (220, 140, 60), (240, 186, 100)],
    'blossom': [(196, 110, 140), (226, 150, 176), (244, 190, 206), (252, 228, 236)],
    'ginkgo': [(170, 140, 40), (206, 176, 60), (232, 206, 90), (250, 232, 140)],
    'dry': [(120, 110, 70), (146, 134, 82), (170, 158, 96), (196, 184, 120)],
    'olive': [(84, 100, 70), (112, 128, 88), (146, 160, 116), (186, 196, 156)],
}

def tree(big, tx, ty, kind='mulberry', s=1.0, ox=24, seed=None):
    rnd = random.Random(seed if seed is not None else tx * 131 + ty * 17 + sum(map(ord, kind)))
    X, Y = tx * TS + ox, ty * TS + 42
    W_, H_ = int(110 * s), int(140 * s)
    soft_shadow(big, [X - 30 * s + 8, Y - 6, X + 30 * s + 14, Y + 8], 90, 4, True)
    col = LEAF.get(kind, LEAF['mulberry'])
    with Prop(big, X - W_ // 2, Y - H_ + 8, W_, H_, 0.45) as d:
        cx, by = W_ // 2, H_ - 8
        bark, bark2 = (96, 70, 50), (70, 50, 36)
        if kind == 'pine':
            d.polygon([(cx - 4, by), (cx + 4, by), (cx + 2, by - 70 * s), (cx - 2, by - 70 * s)], fill=bark)
            d.line([(cx - 3, by), (cx - 1, by - 60 * s)], fill=bark2)
            for i, (yo, w) in enumerate([(-74, 26), (-60, 34), (-44, 40), (-30, 34)]):
                y0 = by + yo * s
                for c_i, c in enumerate(col):
                    ww = (w - c_i * 4) * s
                    d.ellipse([cx - ww + c_i * 2 - 4, y0 - 9 * s + c_i * 1, cx + ww - c_i * 3 - 4, y0 + 7 * s - c_i * 2], fill=c)
                    if c_i == 0: d.ellipse([cx - ww + 6, y0 - 7 * s, cx + ww + 2, y0 + 9 * s], fill=c)
        elif kind == 'cypress':
            d.rectangle([cx - 3, by - 20 * s, cx + 3, by], fill=bark)
            for c_i, c in enumerate(col):
                d.ellipse([cx - (18 - c_i * 3) * s, by - (100 - c_i * 4) * s, cx + (16 - c_i * 4) * s, by - 14 * s - c_i * 2], fill=c)
        elif kind == 'poplar':
            d.rectangle([cx - 3, by - 30 * s, cx + 3, by], fill=bark)
            for c_i, c in enumerate(col):
                d.ellipse([cx - (16 - c_i * 3) * s, by - (112 - c_i * 5) * s, cx + (14 - c_i * 3) * s, by - 24 * s - c_i * 3], fill=c)
        elif kind == 'bamboo':
            for k in range(7):
                bx = cx - 24 * s + k * 8 * s + rnd.randint(-2, 2); top = by - rnd.randint(70, 110) * s
                d.line([(bx, by), (bx + rnd.randint(-4, 4), top)], fill=(96, 150, 70), width=3)
                for jy in range(int(top), by, 12): d.line([(bx - 1, jy), (bx + 2, jy)], fill=(60, 110, 50))
                for _ in range(5):
                    lx, ly = bx + rnd.randint(-10, 10), top + rnd.randint(0, 40)
                    d.polygon([(lx, ly), (lx + 10, ly + 3), (lx, ly + 5)], fill=rnd.choice([(80, 140, 64), (110, 170, 80), (60, 120, 56)]))
        else:
            # 줄기 + 가지
            d.polygon([(cx - 5 * s, by), (cx + 5 * s, by), (cx + 3 * s, by - 46 * s), (cx - 3 * s, by - 46 * s)], fill=bark)
            d.line([(cx - 3 * s, by - 2), (cx - 2 * s, by - 40 * s)], fill=bark2, width=2)
            d.line([(cx, by - 30 * s), (cx - 16 * s, by - 50 * s)], fill=bark, width=3)
            d.line([(cx, by - 34 * s), (cx + 16 * s, by - 54 * s)], fill=bark, width=3)
            blobs = [(0, -78, 30), (-22, -64, 22), (22, -66, 22), (-12, -90, 18), (14, -88, 18), (0, -60, 20)]
            for c_i, c in enumerate(col):
                for (bx, by_, r) in blobs:
                    rr = (r - c_i * 5) * s
                    if rr <= 2: continue
                    ox_ = bx * s - c_i * 2.5; oy = by_ * s - c_i * 3
                    d.ellipse([cx + ox_ - rr, by + oy - rr * 0.9, cx + ox_ + rr, by + oy + rr * 0.9], fill=c)
            # 잎 알갱이 (도트 질감)
            for _ in range(int(90 * s)):
                a = rnd.random() * math.tau; r = rnd.random() ** 0.6 * 34 * s
                px, py = cx + math.cos(a) * r, by - 74 * s + math.sin(a) * r * 0.85
                c = col[min(3, max(0, int(2 - math.sin(a) * 1.5 + rnd.random())))]
                d.rectangle([px, py, px + 2, py + 2], fill=c)
            if kind == 'willow':                               # 늘어진 가지
                for _ in range(int(34 * s)):
                    x0 = cx + rnd.uniform(-34, 34) * s; y0 = by - rnd.uniform(60, 96) * s
                    L_ = rnd.uniform(20, 40) * s
                    d.line([(x0, y0), (x0 + rnd.uniform(-2, 2), y0 + L_)], fill=rnd.choice(col[1:]), width=2)
            if kind == 'blossom':
                for _ in range(40):
                    a = rnd.random() * math.tau; r = rnd.random() * 30 * s
                    px, py = cx + math.cos(a) * r, by - 76 * s + math.sin(a) * r * 0.8
                    d.rectangle([px, py, px + 1, py + 1], fill=(255, 250, 250))

def bush(big, tx, ty, ox=24, oy=40, s=1.0, kind='green'):
    col = {'green': LEAF['mulberry'], 'dry': LEAF['dry'], 'tamarisk': [(150, 110, 120), (176, 130, 140), (200, 160, 170), (226, 196, 204)]}[kind]
    X, Y = tx * TS + ox, ty * TS + oy
    soft_shadow(big, [X - 16 * s, Y - 4, X + 18 * s, Y + 6], 70, 3, True)
    rnd = random.Random(tx * 7 + ty * 3)
    with Prop(big, X - 24 * s, Y - 30 * s, 48 * s, 34 * s, 0.5) as d:
        cx, by = 24 * s, 30 * s
        for c_i, c in enumerate(col):
            for (bx, byy, r) in [(-8, -10, 10), (8, -10, 10), (0, -16, 11)]:
                rr = (r - c_i * 2.5) * s
                d.ellipse([cx + bx * s - rr - c_i, by + byy * s - rr * 0.8 - c_i, cx + bx * s + rr - c_i, by + byy * s + rr * 0.8 - c_i], fill=c)
        for _ in range(16):
            px, py = cx + rnd.uniform(-16, 16) * s, by + rnd.uniform(-24, -4) * s
            d.rectangle([px, py, px + 1, py + 1], fill=col[3])

def rock(big, tx, ty, s=1.0, col=(150, 142, 128), ox=24, oy=40):
    X, Y = tx * TS + ox, ty * TS + oy
    soft_shadow(big, [X - 18 * s, Y - 4, X + 22 * s, Y + 6], 80, 3, True)
    with Prop(big, X - 24 * s, Y - 30 * s, 48 * s, 34 * s, 0.5) as d:
        cx, by = 24 * s, 30 * s
        d.polygon([(cx - 18 * s, by), (cx - 15 * s, by - 14 * s), (cx - 4 * s, by - 24 * s), (cx + 12 * s, by - 18 * s), (cx + 18 * s, by)], fill=col)
        d.polygon([(cx - 4 * s, by - 24 * s), (cx + 12 * s, by - 18 * s), (cx + 18 * s, by), (cx + 2 * s, by)], fill=sh(col, 0.8))
        d.polygon([(cx - 15 * s, by - 14 * s), (cx - 4 * s, by - 24 * s), (cx - 2 * s, by - 16 * s), (cx - 12 * s, by - 8 * s)], fill=sh(col, 1.15))

def scatter(big, grid, seed=7, density=1.0, flowers=True, pal='loess'):
    """풀포기·들꽃·자갈·발자국 흩뿌리기"""
    P = PAL[pal] if isinstance(pal, str) else pal
    th, tw = len(grid), len(grid[0])
    rnd = random.Random(seed)
    d = ImageDraw.Draw(big)
    for y in range(th):
        for x in range(tw):
            ch = grid[y][x]; X, Y = x * TS, y * TS
            r = rnd.random()
            if ch in ',;':
                g = P['grass'] if ch == ',' else P['steppe']
                if r < 0.2 * density:
                    cx, cy = X + rnd.randrange(8, 40, 2), Y + rnd.randrange(14, 42, 2)
                    for k in range(-3, 4):
                        c = sh(g, 0.66) if k % 2 else sh(g, 1.24)
                        hgt = 8 - abs(k) * 2 + rnd.randint(0, 2)
                        d.rectangle([cx + k * 2, cy - hgt, cx + k * 2 + 1, cy], fill=c)
                elif r < 0.28 * density and flowers and ch == ',':
                    cx, cy = X + rnd.randrange(6, 42, 2), Y + rnd.randrange(8, 42, 2)
                    c = rnd.choice([(252, 240, 150), (250, 250, 240), (232, 150, 172), (190, 170, 240), (250, 190, 120)])
                    for (ox, oy) in [(0, 0), (6, 2), (2, 6)]:
                        d.rectangle([cx + ox - 1, cy + oy - 1, cx + ox + 2, cy + oy + 2], fill=c); d.rectangle([cx + ox, cy + oy, cx + ox + 1, cy + oy + 1], fill=(240, 196, 70))
                elif r < 0.31 * density:
                    rock(big, x, y, 0.35, ox=rnd.randint(10, 38), oy=rnd.randint(16, 44))
            elif ch in '.#':
                if r < 0.16 * density:
                    for _ in range(3):
                        cx, cy = X + rnd.randrange(4, 44, 2), Y + rnd.randrange(4, 44, 2)
                        d.rectangle([cx, cy, cx + 3, cy + 1], fill=sh(P['dirt'], 0.78)); d.rectangle([cx, cy - 1, cx + 3, cy - 1], fill=sh(P['dirt'], 1.14))
                elif r < 0.22 * density and ch == '.':
                    cx, cy = X + rnd.randrange(10, 30, 2), Y + rnd.randrange(10, 30, 2)
                    for k in range(3):
                        d.rectangle([cx + k * 6, cy + (k % 2) * 6, cx + k * 6 + 2, cy + (k % 2) * 6 + 4], fill=sh(P['dirt'], 0.84))
                elif r < 0.28 * density:
                    cx, cy = X + rnd.randrange(8, 40, 2), Y + rnd.randrange(14, 42, 2)
                    for k in (-2, 0, 2): d.rectangle([cx + k, cy - 6 + abs(k), cx + k + 1, cy], fill=sh(P['grass'], 0.9))
            elif ch == 's' and r < 0.06 * density:
                bush(big, x, y, rnd.randint(10, 38), rnd.randint(24, 44), 0.6, 'dry')

# ------------------------------------------------------------------ 해방 편 색
KO = dict(FR, dirt=(170, 150, 118), grass=(110, 138, 76), stone=(178, 172, 160), cobble=(150, 146, 138), brick=(150, 96, 76),
          court=(186, 172, 146), earth=(168, 146, 112), mud=(110, 92, 66), floor=(140, 100, 64), check_a=(220, 214, 198), check_b=(120, 112, 104),
          river=(92, 124, 132), river_deep=(60, 92, 108), canal=(70, 104, 124), canal_deep=(44, 72, 98), marble=(214, 210, 198))
PAL['seoul'] = KO
PAL['seoul_w'] = dict(KO, dirt=(160, 150, 138), grass=(130, 132, 100), snow=(232, 236, 242), mud=(110, 100, 90))
PAL['busan'] = dict(KO, dirt=(176, 156, 120), sand=(206, 190, 150), canal=(60, 100, 126), canal_deep=(36, 66, 96))
PAL['hungnam'] = dict(KO, dirt=(170, 168, 168), snow=(236, 240, 246), canal=(66, 90, 112), canal_deep=(38, 56, 80), stone=(160, 160, 160))
PAL['line38'] = dict(KO, grass=(124, 140, 74), field=(196, 170, 96), dirt=(164, 140, 104), river=(100, 128, 130), river_deep=(70, 100, 110))

# ---- 고대 그리스 · 지중해
PAL['hellas'] = dict(FR, dirt=(206, 178, 134), grass=(138, 150, 88), steppe=(186, 176, 112), sand=(228, 208, 160), field=(204, 182, 108),
                     court=(214, 198, 160), earth=(196, 170, 126), stone=(216, 206, 182), cobble=(190, 180, 160), marble=(240, 236, 226),
                     canal=(58, 120, 168), canal_deep=(34, 86, 140), river=(80, 140, 170), river_deep=(50, 110, 150), floor=(176, 140, 96),
                     check_a=(236, 230, 214), check_b=(180, 120, 90), cliff=(186, 160, 120), mud=(150, 120, 90))
PAL['egypt'] = dict(PAL['hellas'], dirt=(222, 196, 146), sand=(234, 214, 166), stone=(226, 214, 186), grass=(120, 150, 90))
PAL['persia'] = dict(PAL['hellas'], dirt=(200, 176, 136), stone=(210, 196, 170), check_a=(214, 196, 160), check_b=(186, 150, 112))

