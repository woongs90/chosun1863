"""종로 사진관 2 데이터 도우미 (대사·연출·촬영·퀘스트 표시)"""
import json, os
HERE = os.path.dirname(os.path.abspath(__file__))
def LAY(): return json.load(open(os.path.join(HERE, 'layout.json'), encoding='utf-8'))

def T(text, speaker=None, face=None, **kw):
    d = {"text": text}
    if speaker: d["speaker"] = speaker
    if face: d["face"] = face
    d.update(kw); return d
def ME(text, face=None, **kw): return T(text, "{name}", face, **kw)
def HK(text, face=None, **kw): return T(text, "삼촌", face, **kw)
def MOM(text, face=None, **kw): return T(text, "엄마", face, **kw)
def SJ(text, face=None, **kw): return T(text, "서준", face, **kw)
def MK(text, face=None, **kw): return T(text, "미경", face, **kw)
def ED(text, face=None, **kw): return T(text, "편집장", face, **kw)
def TAEIL(text, face=None, **kw): return T(text, "전태일", face, **kw)
def N(text, **kw): return T(text, None, None, **kw)
def NOTE(text, **kw): return T(text, "정리", None, **kw)

def CAP(text, **kw):
    d = {"caption": text}; d.update(kw); return d
def CINE(on=True, caption=None):
    d = {"cinema": on}
    if caption: d["caption"] = caption
    return d
def ZOOM(event=None, x=None, y=None, scale=1.6, duration=50, **kw):
    z = {"scale": scale, "duration": duration}
    if event: z["event"] = event
    if x is not None: z["x"] = x; z["y"] = y
    z.update(kw)
    return {"zoom": z}
UNZOOM = {"zoom": False}
def MOVE(event, to=None, route=None, speed=3, wait=True, **kw):
    m = {"event": event, "speed": speed, "wait": wait}
    if to: m["to"] = list(to)
    if route: m["route"] = [list(p) for p in route]
    m.update(kw)
    return {"move": m}
def MOVES(*defs):
    return {"move": [d["move"] for d in defs]}
def PLACE(event, x=None, y=None, dir=None, **kw):
    p = {"event": event}
    if x is not None: p["x"] = x; p["y"] = y
    if dir: p["dir"] = dir
    p.update(kw)
    return {"place": p}
def TURN(event, dir=None, toward=None):
    t = {"event": event}
    if dir: t["dir"] = dir
    if toward: t["toward"] = toward
    return {"turn": t}
def GO(room, x=None, y=None, dir=None, fade=None):
    s = {"go": room}
    if x is not None: s.update(x=x, y=y)
    if dir: s["dir"] = dir
    if fade: s["fade"] = fade
    return s
def WAIT(n): return {"wait": n}
def GOAL(text, *targets):
    """목표 + 퀘스트 표시(!)를 띄울 조사 지점들"""
    g = {"goal": text}
    if targets: g["targets"] = list(targets)
    return g
def PIC(name, text=None, speaker=None, **kw):
    s = {"picture": name}
    if text is not None: s["text"] = text
    if speaker: s["speaker"] = speaker
    s.update(kw); return s
def AGE(age, img):
    return {"setVar": {"age": str(age)}, "heroImage": img}

SEPIA = [40, 14, -34, 255]
NIGHT = [-68, -60, -10, 60]
DAWN = [-40, -36, -6, 40]

def CH(n):
    """n장 진행 중 (n장 시작 깃발은 있고 다음 장은 아직)"""
    return {"flag": "c%d" % n, "noFlag": "c%d" % (n + 1)}

def chapter_title(n, text):
    return {"effect": "card", "text": text}

def focus(n, picture, label, extra=None, success=None, film=4, **opts):
    """초점 촬영 → 성공하면 사진(인화 카드) 얻기"""
    f = {"picture": picture, "label": label, "film": film}
    f.update(opts)
    f["success"] = [{"flag": "shot%d" % n, "give": "photo%d" % n, "effect": "flash", "color": [255, 255, 255, 200], "duration": 20}] + (success or [])
    f["fail"] = [N("필름을 다 썼다. 가방에서 새 필름을 꺼내 끼웠다. 흐렸다가 또렷해지는 순간을 잘 보자!")]
    s = {"focus": f}
    if extra: s.update(extra)
    return s

def develop(n, caption, after):
    """암실에서 현상 → 사진첩에 붙이기"""
    return [
        {"tint": [-90, -120, -120, 40], "duration": 20, "se": "Water1"},
        N("암실의 붉은 불빛 아래, 필름을 약품에 담갔다. 하얀 종이 위로 사진이 천천히 떠올랐다."),
        PIC("cu_photo%d" % n, caption),
        {"tint": [0, 0, 0, 0], "duration": 20, "flag": "dev%d" % n},
        album_step("사진첩에 새 사진을 붙였다. (가방이나 진열 사진 벽에서 다시 볼 수 있어요)"),
    ] + after

def album_step(text):
    return {"picture": "cu_album", "overlays": [{"picture": "cu_album_ov%d" % k, "if": {"flag": "dev%d" % k}} for k in range(8)], "text": text}

def WALK(events, route, loop=False, speed=3, rel=True, always=True, **kw):
    w = {"events": events if isinstance(events, list) else [events], "route": [list(p) for p in route], "loop": loop, "speed": speed, "rel": rel, "always": always}
    w.update(kw); return {"walkers": [w]}
def WANDER(events, r=1, **kw):
    w = {"events": events if isinstance(events, list) else [events], "wander": r, "always": True, "pause": 80}
    w.update(kw); return {"walkers": [w]}
