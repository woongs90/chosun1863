"""금지된 주파수 배경음악·효과음 (전보 소년 악기 재사용 + 새 곡)
 옛 설명: 전보 소년 (모두 코드로 새로 만든 곡)
 Tel_Title   주제 선율 「전신선」 (현악·피아노 + 모스 부호 박자)   Tel_Office  전신국 - 피아노와 똑딱이는 키
 Tel_Tension 긴장 - 낮은 현의 고동          Tel_Africa  아드와 - 현을 뜯는 소리와 북 (에티오피아 5음 음계)
 Tel_Dark    콩고 - 느리고 어두운 현          Tel_Asia    베이징·콜카타·브라이턴 - 피리와 뜯는 현
 Tel_London  런던 거리 - 브라스 밴드 행진     Tel_War     참호 - 낮은 북과 현, 바람
 Tel_Paris   파리 - 아코디언 왈츠             Tel_Ending  「전신선」 느리게
 효과음: Tel_Morse(전신 키) Tel_Boom(포성) Tel_Shot(총소리) Tel_Paper(종이)
"""
import os, sys, subprocess, wave
import numpy as np
from scipy.signal import fftconvolve, butter, lfilter

SR = 44100
rng = np.random.default_rng(1945)

def midi(n): return 440.0 * 2 ** ((n - 69) / 12)
NOTE = {'C': 0, 'D': 2, 'E': 4, 'F': 5, 'G': 7, 'A': 9, 'B': 11}
def nm(s):
    acc = 1 if '#' in s else (-1 if 'b' in s[1:] else 0)
    return 12 * (int(s[-1]) + 1) + NOTE[s[0]] + acc
def lowpass(x, fc, order=2):
    b, a = butter(order, min(0.99, fc / (SR / 2)), 'low'); return lfilter(b, a, x)
def bandpass(x, lo, hi, order=2):
    b, a = butter(order, [lo / (SR / 2), min(0.99, hi / (SR / 2))], 'band'); return lfilter(b, a, x)
def T_(dur): n = int(SR * dur); return n, np.arange(n) / SR

# ------------------------------------------------------------------ 악기
def harpsi(f, dur, vel=0.6):
    n, t = T_(dur + 0.6)
    y = sum(a * np.sin(2 * np.pi * f * h * t + h) * np.exp(-t * (2.5 + h * 0.9)) for h, a in [(1, 1), (2, .7), (3, .55), (4, .4), (5, .3), (6, .22), (8, .12)])
    return y * np.minimum(1, t / 0.002) * vel * 0.16
def piano(f, dur, vel=0.6):
    n, t = T_(dur + 1.2)
    y = sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t * (1.2 + h * 0.7)) for h, a in [(1, 1), (2, .45), (3, .22), (4, .12), (5, .06)])
    return lowpass(y, 5000) * np.minimum(1, t / 0.004) * vel * 0.2
def flute(f, dur, vel=0.5):
    n, t = T_(dur + 0.1)
    vib = 1 + 0.006 * np.sin(2 * np.pi * 5.2 * t) * np.clip(t / 0.3, 0, 1)
    ph = 2 * np.pi * f * np.cumsum(vib) / SR
    y = np.sin(ph) + 0.18 * np.sin(2 * ph) + 0.06 * np.sin(3 * ph)
    y += 0.05 * bandpass(rng.standard_normal(n), f * 0.8, min(f * 3, 18000))
    env = np.clip(np.minimum(t / 0.05, (dur + 0.1 - t) / 0.12), 0, 1)
    return y * env * vel * 0.2
def strings(f, dur, vel=0.5, att=0.25):
    n, t = T_(dur + 0.4)
    y = np.zeros(n)
    for det in (-0.004, 0, 0.005):
        ph = 2 * np.pi * f * (1 + det) * t + 0.002 * np.sin(2 * np.pi * 5 * t) * 2 * np.pi * f / 5
        y += 2 * (ph / (2 * np.pi) % 1) - 1
    y = lowpass(y, min(3200, f * 6))
    env = np.clip(np.minimum(t / att, (dur + 0.4 - t) / 0.4), 0, 1)
    return y * env * vel * 0.06
def organ(f, dur, vel=0.5):
    n, t = T_(dur + 0.3)
    y = sum(a * np.sin(2 * np.pi * f * h * t) for h, a in [(0.5, .5), (1, 1), (2, .6), (3, .3), (4, .25), (6, .1)])
    env = np.clip(np.minimum(t / 0.06, (dur + 0.3 - t) / 0.3), 0, 1)
    return y * env * vel * 0.07
def musicbox(f, dur, vel=0.5):
    n, t = T_(2.0)
    y = np.sin(2 * np.pi * f * t) * np.exp(-t * 3) + 0.4 * np.sin(2 * np.pi * f * 4.1 * t) * np.exp(-t * 9)
    return y * np.minimum(1, t / 0.001) * vel * 0.3
def accordion(f, dur, vel=0.5):
    n, t = T_(dur + 0.1)
    y = np.zeros(n)
    for det in (0, 0.006):
        ph = 2 * np.pi * f * (1 + det) * t
        y += np.sign(np.sin(ph)) * 0.5 + np.sin(2 * ph) * 0.3
    y = lowpass(y, 2400)
    env = np.clip(np.minimum(t / 0.04, (dur + 0.1 - t) / 0.08), 0, 1)
    return y * env * vel * 0.06
def gayageum(f, dur, vel=0.6):
    n, t = T_(dur + 1.0)
    vib = 1 + 0.012 * np.sin(2 * np.pi * 5.5 * t) * np.clip((t - 0.25) / 0.3, 0, 1)
    ph = 2 * np.pi * f * np.cumsum(vib) / SR
    y = sum(a * np.sin(h * ph) * np.exp(-t * (2.0 + h * 1.1)) for h, a in [(1, 1), (2, .5), (3, .35), (4, .2), (5, .1)])
    y += 0.25 * bandpass(rng.standard_normal(n), 2000, 6000) * np.exp(-t * 60)
    return y * np.minimum(1, t / 0.002) * vel * 0.22
def daegeum(f, dur, vel=0.5):
    n, t = T_(dur + 0.2)
    vib = 1 + 0.01 * np.sin(2 * np.pi * 4.6 * t) * np.clip((t - 0.3) / 0.4, 0, 1)
    ph = 2 * np.pi * f * np.cumsum(vib) / SR
    y = np.sin(ph) + 0.3 * np.sin(2 * ph) + 0.12 * np.sin(3 * ph)
    y += 0.12 * bandpass(rng.standard_normal(n), f, min(f * 4, 18000))
    env = np.clip(np.minimum(t / 0.12, (dur + 0.2 - t) / 0.25), 0, 1)
    return y * env * vel * 0.18
def janggu(kind='deong', vel=0.6):
    n, t = T_(0.5)
    if kind == 'deong': y = np.sin(2 * np.pi * (90 + 40 * np.exp(-t * 30)) * t) * np.exp(-t * 9) + 0.3 * bandpass(rng.standard_normal(n), 2000, 6000) * np.exp(-t * 40)
    elif kind == 'kung': y = np.sin(2 * np.pi * (80 + 30 * np.exp(-t * 30)) * t) * np.exp(-t * 10)
    else: y = bandpass(rng.standard_normal(n), 1800, 7000) * np.exp(-t * 35)
    return y * vel * 0.5
def snare(vel=0.6, dur=0.18):
    n, t = T_(dur)
    return (bandpass(rng.standard_normal(n), 1500, 9000) * np.exp(-t * 22) + 0.4 * np.sin(2 * np.pi * 190 * t) * np.exp(-t * 30)) * vel * 0.5
def bass_drum(vel=0.7):
    n, t = T_(0.6)
    f = 55 + 60 * np.exp(-t * 25)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 6) * vel * 0.8
def timpani(f, vel=0.7):
    n, t = T_(1.6)
    y = np.sin(2 * np.pi * f * t) * np.exp(-t * 2.4) + 0.3 * np.sin(2 * np.pi * f * 1.5 * t) * np.exp(-t * 4)
    y += 0.2 * lowpass(rng.standard_normal(n), 400) * np.exp(-t * 20)
    return y * vel * 0.5
def tick(vel=0.3):
    n, t = T_(0.05)
    return bandpass(rng.standard_normal(n), 2500, 7000) * np.exp(-t * 120) * vel
def wind(seconds, vel=0.4):
    n = int(SR * seconds); x = rng.standard_normal(n)
    y = np.zeros(n); seg = 4096
    for i in range(0, n, seg):
        k = 0.5 + 0.5 * np.sin(2 * np.pi * i / n * 3)
        lo = 300 + 900 * k; y[i:i + seg] = bandpass(x[i:i + seg], lo, lo * 2.2)
    return y * (0.6 + 0.4 * np.sin(2 * np.pi * np.arange(n) / n * 4)) * vel * 0.25

class Track:
    def __init__(self, seconds):
        self.L = int(SR * seconds); self.seconds = self.L / SR
        self.buf = np.zeros(self.L + SR * 6); self.loopbuf = np.zeros(self.L)
    def add_loop(self, sig, gain=1.0): self.loopbuf += sig[:self.L] * gain
    def add(self, sig, at, gain=1.0):
        i = int(at * SR); j = min(len(self.buf), i + len(sig))
        if j > i: self.buf[i:j] += sig[:j - i] * gain
    def render(self, reverb=0.28, loop=True):
        ir_n = int(SR * 2.2); tt = np.arange(ir_n) / SR
        ir = lowpass(rng.standard_normal(ir_n) * np.exp(-tt * 2.6), 5000); ir /= np.sqrt(np.sum(ir ** 2))
        wet = fftconvolve(self.buf, ir)[:len(self.buf)]
        mix = self.buf + reverb * wet
        if loop:
            out = mix[:self.L].copy(); tail = mix[self.L:]; out[:len(tail)] += tail[:self.L]; out += self.loopbuf
        else:
            out = mix[:self.L] + self.loopbuf
        out = np.tanh(out * 1.4) / np.tanh(1.4)
        return out / (max(1e-9, np.max(np.abs(out))) / 0.89)

def play(T, inst, notes, start, beat, gain=1.0, oct=0, **kw):
    t = start
    for nn, ln in notes:
        if nn:
            for x in nn.split('+'): T.add(inst(midi(nm(x) + 12 * oct), ln * beat * 0.95, **kw), t, gain)
        t += ln * beat
    return t
def chord_line(T, inst, chords, start, bar, **kw):
    for i, c in enumerate(chords):
        for x in c.split('+'): T.add(inst(midi(nm(x)), bar * 0.98, **kw), start + i * bar)
def length(notes): return sum(l for _, l in notes)


def marimba(f, dur, vel=0.6):
    n, t = T_(dur + 0.5)
    y = np.sin(2 * np.pi * f * t) * np.exp(-t * 6) + 0.25 * np.sin(2 * np.pi * f * 3.9 * t) * np.exp(-t * 18)
    return y * np.minimum(1, t / 0.002) * vel * 0.32
def krar(f, dur, vel=0.6):
    n, t = T_(dur + 0.8)
    y = sum(a * np.sin(2 * np.pi * f * h * t + h * 0.3) * np.exp(-t * (3 + h * 1.6)) for h, a in [(1, 1), (2, .6), (3, .45), (4, .3), (5, .2)])
    return lowpass(y, 4200) * np.minimum(1, t / 0.003) * vel * 0.22
def brass(f, dur, vel=0.6):
    n, t = T_(dur + 0.15)
    ph = 2 * np.pi * f * t
    y = sum(a * np.sin(h * ph) for h, a in [(1, 1), (2, .8), (3, .6), (4, .45), (5, .3), (6, .2)])
    env = np.clip(np.minimum(t / 0.04, (dur + 0.15 - t) / 0.12), 0, 1)
    return lowpass(y, min(3000, f * 7)) * env * vel * 0.07
def kebero(vel=0.6, low=True):
    n, t = T_(0.4)
    f = 90 if low else 180
    y = np.sin(2 * np.pi * f * t * (1 - 0.3 * t)) * np.exp(-t * (10 if low else 20)) + 0.2 * bandpass(rng.standard_normal(n), 200, 2000) * np.exp(-t * 40)
    return y * vel * 0.5

# 이번 편을 위해 새로 지은 주제 선율 「전신선」 (4/4박, 4분음표 = 1). 첫머리 ♪♪♪♩ 는 모스 부호 'V'(···−)
WIRE = [('D5', .5), ('D5', .5), ('D5', .5), ('A5', 2.5), ('G5', 1), ('F#5', 1), ('E5', 1), ('D5', 1), ('E5', 1), ('F#5', 2),
        ('B4', .5), ('B4', .5), ('B4', .5), ('G5', 2.5), ('F#5', 1), ('E5', 1), ('D5', 1), ('C#5', 1), ('D5', 1), ('E5', 2),
        ('D5', .5), ('D5', .5), ('D5', .5), ('B5', 2.5), ('A5', 1), ('G5', 1), ('F#5', 1), ('E5', 1), ('F#5', 1), ('G5', 2),
        ('A5', 1.5), ('G5', .5), ('F#5', 1), ('E5', 1), ('D5', 1), ('C#5', 1), ('E5', 1), ('D5', 5)]
WIRE_CH = ['D3+A3', 'D3+A3', 'G2+D3', 'A2+E3', 'B2+F#3', 'G2+D3', 'E2+B2', 'A2+E3', 'D3+A3', 'G2+D3', 'G2+D3', 'D3+A3', 'A2+E3', 'A2+E3', 'D3+A3', 'D3+A3']

def morse_ticks(T, start, total, q, vel=0.14):
    pat = [0, .5, 1, 1.5, 2.5]     # ··· −  (V)
    t = start
    while t < total:
        for p in pat:
            if t + p * q < total: T.add(tick(vel), t + p * q)
        t += 4 * q

def title():
    e = 60 / 100; bar = 4 * e
    total = length(WIRE) * e + bar; T = Track(total + bar)
    play(T, strings, WIRE, bar, e, vel=0.72, att=0.15)
    play(T, piano, WIRE, bar, e, gain=0.5, vel=0.45, oct=-1)
    for i, c in enumerate(WIRE_CH):
        st = bar + i * bar
        if st < total:
            for x in c.split('+'): T.add(strings(midi(nm(x)), bar * 0.98, 0.38, att=0.6), st)
            T.add(timpani(midi(nm(c.split('+')[0]) - 12), 0.3), st)
    morse_ticks(T, 0, total, e)
    return T.render(0.42)

def office():
    bpm = 104; q = 60 / bpm; bar = 4 * q
    mel = [('F#5', 1), ('A5', .5), ('F#5', .5), ('E5', 1), ('D5', 1), ('E5', .5), ('F#5', .5), ('G5', 1), ('F#5', 2),
           ('E5', 1), ('G5', .5), ('E5', .5), ('D5', 1), ('C#5', 1), ('D5', .5), ('E5', .5), ('A4', 1), ('D5', 2),
           ('B4', 1), ('D5', .5), ('B4', .5), ('A4', 1), ('F#4', 1), ('G4', .5), ('A4', .5), ('B4', 1), ('C#5', 2),
           ('D5', 1), ('F#5', .5), ('E5', .5), ('D5', 1), ('C#5', 1), ('B4', 1), ('C#5', 1), ('D5', 2)]
    total = length(mel) * q * 2; T = Track(total)
    play(T, piano, mel, 0, q, vel=0.55); play(T, harpsi, mel, total / 2, q, vel=0.45); play(T, piano, mel, total / 2, q, gain=0.5, vel=0.4, oct=-1)
    roots = ['D3', 'A2', 'G2', 'D3', 'B2', 'F#2', 'G2', 'A2']
    for b in range(int(total / bar)):
        r = nm(roots[b % 8])
        for k in range(4): T.add(piano(midi(r + (12 if k % 2 else 0) + (7 if k == 3 else 0)), q * 0.9, 0.3), b * bar + k * q)
    morse_ticks(T, 0, total, q, 0.1)
    return T.render(0.4)

def tension():
    bpm = 96; q = 60 / bpm; bar = 4 * q
    secs = 16 * bar; T = Track(secs)
    for b in range(16):
        r = nm(['D2', 'D2', 'C2', 'A#1'][b % 4])
        for k in range(8): T.add(strings(midi(r), q * 0.4, 0.75, att=0.02), b * bar + k * q / 2)
        T.add(strings(midi(r + 15), bar, 0.32, att=1.0), b * bar)
        T.add(timpani(midi(r + 12), 0.4), b * bar)
        T.add(tick(0.15), b * bar + q); T.add(tick(0.15), b * bar + 3 * q)
    mel = [('A4', 3), ('A#4', 1), ('A4', 2), ('G4', 2), ('F4', 4), ('E4', 4), ('D4', 6), (None, 2)]
    play(T, flute, mel, 4 * bar, q, gain=0.6, vel=0.45)
    play(T, strings, mel, 12 * bar, q, gain=0.7, vel=0.5, oct=-1)
    return T.render(0.45)

def africa():
    """에티오피아 '티지타'풍 5음 음계(C D E G A)를 바탕으로 새로 지은 곡 - 크라르(뜯는 현) + 케베로(북)"""
    bpm = 108; q = 60 / bpm; bar = 4 * q
    SC = [nm(x) for x in ['C4', 'D4', 'E4', 'G4', 'A4', 'C5', 'D5', 'E5', 'G5', 'A5']]
    A = [(5, 1), (6, .5), (5, .5), (4, 1), (3, 1), (4, 1), (5, 1), (7, 2), (6, 1), (5, 1), (4, 1), (3, .5), (4, .5), (2, 2), (3, 2),
         (4, 1), (5, 1), (6, 1), (7, 1), (8, 2), (7, 1), (6, 1), (5, 1), (4, 1), (3, 1), (4, 1), (5, 4)]
    total = sum(l for _, l in A) * q * 2; T = Track(total); t = 0
    for rep in range(2):
        for deg, ln in A:
            T.add(krar(midi(SC[deg]), ln * q * 0.95, 0.65), t); t += ln * q
    play(T, flute, [(None, 0)] + [('C5', 2), ('A4', 2), ('G4', 2), ('E4', 2), ('D4', 4), ('E4', 4)] * 2, total / 2, q * 1.0, gain=0.4, vel=0.35)
    for b in range(int(total / bar)):
        s = b * bar
        T.add(kebero(0.6, True), s); T.add(kebero(0.35, False), s + q * 1.5); T.add(kebero(0.5, True), s + 2 * q); T.add(kebero(0.35, False), s + 3 * q); T.add(kebero(0.3, False), s + 3.5 * q)
        T.add(krar(midi(SC[[0, 1, 0, 3][b % 4]] - 12), bar * 0.9, 0.4), s)
    return T.render(0.32)

def dark():
    bpm = 60; q = 60 / bpm; bar = 4 * q
    secs = 12 * bar; T = Track(secs)
    ch = ['A2+E3+C4', 'F2+C3+A3', 'D3+A3+F4', 'E2+B2+G#3'] * 3
    chord_line(T, strings, ch, 0, bar, vel=0.42, att=1.2)
    mel = [('E5', 2), ('C5', 1), ('B4', 1), ('A4', 4), ('F4', 2), ('A4', 1), ('C5', 1), ('B4', 4), ('D5', 2), ('C5', 1), ('A4', 1), ('B4', 2), ('G#4', 2), ('A4', 8)]
    play(T, krar, mel, bar * 2, q, gain=0.7, vel=0.5)
    for b in range(12): T.add(kebero(0.35, True), b * bar); T.add(kebero(0.2, True), b * bar + 2.5 * q)
    T.add_loop(wind(secs, 0.25))
    return T.render(0.5)

def asia():
    e = 60 / 90; bar = 4 * e
    PEN = [nm(x) for x in ['D4', 'E4', 'G4', 'A4', 'B4', 'D5', 'E5', 'G5', 'A5']]
    A = [(5, 1), (6, 1), (5, .5), (4, .5), (3, 1), (4, 2), (2, 2), (3, 1), (4, 1), (5, 1), (4, .5), (3, .5), (2, 4),
         (6, 1), (7, 1), (8, 2), (7, 1), (6, .5), (5, .5), (4, 2), (5, 1), (4, 1), (3, 1), (2, 1), (1, 2), (2, 2), (3, 4)]
    total = sum(l for _, l in A) * e * 2; T = Track(total); t = 0
    for rep in range(2):
        for deg, ln in A:
            T.add(flute(midi(PEN[deg]), ln * e * 0.95, 0.5), t); T.add(krar(midi(PEN[deg]), ln * e * 0.8, 0.3), t, 0.6); t += ln * e
    for b in range(int(total / bar)):
        T.add(krar(midi(PEN[[0, 2, 3, 0][b % 4]] - 12), bar * 0.9, 0.4), b * bar)
        T.add(tick(0.1), b * bar + 2 * e)
    T.add_loop(wind(total, 0.12))
    return T.render(0.35)

def london():
    bpm = 112; q = 60 / bpm; bar = 2 * q
    A = [('D5', .5), ('D5', .5), ('G5', 1), ('B5', 1), ('A5', .5), ('G5', .5), ('E5', 1), ('G5', 1), ('D5', 2),
         ('C5', .5), ('C5', .5), ('E5', 1), ('G5', 1), ('F#5', .5), ('E5', .5), ('D5', 1), ('A4', 1), ('B4', 2),
         ('D5', .5), ('D5', .5), ('G5', 1), ('B5', 1), ('C6', .5), ('B5', .5), ('A5', 1), ('F#5', 1), ('G5', 2),
         ('E5', .5), ('F#5', .5), ('G5', 1), ('A5', 1), ('D5', .5), ('E5', .5), ('F#5', 1), ('A5', 1), ('G5', 2)]
    total = length(A) * q * 2; T = Track(total)
    play(T, brass, A, 0, q, vel=0.7); play(T, brass, A, total / 2, q, vel=0.65); play(T, flute, A, total / 2, q, gain=0.4, vel=0.4, oct=1)
    roots = ['G2', 'D2', 'C2', 'D2', 'G2', 'D2', 'C2', 'G2']
    for b in range(int(total / bar)):
        r = nm(roots[b % 8])
        T.add(brass(midi(r), q * 0.8, 0.5), b * bar); T.add(brass(midi(r + 7 + 12), q * 0.4, 0.3), b * bar + q)
        T.add(bass_drum(0.5), b * bar); T.add(snare(0.25), b * bar + q)
    return T.render(0.3)

def war():
    bpm = 54; q = 60 / bpm; bar = 4 * q
    secs = 12 * bar; T = Track(secs)
    ch = ['D2+A2+F3', 'A#1+F2+D3', 'G1+D2+A#2', 'A1+E2+C#3'] * 3
    chord_line(T, strings, ch, 0, bar, vel=0.45, att=1.5)
    mel = [('A4', 3), ('G4', 1), ('F4', 2), ('E4', 2), ('D4', 4), (None, 4), ('F4', 3), ('E4', 1), ('D4', 2), ('C#4', 2), ('D4', 8)]
    play(T, strings, mel, bar * 2, q, gain=0.8, vel=0.5, att=0.6)
    play(T, flute, mel, bar * 7, q, gain=0.4, vel=0.3, oct=1)
    for b in range(12): T.add(bass_drum(0.45), b * bar); T.add(bass_drum(0.2), b * bar + 3.5 * q)
    T.add_loop(wind(secs, 0.4))
    return T.render(0.5)

def paris():
    bpm = 150; q = 60 / bpm; bar = 3 * q
    mel = [('A5', 1), ('G#5', 1), ('A5', 1), ('E5', 3), ('F5', 1), ('E5', 1), ('D5', 1), ('C5', 3), ('D5', 1), ('C5', 1), ('B4', 1), ('A4', 2), ('C5', 1), ('E5', 6),
           ('A5', 1), ('G#5', 1), ('A5', 1), ('C6', 3), ('B5', 1), ('A5', 1), ('G5', 1), ('F5', 3), ('E5', 1), ('D5', 1), ('B4', 1), ('C5', 2), ('B4', 1), ('A4', 6)]
    total = length(mel) * q * 2; T = Track(total)
    play(T, accordion, mel, 0, q, vel=0.55); play(T, accordion, mel, total / 2, q, vel=0.5); play(T, strings, mel, total / 2, q, gain=0.5, vel=0.4, oct=-1)
    roots = ['A2', 'A2', 'D3', 'A2', 'E2', 'E2', 'A2', 'A2', 'A2', 'A2', 'F2', 'D3', 'E2', 'E2', 'A2', 'A2']
    for b in range(int(total / bar)):
        r = nm(roots[b % 16])
        T.add(piano(midi(r), q, 0.45), b * bar); T.add(piano(midi(r + 12 + 4), q * 0.6, 0.25), b * bar + q); T.add(piano(midi(r + 12 + 7), q * 0.6, 0.25), b * bar + 2 * q)
    return T.render(0.3)

def ending():
    e = 60 / 72; bar = 4 * e
    total = length(WIRE) * e + bar; T = Track(total + bar)
    play(T, flute, WIRE, bar, e, vel=0.55)
    play(T, strings, WIRE, bar, e, gain=0.7, vel=0.6, att=0.4, oct=-1)
    for i, c in enumerate(WIRE_CH):
        st = bar + i * bar
        if st < total:
            for x in c.split('+'): T.add(strings(midi(nm(x)), bar * 0.98, 0.35, att=1.0), st)
            for k in range(4): T.add(piano(midi(nm(c.split('+')[k % 2]) + 12 * (k // 2 % 2)), e, 0.3), st + k * e)
    morse_ticks(T, 0, bar * 2, e, 0.12)
    return T.render(0.5)

def save(path, mono, width=0.25):
    d = int(SR * 0.011)
    right = np.concatenate([mono[-d:], mono[:-d]])
    st = np.stack([mono * (1 - width * 0.3) + right * width * 0.3, right * (1 - width * 0.3) + mono * width * 0.3], 1)
    st = (np.clip(st, -1, 1) * 32767).astype(np.int16)
    with wave.open(path, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())

def encode(wav):
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', wav, '-c:a', 'libvorbis', '-q:a', '3', wav[:-4] + '.ogg'], check=True)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', wav, '-c:a', 'aac', '-b:a', '112k', wav[:-4] + '.m4a'], check=True)
    os.remove(wav)


def se_morse():
    n, t = T_(1.2)
    y = np.zeros(n)
    for (s0, d0) in ((0, .07), (.12, .07), (.24, .07), (.36, .22), (.7, .07), (.82, .22)):
        k0, k1 = int(s0 * SR), int((s0 + d0) * SR)
        y[k0:k1] += np.sin(2 * np.pi * 760 * t[:k1 - k0]) * np.clip(np.minimum(t[:k1 - k0] / .005, (d0 - t[:k1 - k0]) / .005), 0, 1)
        y[k0:k0 + 300] += bandpass(rng.standard_normal(300), 2000, 8000) * 0.4
    return y * 0.5
def se_boom():
    n, t = T_(2.2)
    y = lowpass(rng.standard_normal(n), 300) * np.exp(-t * 3) * 1.2 + np.sin(2 * np.pi * 45 * t) * np.exp(-t * 4) * 0.8
    y += bandpass(rng.standard_normal(n), 400, 3000) * np.exp(-t * 14) * 0.6
    return y / np.max(np.abs(y)) * 0.9
def se_shot():
    n, t = T_(0.7)
    y = bandpass(rng.standard_normal(n), 300, 6000) * np.exp(-t * 18) * 0.9
    y += np.sin(2 * np.pi * 70 * t) * np.exp(-t * 14) * 0.8
    y += lowpass(rng.standard_normal(n), 900) * np.exp(-t * 4) * 0.25
    return y / np.max(np.abs(y)) * 0.85
def se_paper():
    n, t = T_(0.5)
    y = bandpass(rng.standard_normal(n), 1500, 9000) * (np.abs(np.sin(2 * np.pi * 9 * t)) ** 2) * np.exp(-t * 5)
    return y / np.max(np.abs(y)) * 0.6


# ==================================================================== 금지된 주파수 (모두 새로 지은 곡)
# 주제 선율 「주파수」: 첫머리 ♪♪♪♩ 는 모스 부호 'V'(···−), BBC 가 전쟁 중 쓰던 승리의 신호와 같은 리듬
FREQ = [('G4', .5), ('G4', .5), ('G4', .5), ('D5', 2.5), ('C5', 1), ('A#4', 1), ('A4', 1), ('G4', 1), ('A4', 1), ('A#4', 2),
        ('F4', .5), ('F4', .5), ('F4', .5), ('C5', 2.5), ('A#4', 1), ('A4', 1), ('G4', 1), ('F4', 1), ('G4', 1), ('A4', 2),
        ('G4', .5), ('G4', .5), ('G4', .5), ('D5', 2.5), ('D#5', 1), ('D5', 1), ('C5', 1), ('A#4', 1), ('C5', 1), ('D5', 2),
        ('D5', 1.5), ('C5', .5), ('A#4', 1), ('A4', 1), ('G4', 1), ('F#4', 1), ('A4', 1), ('G4', 5)]
FREQ_CH = ['G2+D3', 'G2+D3', 'D#2+A#2', 'D2+A2', 'F2+C3', 'F2+C3', 'C2+G2', 'D2+A2', 'G2+D3', 'D#2+A#2', 'C2+G2', 'D2+A2', 'D2+A2', 'D2+F#2', 'G2+D3', 'G2+D3']
FREQ_MAJ = [(n.replace('A#', 'B').replace('D#5', 'E5').replace('F4', 'F#4') if n else n, l) for n, l in FREQ]

def g_title():
    e = 60 / 96; bar = 4 * e
    total = length(FREQ) * e + bar; T = Track(total + bar)
    play(T, strings, FREQ, bar, e, vel=0.7, att=0.15)
    play(T, piano, FREQ, bar, e, gain=0.5, vel=0.45, oct=-1)
    for i, c in enumerate(FREQ_CH):
        st = bar + i * bar
        if st < total:
            for x in c.split('+'): T.add(strings(midi(nm(x)), bar * 0.98, 0.38, att=0.6), st)
            T.add(timpani(midi(nm(c.split('+')[0]) - 12), 0.3), st)
    morse_ticks(T, 0, total, e)
    return T.render(0.42)

def r_studio():
    """1930년대 라디오 악단풍: 피아노 + 약음 금관 + 가벼운 리듬"""
    bpm = 116; q = 60 / bpm; bar = 4 * q
    mel = [('E5', .5), ('G5', .5), ('C6', 1), ('B5', .5), ('A5', .5), ('G5', 1), ('E5', .5), ('F5', .5), ('G5', 2),
           ('D5', .5), ('F5', .5), ('B5', 1), ('A5', .5), ('G5', .5), ('F5', 1), ('D5', .5), ('E5', .5), ('F5', 2),
           ('E5', .5), ('G5', .5), ('C6', 1), ('D6', .5), ('C6', .5), ('A5', 1), ('F5', .5), ('A5', .5), ('G5', 1), ('E5', 1),
           ('F5', 1), ('D5', 1), ('B4', 1), ('G4', 1), ('C5', 3), (None, 1)]
    total = length(mel) * q * 2; T = Track(total)
    play(T, piano, mel, 0, q, vel=0.55); play(T, brass, mel, total / 2, q, vel=0.5); play(T, piano, mel, total / 2, q, gain=0.5, vel=0.4, oct=-1)
    roots = ['C3', 'A2', 'D3', 'G2', 'C3', 'A2', 'F2', 'G2']
    for b in range(int(total / bar)):
        r = nm(roots[b % 8])
        for k in range(4):
            T.add(piano(midi(r + [0, 7, 12, 7][k]), q * 0.8, 0.3), b * bar + k * q)
        T.add(snare(0.08, 0.06), b * bar + q); T.add(snare(0.08, 0.06), b * bar + 3 * q)
    return T.render(0.38)

def r_berlin():
    """1920~30년대 베를린 카바레풍: 아코디언 + 피아노, 라단조"""
    bpm = 100; q = 60 / bpm; bar = 4 * q
    mel = [('E5', 1.5), ('D5', .5), ('C5', 1), ('B4', 1), ('A4', 1.5), ('C5', .5), ('E5', 2), ('F5', 1.5), ('E5', .5), ('D5', 1), ('C5', 1), ('B4', 4),
           ('D5', 1.5), ('C5', .5), ('B4', 1), ('A4', 1), ('G#4', 1.5), ('B4', .5), ('E5', 2), ('D5', 1), ('C5', 1), ('B4', 1), ('G#4', 1), ('A4', 4)]
    total = length(mel) * q * 2; T = Track(total)
    play(T, accordion, mel, 0, q, vel=0.55); play(T, accordion, mel, total / 2, q, vel=0.5); play(T, strings, mel, total / 2, q, gain=0.5, vel=0.35, oct=-1)
    roots = ['A2', 'A2', 'D3', 'E2', 'D3', 'E2', 'E2', 'A2']
    for b in range(int(total / bar)):
        r = nm(roots[b % 8])
        T.add(piano(midi(r), q, 0.45), b * bar); T.add(piano(midi(r + 12 + 3), q * 0.6, 0.25), b * bar + q)
        T.add(piano(midi(r + 7), q, 0.4), b * bar + 2 * q); T.add(piano(midi(r + 12 + 3), q * 0.6, 0.25), b * bar + 3 * q)
    return T.render(0.32)

def r_crash():
    """대공황: 느린 블루스풍 피아노 (다단조) + 걷는 베이스"""
    bpm = 72; q = 60 / bpm; bar = 4 * q
    mel = [('G4', 1), ('D#5', 1.5), ('D5', .5), ('C5', 1), ('D#5', 2), ('C5', 1), ('A#4', 1), ('G4', 3), (None, 1),
           ('F4', 1), ('G#4', 1.5), ('G4', .5), ('F4', 1), ('D#4', 2), ('F4', 1), ('G4', 1), ('C4', 4)]
    total = length(mel) * q * 2; T = Track(total)
    play(T, piano, mel, 0, q, vel=0.55); play(T, piano, mel, total / 2, q, vel=0.5); play(T, strings, mel, total / 2, q, gain=0.4, vel=0.3)
    walk = ['C3', 'D#3', 'F3', 'F#3', 'G3', 'F3', 'D#3', 'D3', 'F2', 'G#2', 'A#2', 'B2', 'C3', 'A#2', 'G2', 'G2']
    for b in range(int(total / q)):
        T.add(piano(midi(nm(walk[b % len(walk)])), q * 0.9, 0.35), b * q)
    for b in range(int(total / bar)): T.add(tick(0.06), b * bar + 2 * q)
    return T.render(0.4)

def r_sad():
    bpm = 56; q = 60 / bpm; bar = 4 * q
    secs = 12 * bar; T = Track(secs)
    ch = ['D3+A3+F4', 'A#2+F3+D4', 'G2+D3+A#3', 'A2+E3+C#4'] * 3
    chord_line(T, strings, ch, 0, bar, vel=0.42, att=1.3)
    mel = [('A4', 3), ('G4', 1), ('F4', 2), ('E4', 2), ('D4', 4), (None, 4), ('F4', 3), ('E4', 1), ('D4', 2), ('C#4', 2), ('D4', 8)]
    play(T, piano, mel, bar * 2, q, gain=0.8, vel=0.45)
    play(T, flute, mel, bar * 7, q, gain=0.35, vel=0.3, oct=1)
    return T.render(0.5)

def r_ending():
    e = 60 / 74; bar = 4 * e
    total = length(FREQ_MAJ) * e + bar; T = Track(total + bar)
    play(T, flute, FREQ_MAJ, bar, e, vel=0.55)
    play(T, strings, FREQ_MAJ, bar, e, gain=0.7, vel=0.6, att=0.4, oct=-1)
    chs = [c.replace('A#2', 'B2').replace('D#2', 'E2') for c in FREQ_CH]
    for i, c in enumerate(chs):
        st = bar + i * bar
        if st < total:
            for x in c.split('+'): T.add(strings(midi(nm(x)), bar * 0.98, 0.35, att=1.0), st)
            for k in range(4): T.add(piano(midi(nm(c.split('+')[k % 2]) + 12 * (k // 2 % 2)), e, 0.3), st + k * e)
    morse_ticks(T, 0, bar * 2, e, 0.12)
    return T.render(0.5)

def se_siren():
    n, t = T_(5.0)
    f = 420 + 260 * (0.5 - 0.5 * np.cos(2 * np.pi * t / 2.5))
    ph = 2 * np.pi * np.cumsum(f) / SR
    y = (np.sin(ph) + 0.3 * np.sin(2 * ph)) * np.clip(np.minimum(t / 0.3, (5.0 - t) / 0.8), 0, 1)
    return y * 0.35
def se_static():
    n, t = T_(0.8)
    y = bandpass(rng.standard_normal(n), 800, 7000) * (0.6 + 0.4 * np.sin(2 * np.pi * 7 * t)) * np.exp(-t * 2)
    return y / np.max(np.abs(y)) * 0.4
def se_v():
    n, t = T_(1.4)
    y = np.zeros(n)
    for (s0, d0) in ((0, .09), (.16, .09), (.32, .09), (.48, .36)):
        k0, k1 = int(s0 * SR), int((s0 + d0) * SR)
        tt = t[:k1 - k0]
        y[k0:k1] += np.sin(2 * np.pi * 700 * tt) * np.clip(np.minimum(tt / .006, (d0 - tt) / .006), 0, 1)
    return y * 0.5

# ---- The Cold War 주제 선율 「두 개의 말」 (라단조, 이 편을 위해 새로 지음)
COLD = [('D5', 1), ('F5', 1), ('A5', 2), ('G5', 1), ('F5', 1), ('E5', 1), ('D5', 1),
        ('C5', 1), ('D5', 1), ('E5', 1), ('F5', 1), ('E5', 2), ('A4', 2),
        ('D5', 1), ('F5', 1), ('A5', 1), ('C6', 1), ('A#5', 2), ('A5', 1), ('G5', 1),
        ('F5', 1), ('E5', 1), ('D5', 1), ('C#5', 1), ('D5', 4)]
COLD_CH = ['D2+A2', 'A#1+F2', 'C2+G2', 'A1+E2', 'D2+A2', 'G1+D2', 'A1+E2', 'D2+A2']
COLD_MAJ = [(n.replace('F5', 'F#5').replace('C5', 'C#5').replace('A#5', 'B5').replace('C6', 'C#6') if n else n, l) for n, l in COLD]
COLD_MAJ_CH = ['D2+A2', 'B1+F#2', 'G1+D2', 'A1+E2', 'D2+A2', 'G1+D2', 'A1+E2', 'D2+A2']

def cw_title():
    q = 60 / 80; bar = 4 * q
    total = length(COLD) * q * 2 + bar; T = Track(total + bar)
    play(T, strings, COLD, bar, q, vel=0.6, att=0.25)
    play(T, piano, COLD, bar + length(COLD) * q, q, vel=0.5)
    play(T, strings, COLD, bar + length(COLD) * q, q, gain=0.6, vel=0.45, oct=-1, att=0.3)
    for i in range(int((total - bar) / bar)):
        c = COLD_CH[i % len(COLD_CH)]
        for x in c.split('+'): T.add(strings(midi(nm(x) + 12), bar * 0.98, 0.32, att=0.7), bar + i * bar)
        T.add(timpani(midi(nm(c.split('+')[0])), 0.28), bar + i * bar)
    return T.render(0.42)

def cw_home():
    """안나의 집: 오르골 + 피아노 자장가 (라장조)"""
    q = 60 / 92; bar = 3 * q
    mel = [('A4', 1), ('D5', 1), ('F#5', 1), ('E5', 2), ('D5', 1), ('C#5', 1), ('E5', 1), ('A4', 1), ('B4', 3),
           ('B4', 1), ('E5', 1), ('G5', 1), ('F#5', 2), ('E5', 1), ('D5', 1), ('C#5', 1), ('E5', 1), ('D5', 3)]
    total = length(mel) * q * 2; T = Track(total)
    play(T, musicbox, mel, 0, q, vel=0.55); play(T, piano, mel, total / 2, q, vel=0.45); play(T, musicbox, mel, total / 2, q, gain=0.4, vel=0.35, oct=1)
    roots = ['D3', 'A2', 'G2', 'A2', 'E3', 'A2', 'A2', 'D3']
    for b in range(int(total / bar)):
        r = nm(roots[b % len(roots)])
        T.add(piano(midi(r), q * 0.9, 0.3), b * bar); T.add(piano(midi(r + 7), q * 0.8, 0.2), b * bar + q); T.add(piano(midi(r + 12), q * 0.8, 0.2), b * bar + 2 * q)
    return T.render(0.4)

def cw_airlift():
    """공수 작전: 밝은 금관 행진 (내림나장조 느낌의 사장조)"""
    q = 60 / 120; bar = 4 * q
    mel = [('G4', .5), ('B4', .5), ('D5', 1), ('D5', .5), ('E5', .5), ('D5', 1), ('B4', 1), ('C5', 1), ('A4', 2),
           ('A4', .5), ('C5', .5), ('E5', 1), ('E5', .5), ('F#5', .5), ('E5', 1), ('C5', 1), ('D5', 1), ('B4', 2),
           ('G4', .5), ('B4', .5), ('D5', 1), ('G5', 1.5), ('F#5', .5), ('E5', 1), ('C5', 1), ('D5', 1), ('F#4', 1), ('G4', 3), (None, 1)]
    total = length(mel) * q * 2; T = Track(total)
    play(T, brass, mel, 0, q, vel=0.55); play(T, brass, mel, total / 2, q, vel=0.55); play(T, flute, mel, total / 2, q, gain=0.4, vel=0.35, oct=1)
    roots = ['G2', 'D2', 'A2', 'D2', 'G2', 'C2', 'D2', 'G2']
    for b in range(int(total / bar)):
        r = nm(roots[b % 8])
        for k in range(4): T.add(brass(midi(r + (0 if k % 2 == 0 else 7)), q * 0.6, 0.25), b * bar + k * q)
        T.add(bass_drum(0.3), b * bar); T.add(snare(0.12, 0.1), b * bar + q); T.add(snare(0.12, 0.1), b * bar + 3 * q)
    return T.render(0.36)

def cw_thaw():
    """데탕트 · 몰타: 따뜻한 현악 + 플루트, 주제 선율의 장조 (느리게)"""
    q = 60 / 70; bar = 4 * q
    total = length(COLD_MAJ) * q + bar; T = Track(total + bar)
    play(T, flute, COLD_MAJ, bar, q, vel=0.45)
    play(T, strings, COLD_MAJ, bar, q, gain=0.5, vel=0.4, oct=-1, att=0.5)
    for i in range(int((total - bar) / bar) + 1):
        c = COLD_MAJ_CH[i % len(COLD_MAJ_CH)]
        for x in c.split('+'): T.add(strings(midi(nm(x) + 12), bar * 0.98, 0.3, att=1.0), bar * 0 + i * bar)
    return T.render(0.45)

def cw_joy():
    """1989년 11월 9일 밤: 아코디언 + 금관, 빠른 장조 춤곡"""
    q = 60 / 132; bar = 4 * q
    mel = [('D5', .5), ('F#5', .5), ('A5', 1), ('A5', .5), ('B5', .5), ('A5', .5), ('F#5', .5), ('G5', 1), ('E5', 1), ('C#5', 1), ('E5', 1),
           ('D5', .5), ('F#5', .5), ('A5', 1), ('D6', 1), ('C#6', .5), ('B5', .5), ('A5', 1), ('G5', .5), ('E5', .5), ('D5', 2)]
    total = length(mel) * q * 3; T = Track(total)
    for k in range(3):
        play(T, accordion if k != 1 else brass, mel, k * total / 3, q, vel=0.55)
        if k == 2: play(T, flute, mel, k * total / 3, q, gain=0.4, vel=0.35, oct=1)
    roots = ['D3', 'A2', 'G2', 'A2', 'D3', 'G2', 'A2', 'D3']
    for b in range(int(total / bar)):
        r = nm(roots[b % 8])
        for k in range(4): T.add(piano(midi(r + (0 if k % 2 == 0 else 12 + 4)), q * 0.6, 0.3), b * bar + k * q)
        T.add(bass_drum(0.3), b * bar); T.add(bass_drum(0.25), b * bar + 2 * q); T.add(snare(0.1, 0.08), b * bar + q); T.add(snare(0.1, 0.08), b * bar + 3 * q)
    return T.render(0.34)

def cw_ending():
    q = 60 / 74; bar = 4 * q
    total = length(COLD_MAJ) * q * 2 + bar; T = Track(total + bar)
    play(T, piano, COLD_MAJ, bar, q, vel=0.5)
    play(T, flute, COLD_MAJ, bar + length(COLD_MAJ) * q, q, vel=0.5)
    play(T, strings, COLD_MAJ, bar + length(COLD_MAJ) * q, q, gain=0.6, vel=0.5, oct=-1, att=0.4)
    for i in range(int((total - bar) / bar)):
        c = COLD_MAJ_CH[i % len(COLD_MAJ_CH)]
        for x in c.split('+'): T.add(strings(midi(nm(x) + 12), bar * 0.98, 0.32, att=1.0), bar + i * bar)
        for k in range(4): T.add(piano(midi(nm(c.split('+')[k % 2]) + 12 * (1 + k // 2 % 2)), q, 0.22), bar + i * bar + k * q)
    return T.render(0.5)

# ---- 알렉산드리아의 두루마리 주제 선율 「두루마리」 (도리아 선법 느낌의 라음계, 이 편을 위해 새로 지음)
SCR = [('D5', 1), ('E5', .5), ('F5', .5), ('G5', 1), ('A5', 1), ('B5', .5), ('A5', .5), ('G5', 1), ('F5', 1), ('E5', 1),
       ('D5', 1), ('C5', .5), ('D5', .5), ('E5', 1), ('A4', 1), ('D5', 3), (None, 1),
       ('A5', 1), ('B5', .5), ('C6', .5), ('B5', 1), ('A5', 1), ('G5', 1), ('F5', .5), ('E5', .5), ('F5', 1), ('G5', 1),
       ('A5', 1), ('G5', .5), ('F5', .5), ('E5', 1), ('C5', 1), ('D5', 4)]
SCR_CH = ['D2+A2', 'D2+A2', 'G1+D2', 'A1+E2', 'C2+G2', 'D2+A2', 'A1+E2', 'D2+A2']
SCR_MAJ = [(n.replace('F5', 'F#5').replace('C5', 'C#5').replace('C6', 'C#6') if n else n, l) for n, l in SCR]
SCR_MAJ_CH = ['D2+A2', 'D2+A2', 'G1+D2', 'A1+E2', 'G1+D2', 'D2+A2', 'A1+E2', 'D2+A2']

def drone(T, root, total, vel=0.22):
    bar = 6.0
    for k in range(int(total / bar) + 1):
        for x in (root, root + 7): T.add(strings(midi(x), bar * 0.99, vel, att=1.2), k * bar)

# ==================================================================== 척화비 아래에서 (계면조 · 평조, 가야금 · 대금 · 장구)
THEME = [('A4', 1.5), ('C5', .5), ('D5', 1), ('E5', 1), ('D5', .5), ('C5', .5), ('A4', 1), ('G4', 1), ('A4', 2),
         ('E5', 1.5), ('G5', .5), ('A5', 1), ('G5', .5), ('E5', .5), ('D5', 1), ('C5', 1), ('D5', 1), ('E5', 2),
         ('A5', 1), ('G5', .5), ('E5', .5), ('D5', 1), ('C5', 1), ('A4', 1), ('C5', .5), ('D5', .5), ('E5', 2),
         ('D5', 1), ('C5', .5), ('A4', .5), ('G4', 1), ('E4', 1), ('A4', 3), (None, 1)]
THEME_MAJ = [(None if n is None else n.replace('A4', 'G4#').replace('A5', 'G5#'), l) for n, l in THEME]
THEME_MAJ = [('G4', 1.5), ('A4', .5), ('C5', 1), ('D5', 1), ('C5', .5), ('A4', .5), ('G4', 1), ('E4', 1), ('G4', 2),
             ('D5', 1.5), ('E5', .5), ('G5', 1), ('E5', .5), ('D5', .5), ('C5', 1), ('A4', 1), ('C5', 1), ('D5', 2),
             ('G5', 1), ('E5', .5), ('D5', .5), ('C5', 1), ('A4', 1), ('G4', 1), ('A4', .5), ('C5', .5), ('D5', 2),
             ('C5', 1), ('A4', .5), ('G4', .5), ('E4', 1), ('D4', 1), ('G4', 3), (None, 1)]

def jangdan(T, start, total, bar, hits, vel=1.0):
    """한 마디(bar 초) 안의 비율 위치 hits = [(0~1, 종류, 세기)]"""
    k = 0
    while start + k * bar < total:
        for pos, kind, v in hits: T.add(janggu(kind, v * vel), start + k * bar + pos * bar)
        k += 1

GUTGEORI = [(0, 'deong', 0.55), (3 / 12, 'deok', 0.3), (5 / 12, 'deok', 0.25), (6 / 12, 'kung', 0.4), (9 / 12, 'deok', 0.3), (11 / 12, 'deok', 0.22)]
JUNGJUNG = [(0, 'deong', 0.55), (3 / 12, 'deok', 0.25), (6 / 12, 'kung', 0.45), (8 / 12, 'deok', 0.25), (9 / 12, 'kung', 0.35)]
JAJIN = [(0, 'deong', 0.55), (3 / 12, 'deok', 0.3), (6 / 12, 'kung', 0.45), (9 / 12, 'deok', 0.3), (10 / 12, 'deok', 0.2)]

def arp(T, inst, notes, start, total, step, vel=0.4, gain=1.0):
    k = 0
    while start + k * step < total:
        n = notes[k % len(notes)]
        if n: T.add(inst(midi(nm(n)), step * 1.6, vel), start + k * step, gain)
        k += 1

def kr_title():
    q = 60 / 72; total = length(THEME) * q * 2 + 4 * q; T = Track(total)
    arp(T, gayageum, ['A3', 'E4', 'A4', 'C5', 'G3', 'D4', 'G4', 'A4'], 0, total, q / 2, 0.32)
    play(T, daegeum, THEME, 4 * q, q, vel=0.55)
    play(T, gayageum, THEME, 4 * q + length(THEME) * q, q, vel=0.55)
    play(T, strings, THEME, 4 * q + length(THEME) * q, q, gain=0.45, vel=0.4, oct=-1, att=0.4)
    jangdan(T, 4 * q, total, 4 * q * 1.0, JUNGJUNG, 0.9)
    drone(T, nm('A2'), total, 0.14)
    return T.render(0.42)

def kr_home():
    """사랑방 · 밤: 느린 가야금 산조풍 (평조) + 낮은 지속음"""
    q = 60 / 60
    mel = [('G4', 2), ('A4', 1), ('C5', 1), ('D5', 3), ('C5', 1), ('A4', 2), ('G4', 2), ('E4', 3), (None, 1),
           ('D4', 1), ('E4', 1), ('G4', 2), ('A4', 1), ('C5', 1), ('A4', 2), ('G4', 4), (None, 2)]
    total = length(mel) * q * 2; T = Track(total)
    play(T, gayageum, mel, 0, q, vel=0.45)
    play(T, daegeum, mel, length(mel) * q, q, vel=0.32, gain=0.8)
    arp(T, gayageum, ['G2', 'D3', 'G3', None], 0, total, q, 0.25, 0.7)
    return T.render(0.5)

def kr_joseon():
    """궁궐 · 훈련장: 굿거리 장단의 밝은 평조 가락"""
    q = 60 / 96; bar = 12 * q / 3
    mel = [('G4', 1.5), ('A4', .5), ('C5', 1), ('D5', 1.5), ('E5', .5), ('D5', 1), ('C5', 1), ('A4', 1), ('C5', 2), ('A4', 1), ('G4', 3),
           ('D5', 1.5), ('E5', .5), ('G5', 1), ('E5', 1), ('D5', 1), ('C5', 1), ('D5', 1.5), ('C5', .5), ('A4', 1), ('G4', 3)]
    total = length(mel) * q * 3; T = Track(total)
    for k in range(3): play(T, [daegeum, gayageum, daegeum][k], mel, k * total / 3, q, vel=0.5)
    arp(T, gayageum, ['G3', 'D4', 'G4', 'D4'], 0, total, q, 0.28, 0.8)
    jangdan(T, 0, total, bar, GUTGEORI, 1.0)
    return T.render(0.38)

def kr_market():
    """장터: 빠른 자진모리풍 + 가야금 · 대금"""
    q = 60 / 132; bar = 4 * q
    mel = [('A4', .5), ('C5', .5), ('D5', 1), ('E5', .5), ('G5', .5), ('E5', 1), ('D5', .5), ('C5', .5), ('A4', 1), ('C5', 1),
           ('D5', .5), ('E5', .5), ('G5', 1), ('A5', 1), ('G5', .5), ('E5', .5), ('D5', 1), ('E5', 2),
           ('A5', .5), ('G5', .5), ('E5', 1), ('D5', .5), ('C5', .5), ('A4', 1), ('C5', .5), ('D5', .5), ('E5', 1), ('D5', 1), ('A4', 2)]
    total = length(mel) * q * 4; T = Track(total)
    for k in range(4): play(T, [gayageum, daegeum, gayageum, daegeum][k], mel, k * total / 4, q, vel=0.5)
    arp(T, gayageum, ['A2', 'E3', 'A3', 'E3', 'G2', 'D3', 'G3', 'D3'], 0, total, q, 0.25, 0.8)
    jangdan(T, 0, total, bar, JAJIN, 1.0)
    return T.render(0.36)

def kr_night():
    """강화도 밤 잠행: 낮은 현의 긴 음 + 가끔 뜯는 가야금 + 바람"""
    q = 60 / 66; total = 48 * q; T = Track(total)
    for k, n in enumerate(['A2', 'A2', 'G2', 'E2', 'A2', 'F2', 'E2', 'E2']):
        T.add(strings(midi(nm(n)), 6 * q * 0.98, 0.45, att=1.5), k * 6 * q)
        T.add(strings(midi(nm(n) + 7), 6 * q * 0.98, 0.25, att=2.0), k * 6 * q)
    for k in range(int(total / (3 * q))):
        T.add(gayageum(midi(nm(['E4', 'D4', 'C4', 'A3', 'E4', 'G4'][k % 6])), q, 0.25), k * 3 * q + 1.5 * q)
        T.add(janggu('deok', 0.12), k * 3 * q)
    T.add(wind(total, 0.25), 0)
    return T.render(0.42)

def kr_war():
    """광성보 전투 앞: 힘찬 장구 · 낮은 현 · 대금의 외침"""
    q = 60 / 100; bar = 4 * q
    mel = [('E5', 2), ('D5', 1), ('C5', 1), ('A4', 2), ('C5', 1), ('D5', 1), ('E5', 3), (None, 1), ('G5', 2), ('E5', 1), ('D5', 1), ('C5', 1), ('A4', 1), ('G4', 1), ('A4', 4)]
    total = length(mel) * q * 3; T = Track(total)
    for k in range(3): play(T, daegeum if k != 1 else strings, mel, k * total / 3, q, vel=0.55, **({} if k != 1 else {'att': 0.15}))
    for b in range(int(total / bar)):
        T.add(timpani(midi(nm('A1')), 0.35), b * bar); T.add(timpani(midi(nm('E2')), 0.25), b * bar + 2 * q)
    jangdan(T, 0, total, bar, JAJIN, 1.1)
    drone(T, nm('A1'), total, 0.16)
    return T.render(0.4)

def kr_tension():
    """연무당 협상: 긴장된 낮은 현 + 시계 같은 장구 소리"""
    q = 60 / 80; total = 48 * q; T = Track(total)
    for k, c in enumerate(['A2+E3', 'A2+F3', 'G2+D3', 'E2+B2'] * 3):
        for x in c.split('+'): T.add(strings(midi(nm(x)), 4 * q * 0.98, 0.42, att=0.8), k * 4 * q)
    for k in range(int(total / q)): T.add(janggu('deok', 0.12 if k % 4 else 0.22), k * q)
    for k in range(int(total / (8 * q))):
        play(T, gayageum, [('E5', 1), ('D5', 1), ('C5', 2), ('A4', 4)], k * 8 * q + 4 * q, q * 0.5, vel=0.3)
    return T.render(0.42)

def kr_crisis():
    """임오군란: 빠르고 불안한 현 반복 + 큰 북"""
    q = 60 / 140; bar = 4 * q; total = 32 * bar; T = Track(total)
    ost = ['A3', 'C4', 'E4', 'C4', 'A3', 'D4', 'F4', 'D4']
    for k in range(int(total / (q / 2))): T.add(strings(midi(nm(ost[k % 8])), q * 0.45, 0.34, att=0.02), k * q / 2)
    for b in range(int(total / bar)):
        T.add(timpani(midi(nm('A1')), 0.4), b * bar); T.add(janggu('kung', 0.4), b * bar + 2 * q); T.add(janggu('deok', 0.3), b * bar + 3 * q); T.add(janggu('deok', 0.3), b * bar + 3.5 * q)
    play(T, daegeum, [('E5', 4), ('F5', 2), ('E5', 2), ('D5', 4), ('C5', 4), ('A4', 8)] * 2, 8 * bar, q, vel=0.45)
    return T.render(0.4)

def kr_sea():
    """제물포: 가야금과 피아노가 함께 (새 시대)"""
    q = 60 / 84; total = length(THEME_MAJ) * q * 2; T = Track(total)
    play(T, gayageum, THEME_MAJ, 0, q, vel=0.45)
    play(T, piano, THEME_MAJ, length(THEME_MAJ) * q, q, vel=0.45)
    arp(T, piano, ['G2', 'D3', 'G3', 'B3', 'C3', 'G3', 'C4', 'E4'], 0, total, q / 2, 0.22, 0.8)
    return T.render(0.45)

def kr_ending():
    q = 60 / 70; total = length(THEME_MAJ) * q * 2 + 4 * q; T = Track(total)
    arp(T, gayageum, ['G3', 'D4', 'G4', 'A4', 'C4', 'G4', 'C5', 'D5'], 0, total, q / 2, 0.28)
    play(T, daegeum, THEME_MAJ, 4 * q, q, vel=0.5)
    play(T, piano, THEME_MAJ, 4 * q + length(THEME_MAJ) * q, q, vel=0.45)
    play(T, strings, THEME_MAJ, 4 * q + length(THEME_MAJ) * q, q, gain=0.5, vel=0.4, oct=-1, att=0.5)
    jangdan(T, 4 * q, total, 4 * q, JUNGJUNG, 0.6)
    return T.render(0.45)

TRACKS = [('Title', kr_title), ('Home', kr_home), ('Joseon', kr_joseon), ('Market', kr_market), ('Night', kr_night), ('War', kr_war),
          ('Tension', kr_tension), ('Crisis', kr_crisis), ('Sea', kr_sea), ('Ending', kr_ending)]

def build(root, only=None):
    bd = os.path.join(root, 'audio', 'bgm'); sd = os.path.join(root, 'audio', 'se')
    os.makedirs(bd, exist_ok=True); os.makedirs(sd, exist_ok=True)
    for name, fn in TRACKS:
        if only and name not in only: continue
        p = os.path.join(bd, 'Kr_' + name + '.wav'); save(p, fn()); encode(p); print('bgm', name)
    for name, fn in (('Paper', se_paper),):
        p = os.path.join(sd, 'Kr_' + name + '.wav'); save(p, fn(), 0); encode(p)
    print('se ok')

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2:] or None)
