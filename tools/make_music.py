"""국악풍 BGM 합성 (모두 새로 작곡한 곡). 끊김 없이 반복되도록 끝의 잔향을 앞에 겹칩니다.
결과: <out>/<name>.wav  (변환은 ffmpeg로 따로)"""
import sys, os
import numpy as np
from scipy.signal import fftconvolve, butter, lfilter

SR = 44100
OUT = sys.argv[1]
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(7)

def midi(n):
    return 440.0 * 2 ** ((n - 69) / 12)

NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def nm(s):  # 'G3' -> midi
    return 12 * (int(s[-1]) + 1) + NOTE[s[0]]

def lowpass(x, fc, order=2):
    b, a = butter(order, fc / (SR / 2), 'low')
    return lfilter(b, a, x)

def bandpass(x, lo, hi, order=2):
    b, a = butter(order, [lo / (SR / 2), hi / (SR / 2)], 'band')
    return lfilter(b, a, x)

# ------------------------------------------------------------------ 악기
def gayageum(f, dur, vel=0.8, bright=1.0):
    """가야금 느낌: 뜯는 소리 + 배음 감쇠 + 뒤쪽 농현(떨림)"""
    n = int(SR * (dur + 1.2))
    t = np.arange(n) / SR
    vib_depth = np.clip((t - 0.18) / 0.4, 0, 1) * 0.006
    phase_mod = vib_depth * np.sin(2 * np.pi * 5.2 * t)
    y = np.zeros(n)
    for h in range(1, 9):
        amp = (1 / h ** 1.25) * (bright if h > 2 else 1)
        dec = 2.2 + 1.1 * h
        inst = 2 * np.pi * f * h * (t + np.cumsum(phase_mod) / SR)
        y += amp * np.exp(-dec * t) * np.sin(inst + rng.random() * 6.28)
    pluck = rng.standard_normal(int(SR * 0.012)) * np.linspace(1, 0, int(SR * 0.012))
    y[:len(pluck)] += 0.35 * bandpass(pluck, 800, 5000)
    y *= np.minimum(1, t / 0.002)
    y *= vel
    # 줄을 손으로 막는 끝맺음
    rel = np.ones(n)
    k = int(SR * dur)
    if k < n:
        rel[k:] = np.exp(-np.arange(n - k) / (SR * 0.25))
    return y * rel * 0.5

def daegeum(f, dur, vel=0.6, slide=True):
    """대금 느낌: 부드러운 사인 + 숨소리 + 점점 깊어지는 떨림"""
    n = int(SR * (dur + 0.25))
    t = np.arange(n) / SR
    vib = np.clip((t - 0.3) / 0.6, 0, 1) * 0.012 * np.sin(2 * np.pi * 5.4 * t)
    bend = np.where(t < 0.07, -0.03 * (1 - t / 0.07), 0) if slide else 0
    ff = f * (1 + vib + bend)
    ph = 2 * np.pi * np.cumsum(ff) / SR
    y = np.sin(ph) + 0.28 * np.sin(2 * ph) + 0.08 * np.sin(3 * ph)
    breath = bandpass(rng.standard_normal(n), f * 0.9, min(f * 3.5, 15000)) * 0.12
    env = np.minimum(1, t / 0.09) * np.clip((dur + 0.2 - t) / 0.2, 0, 1)
    env *= 0.85 + 0.15 * np.sin(2 * np.pi * 0.7 * t)
    return (y + breath) * env * vel * 0.32

def drone(f, dur, vel=0.4):
    """아쟁 느낌 낮은 지속음"""
    n = int(SR * dur)
    t = np.arange(n) / SR
    saw = np.zeros(n)
    for h in range(1, 14):
        saw += np.sin(2 * np.pi * f * h * t * (1 + 0.0015 * np.sin(2 * np.pi * 0.3 * t))) / h
    saw = lowpass(saw, 900)
    env = np.minimum(1, t / 1.5) * np.minimum(1, (dur - t) / 1.5)
    trem = 0.8 + 0.2 * np.sin(2 * np.pi * 0.25 * t)
    return saw * env * trem * vel * 0.18

def drone_loop(f, seconds, vel=0.4):
    """반복 지점에서 끊기지 않는 지속음: 모든 주파수가 곡 길이 안에서 정수 번 돌도록 맞춤"""
    n = int(SR * seconds)
    t = np.arange(n) / SR
    L = n / SR
    q = lambda fr: max(1, round(fr * L)) / L
    y = np.zeros(n)
    for h in range(1, 14):
        fh = q(f * h)
        amp = (1 / h) / np.sqrt(1 + (f * h / 900) ** 4)
        y += amp * np.sin(2 * np.pi * fh * t + h)
    trem = 0.8 + 0.2 * np.sin(2 * np.pi * q(0.25) * t)
    return y * trem * vel * 0.18

def bell(f, dur=7.0, vel=0.5):
    n = int(SR * dur)
    t = np.arange(n) / SR
    y = np.zeros(n)
    for ratio, amp, dec in [(1, 1, 0.5), (2.76, 0.5, 0.9), (5.40, 0.25, 1.6), (8.93, 0.12, 2.6), (0.5, 0.35, 0.35)]:
        y += amp * np.exp(-dec * t) * np.sin(2 * np.pi * f * ratio * t)
    y *= np.minimum(1, t / 0.004)
    return y * vel * 0.3

def janggu(kind, vel=0.6):
    n = int(SR * 0.6)
    t = np.arange(n) / SR
    if kind in ('kung', 'deong'):
        f = 95 * np.exp(-t * 6) + 62
        y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
        y += 0.15 * lowpass(rng.standard_normal(n), 500) * np.exp(-t * 30)
        if kind == 'deong':
            y += 0.6 * bandpass(rng.standard_normal(n), 1800, 6000) * np.exp(-t * 45)
    else:  # deok: 채편
        y = bandpass(rng.standard_normal(n), 1600, 7000) * np.exp(-t * 55)
        y += 0.4 * np.sin(2 * np.pi * 420 * t) * np.exp(-t * 40)
    return y * vel * 0.55

def buk(vel=0.7):
    n = int(SR * 0.9)
    t = np.arange(n) / SR
    f = 70 * np.exp(-t * 4) + 45
    y = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 5)
    y += 0.2 * lowpass(rng.standard_normal(n), 300) * np.exp(-t * 20)
    return y * vel * 0.8

def whoosh(dur=2.0, vel=0.6):
    n = int(SR * dur)
    t = np.arange(n) / SR
    x = rng.standard_normal(n)
    out = np.zeros(n)
    seg = 2048
    for i in range(0, n, seg):
        k = i / n
        lo = 200 + 4000 * k
        out[i:i + seg] = bandpass(x[i:i + seg], lo, min(lo * 2.5, 18000))
    env = np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 1.5
    return out * env * vel * 0.5

# ------------------------------------------------------------------ 믹스 도구
class Track:
    def __init__(self, seconds):
        self.L = int(SR * seconds)
        self.seconds = self.L / SR
        self.buf = np.zeros(self.L + SR * 6)
        self.loopbuf = np.zeros(self.L)
    def add_loop(self, sig, gain=1.0):
        self.loopbuf += sig[:self.L] * gain
    def add(self, sig, at, gain=1.0):
        i = int(at * SR)
        j = min(len(self.buf), i + len(sig))
        self.buf[i:j] += sig[:j - i] * gain
    def render(self, reverb=0.28, loop=True):
        ir_n = int(SR * 2.2)
        tt = np.arange(ir_n) / SR
        ir = rng.standard_normal(ir_n) * np.exp(-tt * 2.6)
        ir = lowpass(ir, 5000)
        ir /= np.sqrt(np.sum(ir ** 2))
        wet = fftconvolve(self.buf, ir)[:len(self.buf)]
        mix = self.buf + reverb * wet
        if loop:
            out = mix[:self.L].copy()
            tail = mix[self.L:]
            out[:len(tail)] += tail[:self.L]
            out += self.loopbuf
        else:
            out = mix[:self.L] + self.loopbuf
        out = np.tanh(out * 1.4) / np.tanh(1.4)
        out /= max(1e-9, np.max(np.abs(out))) / 0.89
        return out

def save_wav(name, mono, width=0.25):
    # 살짝 넓은 스테레오 (짧은 지연)
    d = int(SR * 0.011)
    left = mono
    right = np.concatenate([mono[-d:], mono[:-d]])
    st = np.stack([left * (1 - width * 0.3) + right * width * 0.3, right * (1 - width * 0.3) + left * width * 0.3], 1)
    st = (np.clip(st, -1, 1) * 32767).astype(np.int16)
    import wave
    with wave.open(os.path.join(OUT, name + '.wav'), 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())

# ------------------------------------------------------------------ 음계
PYEONG = [nm(x) for x in ['G3', 'A3', 'C4', 'D4', 'E4', 'G4', 'A4', 'C5', 'D5', 'E5', 'G5']]      # 평조
GYEMYEON = [nm(x) for x in ['A2', 'C3', 'D3', 'E3', 'G3', 'A3', 'C4', 'D4', 'E4', 'G4', 'A4', 'C5']]  # 계면조

def seq(track, notes, start, eighth, inst, scale, octave=0, gain=1.0, **kw):
    t = start
    for deg, length in notes:
        if deg is not None:
            f = midi(scale[deg] + 12 * octave)
            track.add(inst(f, length * eighth * 0.95, **kw), t, gain)
        t += length * eighth
    return t

# =================================================================== 1. 탐험 (평조, 6/8)
def explore():
    beat = 60 / 64          # 점4분음표
    e = beat / 3            # 8분음표
    bar = 6 * e
    A = [(5, 3), (6, 1), (5, 1), (4, 1), (3, 3), (4, 2), (3, 1), (2, 2), (3, 1), (4, 3), (3, 6)]
    B = [(6, 3), (7, 1), (6, 1), (5, 1), (4, 3), (5, 2), (6, 1), (5, 2), (4, 1), (3, 2), (2, 1), (2, 6)]
    C = [(7, 2), (8, 1), (7, 3), (6, 2), (5, 1), (6, 3), (5, 1), (4, 1), (3, 1), (4, 3), (5, 6)]
    D = [(4, 3), (3, 1), (2, 1), (3, 1), (4, 2), (5, 1), (4, 3), (3, 2), (2, 1), (1, 3), (2, 6)]
    form = [A, B, A, D, C, B, C, D]
    T = Track(32 * bar)
    t = 0
    for i, ph in enumerate(form):
        seq(T, ph, t, e, gayageum, PYEONG, gain=0.9, vel=0.75)
        if i >= 4:   # 후반: 대금이 길게 받쳐 줌
            first = ph[0][0]
            for b in range(4):
                deg = [first, first - 1, first - 2, 2 if b == 3 else first - 1][b]
                T.add(daegeum(midi(PYEONG[max(0, deg)] + 12), bar * 0.95, vel=0.42), t + b * bar, 0.8)
        t += 4 * bar
    roots = [2, 0, 1, 2, 2, 0, 3, 2] * 4
    for b in range(32):
        r = PYEONG[roots[b]] - 12
        T.add(gayageum(midi(r), 3 * e, vel=0.55, bright=0.6), b * bar, 0.8)
        T.add(gayageum(midi(r + 7), 2 * e, vel=0.4, bright=0.6), b * bar + 3 * e, 0.7)
        T.add(janggu('deong' if b % 4 == 0 else 'kung', 0.5), b * bar)
        T.add(janggu('deok', 0.35), b * bar + 3 * e)
        T.add(janggu('deok', 0.22), b * bar + 5 * e)
    T.add_loop(drone_loop(midi(nm('C2')), T.seconds), 0.5)
    return T.render(0.3)

# =================================================================== 2. 긴장 (계면조, 6/8 빠르게)
def tension():
    beat = 60 / 80
    e = beat / 3
    bar = 6 * e
    pats = [[5, 3, 5, 2, 5, 3], [5, 3, 5, 4, 3, 2], [4, 2, 4, 1, 4, 2], [3, 1, 3, 0, 2, 3]]
    T = Track(32 * bar)
    for b in range(32):
        p = pats[b % 4] if b % 8 < 4 else pats[(b + 2) % 4]
        for k, deg in enumerate(p):
            T.add(gayageum(midi(GYEMYEON[deg]), e * 0.9, vel=0.7 if k % 3 == 0 else 0.5, bright=0.8), b * bar + k * e, 0.85)
        T.add(buk(0.7), b * bar)
        T.add(buk(0.45), b * bar + e)
        if b % 2 == 1:
            T.add(janggu('deok', 0.4), b * bar + 3 * e)
            T.add(janggu('deok', 0.3), b * bar + 4 * e)
    T.add_loop(drone_loop(midi(nm('A1')), T.seconds, 0.55))
    T.add_loop(drone_loop(midi(nm('E2')), T.seconds, 0.35))
    wail = [(10, 12), (9, 6), (8, 6), (8, 12), (7, 6), (6, 6), (7, 9), (8, 3), (9, 6), (8, 6), (6, 18), (5, 6)]
    seq(T, wail, 8 * bar, e, daegeum, GYEMYEON, gain=0.85, vel=0.5)
    seq(T, wail, 24 * bar, e, daegeum, GYEMYEON, gain=0.85, vel=0.5)
    return T.render(0.32)

# =================================================================== 3. 피날레 (평조, 밝게)
def finale():
    beat = 60 / 96
    e = beat / 3
    bar = 6 * e
    T = Track(32 * bar)
    roots = [2, 0, 3, 2, 2, 0, 1, 2]
    for b in range(32):
        r = roots[b % 8]
        arp = [r, r + 2, r + 3, r + 5, r + 3, r + 2]
        for k, deg in enumerate(arp):
            T.add(gayageum(midi(PYEONG[min(deg, 10)]), e, vel=0.6 if k else 0.8, bright=1.1), b * bar + k * e, 0.75)
        T.add(gayageum(midi(PYEONG[r] - 12), 3 * e, vel=0.6, bright=0.6), b * bar, 0.8)
        T.add(janggu('deong', 0.6), b * bar)
        T.add(janggu('kung', 0.45), b * bar + 2 * e)
        T.add(janggu('deok', 0.45), b * bar + 3 * e)
        T.add(janggu('kung', 0.35), b * bar + 4 * e)
        T.add(janggu('deok', 0.3), b * bar + 5 * e)
    mel = [(5, 3), (7, 3), (6, 2), (5, 1), (4, 3), (5, 3), (6, 3), (7, 6),
           (8, 3), (7, 3), (6, 2), (5, 1), (6, 3), (5, 2), (4, 1), (3, 3), (2, 6)]
    mel2 = [(7, 3), (8, 3), (9, 2), (8, 1), (7, 3), (6, 3), (7, 3), (8, 6),
            (9, 3), (8, 3), (7, 2), (6, 1), (5, 3), (6, 2), (5, 1), (4, 3), (5, 6)]
    t = seq(T, mel, 0, e, daegeum, PYEONG, octave=1, gain=0.8, vel=0.5)
    t = seq(T, mel2, 8 * bar, e, daegeum, PYEONG, octave=1, gain=0.8, vel=0.5)
    t = seq(T, mel, 16 * bar, e, daegeum, PYEONG, octave=1, gain=0.8, vel=0.5)
    t = seq(T, mel2, 24 * bar, e, daegeum, PYEONG, octave=1, gain=0.8, vel=0.5)
    T.add_loop(drone_loop(midi(nm('C2')), T.seconds, 0.4))
    return T.render(0.26)

# =================================================================== 4. 타이틀 (신비롭게, 자유 리듬)
def title(seconds=64.0, loop=True):
    T = Track(seconds)
    T.add_loop(drone_loop(midi(nm('C2')), T.seconds, 0.55))
    T.add_loop(drone_loop(midi(nm('G2')), T.seconds, 0.35))
    for s in np.arange(0, seconds, 16):
        T.add(bell(midi(nm('C4')), 9, 0.55), s + 0.2)
        T.add(bell(midi(nm('G4')), 7, 0.25), s + 8.2)
    phrases = [(1.5, 'C5', 3.2), (4.8, 'A4', 1.4), (6.3, 'G4', 3.8), (11.0, 'E4', 1.8), (12.9, 'G4', 1.3), (14.3, 'A4', 4.6),
               (20.0, 'D5', 2.6), (22.7, 'C5', 1.4), (24.2, 'A4', 2.2), (26.5, 'G4', 4.5), (32.5, 'E5', 2.8), (35.4, 'D5', 1.2),
               (36.7, 'C5', 2.4), (39.2, 'A4', 1.6), (40.9, 'G4', 5.2), (47.5, 'A4', 2.0), (49.6, 'C5', 2.0), (51.7, 'D5', 1.6),
               (53.4, 'C5', 5.0), (59.0, 'G4', 4.0)]
    for st, n, d in phrases:
        if st < seconds:
            T.add(daegeum(midi(nm(n)), d, vel=0.5), st, 0.9)
    for s in [9.0, 25.0, 41.0, 57.0]:
        for k, deg in enumerate([0, 2, 3, 4, 5, 7, 8]):
            if s + k * 0.09 < seconds:
                T.add(gayageum(midi(PYEONG[deg]), 1.2, vel=0.4), s + k * 0.09, 0.7)
    return T.render(0.4, loop=loop)

if __name__ == '__main__':
    which = sys.argv[2:] or ['title', 'explore', 'tension', 'finale']
    if 'title' in which: save_wav('Goryeo_Title', title())
    if 'explore' in which: save_wav('Goryeo_Explore', explore())
    if 'tension' in which: save_wav('Goryeo_Tension', tension())
    if 'finale' in which: save_wav('Goryeo_Finale', finale())
    print('ok')
