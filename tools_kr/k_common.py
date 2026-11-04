"""종로 사진관 편 공통: 글꼴, 지도 파일 쓰기, 배치 기록 (다른 편 도구 없이 혼자 동작)"""
import os, sys, json
from PIL import ImageFont
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), 'tools'))

TS = 48
FONT_SANS = '/usr/share/fonts/opentype/noto/NotoSansCJK-Bold.ttc'
FONT_SANS_R = '/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc'
FONT_SERIF = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
_fc = {}
def F(size, kind='sans'):
    """kind: sans(굵게) / reg(보통) / serif(명조)"""
    key = (int(size), kind)
    if key not in _fc:
        path = {'sans': FONT_SANS, 'reg': FONT_SANS_R, 'serif': FONT_SERIF}[kind]
        _fc[key] = ImageFont.truetype(path, int(size), index=1)   # index 1 = KR
    return _fc[key]

DIRS = {'down': 2, 'left': 4, 'right': 6, 'up': 8, 2: 2, 4: 4, 6: 6, 8: 8}

def make_event(eid, e):
    sprite = e.get('sprite') or ''
    obj = sprite.startswith('!')
    page = {
        "conditions": {"actorId": 1, "actorValid": False, "itemId": 1, "itemValid": False, "selfSwitchCh": "A",
                       "selfSwitchValid": False, "switch1Id": 1, "switch1Valid": False, "switch2Id": 1,
                       "switch2Valid": False, "variableId": 1, "variableValid": False, "variableValue": 0},
        "directionFix": e.get('fix', obj and not e.get('turn')),
        "image": {"characterIndex": e.get('index', 0), "characterName": sprite, "direction": DIRS[e.get('dir', 'down')],
                  "pattern": e.get('pattern', 1), "tileId": 0},
        "list": [{"code": 0, "indent": 0, "parameters": []}],
        "moveFrequency": 3,
        "moveRoute": {"list": [{"code": 0, "parameters": []}], "repeat": True, "skippable": False, "wait": False},
        "moveSpeed": e.get('speed', 3), "moveType": 0, "priorityType": e.get('priority', 1), "stepAnime": e.get('anime', False),
        "through": e.get('through', False), "trigger": e.get('trigger', 0), "walkAnime": not obj}
    return {"id": eid, "name": e['name'], "note": "", "pages": [page], "x": e['x'], "y": e['y']}

def snd(): return {"name": "", "pan": 0, "pitch": 100, "volume": 90}

def write_map(root, map_id, w, h, region, events, parallax, note=''):
    data = [0] * (w * h * 6)
    for y in range(h):
        for x in range(w):
            data[(5 * h + y) * w + x] = region[y][x]
    evs = [None]
    for e in events: evs.append(make_event(len(evs), e))
    mp = {"autoplayBgm": False, "autoplayBgs": False, "battleback1Name": "", "battleback2Name": "", "bgm": snd(), "bgs": snd(),
          "disableDashing": True, "displayName": "", "encounterList": [], "encounterStep": 30, "height": h, "note": note,
          "parallaxLoopX": False, "parallaxLoopY": False, "parallaxName": parallax, "parallaxShow": True,
          "parallaxSx": 0, "parallaxSy": 0, "scrollType": 0, "specifyBattleback": False, "tilesetId": 1, "width": w,
          "data": data, "events": evs}
    os.makedirs(os.path.join(root, 'data'), exist_ok=True)
    json.dump(mp, open(os.path.join(root, 'data', 'Map%03d.json' % map_id), 'w', encoding='utf-8'), ensure_ascii=False)

def write_mapinfos(root, names):
    infos = [None]
    for i, n in enumerate(names, 1):
        infos.append({"id": i, "expanded": False, "name": n, "order": i, "parentId": 0, "scrollX": 0, "scrollY": 0})
    json.dump(infos, open(os.path.join(root, 'data', 'MapInfos.json'), 'w', encoding='utf-8'), ensure_ascii=False)

def blank(w, h, ch='.'): return [[ch] * w for _ in range(h)]
def fill(g, x0, y0, x1, y1, ch):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1): g[y][x] = ch

def save_layout(key, info):
    p = os.path.join(HERE, 'layout.json')
    d = json.load(open(p, encoding='utf-8')) if os.path.exists(p) else {}
    d[key] = info; json.dump(d, open(p, 'w', encoding='utf-8'), ensure_ascii=False, indent=1)

def out(root, name, big):
    os.makedirs(os.path.join(root, 'img/parallaxes'), exist_ok=True)
    big.save(os.path.join(root, 'img/parallaxes', name + '.png'), optimize=True)
