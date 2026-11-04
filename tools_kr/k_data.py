"""척화비 아래에서 데이터 모으기 -> data/EscapeData.json  (+ 지도 이벤트 · 그림 파일 맞춰 보기)
 python k_data.py <프로젝트 폴더>"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = sys.argv[1]
import k_story as S
import k_portraits as PT

PORTRAIT_FILES = ['kp_%s_%s' % (who, e) for who, exprs in PT.SETS.items() for e in exprs]

# 이어하기 단위: 장을 시작할 때마다 저장 (번호 4자리). 단위 k = 'k장을 시작할 수 있음' (그 앞 장까지의 깃발과 사료 카드)
UNITS = [
    ("c1", ["c0", "p_mom", "p_book", "p_chest", "p_desk"], ["diary"]),
    ("c2", ["a_in", "a_1", "a_2", "a_3", "a_4", "a_talk", "a_stone", "a_sort", "a_mk", "a_m1", "a_m2", "a_m3", "a_pick", "a_q", "r1", "dev1", "quiz1"], ["src_daewon"]),
    ("c3", ["b_in", "b_1", "b_2", "b_3", "b_talk", "b_sneak", "b_order", "b_4", "b_5", "b_6", "b_beacon", "b_stele", "b_rub", "b_words", "r2", "dev2", "quiz2"], ["takbon", "src_yangyo"]),
    ("c4", ["c_in", "c_1", "c_2", "c_3", "c_nego", "c_spot", "c_q", "r3", "dev3", "quiz3"], ["src_treaty"]),
    ("c5", ["d_in", "d_1", "d_2", "d_3", "d_drill", "d_match", "d_paint", "d_sort", "r4", "dev4", "quiz4"], ["src_gaehwa"]),
    ("c6", ["e_in", "e_1", "e_2", "e_3", "e_weigh", "e_riot", "e_r1", "e_r2", "e_r3", "e_r4", "e_map", "e_qing", "e_sort", "r5", "dev5", "quiz5"], ["src_imo"]),
]
NCH = 6

def body(k):
    """k장 처음부터 (저장 표시 단계는 빼고)"""
    st = S.CHAPTER_START[k]()
    return [{"flag": "c%d" % k}] + st[1:]

def resume_steps():
    s = None
    for k in range(1, NCH + 1):
        s = [{"if": {"flag": "c%d" % k}, "then": body(k), "else": s or []}] if s is not None else [{"if": {"flag": "c%d" % k}, "then": body(k)}]
    return s

def code_entry():
    return [{"lock": {"progress": True, "digits": 4, "question": "장을 시작할 때 받은 이어하기 번호 4자리를 입력하세요."},
             "success": [{"text": "번호를 확인했어요. 그 장부터 이어서 합니다."}] + resume_steps(),
             "fail": [{"text": "번호가 맞지 않아요. 처음부터 시작합니다."}]}]

def part(k, label):
    """k장부터 시작 (그 앞 장의 깃발 · 사료 카드를 알림 없이 채움)"""
    flags, items = [], []
    for f, fl, it in UNITS:
        if int(f[1:]) <= k:
            if int(f[1:]) < k: flags.append(f)
            flags += fl; items += it
    return [{"flag": flags, "grant": items}, {"text": label + "부터 시작합니다. 앞 장에서 모을 사료 카드는 가방에 넣어 두었어요.", "speaker": "시작"},
            PREV[k]] + body(k)

PREV = {
    1: {"picture": "kc_diary", "speaker": "지난 이야기", "text": "1882년 가을, 역관 윤재는 일본으로 떠나기 전날 밤 아버지의 통역 일기 다섯 권을 꺼냈다."},
    2: {"picture": "kc_sum1", "speaker": "지난 이야기", "text": "1장: 흥선대원군은 왕권을 세우고 백성의 짐을 덜려 했지만, 경복궁 공사와 당백전으로 원망도 컸다."},
    3: {"picture": "kc_sum2", "speaker": "지난 이야기", "text": "1~2장: 대원군의 개혁, 그리고 병인양요 · 신미양요를 물리친 뒤 척화비를 세워 나라의 문을 굳게 닫았다."},
    4: {"picture": "kc_sum3", "speaker": "지난 이야기", "text": "1~3장: 문을 닫았던 조선은 운요호 사건 뒤 일본과 강화도 조약(1876)을 맺어 문을 열었다. 불평등한 조약이었다."},
    5: {"picture": "kc_sum4", "speaker": "지난 이야기", "text": "1~4장: 정부는 사절단을 보내고 별기군을 만들며 개화를 서둘렀고, 유생들은 위정척사 운동으로 맞섰다."},
}
PART_CHOICES = ["처음부터 하기 (프롤로그부터)", "1장 · 흥선대원군의 개혁", "2장 · 병인양요와 신미양요", "3장 · 강화도 조약",
                "4장 · 개화 정책과 위정척사", "5장 · 임오군란", "이어하기 번호 입력 (다른 기기)"]
def part_menu():
    return {"speaker": "시작", "question": "어디서부터 할까요? (1부 1~2장 · 2부 3~5장)", "choice": PART_CHOICES, "shuffle": False,
            "on2": part(1, "1장"), "on3": part(2, "2장"), "on4": part(3, "3장"), "on5": part(4, "4장"), "on6": part(5, "5장"), "on7": code_entry()}

START = [
    {"if": {"progressSaved": True},
     "then": [{"speaker": "이어하기", "question": "이 기기에 저장된 기록이 있어요. 어떻게 할까요?", "choice": ["새로 시작하기 (장 고르기)", "이 기기에서 이어서 하기"],
               "on2": [{"progressLoad": True, "text": "저장한 곳부터 이어서 합니다."}] + resume_steps(), "on1": [part_menu()], "shuffle": False}],
     "else": [part_menu()]},
]
def add_code_notice(o):
    if isinstance(o, list):
        out = []
        for x in o:
            x = add_code_notice(x); out.append(x)
            if isinstance(x, dict) and x.get("progressSave"):
                out.append({"speaker": "이어하기", "text": "여기까지 이 기기에 저장했어요. 다른 기기에서 이어 하려면 번호 {code} 를 기억하세요."})
        return out
    if isinstance(o, dict): return {k: add_code_notice(v) for k, v in o.items()}
    return o

ROOMS = add_code_notice(S.ROOMS)

PORTRAITS = {"{name}": "kp_{pid}", "통역 · 윤재": "kp_{pid}", "윤희": "kp_{hpid}", "아버지": "kp_father", "어머니": "kp_mother",
             "흥선대원군": "kp_daewongun", "공사 감독관": "kp_overseer", "부역 온 농부": "kp_corvee", "목수": "kp_carpenter", "원납전 낸 부자": "kp_rich",
             "쌀가게 주인": "kp_rice_seller", "상민": "kp_commoner", "유생": "kp_scholar_y", "보부상": "kp_peddler", "장터 아낙": "kp_market_w",
             "양헌수": "kp_yanghs", "포수": "kp_tiger_hunter", "조선 군사": "kp_soldier_k", "어재연": "kp_eojaeyeon", "봉수군": "kp_beacon_m", "박규수": "kp_park_gyusu",
             "신헌": "kp_sinheon", "구로다": "kp_kuroda", "오경석": "kp_ogyeongseok", "최익현": "kp_choi_ik", "일본 상인": "kp_jp_merchant",
             "호리모토": "kp_horimoto", "별기군 병사": "kp_byeolgigun", "구식 군인": "kp_old_soldier", "김홍집": "kp_kimhongjip", "젊은 관리": "kp_young_off",
             "이만손": "kp_imansun", "나이 든 유생": "kp_confucian2", "김춘영": "kp_kimchunyoung", "선혜청 서리": "kp_clerk", "도시 빈민": "kp_poor_m",
             "청 군사": "kp_qing_soldier", "청 상인": "kp_qing_merchant", "박영효": "kp_parkyounghyo", "김옥균": "kp_kimokgyun", "조선 관리": "kp_kyujanggak"}

data = {
    "title": "척화비 아래에서", "gameTitle": "척화비 아래에서",
    "titleImage": "Kr_Title", "titleText": False, "titlePromptY": 0.62,
    "titleLayers": [{"image": "Kr_TitleStele", "side": "left", "margin": 22, "y": 60, "clear": 370},
                    {"image": "Kr_TitleBook", "side": "right", "margin": 24, "y": 80, "clear": 370},
                    {"image": "Kr_TitlePeople", "x": "center", "bottom": 6, "fit": 8}], "titleBgm": "Kr_Title",
    "bgm": "Kr_Home", "timeLimit": 0, "hints": 10, "hp": 3, "wrongPenalty": 0,
    "startRoom": "sarang", "recordTitle": "아버지의 일기를 모두 읽고, 제물포에서 배에 올랐다!",
    "shuffleChoices": True, "roomCards": False, "endingBgm": "Kr_Ending",
    "vars": {"name": "윤재", "pid": "yunjae26", "hpid": "yunhee23", "code": "----", "tension": ""},
    "gauge": {"var": "tension", "label": "협상장 긴장", "min": 0, "max": 10, "style": "level"},
    "archives": S.ARCHIVES,
    "characters": [{"label": "윤재", "image": "$k_yunjae26", "index": 0, "vars": {"name": "윤재"}}],
    "portraits": PORTRAITS,
    "portraitFiles": PORTRAIT_FILES,
    "intro": S.INTRO + START,
    "progress": {"key": "cheokhwabi_1882", "mult": 337, "add": 240, "base": {"flags": []},
                 "keepItems": S.ARCHIVES + ["diary", "takbon", "gatkkeun"],
                 "units": [{"flag": f, "flags": fl, "items": it} for f, fl, it in UNITS]},
    "review": {"url": "https://forms.gle/9PfM9UU7hb5RcCwd6", "picture": "kc_review", "title": "척화비 아래에서 · 후기를 남겨 주세요",
               "text": "끝까지 함께해 줘서 고마워요! [후기 남기기]를 누르면 새 창이 열려요. 휴대폰으로 QR 코드를 찍어도 돼요."},
    "items": S.ITEMS, "hintQuizzes": S.HINTQ, "puzzles": S.PUZZLES, "rooms": ROOMS,
    "ending": {"success": [{"text": "척화비 아래에서 완료!", "speaker": "기록"}],
               "fail": [{"text": "시간이 다 되었다."}],
               "summary": [{"picture": "kc_summary", "speaker": "정리",
                            "text": "흥선대원군의 개혁 → 병인양요 · 신미양요와 척화비 → 강화도 조약 → 개화 정책과 위정척사 → 임오군란 → (2편) 갑신정변"}]},
}

out = os.path.join(ROOT, 'data', 'EscapeData.json')
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False, indent=1))

# ---- 검사
pics = set()
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('picture', 'closeup', 'image', 'image2') and isinstance(v, str) and not v.startswith(('$', '!')) and k != 'image' or (k == 'image' and isinstance(v, str) and v.startswith(('kc_', 'ki_'))): pics.add(v)
            walk(v)
    elif isinstance(o, list):
        for x in o: walk(x)
walk(data)
for k, it in S.ITEMS.items(): pics.add(it['image'])
for f in PORTRAIT_FILES: pics.add(f)
bad = 0
for r in ROOMS:
    mp = json.load(open(os.path.join(ROOT, 'data', 'Map%03d.json' % r['map']), encoding='utf-8'))
    names = {e['name'] for e in mp['events'] if e}
    ids = {h['id'] for h in r['hotspots']}
    for w in r.get('watchers', []): ids.add(w['event'])
    miss = ids - names; extra = names - ids
    if miss or extra: print(r['id'], 'MISSING', sorted(miss), 'EXTRA', sorted(extra)); bad += 1
pd = os.path.join(ROOT, 'img', 'pictures')
have = {f[:-4] for f in os.listdir(pd)} if os.path.isdir(pd) else set()
need = sorted(p for p in pics if p not in have)
print('rooms', len(ROOMS), 'hotspots', sum(len(r['hotspots']) for r in ROOMS), 'pictures', len(pics), 'missing', len(need), need[:30])
items = set(S.ITEMS)
def walk3(o):
    if isinstance(o, dict):
        for k in ('give', 'take', 'grant'):
            if k in o:
                for it in (o[k] if isinstance(o[k], list) else [o[k]]):
                    if it not in items: print('  ? unknown item', it)
        for v in o.values(): walk3(v)
    elif isinstance(o, list):
        for x in o: walk3(x)
walk3(data)
all_ids = {(r['id'], h['id']) for r in ROOMS for h in r['hotspots']}
any_ids = {h for _, h in all_ids}
nogoal = []
def walk4(o, where):
    if isinstance(o, dict):
        if isinstance(o.get('goal'), str):
            t = o.get('targets') or []
            if not t: nogoal.append((where, o['goal'][:30]))
            for x in t:
                if ':' in x:
                    if tuple(x.split(':', 1)) not in all_ids: print('  ? bad target', x)
                elif x not in any_ids: print('  ? bad target', x, 'in', where)
        for v in o.values(): walk4(v, where)
    elif isinstance(o, list):
        for x in o: walk4(x, where)
for r in ROOMS: walk4(r, r['id'])
walk4(data['intro'], 'intro')
print('goals without targets:', len(nogoal), nogoal[:8])
setf = set()
def walk5(o):
    if isinstance(o, dict):
        if 'flag' in o and not any(k in o for k in ('if', 'noFlag', 'flags', 'noFlags')) and len(o) <= 3:
            for f in (o['flag'] if isinstance(o['flag'], list) else [o['flag']]): setf.add(f)
        for v in o.values(): walk5(v)
    elif isinstance(o, list):
        for x in o: walk5(x)
walk5(S.ROOMS)
unit_flags = set(f for f, fl, it in UNITS) | set(x for f, fl, it in UNITS for x in fl)
late = {'h_in', 'h_dad', 'h_1', 'h_2', 'h_ship', 'epi'}
print('flags not in units:', sorted(setf - unit_flags - late))
sp = {r['id']: r for r in ROOMS}
for f, fl, it in UNITS:
    print(f, 'code', '%04d' % ((sum(1 << i for i in range(int(f[1:]))) * 337 + 240) % 10000))
