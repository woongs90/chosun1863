"""넓은 화면용 MV 맵 파일: 가로 29칸(가운데 17칸이 실제 방, 양옆 6칸은 장식 마당 = 못 지나감)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import make_world as MW
from hd_wide import MARGIN

CW, H = MW.W, MW.H          # 17 x 13 (실제 방)
WW = CW + 2 * MARGIN        # 29

def build(out):
    os.makedirs(os.path.join(out, 'data'), exist_ok=True)
    infos = [None]
    for room in MW.ROOMS:
        doors = room['doors']
        region = [[1] * WW for _ in range(H)]
        for y in range(2, 12):
            for x in range(1, 16):
                region[y][x + MARGIN] = 0
        for o in room['objs']:
            for ty in range(o['y'], o['y'] + o['h']):
                for tx in range(o['x'], o['x'] + o['w']):
                    region[ty][tx + MARGIN] = 1
        data = [0] * (WW * H * 6)
        for y in range(H):
            for x in range(WW):
                data[(5 * H + y) * WW + x] = region[y][x]
        events = [None]
        def add(name, x, y, trig=0, sprite=None, d=2):
            events.append(MW.make_event(len(events), name, x + MARGIN, y, trig, sprite, d))
        for o in room['objs']:
            if not o['id'] or o['events'] == 'none': continue
            tiles = [(tx, ty) for ty in range(o['y'], o['y'] + o['h']) for tx in range(o['x'], o['x'] + o['w'])] if o['events'] == 'all' else o['events']
            for tx, ty in tiles: add(o['id'], tx, ty, o['trigger'])
        for nid, sprite, x, y, d in room['npcs']:
            add(nid, x, y, 0, '$' + sprite, MW.DIRS[d])
        if 'left' in doors: add('back', 0, 9, 1)
        if 'right' in doors or 'right_gate' in doors: add('exit', 16, 9, 1)
        mp = {"autoplayBgm": False, "autoplayBgs": False, "battleback1Name": "", "battleback2Name": "", "bgm": MW.snd(), "bgs": MW.snd(),
              "disableDashing": False, "displayName": "", "encounterList": [], "encounterStep": 30, "height": H,
              "note": "<escCenter>", "parallaxLoopX": False, "parallaxLoopY": False, "parallaxName": room['parallax'], "parallaxShow": True,
              "parallaxSx": 0, "parallaxSy": 0, "scrollType": 0, "specifyBattleback": False, "tilesetId": 3, "width": WW,
              "data": data, "events": events}
        json.dump(mp, open(os.path.join(out, 'data', 'Map%03d.json' % room['map']), 'w', encoding='utf-8'), ensure_ascii=False)
        infos.append({"id": room['map'], "expanded": False, "name": room['name'], "order": room['map'], "parentId": 0, "scrollX": 696, "scrollY": 312})
    if '--mapinfos' in sys.argv:   # 기존 프로젝트의 맵 목록을 덮어쓰지 않도록 기본은 만들지 않음
        json.dump(infos, open(os.path.join(out, 'data', 'MapInfos.json'), 'w', encoding='utf-8'), ensure_ascii=False)
    print('wide maps', len(MW.ROOMS), 'width', WW)

if __name__ == '__main__':
    build(sys.argv[1])
