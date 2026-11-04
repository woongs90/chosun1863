//=============================================================================
// EscapeRoom.js  (RPG Maker MV)
// 걸어 다니며 조사하는 방탈출 엔진 v4.6 (어드벤처 · 잠행 · 미션 · 타이밍 · 체력 · 시네마틱 · 초점 촬영 · 표정 초상화 · 퀘스트 표시 · 전신 키 · 멈춤 방지 · 미니게임 16종 · 그림 자동 닫기 · 온도계 · 후기 화면 · 묶음 자리 배치 · 다이얼 · 탁본 · 대열 훈련 · 저울 · 봉수 · 돌 밀기 · 차례 잠행)
//=============================================================================
/*:
 * @plugindesc 걸어 다니며 조사하는 방탈출 엔진 - 이벤트 이름과 데이터 파일 하나로 단서, 자물쇠, 퀴즈를 만듭니다.
 * @author Claude
 *
 * @param DataFile
 * @text 데이터 파일 이름
 * @desc data 폴더 안에 있는 방탈출 데이터 파일 이름입니다.
 * @default EscapeData.json
 *
 * @param WallRegion
 * @text 벽 리전 번호
 * @type number
 * @min 1
 * @max 255
 * @desc 이 번호의 리전을 칠한 칸은 지나갈 수 없습니다.
 * @default 1
 *
 * @param ShowDebug
 * @text 제작 도우미 보기
 * @type boolean
 * @on 보기
 * @off 숨기기
 * @desc 켜면 벽(리전), 조사 이벤트 이름, 주인공 좌표가 화면에 보입니다. 제작할 때만 켜세요.
 * @default false
 *
 * @param SeDoor
 * @text 효과음: 문 열림
 * @desc audio/se 폴더의 효과음 이름. 파일이 없으면 소리만 나지 않고 게임은 그대로 진행됩니다.
 * @default Open1
 *
 * @param SeSolve
 * @text 효과음: 퍼즐 해결
 * @default Chime2
 *
 * @param SeItem
 * @text 효과음: 아이템 획득
 * @default Item3
 *
 * @param SeGate
 * @text 효과음: 시간의 문
 * @default Teleport
 *
 * @param SeWarp
 * @text 효과음: 시대 이동
 * @default Move1
 *
 * @param SeaRegion
 * @text 바다 리전 번호
 * @type number
 * @desc 이 리전은 배를 탔을 때만 지나갈 수 있습니다. (걸어서는 못 감)
 * @default 2
 *
 * @param DockRegion
 * @text 부두 리전 번호
 * @type number
 * @desc 이 리전은 걸어서도, 배로도 지나갈 수 있습니다. (배 타고 내리는 곳)
 * @default 3
 *
 * @param Fullscreen
 * @text 시작할 때 전체 화면
 * @type boolean
 * @on 켜기
 * @off 끄기
 * @desc 타이틀 화면을 누르는 순간 브라우저 전체 화면(주소창 숨김)으로 바꿉니다. 컴퓨터·안드로이드 브라우저에서 동작 (아이폰은 지원 안 함).
 * @default true
 *
 * @param FullscreenButton
 * @text 전체 화면 버튼
 * @type boolean
 * @on 보이기
 * @off 숨기기
 * @desc 게임 화면 위쪽에 [전체 화면] 버튼을 보여 줍니다. (지원하지 않는 기기에서는 자동으로 숨김)
 * @default true
 *
 * @param AutoWidth
 * @text 화면 비율 자동 맞춤
 * @type boolean
 * @on 자동
 * @off 끄기(기본 크기)
 * @desc 켜면 기기 화면 비율에 맞춰 화면 가로 크기를 정합니다(세로 624 고정). 지도는 가운데에 고정됩니다.
 * @default true
 *
 * @param MaxWidth
 * @text 가장 넓은 화면 가로(px)
 * @type number
 * @min 816
 * @desc 자동 맞춤일 때 화면 가로의 최댓값. 지도 가로 칸 수 x 48 이하로 두세요. (29칸 지도 = 1392)
 * @default 1392
 *
 * @help
 * ============================================================================
 *  사용 방법 (자세한 내용은 함께 드린 안내서를 보세요)
 * ============================================================================
 *  - 방 하나 = 맵 하나. 데이터 파일의 각 방에 "map": 맵 번호 를 적습니다.
 *  - 조사할 물건 = 이벤트. 이벤트 '이름'을 데이터 파일의 조사 지점 id와
 *    똑같이 적으면, 그 앞에서 결정키를 눌렀을 때 데이터 파일 내용이 실행됩니다.
 *    이벤트 내용(실행 내용)은 비워 둬도 됩니다.
 *    큰 물건은 같은 이름의 이벤트를 여러 칸에 놓으면 됩니다.
 *  - 문처럼 걸어 들어가면 반응해야 하는 곳은 이벤트 트리거를
 *    '플레이어로부터 접촉'으로 바꾸세요.
 *  - 지나가면 안 되는 곳은 리전 1번(설정에서 변경 가능)을 칠합니다.
 *  - ESC / X / 오른쪽 클릭: 가방,  H: 힌트
 *
 *  v2.1 추가 기능
 *  - 다이얼 자물쇠: 글자·방향·색깔 등 여러 칸을 돌려 맞추는 자물쇠 ("dial")
 *  - 주인공 고르기: 데이터 파일의 "characters" 목록에서 고르기 ("selectCharacter")
 *  - 캐릭터 그림이 있는 조사 이벤트(NPC)는 말을 걸면 주인공 쪽으로 돌아봅니다.
 *
 *  v2.2 효과
 *  - 문 열림, 퍼즐 해결, 아이템 획득, 오답, 시대 이동, 시간의 문 연출
 *  - 효과음은 audio/se에 파일이 없으면 소리만 나지 않고 게임은 멈추지 않습니다.
 *
 *  v2.3 타이틀·음악·영상 (모두 데이터 파일에서 지정)
 *  - "gameTitle", "titleImage"(img/titles1), "titleText", "titleBgm"
 *  - "bgm"(기본), 방마다 "bgm", "endingBgm", 단계 { "bgm": "곡 이름" }
 *  - 단계 { "movie": "영상 이름" } : movies 폴더의 .webm/.mp4, Enter·클릭으로 건너뛰기
 *  - 파일이 없으면 그 기능만 조용히 건너뜁니다.
 *
 *  v2.4 후기 링크
 *  - 데이터 파일의 "review": { "url": "...", "picture": "...", "text": "..." }
 *    엔딩 정리가 끝난 뒤 안내 화면이 나오고, Enter·클릭을 누르는 순간 링크가 열립니다.
 *  - 단계에 "openUrl"을 붙여도 같은 방식으로 링크를 엽니다.
 *
 *  v2.6 화면 비율 자동 맞춤
 *  - 기기(창) 비율에 맞춰 화면 가로를 816~MaxWidth 사이에서 정합니다.
 *    4:3 태블릿은 816, 16:9 크롬북은 약 1104, 휴대폰 가로는 약 1300.
 *  - 지도는 언제나 가운데에 고정됩니다. 지도를 화면보다 넓게(예: 29칸) 만들고
 *    가운데 17칸에 꼭 필요한 것을 두면, 넓은 화면에서는 양옆 장식이 더 보입니다.
 *  - 화면을 돌리거나 창 크기를 바꾸면, 타이틀 화면이나 자유롭게 걷는 중일 때
 *    자동으로 다시 맞춥니다.
 *  - 휴대폰·태블릿: 톡 눌러 이동/조사, 창 바깥을 누르면 닫기, 세로일 때 가로 안내.
 *
 *  v3.0 어드벤처 기능
 *  - 방에 "camera": "follow" 를 적으면 넓은 지도에서 화면이 주인공을 따라갑니다.
 *  - 배 타기: 단계 { "boat": true } / { "boat": false }.  "go"와 함께 쓰면 도착할 때 바뀝니다.
 *    바다 리전(2)은 배로만, 부두 리전(3)은 둘 다 지나갈 수 있습니다. 배 그림은 "boatSprite".
 *  - 추격: 단계 { "chase": { "targets": [이벤트 이름…], "time": 초, "speed": 4,
 *    "success": [...], "fail": [...] } }  제한 시간 안에 모두 따라잡으면 성공.
 *  - 동료: 데이터 "companion": { "actor": 2, "image": "$gaji", "flag": "나타나는 플래그" }
 *    따라다니는 동료(배를 타면 숨음).
 *  - 목표 안내: 단계 { "goal": "동래로 가서 안용복을 만나자" } → 화면 왼쪽 위에 표시.
 *
 *  v3.1 시작할 때 전체 화면
 *  - 타이틀 화면을 누르는 순간 브라우저 주소창까지 숨기는 전체 화면이 됩니다.
 *    (컴퓨터·안드로이드. 아이폰은 브라우저가 막아 둠. ESC를 누르면 전체 화면이 풀림)
 *  - 끄려면 플러그인 설정 "시작할 때 전체 화면"을 [끄기]로.
 *
 *  v4.1 퀘스트 표시 · 걷는 사람들 · 쫓아오는 진압 (「종로 사진관 2」에서 추가)
 *  - 단계 { "goal": "...", "targets": ["조사 지점 id", "방id:id"] } → 그 대상 위에 "!" 퀘스트 표시 (대상에게 말을 걸면 사라짐)
 *    { "addTarget": "id" } 로 표시 더하기. 조사 지점 "quest": 조건 → 조건이 맞는 동안 늘 표시
 *  - 방 "walkers": [{ "event": "이름", "route": [[x,y],...], "rel": true, "loop": true|"pingpong"|"restart"|false, "speed": 3,
 *    "pause": 0, "wander": 2, "if": 조건, "always": true, "through": true, "anime": true }] → 행진·순찰·서성이는 사람들
 *    단계 { "walkers": [...] } (도중에 걷기 시작) / { "walkersStop": true 또는 ["이름"] } / { "scatter": { "events": [...], "dist": 4 } }
 *  - 감시자 "chase": 4 → 4칸 안에 들어오면 쫓아오고, 닿으면 들킴 (들키면 감시자도 처음 자리로)
 *
 *  v4.0 시네마틱 · 초점 촬영 · 표정 초상화 (「종로 사진관」에서 추가)
 *  - 단계 { "cinema": true } / { "cinema": false } → 위아래 검은 띠. 플레이어가 다시 움직일 수 있게 되면 저절로 꺼짐
 *  - 단계 { "caption": "1945년 8월 15일 정오 · 종로" } → 장면 자막(한 글자씩). 시네마틱이면 위쪽 검은 띠 안에
 *  - 단계 { "zoom": { "event": "김구", "scale": 1.6, "duration": 60 } } / { "zoom": { "x": 14, "y": 6 } } / { "zoom": false }
 *    → 그 인물(또는 칸)이 화면 가운데로 오며 확대. 다른 곳으로 다시 쓰면 천천히 옮겨 감(패닝)
 *  - 단계 { "move": { "event": "이름" 또는 "player", "route": [[x,y],...] 또는 "to": [x,y], "speed": 3, "wait": true, "dir": "up" } }
 *    { "place": { "event": "이름", "x": 3, "y": 4, "dir": "down" } }  { "turn": { "event": "이름", "dir": "left" 또는 "toward": "player" } }
 *    { "balloon": { "event": "이름", "id": 1 } } (말풍선 아이콘)
 *  - 방 "overlay": "!그림_top" 또는 [{ "if": 조건, "name": "..." }] → 원경과 같은 크기의 투명 그림을 인물 위에 (나무 윗부분·처마)
 *  - 표정 초상화: 데이터 "portraits": { "{name}": "pt_hg{age}", "아버지": "pt_dad" }, "portraitFiles": [그림 이름...]
 *    단계 { "speaker": "{name}", "text": "...", "face": "웃음" } → 대화창 위에 초상화 (주인공은 왼쪽, 다른 사람은 오른쪽)
 *    표정: 보통 · 웃음 · 놀람 · 슬픔 · 화남 · 결심 · 걱정 · 생각  (그림 이름 끝: _n _smile _surprise _sad _angry _resolve _worry _think)
 *  - 단계 { "setVar": { "age": "18" } } → 글 속 {age} 바꾸기,  { "heroImage": "$hg18" } → 주인공 걷는 그림 바꾸기
 *  - 초점 촬영: 단계 { "focus": { "picture": "fo_그림", "label": "...", "film": 4, "goal": 1, "speed": 1, "zone": 0.16,
 *    "move": true(인물이 움직임), "smoke": true(연기), "crowd": true(앞사람 머리), "flash": true(다른 기자 플래시),
 *    "success": [...], "fail": [...] } } → 흐렸다 또렷해지는 사진에서 가장 또렷한 순간에 셔터
 *  - 단계 { "weather": { "type": "rain", "power": 5 } } / { "weather": null } → 비·눈 (끄기)
 *  - 데이터 "shuffleChoices": true → 정답이 있는 보기는 순서를 섞음 (단계 "shuffle": false 로 끄기)
 *  - 조건 { "any": [조건, 조건] } (하나만 맞아도),  { "vars": { "age": "18" } }
 *  - 글자 자동 맞춤: 목표·이름표·알림·선택지·가방·다이얼 글자가 칸을 넘으면 작게 / 두 줄로
 *  - 하트(체력)는 "hearts": true 이거나 움직이는 것·함정·추위가 있는 방에서만 보임
 *
 *  v3.7 회상 장면 · 진흙 · 추위
 *  - 방 "memory": true + "tint": [40, 14, -34, 255] → 인물까지 옛날 사진 색 + 낡은 필름 무늬 (fx_memory1·2)
 *  - 리전 5 = 진흙 (걸음이 느려짐)
 *  - 방 "drain": { "every": 600, "damage": 1, "text": "..." } → 일정 시간마다 하트 -1 (아이템 effect "warm"은 느리게)
 *  - 방 "older": true → 주인공 그림을 '이름_old'(어른이 된 모습)로 바꿔 보여 줌 (예: $f_boy → $f_boy_old)
 *
 *  v3.6 이어하기 (서버 없이 브라우저에 저장 + 4자리 이어하기 번호)
 *  - 데이터 "progress": { "key": "china", "units": [{ "flag": "hall1", "flags": [...], "items": [...] }, ...],
 *      "base": { "flags": [...] }, "keepItems": [보물 등] }
 *  - 단계 { "progressSave": true }  → 끝낸 단위(관)를 이 기기 브라우저에 저장, 글 속 {code} = 이어하기 번호
 *  - 단계 { "progressLoad": true } / { "progressClear": true }, 조건 { "progressSaved": true }
 *  - 자물쇠 { "lock": { "progress": true, "digits": 4 }, "success": [...], "fail": [...] } → 번호로 이어하기
 *
 *  v3.5 조건 단계 · 확대 그림 겹치기 · 눌러서 조준
 *  - 단계 { "if": 조건, "then": [단계...], "else": [단계...] } → 조건에 따라 다른 단계
 *  - 단계 { "picture": "판", "overlays": [{ "picture": "칸1", "if": 조건 }, ...] }
 *    → 같은 크기의 투명 그림을 조건이 맞을 때만 위에 겹쳐 보여 줌 (연표에 조각 끼우기 등)
 *  - 방 "darkArea": [x0,y0,x1,y1] → "dark" 어둠이 그 네모 구역 안에서만 (석굴 안 등)
 *  - 힌트 수수께끼에 "rooms": [방 id...] 를 쓰면 그 방에 있을 때 그 힌트를 먼저 보여 줌
 *  - 활: 과녁이나 리전 4 칸을 손가락(마우스)으로 누르면 그 쪽으로 바로 쏨 (휴대폰용)
 *
 *  v3.4 체력 · 함정 · 움직이는 것 · 활 · 어둠 · 아이템 효과
 *  - 데이터 "hp": 3 → 체력 하트. 단계 { "damage": 1 } { "heal": 1 }. 다 떨어지면 방의 "ko" 단계 후 "checkpoint"로
 *  - 방 "traps": { "tiles": [[x,y]...], "count": 5, "kind": "pit"|"spike"|"mixed" } → 들어갈 때마다 무작위 자리
 *    "trapsIf": 조건 (함정이 켜지는 때)
 *  - 방 "movers": [{ "event": "돌1", "route": [[x,y],[x,y]], "speed": 4, "damage": 1, "loop": "restart", "if": 조건 }]
 *  - 방 "bow": true 또는 조건 → A·F 키 / 오른쪽 아래 버튼으로 화살. 조사 지점 "target": { "flag": "...", "steps": [] }
 *    미션 중에는 화살로 맞힌 과녁이 미션 대상으로 셈
 *  - 방 "dark": 3 → 주인공 둘레 3칸만 보임. 아이템 "effect": "light" 하나마다 +2칸
 *  - 아이템 "effect": "speed"(빨라짐) / "charm"(감시에 한 번 들켜도 괜찮음, 쓰면 사라짐) / "light"
 *  - 단계 { "random": [[단계...], [단계...]] } → 그중 하나를 무작위로
 *  - 리전 4 = 낮은 울타리 (걸어서는 못 지나가지만 화살은 넘어감 - 활터 과녁 줄 등)
 *
 *  - 인트로 영상은 기본으로 건너뛸 수 없음. 건너뛰게 하려면 데이터에 "movieSkip": true
 *    (또는 단계 { "movie": "이름", "skip": true }). 영상 파일이 고장 나 멈추면 자동으로 넘어감.
 *
 *  v3.2 잠행 · 미션 · 타이밍 · 퀴즈 힌트
 *  - 감시(잠행): 방에 "watchers": [{ "event": "순사1", "route": [[x,y],[x,y]], "sight": 4 }]
 *    "watchIf": 조건, "checkpoint": [x,y,"up"], "caught": [단계...]  → 시야(빨간 칸)에 들어가면 들킴
 *  - 미션: { "mission": { "targets": [이벤트 이름...], "time": 60, "label": "...", "success": [], "fail": [] } }
 *    제한 시간 안에 대상에게 모두 말을 걸면(결정키) 성공
 *  - 타이밍: { "timing": { "goal": 10, "maxMiss": 3, "speed": 1.6, "zone": 0.22, "label": "등사기 인쇄",
 *    "per": 100, "unit": "장", "success": [], "fail": [] } }
 *  - 퀴즈 힌트: 데이터 "hintQuizzes": [{ "question": "...", "choice": [...], "answer": 1 }]
 *    힌트를 다 쓰면 퀴즈를 맞혀 힌트 1개를 더 얻음
 *  - 따라오는 사람들: 조사 지점에 "follow": 조건  → 조건이 맞으면 주인공을 따라 걸음
 *  - 화면 색(밤): 방에 "tint": [-68,-68,0,68]  /  단계 { "tint": [...], "duration": 60 }
 *  - 사료 수집: 데이터 "archives": [아이템 id...] → 기록 화면에 모은 개수 표시
 */

var Imported = Imported || {};
Imported.EscapeRoom = '4.0.0';

var $dataEscape = null;
var EscapeManager = null;

(function() {
    'use strict';

    var params = PluginManager.parameters('EscapeRoom');
    var DATA_FILE = String(params['DataFile'] || 'EscapeData.json');
    var WALL_REGION = Number(params['WallRegion'] || 1);
    var SHOW_DEBUG = String(params['ShowDebug']) === 'true';
    var SE_DOOR = params['SeDoor'] === undefined ? 'Open1' : String(params['SeDoor']);
    var SE_SOLVE = params['SeSolve'] === undefined ? 'Chime2' : String(params['SeSolve']);
    var SE_ITEM = params['SeItem'] === undefined ? 'Item3' : String(params['SeItem']);
    var SE_GATE = params['SeGate'] === undefined ? 'Teleport' : String(params['SeGate']);
    var SE_WARP = params['SeWarp'] === undefined ? 'Move1' : String(params['SeWarp']);

    var SEA_REGION = Number(params['SeaRegion'] || 2);
    var DOCK_REGION = Number(params['DockRegion'] || 3);
    var AUTO_WIDTH = String(params['AutoWidth']) !== 'false';
    var FULLSCREEN = String(params['Fullscreen']) !== 'false';
    var FULL_BUTTON = String(params['FullscreenButton']) !== 'false';
    var MAX_WIDTH = Math.max(816, Number(params['MaxWidth'] || 1392));
    var BASE_W = 816, BASE_H = 624;

    var HUD_H = 40;
    var MSG_LINES = 3;

    //=========================================================================
    // 화면 비율 자동 맞춤
    //=========================================================================
    function escTargetWidth() {
        var w = window.innerWidth || BASE_W, h = window.innerHeight || BASE_H;
        var t = Math.round(BASE_H * (w / h) / 2) * 2;
        return Math.max(BASE_W, Math.min(MAX_WIDTH, t));
    }

    // 휴대폰에서 실제 화면 크기를 재도록 viewport 설정 (MV 기본 index.html은 980px 가상 화면)
    if (AUTO_WIDTH) {
        try {
            var vm = document.querySelector('meta[name="viewport"]');
            if (!vm) { vm = document.createElement('meta'); vm.name = 'viewport'; document.head.appendChild(vm); }
            vm.setAttribute('content', 'width=device-width, initial-scale=1, maximum-scale=1, user-scalable=no, viewport-fit=cover');
        } catch (e) {}
    }

    // 자동 맞춤일 때는 컴퓨터 브라우저에서도 창 크기에 맞춰 확대/축소 (MV 기본은 휴대폰·NW.js만)
    if (AUTO_WIDTH) {
        Graphics._defaultStretchMode = function() { return true; };
    }

    var _SceneManager_initGraphics = SceneManager.initGraphics;
    SceneManager.initGraphics = function() {
        if (AUTO_WIDTH) {
            var tw = escTargetWidth();
            this._screenWidth = this._boxWidth = tw;
            this._screenHeight = this._boxHeight = BASE_H;
        }
        _SceneManager_initGraphics.call(this);
    };

    // 실행 중에 화면을 돌리거나 창 크기가 바뀌면: 안전한 순간에 다시 맞춤
    var escResize = { pending: 0, timer: null };
    function escApplyWidth(tw) {
        SceneManager._screenWidth = SceneManager._boxWidth = tw;
        Graphics.boxWidth = tw;
        Graphics.width = tw;
        escResize.pending = 0;
    }
    if (AUTO_WIDTH) {
        window.addEventListener('resize', function() {
            clearTimeout(escResize.timer);
            escResize.timer = setTimeout(function() {
                if (!Graphics._renderer) return;
                var tw = escTargetWidth();
                escResize.pending = Math.abs(tw - Graphics.width) >= 16 ? tw : 0;
                var sc = SceneManager._scene;
                if (sc && sc.escRefreshHud) sc.escRefreshHud();     // '전체 화면 / 창 모드' 단추 글씨 바꾸기
            }, 150);
        });
    }

    // 새 장면(지도)을 만들기 직전에 바뀐 화면 크기를 바로 반영 (전체 화면 전환 직후 등)
    var _Scene_Map_createDisplayObjects_w = Scene_Map.prototype.createDisplayObjects;
    Scene_Map.prototype.createDisplayObjects = function() {
        if (AUTO_WIDTH && escResize.pending) {
            escApplyWidth(escResize.pending);
            if ($gamePlayer) $gamePlayer.center($gamePlayer.x, $gamePlayer.y);
        }
        _Scene_Map_createDisplayObjects_w.call(this);
    };

    //=========================================================================
    // 시작할 때 전체 화면 (브라우저는 사용자가 누른 순간에만 허락하므로 그 순간에 요청)
    //=========================================================================
    // 설치형(MV 테스트 실행 · Game.exe, NW.js)은 창 자체를 전체 화면으로 (누르지 않아도 됨)
    function escNwWin() {
        try {
            if (!Utils.isNwjs()) return null;
            if (typeof nw !== 'undefined' && nw.Window) return nw.Window.get();
            return require('nw.gui').Window.get();
        } catch (e) { return null; }
    }
    function escCanFullscreen(forButton) {
        if (!FULLSCREEN && !forButton) return false;
        if (Utils.isNwjs()) return !!escNwWin();
        var el = document.documentElement;
        return !!(el.requestFullscreen || el.webkitRequestFullscreen || el.msRequestFullscreen);
    }
    function escIsFullscreen() {
        var w = escNwWin();
        if (w) return !!w.isFullscreen;
        return !!(document.fullscreenElement || document.webkitFullscreenElement || document.msFullscreenElement);
    }
    function escExitFullscreen() {
        var w = escNwWin();
        if (w) { try { w.leaveFullscreen(); } catch (e) {} return; }
        try {
            var r = document.exitFullscreen ? document.exitFullscreen() : document.webkitExitFullscreen ? document.webkitExitFullscreen() : document.msExitFullscreen && document.msExitFullscreen();
            if (r && r.catch) r.catch(function() {});
        } catch (e) {}
    }
    function escToggleFullscreen() {
        if (escIsFullscreen()) escExitFullscreen(); else escRequestFullscreen(true);
    }
    ['fullscreenchange', 'webkitfullscreenchange'].forEach(function(n) {
        document.addEventListener(n, function() {
            var sc = SceneManager._scene;
            if (sc && sc.escRefreshHud) sc.escRefreshHud();
        });
    });
    function escRequestFullscreen(forButton) {
        if (!escCanFullscreen(forButton) || escIsFullscreen()) return;
        var nwW = escNwWin();
        if (nwW) { try { nwW.enterFullscreen(); } catch (e) {} return; }
        var el = document.documentElement;
        try {
            var r = el.requestFullscreen ? el.requestFullscreen({ navigationUI: 'hide' }) :
                    el.webkitRequestFullscreen ? el.webkitRequestFullscreen() : el.msRequestFullscreen();
            if (r && r.catch) r.catch(function() {});
        } catch (e) {}
    }
    var escFsArmed = null, escFsNwDone = false;
    function escArmFullscreen() {
        if (escNwWin()) { if (FULLSCREEN && !escFsNwDone) { escFsNwDone = true; escRequestFullscreen(); } return; }   // 설치형은 바로 전체 화면
        if (!escCanFullscreen() || escFsArmed) return;
        escFsArmed = function(ev) {
            if (ev.type === 'keydown' && ['Enter', ' ', 'Spacebar', 'z', 'Z'].indexOf(ev.key) < 0) return;
            escDisarmFullscreen();
            escRequestFullscreen();
        };
        ['mousedown', 'touchend', 'keydown'].forEach(function(n) { document.addEventListener(n, escFsArmed, true); });
    }
    function escDisarmFullscreen() {
        if (!escFsArmed) return;
        var f = escFsArmed; escFsArmed = null;
        ['mousedown', 'touchend', 'keydown'].forEach(function(n) { document.removeEventListener(n, f, true); });
    }

    var _Scene_Title_update = Scene_Title.prototype.update;
    Scene_Title.prototype.update = function() {
        _Scene_Title_update.call(this);
        if (escResize.pending && this.isActive() && !SceneManager.isSceneChanging()) {
            escApplyWidth(escResize.pending);
            SceneManager.goto(Scene_Title);
        }
    };

    function escMapResizeSafe(scene) {
        var M = EscapeManager;
        if (!scene.isActive() || SceneManager.isSceneChanging()) return false;
        if ($gamePlayer.isMoving() || $gamePlayer.isTransferring() || $gameMap.isEventRunning()) return false;
        if (!M || !M.isActive()) return true;
        return M._phase === 'play' && M.canInteract() && !M._bagOpen;
    }

    // 지도 가운데 고정 (지도가 화면보다 넓으면 양옆이 똑같이 잘려 보임)
    function escCenteredMap() {
        if (!$dataMap) return false;
        if (EscapeManager && EscapeManager.isActive && EscapeManager.isActive()) {
            var room = EscapeManager.currentRoom && EscapeManager.currentRoom();
            if (room && room.camera === 'follow') return false;
        }
        return /<escCenter>/i.test($dataMap.note || '') || (EscapeManager && EscapeManager.isActive && EscapeManager.isActive());
    }
    // 지도가 화면보다 좁으면(예: 예전 17칸 지도) 가운데에 두고 양옆은 검게 가립니다.
    // (원경 그림이 옆으로 반복되어 방이 여러 개처럼 보이는 것을 막음)
    Game_Map.prototype.escCenterView = function() {
        var dx = (this.width() - this.screenTileX()) / 2;
        var dy = (this.height() - this.screenTileY()) / 2;
        this._displayX = dx;
        this._displayY = dy;
        this._parallaxX = dx;
        this._parallaxY = dy;
    };

    var _Spriteset_Map_createParallax = Spriteset_Map.prototype.createParallax;
    Spriteset_Map.prototype.createParallax = function() {
        _Spriteset_Map_createParallax.call(this);
        this._escBars = new PIXI.Graphics();
        this._escBarsKey = '';
        this._baseSprite.addChild(this._escBars);
    };

    var _Spriteset_Map_update = Spriteset_Map.prototype.update;
    Spriteset_Map.prototype.update = function() {
        _Spriteset_Map_update.call(this);
        this.escUpdateBars();
    };

    Spriteset_Map.prototype.escUpdateBars = function() {
        var g = this._escBars;
        if (!g) return;
        var tw = $gameMap.tileWidth(), th = $gameMap.tileHeight();
        var left = Math.round(-$gameMap.displayX() * tw);          // 지도 왼쪽 끝의 화면 x
        var right = left + $gameMap.width() * tw;
        var top = Math.round(-$gameMap.displayY() * th);
        var bottom = top + $gameMap.height() * th;
        var W = Graphics.width, H = Graphics.height;
        var key = [left, right, top, bottom, W, H].join(',');
        if (key === this._escBarsKey) return;
        this._escBarsKey = key;
        g.clear();
        if ($gameMap.isLoopHorizontal() || $gameMap.isLoopVertical()) return;
        g.beginFill(0x000000, 1);
        if (left > 0) g.drawRect(0, 0, left, H);
        if (right < W) g.drawRect(right, 0, W - right, H);
        if (top > 0) g.drawRect(0, 0, W, top);
        if (bottom < H) g.drawRect(0, bottom, W, H - bottom);
        g.endFill();
    };
    var _Game_Player_center = Game_Player.prototype.center;
    Game_Player.prototype.center = function(x, y) {
        if (escCenteredMap()) return $gameMap.escCenterView();
        return _Game_Player_center.call(this, x, y);
    };
    var _Game_Player_updateScroll = Game_Player.prototype.updateScroll;
    Game_Player.prototype.updateScroll = function(lastX, lastY) {
        if (escCenteredMap()) return $gameMap.escCenterView();
        _Game_Player_updateScroll.call(this, lastX, lastY);
    };

    function SW() { return Graphics.boxWidth; }
    function SH() { return Graphics.boxHeight; }

    //=========================================================================
    // 데이터 파일 불러오기
    //=========================================================================
    var _DataManager_loadDatabase = DataManager.loadDatabase;
    DataManager.loadDatabase = function() {
        _DataManager_loadDatabase.call(this);
        loadEscapeData();
    };

    function loadEscapeData() {
        $dataEscape = null;
        var url = 'data/' + DATA_FILE;
        var xhr = new XMLHttpRequest();
        xhr.open('GET', url);
        xhr.overrideMimeType('application/json');
        xhr.onload = function() {
            if (xhr.status >= 400) {
                $dataEscape = { __error: '데이터 파일을 찾을 수 없습니다: ' + url };
                return;
            }
            try {
                $dataEscape = JSON.parse(xhr.responseText);
            } catch (e) {
                $dataEscape = { __error: '데이터 파일에 문법 오류가 있습니다.\n' + e.message +
                    '\n쉼표(,), 따옴표("), 괄호를 확인해 주세요.' };
            }
        };
        xhr.onerror = function() {
            $dataEscape = { __error: '데이터 파일을 찾을 수 없습니다: ' + url };
        };
        xhr.send();
    }

    // 음악·영상·타이틀 그림이 실제로 있는지 미리 확인 (없으면 그 기능만 건너뜀)
    var EscapeAssets = {};
    var _assetState = 'idle';
    var _assetPending = 0;

    // 창 바깥을 톡 눌렀는지 (단서 그림 위를 누른 것은 제외)
    function escTappedOutside(win) {
        if (!TouchInput.isTriggered()) return false;
        var lx = win.canvasToLocalX(TouchInput.x), ly = win.canvasToLocalY(TouchInput.y);
        if (lx >= 0 && ly >= 0 && lx < win.width && ly < win.height) return false;
        if (TouchInput.y < HUD_H) return false;
        var sc = SceneManager._scene, cu = sc && sc._escCloseup;
        if (cu && cu.visible && cu.bitmap && cu.bitmap.width) {
            var w = cu.bitmap.width * cu.scale.x, h = cu.bitmap.height * cu.scale.y;
            if (Math.abs(TouchInput.x - cu.x) < w / 2 && Math.abs(TouchInput.y - cu.y) < h / 2) return false;
        }
        return true;
    }

    // 건너뛴 영상이 MV의 재시도 타이머로 다시 시작되지 않도록
    var _Graphics_playVideoInner = Graphics._playVideo;
    Graphics._playVideo = function(src) {
        if (this._escVideoCancelled) return;
        _Graphics_playVideoInner.call(this, src);
    };

    function videoExt() {
        return Game_Interpreter.prototype.videoFileExt.call(null);
    }

    function assetUrl(key) {
        var i = key.indexOf('/');
        var kind = key.substring(0, i);
        var name = key.substring(i + 1);
        var url;
        if (kind === 'bgm') {
            url = AudioManager._path + 'bgm/' + encodeURIComponent(name) + AudioManager.audioFileExt();
            if (Decrypter.hasEncryptedAudio) url = Decrypter.extToEncryptExt(url);
        } else if (kind === 'title') {
            url = 'img/titles1/' + encodeURIComponent(name) + '.png';
            if (Decrypter.hasEncryptedImages) url = Decrypter.extToEncryptExt(url);
        } else if (kind === 'pic') {
            url = 'img/pictures/' + encodeURIComponent(name) + '.png';
            if (Decrypter.hasEncryptedImages) url = Decrypter.extToEncryptExt(url);
        } else {
            url = 'movies/' + encodeURIComponent(name) + videoExt();
        }
        return url;
    }

    function collectAssets(d) {
        var keys = {};
        var addBgm = function(n) { if (n) keys['bgm/' + n] = true; };
        if (d.titleImage) keys['title/' + d.titleImage] = true;
        toArray(d.titleLayers).forEach(function(L) { if (L && L.image) keys['title/' + L.image] = true; });
        addBgm(d.titleBgm); addBgm(d.bgm); addBgm(d.endingBgm);
        var scan = function(steps) {
            toArray(steps).forEach(function(st) {
                if (!st || typeof st !== 'object') return;
                if (st.bgm) addBgm(st.bgm);
                if (st.movie) keys['movie/' + st.movie] = true;
                Object.keys(st).forEach(function(k) {
                    if (k === 'success' || k === 'fail' || k === 'cancel' || /^on\d+$/.test(k)) scan(st[k]);
                });
            });
        };
        scan(d.intro);
        // 그림(확대 그림·아이템 그림): 없으면 멈추지 않고 건너뛰기
        var deep = function(o) {
            if (!o || typeof o !== 'object') return;
            if (Array.isArray(o)) { o.forEach(deep); return; }
            Object.keys(o).forEach(function(k) {
                var v = o[k];
                if ((k === 'picture' || k === 'closeup') && typeof v === 'string' && v) keys['pic/' + v] = true;
                else deep(v);
            });
        };
        deep(d.intro); deep(d.rooms); deep(d.review); deep(d.ending);
        Object.keys(d.items || {}).forEach(function(id) {
            var it = d.items[id] || {};
            if (it.image) keys['pic/' + it.image] = true;
            if (it.closeup) keys['pic/' + it.closeup] = true;
        });
        toArray(d.rooms).forEach(function(r) {
            addBgm(r.bgm);
            scan(r.enter);
            toArray(r.hotspots).forEach(function(h) {
                scan(h.steps);
                toArray(h.cases).forEach(function(c) { scan(c.steps); });
            });
        });
        return Object.keys(keys);
    }

    function startAssetCheck() {
        _assetState = 'checking';
        var d = $dataEscape;
        var keys = (d && !d.__error) ? collectAssets(d) : [];
        _assetPending = keys.length;
        if (_assetPending === 0) _assetState = 'done';
        keys.forEach(function(key) {
            var done = function(ok) {
                if (EscapeAssets[key] !== undefined) return;
                EscapeAssets[key] = ok;
                if (!ok) console.warn('EscapeRoom: 파일이 없어 건너뜁니다 → ' + assetUrl(key));
                _assetPending--;
                if (_assetPending <= 0) _assetState = 'done';
            };
            try {
                var xhr = new XMLHttpRequest();
                xhr.open('GET', assetUrl(key));
                xhr.responseType = 'arraybuffer';
                xhr.onload = function() {
                    done(xhr.status < 400 && !!xhr.response && xhr.response.byteLength > 0);
                };
                xhr.onerror = function() { done(false); };
                xhr.send();
            } catch (e) {
                done(false);
            }
        });
    }

    var _DataManager_isDatabaseLoaded = DataManager.isDatabaseLoaded;
    DataManager.isDatabaseLoaded = function() {
        if (!_DataManager_isDatabaseLoaded.call(this) || !$dataEscape) return false;
        if (_assetState === 'idle') startAssetCheck();
        return _assetState === 'done';
    };

    function hasAsset(kind, name) {
        return !!name && EscapeAssets[kind + '/' + name] === true;
    }

    // 없는 그림을 불러도 '불러오기 오류'로 멈추지 않게 빈 그림으로 바꿔 줌
    var _ImageManager_loadPicture = ImageManager.loadPicture;
    ImageManager.loadPicture = function(filename, hue) {
        if (filename && EscapeAssets['pic/' + filename] === false) return new Bitmap(1, 1);
        return _ImageManager_loadPicture.call(this, filename, hue);
    };

    //=========================================================================
    // 타이틀 화면: 그림 · 게임 이름 · 음악
    //=========================================================================
    function escData() {
        return $dataEscape && !$dataEscape.__error ? $dataEscape : null;
    }

    var _Scene_Title_createBackground = Scene_Title.prototype.createBackground;
    Scene_Title.prototype.createBackground = function() {
        var d = escData();
        if (d && hasAsset('title', d.titleImage)) {
            var bmp = ImageManager.loadTitle1(d.titleImage);
            this._backSprite1 = new Sprite(bmp);
            this._backSprite1.anchor.x = 0.5;
            this._backSprite1.anchor.y = 0.5;
            this._backSprite1.x = Graphics.width / 2;
            this._backSprite1.y = Graphics.height / 2;
            var spr = this._backSprite1;
            bmp.addLoadListener(function() {
                var sc = Math.max(1, Graphics.width / bmp.width, Graphics.height / bmp.height);
                spr.scale.x = spr.scale.y = sc;
            });
            this._backSprite2 = new Sprite();
            this.addChild(this._backSprite1);
            this.addChild(this._backSprite2);
            this._escTitleImage = true;
        } else {
            _Scene_Title_createBackground.call(this);
        }
    };

    var _Scene_Title_drawGameTitle = Scene_Title.prototype.drawGameTitle;
    Scene_Title.prototype.drawGameTitle = function() {
        var d = escData();
        if (this._escTitleImage && d && d.titleText === false) return;
        if (d && d.gameTitle) {
            var b = this._gameTitleSprite.bitmap;
            b.outlineColor = 'rgba(40,22,10,1)';
            b.outlineWidth = 8;
            b.fontSize = 64;
            b.textColor = '#ffe8a0';
            b.drawText(d.gameTitle, 20, Graphics.height / 4, Graphics.width - 40, 64, 'center');
            return;
        }
        _Scene_Title_drawGameTitle.call(this);
    };

    var _Scene_Title_playTitleMusic = Scene_Title.prototype.playTitleMusic;
    Scene_Title.prototype.playTitleMusic = function() {
        var d = escData();
        if (d && hasAsset('bgm', d.titleBgm)) {
            AudioManager.playBgm({ name: d.titleBgm, volume: 90, pitch: 100, pan: 0 });
            AudioManager.stopBgs();
            AudioManager.stopMe();
            return;
        }
        _Scene_Title_playTitleMusic.call(this);
    };

    var _Scene_Title_start = Scene_Title.prototype.start;
    Scene_Title.prototype.start = function() {
        _Scene_Title_start.call(this);
        var d = escData();
        if (d && d.gameTitle) document.title = d.gameTitle;
        if (d) escArmFullscreen();
    };

    // 타이틀: 새 게임/계속/옵션 메뉴 대신 "화면을 클릭하세요" 안내 → 누르면 바로 시작
    var _Scene_Title_createCommandWindow = Scene_Title.prototype.createCommandWindow;
    Scene_Title.prototype.createCommandWindow = function() {
        _Scene_Title_createCommandWindow.call(this);
        if (!escData()) return;
        this._commandWindow.visible = false;
        this._commandWindow.deactivate();
        this._escPressFrames = 0;
        var touch = Utils.isMobileDevice() || ('ontouchstart' in window) || (navigator.maxTouchPoints > 1);
        var text = touch ? '게임을 시작하려면 화면을 터치하세요' : '게임을 시작하려면 화면을 클릭하세요';
        var bw = 520, bh = 56;
        var bmp = new Bitmap(bw, bh);
        roundRect(bmp, 2, 2, bw - 4, bh - 4, 26, 'rgba(12,10,20,0.62)', 'rgba(255,226,150,0.85)', 2);
        bmp.fontSize = 26;
        bmp.fontFace = '"EscReadable", ' + bmp.fontFace;
        bmp.textColor = '#ffe9b0';
        bmp.outlineColor = 'rgba(0,0,0,0.7)';
        bmp.outlineWidth = 4;
        bmp.drawText(text, 0, 0, bw, bh, 'center');
        var sp = new Sprite(bmp);
        sp.anchor.x = 0.5;
        sp.anchor.y = 0.5;
        sp.x = Graphics.width / 2;
        sp.y = Math.round(Graphics.height * Number(escData().titlePromptY || 0.74));
        this._escPress = sp;
        this.addChild(sp);
    };

    var _Scene_Title_updateTitlePress = Scene_Title.prototype.update;
    Scene_Title.prototype.update = function() {
        if (this._escPress) {
            this._commandWindow.visible = false;
            this._commandWindow.deactivate();
            this._commandWindow.openness = 0;
        }
        _Scene_Title_updateTitlePress.call(this);
        if (!this._escPress) return;
        this._escPressFrames++;
        this._escPress.opacity = 150 + Math.round(105 * Math.abs(Math.sin(this._escPressFrames / 28)));
        if (this._escStarting || !this.isActive() || this.isBusy() || SceneManager.isSceneChanging()) return;
        if (this._escPressFrames > 15 && (Input.isTriggered('ok') || TouchInput.isTriggered())) {
            this._escStarting = true;
            this._escPress.visible = false;
            SoundManager.playOk();
            this.commandNewGame();
        }
    };

    // 대시(Shift, 클릭 이동 시 자동 달리기) 끄기
    var _Game_Player_updateDashing = Game_Player.prototype.updateDashing;
    Game_Player.prototype.updateDashing = function() {
        if (EscapeManager && EscapeManager.isActive && EscapeManager.isActive()) {
            this._dashing = false;
            return;
        }
        _Game_Player_updateDashing.call(this);
    };

    //=========================================================================
    // 도움 함수
    //=========================================================================
    function toArray(v) {
        if (v === undefined || v === null) return [];
        return Array.isArray(v) ? v : [v];
    }

    // 외부 링크 열기 (설치형: 기본 브라우저 / 웹: 새 탭)
    function openExternal(url) {
        try {
            if (Utils.isNwjs()) {
                var shell = (typeof nw !== 'undefined' && nw.Shell) ? nw.Shell : require('nw.gui').Shell;
                shell.openExternal(url);
                return true;
            }
            var w = window.open(url, '_blank');
            if (w) {
                try { w.opener = null; } catch (e) {}
                return true;
            }
        } catch (e) {
            console.warn('EscapeRoom: 링크를 열지 못했습니다 → ' + url);
        }
        return false;
    }

    // 안전한 효과음: 파일이 없어도 게임이 멈추지 않고 조용히 넘어갑니다.
    var _seCache = {};
    function playSafeSe(name, volume, pitch) {
        if (!name) return false;
        var ctx = WebAudio._context;
        if (!ctx) return false;
        var play = function(buffer) {
            try {
                var src = ctx.createBufferSource();
                src.buffer = buffer;
                src.playbackRate.value = (pitch || 100) / 100;
                var g = ctx.createGain();
                g.gain.value = (AudioManager.seVolume / 100) * ((volume || 90) / 100);
                src.connect(g);
                g.connect(WebAudio._masterGainNode || ctx.destination);
                src.start(0);
            } catch (e) {}
        };
        var cached = _seCache[name];
        if (cached === false) return false;
        if (cached && cached !== 'loading') {
            play(cached);
            return true;
        }
        if (cached === 'loading') return true;
        _seCache[name] = 'loading';
        var url = AudioManager._path + 'se/' + encodeURIComponent(name) + AudioManager.audioFileExt();
        if (Decrypter.hasEncryptedAudio) url = Decrypter.extToEncryptExt(url);
        var xhr = new XMLHttpRequest();
        try {
            xhr.open('GET', url);
            xhr.responseType = 'arraybuffer';
            xhr.onload = function() {
                if (xhr.status >= 400 || !xhr.response || !xhr.response.byteLength) {
                    _seCache[name] = false;
                    return;
                }
                try {
                    var arr = xhr.response;
                    if (Decrypter.hasEncryptedAudio) arr = Decrypter.decryptArrayBuffer(arr);
                    ctx.decodeAudioData(arr, function(buffer) {
                        _seCache[name] = buffer;
                        play(buffer);
                    }, function() { _seCache[name] = false; });
                } catch (e) {
                    _seCache[name] = false;
                }
            };
            xhr.onerror = function() { _seCache[name] = false; };
            xhr.send();
        } catch (e) {
            _seCache[name] = false;
        }
        return true;
    }

    // 효과용 그림(코드로 그림)
    var _fxCache = {};
    function fxGlow(size, rgb) {
        var key = 'glow' + size + rgb;
        if (_fxCache[key]) return _fxCache[key];
        var b = new Bitmap(size, size);
        var ctx = b._context || b.context;
        var g = ctx.createRadialGradient(size / 2, size / 2, 0, size / 2, size / 2, size / 2);
        g.addColorStop(0, 'rgba(' + rgb + ',1)');
        g.addColorStop(0.35, 'rgba(' + rgb + ',0.55)');
        g.addColorStop(1, 'rgba(' + rgb + ',0)');
        ctx.fillStyle = g;
        ctx.fillRect(0, 0, size, size);
        setDirty(b);
        _fxCache[key] = b;
        return b;
    }
    function fxSpark(rgb) {
        var key = 'spark' + rgb;
        if (_fxCache[key]) return _fxCache[key];
        var b = new Bitmap(24, 24);
        var ctx = b._context || b.context;
        var g = ctx.createRadialGradient(12, 12, 0, 12, 12, 12);
        g.addColorStop(0, 'rgba(255,255,255,1)');
        g.addColorStop(0.3, 'rgba(' + rgb + ',0.8)');
        g.addColorStop(1, 'rgba(' + rgb + ',0)');
        ctx.fillStyle = g;
        ctx.beginPath();
        ctx.moveTo(12, 0); ctx.lineTo(14, 10); ctx.lineTo(24, 12); ctx.lineTo(14, 14);
        ctx.lineTo(12, 24); ctx.lineTo(10, 14); ctx.lineTo(0, 12); ctx.lineTo(10, 10);
        ctx.closePath();
        ctx.fill();
        setDirty(b);
        _fxCache[key] = b;
        return b;
    }
    function fxRays(size) {
        var key = 'rays' + size;
        if (_fxCache[key]) return _fxCache[key];
        var b = new Bitmap(size, size);
        var ctx = b._context || b.context;
        var c = size / 2;
        for (var i = 0; i < 12; i++) {
            var a = i * Math.PI / 6;
            var g = ctx.createRadialGradient(c, c, 0, c, c, c);
            g.addColorStop(0, 'rgba(255,248,210,0.9)');
            g.addColorStop(1, 'rgba(255,248,210,0)');
            ctx.fillStyle = g;
            ctx.beginPath();
            ctx.moveTo(c, c);
            ctx.lineTo(c + Math.cos(a - 0.09) * c, c + Math.sin(a - 0.09) * c);
            ctx.lineTo(c + Math.cos(a + 0.09) * c, c + Math.sin(a + 0.09) * c);
            ctx.closePath();
            ctx.fill();
        }
        setDirty(b);
        _fxCache[key] = b;
        return b;
    }
    function fxDoorway() {
        if (_fxCache.doorway) return _fxCache.doorway;
        var b = new Bitmap(48, 48);
        var ctx = b._context || b.context;
        var g = ctx.createRadialGradient(24, 24, 2, 24, 24, 30);
        g.addColorStop(0, 'rgba(255,250,220,0.95)');
        g.addColorStop(0.6, 'rgba(255,214,120,0.55)');
        g.addColorStop(1, 'rgba(255,190,90,0)');
        ctx.fillStyle = g;
        ctx.fillRect(0, 0, 48, 48);
        setDirty(b);
        _fxCache.doorway = b;
        return b;
    }

    function setDirty(bitmap) {
        if (bitmap._setDirty) bitmap._setDirty();
    }

    function ctxOf(bitmap) {
        return bitmap._context || bitmap.context;
    }

    function roundRect(bitmap, x, y, w, h, r, fill, stroke, lineWidth) {
        var ctx = ctxOf(bitmap);
        ctx.save();
        ctx.beginPath();
        ctx.moveTo(x + r, y);
        ctx.lineTo(x + w - r, y);
        ctx.quadraticCurveTo(x + w, y, x + w, y + r);
        ctx.lineTo(x + w, y + h - r);
        ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
        ctx.lineTo(x + r, y + h);
        ctx.quadraticCurveTo(x, y + h, x, y + h - r);
        ctx.lineTo(x, y + r);
        ctx.quadraticCurveTo(x, y, x + r, y);
        ctx.closePath();
        if (fill) {
            ctx.fillStyle = fill;
            ctx.fill();
        }
        if (stroke) {
            ctx.strokeStyle = stroke;
            ctx.lineWidth = lineWidth || 2;
            ctx.stroke();
        }
        ctx.restore();
        setDirty(bitmap);
    }

    // 한글 줄바꿈: 띄어쓰기 단위로 자르고, 너무 긴 단어는 글자 단위로 자릅니다.
    function wrapText(bitmap, text, maxWidth) {
        var result = [];
        String(text).replace(/\\n/g, '\n').split('\n').forEach(function(para) {
            var words = para.split(' ');
            var line = '';
            words.forEach(function(word) {
                var test = line ? line + ' ' + word : word;
                if (bitmap.measureTextWidth(test) <= maxWidth) {
                    line = test;
                    return;
                }
                if (line) result.push(line);
                line = '';
                var chunk = '';
                for (var i = 0; i < word.length; i++) {
                    var t = chunk + word[i];
                    if (bitmap.measureTextWidth(t) > maxWidth && chunk) {
                        result.push(chunk);
                        chunk = word[i];
                    } else {
                        chunk = t;
                    }
                }
                line = chunk;
            });
            result.push(line);
        });
        return result;
    }

    function formatTime(sec) {
        sec = Math.max(0, Math.ceil(sec));
        var m = Math.floor(sec / 60);
        var s = sec % 60;
        return (m < 10 ? '0' : '') + m + ':' + (s < 10 ? '0' : '') + s;
    }

    var DIR_NAMES = { down: 2, left: 4, right: 6, up: 8 };
    function toDir(d) {
        if (typeof d === 'string') return DIR_NAMES[d] || 2;
        return Number(d) || 0;
    }

    //=========================================================================
    // Window_EscMessage - 대사창 (글자가 한 글자씩 나타납니다)
    //=========================================================================
    function Window_EscMessage() {
        this.initialize.apply(this, arguments);
    }
    Window_EscMessage.prototype = Object.create(Window_Base.prototype);
    Window_EscMessage.prototype.constructor = Window_EscMessage;

    Window_EscMessage.prototype.initialize = function() {
        var h = this.fittingHeight(MSG_LINES);
        Window_Base.prototype.initialize.call(this, 12, SH() - h - 10, SW() - 24, h);
        this.openness = 0;
        this._pages = [];
        this._callback = null;
        this._waitInput = false;
        this._openFrame = 0;
        this._shown = 0;
        this._total = 0;
        this._nameWindow = null;
    };

    Window_EscMessage.prototype.standardFontSize = function() { return 24; };
    Window_EscMessage.prototype.lineHeight = function() { return 36; };
    Window_EscMessage.prototype.setNameWindow = function(w) { this._nameWindow = w; };

    // 글 속 {이름} 바꾸기: 주인공 고르기 "vars" / 데이터 "vars"
    function escSub(t) {
        if (t === null || t === undefined) return t;
        t = String(t);
        if (t.indexOf('{') < 0 || !EscapeManager) return t;
        var v = EscapeManager._vars || {};
        return t.replace(/\{([^{}]+)\}/g, function(m, k) { return v[k] !== undefined ? String(v[k]) : m; });
    }

    Window_EscMessage.prototype.say = function(text, speaker, callback, waitInput) {
        text = escSub(text); speaker = escSub(speaker);
        this.resetFontSettings();
        var lines = wrapText(this.contents, text, this.contentsWidth() - 12);
        this._pages = [];
        for (var i = 0; i < lines.length; i += MSG_LINES) {
            this._pages.push(lines.slice(i, i + MSG_LINES));
        }
        if (this._pages.length === 0) this._pages.push(['']);
        this._callback = callback || null;
        this._waitInput = waitInput !== false;
        this._openFrame = Graphics.frameCount;
        this.startPage(!this._waitInput);
        this.open();
        if (this._nameWindow) this._nameWindow.setName(speaker || '', this);
    };

    Window_EscMessage.prototype.startPage = function(instant) {
        var page = this._pages[0] || [];
        this._total = page.join('').length;
        this._shown = instant ? this._total : 0;
        this.drawPage();
    };

    Window_EscMessage.prototype.drawPage = function() {
        this.contents.clear();
        this.resetFontSettings();
        var page = this._pages[0] || [];
        var left = this._shown;
        for (var i = 0; i < page.length && left > 0; i++) {
            var part = page[i].substring(0, left);
            left -= page[i].length;
            this.drawText(part, 6, i * this.lineHeight(), this.contentsWidth() - 12, 'left');
        }
    };

    Window_EscMessage.prototype.isTyping = function() {
        return this._shown < this._total;
    };

    Window_EscMessage.prototype.update = function() {
        Window_Base.prototype.update.call(this);
        if (!this.isOpen() || this._pages.length === 0) {
            this.pause = false;
            return;
        }
        if (this.isTyping()) {
            this._shown = Math.min(this._total, this._shown + 2);
            this.drawPage();
        }
        this.pause = this._waitInput && !this.isTyping();
        if (!this._waitInput) return;
        if (Graphics.frameCount === this._openFrame) return;
        if (Input.isTriggered('ok') || Input.isTriggered('cancel') ||
            TouchInput.isTriggered() || TouchInput.isCancelled()) {
            if (this.isTyping()) {
                this._shown = this._total;
                this.drawPage();
                return;
            }
            this._pages.shift();
            if (this._pages.length > 0) {
                this.startPage(false);
            } else {
                this.finish();
            }
        }
    };

    Window_EscMessage.prototype.finish = function() {
        this._pages = [];
        this._waitInput = false;
        this.pause = false;
        this.close();
        if (this._nameWindow) this._nameWindow.setName('', this);
        var cb = this._callback;
        this._callback = null;
        if (cb) cb();
    };

    Window_EscMessage.prototype.dismiss = function() {
        this._pages = [];
        this._waitInput = false;
        this._callback = null;
        this.pause = false;
        this.close();
        if (this._nameWindow) this._nameWindow.setName('', this);
    };

    //=========================================================================
    // Window_EscName - 말하는 사람 이름표
    //=========================================================================
    function Window_EscName() {
        this.initialize.apply(this, arguments);
    }
    Window_EscName.prototype = Object.create(Window_Base.prototype);
    Window_EscName.prototype.constructor = Window_EscName;

    Window_EscName.prototype.initialize = function() {
        Window_Base.prototype.initialize.call(this, 0, 0, 240, this.fittingHeight(1));
        this.openness = 0;
    };

    Window_EscName.prototype.standardFontSize = function() { return 22; };

    Window_EscName.prototype.setName = function(name, msgWindow) {
        if (!name) {
            this.close();
            return;
        }
        this.resetFontSettings();
        var w = Math.min(SW() - 40, Math.max(120, this.contents.measureTextWidth(name) + this.standardPadding() * 2 + 24));
        this.width = w;
        this.createContents();
        this.x = msgWindow.x + 8;
        this.y = msgWindow.y - this.height + 6;
        this.changeTextColor(this.textColor(6));
        this.drawText(name, 0, 0, this.contentsWidth(), 'center');
        this.open();
    };

    //=========================================================================
    // Window_EscChoice - 선택지(퀴즈)
    //=========================================================================
    function Window_EscChoice() {
        this.initialize.apply(this, arguments);
    }
    Window_EscChoice.prototype = Object.create(Window_Command.prototype);
    Window_EscChoice.prototype.constructor = Window_EscChoice;

    Window_EscChoice.prototype.initialize = function() {
        this._options = ['-'];
        Window_Command.prototype.initialize.call(this, 0, 0);
        this.openness = 0;
        this.deactivate();
    };

    Window_EscChoice.prototype.standardFontSize = function() { return 22; };
    Window_EscChoice.prototype.windowWidth = function() { return Math.min(720, SW() - 40); };
    Window_EscChoice.prototype.numVisibleRows = function() { return this._options.length; };

    Window_EscChoice.prototype.makeCommandList = function() {
        var marks = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧'];
        for (var i = 0; i < this._options.length; i++) {
            this.addCommand((marks[i] || (i + 1) + '.') + ' ' + this._options[i], 'choice' + i);
        }
    };

    Window_EscChoice.prototype.setup = function(options, bottomY) {
        this._options = options.slice(0, 8);
        this.width = this.windowWidth();
        this.height = this.fittingHeight(this._options.length);
        this.x = (SW() - this.width) / 2;
        this.y = Math.max(HUD_H + 4, bottomY - this.height - 44);
        this.refresh();
        this.select(0);
        this.open();
        this.activate();
        this._openFrame = Graphics.frameCount;
    };

    Window_EscChoice.prototype.onTouch = function(triggered) {
        var x = this.canvasToLocalX(TouchInput.x);
        var y = this.canvasToLocalY(TouchInput.y);
        var hit = this.hitTest(x, y);
        if (hit >= 0) {
            if (hit !== this.index()) {
                this.select(hit);
                SoundManager.playCursor();
            }
            if (triggered) this.processOk();
        }
    };

    //=========================================================================
    // Window_EscNumpad - 숫자 자물쇠
    //=========================================================================
    function Window_EscNumpad() {
        this.initialize.apply(this, arguments);
    }
    Window_EscNumpad.prototype = Object.create(Window_Selectable.prototype);
    Window_EscNumpad.prototype.constructor = Window_EscNumpad;

    var PAD_KEYS = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '지우기', '0', '확인'];
    var PAD_TOP = 74;

    Window_EscNumpad.prototype.initialize = function() {
        var w = 380;
        var h = this.standardPadding() * 2 + PAD_TOP + 4 * 52;
        Window_Selectable.prototype.initialize.call(this, (SW() - w) / 2, 0, w, h);
        this._digits = 4;
        this._value = '';
        this.openness = 0;
        this.deactivate();
        this.refresh();
    };

    Window_EscNumpad.prototype.standardFontSize = function() { return 24; };
    Window_EscNumpad.prototype.maxItems = function() { return PAD_KEYS.length; };
    Window_EscNumpad.prototype.maxCols = function() { return 3; };
    Window_EscNumpad.prototype.itemHeight = function() { return 52; };

    Window_EscNumpad.prototype.itemRect = function(index) {
        var rect = Window_Selectable.prototype.itemRect.call(this, index);
        rect.y += PAD_TOP;
        return rect;
    };

    Window_EscNumpad.prototype.setup = function(digits, bottomY) {
        this._digits = Math.max(1, Math.min(8, digits || 4));
        this._value = '';
        this.y = Math.max(HUD_H + 4, bottomY - this.height - 44);
        this.refresh();
        this.select(11);
        this.open();
        this.activate();
        this._openFrame = Graphics.frameCount;
    };

    Window_EscNumpad.prototype.value = function() { return this._value; };
    Window_EscNumpad.prototype.isFull = function() { return this._value.length >= this._digits; };

    Window_EscNumpad.prototype.addDigit = function(d) {
        if (this._value.length < this._digits) {
            this._value += d;
            SoundManager.playCursor();
            this.refresh();
        } else {
            SoundManager.playBuzzer();
        }
    };

    Window_EscNumpad.prototype.backspace = function() {
        if (this._value.length > 0) {
            this._value = this._value.slice(0, -1);
            SoundManager.playCancel();
            this.refresh();
        }
    };

    Window_EscNumpad.prototype.refresh = function() {
        if (!this.contents) return;
        this.contents.clear();
        this.resetFontSettings();
        var box = 40;
        var gap = 8;
        var total = this._digits * box + (this._digits - 1) * gap;
        var sx = (this.contentsWidth() - total) / 2;
        for (var i = 0; i < this._digits; i++) {
            var bx = sx + i * (box + gap);
            roundRect(this.contents, bx, 8, box, 52, 6, 'rgba(0,0,0,0.55)', 'rgba(255,224,160,0.9)', 2);
            this.contents.fontSize = 30;
            this.changeTextColor(this.textColor(0));
            this.contents.drawText(this._value[i] || '', bx, 8, box, 52, 'center');
        }
        this.resetFontSettings();
        this.drawAllItems();
    };

    Window_EscNumpad.prototype.drawItem = function(index) {
        var rect = this.itemRect(index);
        var key = PAD_KEYS[index];
        var fill = key === '확인' ? 'rgba(60,120,70,0.85)' : (key === '지우기' ? 'rgba(120,60,50,0.8)' : 'rgba(255,255,255,0.10)');
        roundRect(this.contents, rect.x + 3, rect.y + 3, rect.width - 6, rect.height - 6, 8, fill, 'rgba(255,255,255,0.25)', 1);
        this.resetFontSettings();
        if (key.length > 1) this.contents.fontSize = 20;
        this.contents.drawText(key, rect.x, rect.y, rect.width, rect.height, 'center');
    };

    Window_EscNumpad.prototype.onTouch = function(triggered) {
        var x = this.canvasToLocalX(TouchInput.x);
        var y = this.canvasToLocalY(TouchInput.y);
        var hit = this.hitTest(x, y);
        if (hit >= 0 && triggered) {
            this.select(hit);
            this.processOk();
        }
    };

    Window_EscNumpad.prototype.processOk = function() {
        var key = PAD_KEYS[this.index()];
        if (key === '지우기') {
            this.backspace();
        } else if (key === '확인') {
            this.updateInputData();
            this.callHandler('submit');
        } else if (key) {
            this.addDigit(key);
        }
    };

    //=========================================================================
    // Window_EscTiming - 타이밍 미니게임 (움직이는 바늘이 초록 칸에 왔을 때 누르기)
    //=========================================================================
    function Window_EscTiming() {
        this.initialize.apply(this, arguments);
    }
    Window_EscTiming.prototype = Object.create(Window_Base.prototype);
    Window_EscTiming.prototype.constructor = Window_EscTiming;
    Window_EscTiming.prototype.initialize = function() {
        var w = Math.min(600, SW() - 40), h = 228;
        Window_Base.prototype.initialize.call(this, (SW() - w) / 2, HUD_H + 70, w, h);
        this.openness = 0;
        this.active = false;
        this._handlers = {};
    };
    Window_EscTiming.prototype.setHandler = function(n, f) { this._handlers[n] = f; };
    Window_EscTiming.prototype.setup = function(def) {
        this._def = def;
        this._goal = Number(def.goal || 10);
        this._maxMiss = Number(def.maxMiss || 3);
        this._speed = Number(def.speed || 1.5);
        this._zoneW = Number(def.zone || 0.22);
        this._ok = 0; this._miss = 0; this._t = 0; this._pos = 0; this._dir = 1;
        this._flash = 0; this._flashOk = true; this._end = 0;
        this.newZone();
        this.open(); this.activate();
        this._openFrame = Graphics.frameCount;
        this.refresh();
    };
    Window_EscTiming.prototype.newZone = function() {
        this._zone = 0.08 + Math.random() * (0.84 - this._zoneW);
    };
    Window_EscTiming.prototype.update = function() {
        Window_Base.prototype.update.call(this);
        if (!this.active || !this.isOpen()) return;
        if (this._end > 0) {
            if (--this._end === 0) { var ok = this._ok >= this._goal; this.active = false; if (this._handlers.done) this._handlers.done(ok); }
            this.refresh();
            return;
        }
        this._pos += this._dir * this._speed / 90;
        if (this._pos > 1) { this._pos = 1; this._dir = -1; }
        if (this._pos < 0) { this._pos = 0; this._dir = 1; }
        if (this._flash > 0) this._flash--;
        if (this._openFrame !== Graphics.frameCount && Graphics.frameCount - this._openFrame > 8 &&
            (Input.isTriggered('ok') || TouchInput.isTriggered())) {
            var hit = this._pos >= this._zone && this._pos <= this._zone + this._zoneW;
            this._flash = 18; this._flashOk = hit;
            if (hit) {
                this._ok++;
                if (!playSafeSe(SE_ITEM, 70, 130)) SoundManager.playCursor();
                this.newZone();
                this._speed *= 1.04;
            } else {
                this._miss++;
                SoundManager.playBuzzer();
                $gameScreen.startShake(4, 10, 12);
            }
            if (this._ok >= this._goal || this._miss > this._maxMiss) this._end = 40;
        }
        this.refresh();
    };
    Window_EscTiming.prototype.refresh = function() {
        var c = this.contents; if (!c) return;
        c.clear();
        var w = this.contentsWidth(), def = this._def || {};
        c.fontSize = 22; this.changeTextColor('#ffe9b0');
        c.drawText(def.label || '타이밍', 0, 0, w, 32, 'center');
        c.fontSize = 18; this.resetTextColor();
        var per = Number(def.per || 1), unit = def.unit || '';
        c.drawText((def.countLabel || '완성') + ': ' + (this._ok * per) + ' / ' + (this._goal * per) + unit, 0, 34, w / 2, 26, 'left');
        // 소리(경계) 막대
        var mx = w / 2 + 10, mw = w / 2 - 10;
        c.drawText(def.missLabel || '소리', mx, 34, 50, 26, 'left');
        for (var i = 0; i < this._maxMiss + 1; i++) {
            var bx = mx + 52 + i * ((mw - 56) / (this._maxMiss + 1));
            c.fillRect(bx, 40, (mw - 56) / (this._maxMiss + 1) - 6, 16, i < this._miss ? '#ff6650' : 'rgba(255,255,255,0.2)');
        }
        // 막대
        var bx0 = 10, by = 78, bw = w - 20, bh = 40;
        c.fillRect(bx0, by, bw, bh, 'rgba(0,0,0,0.5)');
        c.fillRect(bx0 + bw * this._zone, by, bw * this._zoneW, bh, 'rgba(90,220,120,0.85)');
        var cx = bx0 + bw * this._pos;
        c.fillRect(cx - 3, by - 8, 6, bh + 16, this._flash > 0 ? (this._flashOk ? '#9dffb0' : '#ff6650') : '#ffffff');
        c.fontSize = 18;
        var msg = this._end > 0 ? (this._ok >= this._goal ? (def.doneMsg || '완성!') : (def.failMsg || '소리가 너무 컸다...')) :
                  (this._flash > 0 ? (this._flashOk ? (def.hitMsg || '좋아!') : (def.missMsg || '덜컹! 소리가 났다')) : (def.hint || 'Enter · 클릭 · 톡: 초록 칸에서 누르기'));
        this.changeTextColor(this._flash > 0 && !this._flashOk ? '#ff9a8a' : '#ffffff');
        c.drawText(msg, 0, by + bh + 14, w, 28, 'center');
        this.resetTextColor();
    };

    //=========================================================================
    // Window_EscDial - 다이얼 자물쇠 (글자·방향·색깔 등)
    //=========================================================================
    function Window_EscDial() {
        this.initialize.apply(this, arguments);
    }
    Window_EscDial.prototype = Object.create(Window_Base.prototype);
    Window_EscDial.prototype.constructor = Window_EscDial;

    var DIAL_ARROW = 26;
    var DIAL_BOX = 54;
    var DIAL_GAP = 10;
    var DIAL_BTN = 40;

    Window_EscDial.prototype.initialize = function() {
        Window_Base.prototype.initialize.call(this, 0, 0, 300, 200);
        this.openness = 0;
        this._slots = [];
        this._values = [];
        this._labels = [];
        this._cursor = 0;
        this._handlers = {};
        this._openFrame = -1;
        this._slotW = 80;
        this._fontSize = 24;
        this.deactivate();
    };

    Window_EscDial.prototype.setHandler = function(name, fn) { this._handlers[name] = fn; };
    Window_EscDial.prototype.callHandler = function(name) {
        if (this._handlers[name]) this._handlers[name]();
    };

    Window_EscDial.prototype.titleH = function() { return this._title ? 34 : 0; };
    Window_EscDial.prototype.labelH = function() { return this.titleH() + (this._labels.length > 0 ? 28 : 0); };

    Window_EscDial.prototype.setup = function(slots, labels, bottomY, title) {
        this._title = title || '';
        this._slots = slots;
        this._labels = labels || [];
        this._values = slots.map(function() { return 0; });
        this._cursor = 0;
        var n = slots.length;
        var probe = this.contents;
        var widest = 0;
        this._fontSize = 24;
        var measure = function(fs) {
            probe.fontSize = fs;
            var w = 0;
            slots.forEach(function(list, i) {
                list.forEach(function(sym) { w = Math.max(w, probe.measureTextWidth(String(sym))); });
            });
            return w;
        };
        var labelW = 0;
        probe.fontSize = 16;
        this._labels.forEach(function(l) { labelW = Math.max(labelW, probe.measureTextWidth(String(l))); });
        var pad = this.standardPadding();
        var maxW = SW() - 24;
        for (var fs = 24; fs >= 16; fs -= 2) {
            widest = measure(fs);
            this._fontSize = fs;
            this._slotW = Math.max(64, widest + 26, Math.min(labelW + 10, 170));
            if (n * this._slotW + (n - 1) * DIAL_GAP + pad * 2 <= maxW) break;
        }
        var minW = 300;
        if (this._title) {
            probe.fontSize = 18;
            minW = Math.max(minW, Math.min(maxW, probe.measureTextWidth(this._title) + pad * 2 + 16));
        }
        this.width = Math.min(maxW, Math.max(minW, n * this._slotW + (n - 1) * DIAL_GAP + pad * 2));
        this.height = pad * 2 + this.labelH() + DIAL_ARROW * 2 + DIAL_BOX + 12 + DIAL_BTN;
        this.x = (SW() - this.width) / 2;
        this.y = Math.max(HUD_H + 4, bottomY - this.height - 44);
        this.createContents();
        this.refresh();
        this.open();
        this.activate();
        this._openFrame = Graphics.frameCount;
    };

    Window_EscDial.prototype.values = function() {
        var self = this;
        return this._slots.map(function(list, i) { return String(list[self._values[i]]); });
    };

    Window_EscDial.prototype.slotX = function(i) {
        var n = this._slots.length;
        var total = n * this._slotW + (n - 1) * DIAL_GAP;
        return (this.contentsWidth() - total) / 2 + i * (this._slotW + DIAL_GAP);
    };

    Window_EscDial.prototype.btnRect = function() {
        var w = 140;
        var y = this.labelH() + DIAL_ARROW * 2 + DIAL_BOX + 12;
        return { x: (this.contentsWidth() - w) / 2, y: y, w: w, h: DIAL_BTN - 4 };
    };

    Window_EscDial.prototype.refresh = function() {
        var b = this.contents;
        b.clear();
        var n = this._slots.length;
        var top = this.labelH();
        if (this._title) {
            b.fontSize = 18;
            b.textColor = '#ffe9b0';
            b.drawText(this._title, 0, 0, this.contentsWidth(), 28, 'center');
        }
        for (var i = 0; i < n; i++) {
            var x = this.slotX(i);
            var sel = this._cursor === i;
            if (this._labels[i]) {
                b.fontSize = 16;
                b.textColor = this.systemColor();
                b.drawText(String(this._labels[i]), x - 6, this.titleH(), this._slotW + 12, 26, 'center');
            }
            var cx = x + this._slotW / 2;
            this.drawTriangle(cx, top + 4, true, sel);
            roundRect(b, x, top + DIAL_ARROW, this._slotW, DIAL_BOX, 8,
                'rgba(0,0,0,0.55)', sel ? 'rgba(255,214,120,1)' : 'rgba(255,224,160,0.55)', sel ? 3 : 2);
            b.fontSize = this._fontSize;
            b.textColor = '#ffffff';
            b.drawText(String(this._slots[i][this._values[i]]), x, top + DIAL_ARROW, this._slotW, DIAL_BOX, 'center');
            this.drawTriangle(cx, top + DIAL_ARROW + DIAL_BOX + 4, false, sel);
        }
        var r = this.btnRect();
        var on = this._cursor === n;
        roundRect(b, r.x, r.y, r.w, r.h, 8, on ? 'rgba(70,140,80,0.95)' : 'rgba(60,110,70,0.75)',
            on ? 'rgba(255,214,120,1)' : 'rgba(255,255,255,0.35)', on ? 3 : 1);
        b.fontSize = 20;
        b.textColor = '#ffffff';
        b.drawText('확인', r.x, r.y, r.w, r.h, 'center');
    };

    Window_EscDial.prototype.drawTriangle = function(cx, y, up, sel) {
        var ctx = ctxOf(this.contents);
        ctx.save();
        ctx.fillStyle = sel ? 'rgba(255,214,120,1)' : 'rgba(255,255,255,0.55)';
        ctx.beginPath();
        if (up) {
            ctx.moveTo(cx, y);
            ctx.lineTo(cx - 11, y + 16);
            ctx.lineTo(cx + 11, y + 16);
        } else {
            ctx.moveTo(cx, y + 16);
            ctx.lineTo(cx - 11, y);
            ctx.lineTo(cx + 11, y);
        }
        ctx.closePath();
        ctx.fill();
        ctx.restore();
        setDirty(this.contents);
    };

    Window_EscDial.prototype.turn = function(i, delta) {
        var len = this._slots[i].length;
        this._values[i] = (this._values[i] + delta + len) % len;
        SoundManager.playCursor();
        this.refresh();
    };

    Window_EscDial.prototype.update = function() {
        Window_Base.prototype.update.call(this);
        if (!this.active || !this.isOpen() || this._openFrame === Graphics.frameCount) return;
        var n = this._slots.length;
        if (Input.isRepeated('left')) {
            this._cursor = (this._cursor + n) % (n + 1);
            SoundManager.playCursor();
            this.refresh();
        } else if (Input.isRepeated('right')) {
            this._cursor = (this._cursor + 1) % (n + 1);
            SoundManager.playCursor();
            this.refresh();
        } else if (Input.isRepeated('up') && this._cursor < n) {
            this.turn(this._cursor, 1);
        } else if (Input.isRepeated('down') && this._cursor < n) {
            this.turn(this._cursor, -1);
        } else if (Input.isTriggered('ok')) {
            if (this._cursor === n) {
                this.callHandler('submit');
            } else {
                this._cursor++;
                SoundManager.playCursor();
                this.refresh();
            }
        } else if (Input.isTriggered('cancel') || TouchInput.isCancelled()) {
            SoundManager.playCancel();
            this.callHandler('cancel');
        } else if (escTappedOutside(this)) {
            SoundManager.playCancel();
            this.callHandler('cancel');
        } else if (TouchInput.isTriggered()) {
            this.onClick(this.canvasToLocalX(TouchInput.x) - this.padding, this.canvasToLocalY(TouchInput.y) - this.padding);
        }
    };

    Window_EscDial.prototype.onClick = function(x, y) {
        var top = this.labelH();
        var r = this.btnRect();
        if (x >= r.x && x < r.x + r.w && y >= r.y && y < r.y + r.h) {
            this._cursor = this._slots.length;
            this.refresh();
            this.callHandler('submit');
            return;
        }
        for (var i = 0; i < this._slots.length; i++) {
            var sx = this.slotX(i);
            if (x < sx - 4 || x >= sx + this._slotW + 4) continue;
            this._cursor = i;
            if (y >= top - 4 && y < top + DIAL_ARROW) {
                this.turn(i, 1);
            } else if (y >= top + DIAL_ARROW && y < top + DIAL_ARROW + DIAL_BOX) {
                this.turn(i, 1);
            } else if (y >= top + DIAL_ARROW + DIAL_BOX && y < top + DIAL_ARROW * 2 + DIAL_BOX + 4) {
                this.turn(i, -1);
            } else {
                this.refresh();
            }
            return;
        }
    };

    //=========================================================================
    // Window_EscBag - 가방 (힌트 + 모은 물건)
    //=========================================================================
    function Window_EscBag() {
        this.initialize.apply(this, arguments);
    }
    Window_EscBag.prototype = Object.create(Window_Selectable.prototype);
    Window_EscBag.prototype.constructor = Window_EscBag;

    Window_EscBag.prototype.initialize = function() {
        var w = 460;
        this._rows = [];
        this._icons = {};
        Window_Selectable.prototype.initialize.call(this, (SW() - w) / 2, 0, w, this.fittingHeight(2));
        this.openness = 0;
        this.deactivate();
    };

    Window_EscBag.prototype.standardFontSize = function() { return 22; };
    Window_EscBag.prototype.itemHeight = function() { return 52; };
    Window_EscBag.prototype.maxItems = function() { return this._rows.length; };
    Window_EscBag.prototype.titleHeight = function() { return 40; };

    Window_EscBag.prototype.itemRect = function(index) {
        var rect = Window_Selectable.prototype.itemRect.call(this, index);
        rect.y += this.titleHeight();
        return rect;
    };

    Window_EscBag.prototype.setup = function(rows, index) {
        this._rows = rows;
        var visible = Math.min(rows.length, 7);
        this.height = this.standardPadding() * 2 + this.titleHeight() + visible * this.itemHeight();
        this.y = Math.max(HUD_H + 6, (SH() - this.height) / 2 - 20);
        this.createContents();
        this.refresh();
        this.select(Math.min(index || 0, rows.length - 1));
        this.open();
        this.activate();
        this._openFrame = Graphics.frameCount;
    };

    Window_EscBag.prototype.currentRow = function() { return this._rows[this.index()]; };

    Window_EscBag.prototype.isCurrentItemEnabled = function() {
        var r = this.currentRow();
        return !!r && r.enabled !== false;
    };

    Window_EscBag.prototype.refresh = function() {
        if (!this.contents) return;
        this.contents.clear();
        this.resetFontSettings();
        this.changeTextColor(this.systemColor());
        this.drawText('가방', 0, 0, this.contentsWidth(), 'center');
        this.resetTextColor();
        this.drawAllItems();
    };

    Window_EscBag.prototype.drawItem = function(index) {
        var r = this._rows[index];
        var rect = this.itemRect(index);
        this.resetFontSettings();
        if (r.hint) {
            roundRect(this.contents, rect.x + 2, rect.y + 4, rect.width - 4, rect.height - 8, 8,
                r.enabled === false ? 'rgba(90,90,90,0.5)' : 'rgba(200,150,60,0.55)', null);
        }
        var tx = rect.x + 12;
        if (r.image) {
            var bmp = this._icons[r.image];
            if (!bmp) {
                bmp = ImageManager.loadPicture(r.image);
                this._icons[r.image] = bmp;
                bmp.addLoadListener(this.refresh.bind(this));
            }
            if (bmp.isReady() && bmp.width > 0) {
                var s = Math.min(40 / bmp.width, 40 / bmp.height);
                var dw = Math.floor(bmp.width * s);
                var dh = Math.floor(bmp.height * s);
                this.contents.blt(bmp, 0, 0, bmp.width, bmp.height, rect.x + 8 + (40 - dw) / 2, rect.y + (rect.height - dh) / 2, dw, dh);
            }
            tx = rect.x + 58;
        }
        this.changePaintOpacity(r.enabled !== false);
        this.contents.drawText(r.text, tx, rect.y, rect.width - (tx - rect.x) - 8, rect.height, 'left');
        this.changePaintOpacity(true);
    };

    Window_EscBag.prototype.onTouch = function(triggered) {
        var x = this.canvasToLocalX(TouchInput.x);
        var y = this.canvasToLocalY(TouchInput.y);
        var hit = this.hitTest(x, y);
        if (hit >= 0) {
            if (hit !== this.index()) {
                this.select(hit);
                SoundManager.playCursor();
            }
            if (triggered && this.isCurrentItemEnabled()) this.processOk();
        }
    };

    // 창이 열린 바로 그 프레임의 입력(ESC, 클릭)으로 다시 닫히지 않도록
    [Window_EscChoice, Window_EscNumpad, Window_EscBag].forEach(function(Klass) {
        var _processHandling = Klass.prototype.processHandling;
        Klass.prototype.processHandling = function() {
            if (this._openFrame === Graphics.frameCount) return;
            _processHandling.call(this);
        };
        var _processTouch = Klass.prototype.processTouch;
        Klass.prototype.processTouch = function() {
            if (this._openFrame === Graphics.frameCount) return;
            if (this.isOpenAndActive() && this.isCancelEnabled() && escTappedOutside(this)) {
                this.processCancel();
                return;
            }
            _processTouch.call(this);
        };
    });

    //=========================================================================
    // EscapeManager - 게임 진행을 관리합니다
    //=========================================================================
    EscapeManager = {
        _scene: null,

        reset: function() {
            this._data = $dataEscape;
            this._flags = {};
            this._items = [];
            this._visited = {};
            this._hintLevel = {};
            this._hintsLeft = Number((this._data && this._data.hints) || 0);
            this._hintsUsed = 0;
            this._timeLeft = Number((this._data && this._data.timeLimit) || 0);
            this._elapsed = 0;
            this._queue = [];
            this._waiting = false;
            this._waitCount = 0;
            this._waitTransfer = false;
            this._afterQueue = null;
            this._bagOpen = false;
            this._bagIndex = 0;
            this._phase = 'new';
            this._lastModalFrame = -1;
            this._boat = false;
            this._pendingBoat = undefined;
            this._chase = null;
            this._chaseMsg = false;
            this._goal = '';
            this._mission = null;
            this._vars = JSON.parse(JSON.stringify((this._data && this._data.vars) || {}));
            this._companionOverride = null;
            this._quizIndex = 0;
            this._caughtCount = 0;
            this._watch = null;
            this._started = true;
        },

        isActive: function() {
            return !!this._started && !!this._data;
        },

        hasError: function() {
            return !this._data || !!this._data.__error || (this._errors && this._errors.length > 0);
        },

        // --- 방과 조사 지점 -------------------------------------------------
        rooms: function() {
            return toArray(this._data && this._data.rooms);
        },

        roomById: function(id) {
            var list = this.rooms();
            for (var i = 0; i < list.length; i++) {
                if (list[i].id === id) return list[i];
            }
            return null;
        },

        roomForMap: function(mapId) {
            var list = this.rooms();
            for (var i = 0; i < list.length; i++) {
                if (Number(list[i].map) === mapId) return list[i];
            }
            return null;
        },

        isRoomMap: function(mapId) {
            return this.isActive() && !this.hasError() && !!this.roomForMap(mapId);
        },

        currentRoom: function() {
            return $gameMap ? this.roomForMap($gameMap.mapId()) : null;
        },

        hotspotById: function(room, id) {
            if (!room || !id) return null;
            var list = toArray(room.hotspots);
            for (var i = 0; i < list.length; i++) {
                if (list[i].id === id) return list[i];
            }
            return null;
        },

        hotspotForEvent: function(event) {
            if (!this.isActive() || this.hasError()) return null;
            var data = event.event ? event.event() : null;
            if (!data) return null;
            return this.hotspotById(this.roomForMap($gameMap.mapId()), String(data.name).trim());
        },

        // --- 조건 -------------------------------------------------------------
        hasItem: function(id) {
            return this._items.indexOf(id) >= 0;
        },

        // --- 이어하기 (v3.6) : 브라우저에 저장 + 4자리 이어하기 번호 -------------------
        // 데이터 "progress": { "key": "저장 이름", "units": [{ "flag": "hall1", "flags": [...], "items": [...] }, ...],
        //                      "base": { "flags": [...] }, "keepItems": [...], "mult": 271, "add": 1357 }
        progressDef: function() { return (this._data && this._data.progress) || null; },
        progressMask: function() {
            var d = this.progressDef(), self = this, m = 0;
            if (!d) return 0;
            toArray(d.units).forEach(function(u, i) { if (self._flags[u.flag]) m |= (1 << i); });
            return m;
        },
        progressCodeOf: function(mask) {
            var d = this.progressDef(); if (!d || !mask) return '----';
            var n = (mask * Number(d.mult || 271) + Number(d.add || 1357)) % 10000;
            return ('000' + n).slice(-4);
        },
        progressDecode: function(code) {
            var d = this.progressDef(); if (!d) return 0;
            var max = (1 << toArray(d.units).length) - 1;
            for (var m = 1; m <= max; m++) if (this.progressCodeOf(m) === String(code)) return m;
            return 0;
        },
        progressRead: function() {
            var d = this.progressDef(); if (!d) return { mask: 0 };
            try {
                var v = JSON.parse(window.localStorage.getItem('escProgress_' + (d.key || 'game')) || 'null');
                return v && v.mask ? v : { mask: 0 };
            } catch (e) { return { mask: 0 }; }
        },
        progressWrite: function(mask) {
            var d = this.progressDef(); if (!d) return;
            var self = this;
            try {
                var k = 'escProgress_' + (d.key || 'game');
                if (!mask) { window.localStorage.removeItem(k); return; }
                var old = this.progressRead();
                var keep = toArray(d.keepItems).filter(function(it) { return self.hasItem(it) || (old.items || []).indexOf(it) >= 0; });
                window.localStorage.setItem(k, JSON.stringify({ mask: mask | (old.mask || 0), items: keep }));
            } catch (e) {}
        },
        // 저장된 관을 다시 채워 넣기 (조용히). 성공하면 true
        progressApply: function(mask, items) {
            var d = this.progressDef(), self = this;
            if (!d || !mask) return false;
            var addF = function(f) { self._flags[f] = true; };
            var addI = function(it) { if (!self.hasItem(it)) self._items.push(it); };
            toArray(d.base && d.base.flags).forEach(addF);
            toArray(d.units).forEach(function(u, i) {
                if (!(mask & (1 << i))) return;
                addF(u.flag); toArray(u.flags).forEach(addF); toArray(u.items).forEach(addI);
            });
            toArray(items).forEach(addI);
            this.progressWrite(this.progressMask());
            this.refreshHud(); this.applyCompanion();
            return true;
        },

        checkCond: function(c) {
            if (!c) return true;
            var self = this;
            var ok = true;
            toArray(c.flag).concat(toArray(c.flags)).forEach(function(f) { if (!self._flags[f]) ok = false; });
            toArray(c.noFlag).concat(toArray(c.noFlags)).forEach(function(f) { if (self._flags[f]) ok = false; });
            toArray(c.item).concat(toArray(c.items)).forEach(function(it) { if (!self.hasItem(it)) ok = false; });
            toArray(c.noItem).concat(toArray(c.noItems)).forEach(function(it) { if (self.hasItem(it)) ok = false; });
            if (c.boat !== undefined && !!c.boat !== !!self._boat) ok = false;
            if (c.progressSaved !== undefined && !!c.progressSaved !== (self.progressRead().mask > 0)) ok = false;
            return ok;
        },

        // --- 상태 -------------------------------------------------------------
        isBusy: function() {
            if (!this.isActive()) return false;
            if (this._phase === 'error' || this._phase === 'ending' || this._phase === 'done' || this._phase === 'new') return true;
            return this._queue.length > 0 || this._waiting || this._waitCount > 0 ||
                this._waitTransfer || this._bagOpen;
        },

        canInteract: function() {
            return this.isActive() && this._phase === 'play' && !this.isBusy();
        },

        // --- 장면 연결 --------------------------------------------------------
        onSceneStart: function(scene) {
            this._scene = scene;
            if (!this.isActive()) return;
            if (this._data.__error) {
                this._phase = 'error';
                scene.escShowError([this._data.__error]);
                return;
            }
            if (this._errors && this._errors.length > 0) {
                this._phase = 'error';
                scene.escShowError(this._errors);
                return;
            }
            this._waitTransfer = false;
            this.applyCompanion();
            this.applyRoomParallax();
            this.setupWatchers();
            var rmT = this.currentRoom();
            // v4.0: 같은 방으로 다시 들어올 때(들켜서 처음 자리로 등)는 지금 화면 색(밤·낮)을 그대로 둔다
            if (!rmT || rmT.id !== this._tintRoom) $gameScreen.startTint(rmT && rmT.tint ? toArray(rmT.tint) : [0, 0, 0, 0], 0);
            this._tintRoom = rmT ? rmT.id : null;
            scene.escRefreshHud();
            this.reportMissingEvents();
            var firstIntro = toArray(this._data.intro)[0];
            if (this._phase !== 'new' || !(firstIntro && firstIntro.movie && hasAsset('movie', firstIntro.movie))) {
                this.updateBgm();
            }
            if (this._phase === 'new') {
                this._phase = 'intro';
                this.runSteps(toArray(this._data.intro), function() {
                    this.hideCloseup();
                    this._phase = 'play';
                    this.refreshHud();
                    this.enterRoom();
                }.bind(this));
            } else {
                this.enterRoom();
            }
        },

        enterRoom: function() {
            var room = this.currentRoom();
            if (room && !this._visited[room.id] && this._scene && this._scene.escTitleCard && this._data.roomCards !== false && room.titleCard !== false) {
                this._scene.escTitleCard(room.name || room.id);
            }
            if (room && room.enter && !this._visited[room.id]) {
                this._visited[room.id] = true;
                if (this._queue.length > 0 || this._waiting) {
                    this.insertSteps(toArray(room.enter));
                } else {
                    this.runSteps(toArray(room.enter));
                }
            }
            if (room) this._visited[room.id] = true;
        },

        reportMissingEvents: function() {
            var room = this.currentRoom();
            if (!room) return;
            var names = {};
            $gameMap.events().forEach(function(ev) {
                names[String(ev.event().name).trim()] = true;
            });
            var missing = toArray(room.hotspots).filter(function(h) { return !names[h.id]; })
                .map(function(h) { return h.id; });
            if (missing.length > 0) {
                console.warn('EscapeRoom: 맵 ' + room.map + '번(' + room.id + ')에 이 이름의 이벤트가 없습니다: ' + missing.join(', '));
            }
            this._missing = missing;
        },

        refreshHud: function() {
            if (this._scene && this._scene.escRefreshHud) this._scene.escRefreshHud();
        },

        // --- 데이터 검사 -----------------------------------------------------
        validate: function() {
            var d = this._data;
            var errors = [];
            if (!Array.isArray(d.rooms) || d.rooms.length === 0) return ['rooms(방 목록)가 비어 있습니다.'];
            var roomIds = {};
            var mapIds = {};
            d.rooms.forEach(function(r) {
                roomIds[r.id] = true;
                if (!r.map) {
                    errors.push('방 "' + r.id + '"에 map(맵 번호)이 없습니다.');
                } else if (!$dataMapInfos[Number(r.map)]) {
                    errors.push('방 "' + r.id + '": ' + r.map + '번 맵이 프로젝트에 없습니다.');
                } else if (mapIds[r.map]) {
                    errors.push('방 "' + r.id + '"과 "' + mapIds[r.map] + '"이 같은 ' + r.map + '번 맵을 쓰고 있습니다.');
                }
                mapIds[r.map] = r.id;
            });
            var items = d.items || {};
            var check = function(steps, where) {
                toArray(steps).forEach(function(s) {
                    if (!s || typeof s !== 'object') return;
                    if (s.go && !roomIds[s.go]) errors.push(where + ': 없는 방 "' + s.go + '"(으)로 이동하려 합니다.');
                    toArray(s.give).concat(toArray(s.take)).forEach(function(it) {
                        if (!items[it]) errors.push(where + ': items에 없는 아이템 "' + it + '"');
                    });
                    if (s.dial) {
                        var ds = EscapeManager.dialSlots(s.dial);
                        var da = toArray(s.dial.answer).map(String);
                        if (da.length !== ds.length) errors.push(where + ': 다이얼 칸 수(' + ds.length + ')와 정답 개수(' + da.length + ')가 다릅니다.');
                        da.forEach(function(v, i) {
                            if (ds[i] && ds[i].indexOf(v) < 0) errors.push(where + ': 다이얼 ' + (i + 1) + '번째 칸에 정답 "' + v + '"이(가) 보기 목록에 없습니다.');
                        });
                    }
                    check(s.success, where);
                    check(s.fail, where);
                    check(s.cancel, where);
                });
            };
            var checkCond = function(c, where) {
                if (!c) return;
                toArray(c.item).concat(toArray(c.items), toArray(c.noItem), toArray(c.noItems)).forEach(function(it) {
                    if (!items[it]) errors.push(where + ': 조건에 쓴 아이템 "' + it + '"이(가) items에 없습니다.');
                });
            };
            if (d.startRoom && !roomIds[d.startRoom]) errors.push('startRoom "' + d.startRoom + '"이(가) 없습니다.');
            check(d.intro, '도입(intro)');
            d.rooms.forEach(function(r) {
                if (!r.start) errors.push('방 "' + r.id + '"에 start(도착 위치)가 없습니다.');
                check(r.enter, '방 "' + r.id + '"의 enter');
                var seen = {};
                toArray(r.hotspots).forEach(function(h) {
                    var where = '방 "' + r.id + '" > "' + h.id + '"';
                    if (!h.id) errors.push('방 "' + r.id + '"에 id가 없는 조사 지점이 있습니다.');
                    if (seen[h.id]) errors.push(where + ': 같은 id가 두 번 있습니다.');
                    seen[h.id] = true;
                    checkCond(h.when, where);
                    if (h.cases) {
                        toArray(h.cases).forEach(function(c) {
                            checkCond(c['if'], where);
                            check(c.steps, where);
                        });
                    } else {
                        check(h.steps, where);
                    }
                });
            });
            return errors;
        },

        // --- 새 게임 시작 위치 --------------------------------------------------
        startPosition: function() {
            if (this.hasError()) return null;
            var id = this._data.startRoom || this._data.rooms[0].id;
            var room = this.roomById(id);
            if (!room || !room.start) return null;
            var s = toArray(room.start);
            return { mapId: Number(room.map), x: Number(s[0]), y: Number(s[1]), d: toDir(s[2]) || 2 };
        },

        // --- 조사 ----------------------------------------------------------------
        triggerHotspot: function(h) {
            if (!this.canInteract()) return;
            if (!this.checkCond(h.when)) return;
            var steps = null;
            if (h.cases) {
                var cases = toArray(h.cases);
                for (var i = 0; i < cases.length; i++) {
                    if (this.checkCond(cases[i]['if'])) {
                        steps = cases[i].steps;
                        break;
                    }
                }
            } else {
                steps = h.steps;
            }
            if (!steps) steps = [{ text: '특별한 것은 없어 보인다.' }];
            $gameTemp.clearDestination();
            this.runSteps(toArray(steps), this.hideCloseup.bind(this));
        },

        // --- 단계 실행기 -----------------------------------------------------------
        runSteps: function(steps, onDone) {
            this._queue = toArray(steps).slice();
            this._afterQueue = onDone || null;
            this._waiting = false;
        },

        insertSteps: function(steps) {
            this._queue = toArray(steps).concat(this._queue);
        },

        resume: function() {
            this._waiting = false;
            this._lastModalFrame = Graphics.frameCount;
        },

        update: function(scene) {
            if (!this.isActive() || scene !== this._scene) return;
            if (this._phase === 'error' || this._phase === 'done') return;
            if (this._movie) {
                this.updateMovie();
                return;
            }
            this.updateTimer();
            if (this._chase) this.updateChase();
            if (this._mission) this.updateMission();
            this.updateWatchers();
            if (this._waitTransfer) return;
            if (this._waitCount > 0) {
                this._waitCount--;
            } else {
                while (!this._waiting && this._waitCount === 0 && !this._waitTransfer &&
                       this._queue.length > 0 && !scene.isBusy()) {
                    this.processStep(this._queue.shift());
                }
                if (!this._waiting && this._waitCount === 0 && !this._waitTransfer &&
                    this._queue.length === 0 && this._afterQueue) {
                    var cb = this._afterQueue;
                    this._afterQueue = null;
                    cb();
                }
            }
            // v4.0: 장면이 다 끝나 다시 걸을 수 있게 됐는데 확대 그림(카드)이 남아 있으면 닫기 (안전장치)
            if (this._phase === 'play' && !this.isBusy() && !this._afterQueue && !scene.isBusy() &&
                scene.escCloseupVisible && scene.escCloseupVisible()) {
                this._closeupIdle = (this._closeupIdle || 0) + 1;
                if (this._closeupIdle > 12) { this._closeupIdle = 0; this.hideCloseup(); }
            } else this._closeupIdle = 0;
        },

        updateTimer: function() {
            if (this._phase !== 'play') return;
            this._elapsed += 1 / 60;
            if (!this._data.timeLimit) return;
            var before = Math.ceil(this._timeLeft);
            this._timeLeft -= 1 / 60;
            if (Math.ceil(this._timeLeft) !== before) this.refreshHud();
            if (this._timeLeft <= 0) {
                this._timeLeft = 0;
                this.finishGame(false);
            }
        },

        processStep: function(s) {
            if (typeof s === 'string') s = { text: s };
            if (!s || typeof s !== 'object') return;
            var self = this;
            var scene = this._scene;

            if (s.picture) this.showCloseup(s.picture, s._maxScale);
            if (s.hidePicture) this.hideCloseup();
            if (s.se) playSafeSe(String(s.se), 90, 100);
            if (s.bgm !== undefined) this.playBgm(String(s.bgm || ''));
            if (s.effect) this.playEffect(s);
            if (s.give) {
                toArray(s.give).forEach(function(it) {
                    if (!self.hasItem(it)) self._items.push(it);
                    if (scene && scene.escItemPopup) scene.escItemPopup(it);
                });
                if (!playSafeSe(SE_ITEM, 90, 100)) SoundManager.playUseItem();
            }
            if (s.grant) toArray(s.grant).forEach(function(it) { if (!self.hasItem(it)) self._items.push(it); });     // v4.5: 알림 없이 아이템 넣기 (부 고르기)
            if (s.take) {
                toArray(s.take).forEach(function(it) {
                    var i = self._items.indexOf(it);
                    if (i >= 0) self._items.splice(i, 1);
                });
            }
            // v4.0: 같은 단계의 flag 를 먼저 세운 뒤 저장 (장 끝 번호가 한 장 늦게 나오던 문제)
            if (s.flag) toArray(s.flag).forEach(function(f) { self._flags[f] = true; });
            if (s.unflag) toArray(s.unflag).forEach(function(f) { delete self._flags[f]; });
            if (s.progressLoad) this.progressApply(this.progressRead().mask, this.progressRead().items);
            if (s.progressClear) this.progressWrite(null);
            if (s.progressSave) this.progressWrite(this.progressMask());
            if (s.progressSave || s.progressCode) this._vars.code = this.progressCodeOf(this.progressMask());
            if (s.solve) {
                toArray(s.solve).forEach(function(f) { self._flags[f] = true; });
                if (!playSafeSe(SE_SOLVE, 90, 100)) SoundManager.playRecovery();
                if (scene && scene.escSolveFx) scene.escSolveFx();
            }
            if (s.penalty) this.applyPenalty(Number(s.penalty));
            if (s._hintBonus) {
                this._hintsLeft++;
                this.refreshHud();
                var selfH = this;
                setTimeout(function() {}, 0);
                this._afterQueue = (function(prev) { return function() { if (prev) prev(); selfH.onHint(); }; })(this._afterQueue);
            }
            if (s.goal !== undefined) { this._goal = String(s.goal || ''); if (scene && scene.escRefreshGoal) scene.escRefreshGoal(); }
            if (s.boat !== undefined && !s.go) this.setBoat(!!s.boat);
            if (s.parallax) $gameMap.changeParallax(String(s.parallax), false, false, 0, 0);
            if (s.tint) $gameScreen.startTint(toArray(s.tint), Number(s.duration || 30));
            if (s.give || s.grant || s.take || s.solve || s.flag || s.unflag) { this.refreshHud(); this.applyCompanion(); }

            if (s.effect === 'gate') {
                this._waiting = true;
                scene.escStartGate(s, this.resume.bind(this));
                return;
            }
            if (s.lock) {
                this.startLock(s);
                return;
            }
            if (s.choice) {
                this.startChoice(s);
                return;
            }
            if (s.dial) {
                this.startDial(s);
                return;
            }
            if (s.movie) {
                if (this.startMovie(s)) return;
            }
            if (s.selectCharacter) {
                this.startSelectCharacter(s);
                return;
            }
            if (s.chase) {
                this.startChase(s.chase);
                return;
            }
            if (s.mission) {
                this.startMission(s.mission);
                return;
            }
            if (s.timing) {
                this.startTiming(s);
                return;
            }
            if (s.text !== undefined) {
                if (s.go || s.escape || s.wait) {
                    this.insertSteps([{ go: s.go, x: s.x, y: s.y, dir: s.dir, fade: s.fade, escape: s.escape, wait: s.wait, boat: s.boat }]);
                }
                this._waiting = true;
                scene._escMsg.say(s.text, s.speaker, this.resume.bind(this), true);
                if (s.openUrl) scene.escArmUrl(String(s.openUrl));
                return;
            }
            if (s.go) {
                this.startTransfer(s);
                return;
            }
            if (s.wait) {
                this._waitCount = Number(s.wait);
                return;
            }
            if (s.escape) {
                this.finishGame(true);
                return;
            }
        },

        // --- 배경 음악 --------------------------------------------------------------
        playBgm: function(name) {
            if (!name) {
                AudioManager.fadeOutBgm(1);
                return;
            }
            if (hasAsset('bgm', name)) {
                AudioManager.playBgm({ name: name, volume: 80, pitch: 100, pan: 0 });
            }
        },

        updateBgm: function() {
            var room = this.currentRoom();
            var name = (room && room.bgm) || this._data.bgm;
            if (name) this.playBgm(name);
        },

        // --- 영상 ------------------------------------------------------------------
        startMovie: function(s) {
            var name = String(s.movie);
            if (!hasAsset('movie', name)) return false;
            AudioManager.stopBgm();
            this._waiting = true;
            // 기본은 건너뛰기 없음. 단계 "skip": true 또는 데이터 "movieSkip": true 일 때만 건너뛸 수 있음
            this._movie = { frames: 0, canSkip: s.skip === true || (s.skip !== false && this._data.movieSkip === true) };
            Graphics._escVideoCancelled = false;
            if (Graphics._video) {
                Graphics._video.style.objectFit = 'contain';
                Graphics._video.style.background = '#000';
            }
            Graphics.playVideo('movies/' + encodeURIComponent(name) + videoExt());
            return true;
        },

        updateMovie: function() {
            var m = this._movie;
            m.frames++;
            var v = Graphics._video;
            var skip = m.canSkip && m.frames > 20 && (Input.isTriggered('ok') || Input.isTriggered('cancel') ||
                TouchInput.isTriggered() || TouchInput.isCancelled());
            var stalled = (m.frames > 150 && v && v.paused && !Graphics._videoLoading && v.currentTime === 0) ||
                (m.frames > 360 && v && (v.error || v.currentTime === 0));
            if ((skip || stalled) && Graphics.isVideoPlaying()) {
                if (v) { v.pause(); v.onerror = null; v.removeAttribute('src'); try { v.load(); } catch (e) {} }
                Graphics._escVideoCancelled = true;
                Graphics._videoLoading = false;
                Graphics._onVideoEnd();
            }
            if (m.frames > 10 && !Graphics.isVideoPlaying()) {
                this._movie = null;
                this.updateBgm();
                this.resume();
            }
        },

        // --- 효과 ------------------------------------------------------------------
        playEffect: function(s) {
            var scene = this._scene;
            var kind = String(s.effect);
            if (kind === 'door') {
                if (scene) scene.escFxDoor(s.target || 'exit');
                this._waitCount = Math.max(this._waitCount, Number(s.wait || 45));
            } else if (kind === 'flash') {
                var c = toArray(s.color).length === 4 ? s.color : [255, 255, 255, 200];
                $gameScreen.startFlash(c, Number(s.duration || 30));
            } else if (kind === 'shake') {
                $gameScreen.startShake(Number(s.power || 5), Number(s.speed || 8), Number(s.duration || 24));
            } else if (kind === 'firework') {
                if (scene) scene.escFirework(s.target);
                $gameScreen.startFlash([255, 250, 230, 110], 16);
                if (!playSafeSe(SE_SOLVE, 85, 110)) SoundManager.playRecovery();
            } else if (kind === 'sparkle') {
                if (scene) scene.escSparkleAt(s.target);
            } else if (kind === 'card') {
                if (scene) scene.escTitleCard(String(s.text || ''));
            }
        },

        wrongFx: function() {
            $gameScreen.startShake(5, 9, 18);
        },

        startTransfer: function(s) {
            var room = this.roomById(s.go);
            var start = toArray(room.start);
            var x = s.x !== undefined ? Number(s.x) : Number(start[0]);
            var y = s.y !== undefined ? Number(s.y) : Number(start[1]);
            var d = s.dir !== undefined ? toDir(s.dir) : (toDir(start[2]) || 0);
            this.hideCloseup();
            this._waitTransfer = true;
            $gameTemp.clearDestination();
            var white = s.fade === 'white';
            if (s.boat !== undefined) this._pendingBoat = !!s.boat;
            if (white) playSafeSe(SE_WARP, 80, 100);
            $gamePlayer.reserveTransfer(Number(room.map), x, y, d, white ? 1 : 0);
        },

        applyPenalty: function(sec) {
            if (this._data.timeLimit && this._timeLeft > 0) {
                this._timeLeft = Math.max(1, this._timeLeft - sec);
                this.refreshHud();
            }
        },

        // --- 자물쇠 ---------------------------------------------------------------
        startLock: function(s) {
            var self = this;
            var scene = this._scene;
            var lock = s.lock;
            var answer = String(lock.answer || '0000');
            var digits = Number(lock.digits || answer.length);
            this._waiting = true;
            scene._escMsg.say(lock.question || (digits + '자리 숫자를 입력하세요.'), s.speaker, null, false);
            var pad = scene._escNumpad;
            pad.setup(digits, scene._escMsg.y);
            pad.setHandler('ok', function() {});
            pad.setHandler('submit', function() {
                if (!pad.isFull()) {
                    SoundManager.playBuzzer();
                    pad.activate();
                    return;
                }
                var correct = lock.progress ? self.progressApply(self.progressDecode(pad.value())) : pad.value() === answer;
                pad.deactivate();
                pad.close();
                scene._escMsg.dismiss();
                if (correct) {
                    SoundManager.playOk();
                    self.insertSteps(toArray(s.success));
                } else {
                    SoundManager.playBuzzer();
                    self.wrongFx();
                    if (self._data.wrongPenalty) self.applyPenalty(Number(self._data.wrongPenalty));
                    self.insertSteps(s.fail ? toArray(s.fail) : [{ text: '딸깍... 열리지 않는다. 다시 생각해 보자.' }]);
                }
                self.resume();
            });
            pad.setHandler('cancel', function() {
                pad.deactivate();
                pad.close();
                scene._escMsg.dismiss();
                self.insertSteps(toArray(s.cancel));
                self.resume();
            });
        },

        // --- 다이얼 자물쇠 -----------------------------------------------------------
        dialSlots: function(d) {
            if (Array.isArray(d.slots)) {
                return d.slots.map(function(list) { return toArray(list).map(String); });
            }
            var syms = toArray(d.symbols).map(String);
            var n = Number(d.count || toArray(d.answer).length || 1);
            var out = [];
            for (var i = 0; i < n; i++) out.push(syms.slice());
            return out;
        },

        startDial: function(s) {
            var self = this;
            var scene = this._scene;
            var d = s.dial;
            var answer = toArray(d.answer).map(String);
            this._waiting = true;
            var win = scene._escDial;
            var question = d.question || '자물쇠를 돌려 맞춰 보자.';
            if (scene.escCloseupVisible()) {
                // 단서 그림을 보면서 풀 수 있도록: 다이얼은 화면 아래, 그림은 그 위로
                win.setup(this.dialSlots(d), d.labels, SH() + 36, question);
                scene.escFitCloseup(win.y - 6);
            } else {
                scene._escMsg.say(question, s.speaker, null, false);
                win.setup(this.dialSlots(d), d.labels, scene._escMsg.y);
            }
            win.setHandler('submit', function() {
                var vals = win.values();
                var correct = vals.length === answer.length && vals.every(function(v, i) { return v === answer[i]; });
                win.deactivate();
                win.close();
                scene._escMsg.dismiss();
                if (correct) {
                    SoundManager.playOk();
                    self.insertSteps(toArray(s.success));
                } else {
                    SoundManager.playBuzzer();
                    self.wrongFx();
                    if (self._data.wrongPenalty) self.applyPenalty(Number(self._data.wrongPenalty));
                    self.insertSteps(s.fail ? toArray(s.fail) : [{ text: '철컥... 맞지 않는다. 다시 생각해 보자.' }]);
                }
                self.resume();
            });
            win.setHandler('cancel', function() {
                win.deactivate();
                win.close();
                scene._escMsg.dismiss();
                self.insertSteps(toArray(s.cancel));
                self.resume();
            });
        },

        // --- 주인공 고르기 -----------------------------------------------------------
        characters: function() {
            return toArray(this._data && this._data.characters);
        },

        // --- 감시(잠행) ----------------------------------------------------------------
        setupWatchers: function() {
            var room = this.currentRoom();
            this._watch = null;
            if (!room || !room.watchers) return;
            var list = [];
            toArray(room.watchers).forEach(function(w) {
                var ev = $gameMap.events().filter(function(e) { return String(e.event().name).trim() === String(w.event); })[0];
                if (!ev) return;
                ev.setMoveSpeed(Number(w.speed || 3));
                ev.setThrough(false);
                list.push({ def: w, ev: ev, idx: 0, wait: 0, stuck: 0, home: [ev.x, ev.y, ev.direction()] });
            });
            this._watch = { list: list, cool: 0 };
        },

        watchActive: function() {
            var room = this.currentRoom();
            if (!this._watch || !room) return false;
            if (room.watchIf && !this.checkCond(room.watchIf)) return false;
            return true;
        },

        // 이벤트가 바라보는 쪽으로 퍼지는 시야 칸들
        sightTiles: function(w) {
            var ev = w.ev, d = ev.direction(), n = Number(w.def.sight || 4);
            var dx = d === 6 ? 1 : d === 4 ? -1 : 0, dy = d === 2 ? 1 : d === 8 ? -1 : 0;
            var tiles = [];
            var blocked = function(x, y) {
                if (!$gameMap.isValid(x, y)) return true;
                return $gameMap.regionId(x, y) === WALL_REGION;
            };
            for (var k = 1; k <= n; k++) {
                var cx = ev.x + dx * k, cy = ev.y + dy * k;
                if (blocked(cx, cy)) break;
                var spread = Math.min(1, Math.floor(k / 2));
                for (var s = -spread; s <= spread; s++) {
                    var tx = cx + (dy !== 0 ? s : 0), ty = cy + (dx !== 0 ? s : 0);
                    if (!blocked(tx, ty)) tiles.push([tx, ty]);
                }
            }
            return tiles;
        },

        updateWatchers: function() {
            if (!this._watch || this._phase !== 'play') return;
            var active = this.watchActive();
            var self = this;
            var frozen = this.isBusy() && !this._mission && !this._chase;
            this._watch.list.forEach(function(w) {
                if (!active || frozen || w.ev._erased || w.ev._escHidden) return;
                if (w.ev.isMoving()) return;
                if (w.wait > 0) { w.wait--; return; }
                var route = toArray(w.def.route);
                if (route.length === 0) {
                    // 제자리에서 두리번거리기
                    var dirs = toArray(w.def.look || [2, 4, 8, 6]);
                    w.idx = (w.idx + 1) % dirs.length;
                    w.ev.setDirection(Number(dirs[w.idx]));
                    w.wait = Number(w.def.wait || 70);
                    return;
                }
                var tgt = route[w.idx % route.length];
                if (w.ev.x === tgt[0] && w.ev.y === tgt[1]) {
                    w.idx = (w.idx + 1) % route.length;
                    w.wait = Number(w.def.wait || 40);
                    var nx = route[w.idx % route.length];
                    var d0 = w.ev.findDirectionTo(nx[0], nx[1]);
                    if (d0 > 0) w.ev.setDirection(d0);
                    return;
                }
                var d = w.ev.findDirectionTo(tgt[0], tgt[1]);
                if (d > 0) w.ev.moveStraight(d);
                // v4.0: 길이 막히면(사람·물건) 잠깐 기다렸다가 반대쪽으로 돌아서 계속 순찰
                if (d <= 0 || !w.ev.isMovementSucceeded()) {
                    w.stuck = (w.stuck || 0) + 1;
                    if (w.stuck > 2) { w.stuck = 0; w.idx = (w.idx + 1) % route.length; }
                    w.wait = 20;
                } else w.stuck = 0;
            });
            if (!active || this._watch.cool > 0) { if (this._watch.cool > 0) this._watch.cool--; return; }
            if ((this.isBusy() && !this._mission && !this._chase) || $gamePlayer.isTransferring() || this._waitTransfer) return;
            var px = $gamePlayer.x, py = $gamePlayer.y;
            for (var i = 0; i < this._watch.list.length; i++) {
                var w = this._watch.list[i];
                if (w.ev._erased || w.ev._escHidden) continue;
                var seen = this.sightTiles(w).some(function(t) { return t[0] === px && t[1] === py; });
                if (seen) { this.onCaught(w); return; }
            }
        },

        onCaught: function(w) {
            var room = this.currentRoom();
            this._watch.cool = 90;
            this._caughtCount++;
            SoundManager.playBuzzer();
            $gameScreen.startFlash([255, 40, 40, 160], 20);
            $gameScreen.startShake(6, 9, 18);
            if (w && w.ev) w.ev.turnTowardPlayer();
            if (this._mission) this._mission.caught = true;
            var cp = toArray(room.checkpoint || room.start);
            // v4.0: 경비병들도 처음 자리·처음 순찰 순서로 되돌린다 (들킨 뒤 한자리에 멈춰 있던 문제)
            this._watch.list.forEach(function(x) {
                x.ev.locate(x.home[0], x.home[1]); x.ev.setDirection(x.home[2]); x.idx = 0; x.wait = 100; x.stuck = 0; x.chasing = false;
            });
            this._watchGrace = 150;    // 다시 시작한 뒤 2.5초 동안은 들키지 않음
            var steps = toArray(room.caught || [{ text: '들켰다! 처음 자리로 돌아가자.' }]).slice();
            var again = [];
            if (this._mission) {
                var m = this._mission; this._mission = null;
                if (this._scene && this._scene.escRefreshChase) this._scene.escRefreshChase();
                this.resetMission(m);
                steps = steps.concat(toArray(m.def.fail || []));
                again = m.def.retry === false ? [] : [{ mission: m.def }];
            }
            steps.push({ go: room.id, x: Number(cp[0]), y: Number(cp[1]), dir: cp[2] || 'up' });
            steps = steps.concat(again);
            if (room.caughtPenalty) this.applyPenalty(Number(room.caughtPenalty));
            if (this._chase) return;
            this._waiting = false;
            this._queue = steps.concat(this._queue);
            if (!this._afterQueue) this._afterQueue = this.hideCloseup.bind(this);
        },

        // --- 미션 (제한 시간 안에 여러 사람에게 전하기) -------------------------------
        startMission: function(def) {
            var targets = toArray(def.targets).map(String);
            this._mission = { def: def, targets: targets, left: targets.slice(), frames: Math.round(Number(def.time || 60) * 60) };
            this.hideCloseup();
            this._waiting = true;
            $gameTemp.clearDestination();
            if (this._scene && this._scene.escRefreshChase) this._scene.escRefreshChase();
        },

        resetMission: function(m) {
            $gameMap.events().forEach(function(ev) {
                if (m.targets.indexOf(String(ev.event().name).trim()) >= 0) ev._escDelivered = false;
            });
        },

        missionTouch: function(ev) {
            var m = this._mission;
            if (!m) return false;
            var n = String(ev.event().name).trim();
            if (m.targets.indexOf(n) < 0) return false;
            if (m.left.indexOf(n) < 0) { if (this._scene) this._scene.escShowToast('이미 전했다'); return true; }
            m.left.splice(m.left.indexOf(n), 1);
            ev._escDelivered = true;
            if (ev.characterName()) ev.turnTowardPlayer();
            var scene = this._scene;
            if (scene) {
                var c = { x: ev.screenX(), y: ev.screenY() - 30 };
                scene.escBurst(c.x, c.y, 12, '255,236,150', 2);
                scene.escShowToast(String(m.def.doneText || '전했다!') + '  ' + (m.targets.length - m.left.length) + ' / ' + m.targets.length);
                scene.escRefreshChase();
            }
            if (!playSafeSe(SE_ITEM, 80, 110)) SoundManager.playOk();
            if (m.left.length === 0) this.endMission(true);
            return true;
        },

        updateMission: function() {
            var m = this._mission;
            if (!m || this._phase !== 'play') return;
            m.frames--;
            if (m.frames % 60 === 0 && this._scene && this._scene.escRefreshChase) this._scene.escRefreshChase();
            if (m.frames <= 0) this.endMission(false);
        },

        endMission: function(ok) {
            var m = this._mission;
            this._mission = null;
            if (this._scene && this._scene.escRefreshChase) this._scene.escRefreshChase();
            $gameTemp.clearDestination();
            if (ok) {
                this.insertSteps(toArray(m.def.success));
            } else {
                this.resetMission(m);
                var again = m.def.retry === false ? [] : [{ mission: m.def }];
                this.insertSteps(toArray(m.def.fail || [{ text: '시간이 다 되었다! 다시 해 보자.' }]).concat(again));
            }
            this.resume();
        },

        // --- 타이밍 미니게임 -------------------------------------------------------------
        startTiming: function(s) {
            var self = this, scene = this._scene, def = s.timing;
            this._waiting = true;
            if (s.text) scene._escMsg.say(s.text, s.speaker, null, false);
            var win = scene._escTiming;
            win.setup(def);
            win.setHandler('done', function(ok) {
                win.close(); win.deactivate();
                if (s.text) scene._escMsg.dismiss();
                self.insertSteps(toArray(ok ? def.success : def.fail));
                self.resume();
            });
        },

        // 방의 "parallax": [{ "if": 조건, "name": "!그림" }]  조건에 따라 원경 그림 바꾸기
        applyRoomParallax: function() {
            var room = this.currentRoom();
            if (!room || !room.parallax) return;
            var list = toArray(room.parallax);
            for (var i = 0; i < list.length; i++) {
                if (this.checkCond(list[i]['if'])) {
                    if ($gameMap.parallaxName() !== list[i].name) $gameMap.changeParallax(String(list[i].name), false, false, 0, 0);
                    return;
                }
            }
        },

        // --- 배 ---------------------------------------------------------------------
        setBoat: function(on) {
            this._boat = !!on;
            if ($gamePlayer) $gamePlayer.refresh();
        },

        // --- 동료 (따라다니는 캐릭터) ------------------------------------------------
        applyCompanion: function(noRefresh) {
            var c = this._data && this._data.companion;
            if (c && this._companionOverride) { var o = {}; Object.keys(c).forEach(function(k) { o[k] = c[k]; });
                Object.keys(this._companionOverride).forEach(function(k) { o[k] = this._companionOverride[k]; }, this); c = o; }
            if (!c || !$gameParty || !$gamePlayer) return;
            var id = Number(c.actor || 2);
            if (!$dataActors[id] && $dataActors[1]) {      // 데이터베이스에 그 배우가 없으면 1번을 복사해 만듦
                var base = JSON.parse(JSON.stringify($dataActors[1]));
                base.id = id;
                base.name = String(c.name || '동료');
                $dataActors[id] = base;
            }
            if (!$dataActors[id]) return;
            var want = !this._boat && (!c.flag || !!this._flags[c.flag]);
            var has = $gameParty._actors.indexOf(id) >= 0;
            if (want) {
                var a = $gameActors.actor(id);
                if (a.characterName() !== String(c.image)) a.setCharacterImage(String(c.image), Number(c.index || 0));
                if (!has) $gameParty._actors.push(id);
                $gamePlayer._followers.show();
            } else {
                $gamePlayer._followers.hide();
            }
            // 동료 말고 다른 파티원은 따라오지 않게
            var lead = $gameParty._actors[0];
            $gameParty._actors = $gameParty._actors.filter(function(a, i) { return i === 0 || (want && a === id); });
            if (!noRefresh) $gamePlayer.refresh();
            $gamePlayer._followers.refresh();
        },

        // --- 추격 -------------------------------------------------------------------
        startChase: function(def) {
            var targets = toArray(def.targets).map(String);
            var c = { def: def, targets: targets, left: targets.slice(), frames: Math.round(Number(def.time || 90) * 60),
                      speed: Number(def.speed || 4), start: {} };
            $gameMap.events().forEach(function(ev) {
                var n = String(ev.event().name).trim();
                if (targets.indexOf(n) >= 0) {
                    if (!c.start[n]) c.start[n] = [];
                    c.start[n].push([ev.eventId(), ev.event().x, ev.event().y]);
                    ev._erased = false;
                    ev.refresh();
                    ev.locate(ev.event().x, ev.event().y);
                    ev.setMoveSpeed(c.speed);
                    ev.setThrough(false);
                }
            });
            this._chase = c;
            this._waiting = true;
            $gameTemp.clearDestination();
            if (this._scene && this._scene.escRefreshChase) this._scene.escRefreshChase();
        },

        chaseEvents: function() {
            var c = this._chase;
            if (!c) return [];
            return $gameMap.events().filter(function(ev) {
                return !ev._erased && c.left.indexOf(String(ev.event().name).trim()) >= 0;
            });
        },

        updateChase: function() {
            var c = this._chase;
            var scene = this._scene;
            if (!c || this._phase !== 'play') return;
            if (scene && scene._escMsg && scene._escMsg.isOpenAndActive && scene._escMsg.visible && this._chaseMsg) return;
            c.frames--;
            var pl = $gamePlayer;
            var self = this;
            this.chaseEvents().forEach(function(ev) {
                var dist = Math.abs(ev._realX - pl._realX) + Math.abs(ev._realY - pl._realY);
                if (dist <= 1.05) {
                    self.chaseCatch(ev);
                    return;
                }
                if (ev.isMoving()) return;
                if (ev._escRest > 0) { ev._escRest--; return; }
                if (Math.random() < Number(c.def.pause || 0)) { ev._escRest = 6 + Math.floor(Math.random() * 10); return; }
                var dirs = [2, 4, 6, 8].filter(function(d) { return ev.canPass(ev.x, ev.y, d); });
                if (dirs.length === 0) return;
                var near = Math.abs(ev.x - pl.x) + Math.abs(ev.y - pl.y) <= Number(c.def.sight || 8);
                var pick;
                if (near && Math.random() < Number(c.def.smart || 0.8)) {
                    var best = -1;
                    dirs.forEach(function(d) {
                        var nx = $gameMap.roundXWithDirection(ev.x, d), ny = $gameMap.roundYWithDirection(ev.y, d);
                        var nd = Math.abs(nx - pl.x) + Math.abs(ny - pl.y);
                        // 막다른 곳은 피하기: 갈 수 있는 이웃이 많을수록 가산점
                        var free = [2, 4, 6, 8].filter(function(d2) { return ev.canPass(nx, ny, d2); }).length;
                        var score = nd * 10 + free * 3 + Math.random() * 4;
                        if (score > best) { best = score; pick = d; }
                    });
                } else if (near || Math.random() < 0.35) {
                    pick = dirs[Math.floor(Math.random() * dirs.length)];
                }
                if (pick) ev.moveStraight(pick);
            });
            if (c.frames % 60 === 0 && scene && scene.escRefreshChase) scene.escRefreshChase();
            if (c.left.length === 0) {
                this.endChase(true);
            } else if (c.frames <= 0) {
                this.endChase(false);
            }
        },

        chaseCatch: function(ev) {
            var c = this._chase;
            var n = String(ev.event().name).trim();
            var i = c.left.indexOf(n);
            if (i < 0) return;
            // 같은 이름 이벤트가 여러 개면 하나만 지움
            ev.erase();
            var still = $gameMap.events().some(function(e) { return !e._erased && String(e.event().name).trim() === n; });
            if (!still) c.left.splice(i, 1);
            var scene = this._scene;
            if (scene) {
                var p = { x: ev.screenX(), y: ev.screenY() - 24 };
                if (scene.escBurst) scene.escBurst(p.x, p.y, 14, '255,255,255', 2.4);
                var caught = c.targets.length - c.left.length;
                scene.escShowToast && scene.escShowToast(String(c.def.caughtText || '따라잡았다!') + '  ' + caught + ' / ' + c.targets.length);
                scene.escRefreshChase && scene.escRefreshChase();
            }
            if (!playSafeSe(SE_SOLVE, 80, 120)) SoundManager.playRecovery();
            $gameScreen.startFlash([255, 255, 255, 120], 12);
        },

        endChase: function(ok) {
            var c = this._chase;
            this._chase = null;
            if (this._scene && this._scene.escRefreshChase) this._scene.escRefreshChase();
            $gameTemp.clearDestination();
            if (ok) {
                this.insertSteps(toArray(c.def.success));
            } else {
                // 배들을 처음 자리로
                Object.keys(c.start).forEach(function(n) {
                    c.start[n].forEach(function(e) {
                        var ev = $gameMap.event(e[0]);
                        if (!ev) return;
                        ev._erased = false;
                        ev.refresh();
                        ev.locate(e[1], e[2]);
                    });
                });
                var again = c.def.retry === false ? [] : [{ chase: c.def }];
                this.insertSteps(toArray(c.def.fail || [{ text: '놓쳤다! 다시 쫓아가자.' }]).concat(again));
            }
            this.resume();
        },

        applyCharacter: function(c) {
            var actor = $gameParty.leader();
            if (!actor || !c || !c.image) return;
            actor.setCharacterImage(String(c.image), Number(c.index || 0));
            var self = this;
            if (c.flag) toArray(c.flag).forEach(function(f) { self._flags[f] = true; });
            if (c.vars) Object.keys(c.vars).forEach(function(k) { self._vars[k] = c.vars[k]; });
            if (c.companion) this._companionOverride = c.companion;
            this.applyCompanion(true);
            if (c.face) actor.setFaceImage(String(c.face), Number(c.faceIndex || 0));
            $gamePlayer.refresh();
        },

        startSelectCharacter: function(s) {
            var self = this;
            var scene = this._scene;
            var list = this.characters();
            if (list.length === 0) return;
            this._waiting = true;
            scene._escMsg.say(s.question || '누구로 시작할까요?', s.speaker, null, false);
            var win = scene._escChoice;
            win.setup(list.map(function(c) { return c.label || c.image; }), scene._escMsg.y);
            var handler = function() {
                var c = list[win.index()];
                win.deactivate();
                win.close();
                scene._escMsg.dismiss();
                self.applyCharacter(c);
                SoundManager.playOk();
                self.resume();
            };
            for (var i = 0; i < list.length; i++) win.setHandler('choice' + i, handler);
        },

        // --- 선택지 ---------------------------------------------------------------
        startChoice: function(s) {
            var self = this;
            var scene = this._scene;
            var options = toArray(s.choice);
            var answer = Number(s.answer || 0);
            this._waiting = true;
            scene._escMsg.say(s.question || '', s.speaker, null, false);
            var win = scene._escChoice;
            win.setup(options, scene._escMsg.y);
            var handler = function() {
                var picked = win.index() + 1;
                win.deactivate();
                win.close();
                scene._escMsg.dismiss();
                if (!answer) {
                    self.insertSteps(toArray(s['on' + picked]));
                } else if (picked === answer) {
                    SoundManager.playOk();
                    self.insertSteps(toArray(s.success));
                } else {
                    SoundManager.playBuzzer();
                    self.wrongFx();
                    if (self._data.wrongPenalty) self.applyPenalty(Number(self._data.wrongPenalty));
                    self.insertSteps(s.fail ? toArray(s.fail) : [{ text: '아니야... 다시 생각해 보자.' }]);
                }
                self.resume();
            };
            for (var i = 0; i < options.length; i++) {
                win.setHandler('choice' + i, handler);
            }
        },

        // --- 확대 그림 ------------------------------------------------------------
        showCloseup: function(name, maxScale) {
            if (this._scene) this._scene.escShowCloseup(name, maxScale);
        },

        hideCloseup: function() {
            if (this._scene) this._scene.escHideCloseup();
        },

        // --- 가방 ------------------------------------------------------------------
        bagRows: function() {
            var rows = [];
            var items = this._data.items || {};
            if (this._data.hints) {
                rows.push({ hint: true, text: '힌트 보기   (남은 횟수 ' + this._hintsLeft + '/' + this._data.hints + ')' });
            }
            this._items.forEach(function(id) {
                var info = items[id] || { name: id };
                rows.push({ item: id, text: info.name, image: info.image });
            });
            if (this._items.length === 0) rows.push({ text: '아직 모은 물건이 없다.', enabled: false });
            return rows;
        },

        openBag: function() {
            if (!this.canInteract()) return;
            var scene = this._scene;
            var self = this;
            var bag = scene._escBag;
            this._bagOpen = true;
            $gameTemp.clearDestination();
            SoundManager.playOk();
            bag.setup(this.bagRows(), this._bagIndex);
            bag.setHandler('ok', function() {
                var r = bag.currentRow();
                self._bagIndex = bag.index();
                bag.deactivate();
                bag.close();
                self._bagOpen = false;
                if (r.hint) {
                    self.onHint();
                } else if (r.item) {
                    self.showItem(r.item);
                }
            });
            bag.setHandler('cancel', function() {
                self._bagIndex = bag.index();
                bag.deactivate();
                bag.close();
                self._bagOpen = false;
                self.resume();
            });
        },

        showItem: function(id) {
            var info = (this._data.items || {})[id] || { name: id };
            var step = { text: info.desc || '', speaker: info.name };
            if (info.closeup || info.image) {
                step.picture = info.closeup || info.image;
                step._maxScale = info.closeup ? 1 : 2.5;
            }
            this.runSteps([step], function() {
                this.hideCloseup();
                this.openBagAfter = true;
            }.bind(this));
        },

        // --- 힌트 ------------------------------------------------------------------
        currentPuzzle: function() {
            var list = toArray(this._data.puzzles);
            var room = this.currentRoom(), rid = room ? room.id : '';
            var self = this, i, p;
            // v3.5: "rooms" 가 있으면 지금 방에 맞는 수수께끼부터
            for (i = 0; i < list.length; i++) {
                p = list[i];
                if (!this._flags[p.id] && p.rooms && toArray(p.rooms).indexOf(rid) >= 0 && this.checkCond(p['if'])) return p;
            }
            for (i = 0; i < list.length; i++) {
                p = list[i];
                if (!this._flags[p.id] && !p.rooms && this.checkCond(p['if'])) return p;
            }
            return null;
        },

        onHint: function() {
            if (!this._data.hints) return;
            var p = this.currentPuzzle();
            if (!p) {
                this.runSteps([{ speaker: '힌트', text: '이제 남은 수수께끼가 없어요. 출구를 찾아보세요!' }]);
                return;
            }
            var hints = toArray(p.hints);
            var level = this._hintLevel[p.id] || 0;
            if (level >= hints.length) {
                this.runSteps([{ speaker: '힌트 - ' + (p.name || p.id), text: hints[hints.length - 1] || '힌트가 없습니다.' }]);
                return;
            }
            if (this._hintsLeft <= 0) {
                var qz = toArray(this._data.hintQuizzes);
                if (this._quizIndex < qz.length) {
                    var q = qz[this._quizIndex++];
                    var self = this;
                    this.runSteps([
                        { speaker: '힌트', text: '힌트를 모두 썼어요. 역사 퀴즈를 맞히면 힌트를 하나 더 얻을 수 있어요!' },
                        { speaker: '역사 퀴즈', choice: q.choice, answer: q.answer, question: q.question,
                          success: [{ speaker: '역사 퀴즈', text: '정답! ' + (q.explain || '') + ' 힌트 1개를 얻었다.', se: '' }, { _hintBonus: true }],
                          fail: [{ speaker: '역사 퀴즈', text: '아쉬워요! ' + (q.explain || '') }] }]);
                    return;
                }
                SoundManager.playBuzzer();
                this.runSteps([{ speaker: '힌트', text: '힌트를 모두 사용했어요. 지금까지 모은 단서를 다시 살펴보세요.' }]);
                return;
            }
            this._hintsLeft--;
            this._hintsUsed++;
            this._hintLevel[p.id] = level + 1;
            this.refreshHud();
            SoundManager.playOk();
            this.runSteps([{ speaker: '힌트 ' + (level + 1) + ' - ' + (p.name || p.id), text: hints[level] }]);
        },

        // --- 끝내기 ----------------------------------------------------------------
        finishGame: function(success) {
            var scene = this._scene;
            this._phase = 'ending';
            this._queue = [];
            this._afterQueue = null;
            this._waiting = false;
            this._waitCount = 0;
            this._bagOpen = false;
            if (scene) scene.escCloseAll();
            this.hideCloseup();
            this.refreshHud();
            var ending = this._data.ending || {};
            var steps = [];
            if (success && this._data.endingBgm) {
                this.playBgm(this._data.endingBgm);
            } else if (!success) {
                AudioManager.fadeOutBgm(3);
            }
            if (success) {
                steps = steps.concat(toArray(ending.success));
                var used = Math.round(this._elapsed);
                var record = (this._data.recordTitle || '탈출 성공!') + '\n걸린 시간: ' + Math.floor(used / 60) + '분 ' + (used % 60) + '초';
                if (this._data.hints) record += '\n사용한 힌트: ' + this._hintsUsed + '개';
                var arch = toArray(this._data.archives);
                if (arch.length) {
                    var self2 = this;
                    record += '   ·   모은 사료: ' + arch.filter(function(a) { return self2.hasItem(a); }).length + ' / ' + arch.length + '장';
                }
                steps.push({ speaker: '기록', text: record });
            } else {
                steps = steps.concat(toArray(ending.fail || '시간이 다 되었습니다...'));
            }
            steps = steps.concat(toArray(ending.summary));
            var review = this._data.review;
            if (review && review.url) {
                steps.push({ picture: review.picture, speaker: review.speaker || '후기', openUrl: review.url,
                    text: review.text || '끝까지 함께해 줘서 고마워요! Enter나 클릭을 누르면 후기 페이지가 열려요.' });
            }
            this._queue = steps;
            this._afterQueue = function() {
                this._phase = 'done';
                this._started = false;
                if (this._scene) this._scene.fadeOutAll();
                SceneManager.goto(Scene_Title);
            }.bind(this);
        }
    };

    //=========================================================================
    // 새 게임: 시작 방으로, 동료는 숨기기
    //=========================================================================
    var _DataManager_setupNewGame = DataManager.setupNewGame;
    DataManager.setupNewGame = function() {
        _DataManager_setupNewGame.call(this);
        EscapeManager.reset();
        EscapeManager._errors = $dataEscape && !$dataEscape.__error ? EscapeManager.validate() : [];
        var pos = EscapeManager.startPosition();
        if (pos) {
            $gamePlayer.reserveTransfer(pos.mapId, pos.x, pos.y, pos.d, 0);
        }
        $gamePlayer.hideFollowers();
        var chars = EscapeManager.characters();
        if (chars.length > 0 && !EscapeManager.hasError()) EscapeManager.applyCharacter(chars[0]);
    };

    //=========================================================================
    // 이동 제한 / 벽 리전
    //=========================================================================
    var _Game_Player_canMove = Game_Player.prototype.canMove;
    Game_Player.prototype.canMove = function() {
        if (EscapeManager.isActive() && (EscapeManager._chase || EscapeManager._mission) && !EscapeManager._chaseMsg) return _Game_Player_canMove.call(this);
        if (EscapeManager.isActive() && EscapeManager.isBusy()) return false;
        return _Game_Player_canMove.call(this);
    };

    var _Game_Map_isPassable = Game_Map.prototype.isPassable;
    Game_Map.prototype.isPassable = function(x, y, d) {
        if (EscapeManager.isRoomMap(this.mapId())) {
            if (this.regionId(x, y) === WALL_REGION) return false;
            if (this.layeredTiles(x, y).every(function(t) { return t === 0; })) return true;
        }
        return _Game_Map_isPassable.call(this, x, y, d);
    };

    // 바다(배로만) / 부두(둘 다) 리전
    Game_CharacterBase.prototype.escIsBoat = function() { return false; };
    Game_Player.prototype.escIsBoat = function() { return !!(EscapeManager && EscapeManager._boat); };
    Game_Event.prototype.escIsBoat = function() {
        var c = EscapeManager && EscapeManager._chase;
        if (!(c && c.targets.indexOf(String(this.event().name).trim()) >= 0)) return false;
        var r = $gameMap.regionId(this.x, this.y);          // v4.0: 바다·부두에서 시작한 추격만 배로 움직임
        return r === SEA_REGION || r === DOCK_REGION;
    };
    var _Game_CharacterBase_isMapPassable = Game_CharacterBase.prototype.isMapPassable;
    Game_CharacterBase.prototype.isMapPassable = function(x, y, d) {
        if (EscapeManager.isRoomMap($gameMap.mapId())) {
            var x2 = $gameMap.roundXWithDirection(x, d);
            var y2 = $gameMap.roundYWithDirection(y, d);
            if (!$gameMap.isValid(x2, y2)) return false;
            var r = $gameMap.regionId(x2, y2);
            var boat = this.escIsBoat();
            if (r === WALL_REGION) return false;
            if (r === 4) return false;          // 낮은 울타리: 걸어서는 못 가지만 화살은 넘어감 (v3.4)
            if (r === SEA_REGION) return boat;
            if (r === DOCK_REGION) return true;
            if (boat) return false;
        }
        return _Game_CharacterBase_isMapPassable.call(this, x, y, d);
    };

    // 배를 타면 주인공 그림을 배로 (MV가 그림을 다시 그려도 유지)
    var _Game_Player_refresh = Game_Player.prototype.refresh;
    Game_Player.prototype.refresh = function() {
        _Game_Player_refresh.call(this);
        if (EscapeManager && EscapeManager.isActive && EscapeManager.isActive()) {
            if (EscapeManager._boat) {
                var bs = String(EscapeManager._data.boatSprite || '$boat');
                this.setImage(bs, 0);
                this._followers.hide();
                this._followers.refresh();
            } else {
                EscapeManager.applyCompanion(true);
            }
        }
    };
    var _Game_Player_realMoveSpeed = Game_Player.prototype.realMoveSpeed;
    Game_Player.prototype.realMoveSpeed = function() {
        var v = _Game_Player_realMoveSpeed.call(this);
        return (EscapeManager && EscapeManager._boat) ? v + 1 : v;
    };
    var _Game_Player_performTransfer = Game_Player.prototype.performTransfer;
    Game_Player.prototype.performTransfer = function() {
        var was = this.isTransferring();
        if (was && EscapeManager && EscapeManager._pendingBoat !== undefined) {
            EscapeManager._boat = EscapeManager._pendingBoat;
            EscapeManager._pendingBoat = undefined;
        }
        _Game_Player_performTransfer.call(this);
        if (was) this.refresh();
    };

    //=========================================================================
    // 이벤트 = 조사 지점
    //=========================================================================
    // 조사 지점의 "visible" 조건: 조건이 맞을 때만 보이고, 그 전에는 투명·통과
    var _Game_Event_update = Game_Event.prototype.update;
    Game_Event.prototype.update = function() {
        _Game_Event_update.call(this);
        if (!EscapeManager.isActive() || this._erased) return;
        var h = EscapeManager.hotspotForEvent(this);
        if (h && (h.follow !== undefined || h.followDelivered) && !this._escHidden && !this.isMoving() &&
            ((h.follow !== undefined && EscapeManager.checkCond(h.follow)) || (h.followDelivered && this._escDelivered))) {
            var ddx = Math.abs(this.x - $gamePlayer.x) + Math.abs(this.y - $gamePlayer.y);
            this.setThrough(true);
            this.setMoveSpeed(4);
            if (ddx > Number(h.followGap || 2)) this.moveTowardCharacter($gamePlayer);
        }
        if (h && h.visible !== undefined) {
            var show = EscapeManager.checkCond(h.visible);
            if (this._escHidden === undefined || this._escHidden === show) {
                this._escHidden = !show;
                this.setTransparent(!show);
                this.setThrough(!show);
            }
        }
    };
    var _Game_Event_isTriggerIn = Game_Event.prototype.isTriggerIn;
    Game_Event.prototype.isTriggerIn = function(triggers) {
        if (this._escHidden) return false;
        return _Game_Event_isTriggerIn.call(this, triggers);
    };

    var _Game_Event_isNormalPriority = Game_Event.prototype.isNormalPriority;
    Game_Event.prototype.isNormalPriority = function() {
        if (this._escHidden) return false;
        if (EscapeManager.hotspotForEvent(this)) return true;
        return _Game_Event_isNormalPriority.call(this);
    };

    // v4.1: 한 칸에 여러 사람이 겹치면(지나가는 행렬 등) 말 걸 대상을 고름
    //   미션 대상 > 목표(!) 대상 > 서 있는 사람 > 지나가는 사람
    function escEventScore(e) {
        var M = EscapeManager, h = M.hotspotForEvent(e);
        if (!h || e._escHidden || e._erased) return -1;
        var sc = 1;
        if (M._mission && toArray(M._mission.left).map(String).indexOf(h.id) >= 0) sc += 8;
        if (M.isGoalTarget && M.isGoalTarget(h)) sc += 4;
        if (!(M._walkers || []).some(function(w) { return w.ev === e && !w.done; })) sc += 2;
        return sc;
    }
    function escBestAt(x, y, fallback) {
        var best = fallback, bs = fallback ? escEventScore(fallback) : -1;
        $gameMap.eventsXy(x, y).forEach(function(e) { var sc = escEventScore(e); if (sc > bs) { best = e; bs = sc; } });
        return best;
    }
    var _Game_Event_start = Game_Event.prototype.start;
    Game_Event.prototype.start = function() {
        if (EscapeManager.isActive() && !this._escPicked) {
            var best = escBestAt(this.x, this.y, this);
            if (best !== this) { best._escPicked = true; best.start(); best._escPicked = false; return; }
        }
        if (EscapeManager.isActive() && EscapeManager._mission && EscapeManager.missionTouch(this)) return;
        var h = EscapeManager.hotspotForEvent(this);
        if (h) {
            if (this.characterName() && !this.isDirectionFixed() && EscapeManager.canInteract()) {
                this.turnTowardPlayer();
            }
            EscapeManager.triggerHotspot(h);
            return;
        }
        _Game_Event_start.call(this);
    };

    //=========================================================================
    // Scene_Map - 화면 요소 추가
    //=========================================================================
    var _Scene_Map_createDisplayObjects = Scene_Map.prototype.createDisplayObjects;
    Scene_Map.prototype.createDisplayObjects = function() {
        _Scene_Map_createDisplayObjects.call(this);
        if (!EscapeManager.isActive()) return;
        this.escCreateLayer();
        this._escMsg = new Window_EscMessage();
        this._escName = new Window_EscName();
        this._escMsg.setNameWindow(this._escName);
        this._escChoice = new Window_EscChoice();
        this._escNumpad = new Window_EscNumpad();
        this._escBag = new Window_EscBag();
        this._escDial = new Window_EscDial();
        this._escTiming = new Window_EscTiming();
        this.addWindow(this._escMsg);
        this.addWindow(this._escName);
        this.addWindow(this._escChoice);
        this.addWindow(this._escNumpad);
        this.addWindow(this._escBag);
        this.addWindow(this._escDial);
        this.addWindow(this._escTiming);
    };

    Scene_Map.prototype.escCreateLayer = function() {
        var at = this.getChildIndex(this._windowLayer);
        var add = function(sprite) { this.addChildAt(sprite, at++); }.bind(this);

        // 효과 층: 맵(캐릭터) 바로 위
        this._escFx = new Sprite();
        this.addChildAt(this._escFx, this.getChildIndex(this._spriteset) + 1);
        at = this.getChildIndex(this._windowLayer);
        this._escParticles = [];
        this._escOpenSprites = [];
        this._escOpenKey = null;

        this._escWhite = new Sprite(new Bitmap(SW(), SH()));
        this._escWhite.bitmap.fillAll('#fffaf0');
        this._escWhite.opacity = 0;
        add(this._escWhite);

        this._escCard = new Sprite(new Bitmap(SW(), 130));
        this._escCard.y = Math.floor(SH() * 0.28);
        this._escCard.opacity = 0;
        this._escCardT = 0;
        add(this._escCard);

        this._escToast = new Sprite(new Bitmap(360, 40));
        this._escToast.x = (SW() - 360) / 2;
        this._escToast.y = HUD_H + 8;
        this._escToast.opacity = 0;
        this._escToastT = 0;

        this._escDebug = new Sprite(new Bitmap(SW(), SH()));
        this._escDebug.visible = SHOW_DEBUG;
        add(this._escDebug);

        this._escTip = new Sprite(new Bitmap(300, 34));
        this._escTip.visible = false;
        this._escTipText = '';
        add(this._escTip);

        this._escDim = new Sprite(new Bitmap(SW(), SH()));
        this._escDim.bitmap.fillAll('rgba(0,0,0,0.6)');
        this._escDim.visible = false;
        add(this._escDim);

        this._escCloseup = new Sprite();
        this._escCloseup.anchor.x = 0.5;
        this._escCloseup.anchor.y = 0.5;
        this._escCloseup.x = SW() / 2;
        this._escCloseup.visible = false;
        add(this._escCloseup);

        this._escHud = new Sprite(new Bitmap(SW(), HUD_H));
        add(this._escHud);
        add(this._escToast);

        // 목표 안내 (왼쪽 위)
        this._escGoal = new Sprite(new Bitmap(520, 34));
        this._escGoal.x = 8;
        this._escGoal.y = HUD_H + 6;
        add(this._escGoal);
        this.escRefreshGoal();

        // 추격 안내 (가운데 위)
        this._escChase = new Sprite(new Bitmap(420, 44));
        this._escChase.x = (SW() - 420) / 2;
        this._escChase.y = HUD_H + 6;
        this._escChase.visible = false;
        add(this._escChase);
        this.escRefreshChase();

        this._escError = new Sprite();
        add(this._escError);

        // 감시 시야 (빨간 칸)
        this._escSight = new PIXI.Graphics();
        this._escFx.addChildAt(this._escSight, 0);

        // 찾아갈 곳 표시 (통통 튀는 화살표)
        this._escMarks = new Sprite();
        this._escFx.addChild(this._escMarks);
        this._escMarkKey = '';
        this._escMarkList = [];
        this.escArmFullButton();

        this._escDebugText = '';
    };

    var _Scene_Map_start = Scene_Map.prototype.start;
    Scene_Map.prototype.start = function() {
        _Scene_Map_start.call(this);
        if (EscapeManager.isActive()) {
            this.escInstallKeys();
            EscapeManager.onSceneStart(this);
        }
    };

    var _Scene_Map_terminate = Scene_Map.prototype.terminate;
    Scene_Map.prototype.terminate = function() {
        _Scene_Map_terminate.call(this);
        this.escRemoveKeys();
        if (this._escFullHandler) {
            var f = this._escFullHandler; this._escFullHandler = null;
            ['mousedown', 'touchend'].forEach(function(n) { document.removeEventListener(n, f, true); });
        }
    };

    Scene_Map.prototype.escArmFullButton = function() {
        if (this._escFullHandler || !FULL_BUTTON) return;
        var self = this;
        this._escFullHandler = function(ev) {
            if (SceneManager._scene !== self || !EscapeManager.isActive() || EscapeManager._phase !== 'play') return;
            var pt = ev.changedTouches && ev.changedTouches[0] ? ev.changedTouches[0] : ev;
            var x = Graphics.pageToCanvasX(pt.pageX), y = Graphics.pageToCanvasY(pt.pageY);
            var r = self.escButtonRects().filter(function(b) { return b.id === 'full'; })[0];
            if (r && x >= r.x && x < r.x + r.w && y >= r.y && y < r.y + r.h) {
                escToggleFullscreen();
                if (ev.cancelable) ev.preventDefault();
            }
        };
        ['mousedown', 'touchend'].forEach(function(n) { document.addEventListener(n, self._escFullHandler, true); });
    };

    // 브라우저는 사용자가 키를 누르거나 클릭한 순간에만 새 창을 허용하므로,
    // 그 순간(DOM 이벤트 안)에 링크를 엽니다.
    Scene_Map.prototype.escArmUrl = function(url) {
        this._escUrl = url;
        this._escUrlFrame = Graphics.frameCount;
    };

    Scene_Map.prototype.escTryOpenUrl = function() {
        if (!this._escUrl || !this._escMsg) return;
        if (Graphics.frameCount < this._escUrlFrame + 10) return;
        if (this._escMsg.isTyping()) return;
        var url = this._escUrl;
        this._escUrl = null;
        openExternal(url);
    };

    Scene_Map.prototype.escInstallKeys = function() {
        var self = this;
        this._escGesture = function(e) {
            if (SceneManager._scene !== self) return;
            if (e.type === 'keydown' && ['Enter', ' ', 'z', 'Z'].indexOf(e.key) < 0) return;
            if (e.type === 'mousedown' && e.button !== 0) return;
            self.escTryOpenUrl();
        };
        document.addEventListener('keydown', this._escGesture);
        document.addEventListener('mousedown', this._escGesture);
        document.addEventListener('touchend', this._escGesture);
        this._escKey = function(e) {
            if (!SceneManager._scene || SceneManager._scene !== self) return;
            if (self._escNumpad && self._escNumpad.active) {
                var k = e.key;
                if (k && k.length === 1 && k >= '0' && k <= '9') {
                    self._escNumpad.addDigit(k);
                    e.preventDefault();
                } else if (k === 'Backspace') {
                    self._escNumpad.backspace();
                    e.preventDefault();
                }
                return;
            }
            if ((e.key === 'h' || e.key === 'H' || e.key === 'ㅗ') && EscapeManager.canInteract()) {
                EscapeManager.onHint();
            }
        };
        this._escMouse = function(e) {
            var x = Graphics.pageToCanvasX(e.pageX);
            var y = Graphics.pageToCanvasY(e.pageY);
            var b = self.escButtonAt(x, y);
            document.body.style.cursor = b && EscapeManager.canInteract() ? 'pointer' : '';
        };
        document.addEventListener('keydown', this._escKey);
        document.addEventListener('mousemove', this._escMouse);
    };

    Scene_Map.prototype.escRemoveKeys = function() {
        if (this._escKey) document.removeEventListener('keydown', this._escKey);
        if (this._escMouse) document.removeEventListener('mousemove', this._escMouse);
        if (this._escGesture) {
            document.removeEventListener('keydown', this._escGesture);
            document.removeEventListener('mousedown', this._escGesture);
            document.removeEventListener('touchend', this._escGesture);
        }
        document.body.style.cursor = '';
    };

    var _Scene_Map_update = Scene_Map.prototype.update;
    Scene_Map.prototype.update = function() {
        _Scene_Map_update.call(this);
        if (escResize.pending && escMapResizeSafe(this)) {
            escApplyWidth(escResize.pending);
            $gamePlayer.center($gamePlayer.x, $gamePlayer.y);
            SceneManager.goto(Scene_Map);
            return;
        }
        if (!EscapeManager.isActive() || !this._escHud) return;
        EscapeManager.update(this);
        if (EscapeManager.openBagAfter && EscapeManager.canInteract()) {
            EscapeManager.openBagAfter = false;
            EscapeManager.openBag();
        }
        this.escUpdateTip();
        this.escUpdateFx();
        if (SHOW_DEBUG) this.escUpdateDebug();
    };

    // 가방 열기 (메뉴 대신)
    var _Scene_Map_isMenuEnabled = Scene_Map.prototype.isMenuEnabled;
    Scene_Map.prototype.isMenuEnabled = function() {
        if (EscapeManager.isActive()) return EscapeManager.canInteract() && !$gameMap.isEventRunning();
        return _Scene_Map_isMenuEnabled.call(this);
    };

    var _Scene_Map_callMenu = Scene_Map.prototype.callMenu;
    Scene_Map.prototype.callMenu = function() {
        if (EscapeManager.isActive()) {
            this.menuCalling = false;
            EscapeManager.openBag();
            return;
        }
        _Scene_Map_callMenu.call(this);
    };

    // 위쪽 버튼 클릭
    Scene_Map.prototype.escButtonRects = function() {
        var rects = [];
        var right = SW() - 8;
        if (EscapeManager._data && EscapeManager._data.hints) {
            rects.push({ id: 'hint', x: right - 118, y: 5, w: 118, h: HUD_H - 10 });
            right -= 126;
        }
        rects.push({ id: 'bag', x: right - 92, y: 5, w: 92, h: HUD_H - 10 });
        right -= 100;
        if (FULL_BUTTON && escCanFullscreen(true)) rects.push({ id: 'full', x: right - 96, y: 5, w: 96, h: HUD_H - 10 });
        return rects;
    };

    Scene_Map.prototype.escButtonAt = function(x, y) {
        if (!EscapeManager.isActive() || EscapeManager._phase !== 'play') return null;
        var list = this.escButtonRects();
        for (var i = 0; i < list.length; i++) {
            var r = list[i];
            if (x >= r.x && x < r.x + r.w && y >= r.y && y < r.y + r.h) return r.id;
        }
        return null;
    };

    var _Scene_Map_processMapTouch = Scene_Map.prototype.processMapTouch;
    Scene_Map.prototype.processMapTouch = function() {
        if (EscapeManager.isActive() && TouchInput.isTriggered() && TouchInput.y < HUD_H) {
            var b = this.escButtonAt(TouchInput.x, TouchInput.y);
            if (b === 'bag') EscapeManager.openBag();
            if (b === 'hint' && EscapeManager.canInteract()) EscapeManager.onHint();
            this._touchCount = 0;
            return;
        }
        _Scene_Map_processMapTouch.call(this);
    };

    // --- 상단 표시줄 ---------------------------------------------------------
    Scene_Map.prototype.escRefreshHud = function() {
        if (!this._escHud) return;
        var M = EscapeManager;
        var bmp = this._escHud.bitmap;
        bmp.clear();
        if (M._phase === 'error') return;
        var ctx = ctxOf(bmp);
        var g = ctx.createLinearGradient(0, 0, 0, HUD_H);
        g.addColorStop(0, 'rgba(10,8,6,0.82)');
        g.addColorStop(1, 'rgba(10,8,6,0.45)');
        ctx.fillStyle = g;
        ctx.fillRect(0, 0, SW(), HUD_H);
        setDirty(bmp);
        var room = M.currentRoom();
        bmp.fontSize = 20;
        bmp.textColor = '#ffe9b0';
        bmp.drawText(room ? (room.name || room.id) : '', 14, 0, 330, HUD_H, 'left');
        if (M._data.timeLimit && M._phase !== 'intro' && M._phase !== 'new') {
            var sec = M._timeLeft;
            bmp.textColor = sec <= 60 ? '#ff7a6a' : '#ffffff';
            bmp.fontSize = 22;
            bmp.drawText('⏱ ' + formatTime(sec), SW() / 2 - 60, 0, 120, HUD_H, 'center');
        }
        if (M._phase === 'play') {
            var self = this;
            this.escButtonRects().forEach(function(r) {
                var label = r.id === 'bag' ? '가방 (' + M._items.length + ')' : r.id === 'full' ? (escIsFullscreen() ? '창 모드' : '전체 화면') : '힌트 ' + M._hintsLeft + '/' + M._data.hints;
                var fill = r.id === 'hint' ? (M._hintsLeft > 0 ? 'rgba(196,140,52,0.95)' : 'rgba(90,90,90,0.85)') : r.id === 'full' ? 'rgba(60,110,90,0.95)' : 'rgba(70,96,120,0.95)';
                roundRect(bmp, r.x, r.y, r.w, r.h, 8, fill, 'rgba(255,255,255,0.45)', 1);
                bmp.fontSize = 18;
                bmp.textColor = '#ffffff';
                bmp.drawText(label, r.x, r.y, r.w, r.h, 'center');
            });
            self = null;
        }
    };

    // --- 바라보는 물건 이름표 --------------------------------------------------
    Scene_Map.prototype.escFacingEvent = function() {
        var p = $gamePlayer;
        var x = $gameMap.roundXWithDirection(p.x, p.direction());
        var y = $gameMap.roundYWithDirection(p.y, p.direction());
        var list = $gameMap.eventsXy(x, y).slice().sort(function(a, b) { return escEventScore(b) - escEventScore(a); });
        for (var i = 0; i < list.length; i++) {
            if (list[i]._escHidden || list[i]._erased) continue;
            var h = EscapeManager.hotspotForEvent(list[i]);
            if (h && EscapeManager.checkCond(h.when)) return { event: list[i], hotspot: h };
        }
        return null;
    };

    Scene_Map.prototype.escUpdateTip = function() {
        var f = null;
        if (EscapeManager.canInteract() && !$gamePlayer.isMoving()) f = this.escFacingEvent();
        var label = f ? (f.hotspot.label || f.hotspot.id) : '';
        if (label !== this._escTipText) {
            this._escTipText = label;
            var bmp = this._escTip.bitmap;
            bmp.clear();
            if (label) {
                bmp.fontSize = 18;
                var text = label + '  [조사]';
                var w = Math.min(296, bmp.measureTextWidth(text) + 24);
                roundRect(bmp, 2, 2, w, 28, 14, 'rgba(20,14,8,0.85)', 'rgba(255,224,160,0.85)', 1);
                bmp.textColor = '#ffe9b0';
                bmp.drawText(text, 14, 2, w - 24, 28, 'left');
                this._escTipW = w;
            }
        }
        this._escTip.visible = !!label;
        if (f) {
            var ex = f.event.screenX();
            var ey = f.event.screenY() - 64;
            this._escTip.x = Math.max(4, Math.min(SW() - this._escTipW - 4, ex - this._escTipW / 2));
            this._escTip.y = Math.max(HUD_H + 2, ey);
        }
    };

    // =========================================================================
    // 효과 (FX)
    // =========================================================================
    Scene_Map.prototype.escTileCenter = function(x, y) {
        var tw = $gameMap.tileWidth();
        var th = $gameMap.tileHeight();
        return { x: $gameMap.adjustX(x) * tw + tw / 2, y: $gameMap.adjustY(y) * th + th / 2 };
    };

    Scene_Map.prototype.escHotspotEvents = function(id) {
        return $gameMap.events().filter(function(ev) { return String(ev.event().name).trim() === id; });
    };

    Scene_Map.prototype.escHotspotCenter = function(id) {
        var list = this.escHotspotEvents(id);
        if (list.length === 0) return null;
        var sx = 0, sy = 0, self = this;
        list.forEach(function(ev) {
            var c = self.escTileCenter(ev.x, ev.y);
            sx += c.x; sy += c.y;
        });
        return { x: sx / list.length, y: sy / list.length, n: list.length };
    };

    Scene_Map.prototype.escPlayerPos = function() {
        return { x: $gamePlayer.screenX(), y: $gamePlayer.screenY() - 24 };
    };

    Scene_Map.prototype.escSpawn = function(o) {
        var sp = new Sprite(o.bitmap);
        sp.anchor.x = 0.5;
        sp.anchor.y = 0.5;
        sp.x = o.x;
        sp.y = o.y;
        sp.blendMode = o.blend === false ? 0 : 1;
        sp.scale.x = sp.scale.y = o.scale || 1;
        this._escFx.addChild(sp);
        this._escParticles.push({ sp: sp, vx: o.vx || 0, vy: o.vy || 0, life: o.life || 40, max: o.life || 40,
            ds: o.ds || 0, g: o.g || 0, tx: o.tx, ty: o.ty, spin: o.spin || 0, alpha: o.alpha || 255 });
        return sp;
    };

    Scene_Map.prototype.escBurst = function(x, y, n, rgb, speed) {
        for (var i = 0; i < n; i++) {
            var a = Math.random() * Math.PI * 2;
            var v = (speed || 3) * (0.4 + Math.random());
            this.escSpawn({ bitmap: fxSpark(rgb || '255,220,120'), x: x, y: y, vx: Math.cos(a) * v, vy: Math.sin(a) * v - 1,
                life: 30 + Math.floor(Math.random() * 25), ds: -0.012, scale: 0.6 + Math.random() * 0.8, g: 0.04, spin: 0.1 });
        }
    };

    Scene_Map.prototype.escFxDoor = function(target) {
        var c = this.escHotspotCenter(target);
        if (!c) c = this.escPlayerPos();
        if (!playSafeSe(SE_DOOR, 90, 100)) SoundManager.playOk();
        $gameScreen.startFlash([255, 240, 200, 150], 24);
        var ring = this.escSpawn({ bitmap: fxGlow(160, '255,236,170'), x: c.x, y: c.y, life: 45, ds: 0.05, scale: 0.4 });
        ring.opacity = 255;
        this.escBurst(c.x, c.y, 34, '255,226,140', 4);
        this._escOpenKey = null;
    };

    Scene_Map.prototype.escSolveFx = function() {
        var p = this.escPlayerPos();
        for (var i = 0; i < 14; i++) {
            this.escSpawn({ bitmap: fxSpark('255,236,150'), x: p.x + (Math.random() - 0.5) * 50, y: p.y + 10 + Math.random() * 20,
                vx: (Math.random() - 0.5) * 0.6, vy: -1.2 - Math.random() * 1.4, life: 50 + Math.floor(Math.random() * 20),
                scale: 0.5 + Math.random() * 0.6, ds: -0.006, spin: 0.08 });
        }
        this.escSpawn({ bitmap: fxGlow(120, '255,240,180'), x: p.x, y: p.y, life: 40, ds: 0.03, scale: 0.5 });
    };

    Scene_Map.prototype.escFirework = function(target) {
        var c = target ? this.escHotspotCenter(target) : null;
        if (!c) c = this.escPlayerPos();
        var cols = ['255,214,90', '120,220,255', '255,130,170', '170,255,150', '255,255,255'];
        for (var k = 0; k < 5; k++) {
            var ox = (k === 0) ? 0 : (Math.random() - 0.5) * 120, oy = (k === 0) ? -10 : -30 - Math.random() * 60;
            this.escBurst(c.x + ox, c.y + oy, k === 0 ? 30 : 16, cols[k], k === 0 ? 3.4 : 2.4);
        }
        this.escSpawn({ bitmap: fxGlow(140, '255,240,200'), x: c.x, y: c.y - 10, life: 45, ds: 0.03, scale: 0.6 });
    };

    Scene_Map.prototype.escSparkleAt = function(target) {
        var c = target ? this.escHotspotCenter(target) : null;
        if (!c) c = this.escPlayerPos();
        this.escBurst(c.x, c.y, 20, '200,230,255', 2.5);
    };

    Scene_Map.prototype.escItemPopup = function(id) {
        var info = (EscapeManager._data.items || {})[id] || { name: id };
        var p = this.escPlayerPos();
        if (info.image) {
            var bmp = ImageManager.loadPicture(info.image);
            var sp = this.escSpawn({ bitmap: bmp, x: p.x, y: p.y - 20, vy: -0.7, life: 80, scale: 0.55, blend: false });
            sp.blendMode = 0;
        }
        this.escSpawn({ bitmap: fxGlow(100, '255,244,190'), x: p.x, y: p.y - 30, life: 50, ds: 0.02, scale: 0.6 });
        this.escBurst(p.x, p.y - 30, 12, '255,236,150', 2);
        var b = this._escToast.bitmap;
        b.clear();
        roundRect(b, 2, 2, 356, 36, 18, 'rgba(30,22,10,0.88)', 'rgba(255,214,120,0.95)', 2);
        b.fontSize = 20;
        b.textColor = '#ffe9b0';
        b.drawText('✦ ' + info.name + ' 획득!', 0, 2, 360, 36, 'center');
        this._escToastT = 110;
    };

    Scene_Map.prototype.escShowToast = function(text) {
        var b = this._escToast.bitmap;
        b.clear();
        roundRect(b, 2, 2, 356, 36, 18, 'rgba(30,22,10,0.88)', 'rgba(255,214,120,0.95)', 2);
        b.fontSize = 20;
        b.textColor = '#ffe9b0';
        b.drawText(String(text), 0, 2, 360, 36, 'center');
        this._escToastT = 110;
    };

    Scene_Map.prototype.escRefreshGoal = function() {
        if (!this._escGoal) return;
        var b = this._escGoal.bitmap;
        b.clear();
        var g = escSub(EscapeManager._goal);
        this._escGoal.visible = !!g;
        if (!g) return;
        b.fontSize = 18;
        var w = Math.min(516, b.measureTextWidth('목표  ' + g) + 34);
        roundRect(b, 1, 1, w, 30, 14, 'rgba(10,30,50,0.72)', 'rgba(140,210,255,0.8)', 1.5);
        b.textColor = '#9fe0ff';
        b.drawText('목표', 12, 1, 60, 30, 'left');
        b.textColor = '#ffffff';
        b.drawText(g, 56, 1, w - 62, 30, 'left');
    };

    Scene_Map.prototype.escRefreshChase = function() {
        if (!this._escChase) return;
        var c = EscapeManager._chase || EscapeManager._mission;
        this._escChase.visible = !!c;
        if (this._escGoal) this._escGoal.visible = !c && !!EscapeManager._goal;
        if (!c) return;
        var b = this._escChase.bitmap;
        b.clear();
        roundRect(b, 2, 2, 416, 40, 20, 'rgba(60,10,10,0.85)', 'rgba(255,150,120,0.95)', 2);
        var sec = Math.max(0, Math.ceil(c.frames / 60));
        b.fontSize = 22;
        b.textColor = sec <= 15 ? '#ff9a8a' : '#ffffff';
        var label = String(c.def.label || '쫓아가자!');
        b.drawText(label + '   ' + (c.targets.length - c.left.length) + ' / ' + c.targets.length + '   ⏱ ' + sec + '초', 0, 2, 420, 40, 'center');
    };

    Scene_Map.prototype.escTitleCard = function(text) {
        var parts = String(text).split('·');
        var top = parts.length > 1 ? parts[0].trim() : '';
        var main = parts.length > 1 ? parts.slice(1).join('·').trim() : String(text);
        var b = this._escCard.bitmap;
        b.clear();
        var ctx = ctxOf(b);
        var g = ctx.createLinearGradient(0, 0, SW(), 0);
        g.addColorStop(0, 'rgba(10,8,6,0)');
        g.addColorStop(0.2, 'rgba(10,8,6,0.78)');
        g.addColorStop(0.8, 'rgba(10,8,6,0.78)');
        g.addColorStop(1, 'rgba(10,8,6,0)');
        ctx.fillStyle = g;
        ctx.fillRect(0, 10, SW(), 110);
        setDirty(b);
        b.fillRect(SW() * 0.2, 12, SW() * 0.6, 2, 'rgba(255,214,120,0.85)');
        b.fillRect(SW() * 0.2, 116, SW() * 0.6, 2, 'rgba(255,214,120,0.85)');
        if (top) {
            b.fontSize = 22;
            b.textColor = '#ffd27a';
            b.drawText(top, 0, 18, SW(), 34, 'center');
        }
        b.fontSize = 38;
        b.textColor = '#ffffff';
        b.drawText(main, 0, top ? 54 : 36, SW(), 54, 'center');
        this._escCardT = 170;
    };

    Scene_Map.prototype.escRefreshOpen = function() {
        var room = EscapeManager.currentRoom();
        var list = room ? toArray(room.hotspots).filter(function(h) {
            return h.open && EscapeManager.checkCond(h.open);
        }) : [];
        var key = list.map(function(h) { return h.id; }).join(',');
        if (key === this._escOpenKey) return;
        this._escOpenKey = key;
        var self = this;
        this._escOpenSprites.forEach(function(o) { self._escFx.removeChild(o.sp); });
        this._escOpenSprites = [];
        list.forEach(function(h) {
            var style = h.openStyle || 'door';
            if (style === 'glow') {
                var c = self.escHotspotCenter(h.id);
                if (!c) return;
                var sp = new Sprite(fxGlow(256, '255,236,170'));
                sp.anchor.x = sp.anchor.y = 0.5;
                sp.blendMode = 1;
                self._escFx.addChildAt(sp, 0);
                self._escOpenSprites.push({ sp: sp, id: h.id, style: style, base: 0.7 + c.n * 0.08 });
                var rays = new Sprite(fxRays(256));
                rays.anchor.x = rays.anchor.y = 0.5;
                rays.blendMode = 1;
                self._escFx.addChildAt(rays, 0);
                self._escOpenSprites.push({ sp: rays, id: h.id, style: 'rays', base: 0.7 + c.n * 0.08 });
            } else {
                self.escHotspotEvents(h.id).forEach(function(ev) {
                    var sp = new Sprite(fxDoorway());
                    sp.anchor.x = sp.anchor.y = 0.5;
                    sp.blendMode = 1;
                    self._escFx.addChildAt(sp, 0);
                    self._escOpenSprites.push({ sp: sp, ev: ev, style: 'door' });
                });
            }
        });
    };

    Scene_Map.prototype.escDrawSight = function() {
        var g = this._escSight;
        if (!g) return;
        g.clear();
        var M = EscapeManager;
        if (!M._watch || !M.watchActive() || M._phase !== 'play') return;
        var tw = $gameMap.tileWidth(), th = $gameMap.tileHeight();
        var pulse = 0.22 + 0.08 * Math.sin(Graphics.frameCount / 8);
        M._watch.list.forEach(function(w) {
            if (w.ev._erased || w.ev._escHidden) return;
            M.sightTiles(w).forEach(function(t) {
                var sx = Math.round($gameMap.adjustX(t[0]) * tw), sy = Math.round($gameMap.adjustY(t[1]) * th);
                g.beginFill(0xff3020, pulse);
                g.drawRect(sx + 2, sy + 2, tw - 4, th - 4);
                g.endFill();
            });
            // 머리 위 경계 표시
            var ex = Math.round($gameMap.adjustX(w.ev._realX) * tw + tw / 2), ey = Math.round($gameMap.adjustY(w.ev._realY) * th - 12);
            g.beginFill(0xffcc30, 0.95); g.drawCircle(ex, ey - 30, 7); g.endFill();
            g.beginFill(0x402000, 1); g.drawRect(ex - 1.5, ey - 35, 3, 6); g.drawRect(ex - 1.5, ey - 27, 3, 2.5); g.endFill();
        });
    };

    // 조사 지점의 "mark": "이름" (+ "markIf": 조건) → 그 위에 통통 튀는 화살표와 이름표
    Scene_Map.prototype.escUpdateMarks = function() {
        if (!this._escMarks) return;
        var M = EscapeManager, room = M.currentRoom();
        var list = [];
        if (room && M._phase === 'play') {
            toArray(room.hotspots).forEach(function(h) {
                if (h.mark && M.checkCond(h.markIf) && (h.visible === undefined || M.checkCond(h.visible))) list.push(h);
            });
        }
        var key = list.map(function(h) { return h.id; }).join(',');
        if (key !== this._escMarkKey) {
            this._escMarkKey = key;
            this._escMarks.removeChildren();
            this._escMarkList = list.map(function(h) {
                var text = typeof h.mark === 'string' ? h.mark : (h.label || h.id);
                var bmp = new Bitmap(220, 64);
                bmp.fontSize = 18;
                var w = Math.min(214, bmp.measureTextWidth(text) + 26);
                roundRect(bmp, (220 - w) / 2, 2, w, 28, 13, 'rgba(255,214,60,0.95)', 'rgba(90,60,10,0.9)', 2);
                bmp.textColor = '#3a2608'; bmp.outlineWidth = 0;
                bmp.drawText(text, 0, 2, 220, 28, 'center');
                var ctx = ctxOf(bmp);
                ctx.fillStyle = 'rgba(255,214,60,0.98)'; ctx.strokeStyle = 'rgba(90,60,10,0.9)'; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.moveTo(98, 34); ctx.lineTo(122, 34); ctx.lineTo(110, 52); ctx.closePath(); ctx.fill(); ctx.stroke();
                setDirty(bmp);
                var sp = new Sprite(bmp);
                sp.anchor.x = 0.5; sp.anchor.y = 1;
                return { h: h, sp: sp };
            });
            var self = this;
            this._escMarkList.forEach(function(m) { self._escMarks.addChild(m.sp); });
        }
        var t = Graphics.frameCount, self2 = this;
        this._escMarkList.forEach(function(m, i) {
            var c = self2.escHotspotCenter(m.h.id);
            if (!c) { m.sp.visible = false; return; }
            m.sp.visible = true;
            m.sp.x = c.x;
            m.sp.y = c.y - 34 + Math.sin(t / 10 + i) * 5;
        });
    };

    Scene_Map.prototype.escUpdateFx = function() {
        var t = Graphics.frameCount;
        var self = this;
        this.escUpdateMarks();
        this.escDrawSight();
        // 열린 문 / 빛나는 물건
        this.escRefreshOpen();
        this._escOpenSprites.forEach(function(o) {
            if (o.style === 'door') {
                var c = self.escTileCenter(o.ev.x, o.ev.y);
                o.sp.x = c.x;
                o.sp.y = c.y;
                o.sp.opacity = 170 + Math.sin(t / 18) * 50;
            } else {
                var cc = self.escHotspotCenter(o.id);
                if (!cc) return;
                o.sp.x = cc.x;
                o.sp.y = cc.y;
                if (o.style === 'rays') {
                    o.sp.rotation = t / 160;
                    o.sp.scale.x = o.sp.scale.y = o.base;
                    o.sp.opacity = 80 + Math.sin(t / 25) * 30;
                } else {
                    var s = o.base + Math.sin(t / 22) * 0.08;
                    o.sp.scale.x = o.sp.scale.y = s;
                    o.sp.opacity = 130 + Math.sin(t / 22) * 40;
                }
            }
        });
        // 파티클
        for (var i = this._escParticles.length - 1; i >= 0; i--) {
            var q = this._escParticles[i];
            q.life--;
            if (q.tx !== undefined) {
                q.sp.x += (q.tx - q.sp.x) * 0.08;
                q.sp.y += (q.ty - q.sp.y) * 0.08;
            } else {
                q.vy += q.g;
                q.sp.x += q.vx;
                q.sp.y += q.vy;
            }
            q.sp.rotation += q.spin;
            q.sp.scale.x = q.sp.scale.y = Math.max(0.05, q.sp.scale.x + q.ds);
            q.sp.opacity = q.alpha * Math.min(1, q.life / (q.max * 0.5));
            if (q.life <= 0) {
                this._escFx.removeChild(q.sp);
                this._escParticles.splice(i, 1);
            }
        }
        // 시대 카드
        if (this._escCardT > 0) {
            this._escCardT--;
            var e = 170 - this._escCardT;
            this._escCard.opacity = e < 20 ? e / 20 * 255 : (this._escCardT < 30 ? this._escCardT / 30 * 255 : 255);
        } else {
            this._escCard.opacity = 0;
        }
        // 획득 알림
        if (this._escToastT > 0) {
            this._escToastT--;
            var f = 110 - this._escToastT;
            this._escToast.opacity = f < 10 ? f / 10 * 255 : (this._escToastT < 20 ? this._escToastT / 20 * 255 : 255);
        } else {
            this._escToast.opacity = 0;
        }
        if (this._escCine) this.escUpdateGate();
    };

    // --- 시간의 문 연출 ---------------------------------------------------------
    Scene_Map.prototype.escStartGate = function(s, done) {
        var self = this;
        var items = EscapeManager._data.items || {};
        var target = s.target || 'gate';
        var c = this.escHotspotCenter(target) || { x: SW() / 2, y: 140, n: 1 };
        var cine = { t: 0, c: c, done: done, icons: [] };
        toArray(s.items).forEach(function(id) {
            var info = items[id];
            if (!info || !info.image) return;
            var sp = new Sprite(ImageManager.loadPicture(info.image));
            sp.anchor.x = sp.anchor.y = 0.5;
            sp.visible = false;
            self._escFx.addChild(sp);
            cine.icons.push(sp);
        });
        cine.glow = new Sprite(fxGlow(256, '255,240,190'));
        cine.glow.anchor.x = cine.glow.anchor.y = 0.5;
        cine.glow.blendMode = 1;
        cine.glow.x = c.x;
        cine.glow.y = c.y;
        cine.glow.opacity = 0;
        cine.rays = new Sprite(fxRays(320));
        cine.rays.anchor.x = cine.rays.anchor.y = 0.5;
        cine.rays.blendMode = 1;
        cine.rays.x = c.x;
        cine.rays.y = c.y;
        cine.rays.opacity = 0;
        this._escFx.addChild(cine.rays);
        this._escFx.addChild(cine.glow);
        this._escCine = cine;
        $gameTemp.clearDestination();
    };

    Scene_Map.prototype.escUpdateGate = function() {
        var cine = this._escCine;
        var t = ++cine.t;
        var c = cine.c;
        var p = this.escPlayerPos();
        var self = this;
        // 1) 세 보물이 차례로 문으로 날아감
        cine.icons.forEach(function(sp, i) {
            var start = 10 + i * 24;
            if (t < start) return;
            var k = (t - start) / 40;
            if (k <= 1) {
                sp.visible = true;
                sp.x = p.x + (c.x - p.x) * k;
                sp.y = p.y - 20 + (c.y - p.y + 20) * k - Math.sin(k * Math.PI) * 70;
                sp.scale.x = sp.scale.y = 0.55 - k * 0.3;
                sp.rotation = Math.sin(k * 6) * 0.2;
            } else if (sp.visible) {
                sp.visible = false;
                self.escBurst(c.x, c.y, 18, '255,230,150', 3);
                if (!playSafeSe(SE_SOLVE, 90, 110 + i * 10)) SoundManager.playOk();
                cine.glow.opacity = Math.min(255, cine.glow.opacity + 70);
            }
        });
        // 2) 문이 커지며 빛을 빨아들임
        if (t === 92) {
            if (!playSafeSe(SE_GATE, 90, 100)) SoundManager.playRecovery();
            $gameScreen.startShake(3, 6, 110);
        }
        if (t > 92 && t <= 200) {
            var k2 = (t - 92) / 108;
            cine.glow.scale.x = cine.glow.scale.y = 1 + k2 * 2.2 + Math.sin(t / 6) * 0.06;
            cine.glow.opacity = 200 + k2 * 55;
            cine.rays.opacity = Math.min(230, k2 * 400);
            cine.rays.scale.x = cine.rays.scale.y = 0.8 + k2 * 1.6;
            if (t % 2 === 0) {
                var a = Math.random() * Math.PI * 2;
                var r = 260 + Math.random() * 120;
                this.escSpawn({ bitmap: fxSpark('255,236,170'), x: c.x + Math.cos(a) * r, y: c.y + Math.sin(a) * r,
                    tx: c.x, ty: c.y, life: 36, scale: 0.5 + Math.random() * 0.6, ds: -0.01, spin: 0.15 });
            }
        }
        cine.rays.rotation += 0.01 + (t > 92 ? (t - 92) / 3000 : 0);
        // 3) 주인공이 문으로 걸어 들어감
        if (t === 170) {
            $gamePlayer.setThrough(true);
            $gamePlayer.setDirection(8);
        }
        if (t >= 170 && t < 230 && !$gamePlayer.isMoving() && (t - 170) % 16 === 0) {
            $gamePlayer.moveStraight(8);
        }
        if (t >= 170 && t <= 230) {
            $gamePlayer.setOpacity(Math.max(0, 255 - (t - 170) * 4.5));
        }
        // 4) 하얗게
        if (t >= 190 && t <= 250) {
            this._escWhite.opacity = Math.min(255, (t - 190) / 60 * 255);
        }
        if (t === 262) {
            this._escFx.removeChild(cine.glow);
            this._escFx.removeChild(cine.rays);
            cine.icons.forEach(function(sp) { self._escFx.removeChild(sp); });
            $gamePlayer.setThrough(false);
            this._escCine = null;
            if (cine.done) cine.done();
        }
    };

    // --- 확대 그림 ---------------------------------------------------------------
    Scene_Map.prototype.escShowCloseup = function(name, maxScale) {
        var bmp = ImageManager.loadPicture(name);
        var sprite = this._escCloseup;
        var self = this;
        this._escCloseupName = name;
        if (this.escCloseupOverlays) this.escCloseupOverlays([]);
        sprite.bitmap = bmp;
        sprite.visible = false;
        this._escDim.visible = true;
        bmp.addLoadListener(function() {
            var maxW = SW() - 60;
            var maxH = self._escMsg.y - HUD_H - 60;
            var scale = Math.min(maxScale || 1, maxW / bmp.width, maxH / bmp.height);
            sprite.scale.x = scale;
            sprite.scale.y = scale;
            sprite.y = HUD_H + 10 + maxH / 2;
            sprite.visible = self._escCloseupName === name;
        });
    };

    Scene_Map.prototype.escCloseupOverlays = function(names) {
        var sprite = this._escCloseup; if (!sprite) return;
        if (sprite._escOv) sprite._escOv.forEach(function(c) { sprite.removeChild(c); });
        sprite._escOv = (names || []).map(function(n) {
            var c = new Sprite(ImageManager.loadPicture(n));
            c.anchor.x = sprite.anchor.x; c.anchor.y = sprite.anchor.y;
            sprite.addChild(c); return c;
        });
    };

    Scene_Map.prototype.escCloseupVisible = function() {
        return !!this._escCloseupName;
    };

    // 확대 그림을 HUD 아래 ~ bottom 사이에 맞춰 다시 배치
    Scene_Map.prototype.escFitCloseup = function(bottom) {
        var sprite = this._escCloseup;
        var bmp = sprite.bitmap;
        if (!bmp) return;
        var fit = function() {
            var maxW = SW() - 40;
            var maxH = bottom - HUD_H - 8;
            var scale = Math.min(1, maxW / bmp.width, maxH / bmp.height);
            sprite.scale.x = scale;
            sprite.scale.y = scale;
            sprite.y = HUD_H + 4 + maxH / 2;
        };
        if (bmp.isReady()) fit(); else bmp.addLoadListener(fit);
    };

    Scene_Map.prototype.escHideCloseup = function() {
        if (!this._escCloseup) return;
        this._escCloseupName = '';
        this._escCloseup.visible = false;
        this._escDim.visible = false;
    };

    Scene_Map.prototype.escCloseAll = function() {
        [this._escChoice, this._escNumpad, this._escBag, this._escDial, this._escTiming].forEach(function(w) {
            if (w) {
                w.deactivate();
                w.close();
            }
        });
        if (this._escMsg) this._escMsg.dismiss();
    };

    // --- 오류 화면 ---------------------------------------------------------------
    Scene_Map.prototype.escShowError = function(errors) {
        var text = '[데이터 파일 확인 필요]\n' + errors.slice(0, 12).join('\n');
        if (errors.length > 12) text += '\n... 외 ' + (errors.length - 12) + '개';
        console.error('EscapeRoom 데이터 오류:\n' + errors.join('\n'));
        var bmp = new Bitmap(SW(), SH());
        bmp.fillAll('#1a1010');
        bmp.fontSize = 20;
        var lines = wrapText(bmp, text, SW() - 60);
        for (var i = 0; i < lines.length && i < 22; i++) {
            bmp.textColor = i === 0 ? '#ffb070' : '#ffffff';
            bmp.drawText(lines[i], 30, 30 + i * 26, SW() - 60, 26, 'left');
        }
        this._escError.bitmap = bmp;
        this._escHud.bitmap.clear();
    };

    // --- 제작 도우미 -------------------------------------------------------------
    Scene_Map.prototype.escUpdateDebug = function() {
        var key = $gameMap.displayX() + ',' + $gameMap.displayY() + ',' + $gamePlayer.x + ',' + $gamePlayer.y;
        if (key === this._escDebugText) return;
        this._escDebugText = key;
        var bmp = this._escDebug.bitmap;
        bmp.clear();
        var tw = $gameMap.tileWidth();
        var th = $gameMap.tileHeight();
        var ox = $gameMap.displayX();
        var oy = $gameMap.displayY();
        for (var y = 0; y < $gameMap.height(); y++) {
            for (var x = 0; x < $gameMap.width(); x++) {
                var sx = (x - ox) * tw;
                var sy = (y - oy) * th;
                if (sx < -tw || sy < -th || sx > SW() || sy > SH()) continue;
                if ($gameMap.regionId(x, y) === WALL_REGION) {
                    bmp.fillRect(sx, sy, tw, th, 'rgba(255,40,40,0.28)');
                }
            }
        }
        $gameMap.events().forEach(function(ev) {
            var h = EscapeManager.hotspotForEvent(ev);
            var sx = (ev.x - ox) * tw;
            var sy = (ev.y - oy) * th;
            bmp.fillRect(sx + 2, sy + 2, tw - 4, th - 4, h ? 'rgba(255,230,0,0.35)' : 'rgba(120,200,255,0.3)');
            bmp.fontSize = 12;
            bmp.textColor = h ? '#fff27a' : '#bfe6ff';
            bmp.drawText(String(ev.event().name), sx, sy + th - 16, tw, 14, 'center');
        });
        bmp.fillRect(SW() - 210, SH() - 34, 206, 30, 'rgba(0,0,0,0.7)');
        bmp.fontSize = 16;
        bmp.textColor = '#7fffd4';
        bmp.drawText('맵 ' + $gameMap.mapId() + '번  x: ' + $gamePlayer.x + '  y: ' + $gamePlayer.y, SW() - 204, SH() - 34, 196, 30, 'left');
        var missing = EscapeManager._missing || [];
        if (missing.length > 0) {
            bmp.fillRect(4, SH() - 34, SW() - 220, 30, 'rgba(120,0,0,0.75)');
            bmp.textColor = '#ffffff';
            bmp.drawText('이벤트가 없는 조사 지점: ' + missing.join(', '), 10, SH() - 34, SW() - 232, 30, 'left');
        }
    };

    //=========================================================================
    // v3.4 어드벤처: 체력 · 함정 · 움직이는 것 · 활 · 어둠 · 아이템 효과 · 무작위 단계
    //   (데이터에 적었을 때만 켜짐 - 예전 게임에는 영향 없음)
    //=========================================================================
    var ADV = { tw: 48 };

    function advItemEffect(kind) {
        var M = EscapeManager, items = (M._data && M._data.items) || {};
        var n = 0;
        (M._items || []).forEach(function(id) {
            var it = items[id];
            if (it && it.effect) toArray(it.effect).forEach(function(e) { if (e === kind) n++; });
        });
        return n;
    }

    // --- 초기화 ---------------------------------------------------------------
    var _ER_reset = EscapeManager.reset;
    EscapeManager.reset = function() {
        _ER_reset.apply(this, arguments);
        var max = Number((this._data && this._data.hp) || 0);
        this._hpMax = max; this._hp = max;
        this._inv = 0;
        this._adv = null;
        this._arrowCool = 0;
    };

    // --- 무작위 단계 / 피해 / 회복 ---------------------------------------------
    var _ER_processStep = EscapeManager.processStep;
    EscapeManager.processStep = function(s) {
        if (s && s.random) {
            var list = toArray(s.random);
            var pick = list[Math.floor(Math.random() * list.length)];
            this.insertSteps(toArray(pick));
            return;
        }
        if (s && s['if'] !== undefined && (s.then || s['else'])) {
            this.insertSteps(toArray(this.checkCond(s['if']) ? (s.then || []) : (s['else'] || [])));
            return;
        }
        if (s && s.damage) this.advDamage(Number(s.damage), true);
        if (s && s.picture) {
            var _r = _ER_processStep.call(this, s), self = this;
            var ov = toArray(s.overlays).filter(function(o) { return o && o.picture && self.checkCond(o['if']); });
            if (this._scene && this._scene.escCloseupOverlays) this._scene.escCloseupOverlays(ov.map(function(o) { return String(o.picture); }));
            return _r;
        }
        if (s && s.heal) { this._hp = Math.min(this._hpMax, this._hp + Number(s.heal)); this.refreshHud(); }
        if (s && s.fullHeal) { this._hp = this._hpMax; this.refreshHud(); }
        return _ER_processStep.call(this, s);
    };

    // --- 체력 -----------------------------------------------------------------
    EscapeManager.advDamage = function(n, fromStep) {
        if (!this._hpMax) return;
        if (!fromStep && (this._inv > 0 || this._phase !== 'play')) return;
        this._hp = Math.max(0, this._hp - n);
        this._inv = 75;
        SoundManager.playActorDamage ? SoundManager.playActorDamage() : SoundManager.playBuzzer();
        $gameScreen.startFlash([255, 60, 40, 150], 16);
        $gameScreen.startShake(5, 9, 14);
        this.refreshHud();
        if (this._scene && this._scene.escShowToast) this._scene.escShowToast('❤ -' + n);
        if (this._hp <= 0 && !fromStep) this.advKnockout();
    };

    EscapeManager.advKnockout = function() {
        var room = this.currentRoom();
        this._hp = this._hpMax;
        var cp = toArray(room.checkpoint || room.start);
        var steps = toArray(room.ko || [{ speaker: '갑이', text: '으악, 기운이 다 빠졌어! 조금 앞에서 다시 해 보자.' }]).slice();
        var again = [];
        if (this._mission) {
            var m = this._mission; this._mission = null;
            if (this._scene && this._scene.escRefreshChase) this._scene.escRefreshChase();
            this.resetMission(m);
            again = m.def.retry === false ? [] : [{ mission: m.def }];
        }
        steps.push({ go: room.id, x: Number(cp[0]), y: Number(cp[1]), dir: cp[2] || 'up' });
        this._waiting = false;
        this._queue = steps.concat(again).concat(this._queue);
        if (!this._afterQueue) this._afterQueue = this.hideCloseup.bind(this);
    };

    // 부적(charm): 감시에 한 번 들켜도 넘어감
    var _ER_onCaught = EscapeManager.onCaught;
    EscapeManager.onCaught = function(w) {
        var items = (this._data && this._data.items) || {};
        for (var i = 0; i < this._items.length; i++) {
            var it = items[this._items[i]];
            if (it && toArray(it.effect).indexOf('charm') >= 0) {
                var id = this._items[i];
                this._items.splice(i, 1);
                this._watch.cool = 120;
                if (w && w.ev) w.ev.turnTowardPlayer();
                $gameScreen.startFlash([255, 240, 160, 160], 20);
                if (this._scene) this._scene.escShowToast((it.name || id) + ' 덕분에 들키지 않았다!');
                this.refreshHud();
                return;
            }
        }
        return _ER_onCaught.apply(this, arguments);
    };

    // --- 방에 들어갈 때: 함정 고르기, 움직이는 것 준비 --------------------------
    var _ER_setupWatchers = EscapeManager.setupWatchers;
    EscapeManager.setupWatchers = function() {
        _ER_setupWatchers.apply(this, arguments);
        var room = this.currentRoom();
        var adv = { traps: [], movers: [], arrows: [], last: null, dark: 0 };
        if (room && room.traps) {
            var T = room.traps;
            var cand = toArray(T.tiles).slice();
            var n = Math.min(cand.length, Number(T.count || cand.length));
            for (var i = cand.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = cand[i]; cand[i] = cand[j]; cand[j] = t; }
            for (var k = 0; k < n; k++) {
                var kind = T.kind === 'mixed' ? (Math.random() < 0.5 ? 'pit' : 'spike') : (T.kind || 'pit');
                adv.traps.push({ x: cand[k][0], y: cand[k][1], kind: kind, shown: kind !== 'pit', up: false,
                                 t: Math.floor(Math.random() * 150), dmg: Number(T.damage || 1) });
            }
        }
        if (room && room.movers) {
            toArray(room.movers).forEach(function(m) {
                var ev = $gameMap.events().filter(function(e) { return String(e.event().name).trim() === String(m.event); })[0];
                if (!ev) return;
                ev.setMoveSpeed(Number(m.speed || 4));
                ev.setThrough(true);
                adv.movers.push({ def: m, ev: ev, idx: 0, wait: Number(m.delay || 0) });
            });
        }
        adv.dark = room && room.dark ? Number(room.dark) : 0;
        this._adv = adv;
        if (this._scene && this._scene.escAdvBuild) this._scene.escAdvBuild();
    };

    // --- 매 프레임 -----------------------------------------------------------
    var _ER_update = EscapeManager.update;
    EscapeManager.update = function(scene) {
        _ER_update.apply(this, arguments);
        if (!this.isActive() || scene !== this._scene || this._phase !== 'play') return;
        this.advUpdate();
    };

    EscapeManager.advCond = function(def) {
        return !def || def['if'] === undefined || this.checkCond(def['if']);
    };

    EscapeManager.advUpdate = function() {
        var adv = this._adv; if (!adv) return;
        if (this._inv > 0) this._inv--;
        if (this._arrowCool > 0) this._arrowCool--;
        var busy = this.isBusy() && !this._mission && !this._chase;
        var p = $gamePlayer, px = p.x, py = p.y;
        var room = this.currentRoom();
        var trapOn = !room.trapsIf || this.checkCond(room.trapsIf);
        // 함정
        var self = this;
        adv.traps.forEach(function(t) {
            if (t.kind === 'spike') {
                if (!busy) t.t = (t.t + 1) % 150;
                t.up = trapOn && t.t < 55;
            }
        });
        if (!busy && trapOn && !p.isTransferring()) {
            var here = adv.traps.filter(function(t) { return t.x === px && t.y === py; })[0];
            if (here && !p.isMoving()) {
                if (here.kind === 'pit') {
                    here.shown = true;
                    this.advDamage(here.dmg);
                    if (adv.last && (adv.last[0] !== px || adv.last[1] !== py)) p.locate(adv.last[0], adv.last[1]);
                    if (this._scene) this._scene.escShowToast('앗, 함정이다!');
                } else if (here.up && this._inv === 0) {
                    this.advDamage(here.dmg);
                    if (adv.last && (adv.last[0] !== px || adv.last[1] !== py)) p.locate(adv.last[0], adv.last[1]);
                }
            }
        }
        if (!p.isMoving()) {
            var onTrap = adv.traps.some(function(t) { return t.x === p.x && t.y === p.y && (t.kind === 'pit' || t.up); });
            if (!onTrap) adv.last = [p.x, p.y];
        }
        // 움직이는 것 (굴러오는 돌, 움직이는 과녁 등)
        adv.movers.forEach(function(m) {
            var ev = m.ev;
            if (ev._erased || ev._escHidden) return;
            var on = self.advCond(m.def);
            if (!on || busy) return;
            if (!ev.isMoving()) {
                if (m.wait > 0) { m.wait--; }
                else {
                    var route = toArray(m.def.route);
                    if (route.length) {
                        var tgt = route[m.idx % route.length];
                        if (ev.x === tgt[0] && ev.y === tgt[1]) {
                            m.idx++;
                            if (m.def.loop === 'restart' && m.idx >= route.length) { m.idx = 1; ev.locate(route[0][0], route[0][1]); }
                            m.wait = Number(m.def.wait || 0);
                        } else {
                            var dx = tgt[0] - ev.x, dy = tgt[1] - ev.y;
                            var dir = Math.abs(dx) >= Math.abs(dy) ? (dx > 0 ? 6 : 4) : (dy > 0 ? 2 : 8);
                            ev.setDirection(dir);
                            ev.setThrough(true);
                            ev.moveStraight(dir);
                        }
                    }
                }
            }
            if (m.def.damage && !p.isTransferring()) {
                var ex = Math.round(ev._realX), ey = Math.round(ev._realY);
                if (Math.abs(ev._realX - p._realX) < 0.7 && Math.abs(ev._realY - p._realY) < 0.7) {
                    self.advDamage(Number(m.def.damage));
                }
            }
        });
        // 화살
        var fire = (Input.isTriggered('escFire') || this._fireTap) && this.advCanFire();
        this._fireTap = false;
        if (fire) this.advFire();
        adv.arrows = adv.arrows.filter(function(a) { return self.advMoveArrow(a); });
    };

    // --- 활 -------------------------------------------------------------------
    EscapeManager.advBowOn = function() {
        var room = this.currentRoom();
        if (!room || !room.bow) return false;
        if (room.bow === true) return true;
        return this.checkCond(room.bow);
    };
    EscapeManager.advCanFire = function() {
        if (!this.advBowOn() || this._arrowCool > 0) return false;
        if (this.isBusy() && !this._mission && !this._chase) return false;
        return !$gamePlayer.isTransferring();
    };
    EscapeManager.advFire = function() {
        var p = $gamePlayer, d = p.direction();
        var a = { x: p._realX, y: p._realY, dx: d === 6 ? 1 : d === 4 ? -1 : 0, dy: d === 2 ? 1 : d === 8 ? -1 : 0, life: 40, sp: null };
        this._adv.arrows.push(a);
        this._arrowCool = 18;
        if (!playSafeSe('Bow1', 80, 110)) SoundManager.playCursor();
        if (this._scene && this._scene.escAdvArrowSprite) a.sp = this._scene.escAdvArrowSprite(a);
    };
    // 화면을 눌러 그 쪽으로 쏘기 (휴대폰·마우스)
    EscapeManager.advFireAt = function(mx, my) {
        var p = $gamePlayer;
        var vx = mx - p._realX, vy = my - p._realY, L = Math.hypot(vx, vy);
        if (L < 0.3) return;
        p.setDirection(Math.abs(vx) > Math.abs(vy) ? (vx > 0 ? 6 : 4) : (vy > 0 ? 2 : 8));
        var a = { x: p._realX, y: p._realY, dx: vx / L, dy: vy / L, life: 46, sp: null };
        this._adv.arrows.push(a);
        this._arrowCool = 18;
        if (!playSafeSe('Bow1', 80, 110)) SoundManager.playCursor();
        if (this._scene && this._scene.escAdvArrowSprite) a.sp = this._scene.escAdvArrowSprite(a);
    };
    EscapeManager.advMoveArrow = function(a) {
        var step = 0.34;
        a.x += a.dx * step; a.y += a.dy * step; a.life--;
        var tx = Math.round(a.x), ty = Math.round(a.y);
        var end = a.life <= 0 || !$gameMap.isValid(tx, ty);
        if (!end && $gameMap.regionId(tx, ty) === WALL_REGION) {
            // 벽 칸이라도 과녁 이벤트가 있으면 맞힘
            if (!$gameMap.eventsXy(tx, ty).some(function(e) { var h = EscapeManager.hotspotForEvent(e); return h && h.target && !e._escHidden; })) end = true;
        }
        if (!end) {
            var hit = null, self = this;
            $gameMap.events().forEach(function(e) {
                if (hit || e._erased || e._escHidden) return;
                var h = self.hotspotForEvent(e);
                if (!h || !h.target) return;
                if (Math.abs(e._realX - a.x) < 0.6 && Math.abs(e._realY - a.y) < 0.6) hit = { ev: e, h: h };
            });
            if (hit) { this.advHit(hit.ev, hit.h, a); end = true; }
        }
        if (end) {
            if (a.sp && a.sp.parent) a.sp.parent.removeChild(a.sp);
            return false;
        }
        return true;
    };
    EscapeManager.advHit = function(ev, h, a) {
        var scene = this._scene;
        if (scene) scene.escBurst(ev.screenX(), ev.screenY() - 24, 14, '255,230,140', 2.2);
        if (!playSafeSe('Damage1', 70, 130)) SoundManager.playOk();
        if (this._mission && this.missionTouch(ev)) return;
        var T = h.target === true ? {} : h.target;
        if (T.flag) { var self = this; toArray(T.flag).forEach(function(f) { self._flags[f] = true; }); this.refreshHud(); }
        if (T.steps && this.canInteract()) this.runSteps(toArray(T.steps), this.hideCloseup.bind(this));
        else if (T.steps) this.insertSteps(toArray(T.steps));
    };

    // 이동 속도 아이템
    var _GP_realMoveSpeed = Game_Player.prototype.realMoveSpeed;
    Game_Player.prototype.realMoveSpeed = function() {
        var s = _GP_realMoveSpeed.call(this);
        if (EscapeManager && EscapeManager.isActive && EscapeManager.isActive()) s += Math.min(1, advItemEffect('speed'));
        return s;
    };

    // 드러난 구덩이는 지나갈 수 없음
    var _GP_isMapPassable = Game_Player.prototype.isMapPassable;
    Game_Player.prototype.isMapPassable = function(x, y, d) {
        var M = EscapeManager;
        if (M && M._adv && M._adv.traps.length) {
            var x2 = $gameMap.roundXWithDirection(x, d), y2 = $gameMap.roundYWithDirection(y, d);
            if (M._adv.traps.some(function(t) { return t.kind === 'pit' && t.shown && t.x === x2 && t.y === y2; })) return false;
        }
        return _GP_isMapPassable.call(this, x, y, d);
    };

    Input.keyMapper[65] = 'escFire';     // A
    Input.keyMapper[70] = 'escFire';     // F

    // --- 화면: 함정·화살·어둠 그리기 ---------------------------------------------
    function advTrapBitmap(kind, up) {
        var b = new Bitmap(48, 48), c = b._context;
        if (kind === 'pit') {
            c.fillStyle = 'rgba(40,24,14,0.95)'; c.beginPath(); c.ellipse(24, 26, 19, 15, 0, 0, Math.PI * 2); c.fill();
            c.fillStyle = 'rgba(10,6,4,1)'; c.beginPath(); c.ellipse(24, 28, 14, 10, 0, 0, Math.PI * 2); c.fill();
            c.strokeStyle = 'rgba(120,90,60,1)'; c.lineWidth = 2; c.beginPath(); c.ellipse(24, 26, 19, 15, 0, 0, Math.PI * 2); c.stroke();
        } else {
            c.fillStyle = '#6e6458'; c.fillRect(4, 8, 40, 34); c.fillStyle = '#8a7f70'; c.fillRect(4, 8, 40, 4);
            for (var i = 0; i < 3; i++) for (var j = 0; j < 3; j++) {
                var x = 10 + i * 13, y = 16 + j * 10;
                if (up) { c.fillStyle = '#d8d0c0'; c.beginPath(); c.moveTo(x - 4, y + 6); c.lineTo(x, y - 8); c.lineTo(x + 4, y + 6); c.fill();
                          c.fillStyle = '#8a8070'; c.beginPath(); c.moveTo(x, y - 8); c.lineTo(x + 4, y + 6); c.lineTo(x, y + 6); c.fill(); }
                else { c.fillStyle = '#3a342c'; c.fillRect(x - 2, y, 4, 3); }
            }
        }
        b._setDirty ? b._setDirty() : (b._baseTexture && b._baseTexture.update());
        return b;
    }
    function advArrowBitmap() {
        var b = new Bitmap(32, 32), c = b._context;
        c.strokeStyle = '#8a5a30'; c.lineWidth = 2; c.beginPath(); c.moveTo(4, 16); c.lineTo(26, 16); c.stroke();
        c.fillStyle = '#d0d0d8'; c.beginPath(); c.moveTo(30, 16); c.lineTo(24, 12); c.lineTo(24, 20); c.fill();
        c.fillStyle = '#f0f0f0'; c.fillRect(3, 13, 5, 2); c.fillRect(3, 17, 5, 2);
        b._setDirty ? b._setDirty() : (b._baseTexture && b._baseTexture.update());
        return b;
    }
    function advHoleBitmap(r) {
        var D = r * 2, b = new Bitmap(D, D), c = b._context;
        var g = c.createRadialGradient(r, r, r * 0.35, r, r, r);
        g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(0.7, 'rgba(0,0,0,0.55)'); g.addColorStop(1, 'rgba(0,0,0,0.94)');
        c.fillStyle = g; c.fillRect(0, 0, D, D);
        b._setDirty ? b._setDirty() : (b._baseTexture && b._baseTexture.update());
        return b;
    }

    Scene_Map.prototype.escAdvBuild = function() {
        var tm = this._spriteset && this._spriteset._tilemap;
        if (this._escAdvSprites) this._escAdvSprites.forEach(function(s) { if (s.parent) s.parent.removeChild(s); });
        this._escAdvSprites = [];
        if (this._escDark) { if (this._escDark.parent) this._escDark.parent.removeChild(this._escDark); this._escDark = null; }
        var adv = EscapeManager._adv; if (!adv || !tm) return;
        this._escTrapBmp = this._escTrapBmp || { pit: advTrapBitmap('pit'), up: advTrapBitmap('spike', true), down: advTrapBitmap('spike', false) };
        var self = this;
        adv.traps.forEach(function(t) {
            var sp = new Sprite(self._escTrapBmp.pit);
            sp.z = 1; t.sp = sp; tm.addChild(sp); self._escAdvSprites.push(sp);
        });
        if (adv.dark > 0) {
            var cont = new Sprite();
            var r = Math.round((adv.dark + 2 * advItemEffect('light')) * 48);
            cont._hole = new Sprite(advHoleBitmap(r)); cont._r = r;
            cont._g = new PIXI.Graphics();
            cont.addChild(cont._g); cont.addChild(cont._hole);
            this._escFx.addChildAt(cont, 0);
            this._escDark = cont;
        }
    };

    Scene_Map.prototype.escAdvArrowSprite = function(a) {
        var tm = this._spriteset && this._spriteset._tilemap; if (!tm) return null;
        this._escArrowBmp = this._escArrowBmp || advArrowBitmap();
        var sp = new Sprite(this._escArrowBmp);
        sp.anchor.x = sp.anchor.y = 0.5; sp.z = 6;
        sp.rotation = Math.atan2(a.dy, a.dx);
        tm.addChild(sp);
        return sp;
    };

    var _SM_escUpdateFx = Scene_Map.prototype.escUpdateFx;
    Scene_Map.prototype.escUpdateFx = function() {
        _SM_escUpdateFx.apply(this, arguments);
        var adv = EscapeManager._adv; if (!adv) return;
        var tw = $gameMap.tileWidth(), th = $gameMap.tileHeight();
        var self = this;
        adv.traps.forEach(function(t) {
            if (!t.sp) return;
            t.sp.x = Math.round($gameMap.adjustX(t.x) * tw); t.sp.y = Math.round($gameMap.adjustY(t.y) * th);
            if (t.kind === 'pit') { t.sp.visible = t.shown; }
            else { t.sp.visible = true; t.sp.bitmap = t.up ? self._escTrapBmp.up : self._escTrapBmp.down; }
        });
        adv.arrows.forEach(function(a) {
            if (!a.sp) return;
            a.sp.x = Math.round($gameMap.adjustX(a.x) * tw + tw / 2); a.sp.y = Math.round($gameMap.adjustY(a.y) * th + th / 2 - 8);
        });
        if (this._escDark) {
            var rmD = EscapeManager.currentRoom(), da = rmD && rmD.darkArea;
            if (da) {   // v3.5: 어둠이 그 구역 안에서만
                var inD = $gamePlayer._realY <= da[3] + 0.5 && $gamePlayer._realY >= da[1] - 0.5 && $gamePlayer._realX >= da[0] - 0.5 && $gamePlayer._realX <= da[2] + 0.5;
                this._escDark.visible = inD;
            }
        }
        if (this._escDark && this._escDark.visible) {
            var d = this._escDark, r = d._r;
            var cx = $gamePlayer.screenX(), cy = $gamePlayer.screenY() - 20;
            d._hole.x = cx - r; d._hole.y = cy - r;
            var g = d._g; g.clear(); g.beginFill(0x000000, 0.94);
            var W = Graphics.width, H = Graphics.height;
            g.drawRect(0, 0, W, Math.max(0, cy - r));
            g.drawRect(0, cy + r, W, Math.max(0, H - cy - r));
            g.drawRect(0, cy - r, Math.max(0, cx - r), 2 * r);
            g.drawRect(cx + r, cy - r, Math.max(0, W - cx - r), 2 * r);
            g.endFill();
        }
        // 맞으면 깜빡임
        if (EscapeManager._inv > 0) $gamePlayer.setOpacity((Math.floor(EscapeManager._inv / 5) % 2) ? 90 : 255);
        else if ($gamePlayer.opacity() !== 255 && EscapeManager._hpMax > 0) $gamePlayer.setOpacity(255);
        if (this._escBowBtn) this._escBowBtn.visible = EscapeManager._phase === 'play' && EscapeManager.advBowOn();
    };

    // ===== v3.7 회상(세피아 + 낡은 필름) · 진흙 칸(리전 5) · 추위(방 "drain") =====
    //  방 "memory": true  → 화면 가장자리 어둡게 + 필름 무늬(img/pictures/fx_memory1·2) 겹치기
    //                      (색은 방 "tint": [40, 14, -34, 255] 처럼 함께 지정: 인물까지 모두 옛날 사진 색)
    //  리전 5 = 진흙: 걸음이 느려짐
    //  방 "drain": { "every": 600, "damage": 1, "text": "너무 추워!" } → 일정 시간마다 하트 -1
    //            아이템 "effect": "warm" 이 있으면 1.6배 느리게, 단계 { "heal": 1 } 에서 시간 다시 셈
    var _ER_setupWatchers37 = EscapeManager.setupWatchers;
    EscapeManager.setupWatchers = function() {
        _ER_setupWatchers37.apply(this, arguments);
        this._drainT = 0;
    };
    var _ER_advUpdate37 = EscapeManager.advUpdate;
    EscapeManager.advUpdate = function() {
        _ER_advUpdate37.apply(this, arguments);
        var room = this.currentRoom(); if (!room || !room.drain || !this._hpMax) return;
        var dr = room.drain;
        if (dr['if'] !== undefined && !this.checkCond(dr['if'])) return;
        if (this.isBusy() && !this._mission) return;
        var every = Number(dr.every || 900) * (advItemEffect('warm') > 0 ? 1.6 : 1);
        this._drainT = (this._drainT || 0) + 1;
        if (this._drainT >= every) {
            this._drainT = 0;
            if (this._scene) this._scene.escShowToast(dr.text || '너무 추워!');
            this.advDamage(Number(dr.damage || 1));
        }
    };
    var _ER_processStep37 = EscapeManager.processStep;
    EscapeManager.processStep = function(s) {
        if (s && typeof s === 'object' && (s.heal || s.fullHeal)) this._drainT = 0;
        return _ER_processStep37.apply(this, arguments);
    };
    var _ER_applyChar37 = EscapeManager.applyCharacter;
    EscapeManager.applyCharacter = function(c) {
        if (c && c.image) this._baseImage = String(c.image);
        return _ER_applyChar37.apply(this, arguments);
    };
    var _GP_rms37 = Game_Player.prototype.realMoveSpeed;
    Game_Player.prototype.realMoveSpeed = function() {
        var v = _GP_rms37.call(this);
        if (EscapeManager && EscapeManager.isRoomMap && EscapeManager.isRoomMap($gameMap.mapId()) && $gameMap.regionId(this.x, this.y) === 5) v -= 1.5;
        return v;
    };
    var _SM_escAdvBuild37 = Scene_Map.prototype.escAdvBuild;
    Scene_Map.prototype.escAdvBuild = function() {
        _SM_escAdvBuild37.apply(this, arguments);
        if (this._escMemory) { if (this._escMemory.parent) this._escMemory.parent.removeChild(this._escMemory); this._escMemory = null; }
        var room = EscapeManager.currentRoom();
        var lead = $gameParty.leader(), M7 = EscapeManager;
        if (lead && M7._baseImage) {
            var want = room && room.older ? M7._baseImage + '_old' : M7._baseImage;
            if (lead.characterName() !== want) { lead.setCharacterImage(want, lead.characterIndex()); $gamePlayer.refresh(); }
        }
        if (room && room.memory && this._escFx) {
            var sp = new Sprite();
            sp._a = ImageManager.loadPicture('fx_memory1'); sp._b = ImageManager.loadPicture('fx_memory2');
            sp.bitmap = sp._a;
            this._escFx.addChildAt(sp, 0);
            this._escMemory = sp;
        }
    };
    var _SM_escUpdateFx37 = Scene_Map.prototype.escUpdateFx;
    Scene_Map.prototype.escUpdateFx = function() {
        _SM_escUpdateFx37.apply(this, arguments);
        var m = this._escMemory;
        if (m) {
            var t = Graphics.frameCount;
            if (t % 6 === 0) m.bitmap = (Math.floor(t / 6) % 2) ? m._b : m._a;
            if (m.bitmap && m.bitmap.width > 1) { m.scale.x = Graphics.width / m.bitmap.width; m.scale.y = Graphics.height / m.bitmap.height; }
            m.opacity = 205 + Math.floor(Math.random() * 40);
        }
    };

    // --- 체력 하트 (위쪽 표시줄 아래 오른쪽) / 활 버튼 (오른쪽 아래 둥근 버튼) -----
    var _SM_escRefreshHud = Scene_Map.prototype.escRefreshHud;
    Scene_Map.prototype.escRefreshHud = function() {
        _SM_escRefreshHud.apply(this, arguments);
        var M = EscapeManager; if (!this._escHud) return;
        if (M._hpMax > 0) {
            if (!this._escHearts) {
                this._escHearts = new Sprite(new Bitmap(30 * 6 + 16, 34));
                this.addChildAt(this._escHearts, this.getChildIndex(this._escHud) + 1);
            }
            var b = this._escHearts.bitmap; b.clear();
            this._escHearts.x = SW() - b.width - 8; this._escHearts.y = HUD_H + 6;
            this._escHearts.visible = M._phase === 'play';
            var w = M._hpMax * 26 + 16;
            roundRect(b, b.width - w, 1, w - 1, 30, 14, 'rgba(30,10,10,0.6)', 'rgba(255,150,150,0.7)', 1.5);
            for (var i = 0; i < M._hpMax; i++) {
                b.fontSize = 22; b.textColor = i < M._hp ? '#ff5a6a' : 'rgba(255,255,255,0.28)';
                b.drawText('♥', b.width - w + 8 + i * 26, 0, 26, 32, 'center');
            }
        }
        if (!this._escBowBtn && M._data && JSON.stringify(M._data.rooms || []).indexOf('"bow"') >= 0) {
            var bb = new Bitmap(84, 84);
            bb._context.fillStyle = 'rgba(120,60,30,0.85)'; bb._context.beginPath(); bb._context.arc(42, 42, 38, 0, Math.PI * 2); bb._context.fill();
            bb._context.strokeStyle = 'rgba(255,230,180,0.9)'; bb._context.lineWidth = 3; bb._context.stroke();
            bb._setDirty ? bb._setDirty() : null;
            bb.fontSize = 30; bb.drawText('🏹', 0, 10, 84, 40, 'center');
            bb.fontSize = 15; bb.textColor = '#ffe9c0'; bb.drawText('활 (A)', 0, 48, 84, 22, 'center');
            this._escBowBtn = new Sprite(bb);
            this.addChildAt(this._escBowBtn, this.getChildIndex(this._escHud) + 1);
        }
        if (this._escBowBtn) { this._escBowBtn.x = SW() - 96; this._escBowBtn.y = SH() - 100; }
    };
    var _SM_processMapTouch2 = Scene_Map.prototype.processMapTouch;
    Scene_Map.prototype.processMapTouch = function() {
        var b = this._escBowBtn;
        if (b && b.visible && TouchInput.isTriggered() && Math.hypot(TouchInput.x - b.x - 42, TouchInput.y - b.y - 42) < 44) {
            EscapeManager._fireTap = true; this._touchCount = 0; $gameTemp.clearDestination(); return;
        }
        if (b && b.visible && TouchInput.isPressed() && Math.hypot(TouchInput.x - b.x - 42, TouchInput.y - b.y - 42) < 44) return;
        var M = EscapeManager;
        if (TouchInput.isTriggered() && M._adv && M.advBowOn() && TouchInput.y > HUD_H) {
            var tw = $gameMap.tileWidth(), th = $gameMap.tileHeight();
            var mx = $gameMap.displayX() + TouchInput.x / tw - 0.5, my = $gameMap.displayY() + (TouchInput.y + 12) / th - 0.5;
            var ix = Math.round(mx), iy = Math.round(my);
            var aim = $gameMap.regionId(ix, iy) === 4;
            if (!aim) aim = $gameMap.events().some(function(e) {
                var h = M.hotspotForEvent(e);
                return h && h.target && !e._escHidden && Math.abs(e._realX - mx) < 0.8 && Math.abs(e._realY - my) < 0.9;
            });
            if (aim) {
                if (M.advCanFire()) M.advFireAt(mx, my);
                this._touchCount = 0; $gameTemp.clearDestination(); this._escAimHold = true; return;
            }
        }
        if (this._escAimHold) { if (TouchInput.isPressed()) return; this._escAimHold = false; }
        _SM_processMapTouch2.call(this);
    };

    //=========================================================================
    // v4.0  시네마틱 · 카메라 · 인물 움직이기 · 위 겹침 그림 · 표정 초상화 · 초점 촬영
    //       · 장면 자막 · 글자 자동 맞춤 · 보기 섞기  (데이터에 적었을 때만 켜짐)
    //=========================================================================

    // ---- 글자 자동 맞춤 ------------------------------------------------------
    // 칸 너비에 맞을 때까지 글자 크기를 줄입니다. 돌려주는 값 = 쓴 글자 크기
    function escFitSize(bmp, text, maxW, size, min) {
        size = size || bmp.fontSize; min = min || 12;
        bmp.fontSize = size;
        while (size > min && bmp.measureTextWidth(String(text)) > maxW) { size--; bmp.fontSize = size; }
        return size;
    }
    function escDrawFit(bmp, text, x, y, w, h, align, size, min) {
        escFitSize(bmp, text, w, size, min);
        bmp.drawText(String(text), x, y, w, h, align || 'left');
    }
    // 한 줄에 안 들어가면 두 줄로 (그래도 넘치면 글자를 줄임). { size, lines }
    function escFitWrap(bmp, text, maxW, size, min, maxLines) {
        size = size || bmp.fontSize; min = min || 12; maxLines = maxLines || 2;
        text = String(text);
        bmp.fontSize = size;
        if (bmp.measureTextWidth(text) <= maxW) return { size: size, lines: [text] };
        var s1 = escFitSize(bmp, text, maxW, size, Math.max(min, Math.round(size * 0.86)));
        if (bmp.measureTextWidth(text) <= maxW) return { size: s1, lines: [text] };
        for (var s = size; s >= min; s--) {
            bmp.fontSize = s;
            var lines = wrapText(bmp, text, maxW);
            if (lines.length <= maxLines) return { size: s, lines: lines };
        }
        bmp.fontSize = min;
        return { size: min, lines: wrapText(bmp, text, maxW).slice(0, maxLines) };
    }

    // 위쪽 표시줄: 방 이름이 버튼과 겹치지 않게
    var _v4_refreshHud = Scene_Map.prototype.escRefreshHud;
    Scene_Map.prototype.escRefreshHud = function() {
        var M = EscapeManager;
        var room = M.currentRoom && M.currentRoom();
        var saveName = room ? room.name : null;
        if (room) room.name = ' ';
        _v4_refreshHud.apply(this, arguments);
        if (room) room.name = saveName;
        if (!this._escHud || M._phase === 'error') return;
        var bmp = this._escHud.bitmap;
        var left = SW() - 8;
        if (M._phase === 'play') this.escButtonRects().forEach(function(r) { left = Math.min(left, r.x); });
        if (M._data && M._data.timeLimit) left = Math.min(left, SW() / 2 - 66);
        bmp.textColor = '#ffe9b0';
        escDrawFit(bmp, room ? escSub(saveName || room.id) : '', 14, 0, Math.max(80, left - 24), HUD_H, 'left', 20, 13);
        // 하트는 다칠 수 있는 방에서만
        if (this._escHearts) {
            var hp = room && (room.hearts || room.movers || room.traps || room.drain);
            this._escHearts.visible = !!hp && M._phase === 'play';
        }
        this.escApplyCinemaHud && this.escApplyCinemaHud();
    };

    // 목표: 너무 길면 두 줄
    Scene_Map.prototype.escRefreshGoal = function() {
        if (!this._escGoal) return;
        var g = escSub(EscapeManager._goal);
        this._escGoal.visible = !!g && !EscapeManager._chase && !EscapeManager._mission;
        var maxW = Math.min(620, SW() - 16 - (this._escHearts && this._escHearts.visible ? 190 : 0));
        if (!this._escGoal.bitmap || this._escGoal.bitmap.width !== maxW) this._escGoal.bitmap = new Bitmap(maxW, 60);
        var b = this._escGoal.bitmap;
        b.clear();
        if (!g) return;
        var fit = escFitWrap(b, g, maxW - 70, 18, 13, 2);
        b.fontSize = fit.size;
        var tw = 0; fit.lines.forEach(function(l) { tw = Math.max(tw, b.measureTextWidth(l)); });
        var lh = fit.size + 7, h = fit.lines.length * lh + 9;
        var w = Math.min(maxW - 2, tw + 72);
        roundRect(b, 1, 1, w, h, 14, 'rgba(10,30,50,0.74)', 'rgba(140,210,255,0.8)', 1.5);
        b.fontSize = 18; b.textColor = '#9fe0ff';
        b.drawText('목표', 12, 1, 50, Math.min(h, 30), 'left');
        b.fontSize = fit.size; b.textColor = '#ffffff';
        fit.lines.forEach(function(l, i) { b.drawText(l, 58, 5 + i * lh, w - 64, lh, 'left'); });
    };

    // 추격·미션 막대
    Scene_Map.prototype.escRefreshChase = function() {
        if (!this._escChase) return;
        var c = EscapeManager._chase || EscapeManager._mission;
        this._escChase.visible = !!c;
        if (this._escGoal) this._escGoal.visible = !c && !!EscapeManager._goal;
        if (!c) return;
        var w = Math.min(560, SW() - 40);
        if (this._escChase.bitmap.width !== w) this._escChase.bitmap = new Bitmap(w, 44);
        this._escChase.x = (SW() - w) / 2;
        var b = this._escChase.bitmap;
        b.clear();
        roundRect(b, 2, 2, w - 4, 40, 20, 'rgba(60,10,10,0.85)', 'rgba(255,150,120,0.95)', 2);
        var sec = Math.max(0, Math.ceil(c.frames / 60));
        b.textColor = sec <= 15 ? '#ff9a8a' : '#ffffff';
        var label = escSub(String(c.def.label || '쫓아가자!'));
        escDrawFit(b, label + '   ' + (c.targets.length - c.left.length) + ' / ' + c.targets.length + '   남은 시간 ' + sec + '초', 12, 2, w - 24, 40, 'center', 21, 13);
    };

    // 이름표(조사)
    Scene_Map.prototype.escUpdateTip = function() {
        var f = null;
        if (EscapeManager.canInteract() && !$gamePlayer.isMoving()) f = this.escFacingEvent();
        var label = f ? escSub(f.hotspot.label || f.hotspot.id) : '';
        if (label !== this._escTipText) {
            this._escTipText = label;
            var maxW = Math.min(440, SW() - 8);
            if (this._escTip.bitmap.width !== maxW) this._escTip.bitmap = new Bitmap(maxW, 34);
            var bmp = this._escTip.bitmap;
            bmp.clear();
            if (label) {
                var text = label + '  [조사]';
                var size = escFitSize(bmp, text, maxW - 28, 18, 12);
                var w = Math.min(maxW - 4, bmp.measureTextWidth(text) + 26);
                roundRect(bmp, 2, 2, w, 28, 14, 'rgba(20,14,8,0.85)', 'rgba(255,224,160,0.85)', 1);
                bmp.textColor = '#ffe9b0'; bmp.fontSize = size;
                bmp.drawText(text, 13, 2, w - 22, 28, 'left');
                this._escTipW = w;
            }
        }
        this._escTip.visible = !!label;
        if (f) {
            var ex = f.event.screenX();
            var ey = f.event.screenY() - 64;
            this._escTip.x = Math.max(4, Math.min(SW() - this._escTipW - 4, ex - this._escTipW / 2));
            this._escTip.y = Math.max(HUD_H + 2, ey);
        }
    };

    function escToastDraw(scene, text) {
        var w = Math.min(560, SW() - 40);
        if (scene._escToast.bitmap.width !== w) scene._escToast.bitmap = new Bitmap(w, 40);
        scene._escToast.x = (SW() - w) / 2;
        var b = scene._escToast.bitmap;
        b.clear();
        b.fontSize = 20;
        var size = escFitSize(b, text, w - 40, 20, 13);
        var tw = Math.min(w - 4, b.measureTextWidth(text) + 44);
        roundRect(b, (w - tw) / 2, 2, tw, 36, 18, 'rgba(30,22,10,0.88)', 'rgba(255,214,120,0.95)', 2);
        b.fontSize = size; b.textColor = '#ffe9b0';
        b.drawText(text, 0, 2, w, 36, 'center');
        scene._escToastT = 110;
    }
    Scene_Map.prototype.escShowToast = function(text) { escToastDraw(this, escSub(String(text))); };
    var _v4_itemPopup = Scene_Map.prototype.escItemPopup;
    Scene_Map.prototype.escItemPopup = function(id) {
        _v4_itemPopup.apply(this, arguments);
        var info = (EscapeManager._data.items || {})[id] || { name: id };
        escToastDraw(this, escSub(info.name) + ' 얻음!');
    };

    // 장 제목 카드
    Scene_Map.prototype.escTitleCard = function(text) {
        text = escSub(String(text));
        var parts = text.split('·');
        var top = parts.length > 1 ? parts[0].trim() : '';
        var main = parts.length > 1 ? parts.slice(1).join('·').trim() : text;
        if (this._escCard.bitmap.width !== SW()) this._escCard.bitmap = new Bitmap(SW(), 130);
        var b = this._escCard.bitmap;
        b.clear();
        var ctx = ctxOf(b);
        var g = ctx.createLinearGradient(0, 0, SW(), 0);
        g.addColorStop(0, 'rgba(10,8,6,0)'); g.addColorStop(0.15, 'rgba(10,8,6,0.8)');
        g.addColorStop(0.85, 'rgba(10,8,6,0.8)'); g.addColorStop(1, 'rgba(10,8,6,0)');
        ctx.fillStyle = g; ctx.fillRect(0, 10, SW(), 110); setDirty(b);
        b.fillRect(SW() * 0.15, 12, SW() * 0.7, 2, 'rgba(255,214,120,0.85)');
        b.fillRect(SW() * 0.15, 116, SW() * 0.7, 2, 'rgba(255,214,120,0.85)');
        if (top) { b.textColor = '#ffd27a'; escDrawFit(b, top, 30, 18, SW() - 60, 34, 'center', 22, 14); }
        b.textColor = '#ffffff';
        escDrawFit(b, main, 30, top ? 54 : 36, SW() - 60, 54, 'center', 38, 18);
        this._escCardT = 170;
    };

    // 찾아갈 곳 표시: 이름이 길어도 들어가게
    var _v4_updateMarks = Scene_Map.prototype.escUpdateMarks;
    Scene_Map.prototype.escUpdateMarks = function() {
        var M = EscapeManager, room = M.currentRoom();
        if (!this._escMarks) return;
        var list = [];
        if (room && M._phase === 'play' && !M._cine) {
            toArray(room.hotspots).forEach(function(h) {
                if (h.mark && M.checkCond(h.markIf) && (h.visible === undefined || M.checkCond(h.visible))) list.push(h);
            });
        }
        var key = list.map(function(h) { return h.id; }).join(',');
        if (key !== this._escMarkKey) {
            this._escMarkKey = key;
            this._escMarks.removeChildren();
            this._escMarkList = list.map(function(h) {
                var text = escSub(typeof h.mark === 'string' ? h.mark : (h.label || h.id));
                var BW = 300;
                var bmp = new Bitmap(BW, 64);
                var size = escFitSize(bmp, text, BW - 30, 18, 12);
                var w = Math.min(BW - 6, bmp.measureTextWidth(text) + 26);
                roundRect(bmp, (BW - w) / 2, 2, w, 28, 13, 'rgba(255,214,60,0.95)', 'rgba(90,60,10,0.9)', 2);
                bmp.textColor = '#3a2608'; bmp.outlineWidth = 0; bmp.fontSize = size;
                bmp.drawText(text, 0, 2, BW, 28, 'center');
                var ctx = ctxOf(bmp);
                ctx.fillStyle = 'rgba(255,214,60,0.98)'; ctx.strokeStyle = 'rgba(90,60,10,0.9)'; ctx.lineWidth = 2;
                ctx.beginPath(); ctx.moveTo(BW / 2 - 12, 34); ctx.lineTo(BW / 2 + 12, 34); ctx.lineTo(BW / 2, 52); ctx.closePath(); ctx.fill(); ctx.stroke();
                setDirty(bmp);
                var sp = new Sprite(bmp);
                sp.anchor.x = 0.5; sp.anchor.y = 1;
                return { h: h, sp: sp };
            });
            var self = this;
            this._escMarkList.forEach(function(m) { self._escMarks.addChild(m.sp); });
        }
        var t = Graphics.frameCount, self2 = this;
        this._escMarkList.forEach(function(m, i) {
            var c = self2.escHotspotCenter(m.h.id);
            if (!c) { m.sp.visible = false; return; }
            m.sp.visible = true;
            m.sp.x = Math.max(80, Math.min(SW() - 80, c.x));
            m.sp.y = Math.max(HUD_H + 60, c.y - 34 + Math.sin(t / 10 + i) * 5);
        });
    };

    // 선택지: 너무 긴 보기는 글자를 줄이고, 그래도 넘치면 두 줄 칸
    Window_EscChoice.prototype.itemHeight = function() { return this._twoLine ? 60 : this.lineHeight(); };
    Window_EscChoice.prototype.windowHeight = function() { return this.fittingHeight(this._options.length); };
    Window_EscChoice.prototype.fittingHeight = function(n) { return n * this.itemHeight() + this.standardPadding() * 2; };
    var _v4_choiceSetup = Window_EscChoice.prototype.setup;
    Window_EscChoice.prototype.setup = function(options, bottomY) {
        this._options = options.slice(0, 8).map(function(o) { return escSub(o); });
        this.width = this.windowWidth();
        var probe = this.contents, inner = this.width - this.standardPadding() * 2 - this.textPadding() * 2 - 8;
        this._twoLine = false;
        var marks = ['①', '②', '③', '④', '⑤', '⑥', '⑦', '⑧'];
        for (var i = 0; i < this._options.length; i++) {
            probe.fontSize = 17;
            if (probe.measureTextWidth(marks[i] + ' ' + this._options[i]) > inner) this._twoLine = true;
        }
        this.createContents();
        _v4_choiceSetup.call(this, this._options, bottomY);
        this.height = this.fittingHeight(this._options.length);
        this.y = Math.max(HUD_H + 4, bottomY - this.height - 44);
        this.createContents();
        this.refresh();
    };
    Window_EscChoice.prototype.drawItem = function(index) {
        var rect = this.itemRectForText(index);
        var text = this.commandName(index);
        var b = this.contents;
        this.resetTextColor();
        this.changePaintOpacity(this.isCommandEnabled(index));
        if (!this._twoLine) {
            escDrawFit(b, text, rect.x, rect.y, rect.width, rect.height, 'left', 22, 15);
        } else {
            var fit = escFitWrap(b, text, rect.width, 19, 13, 2);
            var lh = fit.size + 6, top = rect.y + (rect.height - lh * fit.lines.length) / 2;
            b.fontSize = fit.size;
            fit.lines.forEach(function(l, i) { b.drawText(l, rect.x + (i > 0 ? 22 : 0), top + i * lh, rect.width - (i > 0 ? 22 : 0), lh, 'left'); });
        }
        this.resetFontSettings();
    };

    // 가방 줄
    Window_EscBag.prototype.windowWidth = function() { return Math.min(560, SW() - 40); };
    var _v4_bagSetup = Window_EscBag.prototype.setup;
    Window_EscBag.prototype.setup = function(rows, index) {
        this.width = this.windowWidth(); this.x = (SW() - this.width) / 2;
        _v4_bagSetup.call(this, rows, index);
    };
    Window_EscBag.prototype.drawItem = function(index) {
        var r = this._rows[index];
        var rect = this.itemRect(index);
        this.resetFontSettings();
        if (r.hint) {
            roundRect(this.contents, rect.x + 2, rect.y + 4, rect.width - 4, rect.height - 8, 8,
                r.enabled === false ? 'rgba(90,90,90,0.5)' : 'rgba(200,150,60,0.55)', null);
        }
        var tx = rect.x + 12;
        if (r.image) {
            var bmp = this._icons[r.image];
            if (!bmp) {
                bmp = ImageManager.loadPicture(r.image);
                this._icons[r.image] = bmp;
                bmp.addLoadListener(this.refresh.bind(this));
            }
            if (bmp.isReady() && bmp.width > 0) {
                var s = Math.min(40 / bmp.width, 40 / bmp.height);
                var dw = Math.floor(bmp.width * s), dh = Math.floor(bmp.height * s);
                this.contents.blt(bmp, 0, 0, bmp.width, bmp.height, rect.x + 8 + (40 - dw) / 2, rect.y + (rect.height - dh) / 2, dw, dh);
            }
            tx = rect.x + 58;
        }
        this.changePaintOpacity(r.enabled !== false);
        escDrawFit(this.contents, escSub(r.text), tx, rect.y, rect.width - (tx - rect.x) - 8, rect.height, 'left', 22, 14);
        this.changePaintOpacity(true);
    };

    // 다이얼 칸 이름표
    var _v4_dialRefresh = Window_EscDial.prototype.refresh;
    Window_EscDial.prototype.titleH = function() { return (this._title || (this._v4In && this._v4Title)) ? 34 : 0; };
    Window_EscDial.prototype.refresh = function() {
        var labels = this._labels; this._labels = labels.map(function() { return ''; });
        var title = this._title; this._v4Title = title; this._v4In = true; this._title = '';
        _v4_dialRefresh.call(this);
        this._labels = labels; this._title = title; this._v4In = false;
        var b = this.contents;
        if (title) { b.textColor = '#ffe9b0'; escDrawFit(b, escSub(title), 0, 0, this.contentsWidth(), 28, 'center', 18, 12); }
        for (var i = 0; i < this._slots.length; i++) {
            if (!labels[i]) continue;
            b.textColor = this.systemColor();
            escDrawFit(b, escSub(String(labels[i])), this.slotX(i) - 6, this.titleH(), this._slotW + 12, 26, 'center', 16, 11);
        }
    };

    // 타이밍 창 제목
    var _v4_timingRefresh = Window_EscTiming.prototype.refresh;
    Window_EscTiming.prototype.refresh = function() {
        var def = this._def || {}, lab = def.label;
        if (this._def) this._def.label = ' ';
        _v4_timingRefresh.call(this);
        if (this._def) this._def.label = lab;
        var c = this.contents; if (!c) return;
        c.textColor = '#ffe9b0';
        escDrawFit(c, escSub(lab || '타이밍'), 0, 0, this.contentsWidth(), 32, 'center', 22, 13);
        this.resetTextColor();
    };

    // ---- 보기 섞기 ---------------------------------------------------------------
    var _v4_startChoice = EscapeManager.startChoice;
    EscapeManager.startChoice = function(s) {
        var d = this._data || {};
        if (d.shuffleChoices && s.shuffle !== false && Number(s.answer || 0) > 0 && toArray(s.choice).length > 1) {
            var opts = toArray(s.choice).map(function(o, i) { return { o: o, i: i + 1 }; });
            for (var k = opts.length - 1; k > 0; k--) { var j = Math.floor(Math.random() * (k + 1)); var t = opts[k]; opts[k] = opts[j]; opts[j] = t; }
            var s2 = {}; Object.keys(s).forEach(function(key) { s2[key] = s[key]; });
            s2.choice = opts.map(function(x) { return x.o; });
            var ans = Number(s.answer);
            for (var q = 0; q < opts.length; q++) if (opts[q].i === ans) s2.answer = q + 1;
            this._choiceAnswer = s2.answer;
            _v4_startChoice.call(this, s2);
        } else {
            this._choiceAnswer = Number(s.answer || 0);
            _v4_startChoice.call(this, s);
        }
        // 확대 그림이 떠 있으면 선택지 위쪽에 맞춰 줄이기
        var sc = this._scene;
        if (sc && sc.escCloseupVisible && sc.escCloseupVisible() && sc._escChoice) sc.escFitCloseup(sc._escChoice.y - 6);
    };

    // 확대 그림(사료 카드 등)이 떠 있는 동안에는 목표 상자를 숨겨 카드 제목을 가리지 않게
    var _v4_mapUpdateGoal = Scene_Map.prototype.update;
    Scene_Map.prototype.update = function() {
        _v4_mapUpdateGoal.apply(this, arguments);
        if (this._escGoal) this._escGoal.opacity = ((this._escCloseupName || EscapeManager._cine || EscapeManager._gameOpen) ? 0 : 255);
    };

    var _v4_startDial = EscapeManager.startDial;
    EscapeManager.startDial = function(s) {
        this._dialAnswer = toArray(s.dial && s.dial.answer).map(String);
        return _v4_startDial.apply(this, arguments);
    };

    // ---- 조건 any (여러 조건 중 하나) ---------------------------------------------
    var _v4_checkCond = EscapeManager.checkCond;
    EscapeManager.checkCond = function(c) {
        if (!c) return true;
        if (c.any) {
            var self = this;
            if (!toArray(c.any).some(function(x) { return self.checkCond(x); })) return false;
        }
        if (c.vars) {
            var v = this._vars || {}, ok = true;
            Object.keys(c.vars).forEach(function(k) { if (String(v[k]) !== String(c.vars[k])) ok = false; });
            if (!ok) return false;
        }
        return _v4_checkCond.call(this, c);
    };

    // ---- 인물 찾기 / 움직이기 ------------------------------------------------------
    EscapeManager.charByName = function(name) {
        if (name === 'player' || name === '주인공') return $gamePlayer;
        var list = $gameMap.events().filter(function(e) { return !e._erased && String(e.event().name).trim() === String(name); });
        return list[0] || null;
    };
    EscapeManager.charsByName = function(name) {
        if (name === 'player' || name === '주인공') return [$gamePlayer];
        return $gameMap.events().filter(function(e) { return !e._erased && String(e.event().name).trim() === String(name); });
    };
    EscapeManager.startMove = function(def) {
        var self = this;
        var chars = this.charsByName(def.event);
        if (!chars.length) return false;
        this._moves = this._moves || [];
        var made = false;
        chars.forEach(function(ch, k) {
            if (k > 0 && !def.all) return;
            var route = def.route ? toArray(def.route).map(function(p) { return [Number(p[0]), Number(p[1])]; }) : [];
            if (def.to) route = [[Number(def.to[0]), Number(def.to[1])]];
            if (def.by) route = [[ch.x + Number(def.by[0]), ch.y + Number(def.by[1])]];
            if (def.away) {
                var dx = ch.x - $gamePlayer.x, dy = ch.y - $gamePlayer.y;
                var ax = Math.abs(dx) >= Math.abs(dy) ? (dx >= 0 ? 1 : -1) : 0, ay = ax === 0 ? (dy >= 0 ? 1 : -1) : 0;
                route = [[ch.x + ax * Number(def.away), ch.y + ay * Number(def.away)]];
            }
            var old = self._moves.filter(function(o) { return o.ch === ch; })[0];
            var m = { ch: ch, route: route, idx: 0, def: def, stuck: 0, through: def.through !== false && ch !== $gamePlayer,
                      speed0: old ? old.speed0 : ch.moveSpeed() };
            if (def.speed) ch.setMoveSpeed(Number(def.speed));
            if (m.through) ch.setThrough(true);
            if (ch !== $gamePlayer && ch._escHidden) { ch._escHidden = false; ch.setTransparent(false); }
            self._moves = self._moves.filter(function(o) { return o.ch !== ch; });
            self._moves.push(m);
            made = true;
        });
        if (made && def.wait !== false) { this._waiting = true; this._moveWait = true; }
        return made;
    };
    EscapeManager.updateMoves = function() {
        if (!this._moves || !this._moves.length) return;
        var self = this;
        this._moves = this._moves.filter(function(m) {
            var ch = m.ch;
            if (ch.isMoving()) return true;
            var tgt = m.route[m.idx];
            if (!tgt) {
                if (m.def.dir) ch.setDirection(toDir(m.def.dir));
                if (m.def.speed && m.speed0) ch.setMoveSpeed(m.speed0);     // v4.1: 연출이 끝나면 원래 걸음 속도로
                if (m.through && ch !== $gamePlayer && !m.def.keepThrough) ch.setThrough(false);
                if (m.def.erase && ch.erase) ch.erase();
                return false;
            }
            if (ch.x === tgt[0] && ch.y === tgt[1]) { m.idx++; m.stuck = 0; return true; }
            var d;
            if (m.through) {
                var dx = tgt[0] - ch.x, dy = tgt[1] - ch.y;
                d = Math.abs(dx) >= Math.abs(dy) ? (dx > 0 ? 6 : 4) : (dy > 0 ? 2 : 8);
            } else {
                d = ch.findDirectionTo(tgt[0], tgt[1]);
            }
            if (d > 0) {
                var bx = ch.x, by = ch.y;
                ch.moveStraight(d);
                if (ch.x === bx && ch.y === by && !ch.isMoving()) {
                    if (++m.stuck > 40) { ch.locate(tgt[0], tgt[1]); m.idx++; m.stuck = 0; }
                }
            } else if (++m.stuck > 40) { ch.locate(tgt[0], tgt[1]); m.idx++; m.stuck = 0; }
            return true;
        });
        var still = this._moves.some(function(m) { return m.def.wait !== false; });
        if (this._moveWait && !still) { this._moveWait = false; this.resume(); }
    };

    // ---- 카메라 (확대·천천히 옮기기) -------------------------------------------------
    // 지도 칸 좌표(tx, ty)가 화면 가운데에 오도록 scale 배로 확대
    EscapeManager.camTarget = function(def) {
        var tw = $gameMap.tileWidth(), th = $gameMap.tileHeight();
        var tx, ty;
        if (def.event) {
            var list = this.charsByName(def.event);
            if (list.length) {
                tx = 0; ty = 0;
                list.forEach(function(c) { tx += c._realX; ty += c._realY; });
                tx /= list.length; ty /= list.length;
            }
        }
        if (tx === undefined && def.x !== undefined) { tx = Number(def.x); ty = Number(def.y); }
        if (tx === undefined) { tx = $gamePlayer._realX; ty = $gamePlayer._realY; }
        tx += Number(def.dx || 0); ty += Number(def.dy || 0);
        var px = ($gameMap.adjustX(tx) + 0.5) * tw, py = ($gameMap.adjustY(ty) + 0.5) * th - 12;
        return { px: px, py: py, s: Number(def.scale || 1.5) };
    };
    EscapeManager.startCam = function(def) {
        var cur = this._cam || { px: SW() / 2, py: SH() / 2, s: 1 };
        if (def === false || def === null || def.reset) {
            this._cam = { px: cur.px, py: cur.py, s: cur.s, from: cur, to: { px: SW() / 2, py: SH() / 2, s: 1 },
                          t: 0, dur: Math.max(1, Number((def && def.duration) || 40)), end: true };
            return;
        }
        var to = this.camTarget(def);
        this._cam = { px: cur.px, py: cur.py, s: cur.s, from: { px: cur.px, py: cur.py, s: cur.s }, to: to,
                      t: 0, dur: Math.max(1, Number(def.duration || 50)), follow: def.follow ? def : null };
        if (def.wait) this._waitCount = Math.max(this._waitCount, this._cam.dur);
    };
    EscapeManager.updateCam = function() {
        var c = this._cam; if (!c) return;
        if (c.t < c.dur) c.t++;
        var k = c.t / c.dur; k = k * k * (3 - 2 * k);
        if (c.follow && c.t >= c.dur) c.to = this.camTarget(c.follow);
        c.px = c.from.px + (c.to.px - c.from.px) * k;
        c.py = c.from.py + (c.to.py - c.from.py) * k;
        c.s = c.from.s + (c.to.s - c.from.s) * k;
        var s = Math.max(1, c.s), W = SW(), H = SH();
        var zx, zy;
        if (s <= 1.0001) { zx = W / 2; zy = H / 2; }
        else {
            zx = (c.px * s - W / 2) / (s - 1);
            zy = (c.py * s - H / 2) / (s - 1);
        }
        zx = Math.max(0, Math.min(W, zx)); zy = Math.max(0, Math.min(H, zy));
        $gameScreen._zoomX = zx; $gameScreen._zoomY = zy; $gameScreen._zoomScale = s;
        $gameScreen._zoomDuration = 0; $gameScreen._zoomScaleTarget = s;
        if (c.end && c.t >= c.dur) { this._cam = null; $gameScreen.clearZoom(); }
    };

    // ---- 시네마틱 (위아래 검은 띠 + 장면 자막) --------------------------------------
    EscapeManager.setCinema = function(on) {
        this._cine = !!on;
        if (this._scene && this._scene.escApplyCinemaHud) this._scene.escApplyCinemaHud();
    };

    // ---- 단계 추가 ---------------------------------------------------------------
    var _v4_processStep = EscapeManager.processStep;
    EscapeManager.processStep = function(s) {
        if (typeof s === 'string') s = { text: s };
        if (!s || typeof s !== 'object') return;
        var self = this, scene = this._scene;
        if (s.setVar) Object.keys(s.setVar).forEach(function(k) { self._vars[k] = s.setVar[k]; });
        if (s.weather !== undefined) {
            var wt = s.weather || {};
            $gameScreen.changeWeather(String(wt.type || 'none'), Number(wt.power || 0), Number(wt.duration || 30));
        }
        if (s.heroImage) this.setHeroImage(String(s.heroImage));
        if (s.cinema !== undefined) this.setCinema(s.cinema);
        if (s.caption !== undefined && scene && scene.escCaption) scene.escCaption(s.caption, s.captionTime);
        if (s.zoom !== undefined) this.startCam(s.zoom);
        if (s.place) toArray(s.place).forEach(function(p) {
            self.charsByName(p.event).forEach(function(ch, k) {
                if (k > 0 && !p.all) return;
                if (p.x !== undefined) ch.locate(Number(p.x), Number(p.y));
                if (p.dir) ch.setDirection(toDir(p.dir));
                if (p.toward === 'player' && ch.turnTowardPlayer) ch.turnTowardPlayer();
                if (p.opacity !== undefined) ch.setOpacity(Number(p.opacity));
            });
        });
        if (s.turn) toArray(s.turn).forEach(function(p) {
            self.charsByName(p.event).forEach(function(ch) {
                if (p.toward === 'player' && ch.turnTowardPlayer) ch.turnTowardPlayer();
                else if (p.toward && p.toward !== 'player') { var o = self.charByName(p.toward); if (o) ch.turnTowardCharacter(o); }
                else ch.setDirection(toDir(p.dir));
            });
        });
        if (s.balloon) toArray(s.balloon).forEach(function(p) {
            var ch = self.charByName(p.event || 'player'); if (ch) ch.requestBalloon(Number(p.id || 1));
        });
        if (s.move) {
            var any = false;
            toArray(s.move).forEach(function(m) { if (self.startMove(m)) any = true; });
            var rest = {}; Object.keys(s).forEach(function(k) {
                if (['move', 'setVar', 'heroImage', 'cinema', 'caption', 'captionTime', 'zoom', 'place', 'turn', 'balloon', 'weather'].indexOf(k) < 0) rest[k] = s[k];
            });
            if (this._moveWait) { if (Object.keys(rest).length) this.insertSteps([rest]); return; }
            if (Object.keys(rest).length) return _v4_processStep.call(this, rest);
            return;
        }
        if (s.focus) { this.startFocus(s); return _v4_processStep.call(this, this.stepWithout(s, ['focus', 'text', 'speaker'])); }
        return _v4_processStep.call(this, s);
    };
    EscapeManager.stepWithout = function(s, keys) {
        var o = {}; Object.keys(s).forEach(function(k) {
            if (keys.indexOf(k) < 0 && ['setVar', 'heroImage', 'cinema', 'caption', 'captionTime', 'zoom', 'place', 'turn', 'balloon', 'move'].indexOf(k) < 0) o[k] = s[k];
        });
        return o;
    };

    // 주인공 그림 바꾸기 (나이가 들면)
    EscapeManager.setHeroImage = function(name) {
        this._baseImage = name;
        var lead = $gameParty.leader();
        if (lead && lead.characterName() !== name) { lead.setCharacterImage(name, 0); $gamePlayer.refresh(); }
    };

    var _v4_update = EscapeManager.update;
    EscapeManager.update = function(scene) {
        if (this.isActive() && scene === this._scene) {
            this.updateMoves();
            this.updateCam();
        }
        _v4_update.apply(this, arguments);
        if (this.isActive() && scene === this._scene && this._cine && this._phase === 'play' && this.canInteract() && !this._moveWait) {
            this.setCinema(false);
            if (scene.escCaption) scene.escCaption('');
            if (this._cam && !this._cam.end) this.startCam(false);
        }
    };

    // 다른 방으로 가면 움직임·카메라 정리
    var _v4_onSceneStart = EscapeManager.onSceneStart;
    EscapeManager.onSceneStart = function(scene) {
        (this._moves || []).forEach(function(m) { if (m.ch === $gamePlayer && m.def.speed && m.speed0) $gamePlayer.setMoveSpeed(m.speed0); });
        this._moves = [];
        if (this._moveWait) { this._moveWait = false; this._waiting = false; }
        this._cam = null;
        if ($gameScreen) $gameScreen.clearZoom();
        _v4_onSceneStart.apply(this, arguments);
        if (scene.escApplyCinemaHud) scene.escApplyCinemaHud();
    };

    var _v4_reset = EscapeManager.reset;
    EscapeManager.reset = function() {
        _v4_reset.apply(this, arguments);
        this._moves = []; this._moveWait = false; this._cam = null; this._cine = false; this._focus = null;
    };

    // 플레이어가 움직이는 동안(대본 이동) 입력 막기
    var _v4_canMove = Game_Player.prototype.canMove;
    Game_Player.prototype.canMove = function() {
        var M = EscapeManager;
        if (M.isActive() && M._moves && M._moves.some(function(m) { return m.ch === $gamePlayer; })) return false;
        if (M.isActive() && M._focus) return false;
        return _v4_canMove.call(this);
    };

    // ---- 화면: 검은 띠 · 자막 · 확대 맞추기 -------------------------------------------
    var _v4_createLayer = Scene_Map.prototype.escCreateLayer;
    Scene_Map.prototype.escCreateLayer = function() {
        _v4_createLayer.apply(this, arguments);
        var at = this.getChildIndex(this._escHud);
        this._escLetterbox = new PIXI.Graphics();
        this._escLetterboxH = 0;
        this.addChildAt(this._escLetterbox, at);
        this._escCap = new Sprite(new Bitmap(SW(), 64));
        this._escCap.opacity = 0;
        this._escCapT = 0;
        this.addChildAt(this._escCap, at + 1);
        // 초상화 (말하는 사람)
        this._escPortrait = new Sprite();
        this._escPortrait.anchor.x = 0.5; this._escPortrait.anchor.y = 1;
        this._escPortrait.opacity = 0;
        this._escPortraitKey = '';
        this.addChildAt(this._escPortrait, this.getChildIndex(this._escCloseup) + 1);
    };

    Scene_Map.prototype.escApplyCinemaHud = function() {
        var on = !!EscapeManager._cine;
        var list = [this._escHud, this._escGoal, this._escHearts, this._escBowBtn];
        list.forEach(function(sp) { if (sp) sp.alpha = on ? 0 : 1; });
    };

    Scene_Map.prototype.escCaption = function(text, time) {
        text = escSub(text || '');
        this._escCapText = text;
        var b = this._escCap.bitmap;
        if (b.width !== SW()) { this._escCap.bitmap = b = new Bitmap(SW(), 64); }
        b.clear();
        if (!text) { this._escCapT = Math.min(this._escCapT, 20); return; }
        this._escCapT = Number(time || 300);
        this._escCapShown = 0;
    };

    Scene_Map.prototype.escDrawCaption = function() {
        var text = this._escCapText || '';
        var b = this._escCap.bitmap;
        b.clear();
        if (!text) return;
        var shown = text.substring(0, Math.floor(this._escCapShown));
        var cine = !!EscapeManager._cine;
        var size = escFitSize(b, text, SW() - 80, cine ? 24 : 21, 14);
        var tw = b.measureTextWidth(text);
        if (!cine) roundRect(b, (SW() - tw) / 2 - 22, 8, tw + 44, 42, 10, 'rgba(8,8,10,0.66)', 'rgba(255,226,170,0.6)', 1);
        b.fontSize = size; b.textColor = '#f5e6c4';
        b.outlineColor = 'rgba(0,0,0,0.8)'; b.outlineWidth = 4;
        b.drawText(shown, (SW() - tw) / 2, 8, tw + 4, 42, 'left');
        b.outlineWidth = 4;
    };

    var _v4_updateFx = Scene_Map.prototype.escUpdateFx;
    Scene_Map.prototype.escUpdateFx = function() {
        _v4_updateFx.apply(this, arguments);
        // 확대: 효과 층도 지도와 똑같이
        if (this._escFx && this._spriteset) {
            this._escFx.scale.x = this._spriteset.scale.x; this._escFx.scale.y = this._spriteset.scale.y;
            this._escFx.x = this._spriteset.x; this._escFx.y = this._spriteset.y;
        }
        // v4.1: 시네마틱 검은 띠가 있을 때 확대 그림(카드)이 띠에 가리지 않게 띠 아래 ~ 대화창 위에 맞춤
        var cu = this._escCloseup;
        if (cu && cu.visible && cu.bitmap && cu.bitmap.isReady() && cu.bitmap.width > 0) {
            var bh = EscapeManager._cine ? Math.round(SH() * 0.115) : 0;
            var key2 = bh + ':' + cu.bitmap.width + ':' + (this._escMsg ? this._escMsg.y : 0);
            if (bh > 0 && this._escCuFitKey !== key2) {
                if (!this._escCuOrig || this._escCuOrig.bmp !== cu.bitmap) this._escCuOrig = { bmp: cu.bitmap, sx: cu.scale.x, y: cu.y };
                var top = bh + 8, bottom = (this._escMsg && this._escMsg.isOpen() ? this._escMsg.y : SH() - bh) - 8;
                var sc = Math.min(this._escCuOrig.sx, (bottom - top) / cu.bitmap.height, (SW() - 40) / cu.bitmap.width);
                cu.scale.x = cu.scale.y = sc;
                cu.y = top + (bottom - top) / 2;
                this._escCuFitKey = key2;
            } else if (bh === 0 && this._escCuFitKey && this._escCuOrig && this._escCuOrig.bmp === cu.bitmap) {
                cu.scale.x = cu.scale.y = this._escCuOrig.sx; cu.y = this._escCuOrig.y; this._escCuFitKey = '';
            }
        } else if (this._escCuFitKey) { this._escCuFitKey = ''; this._escCuOrig = null; }
        // 검은 띠
        var g = this._escLetterbox;
        if (g) {
            var want = (EscapeManager._cine && !this._escCloseupName) ? Math.round(SH() * 0.115) : 0;   // 카드가 뜨면 검은 띠를 걷어 카드가 잘리지 않게
            var h = this._escLetterboxH;
            h += (want - h) * 0.12;
            if (Math.abs(want - h) < 0.6) h = want;
            this._escLetterboxH = h;
            g.clear();
            if (h > 0.5) {
                g.beginFill(0x000000, 1);
                g.drawRect(0, 0, SW(), h);
                g.drawRect(0, SH() - h, SW(), h);
                g.endFill();
            }
        }
        // 자막
        if (this._escCap) {
            if (this._escCapT > 0) {
                this._escCapT--;
                if (this._escCapText && this._escCapShown < this._escCapText.length) { this._escCapShown += 0.5; this.escDrawCaption(); }
                this._escCap.opacity = Math.min(255, this._escCap.opacity + 20);
                if (this._escCapT < 20) this._escCap.opacity = this._escCapT / 20 * 255;
            } else this._escCap.opacity = 0;
            var lb = this._escLetterboxH || 0;
            this._escCap.y = lb > 20 ? Math.max(0, lb / 2 - 28) : HUD_H + 4 + (this._escGoal && this._escGoal.visible ? 40 : 0);
        }
        this.escUpdatePortrait();
    };

    // ---- 표정 초상화 ---------------------------------------------------------------
    //  데이터 "portraits": { "말하는 사람": "그림 앞 이름" }  예) { "{name}": "pt_hg{age}", "아버지": "pt_dad" }
    //  데이터 "portraitFiles": [ 실제로 있는 그림 이름 목록 ]
    //  단계 "face": "웃음" → pt_hg15_smile.png  (보통 n · 웃음 smile · 놀람 surprise · 슬픔 sad · 화남 angry · 결심 resolve · 걱정 worry)
    var FACE_KEYS = { '보통': 'n', '웃음': 'smile', '놀람': 'surprise', '슬픔': 'sad', '화남': 'angry', '결심': 'resolve', '걱정': 'worry', '생각': 'think' };
    EscapeManager.portraitFor = function(speaker, face) {
        var d = this._data || {}, map = d.portraits;
        if (!map || !speaker) return null;
        var raw = String(speaker), key = null;
        if (map[raw] !== undefined) key = raw;
        else if (map[escSub(raw)] !== undefined) key = escSub(raw);
        else {
            var sub = escSub(raw);
            Object.keys(map).forEach(function(k) { if (!key && escSub(k) === sub) key = k; });
        }
        if (!key) return null;
        var base = escSub(map[key]);
        var suf = FACE_KEYS[face] || face || 'n';
        var files = d.portraitFiles || [];
        var name = base + '_' + suf;
        if (files.indexOf(name) < 0 || !hasAsset('pic', name)) name = base + '_n';
        if (files.indexOf(name) < 0 || !hasAsset('pic', name)) return null;
        var left = escSub(raw) === escSub('{name}') || (d.heroSpeakers || []).indexOf(raw) >= 0;
        return { name: name, left: left };
    };
    var _v4_say = Window_EscMessage.prototype.say;
    Window_EscMessage.prototype.say = function(text, speaker, callback, waitInput) {
        var M = EscapeManager;
        this._escFace = M._sayFace || '';
        this._escSpeaker = speaker || '';
        M._sayFace = '';
        _v4_say.apply(this, arguments);
    };
    var _v4_ps_text = EscapeManager.processStep;
    EscapeManager.processStep = function(s) {
        if (s && typeof s === 'object') this._sayFace = s.face || '';
        return _v4_ps_text.apply(this, arguments);
    };
    Scene_Map.prototype.escUpdatePortrait = function() {
        var sp = this._escPortrait; if (!sp) return;
        var M = EscapeManager, msg = this._escMsg;
        var modal = (this._escChoice && this._escChoice.isOpen()) || (this._escNumpad && this._escNumpad.isOpen()) ||
            (this._escDial && this._escDial.isOpen()) || (this._escTiming && this._escTiming.isOpen()) || !!M._focus ||
            this.escCloseupVisible() || M._bagOpen;
        var info = null;
        if (msg && msg.isOpen() && msg._pages && msg._pages.length && !modal) info = M.portraitFor(msg._escSpeaker, msg._escFace);
        var key = info ? info.name + (info.left ? 'L' : 'R') : '';
        if (key !== this._escPortraitKey) {
            var was = this._escPortraitKey;
            this._escPortraitKey = key;
            if (info) {
                var sameSide = was && was.slice(-1) === key.slice(-1) && sp.opacity > 120;
                sp.bitmap = ImageManager.loadPicture(info.name);
                sp._left = info.left;
                sp._pop = sameSide ? 8 : 0;
                sp._slide = sameSide ? 0 : 14;
                if (!sameSide) sp.opacity = 0;
            }
        }
        var h = msg ? msg.y : SH() - 150;
        if (info) {
            var bw = sp.bitmap && sp.bitmap.width > 1 ? sp.bitmap.width : 240;
            var bh = sp.bitmap && sp.bitmap.height > 1 ? sp.bitmap.height : 264;
            var room = h - HUD_H - 16;
            var sc = Math.min(1, room / bh, (SW() * 0.34) / bw);
            var pop = sp._pop > 0 ? 1 + Math.sin(sp._pop / 8 * Math.PI) * 0.035 : 1;
            if (sp._pop > 0) sp._pop--;
            sp.scale.x = sp.scale.y = sc * pop;
            var half = bw * sc / 2;
            var off = sp._slide > 0 ? sp._slide * 3 : 0;
            if (sp._slide > 0) sp._slide--;
            sp.x = sp._left ? 18 + half - off : SW() - 18 - half + off;
            sp.y = h + 12;
            sp.opacity = Math.min(255, sp.opacity + 36);
            sp._w = bw * sc;
        } else {
            sp.opacity = Math.max(0, sp.opacity - 40);
        }
        // 왼쪽 초상화가 있으면 이름표를 그 오른쪽으로
        var nw = this._escName;
        if (nw && msg) {
            var leftOn = info && info.left;
            var want = leftOn ? msg.x + 8 + Math.round(sp._w || 0) + 6 : msg.x + 8;
            if (nw.x !== want) nw.x = want;
        }
    };

    // ---- 초점 촬영 -------------------------------------------------------------------
    //  { "focus": { "picture": "fo_xxx", "label": "...", "goal": 1, "film": 4, "speed": 1, "zone": 0.16,
    //               "move": true, "smoke": true, "crowd": true, "flash": true, "success": [...], "fail": [...] } }
    //  흐렸다 또렷해졌다를 되풀이하는 사진에서 가장 또렷한 순간에 셔터(Enter · 클릭 · 톡)
    EscapeManager.startFocus = function(s) {
        var self = this, def = s.focus;
        this._waiting = true;
        this._focus = def;
        this.hideCloseup();
        $gameTemp.clearDestination();
        this._scene.escStartFocus(def, function(ok) {
            self._focus = null;
            self.insertSteps(toArray(ok ? def.success : (def.fail || [{ text: '필름을 다 썼다... 다시 해 보자.' }])).concat(ok || def.retry === false ? [] : [{ focus: def }]));
            self.resume();
        });
    };

    function focusFrameBitmap(fw, fh) {
        var b = new Bitmap(fw, fh), c = ctxOf(b);
        c.strokeStyle = 'rgba(255,255,255,0.85)'; c.lineWidth = 3;
        var L = Math.round(Math.min(fw, fh) * 0.09);
        [[8, 8, 1, 1], [fw - 8, 8, -1, 1], [8, fh - 8, 1, -1], [fw - 8, fh - 8, -1, -1]].forEach(function(p) {
            c.beginPath(); c.moveTo(p[0], p[1] + L * p[3]); c.lineTo(p[0], p[1]); c.lineTo(p[0] + L * p[2], p[1]); c.stroke();
        });
        c.strokeStyle = 'rgba(255,255,255,0.22)'; c.lineWidth = 1;
        for (var i = 1; i < 3; i++) {
            c.beginPath(); c.moveTo(fw * i / 3, 0); c.lineTo(fw * i / 3, fh); c.stroke();
            c.beginPath(); c.moveTo(0, fh * i / 3); c.lineTo(fw, fh * i / 3); c.stroke();
        }
        var r = Math.round(Math.min(fw, fh) * 0.11);
        c.strokeStyle = 'rgba(255,255,255,0.8)'; c.lineWidth = 2;
        c.beginPath(); c.arc(fw / 2, fh / 2, r, 0, Math.PI * 2); c.stroke();
        c.beginPath(); c.moveTo(fw / 2 - r, fh / 2); c.lineTo(fw / 2 + r, fh / 2); c.stroke();
        var g = c.createRadialGradient(fw / 2, fh / 2, Math.min(fw, fh) * 0.35, fw / 2, fh / 2, Math.max(fw, fh) * 0.62);
        g.addColorStop(0, 'rgba(0,0,0,0)'); g.addColorStop(1, 'rgba(0,0,0,0.45)');
        c.fillStyle = g; c.fillRect(0, 0, fw, fh);
        setDirty(b);
        return b;
    }
    function focusPuffBitmap(r, rgb) {
        var b = new Bitmap(r * 2, r * 2), c = ctxOf(b);
        var g = c.createRadialGradient(r, r, 0, r, r, r);
        g.addColorStop(0, 'rgba(' + rgb + ',0.92)'); g.addColorStop(0.6, 'rgba(' + rgb + ',0.6)'); g.addColorStop(1, 'rgba(' + rgb + ',0)');
        c.fillStyle = g; c.fillRect(0, 0, r * 2, r * 2); setDirty(b);
        return b;
    }
    function focusHeadBitmap(w, h) {
        var b = new Bitmap(w, h), c = ctxOf(b);
        c.fillStyle = 'rgba(14,12,12,0.96)';
        c.beginPath(); c.ellipse(w / 2, h * 0.36, w * 0.24, h * 0.3, 0, 0, Math.PI * 2); c.fill();
        c.beginPath(); c.ellipse(w / 2, h * 1.05, w * 0.5, h * 0.42, 0, 0, Math.PI * 2); c.fill();
        setDirty(b);
        return b;
    }

    Scene_Map.prototype.escStartFocus = function(def, done) {
        var self = this;
        var L = new Sprite();
        var W = SW(), H = SH();
        var fw = Math.min(W - 70, Math.round((H - 200) * 16 / 9)), fh = Math.round(fw * 9 / 16);
        var fx = Math.round((W - fw) / 2), fy = Math.round(HUD_H + 54 + (H - HUD_H - 54 - 120 - fh) / 2);
        var back = new Sprite(new Bitmap(W, H)); back.bitmap.fillAll('rgba(6,6,8,0.9)'); L.addChild(back);
        var box = new Sprite(); box.x = fx; box.y = fy; L.addChild(box);
        var mask = new PIXI.Graphics(); mask.beginFill(0xffffff); mask.drawRect(fx, fy, fw, fh); mask.endFill();
        L.addChild(mask); box.mask = mask;
        var photo = new Sprite(ImageManager.loadPicture(def.picture));
        photo.anchor.x = photo.anchor.y = 0.5; photo.x = fw / 2; photo.y = fh / 2;
        var blur = PIXI.filters && PIXI.filters.BlurFilter ? new PIXI.filters.BlurFilter(0, 3) : null;
        if (blur) photo.filters = [blur];
        box.addChild(photo);
        var obst = new Sprite(); box.addChild(obst);
        var tint = new Sprite(new Bitmap(fw, fh)); tint.bitmap.fillAll('#f4ead2'); tint.opacity = 0; box.addChild(tint);
        var frame = new Sprite(focusFrameBitmap(fw, fh)); box.addChild(frame);
        var info = new Sprite(new Bitmap(W, H)); L.addChild(info);
        var flash = new Sprite(new Bitmap(W, H)); flash.bitmap.fillAll('#ffffff'); flash.opacity = 0; L.addChild(flash);
        var print = new Sprite(); print.anchor.x = print.anchor.y = 0.5; print.visible = false; L.addChild(print);
        this.addChild(L);
        var st = {
            def: def, L: L, photo: photo, blur: blur, info: info, flash: flash, print: print, tint: tint, obst: obst,
            fw: fw, fh: fh, fx: fx, fy: fy, t: 0, phase: Math.random() * 6.28, v: 1,
            film: Number(def.film || 4), filmMax: Number(def.film || 4), goal: Number(def.goal || 1), ok: 0,
            result: 0, resultOk: false, msg: '', puffs: [], done: done, zone: Number(def.zone || 0.16),
            speed: Number(def.speed || 1), flashT: 0, nextFlash: 120 + Math.floor(Math.random() * 120)
        };
        var puffN = def.smoke ? 4 : 0, headN = def.crowd ? 5 : 0;
        for (var i = 0; i < puffN; i++) {
            var r = Math.round(fh * (0.22 + Math.random() * 0.12));
            var p = new Sprite(focusPuffBitmap(r, def.smokeColor || '226,222,212')); p.anchor.x = p.anchor.y = 0.5;
            p._vx = (0.6 + Math.random() * 0.8) * (fw / 600) * (i % 2 ? 1 : -1); p.x = Math.random() * fw; p.y = fh * (0.3 + Math.random() * 0.5); p._r = r;
            obst.addChild(p); st.puffs.push(p);
        }
        for (var j = 0; j < headN; j++) {
            var hw = Math.round(fh * 0.34), hh = Math.round(fh * 0.5);
            var hd = new Sprite(focusHeadBitmap(hw, hh)); hd.anchor.x = 0.5; hd.anchor.y = 1;
            hd._vx = (0.7 + Math.random() * 0.9) * (fw / 600) * (j % 2 ? 1 : -1); hd.x = (j + 0.5) * fw / headN; hd.y = fh + 6; hd._r = hw * 0.45;
            hd._bob = Math.random() * 6;
            obst.addChild(hd); st.puffs.push(hd);
        }
        this._escFocus = st;
        photo.bitmap.addLoadListener(function() {
            var bw = photo.bitmap.width, bh = photo.bitmap.height;
            var sc = Math.max(fw / bw, fh / bh) * (def.move ? 1.1 : 1.02);
            photo.scale.x = photo.scale.y = sc;
            st.baseScale = sc;
        });
        this.escDrawFocusInfo();
    };

    Scene_Map.prototype.escDrawFocusInfo = function() {
        var st = this._escFocus; if (!st) return;
        var b = st.info.bitmap; b.clear();
        var W = SW(), def = st.def;
        b.textColor = '#ffe9b0'; b.outlineColor = 'rgba(0,0,0,0.8)'; b.outlineWidth = 4;
        escDrawFit(b, escSub(def.label || '초점을 맞춰 찍자'), 20, HUD_H + 6, W - 40, 40, 'center', 26, 15);
        // 필름
        var fw = 22, gap = 6, tot = st.filmMax * (fw + gap) - gap, x0 = (W - tot) / 2, y0 = HUD_H + 46;
        for (var i = 0; i < st.filmMax; i++) {
            var used = i >= st.film;
            roundRect(b, x0 + i * (fw + gap), y0, fw, 14, 3, used ? 'rgba(90,80,70,0.6)' : 'rgba(250,210,110,0.95)', 'rgba(0,0,0,0.6)', 1);
        }
        // 초점 막대
        var my = st.fy + st.fh + 18, mw = Math.min(520, st.fw * 0.8), mx = (W - mw) / 2;
        b.fillRect(mx, my, mw, 16, 'rgba(255,255,255,0.18)');
        var zw = mw * st.zone;
        b.fillRect(mx + mw / 2 - zw / 2, my, zw, 16, 'rgba(110,230,140,0.85)');
        var nx = mx + mw / 2 + st.v * (mw / 2 - 4);
        var sharp = Math.abs(st.v) < st.zone / 2;
        b.fillRect(nx - 3, my - 6, 6, 28, sharp ? '#b8ffc8' : '#ffffff');
        b.fontSize = 15; b.textColor = '#d9d2c0'; b.outlineWidth = 3;
        b.drawText('흐림', mx - 50, my - 4, 44, 24, 'right'); b.drawText('흐림', mx + mw + 6, my - 4, 44, 24, 'left');
        var msg = st.result > 0 ? st.msg : (st.goal > 1 ? '또렷해지는 순간 셔터!  (' + st.ok + ' / ' + st.goal + ')' : '사진이 가장 또렷해지는 순간 셔터!');
        var touch = Utils.isMobileDevice() || ('ontouchstart' in window);
        if (!st.result) msg += touch ? '  —  화면을 톡' : '  —  Enter · 클릭';
        b.textColor = st.result > 0 ? (st.resultOk ? '#b8ffc8' : '#ffb0a0') : '#ffffff';
        escDrawFit(b, msg, 20, my + 26, W - 40, 34, 'center', 21, 13);
        b.outlineWidth = 4;
    };

    Scene_Map.prototype.escUpdateFocus = function() {
        var st = this._escFocus; if (!st) return;
        var def = st.def;
        st.t++;
        // 렌즈가 앞뒤로 초점을 찾는 움직임
        var w = 0.045 * st.speed * (def.move ? (1 + 0.45 * Math.sin(st.t * 0.017)) : 1);
        if (!st.result) st.phase += w;
        st.v = Math.sin(st.phase);
        var a = Math.abs(st.v);
        if (st.blur) st.blur.blur = st.result > 0 && st.resultOk ? 0 : Math.max(0, (a - st.zone * 0.35)) * 26;
        var sc = st.baseScale || 1;
        if (def.move && !st.result) {
            st.photo.x = st.fw / 2 + Math.sin(st.t * 0.021) * st.fw * 0.035;
            st.photo.y = st.fh / 2 + Math.sin(st.t * 0.033) * st.fh * 0.02;
            st.photo.scale.x = st.photo.scale.y = sc * (1 + Math.sin(st.t * 0.011) * 0.015);
        }
        st.puffs.forEach(function(p) {
            if (st.result) return;
            p.x += p._vx;
            if (p._bob !== undefined) { p._bob += 0.12; p.y = st.fh + 6 - Math.abs(Math.sin(p._bob)) * 8; }
            if (p.x < -p._r * 1.2) p.x = st.fw + p._r; if (p.x > st.fw + p._r * 1.2) p.x = -p._r;
        });
        // 다른 기자들의 플래시
        if (def.flash && !st.result) {
            if (st.flashT > 0) { st.flashT--; st.tint.opacity = st.flashT * 26; }
            else { st.tint.opacity = 0; if (--st.nextFlash <= 0) { st.flashT = 10; st.nextFlash = 90 + Math.floor(Math.random() * 150); } }
        }
        st.flash.opacity = Math.max(0, st.flash.opacity - 18);
        if (st.result > 0) {
            st.result--;
            var k = 1 - st.result / 90;
            if (st.print.visible) {
                st.print.rotation = -0.06 + k * 0.03;
                st.print.scale.x = st.print.scale.y = st.printScale * (1.08 - Math.min(1, k * 3) * 0.08);
            }
            if (st.result === 0) {
                st.print.visible = false;
                if (st.resultOk && st.ok >= st.goal) return this.escEndFocus(true);
                if (!st.resultOk && st.film <= 0) return this.escEndFocus(false);
            }
        } else if (st.t > 24 && (Input.isTriggered('ok') || TouchInput.isTriggered())) {
            this.escShoot();
        }
        this.escDrawFocusInfo();
    };

    Scene_Map.prototype.escShoot = function() {
        var st = this._escFocus, def = st.def;
        if (!playSafeSe(def.se || (escData() && escData().shutterSe) || 'Haebang_Shutter', 90, 100)) SoundManager.playOk();
        st.flash.opacity = 230;
        var sharp = Math.abs(st.v) < st.zone / 2;
        var hidden = false, cx = st.fw / 2, cy = st.fh / 2;
        st.puffs.forEach(function(p) {
            var py = p._bob !== undefined ? p.y - p._r * 1.6 : p.y;
            if (Math.abs(p.x - cx) < p._r * 0.75 && Math.abs(py - cy) < p._r * 1.1) hidden = true;
        });
        var flashed = def.flash && st.flashT > 0;
        var ok = sharp && !hidden && !flashed;
        st.resultOk = ok;
        st.result = 90;
        // 인화된 사진
        var pw = Math.round(st.fw * 0.62), ph = Math.round(st.fh * 0.62);
        var pb = new Bitmap(pw + 24, ph + 44);
        pb.fillAll('#f6f1e4');
        var src = st.photo.bitmap;
        if (src && src.width > 1) {
            var sc = Math.max(pw / src.width, ph / src.height);
            var sw = pw / sc, sh = ph / sc;
            pb.blt(src, (src.width - sw) / 2, (src.height - sh) / 2, sw, sh, 12, 12, pw, ph);
            if (!ok) {   // 흐린 사진 흉내: 여러 번 겹쳐 찍기
                pb.paintOpacity = 70;
                for (var k = -3; k <= 3; k++) if (k) pb.blt(src, (src.width - sw) / 2 + k * 6, (src.height - sh) / 2, sw, sh, 12, 12, pw, ph);
                pb.paintOpacity = 255;
                if (hidden) pb.fillRect(12, 12, pw, ph, 'rgba(230,226,216,0.55)');
                if (flashed) pb.fillRect(12, 12, pw, ph, 'rgba(255,255,255,0.6)');
            }
        }
        st.print.bitmap = pb;
        st.printScale = 1;
        st.print.x = SW() / 2; st.print.y = st.fy + st.fh / 2;
        st.print.visible = true;
        if (ok) {
            st.ok++;
            st.msg = st.ok >= st.goal ? '찰칵! 또렷하게 찍혔다!' : '좋아! 한 장 더!';
            if (!playSafeSe(SE_SOLVE, 80, 110)) SoundManager.playRecovery();
        } else {
            st.film--;
            st.msg = (hidden ? '앞이 가려서 흐리게 찍혔다' : flashed ? '다른 사람의 플래시 때문에 하얗게 찍혔다' : '초점이 안 맞아 흐리게 찍혔다') +
                (st.film > 0 ? '  (필름 ' + st.film + '장 남음)' : '  (필름을 다 썼다)');
            SoundManager.playBuzzer();
        }
    };

    Scene_Map.prototype.escEndFocus = function(ok) {
        var st = this._escFocus; if (!st) return;
        this.removeChild(st.L);
        this._escFocus = null;
        if (st.done) st.done(ok);
    };

    var _v4_smUpdate = Scene_Map.prototype.update;
    Scene_Map.prototype.update = function() {
        _v4_smUpdate.apply(this, arguments);
        if (this._escFocus) this.escUpdateFocus();
    };
    var _v4_mapTouch = Scene_Map.prototype.processMapTouch;
    Scene_Map.prototype.processMapTouch = function() {
        if (this._escFocus) return;
        _v4_mapTouch.call(this);
    };
    var _v4_closeAll = Scene_Map.prototype.escCloseAll;
    Scene_Map.prototype.escCloseAll = function() {
        _v4_closeAll.apply(this, arguments);
        if (this._escFocus) { this.removeChild(this._escFocus.L); this._escFocus = null; EscapeManager._focus = null; }
    };

    // ---- 위에 겹치는 그림 (나무 윗부분·지붕 처마 등이 인물보다 위) -------------------------
    //  방 "overlay": "!그림_top"  또는 [{ "if": 조건, "name": "..." }]   (원경과 같은 크기의 투명 PNG)
    EscapeManager.overlayName = function() {
        var room = this.currentRoom();
        if (!room || !room.overlay) return '';
        if (typeof room.overlay === 'string') return room.overlay;
        var list = toArray(room.overlay);
        for (var i = 0; i < list.length; i++) if (this.checkCond(list[i]['if'])) return String(list[i].name || '');
        return '';
    };
    var _v4_createCharacters = Spriteset_Map.prototype.createCharacters;
    Spriteset_Map.prototype.createCharacters = function() {
        _v4_createCharacters.apply(this, arguments);
        this._escTop = new Sprite();
        this._escTop.z = 6;
        this._escTopName = null;
        this._tilemap.addChild(this._escTop);
    };
    var _v4_ssUpdate = Spriteset_Map.prototype.update;
    Spriteset_Map.prototype.update = function() {
        _v4_ssUpdate.apply(this, arguments);
        var top = this._escTop; if (!top) return;
        var M = EscapeManager;
        if (!M.isActive || !M.isActive() || !M.isRoomMap($gameMap.mapId())) { top.visible = false; return; }
        if (Graphics.frameCount % 15 === 0 || this._escTopName === null) {
            var n = M.overlayName();
            if (n !== this._escTopName) {
                this._escTopName = n;
                top.bitmap = n && hasAsset('par', n) ? ImageManager.loadParallax(n) : null;
            }
        }
        top.visible = !!top.bitmap;
        top.x = -Math.round($gameMap.displayX() * $gameMap.tileWidth());
        top.y = -Math.round($gameMap.displayY() * $gameMap.tileHeight());
    };
    // 겹침 그림도 미리 있는지 확인
    var _v4_collect = collectAssets;
    collectAssets = function(d) {
        var keys = _v4_collect(d);
        var add = function(k) { if (keys.indexOf(k) < 0) keys.push(k); };
        toArray(d.rooms).forEach(function(r) {
            if (typeof r.overlay === 'string') add('par/' + r.overlay);
            else toArray(r.overlay).forEach(function(o) { if (o && o.name) add('par/' + o.name); });
        });
        toArray(d.portraitFiles).forEach(function(n) { add('pic/' + n); });
        // 초점 촬영 그림
        var deep = function(o) {
            if (!o || typeof o !== 'object') return;
            if (Array.isArray(o)) { o.forEach(deep); return; }
            if (o.focus && o.focus.picture) add('pic/' + o.focus.picture);
            Object.keys(o).forEach(function(k) { deep(o[k]); });
        };
        deep(d.rooms); deep(d.intro);
        return keys;
    };
    var _v4_assetUrl = assetUrl;
    assetUrl = function(key) {
        if (key.indexOf('par/') === 0) {
            var url = 'img/parallaxes/' + encodeURIComponent(key.substring(4)) + '.png';
            if (Decrypter.hasEncryptedImages) url = Decrypter.extToEncryptExt(url);
            return url;
        }
        return _v4_assetUrl(key);
    };

    // 감시·움직이는 것: 시네마틱 중에는 쉬기
    var _v4_updWatch = EscapeManager.updateWatchers;
    EscapeManager.updateWatchers = function() {
        if (this._cine || this._focus) return;
        return _v4_updWatch.apply(this, arguments);
    };

    // 주인공 그림: heroImage 단계로 바꾼 그림을 방을 옮겨도 유지
    var _v4_advBuild = Scene_Map.prototype.escAdvBuild;
    Scene_Map.prototype.escAdvBuild = function() {
        _v4_advBuild.apply(this, arguments);
        var lead = $gameParty.leader(), M = EscapeManager, room = M.currentRoom();
        if (lead && M._baseImage && !(room && room.older)) {
            var want = M._baseImage + ((room && room.heroSuffix) || '');
            if (lead.characterName() !== want) { lead.setCharacterImage(want, 0); $gamePlayer.refresh(); }
        }
    };

    //=========================================================================
    // v4.1 퀘스트 표시 · 걷는 사람들(행진·서성임) · 쫓아오는 진압 · 흩어지기  (「종로 사진관 2」에서 추가)
    //=========================================================================
    Imported.EscapeRoom = '4.1.0';

    // 목표 대상 이름: "id" 또는 "방id:id"
    function escTargetMatch(t, roomId, hid) {
        t = String(t);
        var k = t.indexOf(':');
        if (k >= 0) return t.slice(0, k) === roomId && t.slice(k + 1) === hid;
        return t === hid;
    }

    // ---- 단계: goal + targets / walkers / walkersStop / scatter / addTarget --------
    var _v41_processStep = EscapeManager.processStep;
    EscapeManager.processStep = function(s) {
        if (s && typeof s === 'object') {
            if (s.goal !== undefined) this._goalTargets = toArray(s.targets).map(String);
            if (s.addTarget !== undefined) {
                this._goalTargets = (this._goalTargets || []).concat(toArray(s.addTarget).map(String));
            }
            if (s.walkersStop !== undefined) this.stopWalkers(s.walkersStop);
            if (s.walkers) this.addWalkers(s.walkers);
            if (s.scatter) this.scatterEvents(s.scatter);
        }
        return _v41_processStep.apply(this, arguments);
    };

    // 대상에게 말을 걸면 그 대상의 표시는 사라짐 (같은 단계에서 새 목표가 오면 새 표시)
    var _v41_trigger = EscapeManager.triggerHotspot;
    EscapeManager.triggerHotspot = function(h) {
        if (h && this.canInteract() && this.checkCond(h.when) && this._goalTargets && !h.keepTarget) {
            var room = this.currentRoom(), rid = room ? room.id : '';
            this._goalTargets = this._goalTargets.filter(function(t) { return !escTargetMatch(t, rid, h.id); });
        }
        return _v41_trigger.apply(this, arguments);
    };

    EscapeManager.isGoalTarget = function(h) {
        var room = this.currentRoom(), rid = room ? room.id : '';
        return toArray(this._goalTargets).some(function(t) { return escTargetMatch(t, rid, h.id); });
    };

    // ---- 걷는 사람들 ------------------------------------------------------------
    //  방 "walkers": [{ "event": "이름", "route": [[x,y],...], "rel": true(처음 자리 기준), "loop": true|"pingpong"|false,
    //                   "speed": 3, "pause": 0, "wander": 2, "if": 조건, "always": true(대화 중에도), "through": true, "anime": true }]
    //  같은 이름의 이벤트가 여럿이면 모두 같은 규칙으로 (rel 이면 각자 자리 기준)
    EscapeManager.setupWalkers = function() {
        this._walkers = [];
        var room = this.currentRoom();
        if (room && room.walkers) this.addWalkers(room.walkers);
    };

    EscapeManager.addWalkers = function(defs) {
        var self = this;
        this._walkers = this._walkers || [];
        toArray(defs).forEach(function(def) {
            var names = toArray(def.events || def.event).map(String);
            $gameMap.events().forEach(function(ev) {
                if (names.indexOf(String(ev.event().name).trim()) < 0) return;
                self._walkers = self._walkers.filter(function(w) { return w.ev !== ev; });
                var home = ev._escWalkHome || [ev.x, ev.y];
                ev._escWalkHome = home;
                var w = { def: def, ev: ev, idx: 0, dirStep: 1, wait: Number(def.delay || 0), stuck: 0, home: [ev.x, ev.y] };
                if (def.rel) w.home = [ev.x, ev.y];
                self._walkers.push(w);
            });
        });
    };

    EscapeManager.stopWalkers = function(which) {
        if (!this._walkers) return;
        if (which === true) { this._walkers = []; return; }
        var names = toArray(which).map(String);
        this._walkers = this._walkers.filter(function(w) { return names.indexOf(String(w.ev.event().name).trim()) < 0; });
    };

    function escWalkFree(x, y) {
        return $gameMap.isValid(x, y) && $gameMap.regionId(x, y) !== WALL_REGION;
    }

    EscapeManager.updateWalkers = function() {
        if (!this._walkers || this._walkers.length === 0) return;
        if (this._phase !== 'play' && this._phase !== 'intro') return;
        if (this._waitTransfer || $gamePlayer.isTransferring()) return;
        var busy = this.isBusy(), self = this;
        this._walkers.forEach(function(w) {
            var def = w.def, ev = w.ev;
            if (ev._erased || ev._escHidden || w.done) return;
            if (def['if'] && !self.checkCond(def['if'])) return;
            if (w.fade) {                 // loop "restart": 끝에서 사라졌다가 처음 자리에서 다시 나타남
                w.fade--;
                if (w.fade === 20) { ev.locate(w.home[0], w.home[1]); ev.setDirection(w.dir0 || ev.direction()); }
                ev.setOpacity(w.fade > 20 ? (w.fade - 20) * 12 : (20 - w.fade) * 12 + 15);
                if (w.fade === 0) ev.setOpacity(255);
                return;
            }
            if (busy && !def.always) return;
            if (ev.isMoving()) return;
            ev.setThrough(def.through !== false);
            ev.setMoveSpeed(Number(def.speed || 3));
            if (def.anime) ev.setStepAnime(true);
            if (w.wait > 0) { w.wait--; return; }
            if (def.wander) {
                var r = Number(def.wander), dirs = [2, 4, 6, 8];
                var d = dirs[Math.floor(Math.random() * 4)];
                var nx = $gameMap.roundXWithDirection(ev.x, d), ny = $gameMap.roundYWithDirection(ev.y, d);
                if (Math.abs(nx - w.home[0]) <= r && Math.abs(ny - w.home[1]) <= r && escWalkFree(nx, ny) &&
                    !(nx === $gamePlayer.x && ny === $gamePlayer.y)) ev.moveStraight(d);
                else ev.setDirection(d);
                w.wait = 40 + Math.floor(Math.random() * Number(def.pause || 90));
                return;
            }
            var route = toArray(def.route);
            if (route.length === 0) return;
            var p = route[w.idx];
            var tx = Number(p[0]) + (def.rel ? w.home[0] : 0), ty = Number(p[1]) + (def.rel ? w.home[1] : 0);
            if (ev.x === tx && ev.y === ty) {
                var n = route.length;
                if (def.loop === 'pingpong') {
                    if (w.idx + w.dirStep < 0 || w.idx + w.dirStep >= n) w.dirStep = -w.dirStep;
                    w.idx += w.dirStep;
                } else if (def.loop === 'restart') {
                    if (w.idx + 1 >= n) { w.idx = 0; w.fade = 40; w.dir0 = ev.direction(); return; }
                    w.idx++;
                } else if (def.loop === false) {
                    if (w.idx + 1 >= n) {
                        w.done = true;
                        if (def.face) ev.setDirection({ down: 2, left: 4, right: 6, up: 8 }[def.face] || 2);
                        return;
                    }
                    w.idx++;
                } else w.idx = (w.idx + 1) % n;
                w.wait = Number(def.pause || 0);
                return;
            }
            var dx = tx - ev.x, dy = ty - ev.y, dd;
            if (Math.abs(dx) >= Math.abs(dy)) dd = dx > 0 ? 6 : 4; else dd = dy > 0 ? 2 : 8;
            if (def.through === false) dd = ev.findDirectionTo(tx, ty) || dd;
            ev.moveStraight(dd);
            if (!ev.isMovementSucceeded()) {
                // 옆으로 비켜 가기
                var alt = (dd === 2 || dd === 8) ? (dx > 0 ? 6 : dx < 0 ? 4 : 0) : (dy > 0 ? 2 : dy < 0 ? 8 : 0);
                if (alt) ev.moveStraight(alt);
                if (!ev.isMovementSucceeded()) {
                    w.stuck++;
                    w.wait = 15;
                    if (w.stuck > 8) { ev.locate(tx, ty); w.stuck = 0; }
                } else w.stuck = 0;
            } else w.stuck = 0;
        });
    };

    // 흩어지기: { "scatter": { "events": [...], "from": "player" 또는 [x,y], "dist": 4, "speed": 5 } }
    EscapeManager.scatterEvents = function(def) {
        var names = toArray(def.events).map(String), self = this;
        var from = def.from && def.from !== 'player' ? toArray(def.from) : [$gamePlayer.x, $gamePlayer.y];
        var dist = Number(def.dist || 4);
        $gameMap.events().forEach(function(ev) {
            if (names.indexOf(String(ev.event().name).trim()) < 0) return;
            var vx = ev.x - Number(from[0]), vy = ev.y - Number(from[1]);
            if (vx === 0 && vy === 0) vx = Math.random() < 0.5 ? -1 : 1;
            var len = Math.sqrt(vx * vx + vy * vy);
            var tx = Math.round(ev.x + vx / len * dist), ty = Math.round(ev.y + vy / len * dist);
            for (var k = 0; k < 6 && !escWalkFree(tx, ty); k++) { tx = Math.round((tx + ev.x) / 2); ty = Math.round((ty + ev.y) / 2); }
            self.addWalkers([{ event: String(ev.event().name).trim(), route: [[tx, ty]], loop: false, speed: Number(def.speed || 5), always: true, through: true, face: def.face }]);
        });
    };

    // 방에 들어올 때 걷는 사람들 준비
    var _v41_setupWatchers = EscapeManager.setupWatchers;
    EscapeManager.setupWatchers = function() {
        _v41_setupWatchers.apply(this, arguments);
        if (this._watch && this._watchGrace) { this._watch.cool = this._watchGrace; this._watchGrace = 0; }
        this.setupWalkers();
    };

    // ---- 쫓아오는 감시자: watchers 에 "chase": 4 → 4칸 안에 들어오면 쫓아옴, 닿으면 들킴 ----
    var _v41_updateWatchers = EscapeManager.updateWatchers;
    EscapeManager.updateWatchers = function() {
        if (this._watch && this._phase === 'play' && this.watchActive() && !(this.isBusy() && !this._mission && !this._chase) &&
            !$gamePlayer.isTransferring() && !this._waitTransfer) {
            var px = $gamePlayer.x, py = $gamePlayer.y, self = this;
            for (var i = 0; i < this._watch.list.length; i++) {
                var w = this._watch.list[i], r = Number(w.def.chase || 0);
                if (!r || w.ev._erased || w.ev._escHidden || this._watch.cool > 0) continue;
                var dist = Math.abs(w.ev.x - px) + Math.abs(w.ev.y - py);
                if (dist <= 1 && this._watch.cool <= 0) { w.ev.turnTowardPlayer(); this.onCaught(w); return; }
                if (dist <= r && !w.ev.isMoving()) {
                    w.ev.setMoveSpeed(Number(w.def.chaseSpeed || 4));
                    w.ev.moveTowardPlayer();
                    w.chasing = true;
                } else if (w.chasing && dist > r + 2) {
                    w.chasing = false; w.ev.setMoveSpeed(Number(w.def.speed || 3));
                }
            }
        }
        _v41_updateWatchers.apply(this, arguments);
        this.updateWalkers();
    };

    // ---- 퀘스트 표시: 목표 대상 위에 "!" 표시 (대상이 움직여도 따라감) -------------------
    function escQuestBitmap(text) {
        var BW = 300, bmp = new Bitmap(BW, 92);
        var ctx = ctxOf(bmp);
        // 동그라미 + 느낌표
        ctx.fillStyle = 'rgba(255,196,40,1)'; ctx.strokeStyle = 'rgba(80,44,0,0.95)'; ctx.lineWidth = 3;
        ctx.beginPath(); ctx.arc(BW / 2, 20, 17, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
        setDirty(bmp);
        bmp.fontSize = 26; bmp.textColor = '#3a1e00'; bmp.outlineWidth = 0;
        bmp.drawText('!', 0, 2, BW, 36, 'center');
        if (text) {
            var size = escFitSize(bmp, text, BW - 30, 16, 11);
            bmp.fontSize = size;
            var w = Math.min(BW - 6, bmp.measureTextWidth(text) + 22);
            roundRect(bmp, (BW - w) / 2, 42, w, 24, 11, 'rgba(40,24,6,0.88)', 'rgba(255,196,40,0.95)', 2);
            bmp.textColor = '#ffe9a8';
            bmp.drawText(text, 0, 42, BW, 24, 'center');
        }
        ctx = ctxOf(bmp);
        ctx.fillStyle = 'rgba(255,196,40,1)'; ctx.strokeStyle = 'rgba(80,44,0,0.95)'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(BW / 2 - 9, 70); ctx.lineTo(BW / 2 + 9, 70); ctx.lineTo(BW / 2, 84); ctx.closePath(); ctx.fill(); ctx.stroke();
        setDirty(bmp);
        return bmp;
    }

    var _v41_updateMarks = Scene_Map.prototype.escUpdateMarks;
    Scene_Map.prototype.escUpdateMarks = function() {
        _v41_updateMarks.apply(this, arguments);
        var M = EscapeManager, room = M.currentRoom();
        if (!this._escMarks) return;
        if (!this._escQuest) { this._escQuest = new Sprite(); this._escMarks.parent.addChild(this._escQuest); this._escQuestList = []; }
        var list = [];
        var mis = M._mission ? toArray(M._mission.left).map(String) : null;
        if (room && M._phase === 'play' && !M._cine && (mis || !M.isBusy())) {
            toArray(room.hotspots).forEach(function(h) {
                var want = mis ? mis.indexOf(h.id) >= 0 : (M.isGoalTarget(h) || (h.quest !== undefined && M.checkCond(h.quest)));
                if (want && (h.visible === undefined || M.checkCond(h.visible))) list.push(h);
            });
        }
        var key = list.map(function(h) { return h.id; }).join(',');
        if (key !== this._escQuestKey) {
            this._escQuestKey = key;
            this._escQuest.removeChildren();
            var self = this;
            this._escQuestList = list.map(function(h) {
                var text = escSub(typeof h.mark === 'string' ? h.mark : (h.questLabel || h.label || ''));
                var sp = new Sprite(escQuestBitmap(text));
                sp.anchor.x = 0.5; sp.anchor.y = 1;
                self._escQuest.addChild(sp);
                return { h: h, sp: sp };
            });
        }
        // 퀘스트 표시가 있는 지점은 노란 이름표(mark)를 겹쳐 그리지 않음
        if (this._escMarkList) {
            var qids = list.map(function(h) { return h.id; });
            this._escMarkList.forEach(function(m) { if (qids.indexOf(m.h.id) >= 0) m.sp.visible = false; });
        }
        var t = Graphics.frameCount, self2 = this;
        this._escQuestList.forEach(function(m, i) {
            var evs = self2.escHotspotEvents(m.h.id).filter(function(e) { return !e._erased && !e._escHidden; });
            if (evs.length === 0) { m.sp.visible = false; return; }
            var sx = 0, sy = 0;
            evs.forEach(function(e) { sx += e.screenX(); sy += e.screenY(); });
            sx /= evs.length; sy /= evs.length;
            var hasPic = evs.some(function(e) { return !!e.characterName(); });
            m.sp.visible = true;
            m.sp.x = Math.max(70, Math.min(SW() - 70, sx));
            m.sp.y = Math.max(HUD_H + 96, sy - (hasPic ? 46 : 18) + Math.sin(t / 9 + i) * 5);
        });
    };

    //=========================================================================
    // 휴대폰·태블릿을 세로로 들었을 때 "가로로 돌려 주세요" 안내
    //=========================================================================
    (function() {
        var box = null, dismissed = false;
        function isTouchDevice() {
            return Utils.isMobileDevice() || ('ontouchstart' in window) || (navigator.maxTouchPoints > 1);
        }
        function block(e) { e.stopPropagation(); }
        function check() {
            var show = !dismissed && isTouchDevice() && window.innerHeight > window.innerWidth * 1.05;
            if (!box) {
                if (!show) return;
                box = document.createElement('div');
                box.style.cssText = 'position:fixed;left:0;top:0;right:0;bottom:0;z-index:200;display:flex;' +
                    'flex-direction:column;align-items:center;justify-content:center;background:rgba(12,10,8,0.92);' +
                    'color:#ffe9b0;font-family:GameFont,sans-serif;text-align:center;';
                box.innerHTML = '<div style="font-size:20vmin;line-height:1">&#x1F4F1;&#x21BB;</div>' +
                    '<div style="font-size:7vmin;margin-top:4vmin">화면을 <b>가로</b>로 돌려 주세요</div>' +
                    '<div style="font-size:4.2vmin;margin-top:2vmin;color:#cdbf9f;line-height:1.5">가로로 들면 게임 화면이 훨씬 크게 보여요.<br>' +
                    '(화면 자동 회전이 꺼져 있다면 켜 주세요)</div>' +
                    '<div id="escRotateSkip" style="margin-top:7vmin;padding:2.5vmin 6vmin;border:1px solid #8a7a5a;' +
                    'border-radius:2vmin;font-size:4.5vmin;color:#ffffff">그냥 세로로 할래요</div>';
                ['touchstart', 'touchmove', 'touchend', 'mousedown', 'mouseup', 'pointerdown', 'wheel'].forEach(function(n) {
                    box.addEventListener(n, block);
                });
                var skip = box.querySelector('#escRotateSkip');
                var onSkip = function(e) { e.preventDefault(); e.stopPropagation(); dismissed = true; check(); };
                skip.addEventListener('touchend', onSkip);
                skip.addEventListener('click', onSkip);
                document.body.appendChild(box);
            }
            box.style.setProperty('z-index', '1000', 'important');
            box.style.display = show ? 'flex' : 'none';
        }
        window.addEventListener('resize', check);
        window.addEventListener('orientationchange', function() { setTimeout(check, 300); });
        window.addEventListener('load', check);
        setTimeout(check, 0);
    })();

    //=========================================================================
    // v4.3  (금지된 주파수)
    //  1) 퀘스트 표시 '!' 를 오브젝트 그림 바로 위에 정확히 (화면 가장자리에서 안쪽으로 밀리지 않음)
    //     조사 지점에 "markAt": [칸x, 칸y] 를 주면 그 칸 위에, "markUp": 픽셀 을 주면 그만큼 더 위에
    //  2) 멈춤 방지 안전장치 (풀리지 않는 기다림 · 끝나지 않는 장소 이동 · 어두운 화면 · 끝나지 않은 시네마틱 ·
    //     사방이 막힌 주인공 · 실행 중 오류) → 몇 초 안에 스스로 풀고 계속 진행
    //  3) 새 미니게임 "game": knob(주파수 노브) strike(선전 문장 지우기) sort(나눠 담기) order(순서 놓기)
    //     lights(등화관제) match(선 잇기) wheel(암호 바퀴) pick(돈 맞춰 내기)
    //     모든 미니게임: 틀려도 벌점 없음, 두 번 틀리면 힌트, 세 번 틀리면 정답을 보여 주고 넘어감, Esc 로 나중에 하기
    //=========================================================================
    var ESC_VERSION = '4.3';

    // ---- 1) 퀘스트 표시 위치 -------------------------------------------------------------
    function escSpriteOf(ev) {
        var sc = SceneManager._scene, ss = sc && sc._spriteset;
        if (!ss || !ss._characterSprites) return null;
        for (var i = 0; i < ss._characterSprites.length; i++) if (ss._characterSprites[i]._character === ev) return ss._characterSprites[i];
        return null;
    }
    // 표시 끝(화살표 끝)이 닿을 화면 좌표
    Scene_Map.prototype.escMarkTip = function(h) {
        var tw = $gameMap.tileWidth(), th = $gameMap.tileHeight();
        if (h.markAt) {
            var a = toArray(h.markAt);
            return { x: ($gameMap.adjustX(Number(a[0])) + 0.5) * tw, y: $gameMap.adjustY(Number(a[1])) * th + 6 - Number(h.markUp || 0), ok: true };
        }
        var evs = this.escHotspotEvents(h.id).filter(function(e) { return !e._erased && !e._escHidden; });
        if (evs.length === 0) return null;
        // 같은 이름이 여럿이면 가장 가까운 것 하나 (가운데 빈 곳을 가리키지 않게)
        var px = $gamePlayer.x, py = $gamePlayer.y;
        evs.sort(function(a, b) { return (Math.abs(a.x - px) + Math.abs(a.y - py)) - (Math.abs(b.x - px) + Math.abs(b.y - py)); });
        var ev = evs[0], sx = ev.screenX(), sy = ev.screenY(), top;
        var sp = escSpriteOf(ev);
        if (ev.characterName() && sp && sp.bitmap && sp.bitmap.isReady() && sp.patternHeight) top = sy - sp.patternHeight() * (sp.scale ? sp.scale.y : 1);
        else if (ev.characterName()) top = sy - 50;
        else top = sy - th + 10 + (ev.shiftY ? ev.shiftY() : 0);
        return { x: sx, y: top - 2 - Number(h.markUp || 0), ok: true };
    };
    var _v43_updateMarks = Scene_Map.prototype.escUpdateMarks;
    Scene_Map.prototype.escUpdateMarks = function() {
        _v43_updateMarks.apply(this, arguments);
        var self = this, t = Graphics.frameCount;
        (this._escQuestList || []).forEach(function(m, i) {
            var tip = self.escMarkTip(m.h);
            if (!tip) { m.sp.visible = false; return; }
            m.sp.visible = true;
            var x = tip.x, y = tip.y + Math.sin(t / 9 + i) * 3;
            // 화면 밖일 때만 가장자리에 붙임 (화면 안이면 정확한 자리)
            if (x < 16) x = 16; if (x > SW() - 16) x = SW() - 16;
            if (y > SH() - 8) y = SH() - 8; if (y < 30) y = 30;
            m.sp.x = x; m.sp.y = y + 8;          // 그림 아래쪽 8px 이 화살표 끝
        });
    };

    // ---- 3) 미니게임 창 ----------------------------------------------------------------
    function Window_EscGame() { this.initialize.apply(this, arguments); }
    Window_EscGame.prototype = Object.create(Window_Base.prototype);
    Window_EscGame.prototype.constructor = Window_EscGame;
    Window_EscGame.prototype.initialize = function() {
        var w = Math.min(780, SW() - 24), h = Math.min(SH() - HUD_H - 16, 560);
        Window_Base.prototype.initialize.call(this, (SW() - w) / 2, HUD_H + 8, w, h);
        this.openness = 0; this.active = false; this._handlers = {}; this._def = null;
    };
    Window_EscGame.prototype.setHandler = function(n, f) { this._handlers[n] = f; };
    Window_EscGame.prototype.standardFontSize = function() { return 20; };
    Window_EscGame.prototype.setup = function(def) {
        var w = Math.min(780, SW() - 24), h = Math.min(SH() - HUD_H - 16, Number(def.height || 560));
        this.move((SW() - w) / 2, HUD_H + 8 + Math.max(0, (SH() - HUD_H - 16 - h) / 2), w, h);
        this.createContents();
        this._def = def; this._type = String(def.type);
        this._fails = 0; this._msg = ''; this._msgCol = '#ffffff'; this._msgT = 0; this._end = 0; this._endOk = false;
        this._cur = 0; this._sel = -1; this._t = 0; this._openFrame = Graphics.frameCount; this._shown = false;
        var n, i;
        switch (this._type) {
        case 'knob': this._pos = Number(def.start !== undefined ? def.start : 8); this._hold = 0; break;
        case 'strike': this._marks = toArray(def.lines).map(function() { return false; }); break;
        case 'sort': this._bins = toArray(def.items).map(function() { return -1; }); break;
        case 'order':
            n = toArray(def.items).length; this._ord = [];
            for (i = 0; i < n; i++) this._ord.push(i);
            if (def.shuffle !== false) this._ord = escShuffleNot(this._ord, toArray(def.answer).map(function(v) { return Number(v) - 1; }));
            break;
        case 'lights':
            this._cols = Number(def.cols || 6); this._rows = Number(def.rows || 3);
            this._lit = []; for (i = 0; i < this._cols * this._rows; i++) this._lit.push(false);
            this._off = 0; this._time = Number(def.time || 40) * 60; this._spawn = 0; this._cx = 0; this._cy = 0;
            for (i = 0; i < Number(def.startLit || 4); i++) this.lightOne();
            break;
        case 'match': this._links = toArray(def.left).map(function() { return -1; }); this._side = 0; this._rc = 0; break;
        case 'wheel': this._shift = 0; break;
        case 'pick': this._picked = toArray(def.items).map(function() { return 0; }); break;
        }
        this.open(); this.activate();
        this.refresh();
    };
    function escShuffleNot(a, avoid) {
        var b = a.slice();
        for (var k = 0; k < 20; k++) {
            for (var i = b.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = b[i]; b[i] = b[j]; b[j] = t; }
            if (b.join(',') !== avoid.join(',')) return b;
        }
        return b.reverse();
    }
    Window_EscGame.prototype.lightOne = function() {
        var dark = []; for (var i = 0; i < this._lit.length; i++) if (!this._lit[i]) dark.push(i);
        if (dark.length) this._lit[dark[Math.floor(Math.random() * dark.length)]] = true;
    };
    Window_EscGame.prototype.say = function(text, col) { this._msg = text; this._msgCol = col || '#ffffff'; this._msgT = 150; };
    Window_EscGame.prototype.local = function() {
        return { x: TouchInput.x - this.x - this.standardPadding(), y: TouchInput.y - this.y - this.standardPadding() };
    };
    Window_EscGame.prototype.inside = function(r, p) { return p.x >= r.x && p.x < r.x + r.w && p.y >= r.y && p.y < r.y + r.h; };
    Window_EscGame.prototype.ready = function() { return Graphics.frameCount - this._openFrame > 10; };
    Window_EscGame.prototype.isSolved = function() {
        var d = this._def, ans = toArray(d.answer), i;
        switch (this._type) {
        case 'strike':
            var want = ans.map(function(v) { return Number(v) - 1; });
            for (i = 0; i < this._marks.length; i++) if (this._marks[i] !== (want.indexOf(i) >= 0)) return false;
            return true;
        case 'sort':
            for (i = 0; i < this._bins.length; i++) if (this._bins[i] !== Number(ans[i]) - 1) return false;
            return true;
        case 'order':
            for (i = 0; i < this._ord.length; i++) if (this._ord[i] !== Number(ans[i]) - 1) return false;
            return true;
        case 'match':
            for (i = 0; i < this._links.length; i++) if (this._links[i] !== Number(ans[i]) - 1) return false;
            return true;
        case 'wheel': return ((this._shift % 26) + 26) % 26 === ((Number(d.shift) % 26) + 26) % 26;
        case 'pick':
            var sum = 0, items = toArray(d.items);
            for (i = 0; i < items.length; i++) sum += this._picked[i] * Number(items[i].value);
            return sum === Number(d.target);
        }
        return false;
    };
    Window_EscGame.prototype.showAnswer = function() {
        var d = this._def, ans = toArray(d.answer), i;
        switch (this._type) {
        case 'strike': this._marks = this._marks.map(function(v, k) { return ans.map(Number).indexOf(k + 1) >= 0; }); break;
        case 'sort': this._bins = this._bins.map(function(v, k) { return Number(ans[k]) - 1; }); break;
        case 'order': this._ord = ans.map(function(v) { return Number(v) - 1; }); break;
        case 'match': this._links = this._links.map(function(v, k) { return Number(ans[k]) - 1; }); break;
        case 'wheel': this._shift = Number(d.shift); break;
        case 'knob': var st = escAnswerStation(d); if (st) this._pos = Number(st.at); break;
        case 'pick': if (d.solution) this._picked = toArray(d.solution).map(Number); break;
        }
    };
    function escAnswerStation(d) {
        var list = toArray(d.stations);
        for (var i = 0; i < list.length; i++) if (list[i].answer) return list[i];
        return list[0] || null;
    }
    Window_EscGame.prototype.finish = function(ok, auto) {
        this._end = auto ? 150 : 70; this._endOk = ok;
        if (ok) { this.say(auto ? (this._def.autoMsg || '정답을 보여 줄게요. 다음으로 넘어가요!') : (this._def.okMsg || '정답!'), '#9dffb0'); if (!playSafeSe(SE_SOLVE, 80, 100)) SoundManager.playRecovery(); }
        else this.say(this._def.failMsg || '시간이 다 되었어요. 다시 해 봐요!', '#ff9a8a');
        this.refresh();
    };
    Window_EscGame.prototype.submit = function() {
        if (this._end) return;
        if (this.isSolved()) { this.finish(true); return; }
        this._fails++;
        SoundManager.playBuzzer();
        var d = this._def;
        if (this._fails >= Number(d.autoAfter || 3)) { this.showAnswer(); this.finish(true, true); return; }
        if (this._fails >= Number(d.hintAfter || 2) && d.hint) this.say('힌트: ' + escSub(d.hint), '#ffe9a8');
        else this.say(escSub(d.wrongMsg || '아직 아니에요. 다시 살펴봐요.'), '#ff9a8a');
    };
    Window_EscGame.prototype.update = function() {
        Window_Base.prototype.update.call(this);
        if (!this.active || !this.isOpen() || !this._def) return;
        this._t++;
        if (this._msgT > 0) this._msgT--;
        if (this._end > 0) {
            if (--this._end === 0 || (this._end < 50 && this.ready() && (Input.isTriggered('ok') || TouchInput.isTriggered()))) {
                this._end = 0; this.active = false;
                if (this._handlers.done) this._handlers.done(this._endOk);
                return;
            }
            if (this._t % 4 === 0) this.refresh();
            return;
        }
        if (!this.ready()) return;
        if (Input.isTriggered('cancel') || (TouchInput.isCancelled && TouchInput.isCancelled())) {
            this.active = false; SoundManager.playCancel();
            if (this._handlers.cancel) this._handlers.cancel();
            return;
        }
        var fn = this['update_' + this._type];
        if (fn) fn.call(this);
        if (this._t % 3 === 0) this.refresh();
    };
    // 공통: 아래쪽 단추 줄 (확인 · 나중에)
    Window_EscGame.prototype.btnRects = function() {
        var w = this.contentsWidth(), h = this.contentsHeight();
        return { ok: { x: w / 2 - 170, y: h - 44, w: 160, h: 38 }, later: { x: w / 2 + 10, y: h - 44, w: 160, h: 38 } };
    };
    Window_EscGame.prototype.touchButtons = function() {
        if (!TouchInput.isTriggered()) return false;
        var p = this.local(), b = this.btnRects();
        if (this.inside(b.ok, p)) { SoundManager.playOk(); this.submit(); return true; }
        if (this.inside(b.later, p)) { this.active = false; SoundManager.playCancel(); if (this._handlers.cancel) this._handlers.cancel(); return true; }
        return false;
    };
    Window_EscGame.prototype.drawButtons = function(okLabel, focused) {
        var c = this.contents, b = this.btnRects();
        roundRect(c, b.ok.x, b.ok.y, b.ok.w, b.ok.h, 10, focused ? 'rgba(255,200,70,0.95)' : 'rgba(255,200,70,0.7)', focused ? '#ffffff' : 'rgba(0,0,0,0)', 3);
        roundRect(c, b.later.x, b.later.y, b.later.w, b.later.h, 10, 'rgba(255,255,255,0.15)', 'rgba(255,255,255,0.4)', 1);
        c.fontSize = 18; c.textColor = '#2a1a06'; c.drawText(okLabel || '확인', b.ok.x, b.ok.y + 2, b.ok.w, 34, 'center');
        c.textColor = '#ffffff'; c.drawText('나중에 (Esc)', b.later.x, b.later.y + 2, b.later.w, 34, 'center');
        this.resetTextColor();
    };
    Window_EscGame.prototype.drawHeader = function() {
        var c = this.contents, w = this.contentsWidth(), d = this._def;
        c.fontSize = 22; this.changeTextColor('#ffe9b0'); c.drawText(escSub(d.title || ''), 0, 0, w, 30, 'center');
        c.fontSize = 16; this.changeTextColor('#d8ccb0');
        var help = escSub(d.help || ''), lines = escWrap(c, help, w - 10);
        for (var i = 0; i < lines.length && i < 2; i++) c.drawText(lines[i], 0, 30 + i * 22, w, 22, 'center');
        this.resetTextColor();
        return 30 + Math.min(2, lines.length) * 22 + 8;
    };
    Window_EscGame.prototype.drawMsg = function(y) {
        var c = this.contents, w = this.contentsWidth();
        if (!this._msg || (this._msgT <= 0 && !this._end)) return;
        c.fontSize = 18; c.textColor = this._msgCol;
        var lines = escWrap(c, this._msg, w - 20);
        for (var i = 0; i < lines.length && i < 2; i++) c.drawText(lines[i], 0, y + i * 24, w, 24, 'center');
        this.resetTextColor();
    };
    function escWrap(bmp, text, maxW) {
        var out = [], parts = String(text).split('\n');
        parts.forEach(function(p) {
            // 띄어쓰기 단위로 줄을 바꿈 (낱말이 한 줄보다 길 때만 글자 단위로 자름)
            var words = p.split(' '), line = '';
            for (var k = 0; k < words.length; k++) {
                var wd = words[k], tryL = line ? line + ' ' + wd : wd;
                if (bmp.measureTextWidth(tryL) <= maxW) { line = tryL; continue; }
                if (line) { out.push(line); line = ''; }
                if (bmp.measureTextWidth(wd) <= maxW) { line = wd; continue; }
                for (var i = 0; i < wd.length; i++) {
                    var t2 = line + wd[i];
                    if (bmp.measureTextWidth(t2) > maxW && line) { out.push(line); line = wd[i]; } else line = t2;
                }
            }
            out.push(line);
        });
        return out;
    }
    Window_EscGame.prototype.refresh = function() {
        var c = this.contents; if (!c || !this._def) return;
        c.clear();
        roundRect(c, 0, 0, this.contentsWidth(), this.contentsHeight(), 12, 'rgba(24,18,12,0.94)', 'rgba(200,160,96,0.6)', 2);
        var fn = this['draw_' + this._type];
        if (fn) fn.call(this);
    };

    // ----- knob: 주파수 노브 ---------------------------------------------------------------
    //  { type:'knob', title, help, stations:[{at: 0~100, name:'BBC 런던', text:'또렷하게 들릴 글', answer:true}], tol: 4 }
    Window_EscGame.prototype.bandRect = function() { var w = this.contentsWidth(); return { x: 30, y: 100, w: w - 60, h: 70 }; };
    Window_EscGame.prototype.knobStation = function() {
        var list = toArray(this._def.stations), tol = Number(this._def.tol || 4), best = null, bd = 999;
        for (var i = 0; i < list.length; i++) { var dd = Math.abs(Number(list[i].at) - this._pos); if (dd < bd) { bd = dd; best = list[i]; } }
        return { st: best, d: bd, clear: Math.max(0, 1 - bd / (tol * 3)), on: bd <= tol };
    };
    Window_EscGame.prototype.update_knob = function() {
        var sp = Input.isPressed('shift') ? 1.2 : 0.45;
        if (Input.isPressed('left')) this._pos = Math.max(0, this._pos - sp);
        if (Input.isPressed('right')) this._pos = Math.min(100, this._pos + sp);
        var r = this.bandRect();
        if (TouchInput.isPressed()) {
            var p = this.local();
            if (p.y > r.y - 20 && p.y < r.y + r.h + 40 && p.x > r.x - 20 && p.x < r.x + r.w + 20) this._pos = Math.max(0, Math.min(100, (p.x - r.x) / r.w * 100));
        }
        if (this.touchButtons()) return;
        if (Input.isTriggered('ok')) {
            var k = this.knobStation();
            if (!k.on) { this.say(escSub(this._def.noiseMsg || '치지직… 잡음뿐이에요. 노브를 더 돌려 봐요.'), '#ffcf9a'); return; }
            if (k.st.answer) { this.finish(true); return; }
            this.submit();
            if (!this._end) this.say(escSub(k.st.wrong || ('「' + (k.st.name || '') + '」 방송이에요. 찾는 방송이 아니에요.')), '#ffcf9a');
        }
    };
    Window_EscGame.prototype.draw_knob = function() {
        var c = this.contents, w = this.contentsWidth(), y0 = this.drawHeader(), r = this.bandRect(), i;
        r.y = Math.max(r.y, y0 + 6);
        // 눈금판
        roundRect(c, r.x - 10, r.y - 10, r.w + 20, r.h + 20, 12, '#3a2a18', '#c8a060', 3);
        c.fillRect(r.x, r.y, r.w, r.h, '#f0dfb0');
        c.fontSize = 13; c.textColor = '#4a3418';
        for (i = 0; i <= 50; i++) {
            var x = r.x + r.w * i / 50, big = i % 5 === 0;
            c.fillRect(x, r.y + r.h - (big ? 22 : 12), 2, big ? 22 : 12, '#4a3418');
            if (big) c.drawText(String(550 + i * 20), i === 0 ? x + 2 : (i === 50 ? x - 62 : x - 30), r.y + r.h - 46, 60, 20, i === 0 ? 'left' : (i === 50 ? 'right' : 'center'));
        }
        var list = toArray(this._def.stations);
        c.fontSize = 13;
        for (i = 0; i < list.length; i++) if (list[i].show !== false && list[i].name) {
            var sx = r.x + r.w * Number(list[i].at) / 100;
            c.textColor = '#7a2a18'; c.drawText(list[i].name, sx - 60, r.y + 2, 120, 18, 'center');
        }
        var nx = r.x + r.w * this._pos / 100;
        c.fillRect(nx - 2, r.y - 8, 4, r.h + 16, '#c81e1e');
        // 신호 세기
        var k = this.knobStation();
        c.fontSize = 16; c.textColor = '#ffffff'; c.drawText('신호', r.x, r.y + r.h + 18, 50, 22, 'left');
        for (i = 0; i < 10; i++) c.fillRect(r.x + 50 + i * 18, r.y + r.h + 22, 14, 14, i < Math.round(k.clear * 10) ? '#7dff9a' : 'rgba(255,255,255,0.18)');
        // 들리는 글
        var ty = r.y + r.h + 52, text = k.st ? escSub(k.st.text || '') : '';
        var lines = escWrap(c, text, w - 60), rnd = this._t;
        roundRect(c, 20, ty, w - 40, 112, 10, 'rgba(0,0,0,0.45)', 'rgba(255,255,255,0.2)', 1);
        c.fontSize = 18;
        var noise = '~*#%&@!?-_=+';
        for (var li = 0; li < lines.length && li < 4; li++) {
            var s = '';
            for (var j = 0; j < lines[li].length; j++) {
                var ch = lines[li][j];
                s += (ch !== ' ' && Math.random() > k.clear * 1.05) ? noise[(j * 7 + rnd + li) % noise.length] : ch;
            }
            c.textColor = k.on ? '#ffffff' : '#bcbcbc';
            c.drawText(s, 34, ty + 8 + li * 25, w - 68, 25, 'left');
        }
        c.fontSize = 15; this.changeTextColor('#d8ccb0');
        c.drawText('← → (누르고 있기) · 눈금판 끌기: 주파수 맞추기   Enter: 이 방송 듣기', 0, ty + 118, w, 22, 'center');
        this.drawMsg(ty + 142);
        this.drawButtons('이 방송 듣기', false);
    };

    // ----- strike: 사실과 다른 문장 지우기 -----------------------------------------------------
    //  { type:'strike', title, help, lines:[...], answer:[2,4], side:['증거 1', ...] }
    Window_EscGame.prototype.strikeRects = function() {
        var w = this.contentsWidth(), y0 = 82, side = toArray(this._def.side).length ? 250 : 0, list = toArray(this._def.lines), rs = [];
        var lh = Math.min(52, Math.floor((this.contentsHeight() - y0 - 110) / Math.max(1, list.length)));
        for (var i = 0; i < list.length; i++) rs.push({ x: 0, y: y0 + i * lh, w: w - side - 10, h: lh - 6 });
        return rs;
    };
    Window_EscGame.prototype.update_strike = function() {
        var n = this._marks.length;
        if (Input.isRepeated('down')) { this._cur = (this._cur + 1) % (n + 1); SoundManager.playCursor(); }
        if (Input.isRepeated('up')) { this._cur = (this._cur + n) % (n + 1); SoundManager.playCursor(); }
        if (TouchInput.isTriggered()) {
            var p = this.local(), rs = this.strikeRects();
            for (var i = 0; i < rs.length; i++) if (this.inside(rs[i], p)) { this._cur = i; this._marks[i] = !this._marks[i]; SoundManager.playOk(); return; }
            if (this.touchButtons()) return;
        }
        if (Input.isTriggered('ok')) {
            if (this._cur === n) { SoundManager.playOk(); this.submit(); }
            else { this._marks[this._cur] = !this._marks[this._cur]; SoundManager.playOk(); }
        }
    };
    Window_EscGame.prototype.draw_strike = function() {
        var c = this.contents, w = this.contentsWidth(), list = toArray(this._def.lines), rs = this.strikeRects(), i;
        this.drawHeader();
        for (i = 0; i < list.length; i++) {
            var r = rs[i], on = this._marks[i], cur = this._cur === i && !this._end;
            roundRect(c, r.x, r.y, r.w, r.h, 8, cur ? 'rgba(255,220,120,0.22)' : 'rgba(255,255,255,0.07)', cur ? '#ffe08a' : 'rgba(255,255,255,0.15)', cur ? 2 : 1);
            c.fontSize = 17; c.textColor = on ? '#ff9a8a' : '#ffffff';
            var lines = escWrap(c, escSub(list[i]), r.w - 20);
            var lh = Math.min(22, r.h / Math.max(1, lines.length));
            for (var k = 0; k < lines.length && k < 2; k++) {
                var ty = r.y + (r.h - Math.min(2, lines.length) * 22) / 2 + k * 22;
                c.drawText(lines[k], r.x + 12, ty, r.w - 24, 22, 'left');
                if (on) c.fillRect(r.x + 10, ty + 11, Math.min(r.w - 20, c.measureTextWidth(lines[k]) + 4), 3, '#ff4a3a');
            }
        }
        var side = toArray(this._def.side);
        if (side.length) {
            var sx = w - 245, sy = 82;
            roundRect(c, sx, sy, 245, rs.length ? rs[rs.length - 1].y + rs[rs.length - 1].h - sy : 200, 10, 'rgba(246,236,206,0.95)', '#c8a060', 2);
            c.fontSize = 16; c.textColor = '#7a2a18'; c.drawText(escSub(this._def.sideTitle || '증거'), sx, sy + 6, 245, 22, 'center');
            c.fontSize = 15; c.textColor = '#3a2a18';
            var yy = sy + 34;
            side.forEach(function(s) { escWrap(c, '· ' + escSub(s), 225).forEach(function(l) { c.drawText(l, sx + 10, yy, 230, 20, 'left'); yy += 20; }); yy += 6; });
        }
        c.fontSize = 15; this.changeTextColor('#d8ccb0');
        c.drawText('↑↓ 고르기 · Enter 또는 클릭: 빨간 줄 긋기/지우기 · 다 고르면 [확인]', 0, this.contentsHeight() - 96, w, 22, 'center');
        this.drawMsg(this.contentsHeight() - 74);
        this.drawButtons('확인', this._cur === list.length);
    };

    // ----- sort: 항목을 칸에 나눠 담기 ------------------------------------------------------
    //  { type:'sort', title, help, bins:['가방에 넣기','두고 가기'], items:[{text:'가족 사진'}, ...], answer:[1,2,...] }
    Window_EscGame.prototype.sortLayout = function() {
        var w = this.contentsWidth(), h = this.contentsHeight(), bins = toArray(this._def.bins), items = toArray(this._def.items);
        var y0 = 86, poolH = Math.ceil(items.length / 3) * 40 + 10, by = y0 + poolH + 10, bh = h - by - 110;
        var bw = (w - (bins.length - 1) * 10) / bins.length, L = { pool: { x: 0, y: y0, w: w, h: poolH }, bins: [], items: [] };
        for (var b = 0; b < bins.length; b++) L.bins.push({ x: b * (bw + 10), y: by, w: bw, h: bh });
        var cnt = bins.map(function() { return 0; }), pc = 0, iw = Math.min(240, (w - 20) / 3);
        for (var i = 0; i < items.length; i++) {
            var bi = this._bins[i];
            if (bi < 0) { L.items.push({ x: 4 + (pc % 3) * (iw + 6), y: y0 + 6 + Math.floor(pc / 3) * 40, w: iw, h: 34 }); pc++; }
            else { var bb = L.bins[bi], per = Math.max(1, Math.floor((bb.w - 8) / 200)), cw = (bb.w - 8) / per - 6, k = cnt[bi]++;
                L.items.push({ x: bb.x + 6 + (k % per) * (cw + 6), y: bb.y + 32 + Math.floor(k / per) * 38, w: cw, h: 32 }); }
        }
        return L;
    };
    Window_EscGame.prototype.update_sort = function() {
        var n = this._bins.length, nb = toArray(this._def.bins).length;
        if (Input.isRepeated('down')) { this._cur = (this._cur + 1) % (n + 1); SoundManager.playCursor(); }
        if (Input.isRepeated('up')) { this._cur = (this._cur + n) % (n + 1); SoundManager.playCursor(); }
        if (this._cur < n && (Input.isRepeated('right') || Input.isRepeated('left'))) {
            var dir = Input.isRepeated('right') ? 1 : -1, v = this._bins[this._cur];
            v = v < 0 ? (dir > 0 ? 0 : nb - 1) : v + dir;
            if (v >= nb) v = 0; if (v < 0) v = nb - 1;
            this._bins[this._cur] = v; SoundManager.playCursor();
        }
        if (Input.isTriggered('ok')) {
            if (this._cur === n) { SoundManager.playOk(); this.submit(); }
            else { var v2 = this._bins[this._cur] + 1; if (v2 >= nb) v2 = 0; this._bins[this._cur] = v2; SoundManager.playOk(); }
        }
        if (TouchInput.isTriggered()) {
            var p = this.local(), L = this.sortLayout(), i;
            for (i = 0; i < n; i++) if (this.inside(L.items[i], p)) { this._drag = i; this._cur = i; this._dragFrom = { x: p.x, y: p.y }; return; }
            if (this.touchButtons()) return;
        }
        if (this._drag !== undefined && this._drag >= 0) {
            if (TouchInput.isPressed()) { this._dragP = this.local(); return; }
            var q = this._dragP || this._dragFrom, L2 = this.sortLayout(), moved = false;
            for (var b = 0; b < L2.bins.length; b++) if (this.inside(L2.bins[b], q)) { this._bins[this._drag] = b; moved = true; }
            if (!moved && Math.abs(q.x - this._dragFrom.x) < 8 && Math.abs(q.y - this._dragFrom.y) < 8) {   // 톡: 다음 칸으로
                var v3 = this._bins[this._drag] + 1; if (v3 >= nb) v3 = 0; this._bins[this._drag] = v3;
            }
            SoundManager.playOk(); this._drag = -1; this._dragP = null;
        }
    };
    Window_EscGame.prototype.draw_sort = function() {
        var c = this.contents, w = this.contentsWidth(), L = this.sortLayout(), bins = toArray(this._def.bins), items = toArray(this._def.items), i;
        this.drawHeader();
        roundRect(c, L.pool.x, L.pool.y, L.pool.w, L.pool.h, 8, 'rgba(255,255,255,0.05)', 'rgba(255,255,255,0.15)', 1);
        var pal = ['rgba(120,170,230,0.25)', 'rgba(230,140,120,0.25)', 'rgba(140,210,140,0.25)', 'rgba(220,200,110,0.25)'];
        for (var b = 0; b < L.bins.length; b++) {
            var bb = L.bins[b];
            roundRect(c, bb.x, bb.y, bb.w, bb.h, 10, pal[b % 4], 'rgba(255,255,255,0.35)', 2);
            c.fontSize = 18; c.textColor = '#ffe9b0'; c.drawText(escSub(bins[b]), bb.x, bb.y + 4, bb.w, 24, 'center');
        }
        for (i = 0; i < items.length; i++) {
            var r = L.items[i], cur = this._cur === i && !this._end;
            if (this._drag === i && this._dragP) r = { x: this._dragP.x - r.w / 2, y: this._dragP.y - r.h / 2, w: r.w, h: r.h };
            roundRect(c, r.x, r.y, r.w, r.h, 8, cur ? 'rgba(255,230,160,0.98)' : 'rgba(246,236,206,0.95)', cur ? '#ffffff' : '#8a6a40', cur ? 3 : 1);
            c.fontSize = 16; c.textColor = '#2a1a06';
            var s = escSub(items[i].text || items[i]), fs = 16;
            while (fs > 13 && c.measureTextWidth(s) > r.w - 12) { fs--; c.fontSize = fs; }
            if (c.measureTextWidth(s) > r.w - 12 && s.indexOf(' ') > 0) {     // 너무 길면 두 줄로 (글씨를 작게 줄이지 않게)
                var ln2 = null;
                for (fs = 15; fs >= 11; fs--) { c.fontSize = fs; ln2 = escWrap(c, s, r.w - 12); if (ln2.length <= 2) break; }
                var lh = Math.min(fs + 3, (r.h - 2) / 2);
                for (var q = 0; q < Math.min(2, ln2.length); q++) c.drawText(ln2[q], r.x + 6, r.y + (r.h - lh * Math.min(2, ln2.length)) / 2 + q * lh, r.w - 12, lh, 'center');
            } else c.drawText(s, r.x + 6, r.y + (r.h - 22) / 2, r.w - 12, 22, 'center');
        }
        c.fontSize = 15; this.changeTextColor('#d8ccb0');
        c.drawText('↑↓ 고르기 · ← → 칸 옮기기 · 끌어다 놓기도 돼요 · 다 놓으면 [확인]', 0, this.contentsHeight() - 96, w, 22, 'center');
        this.drawMsg(this.contentsHeight() - 74);
        this.drawButtons('확인', this._cur === items.length);
    };

    // ----- order: 순서대로 놓기 ----------------------------------------------------------
    //  { type:'order', title, help, items:['A','B',...], answer:[3,1,2,...] (위에서부터 놓일 항목 번호), axis:['먼저','나중'] }
    Window_EscGame.prototype.orderRects = function() {
        var w = this.contentsWidth(), n = this._ord.length, y0 = 90, lh = Math.min(56, Math.floor((this.contentsHeight() - y0 - 110) / n)), rs = [];
        for (var i = 0; i < n; i++) rs.push({ x: 60, y: y0 + i * lh, w: w - 120, h: lh - 8 });
        return rs;
    };
    Window_EscGame.prototype.update_order = function() {
        var n = this._ord.length, t;
        if (this._sel < 0) {
            if (Input.isRepeated('down')) { this._cur = (this._cur + 1) % (n + 1); SoundManager.playCursor(); }
            if (Input.isRepeated('up')) { this._cur = (this._cur + n) % (n + 1); SoundManager.playCursor(); }
            if (Input.isTriggered('ok')) {
                if (this._cur === n) { SoundManager.playOk(); this.submit(); } else { this._sel = this._cur; SoundManager.playOk(); }
            }
        } else {
            if (Input.isRepeated('down') && this._sel < n - 1) { t = this._ord[this._sel]; this._ord[this._sel] = this._ord[this._sel + 1]; this._ord[this._sel + 1] = t; this._sel++; this._cur = this._sel; SoundManager.playCursor(); }
            if (Input.isRepeated('up') && this._sel > 0) { t = this._ord[this._sel]; this._ord[this._sel] = this._ord[this._sel - 1]; this._ord[this._sel - 1] = t; this._sel--; this._cur = this._sel; SoundManager.playCursor(); }
            if (Input.isTriggered('ok')) { this._sel = -1; SoundManager.playOk(); }
        }
        if (TouchInput.isTriggered()) {
            var p = this.local(), rs = this.orderRects();
            for (var i = 0; i < rs.length; i++) if (this.inside(rs[i], p)) {
                if (this._sel >= 0 && this._sel !== i) { t = this._ord[this._sel]; this._ord[this._sel] = this._ord[i]; this._ord[i] = t; this._sel = -1; }
                else this._sel = this._sel === i ? -1 : i;
                this._cur = i; SoundManager.playOk(); return;
            }
            this.touchButtons();
        }
    };
    Window_EscGame.prototype.draw_order = function() {
        var c = this.contents, w = this.contentsWidth(), items = toArray(this._def.items), rs = this.orderRects(), i, axis = toArray(this._def.axis);
        this.drawHeader();
        c.fillRect(30, rs[0].y + 6, 4, rs[rs.length - 1].y + rs[rs.length - 1].h - rs[0].y - 12, 'rgba(255,220,140,0.6)');
        c.fontSize = 14; c.textColor = '#ffe9b0';
        if (axis[0]) c.drawText(escSub(axis[0]), 0, rs[0].y - 22, 70, 20, 'center');
        if (axis[1]) c.drawText(escSub(axis[1]), 0, rs[rs.length - 1].y + rs[rs.length - 1].h, 70, 20, 'center');
        for (i = 0; i < rs.length; i++) {
            var r = rs[i], cur = this._cur === i && !this._end, sel = this._sel === i;
            c.fillRect(24, r.y + r.h / 2 - 8, 16, 16, '#ffd070');
            roundRect(c, r.x, r.y, r.w, r.h, 8, sel ? 'rgba(255,214,100,0.98)' : 'rgba(246,236,206,0.95)', cur ? '#ffffff' : '#8a6a40', cur ? 3 : 1);
            c.fontSize = 17; c.textColor = '#2a1a06';
            c.drawText((i + 1) + '.  ' + escSub(items[this._ord[i]]), r.x + 12, r.y + (r.h - 24) / 2, r.w - 24, 24, 'left');
            if (sel) { c.fontSize = 14; c.drawText('↑↓ 로 옮기기', r.x + r.w - 130, r.y + (r.h - 24) / 2, 120, 24, 'right'); }
        }
        c.fontSize = 15; this.changeTextColor('#d8ccb0');
        c.drawText('Enter(클릭)로 카드를 집고 ↑↓ 로 옮긴 뒤 다시 Enter · 다 놓으면 [확인]', 0, this.contentsHeight() - 96, w, 22, 'center');
        this.drawMsg(this.contentsHeight() - 74);
        this.drawButtons('확인', this._cur === items.length && this._sel < 0);
    };

    // ----- lights: 등화관제 (불 켜진 창 끄기) ----------------------------------------------
    //  { type:'lights', title, help, cols:6, rows:3, goal:12, time:40, every:70, maxLit:10 }
    Window_EscGame.prototype.lightRect = function(i) {
        var w = this.contentsWidth(), gx = 40, gy = 110, gw = w - 80, gh = this.contentsHeight() - gy - 120;
        var cw = gw / this._cols, ch = gh / this._rows, cx = i % this._cols, cy = Math.floor(i / this._cols);
        return { x: gx + cx * cw + 8, y: gy + cy * ch + 8, w: cw - 16, h: ch - 16 };
    };
    Window_EscGame.prototype.update_lights = function() {
        var d = this._def, n = this._lit.length;
        this._time--;
        if (++this._spawn >= Number(d.every || 70)) { this._spawn = 0; this.lightOne(); if (Math.random() < 0.35) this.lightOne(); }
        if (Input.isRepeated('right')) this._cx = (this._cx + 1) % this._cols;
        if (Input.isRepeated('left')) this._cx = (this._cx + this._cols - 1) % this._cols;
        if (Input.isRepeated('down')) this._cy = (this._cy + 1) % this._rows;
        if (Input.isRepeated('up')) this._cy = (this._cy + this._rows - 1) % this._rows;
        var hit = -1;
        if (Input.isTriggered('ok')) hit = this._cy * this._cols + this._cx;
        if (TouchInput.isTriggered()) {
            var p = this.local();
            for (var i = 0; i < n; i++) if (this.inside(this.lightRect(i), p)) { hit = i; this._cx = i % this._cols; this._cy = Math.floor(i / this._cols); }
            if (hit < 0 && this.touchButtons()) return;
        }
        if (hit >= 0 && this._lit[hit]) { this._lit[hit] = false; this._off++; SoundManager.playCursor(); }
        var litN = this._lit.filter(function(v) { return v; }).length;
        if (this._off >= Number(d.goal || 12)) { this.finish(true); return; }
        if (this._time <= 0 || litN >= Number(d.maxLit || n)) {
            this._fails++;
            if (this._fails >= Number(d.autoAfter || 3)) { this.finish(true, true); return; }
            this.say(this._fails >= 2 && d.hint ? '힌트: ' + escSub(d.hint) : escSub(d.failMsg || '불빛이 너무 많아요! 다시 해 봐요.'), '#ff9a8a');
            SoundManager.playBuzzer();
            for (var k = 0; k < n; k++) this._lit[k] = false;
            for (k = 0; k < Number(d.startLit || 4); k++) this.lightOne();
            this._off = 0; this._time = Number(d.time || 40) * 60;
        }
    };
    Window_EscGame.prototype.draw_lights = function() {
        var c = this.contents, w = this.contentsWidth(), d = this._def, i;
        this.drawHeader();
        c.fontSize = 18; c.textColor = '#ffffff';
        c.drawText('끈 창: ' + this._off + ' / ' + Number(d.goal || 12), 40, 80, 200, 24, 'left');
        c.drawText('폭격기 도착까지 ' + Math.max(0, Math.ceil(this._time / 60)) + '초', w - 280, 80, 240, 24, 'right');
        var gx = 40, gy = 110, gw = w - 80, gh = this.contentsHeight() - gy - 120;
        c.fillRect(gx, gy, gw, gh, '#4a3a34');
        for (var yy = gy; yy < gy + gh; yy += 10) c.fillRect(gx, yy, gw, 1, 'rgba(0,0,0,0.25)');
        for (i = 0; i < this._lit.length; i++) {
            var r = this.lightRect(i), cur = (i === this._cy * this._cols + this._cx) && !this._end;
            c.fillRect(r.x, r.y, r.w, r.h, this._lit[i] ? '#ffd86a' : '#1a1a24');
            if (this._lit[i]) c.fillRect(r.x + 4, r.y + 4, r.w - 8, r.h / 2, '#fff0b0');
            c.fillRect(r.x + r.w / 2 - 1, r.y, 2, r.h, '#4a3a34'); c.fillRect(r.x, r.y + r.h / 2 - 1, r.w, 2, '#4a3a34');
            if (cur) { c.fillRect(r.x - 4, r.y - 4, r.w + 8, 3, '#ffffff'); c.fillRect(r.x - 4, r.y + r.h + 1, r.w + 8, 3, '#ffffff');
                       c.fillRect(r.x - 4, r.y - 4, 3, r.h + 8, '#ffffff'); c.fillRect(r.x + r.w + 1, r.y - 4, 3, r.h + 8, '#ffffff'); }
        }
        c.fontSize = 15; this.changeTextColor('#d8ccb0');
        c.drawText('방향키로 고르고 Enter · 또는 불 켜진 창을 클릭(톡)해서 커튼 치기', 0, this.contentsHeight() - 96, w, 22, 'center');
        this.drawMsg(this.contentsHeight() - 74);
        this.drawButtons('　', false);
    };

    // ----- match: 선 잇기 -----------------------------------------------------------------
    //  { type:'match', title, help, left:[...], right:[...], answer:[2,1,3] (왼쪽 i 와 이어질 오른쪽 번호) }
    Window_EscGame.prototype.matchRects = function() {
        var w = this.contentsWidth(), L = toArray(this._def.left), R = toArray(this._def.right), y0 = 90;
        var n = Math.max(L.length, R.length), lh = Math.min(64, Math.floor((this.contentsHeight() - y0 - 110) / n)), cw = (w - 120) / 2;
        var out = { l: [], r: [] };
        for (var i = 0; i < L.length; i++) out.l.push({ x: 0, y: y0 + i * lh, w: cw, h: lh - 8 });
        for (i = 0; i < R.length; i++) out.r.push({ x: w - cw, y: y0 + i * lh, w: cw, h: lh - 8 });
        return out;
    };
    Window_EscGame.prototype.update_match = function() {
        var nl = this._links.length, nr = toArray(this._def.right).length;
        if (this._side === 0) {
            if (Input.isRepeated('down')) { this._cur = (this._cur + 1) % (nl + 1); SoundManager.playCursor(); }
            if (Input.isRepeated('up')) { this._cur = (this._cur + nl) % (nl + 1); SoundManager.playCursor(); }
            if (Input.isTriggered('ok')) {
                if (this._cur === nl) { SoundManager.playOk(); this.submit(); }
                else { this._side = 1; this._rc = Math.max(0, this._links[this._cur]); SoundManager.playOk(); }
            }
        } else {
            if (Input.isRepeated('down')) { this._rc = (this._rc + 1) % nr; SoundManager.playCursor(); }
            if (Input.isRepeated('up')) { this._rc = (this._rc + nr - 1) % nr; SoundManager.playCursor(); }
            if (Input.isTriggered('ok')) { this.linkTo(this._cur, this._rc); this._side = 0; if (this._cur < nl - 1) this._cur++; }
            if (Input.isTriggered('left')) this._side = 0;
        }
        if (TouchInput.isTriggered()) {
            var p = this.local(), rs = this.matchRects(), i;
            for (i = 0; i < rs.l.length; i++) if (this.inside(rs.l[i], p)) { this._cur = i; this._side = 1; this._rc = Math.max(0, this._links[i]); SoundManager.playOk(); return; }
            for (i = 0; i < rs.r.length; i++) if (this.inside(rs.r[i], p) && this._side === 1) { this.linkTo(this._cur, i); this._side = 0; return; }
            this.touchButtons();
        }
    };
    Window_EscGame.prototype.linkTo = function(l, r) {
        for (var i = 0; i < this._links.length; i++) if (this._links[i] === r && toArray(this._def.right).length === this._links.length) this._links[i] = -1;
        this._links[l] = r; SoundManager.playOk();
    };
    Window_EscGame.prototype.draw_match = function() {
        var c = this.contents, w = this.contentsWidth(), L = toArray(this._def.left), R = toArray(this._def.right), rs = this.matchRects(), i, ctx;
        this.drawHeader();
        var cols = ['#ff8a6a', '#7ac8ff', '#9dff9a', '#ffd86a', '#d89aff', '#ffffff'];
        ctx = ctxOf(c);
        for (i = 0; i < L.length; i++) if (this._links[i] >= 0) {
            var a = rs.l[i], b = rs.r[this._links[i]];
            ctx.strokeStyle = cols[i % cols.length]; ctx.lineWidth = 4; ctx.beginPath(); ctx.moveTo(a.x + a.w, a.y + a.h / 2); ctx.lineTo(b.x, b.y + b.h / 2); ctx.stroke();
        }
        setDirty(c);
        var self = this;
        function box(r, text, cur, col) {
            roundRect(c, r.x, r.y, r.w, r.h, 8, 'rgba(246,236,206,0.95)', cur ? '#ffffff' : (col || '#8a6a40'), cur ? 3 : 2);
            c.fontSize = 16; c.textColor = '#2a1a06';
            var ls = escWrap(c, escSub(text), r.w - 16);
            for (var k = 0; k < ls.length && k < 2; k++) c.drawText(ls[k], r.x + 8, r.y + (r.h - Math.min(2, ls.length) * 21) / 2 + k * 21, r.w - 16, 21, 'center');
        }
        for (i = 0; i < L.length; i++) box(rs.l[i], L[i], this._side === 0 && this._cur === i && !this._end, this._links[i] >= 0 ? cols[i % cols.length] : null);
        for (i = 0; i < R.length; i++) box(rs.r[i], R[i], this._side === 1 && this._rc === i && !this._end);
        c.fontSize = 15; this.changeTextColor('#d8ccb0');
        c.drawText('왼쪽 카드를 고르고(Enter·클릭) → 이어질 오른쪽 카드를 고르기 · 다 이으면 [확인]', 0, this.contentsHeight() - 96, w, 22, 'center');
        this.drawMsg(this.contentsHeight() - 74);
        this.drawButtons('확인', this._side === 0 && this._cur === L.length);
    };

    // ----- wheel: 암호 바퀴 (글자 밀기) -------------------------------------------------------
    //  { type:'wheel', title, help, cipher:'DWWDFN', shift:3, example:['A→D'] }
    function escShiftText(s, k) {
        return String(s).replace(/[A-Z]/g, function(ch) { return String.fromCharCode((ch.charCodeAt(0) - 65 - k + 260) % 26 + 65); });
    }
    Window_EscGame.prototype.update_wheel = function() {
        if (Input.isRepeated('right')) { this._shift = (this._shift + 1) % 26; SoundManager.playCursor(); }
        if (Input.isRepeated('left')) { this._shift = (this._shift + 25) % 26; SoundManager.playCursor(); }
        if (TouchInput.isTriggered()) {
            var p = this.local(), w = this.contentsWidth();
            if (this.touchButtons()) return;
            if (p.y > 90 && p.y < this.contentsHeight() - 110) { this._shift = (this._shift + (p.x > w / 2 ? 1 : 25)) % 26; SoundManager.playCursor(); }
        }
        if (Input.isTriggered('ok')) { SoundManager.playOk(); this.submit(); }
    };
    Window_EscGame.prototype.draw_wheel = function() {
        var c = this.contents, w = this.contentsWidth(), d = this._def, ctx, i;
        this.drawHeader();
        var cx = 170, cy = 92 + 140, R1 = 128, R2 = 96;
        ctx = ctxOf(c);
        ctx.fillStyle = '#3a2a18'; ctx.beginPath(); ctx.arc(cx, cy, R1 + 18, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#f0dfb0'; ctx.beginPath(); ctx.arc(cx, cy, R1 + 12, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#d8c090'; ctx.beginPath(); ctx.arc(cx, cy, R2 + 12, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#5a3a20'; ctx.beginPath(); ctx.arc(cx, cy, 30, 0, Math.PI * 2); ctx.fill();
        ctx.font = 'bold 15px GameFont'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        for (i = 0; i < 26; i++) {
            var a = -Math.PI / 2 + i / 26 * Math.PI * 2;
            ctx.fillStyle = '#7a2a18'; ctx.fillText(String.fromCharCode(65 + i), cx + Math.cos(a) * R1, cy + Math.sin(a) * R1);        // 바깥: 암호 글자
            var b = a;                                                                                                                  // 안쪽: 원래 글자 (밀린 만큼)
            ctx.fillStyle = '#1a2a4a'; ctx.fillText(String.fromCharCode(65 + (i - this._shift + 26) % 26), cx + Math.cos(b) * R2, cy + Math.sin(b) * R2);
        }
        ctx.strokeStyle = '#c81e1e'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(cx, cy - R1 - 16); ctx.lineTo(cx, cy - R2 + 8); ctx.stroke();
        setDirty(c);
        var x0 = 340, y = 100;
        c.fontSize = 16; c.textColor = '#d8ccb0'; c.drawText('가로챈 암호', x0, y, w - x0, 22, 'left'); y += 24;
        c.fontSize = 26; c.textColor = '#ff9a8a'; c.drawText(String(d.cipher), x0, y, w - x0, 32, 'left'); y += 42;
        c.fontSize = 16; c.textColor = '#d8ccb0'; c.drawText('바퀴로 풀어 본 글자', x0, y, w - x0, 22, 'left'); y += 24;
        c.fontSize = 26; c.textColor = '#9dffb0'; c.drawText(escShiftText(String(d.cipher), this._shift), x0, y, w - x0, 32, 'left'); y += 42;
        c.fontSize = 16; c.textColor = '#ffe9b0'; c.drawText('바퀴를 ' + this._shift + '칸 돌림', x0, y, w - x0, 22, 'left'); y += 30;
        toArray(d.example).forEach(function(e) { c.fontSize = 15; c.textColor = '#d8ccb0'; c.drawText(escSub(e), x0, y, w - x0, 22, 'left'); y += 22; });
        c.fontSize = 15; this.changeTextColor('#d8ccb0');
        c.drawText('← → (또는 바퀴 왼쪽·오른쪽 클릭): 바퀴 돌리기 · 뜻이 통하면 Enter', 0, this.contentsHeight() - 96, w, 22, 'center');
        this.drawMsg(this.contentsHeight() - 74);
        this.drawButtons('이 글자로 확인', true);
    };

    // ----- pick: 값 맞춰 내기 (지폐 고르기) ------------------------------------------------
    //  { type:'pick', title, help, items:[{label:'1억 마르크', value:1, max:9}], target: 200, unit:'억 마르크', solution:[...] }
    Window_EscGame.prototype.pickRects = function() {
        var w = this.contentsWidth(), items = toArray(this._def.items), y0 = 130, rs = [];
        var cw = Math.min(170, (w - 20) / items.length - 10);
        for (var i = 0; i < items.length; i++) rs.push({ x: (w - items.length * (cw + 10)) / 2 + i * (cw + 10), y: y0, w: cw, h: 150 });
        return rs;
    };
    Window_EscGame.prototype.pickSum = function() {
        var items = toArray(this._def.items), s = 0;
        for (var i = 0; i < items.length; i++) s += this._picked[i] * Number(items[i].value);
        return s;
    };
    Window_EscGame.prototype.update_pick = function() {
        var items = toArray(this._def.items), n = items.length;
        if (Input.isRepeated('right')) { this._cur = (this._cur + 1) % (n + 1); SoundManager.playCursor(); }
        if (Input.isRepeated('left')) { this._cur = (this._cur + n) % (n + 1); SoundManager.playCursor(); }
        if (this._cur < n) {
            var mx = Number(items[this._cur].max || 9);
            if (Input.isRepeated('up') || Input.isTriggered('ok')) { this._picked[this._cur] = Math.min(mx, this._picked[this._cur] + 1); SoundManager.playCursor(); }
            if (Input.isRepeated('down')) { this._picked[this._cur] = Math.max(0, this._picked[this._cur] - 1); SoundManager.playCursor(); }
        } else if (Input.isTriggered('ok')) { SoundManager.playOk(); this.submit(); }
        if (TouchInput.isTriggered()) {
            var p = this.local(), rs = this.pickRects();
            for (var i = 0; i < n; i++) if (this.inside(rs[i], p)) {
                this._cur = i;
                if (p.y > rs[i].y + rs[i].h - 40) this._picked[i] = Math.max(0, this._picked[i] - 1);
                else this._picked[i] = Math.min(Number(items[i].max || 9), this._picked[i] + 1);
                SoundManager.playCursor(); return;
            }
            this.touchButtons();
        }
    };
    Window_EscGame.prototype.draw_pick = function() {
        var c = this.contents, w = this.contentsWidth(), d = this._def, items = toArray(d.items), rs = this.pickRects(), i;
        this.drawHeader();
        c.fontSize = 20; c.textColor = '#ffe9b0';
        c.drawText('내야 할 돈: ' + escSub(d.targetLabel || (d.target + (d.unit || ''))), 0, 92, w / 2, 28, 'center');
        var sum = this.pickSum();
        c.textColor = sum === Number(d.target) ? '#9dffb0' : '#ffffff';
        c.drawText('지금 고른 돈: ' + sum + (d.unit || ''), w / 2, 92, w / 2, 28, 'center');
        for (i = 0; i < items.length; i++) {
            var r = rs[i], cur = this._cur === i && !this._end;
            roundRect(c, r.x, r.y, r.w, r.h, 10, 'rgba(206,214,180,0.95)', cur ? '#ffffff' : '#6a7a50', cur ? 3 : 2);
            for (var k = 0; k < Math.min(6, this._picked[i]); k++) c.fillRect(r.x + 12 + k * 4, r.y + 40 - k * 3, r.w - 40, 30, k % 2 ? '#b8c49a' : '#a8b48a');
            c.fontSize = 17; c.textColor = '#1a2a10'; c.drawText(escSub(items[i].label), r.x, r.y + 76, r.w, 24, 'center');
            c.fontSize = 22; c.drawText('× ' + this._picked[i], r.x, r.y + 100, r.w, 28, 'center');
            c.fontSize = 13; c.drawText('▲ 더 · ▼ 빼기', r.x, r.y + r.h - 24, r.w, 20, 'center');
        }
        c.fontSize = 15; this.changeTextColor('#d8ccb0');
        c.drawText('← → 지폐 고르기 · ↑(Enter) 한 묶음 더 · ↓ 빼기 · 클릭: 위쪽 더하기 / 아래쪽 빼기', 0, this.contentsHeight() - 96, w, 22, 'center');
        this.drawMsg(this.contentsHeight() - 74);
        this.drawButtons('돈 내기', this._cur === items.length);
    };

    // ---- 창 붙이기 · 단계 처리 -----------------------------------------------------------
    var _v43_createDO = Scene_Map.prototype.createDisplayObjects;
    Scene_Map.prototype.createDisplayObjects = function() {
        _v43_createDO.apply(this, arguments);
        if (!EscapeManager.isActive()) return;
        this._escGame = new Window_EscGame();
        this.addWindow(this._escGame);
    };
    var _v43_closeAll = Scene_Map.prototype.escCloseAll;
    Scene_Map.prototype.escCloseAll = function() {
        _v43_closeAll.apply(this, arguments);
        if (this._escGame) { this._escGame.deactivate(); this._escGame.close(); }
    };
    EscapeManager.startGame = function(s) {
        var self = this, scene = this._scene, def = s.game, win = scene && scene._escGame;
        if (!win) { this.insertSteps(toArray(def.success)); return; }
        this._waiting = true; this._gameOpen = true;
        $gameTemp.clearDestination();
        win.setup(def);
        win.setHandler('done', function(ok) {
            win.close(); win.deactivate(); self._gameOpen = false;
            self.insertSteps(toArray(ok ? def.success : (def.fail || [{ game: def }])));
            self.resume();
        });
        win.setHandler('cancel', function() {
            win.close(); win.deactivate(); self._gameOpen = false;
            self.insertSteps(toArray(def.cancel || [{ text: '나중에 다시 해 보자. (같은 곳을 다시 조사하면 이어서 할 수 있어요)' }]));
            self.resume();
        });
    };
    var _v43_ps = EscapeManager.processStep;
    EscapeManager.processStep = function(s) {
        if (s && typeof s === 'object' && s.game) {
            if (s.text) this.insertSteps([{ text: s.text, speaker: s.speaker, face: s.face }, { game: s.game }]);
            else this.startGame(s);
            return;
        }
        // 실행 중 오류가 나도 게임이 멈추지 않게: 그 단계만 건너뛰고 계속
        try { return _v43_ps.apply(this, arguments); }
        catch (e) {
            console.error('[EscapeRoom] 단계 처리 오류 - 건너뜀', e, s);
            this._waiting = false;
        }
    };

    // ---- 2) 멈춤 방지 안전장치 ---------------------------------------------------------------
    EscapeManager.escModalVisible = function() {
        var sc = this._scene; if (!sc) return false;
        var open = function(w) { return !!(w && w.isOpen && (w.isOpen() || w.isOpening && w.isOpening())); };
        if (sc._escMsg && (sc._escMsg.isOpen() || sc._escMsg.isOpening())) return true;
        if (open(sc._escChoice) || open(sc._escNumpad) || open(sc._escDial) || open(sc._escTiming) || open(sc._escGame) || open(sc._escBag)) return true;
        if (this._movie || this._focus || this._mission || this._chase || this._gameOpen || this._bagOpen) return true;
        if (this._moveWait && this._moves && this._moves.length) return true;
        if (sc._escGate || sc._escGateT) return true;
        return false;
    };
    EscapeManager.escWatchdog = function() {
        var sc = this._scene;
        if (!sc || !(sc instanceof Scene_Map) || !this.isActive()) return;
        if (this._phase !== 'play' && this._phase !== 'intro') { this._wd = null; return; }
        var wd = this._wd || (this._wd = { orphan: 0, trans: 0, dark: 0, cine: 0, boxed: 0, ev: 0 });
        // (가) 아무 창도 없는데 계속 기다림
        if (this._waiting && !this._waitTransfer && !this.escModalVisible() && !sc.isBusy()) {
            if (++wd.orphan > 150) { console.warn('[EscapeRoom] 안전장치: 끝나지 않은 기다림을 풀었어요'); wd.orphan = 0; this._moveWait = false; this.resume(); }
        } else wd.orphan = 0;
        // (나) 장소 이동을 기다리는데 이동이 일어나지 않음
        if (this._waitTransfer && !$gamePlayer.isTransferring() && !sc.isBusy()) {
            if (++wd.trans > 120) { console.warn('[EscapeRoom] 안전장치: 장소 이동 기다림을 풀었어요'); wd.trans = 0; this._waitTransfer = false; }
        } else wd.trans = 0;
        // (다) 할 일이 없는데 화면이 계속 어두움
        if (this._phase === 'play' && !this.isBusy() && $gameScreen.brightness() < 255 && !$gameScreen._fadeInDuration && !$gameScreen._fadeOutDuration && !$gamePlayer.isTransferring()) {
            if (++wd.dark > 90) { console.warn('[EscapeRoom] 안전장치: 어두운 화면을 밝혔어요'); wd.dark = 0; $gameScreen.startFadeIn(24); }
        } else wd.dark = 0;
        // (라) 장면이 끝났는데 시네마틱(검은 띠·카메라)이 남아 있음
        if ((this._cine || this._cam) && !this.isBusy() && this._queue.length === 0) {
            if (++wd.cine > 120) { console.warn('[EscapeRoom] 안전장치: 시네마틱을 끝냈어요'); wd.cine = 0; this.setCinema(false); if (this._cam) { this._cam = null; $gameScreen.clearZoom(); } }
        } else wd.cine = 0;
        // (마) 주인공 사방이 사람·물건 이벤트로 막힘 → 막은 이벤트를 지나갈 수 있게
        if (this.canInteract() && !$gamePlayer.isMoving()) {
            var px = $gamePlayer.x, py = $gamePlayer.y, blockers = [], free = false;
            [2, 4, 6, 8].forEach(function(d) {
                var nx = $gameMap.roundXWithDirection(px, d), ny = $gameMap.roundYWithDirection(py, d);
                if (!$gameMap.isPassable(px, py, d) || !$gameMap.isValid(nx, ny) || $gameMap.regionId(nx, ny) === WALL_REGION) return;
                var evs = $gameMap.eventsXyNt(nx, ny).filter(function(e) { return e.isNormalPriority() && !e._erased; });
                if (evs.length) blockers = blockers.concat(evs); else free = true;
            });
            if (!free && blockers.length) {
                if (++wd.boxed > 120) { console.warn('[EscapeRoom] 안전장치: 길을 막은 사람을 비켜 세웠어요'); wd.boxed = 0; blockers.forEach(function(e) { e.setThrough(true); }); }
            } else wd.boxed = 0;
        } else wd.boxed = 0;
        // (바) 지도 이벤트 실행기가 오래 붙잡혀 있음 (방탈출 맵의 이벤트는 내용이 비어 있어야 함)
        if ($gameMap.isEventRunning() && this.isRoomMap($gameMap.mapId())) {
            if (++wd.ev > 600) { console.warn('[EscapeRoom] 안전장치: 멈춘 지도 이벤트를 끝냈어요'); wd.ev = 0; $gameMap._interpreter.clear(); }
        } else wd.ev = 0;
    };
    var _v43_update = EscapeManager.update;
    EscapeManager.update = function(scene) {
        try { _v43_update.apply(this, arguments); }
        catch (e) {
            console.error('[EscapeRoom] 진행 오류 - 계속합니다', e);
            this._errCount = (this._errCount || 0) + 1;
            if (this._queue && this._queue.length && this._errCount % 3 === 0) this._queue.shift();
        }
        try { this.escWatchdog(); } catch (e2) { console.error(e2); }
    };

    // 지나갈 수 있는(through) 사람과 같은 칸에 겹쳐 서 있을 때도 Enter 로 말을 걸 수 있게
    var _v43_facing = Scene_Map.prototype.escFacingEvent;
    Scene_Map.prototype.escFacingEvent = function() {
        var f = _v43_facing.apply(this, arguments);
        if (f) return f;
        var p = $gamePlayer, list = $gameMap.eventsXy(p.x, p.y);
        for (var i = 0; i < list.length; i++) {
            if (list[i]._escHidden || list[i]._erased || !list[i].characterName()) continue;
            var h = EscapeManager.hotspotForEvent(list[i]);
            if (h && EscapeManager.checkCond(h.when) && list[i].isThrough && list[i].isThrough()) return { event: list[i], hotspot: h };
        }
        return null;
    };
    // 이리저리 걷는 사람(wander)은 기본으로 길을 막는 사람 (겹쳐 지나가지 않게). 꼭 필요하면 "through": true
    var _v43_addWalkers = EscapeManager.addWalkers;
    EscapeManager.addWalkers = function(defs) {
        toArray(defs).forEach(function(d) { if (d && d.wander && d.through === undefined) d.through = false; });
        return _v43_addWalkers.apply(this, arguments);
    };
    EscapeManager.escVersion = ESC_VERSION;


    //=========================================================================
    // v4.4  (The Cold War)
    //  1) 확대 그림(사료 카드 등)이 알아서 사라짐: 그림과 함께 나온 글(대사)이 끝나면 다음 단계에서 자동으로 닫힘
    //     계속 띄워 두려면 그 단계에 "keep": true. 미니게임 창이 열릴 때도 닫힘.
    //  2) 새 미니게임 (타이밍 없음 · 모두 마우스/터치/키보드):
    //     balance(저울 싣기) spot(그림에서 찾기 · 돋보기) diff(두 그림 다른 곳 찾기) paint(지도 색칠)
    //     words(단어 카드로 문장 만들기) seat(자리 배치) dock(조절 막대 맞추기) rounds(알맞은 번역 고르기)
    //  3) 화면 오른쪽 '온도계' 게이지: 데이터 "gauge": { "var": "temp", "label": "냉전 온도", "min": -50, "max": 10 }
    //     단계 { "setVar": { "temp": "-30" } } 로 값을 바꾸면 눈금이 천천히 움직임
    //  4) 후기 페이지: 엔딩 뒤 QR 카드 + [후기 남기기] [처음 화면으로] 단추가 있는 화면이 떠 있음 (저절로 넘어가지 않음)
    //     단추를 누르는 바로 그 순간 새 창으로 열어 팝업 차단을 피하고, 전체 화면이면 먼저 창 모드로 바꿈
    //=========================================================================
    ESC_VERSION = '4.4';

    // ---- 1) 확대 그림 자동 닫기 ---------------------------------------------------------------
    var _v44_ps = EscapeManager.processStep;
    EscapeManager.processStep = function(s) {
        if (typeof s === 'string') s = { text: s };
        if (s && typeof s === 'object') {
            var sc = this._scene, vis = sc && sc.escCloseupVisible && sc.escCloseupVisible();
            if (this._picAuto && vis && !s.picture && !s.hidePicture && !s.keep && !s.keepPicture && (this._picTexts || 0) >= 1) {
                this.hideCloseup(); this._picAuto = false;
            }
            if (s.game && vis) { this.hideCloseup(); this._picAuto = false; }
            if (s.picture) { this._picAuto = !(s.keep || s.keepPicture); this._picTexts = (s.text || s.question) ? 1 : 0; }
            else if (s.hidePicture) this._picAuto = false;
            else if (s.text || s.question || s.choice) this._picTexts = (this._picTexts || 0) + 1;
        }
        return _v44_ps.call(this, s);
    };

    // ---- 2) 새 미니게임 -----------------------------------------------------------------------
    var _v44_setup = Window_EscGame.prototype.setup;
    Window_EscGame.prototype.setup = function(def) {
        var i, d = def;
        switch (String(def.type)) {
        case 'balance': this._fb = toArray(d.items).map(function() { return [0, 0]; }); this._col = 0; break;
        case 'spot': case 'diff':
            this._found = toArray(d.spots).map(function() { return false; }); this._cx = 0.5; this._cy = 0.5; this._miss = 0; this._blink = -1;
            this._img = ImageManager.loadPicture(String(d.image || ''));
            this._img2 = d.image2 ? ImageManager.loadPicture(String(d.image2)) : null;
            break;
        case 'paint': this._paint = toArray(d.marks).map(function() { return -1; });
            this._img = d.image ? ImageManager.loadPicture(String(d.image)) : null; break;
        case 'words': this._line = []; break;
        case 'seat': this._seat = toArray(d.seats).map(function() { return -1; }); this._hold = -1; this._pc = 0; this._focus = 0; break;
        case 'dock': var st = d.start || {}; this._dv = [Number(st.x !== undefined ? st.x : 15), Number(st.y !== undefined ? st.y : 80), Number(d.speedStart || 0)]; this._row = 0; break;
        case 'rounds': this._round = 0; this._rfail = 0; this._picked = -1; this._after = 0; break;
        }
        _v44_setup.apply(this, arguments);
    };
    var _v44_isSolved = Window_EscGame.prototype.isSolved;
    Window_EscGame.prototype.isSolved = function() {
        var d = this._def, ans = toArray(d.answer), i;
        switch (this._type) {
        case 'balance':
            var f = this.balSide(0), b = this.balSide(1);
            return f + b === Number(d.target) && Math.abs(f - b) <= Number(d.tol || 0);
        case 'paint':
            for (i = 0; i < this._paint.length; i++) if (this._paint[i] !== Number(ans[i]) - 1) return false;
            return true;
        case 'words':
            if (this._line.length !== ans.length) return false;
            for (i = 0; i < ans.length; i++) if (this._line[i] !== Number(ans[i]) - 1) return false;
            return true;
        case 'seat':
            for (i = 0; i < this._seat.length; i++) if (this._seat[i] !== Number(ans[i]) - 1) return false;
            return true;
        case 'dock':
            var t = d.target || {};
            return Math.abs(this._dv[0] - Number(t.x)) <= Number(d.tol || 4) && Math.abs(this._dv[1] - Number(t.y)) <= Number(d.tol || 4) &&
                   (d.speedAnswer === undefined || this._dv[2] === Number(d.speedAnswer) - 1);
        case 'spot': case 'diff': return this._found.every(function(v) { return v; });
        }
        return _v44_isSolved.apply(this, arguments);
    };
    var _v44_showAnswer = Window_EscGame.prototype.showAnswer;
    Window_EscGame.prototype.showAnswer = function() {
        var d = this._def, ans = toArray(d.answer);
        switch (this._type) {
        case 'balance': if (d.solution) this._fb = toArray(d.solution).map(function(p) { return [Number(p[0]), Number(p[1])]; }); return;
        case 'paint': this._paint = ans.map(function(v) { return Number(v) - 1; }); return;
        case 'words': this._line = ans.map(function(v) { return Number(v) - 1; }); return;
        case 'seat': this._seat = ans.map(function(v) { return Number(v) - 1; }); return;
        case 'dock': var t = d.target || {}; this._dv = [Number(t.x), Number(t.y), d.speedAnswer !== undefined ? Number(d.speedAnswer) - 1 : this._dv[2]]; return;
        case 'spot': case 'diff': this._found = this._found.map(function() { return true; }); return;
        }
        return _v44_showAnswer.apply(this, arguments);
    };
    // 그림이 아직 안 불러졌으면 다시 그리기
    var _v44_drawButtons = Window_EscGame.prototype.drawButtons;
    Window_EscGame.prototype.drawButtons = function(okLabel, focused) {
        if (okLabel && !String(okLabel).replace(/[\s\u3000]/g, '')) {     // 확인 단추가 필요 없는 게임: '나중에'만
            var c = this.contents, b = this.btnRects();
            roundRect(c, b.later.x, b.later.y, b.later.w, b.later.h, 10, 'rgba(255,255,255,0.15)', 'rgba(255,255,255,0.4)', 1);
            c.fontSize = 18; c.textColor = '#ffffff'; c.drawText('나중에 (Esc)', b.later.x, b.later.y + 2, b.later.w, 34, 'center');
            this.resetTextColor(); return;
        }
        return _v44_drawButtons.apply(this, arguments);
    };
    var V44_TYPES = { balance: 1, spot: 1, diff: 1, paint: 1, words: 1, seat: 1, dock: 1, rounds: 1 };
    var _v44_refresh = Window_EscGame.prototype.refresh;
    Window_EscGame.prototype.refresh = function() {
        var flat = this.contents && V44_TYPES[this._type];
        if (flat) this.contents.outlineWidth = 0;
        _v44_refresh.apply(this, arguments);
        if (this.contents) this.contents.outlineWidth = 4;
        var self = this;
        [this._img, this._img2].forEach(function(bm) {
            if (bm && !bm.isReady() && !bm._escHooked && bm.addLoadListener) { bm._escHooked = true; bm.addLoadListener(function() { if (self._def) self.refresh(); }); }
        });
    };
    function escFit(c, text, maxW, size, min) {
        var fs = size; c.fontSize = fs;
        while (fs > (min || 11) && c.measureTextWidth(text) > maxW) { fs--; c.fontSize = fs; }
        return fs;
    }
    function escBox(c, r, fill, stroke, lw) { roundRect(c, r.x, r.y, r.w, r.h, 8, fill, stroke, lw || 1); }
    function escCardText(c, r, text, col, size) {
        c.textColor = col || '#2a1a06';
        if (String(text).indexOf('\n') >= 0) {
            var parts = String(text).split('\n').slice(0, 2), lh2 = Math.min(20, (r.h - 4) / 2);
            for (var q = 0; q < parts.length; q++) { escFit(c, parts[q], r.w - 12, q === 0 ? (size || 16) : (size || 16) - 3, 10); c.drawText(parts[q], r.x + 6, r.y + (r.h - parts.length * lh2) / 2 + q * lh2, r.w - 12, lh2, 'center'); }
            return;
        }
        var lines = escWrap(c, text, r.w - 14);
        if (lines.length > 1) { escFit(c, text, (r.w - 14) * 2, size || 16, 12); lines = escWrap(c, text, r.w - 14); }
        else escFit(c, text, r.w - 14, size || 16, 11);
        var n = Math.min(2, lines.length), lh = Math.min(22, (r.h - 4) / n);
        for (var k = 0; k < n; k++) c.drawText(lines[k], r.x + 7, r.y + (r.h - n * lh) / 2 + k * lh, r.w - 14, lh, 'center');
    }
    Window_EscGame.prototype.footer = function(help) {
        var c = this.contents, w = this.contentsWidth();
        c.fontSize = 15; this.changeTextColor('#d8ccb0');
        c.drawText(help, 0, this.contentsHeight() - 96, w, 22, 'center');
        this.drawMsg(this.contentsHeight() - 74);
    };
    Window_EscGame.prototype.areaRect = function(top) {
        var w = this.contentsWidth(), h = this.contentsHeight();
        return { x: 12, y: top, w: w - 24, h: h - top - 104 };
    };

    // ----- balance: 저울에 맞춰 싣기 --------------------------------------------------------------
    //  { type:'balance', title, help, items:[{label:'석탄 자루', weight:2, max:4}], target:10, unit:'톤', sides:['앞칸','뒤칸'], tol:0, solution:[[1,1],...] }
    Window_EscGame.prototype.balSide = function(s) {
        var items = toArray(this._def.items), t = 0;
        for (var i = 0; i < items.length; i++) t += this._fb[i][s] * Number(items[i].weight);
        return t;
    };
    Window_EscGame.prototype.balRects = function() {
        var w = this.contentsWidth(), items = toArray(this._def.items), y0 = 196, lh = Math.min(48, Math.floor((this.contentsHeight() - y0 - 110) / items.length)), rs = [];
        for (var i = 0; i < items.length; i++) rs.push({ name: { x: 12, y: y0 + i * lh, w: w * 0.36 - 12, h: lh - 6 },
            c: [{ x: w * 0.38, y: y0 + i * lh, w: w * 0.29, h: lh - 6 }, { x: w * 0.69, y: y0 + i * lh, w: w * 0.29 - 12, h: lh - 6 }] });
        return rs;
    };
    Window_EscGame.prototype.balAdd = function(i, s, dlt) {
        var it = toArray(this._def.items)[i], mx = Number(it.max || 5);
        var v = this._fb[i][s] + dlt;
        if (v < 0) v = 0; if (v > mx) v = mx;
        if (v !== this._fb[i][s]) { this._fb[i][s] = v; SoundManager.playCursor(); } else SoundManager.playBuzzer();
    };
    Window_EscGame.prototype.update_balance = function() {
        var n = this._fb.length;
        if (Input.isRepeated('down')) { this._cur = (this._cur + 1) % (n + 1); SoundManager.playCursor(); }
        if (Input.isRepeated('up')) { this._cur = (this._cur + n) % (n + 1); SoundManager.playCursor(); }
        if (Input.isRepeated('left') && this._cur < n) { this._col = 0; SoundManager.playCursor(); }
        if (Input.isRepeated('right') && this._cur < n) { this._col = 1; SoundManager.playCursor(); }
        if (Input.isTriggered('ok')) {
            if (this._cur === n) { SoundManager.playOk(); this.submit(); }
            else { var it = toArray(this._def.items)[this._cur], mx = Number(it.max || 5);
                   if (this._fb[this._cur][this._col] >= mx) { this._fb[this._cur][this._col] = 0; SoundManager.playCancel(); } else this.balAdd(this._cur, this._col, 1); }
        }
        if (Input.isTriggered('pagedown') && this._cur < n) this.balAdd(this._cur, this._col, -1);
        if (TouchInput.isTriggered()) {
            var p = this.local(), rs = this.balRects();
            for (var i = 0; i < rs.length; i++) for (var s = 0; s < 2; s++) {
                var r = rs[i].c[s];
                if (this.inside(r, p)) { this._cur = i; this._col = s; this.balAdd(i, s, p.x < r.x + r.w / 2 ? -1 : 1); return; }
            }
            this.touchButtons();
        }
    };
    Window_EscGame.prototype.draw_balance = function() {
        var c = this.contents, w = this.contentsWidth(), d = this._def, items = toArray(d.items), rs = this.balRects(), i, s;
        var sides = toArray(d.sides).length ? toArray(d.sides) : ['앞칸', '뒤칸'], unit = d.unit || '';
        this.drawHeader();
        // 저울 (기울기)
        var f = this.balSide(0), b = this.balSide(1), tot = f + b, cx = w / 2, cy = 120;
        var ang = Math.max(-0.28, Math.min(0.28, (b - f) * 0.05));
        var ctx = ctxOf(c);
        ctx.save(); ctx.translate(cx, cy); ctx.fillStyle = '#6a5030'; ctx.beginPath(); ctx.moveTo(-14, 52); ctx.lineTo(14, 52); ctx.lineTo(0, 4); ctx.fill();
        ctx.rotate(ang); ctx.fillStyle = '#c8a060'; ctx.fillRect(-230, -4, 460, 8);
        ctx.fillStyle = '#e8dcc0'; ctx.fillRect(-250, -26, 70, 22); ctx.fillRect(180, -26, 70, 22);
        ctx.fillStyle = '#2a1a06'; ctx.font = '15px GameFont'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
        ctx.fillText(f + unit, -215, -15); ctx.fillText(b + unit, 215, -15);
        ctx.restore(); setDirty(c);
        c.fontSize = 16; c.textColor = '#ffe9b0';
        c.drawText(escSub(sides[0]), cx - 300, cy + 18, 140, 22, 'center'); c.drawText(escSub(sides[1]), cx + 160, cy + 18, 140, 22, 'center');
        c.fontSize = 18; c.textColor = tot === Number(d.target) ? '#9dffb0' : '#ffffff';
        c.drawText('실은 짐: ' + tot + ' / ' + d.target + unit + (f === b ? '   · 수평!' : '   · ' + (f > b ? sides[0] : sides[1]) + '이 무거워요'), 0, cy + 44, w, 24, 'center');
        for (i = 0; i < items.length; i++) {
            var r = rs[i], it = items[i];
            escBox(c, r.name, 'rgba(255,255,255,0.08)', 'rgba(255,255,255,0.2)');
            c.textColor = '#ffffff'; escFit(c, escSub(it.label) + ' (' + it.weight + unit + ')', r.name.w - 16, 16, 11);
            c.drawText(escSub(it.label) + ' (' + it.weight + unit + ')', r.name.x + 8, r.name.y + (r.name.h - 24) / 2, r.name.w - 16, 24, 'left');
            for (s = 0; s < 2; s++) {
                var q = r.c[s], cur = this._cur === i && this._col === s && !this._end;
                escBox(c, q, cur ? 'rgba(255,230,160,0.98)' : 'rgba(246,236,206,0.92)', cur ? '#ffffff' : '#8a6a40', cur ? 3 : 1);
                c.fontSize = 18; c.textColor = '#2a1a06';
                c.drawText('－', q.x + 6, q.y + (q.h - 26) / 2, 30, 26, 'center'); c.drawText('＋', q.x + q.w - 36, q.y + (q.h - 26) / 2, 30, 26, 'center');
                c.drawText(String(this._fb[i][s]), q.x, q.y + (q.h - 26) / 2, q.w, 26, 'center');
            }
        }
        this.footer('↑↓ 짐 고르기 · ← → ' + sides[0] + '/' + sides[1] + ' · Enter 하나 더(가득 차면 0) · W 하나 빼기 · 클릭: 왼쪽 빼기 / 오른쪽 더하기');
        this.drawButtons('이대로 싣기', this._cur === items.length);
    };

    // ----- spot / diff: 그림에서 찾기 ------------------------------------------------------------
    //  { type:'spot', image:'cu_u2', spots:[{x:120,y:80,r:30,label:'발사대'}], hint, zoom:2.2 }   (x, y, r 는 그림 픽셀)
    //  { type:'diff', image:'cu_a', image2:'cu_b', spots:[...] }   두 그림을 나란히, 어느 쪽을 눌러도 됨
    Window_EscGame.prototype.spotFrames = function() {
        var a = this.areaRect(this._type === 'diff' ? 86 : 80), img = this._img, iw = img && img.width || 600, ih = img && img.height || 400;
        if (this._type === 'diff') {
            var half = (a.w - 16) / 2, sc = Math.min(half / iw, a.h / ih), fw = iw * sc, fh = ih * sc;
            return [{ x: a.x + (half - fw) / 2, y: a.y + (a.h - fh) / 2, w: fw, h: fh, s: sc, bm: this._img },
                    { x: a.x + half + 16 + (half - fw) / 2, y: a.y + (a.h - fh) / 2, w: fw, h: fh, s: sc, bm: this._img2 }];
        }
        var lens = Math.min(200, a.w * 0.3), aw = a.w - lens - 16, sc2 = Math.min(aw / iw, a.h / ih);
        return [{ x: a.x + (aw - iw * sc2) / 2, y: a.y + (a.h - ih * sc2) / 2, w: iw * sc2, h: ih * sc2, s: sc2, bm: this._img, lens: { x: a.x + aw + 16, y: a.y, w: lens, h: lens } }];
    };
    // 찾을 곳 좌표: 보통은 그림 픽셀, "unit": "ratio" 이면 그림 크기에 대한 비율(0~1 · r은 너비 비율) → 다른 크기의 사진으로 바꿔도 맞음
    Window_EscGame.prototype.spotPx = function(sp) {
        if (this._def.unit !== 'ratio') return { x: Number(sp.x), y: Number(sp.y), r: Number(sp.r || 30) };
        var img = this._img, iw = img && img.width > 1 ? img.width : 600, ih = img && img.height > 1 ? img.height : 400;
        return { x: Number(sp.x) * iw, y: Number(sp.y) * ih, r: Number(sp.r || 0.08) * iw };
    };
    Window_EscGame.prototype.spotCheck = function(ix, iy) {
        var spots = toArray(this._def.spots), best = -1;
        for (var i = 0; i < spots.length; i++) {
            var q = this.spotPx(spots[i]), dx = ix - q.x, dy = iy - q.y, r = q.r;
            if (dx * dx + dy * dy <= r * r) { best = i; if (!this._found[i]) break; }
        }
        if (best >= 0 && !this._found[best]) {
            this._found[best] = true; SoundManager.playOk(); playSafeSe(SE_ITEM, 80, 120);
            var sp = spots[best];
            this.say((sp.label ? '「' + escSub(sp.label) + '」 ' : '') + escSub(sp.text || '찾았다!'), '#9dffb0');
            this._blink = -1;
            if (this.isSolved()) this.finish(true);
        } else if (best >= 0) { this.say('이미 찾은 곳이에요.', '#ffe9a8'); }
        else {
            this._miss++; SoundManager.playBuzzer();
            var d = this._def, give = Number(d.revealAfter || 7);
            if (this._miss >= give) { this.showAnswer(); this.finish(true, true); return; }
            if (this._miss >= Number(d.hintAfter || 3)) {
                for (var k = 0; k < this._found.length; k++) if (!this._found[k]) { this._blink = k; break; }
                this.say('힌트: ' + escSub(d.hint || '깜빡이는 동그라미 근처를 살펴봐요.'), '#ffe9a8');
            } else this.say(escSub(d.missMsg || '여기엔 없는 것 같아요. 다른 곳을 살펴봐요.'), '#ff9a8a');
        }
    };
    Window_EscGame.prototype.update_spot = function() {
        var fr = this.spotFrames(), f0 = fr[0], sp = Input.isPressed('shift') ? 0.02 : 0.008;
        if (Input.isPressed('left')) this._cx = Math.max(0, this._cx - sp);
        if (Input.isPressed('right')) this._cx = Math.min(1, this._cx + sp);
        if (Input.isPressed('up')) this._cy = Math.max(0, this._cy - sp);
        if (Input.isPressed('down')) this._cy = Math.min(1, this._cy + sp);
        if (TouchInput.isMoved && TouchInput.isMoved() || TouchInput.isPressed()) {
            var mp = this.local();
            for (var j = 0; j < fr.length; j++) if (this.inside(fr[j], mp)) { this._cx = (mp.x - fr[j].x) / fr[j].w; this._cy = (mp.y - fr[j].y) / fr[j].h; }
        }
        if (Input.isTriggered('ok')) { this.spotCheck(this._cx * f0.w / f0.s, this._cy * f0.h / f0.s); return; }
        if (TouchInput.isTriggered()) {
            var p = this.local();
            for (var i = 0; i < fr.length; i++) if (this.inside(fr[i], p)) { this.spotCheck((p.x - fr[i].x) / fr[i].s, (p.y - fr[i].y) / fr[i].s); return; }
            if (this.touchButtons()) return;
        }
    };
    Window_EscGame.prototype.update_diff = Window_EscGame.prototype.update_spot;
    Window_EscGame.prototype.draw_spot = function() {
        var c = this.contents, d = this._def, fr = this.spotFrames(), spots = toArray(d.spots), self = this, i;
        this.drawHeader();
        fr.forEach(function(f) {
            c.fillRect(f.x - 3, f.y - 3, f.w + 6, f.h + 6, '#c8a060');
            if (f.bm && f.bm.isReady()) c.blt(f.bm, 0, 0, f.bm.width, f.bm.height, f.x, f.y, f.w, f.h);
            else { c.fillRect(f.x, f.y, f.w, f.h, '#333'); c.fontSize = 16; c.textColor = '#fff'; c.drawText('그림을 불러오는 중…', f.x, f.y + f.h / 2 - 12, f.w, 24, 'center'); }
        });
        var ctx = ctxOf(c);
        fr.forEach(function(f) {
            for (i = 0; i < spots.length; i++) {
                var q = self.spotPx(spots[i]), x = f.x + q.x * f.s, y = f.y + q.y * f.s, r = q.r * f.s;
                if (self._found[i]) { ctx.strokeStyle = '#ff3a2a'; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(x, y, r, 0, Math.PI * 2); ctx.stroke(); }
                else if (self._blink === i && Math.floor(self._t / 15) % 2 === 0) { ctx.strokeStyle = 'rgba(255,230,120,0.9)'; ctx.lineWidth = 2; ctx.setLineDash && ctx.setLineDash([6, 5]);
                    ctx.beginPath(); ctx.arc(x, y, r * 1.8, 0, Math.PI * 2); ctx.stroke(); ctx.setLineDash && ctx.setLineDash([]); }
            }
            // 조준 (돋보기 자리)
            var mx = f.x + self._cx * f.w, my = f.y + self._cy * f.h;
            ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 2; ctx.beginPath(); ctx.arc(mx, my, 16, 0, Math.PI * 2); ctx.moveTo(mx - 24, my); ctx.lineTo(mx - 8, my);
            ctx.moveTo(mx + 8, my); ctx.lineTo(mx + 24, my); ctx.moveTo(mx, my - 24); ctx.lineTo(mx, my - 8); ctx.moveTo(mx, my + 8); ctx.lineTo(mx, my + 24); ctx.stroke();
        });
        setDirty(c);
        var f0 = fr[0];
        if (f0.lens && f0.bm && f0.bm.isReady()) {     // 돋보기 창
            var L = f0.lens, z = Number(d.zoom || 2.4), src = L.w / (f0.s * z);
            var sx = Math.max(0, Math.min(f0.bm.width - src, this._cx * f0.bm.width - src / 2)), sy = Math.max(0, Math.min(f0.bm.height - src, this._cy * f0.bm.height - src / 2));
            c.fillRect(L.x - 4, L.y - 4, L.w + 8, L.h + 8, '#c8a060');
            c.blt(f0.bm, sx, sy, src, src, L.x, L.y, L.w, L.h);
            c.fontSize = 15; c.textColor = '#ffe9b0'; c.drawText('돋보기', L.x, L.y + L.h + 6, L.w, 20, 'center');
            var cnt = this._found.filter(function(v) { return v; }).length;
            c.fontSize = 18; c.textColor = '#ffffff'; c.drawText('찾은 것: ' + cnt + ' / ' + spots.length, L.x, L.y + L.h + 34, L.w, 24, 'center');
            c.fontSize = 14; c.textColor = '#d8ccb0';
            var yy = L.y + L.h + 64;
            for (i = 0; i < spots.length; i++) if (this._found[i] && spots[i].label) { c.drawText('✓ ' + escSub(spots[i].label), L.x, yy, L.w, 20, 'left'); yy += 20; }
        } else {
            var cnt2 = this._found.filter(function(v) { return v; }).length;
            c.fontSize = 17; c.textColor = '#ffffff'; c.drawText('찾은 곳: ' + cnt2 + ' / ' + spots.length, 0, 56 + 6, this.contentsWidth() - 14, 22, 'right');
        }
        this.footer(this._type === 'diff' ? '다른 곳을 클릭(톡) · 또는 방향키로 조준하고 Enter' : '그림 위를 움직이면 돋보기로 크게 보여요 · 찾으면 클릭(톡) 또는 Enter · 방향키로도 조준');
        this.drawButtons('　', false);
    };
    Window_EscGame.prototype.draw_diff = Window_EscGame.prototype.draw_spot;

    // ----- paint: 지도 색칠 -----------------------------------------------------------------------
    //  { type:'paint', image:'cu_europe61', marks:[{x:120,y:80,label:'1'}], colors:[{name:'NATO', col:'#3a6ad8'}, ...], answer:[1,2,...], legend:['1 영국', ...] }
    Window_EscGame.prototype.paintFrame = function() {
        var a = this.areaRect(80), img = this._img, iw = img && img.width || 500, ih = img && img.height || 400, side = Math.min(230, a.w * 0.32);
        var aw = a.w - side - 12, s = Math.min(aw / iw, a.h / ih);
        return { x: a.x + (aw - iw * s) / 2, y: a.y + (a.h - ih * s) / 2, w: iw * s, h: ih * s, s: s, side: { x: a.x + aw + 12, y: a.y, w: side, h: a.h } };
    };
    Window_EscGame.prototype.paintAt = function(i) {
        var f = this.paintFrame(), m = toArray(this._def.marks)[i];
        return { x: f.x + Number(m.x) * f.s - 15, y: f.y + Number(m.y) * f.s - 15, w: 30, h: 30 };
    };
    Window_EscGame.prototype.paintCycle = function(i, dir) {
        var nc = toArray(this._def.colors).length, v = this._paint[i] + (dir || 1);
        if (v >= nc) v = 0; if (v < 0) v = nc - 1;
        this._paint[i] = v; SoundManager.playCursor();
    };
    Window_EscGame.prototype.update_paint = function() {
        var n = this._paint.length;
        if (Input.isRepeated('down') || Input.isRepeated('right') && this._cur === n) { this._cur = (this._cur + 1) % (n + 1); SoundManager.playCursor(); }
        else if (Input.isRepeated('up')) { this._cur = (this._cur + n) % (n + 1); SoundManager.playCursor(); }
        else if (this._cur < n && Input.isRepeated('right')) this.paintCycle(this._cur, 1);
        else if (this._cur < n && Input.isRepeated('left')) this.paintCycle(this._cur, -1);
        if (Input.isTriggered('ok')) { if (this._cur === n) { SoundManager.playOk(); this.submit(); } else this.paintCycle(this._cur, 1); }
        if (TouchInput.isTriggered()) {
            var p = this.local();
            for (var i = 0; i < n; i++) { var r = this.paintAt(i); r.x -= 6; r.y -= 6; r.w += 12; r.h += 12; if (this.inside(r, p)) { this._cur = i; this.paintCycle(i, 1); return; } }
            this.touchButtons();
        }
    };
    Window_EscGame.prototype.draw_paint = function() {
        var c = this.contents, d = this._def, f = this.paintFrame(), marks = toArray(d.marks), cols = toArray(d.colors), i;
        this.drawHeader();
        c.fillRect(f.x - 3, f.y - 3, f.w + 6, f.h + 6, '#c8a060');
        if (this._img && this._img.isReady()) c.blt(this._img, 0, 0, this._img.width, this._img.height, f.x, f.y, f.w, f.h);
        else c.fillRect(f.x, f.y, f.w, f.h, '#d8d0b8');
        var ctx = ctxOf(c);
        for (i = 0; i < marks.length; i++) {
            var r = this.paintAt(i), v = this._paint[i], cur = this._cur === i && !this._end;
            ctx.fillStyle = v >= 0 ? cols[v].col : 'rgba(255,255,255,0.92)'; ctx.strokeStyle = cur ? '#ffffff' : '#2a1a06'; ctx.lineWidth = cur ? 4 : 2;
            ctx.beginPath(); ctx.arc(r.x + 15, r.y + 15, cur ? 17 : 15, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
            ctx.fillStyle = v >= 0 ? '#ffffff' : '#2a1a06'; ctx.font = 'bold 15px GameFont'; ctx.textAlign = 'center'; ctx.textBaseline = 'middle';
            ctx.fillText(String(marks[i].label || (i + 1)), r.x + 15, r.y + 16);
        }
        setDirty(c);
        var S = f.side, y = S.y;
        c.fontSize = 16; c.textColor = '#ffe9b0'; c.drawText('색 (누를 때마다 바뀜)', S.x, y, S.w, 22, 'left'); y += 26;
        for (i = 0; i < cols.length; i++) { c.fillRect(S.x, y + 3, 22, 18, cols[i].col); c.fontSize = 15; c.textColor = '#ffffff'; c.drawText(escSub(cols[i].name), S.x + 30, y, S.w - 30, 24, 'left'); y += 26; }
        y += 8; c.fontSize = 16; c.textColor = '#ffe9b0'; c.drawText('나라', S.x, y, S.w, 22, 'left'); y += 24;
        var leg = toArray(d.legend), half = Math.ceil(leg.length / 2), cw2 = leg.length > 7 ? S.w / 2 : S.w;
        leg.forEach(function(t, k) {
            var col2 = leg.length > 7 && k >= half ? 1 : 0, row = leg.length > 7 ? (k % half) : k;
            c.fontSize = 14; c.textColor = '#ffffff'; escFit(c, escSub(t), cw2 - 4, 14, 10); c.drawText(escSub(t), S.x + col2 * cw2, y + row * 20, cw2 - 4, 20, 'left');
        });
        this.footer('↑↓ 나라 고르기 · ← → / Enter 색 바꾸기 · 동그라미를 클릭(톡)해도 돼요 · 다 칠하면 [확인]');
        this.drawButtons('확인', this._cur === marks.length);
    };

    // ----- words: 단어 카드로 문장 만들기 ----------------------------------------------------------
    //  { type:'words', title, help, cards:['미국은', ...], answer:[1,4,2,...], note:'뜻이 두 가지인 낱말은 오해를 불러요' }
    Window_EscGame.prototype.wordRects = function() {
        var w = this.contentsWidth(), cards = toArray(this._def.cards), c = this.contents, out = { line: [], bank: [], clear: null }, x = 22, y = 100, i, cw;
        c.fontSize = 17;
        for (i = 0; i < this._line.length; i++) {
            cw = Math.min(w - 44, c.measureTextWidth(escSub(cards[this._line[i]])) + 26);
            if (x + cw > w - 22) { x = 22; y += 44; }
            out.line.push({ x: x, y: y, w: cw, h: 36 }); x += cw + 6;
        }
        out.lineBox = { x: 12, y: 92, w: w - 24, h: Math.max(100, y + 44 - 92 + 8) };
        x = 22; y = out.lineBox.y + out.lineBox.h + 30;
        for (i = 0; i < cards.length; i++) {
            cw = Math.min(w - 44, c.measureTextWidth(escSub(cards[i])) + 26);
            if (x + cw > w - 22) { x = 22; y += 44; }
            out.bank.push({ x: x, y: y, w: cw, h: 36 }); x += cw + 6;
        }
        out.clear = { x: w - 162, y: out.lineBox.y + out.lineBox.h + 2, w: 140, h: 26 };
        return out;
    };
    Window_EscGame.prototype.update_words = function() {
        var cards = toArray(this._def.cards), n = cards.length, used = this._line;
        if (Input.isRepeated('right') || Input.isRepeated('down')) { this._cur = (this._cur + 1) % (n + 2); SoundManager.playCursor(); }
        if (Input.isRepeated('left') || Input.isRepeated('up')) { this._cur = (this._cur + n + 1) % (n + 2); SoundManager.playCursor(); }
        if (Input.isTriggered('pagedown') && used.length) { used.pop(); SoundManager.playCancel(); }
        if (Input.isTriggered('ok')) {
            if (this._cur === n + 1) { SoundManager.playOk(); this.submit(); }
            else if (this._cur === n) { if (used.length) { used.pop(); SoundManager.playCancel(); } }
            else if (used.indexOf(this._cur) < 0) { used.push(this._cur); SoundManager.playOk(); }
            else SoundManager.playBuzzer();
        }
        if (TouchInput.isTriggered()) {
            var p = this.local(), R = this.wordRects(), i;
            for (i = 0; i < R.line.length; i++) if (this.inside(R.line[i], p)) { used.splice(i, 1); SoundManager.playCancel(); return; }
            for (i = 0; i < R.bank.length; i++) if (this.inside(R.bank[i], p)) { this._cur = i; if (used.indexOf(i) < 0) { used.push(i); SoundManager.playOk(); } return; }
            if (this.inside(R.clear, p)) { if (used.length) { used.pop(); SoundManager.playCancel(); } return; }
            this.touchButtons();
        }
    };
    Window_EscGame.prototype.draw_words = function() {
        var c = this.contents, w = this.contentsWidth(), d = this._def, cards = toArray(d.cards), R = this.wordRects(), i;
        this.drawHeader();
        escBox(c, R.lineBox, 'rgba(0,0,0,0.35)', 'rgba(200,160,96,0.8)', 2);
        if (!this._line.length) { c.fontSize = 16; c.textColor = '#a89c84'; c.drawText('여기에 문장이 만들어져요', 0, R.lineBox.y + R.lineBox.h / 2 - 12, w, 24, 'center'); }
        for (i = 0; i < this._line.length; i++) { escBox(c, R.line[i], 'rgba(255,240,190,0.98)', '#c8a060', 2); c.fontSize = 17; c.textColor = '#2a1a06'; c.drawText(escSub(cards[this._line[i]]), R.line[i].x, R.line[i].y + 6, R.line[i].w, 24, 'center'); }
        var cur = this._cur;
        escBox(c, R.clear, cur === cards.length ? 'rgba(255,200,120,0.9)' : 'rgba(255,255,255,0.12)', cur === cards.length ? '#ffffff' : 'rgba(255,255,255,0.4)', cur === cards.length ? 3 : 1);
        c.fontSize = 14; c.textColor = '#ffffff'; c.drawText('← 마지막 카드 빼기', R.clear.x, R.clear.y + 2, R.clear.w, 22, 'center');
        if (d.note) { c.fontSize = 14; c.textColor = '#ffcf9a'; c.drawText(escSub(d.note), 16, R.clear.y + 2, w - 186, 22, 'left'); }
        for (i = 0; i < cards.length; i++) {
            var r = R.bank[i], usedI = this._line.indexOf(i) >= 0, on = cur === i && !this._end;
            escBox(c, r, usedI ? 'rgba(255,255,255,0.08)' : 'rgba(246,236,206,0.95)', on ? '#ffffff' : (usedI ? 'rgba(255,255,255,0.2)' : '#8a6a40'), on ? 3 : 1);
            c.fontSize = 17; c.textColor = usedI ? '#7a7060' : '#2a1a06'; c.drawText(escSub(cards[i]), r.x, r.y + 6, r.w, 24, 'center');
        }
        this.footer('카드를 순서대로 클릭(톡)하거나 ← → 로 고르고 Enter · 위 문장의 카드를 누르면 빠져요 · W: 마지막 카드 빼기');
        this.drawButtons('이 문장 보내기', cur === cards.length + 1);
    };

    // ----- seat: 자리 배치 -------------------------------------------------------------------------
    //  { type:'seat', title, help, people:['닉슨',...], seats:[{x:0.2,y:0.3,label:'1'}] (탁자 그림 안 비율), clues:['…'], answer:[사람 번호 per 자리] , table:'rect'|'round' }
    Window_EscGame.prototype.seatLayout = function() {
        var w = this.contentsWidth(), a = this.areaRect(84), pw = Math.min(176, w * 0.23), cw = Math.min(196, w * 0.26);
        var tb = { x: a.x + pw + 12, y: a.y, w: a.w - pw - cw - 24, h: a.h };
        var people = toArray(this._def.people), ph = Math.min(46, (a.h - 30) / Math.max(1, people.length)), P = [];
        for (var i = 0; i < people.length; i++) P.push({ x: a.x, y: a.y + 26 + i * ph, w: pw, h: ph - 5 });
        if (this._def.image && this._img && this._img.isReady()) {     // v4.6: 지도 그림 위 자리 (그림 비율에 맞춤)
            var im_ = this._img, sc_ = Math.min(tb.w / im_.width, tb.h / im_.height);
            tb = { x: tb.x + (tb.w - im_.width * sc_) / 2, y: tb.y + (tb.h - im_.height * sc_) / 2, w: im_.width * sc_, h: im_.height * sc_ };
        }
        var bw = Math.min(this._def.image ? 96 : 100, tb.w / 3 - 12), S = toArray(this._def.seats).map(function(s) { return { x: tb.x + Number(s.x) * tb.w - bw / 2, y: tb.y + Number(s.y) * tb.h - 17, w: bw, h: 34 }; });
        if (!this._def.image) S = toArray(this._def.seats).map(function(s) { return { x: tb.x + Number(s.x) * tb.w - bw / 2, y: tb.y + Number(s.y) * tb.h - 22, w: bw, h: 44 }; });
        return { table: tb, people: P, seats: S, clue: { x: a.x + a.w - cw, y: a.y, w: cw, h: a.h } };
    };
    Window_EscGame.prototype.seatPut = function(si, pi) {
        for (var k = 0; k < this._seat.length; k++) if (this._seat[k] === pi) this._seat[k] = -1;
        this._seat[si] = pi; SoundManager.playOk();
    };
    Window_EscGame.prototype.update_seat = function() {
        var ns = this._seat.length, np = toArray(this._def.people).length;
        if (Input.isRepeated('down')) { this._cur = (this._cur + 1) % (ns + 1); SoundManager.playCursor(); }
        if (Input.isRepeated('up')) { this._cur = (this._cur + ns) % (ns + 1); SoundManager.playCursor(); }
        if (this._cur < ns && (Input.isRepeated('right') || Input.isRepeated('left'))) {
            var dir = Input.isRepeated('right') ? 1 : -1, v = this._seat[this._cur];
            for (var t = 0; t < np + 1; t++) {
                v += dir; if (v >= np) v = -1; if (v < -1) v = np - 1;
                if (v === -1 || this._seat.indexOf(v) < 0) break;
            }
            this._seat[this._cur] = v; SoundManager.playCursor();
        }
        if (Input.isTriggered('ok') && this._cur === ns) { SoundManager.playOk(); this.submit(); }
        else if (Input.isTriggered('ok') && this._cur < ns) { this._cur = (this._cur + 1) % (ns + 1); SoundManager.playCursor(); }
        if (TouchInput.isTriggered()) {
            var p = this.local(), L = this.seatLayout(), i;
            for (i = 0; i < L.people.length; i++) if (this.inside(L.people[i], p)) { this._hold = this._hold === i ? -1 : i; SoundManager.playCursor(); return; }
            for (i = 0; i < L.seats.length; i++) if (this.inside(L.seats[i], p)) {
                this._cur = i;
                if (this._hold >= 0) { this.seatPut(i, this._hold); this._hold = -1; }
                else if (this._seat[i] >= 0) { this._seat[i] = -1; SoundManager.playCancel(); }
                return;
            }
            this.touchButtons();
        }
    };
    Window_EscGame.prototype.draw_seat = function() {
        var c = this.contents, d = this._def, L = this.seatLayout(), people = toArray(d.people), i, tb = L.table;
        this.drawHeader();
        var ctx = ctxOf(c);
        ctx.fillStyle = '#5a3a20'; ctx.strokeStyle = '#c8a060'; ctx.lineWidth = 3;
        if (d.table === 'round') { ctx.beginPath(); ctx.ellipse ? ctx.ellipse(tb.x + tb.w / 2, tb.y + tb.h / 2, tb.w * 0.3, tb.h * 0.28, 0, 0, Math.PI * 2) : ctx.arc(tb.x + tb.w / 2, tb.y + tb.h / 2, tb.h * 0.28, 0, Math.PI * 2); ctx.fill(); ctx.stroke(); }
        else if (d.table !== 'none') { ctx.fillRect(tb.x + tb.w * 0.18, tb.y + tb.h * 0.36, tb.w * 0.64, tb.h * 0.28); ctx.strokeRect(tb.x + tb.w * 0.18, tb.y + tb.h * 0.36, tb.w * 0.64, tb.h * 0.28); }
        setDirty(c);
        toArray(d.tableLabels).forEach(function(t) { c.fontSize = 14; c.textColor = '#ffe9b0'; c.drawText(escSub(t.text), tb.x + Number(t.x) * tb.w - 80, tb.y + Number(t.y) * tb.h - 10, 160, 20, 'center'); });
        c.fontSize = 16; c.textColor = '#ffe9b0'; c.drawText(escSub(d.peopleTitle || '사람 (클릭해서 집기)'), (L.people[0] ? L.people[0].x : 0) + 6, (L.people[0] ? L.people[0].y : 100) - 26, 200, 22, 'left');
        for (i = 0; i < people.length; i++) {
            var pr = L.people[i], placed = this._seat.indexOf(i) >= 0, held = this._hold === i;
            escBox(c, pr, held ? 'rgba(255,214,100,0.98)' : (placed ? 'rgba(255,255,255,0.08)' : 'rgba(246,236,206,0.95)'), held ? '#ffffff' : '#8a6a40', held ? 3 : 1);
            escCardText(c, pr, escSub(people[i]), placed ? '#8a8070' : '#2a1a06', 15);
        }
        for (i = 0; i < L.seats.length; i++) {
            var sr = L.seats[i], v = this._seat[i], cur = this._cur === i && !this._end;
            escBox(c, sr, v >= 0 ? 'rgba(255,240,190,0.98)' : (d.image ? 'rgba(40,28,18,0.88)' : 'rgba(255,255,255,0.18)'), cur ? '#ffffff' : '#c8a060', cur ? 3 : 2);
            if (v >= 0) escCardText(c, sr, escSub(String(people[v]).split('\n')[0].split(' (')[0]), '#2a1a06', d.image ? 13 : 15);
            else { c.fontSize = 14; c.textColor = '#ffffff'; c.drawText((d.seatPrefix !== undefined ? d.seatPrefix : '자리 ') + (toArray(d.seats)[i].label || (i + 1)), sr.x, sr.y + (sr.h - 22) / 2, sr.w, 22, 'center'); }
        }
        var C = L.clue, y = C.y;
        escBox(c, C, 'rgba(246,236,206,0.95)', '#c8a060', 2);
        c.fontSize = 16; c.textColor = '#7a2a18'; c.drawText(escSub(d.clueTitle || '자리 규칙'), C.x, y + 6, C.w, 22, 'center'); y += 34;
        toArray(d.clues).forEach(function(s) { c.fontSize = 14; c.textColor = '#3a2a18'; escWrap(c, '· ' + escSub(s), C.w - 16).forEach(function(l) { c.drawText(l, C.x + 8, y, C.w - 16, 18, 'left'); y += 18; }); y += 6; });
        this.footer(escSub(d.footer || '사람을 클릭해 집고 → 자리를 클릭 · 키보드: ↑↓ 자리 고르기, ← → 앉을 사람 바꾸기 · 다 앉히면 [확인]'));
        this.drawButtons(d.okLabel || '이대로 앉히기', this._cur === L.seats.length);
    };

    // ----- dock: 조절 막대 맞추기 (도킹) ------------------------------------------------------------
    //  { type:'dock', title, help, target:{x:50,y:50}, start:{x:15,y:80}, tol:4, speeds:['빠르게','보통','아주 느리게'], speedAnswer:3 }
    Window_EscGame.prototype.dockLayout = function() {
        var w = this.contentsWidth(), a = this.areaRect(84), vw = Math.min(a.h, a.w * 0.48);
        var view = { x: a.x + 10, y: a.y, w: vw, h: vw }, sx = view.x + vw + 30, sw = a.w - vw - 50, rows = [];
        for (var i = 0; i < 3; i++) rows.push({ x: sx, y: a.y + 20 + i * 76, w: sw, h: 50 });
        return { view: view, rows: rows };
    };
    Window_EscGame.prototype.update_dock = function() {
        var d = this._def, nspeed = toArray(d.speeds).length || 3, L = this.dockLayout();
        if (Input.isRepeated('down')) { this._row = (this._row + 1) % 4; SoundManager.playCursor(); }
        if (Input.isRepeated('up')) { this._row = (this._row + 3) % 4; SoundManager.playCursor(); }
        var st = Input.isPressed('shift') ? 2 : 0.6;
        if (this._row < 2) {
            if (Input.isPressed('left')) this._dv[this._row] = Math.max(0, this._dv[this._row] - st);
            if (Input.isPressed('right')) this._dv[this._row] = Math.min(100, this._dv[this._row] + st);
        } else if (this._row === 2) {
            if (Input.isRepeated('left')) { this._dv[2] = Math.max(0, this._dv[2] - 1); SoundManager.playCursor(); }
            if (Input.isRepeated('right')) { this._dv[2] = Math.min(nspeed - 1, this._dv[2] + 1); SoundManager.playCursor(); }
        }
        if (Input.isTriggered('ok')) { if (this._row === 3) { SoundManager.playOk(); this.submit(); } else { this._row++; SoundManager.playCursor(); } }
        if (TouchInput.isPressed()) {
            var p = this.local();
            for (var i = 0; i < 2; i++) { var r = L.rows[i]; if (p.y >= r.y - 6 && p.y <= r.y + r.h + 6 && p.x >= r.x - 10 && p.x <= r.x + r.w + 10) { this._row = i; this._dv[i] = Math.max(0, Math.min(100, (p.x - r.x) / r.w * 100)); } }
        }
        if (TouchInput.isTriggered()) {
            var q = this.local(), r2 = L.rows[2];
            if (this.inside(r2, q)) { this._row = 2; this._dv[2] = Math.max(0, Math.min(nspeed - 1, Math.floor((q.x - r2.x) / (r2.w / nspeed)))); SoundManager.playCursor(); return; }
            this.touchButtons();
        }
    };
    Window_EscGame.prototype.draw_dock = function() {
        var c = this.contents, d = this._def, L = this.dockLayout(), V = L.view, t = d.target || {}, speeds = toArray(d.speeds).length ? toArray(d.speeds) : ['빠르게', '보통', '아주 느리게'], i;
        this.drawHeader();
        var ctx = ctxOf(c), cx = V.x + V.w / 2, cy = V.y + V.h / 2;
        ctx.fillStyle = '#05070f'; ctx.fillRect(V.x, V.y, V.w, V.h);
        for (i = 0; i < 40; i++) { ctx.fillStyle = 'rgba(255,255,255,' + (0.3 + (i * 37 % 10) / 15) + ')'; ctx.fillRect(V.x + (i * 97 % V.w), V.y + (i * 53 % V.h), 2, 2); }
        // 상대 우주선 (목표가 화면 가운데에 오면 정렬)
        var ox = cx + (Number(t.x) - this._dv[0]) / 100 * V.w, oy = cy + (Number(t.y) - this._dv[1]) / 100 * V.h;
        ctx.fillStyle = '#7a8a6a'; ctx.beginPath(); ctx.arc(ox, oy, 46, 0, Math.PI * 2); ctx.fill();
        ctx.fillStyle = '#c8b070'; ctx.fillRect(ox - 120, oy - 12, 70, 24); ctx.fillRect(ox + 50, oy - 12, 70, 24);
        ctx.fillStyle = '#20242a'; ctx.beginPath(); ctx.arc(ox, oy, 18, 0, Math.PI * 2); ctx.fill();
        ctx.strokeStyle = '#e8e8e8'; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(ox - 10, oy); ctx.lineTo(ox + 10, oy); ctx.moveTo(ox, oy - 10); ctx.lineTo(ox, oy + 10); ctx.stroke();
        // 우리 쪽 조준선
        var ok = Math.abs(this._dv[0] - Number(t.x)) <= Number(d.tol || 4) && Math.abs(this._dv[1] - Number(t.y)) <= Number(d.tol || 4);
        ctx.strokeStyle = ok ? '#7dff9a' : '#ff9a6a'; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(cx - 40, cy); ctx.lineTo(cx + 40, cy); ctx.moveTo(cx, cy - 40); ctx.lineTo(cx, cy + 40); ctx.arc(cx, cy, 26, 0, Math.PI * 2); ctx.stroke();
        setDirty(c);
        c.fontSize = 15; c.textColor = ok ? '#7dff9a' : '#ffcf9a'; c.drawText(ok ? '정렬 완료!' : '십자선을 상대 우주선 가운데로', V.x, V.y + V.h - 26, V.w, 22, 'center');
        var names = [d.xLabel || '좌우', d.yLabel || '위아래', d.sLabel || '다가가는 속도'];
        for (i = 0; i < 3; i++) {
            var r = L.rows[i], cur = this._row === i && !this._end;
            c.fontSize = 16; c.textColor = cur ? '#ffffff' : '#ffe9b0'; c.drawText((cur ? '▶ ' : '') + escSub(names[i]), r.x, r.y - 24, r.w, 22, 'left');
            if (i < 2) {
                c.fillRect(r.x, r.y + r.h / 2 - 4, r.w, 8, 'rgba(255,255,255,0.25)');
                var kx = r.x + this._dv[i] / 100 * r.w;
                roundRect(c, kx - 12, r.y + 4, 24, r.h - 8, 6, cur ? '#ffd070' : '#c8a060', '#ffffff', cur ? 3 : 1);
            } else {
                var bw = r.w / speeds.length;
                for (var k = 0; k < speeds.length; k++) {
                    var br = { x: r.x + k * bw + 3, y: r.y + 6, w: bw - 6, h: r.h - 12 };
                    escBox(c, br, this._dv[2] === k ? 'rgba(255,214,100,0.98)' : 'rgba(255,255,255,0.12)', this._dv[2] === k ? '#ffffff' : 'rgba(255,255,255,0.3)', this._dv[2] === k ? 2 : 1);
                    c.fontSize = 15; c.textColor = this._dv[2] === k ? '#2a1a06' : '#ffffff'; c.drawText(escSub(speeds[k]), br.x, br.y + (br.h - 22) / 2, br.w, 22, 'center');
                }
            }
        }
        if (d.note) { var ny = L.rows[2].y + L.rows[2].h + 14; c.fontSize = 14; c.textColor = '#d8ccb0'; escWrap(c, escSub(d.note), L.rows[2].w).forEach(function(l) { c.drawText(l, L.rows[2].x, ny, L.rows[2].w, 20, 'left'); ny += 20; }); }
        this.footer('↑↓ 조절 막대 고르기 · ← → 움직이기(Shift 빠르게) · 막대를 끌어도 돼요 · 다 맞추면 [도킹]');
        this.drawButtons('도킹', this._row === 3);
    };

    // ----- rounds: 알맞은 번역 고르기 (여러 문제) ------------------------------------------------------
    //  { type:'rounds', title, help, rounds:[{ who:'고르바초프', src:'원문', gloss:'(말뜻 풀이)', options:['…','…','…'], answer:2, why:'…', hint:'…' }] }
    Window_EscGame.prototype.roundRects = function() {
        var w = this.contentsWidth(), R = toArray(this._def.rounds)[this._round] || {}, n = toArray(R.options).length, y0 = 214, rs = [];
        var lh = Math.min(62, Math.floor((this.contentsHeight() - y0 - 106) / Math.max(1, n)));
        for (var i = 0; i < n; i++) rs.push({ x: 20, y: y0 + i * lh, w: w - 40, h: lh - 8 });
        return rs;
    };
    Window_EscGame.prototype.roundPick = function(i) {
        var rounds = toArray(this._def.rounds), R = rounds[this._round], d = this._def;
        if (this._after > 0) return;
        if (i === Number(R.answer) - 1) {
            SoundManager.playOk(); playSafeSe(SE_ITEM, 80, 120);
            this._picked = i; this._after = 1; this.say('정답! ' + escSub(R.why || ''), '#9dffb0'); this._msgT = 99999;
        } else {
            this._rfail++; SoundManager.playBuzzer();
            if (this._rfail >= Number(d.autoAfter || 3)) { this._picked = Number(R.answer) - 1; this._after = 1; this.say('정답을 보여 줄게요. ' + escSub(R.why || ''), '#ffe9a8'); this._msgT = 99999; }
            else if (this._rfail >= Number(d.hintAfter || 2) && R.hint) this.say('힌트: ' + escSub(R.hint), '#ffe9a8');
            else this.say(escSub(R.wrong && R.wrong[i] ? R.wrong[i] : '원래 말과 뜻이 달라져요. 다시 골라 봐요.'), '#ff9a8a');
        }
    };
    Window_EscGame.prototype.roundNext = function() {
        var rounds = toArray(this._def.rounds);
        this._round++; this._rfail = 0; this._picked = -1; this._after = 0; this._cur = 0; this._msg = ''; this._msgT = 0;
        if (this._round >= rounds.length) { this._round = rounds.length - 1; this._picked = Number(rounds[this._round].answer) - 1; this.finish(true); }
    };
    Window_EscGame.prototype.update_rounds = function() {
        var rs = this.roundRects(), n = rs.length;
        if (this._after > 0) {
            if (Input.isTriggered('ok') || TouchInput.isTriggered()) { SoundManager.playCursor(); this.roundNext(); }
            return;
        }
        if (Input.isRepeated('down')) { this._cur = (this._cur + 1) % n; SoundManager.playCursor(); }
        if (Input.isRepeated('up')) { this._cur = (this._cur + n - 1) % n; SoundManager.playCursor(); }
        if (Input.isTriggered('ok')) this.roundPick(this._cur);
        if (TouchInput.isTriggered()) {
            var p = this.local();
            for (var i = 0; i < n; i++) if (this.inside(rs[i], p)) { this._cur = i; this.roundPick(i); return; }
            var b = this.btnRects();
            if (this.inside(b.later, p)) { this.active = false; SoundManager.playCancel(); if (this._handlers.cancel) this._handlers.cancel(); }
        }
    };
    Window_EscGame.prototype.draw_rounds = function() {
        var c = this.contents, w = this.contentsWidth(), d = this._def, rounds = toArray(d.rounds), R = rounds[this._round] || {}, rs = this.roundRects(), i;
        this.drawHeader();
        c.fontSize = 15; c.textColor = '#d8ccb0'; c.drawText('문제 ' + (this._round + 1) + ' / ' + rounds.length, 0, 76, w - 14, 20, 'right');
        var box = { x: 20, y: 100, w: w - 40, h: 104 };
        escBox(c, box, 'rgba(246,236,206,0.95)', '#c8a060', 2);
        c.fontSize = 15; c.textColor = '#7a2a18'; c.drawText(escSub(R.who || '원문'), box.x + 12, box.y + 6, box.w - 24, 20, 'left');
        c.fontSize = 18; c.textColor = '#1a1a2a';
        var ls = escWrap(c, escSub(R.src || ''), box.w - 24);
        for (i = 0; i < ls.length && i < 2; i++) c.drawText(ls[i], box.x + 12, box.y + 28 + i * 24, box.w - 24, 24, 'left');
        if (R.gloss) { c.fontSize = 14; c.textColor = '#6a5a40'; c.drawText(escSub(R.gloss), box.x + 12, box.y + box.h - 24, box.w - 24, 20, 'left'); }
        for (i = 0; i < rs.length; i++) {
            var r = rs[i], cur = this._cur === i && !this._end && this._after === 0, ok = this._picked === i;
            escBox(c, r, ok ? 'rgba(160,240,170,0.98)' : (cur ? 'rgba(255,230,160,0.98)' : 'rgba(246,236,206,0.9)'), cur ? '#ffffff' : '#8a6a40', cur ? 3 : 1);
            escCardText(c, { x: r.x + 30, y: r.y, w: r.w - 30, h: r.h }, escSub(toArray(R.options)[i]), '#2a1a06', 16);
            c.fontSize = 16; c.textColor = '#7a2a18'; c.drawText('ⓐⓑⓒⓓⓔ'.charAt(i), r.x + 6, r.y + (r.h - 22) / 2, 26, 22, 'center');
        }
        this.footer(this._after > 0 ? 'Enter 또는 클릭: 다음' : '↑↓ 고르고 Enter · 또는 번역을 클릭(톡)');
        this.drawButtons('　', false);
    };

    // ---- 3) 온도계 게이지 ---------------------------------------------------------------------
    function Sprite_EscGauge() { this.initialize.apply(this, arguments); }
    Sprite_EscGauge.prototype = Object.create(Sprite.prototype);
    Sprite_EscGauge.prototype.constructor = Sprite_EscGauge;
    Sprite_EscGauge.prototype.initialize = function(def) {
        Sprite.prototype.initialize.call(this, new Bitmap(70, 230));
        this._def = def; this._shown = null; this._val = null;
    };
    Sprite_EscGauge.prototype.target = function() {
        var v = EscapeManager._vars && EscapeManager._vars[this._def['var'] || 'temp'];
        if (v === undefined || v === null || v === '') return null;
        var n = Number(v); return isNaN(n) ? null : n;
    };
    Sprite_EscGauge.prototype.update = function() {
        Sprite.prototype.update.call(this);
        var t = this.target(), M = EscapeManager, sc = SceneManager._scene;
        var hide = t === null || M._phase !== 'play' || M._gameOpen || M._bagOpen || (sc && sc._escCloseupName);
        this.opacity += hide ? -24 : 24;
        if (t === null) return;
        if (this._val === null) this._val = t;
        if (Math.abs(this._val - t) > 0.05) this._val += (t - this._val) * 0.04; else this._val = t;
        var key = Math.round(this._val * 4);
        if (key !== this._shown) { this._shown = key; this.redraw(); }
        this.x = SW() - 70 - 6; this.y = HUD_H + 54;
    };
    Sprite_EscGauge.prototype.redraw = function() {
        var b = this.bitmap, d = this._def, mn = Number(d.min !== undefined ? d.min : -50), mx = Number(d.max !== undefined ? d.max : 10), v = this._val;
        b.clear();
        roundRect(b, 0, 0, 70, 230, 10, 'rgba(10,14,24,0.72)', 'rgba(170,200,230,0.6)', 2);
        b.fontSize = 12; b.textColor = '#cfe6ff'; b.drawText(d.label || '냉전 온도', 0, 4, 70, 18, 'center');
        var tx = 28, ty = 28, th = 150, f = Math.max(0, Math.min(1, (v - mn) / (mx - mn)));
        b.fillRect(tx, ty, 14, th, 'rgba(255,255,255,0.18)');
        var col = v <= -35 ? '#4a8cff' : v <= -15 ? '#7ab8ff' : v < 0 ? '#bfe0ff' : '#ff8a5a';
        b.fillRect(tx + 2, ty + th * (1 - f), 10, th * f, col);
        var ctx = ctxOf(b); ctx.fillStyle = col; ctx.beginPath(); ctx.arc(tx + 7, ty + th + 12, 13, 0, Math.PI * 2); ctx.fill(); setDirty(b);
        var z = ty + th * (1 - (0 - mn) / (mx - mn));
        b.fillRect(tx - 6, z, 26, 2, '#ffffff'); b.fontSize = 11; b.textColor = '#ffffff'; b.drawText('0°', tx + 20, z - 9, 24, 18, 'left');
        b.fontSize = 14; b.textColor = '#ffffff'; b.drawText(Math.round(v) + '°', 0, 206, 70, 20, 'center');
    };
    var _v44_cdo = Scene_Map.prototype.createDisplayObjects;
    Scene_Map.prototype.createDisplayObjects = function() {
        _v44_cdo.apply(this, arguments);
        var g = EscapeManager.isActive() && $dataEscape && $dataEscape.gauge;
        if (g) { this._escGauge = new Sprite_EscGauge(g); this._escGauge.opacity = 0; this.addChild(this._escGauge); }
    };

    // ---- 4) 후기 화면 (저절로 넘어가지 않음 · 단추를 누르는 순간 새 창) --------------------------------
    function Window_EscReview() { this.initialize.apply(this, arguments); }
    Window_EscReview.prototype = Object.create(Window_Base.prototype);
    Window_EscReview.prototype.constructor = Window_EscReview;
    Window_EscReview.prototype.initialize = function() {
        var w = Math.min(760, SW() - 24), h = Math.min(SH() - 24, 600);
        Window_Base.prototype.initialize.call(this, (SW() - w) / 2, (SH() - h) / 2, w, h);
        this.openness = 0; this.active = false; this._focus = 0; this._note = ''; this._def = null;
        this.opacity = 0; this.backOpacity = 0;
    };
    Window_EscReview.prototype.setup = function(def, done) {
        this._def = def; this._done = done; this._focus = 0; this._note = ''; this._openFrame = Graphics.frameCount;
        this._pic = def.picture ? ImageManager.loadPicture(String(def.picture)) : null;
        var self = this; if (this._pic) this._pic.addLoadListener(function() { self.refresh(); });
        this.open(); this.activate(); this.refresh();
    };
    Window_EscReview.prototype.btns = function() {
        var w = this.contentsWidth(), h = this.contentsHeight();
        return [{ x: w / 2 - 250, y: h - 74, w: 240, h: 46, t: '후기 남기기 (새 창)' }, { x: w / 2 + 10, y: h - 74, w: 240, h: 46, t: '처음 화면으로' }];
    };
    Window_EscReview.prototype.canvasRect = function(r) {
        var p = this.standardPadding();
        return { x: this.x + p + r.x, y: this.y + p + r.y, w: r.w, h: r.h };
    };
    Window_EscReview.prototype.ready = function() { return this.active && this.isOpen() && Graphics.frameCount - this._openFrame > 20; };
    Window_EscReview.prototype.openNow = function() {
        if (!this._def) return;
        var now = Date.now(); if (this._lastOpen && now - this._lastOpen < 800) return; this._lastOpen = now;
        try { if (escIsFullscreen()) escExitFullscreen(); } catch (e) {}
        var ok = openExternal(String(this._def.url));
        this._note = ok ? '새 창(탭)에서 후기 페이지가 열렸어요. 안 보이면 화면 아래 작업 표시줄이나 브라우저 탭을 확인해 주세요.'
                        : '브라우저가 새 창을 막았어요. 휴대폰으로 QR 코드를 찍거나 아래 주소를 입력해 주세요.';
        this.refresh();
    };
    Window_EscReview.prototype.update = function() {
        Window_Base.prototype.update.call(this);
        if (!this.ready()) return;
        if (Input.isRepeated('left') || Input.isRepeated('right')) { this._focus = 1 - this._focus; SoundManager.playCursor(); this.refresh(); }
        if (Input.isTriggered('ok') && this._focus === 1) { this.finish(); return; }
        if (Input.isTriggered('cancel')) { this._focus = 1; this.refresh(); }
        if (TouchInput.isTriggered()) {
            var b = this.btns(), x = TouchInput.x, y = TouchInput.y;
            for (var i = 0; i < 2; i++) { var r = this.canvasRect(b[i]); if (x >= r.x && x < r.x + r.w && y >= r.y && y < r.y + r.h) { this._focus = i; this.refresh(); if (i === 1) { this.finish(); return; } } }
        }
    };
    Window_EscReview.prototype.finish = function() {
        SoundManager.playOk(); this.active = false; this.close();
        var f = this._done; this._done = null; if (f) f();
    };
    Window_EscReview.prototype.refresh = function() {
        var c = this.contents, d = this._def; if (!c || !d) return;
        var w = this.contentsWidth(), h = this.contentsHeight();
        c.clear(); roundRect(c, 0, 0, w, h, 12, 'rgba(20,24,34,0.97)', 'rgba(170,200,230,0.7)', 2);
        c.fontSize = 24; c.textColor = '#ffe9b0'; c.drawText(d.title || '후기를 남겨 주세요', 0, 6, w, 32, 'center');
        var top = 46, bottom = h - 150, ph = bottom - top;
        if (this._pic && this._pic.isReady()) {
            var s = Math.min((w - 20) / this._pic.width, ph / this._pic.height), pw = this._pic.width * s, pph = this._pic.height * s;
            c.blt(this._pic, 0, 0, this._pic.width, this._pic.height, (w - pw) / 2, top + (ph - pph) / 2, pw, pph);
        }
        c.fontSize = 16; c.textColor = '#ffffff';
        var lines = escWrap(c, this._note || d.text || '끝까지 함께해 줘서 고마워요!', w - 30);
        for (var i = 0; i < lines.length && i < 2; i++) c.drawText(lines[i], 15, bottom + 4 + i * 22, w - 30, 22, 'center');
        c.fontSize = 15; c.textColor = '#9ad0ff'; c.drawText(String(d.url).replace(/^https?:\/\//, ''), 0, bottom + 50, w, 20, 'center');
        var b = this.btns();
        for (var k = 0; k < 2; k++) {
            var f = this._focus === k;
            roundRect(c, b[k].x, b[k].y, b[k].w, b[k].h, 10, k === 0 ? (f ? 'rgba(255,200,70,0.98)' : 'rgba(255,200,70,0.7)') : (f ? 'rgba(255,255,255,0.35)' : 'rgba(255,255,255,0.15)'), f ? '#ffffff' : 'rgba(255,255,255,0.4)', f ? 3 : 1);
            c.fontSize = 18; c.textColor = k === 0 ? '#2a1a06' : '#ffffff'; c.drawText(b[k].t, b[k].x, b[k].y + 7, b[k].w, 30, 'center');
        }
        c.fontSize = 13; c.textColor = '#a8b4c8'; c.drawText('← → 고르기 · Enter 또는 클릭', 0, h - 24, w, 18, 'center');
    };
    // 단추를 누른 '그 순간'(브라우저 입력 이벤트 안)에서 창을 열어야 팝업 차단을 피함
    function escReviewGesture(e) {
        var sc = SceneManager._scene, win = sc && sc._escReview;
        if (!win || !win.ready()) return;
        if (e.type === 'keydown') {
            if (['Enter', ' ', 'z', 'Z'].indexOf(e.key) >= 0 && win._focus === 0) win.openNow();
            return;
        }
        var pt = e.changedTouches && e.changedTouches[0] ? e.changedTouches[0] : e;
        var x = Graphics.pageToCanvasX(pt.pageX), y = Graphics.pageToCanvasY(pt.pageY), r = win.canvasRect(win.btns()[0]);
        if (x >= r.x && x < r.x + r.w && y >= r.y && y < r.y + r.h) { win._focus = 0; win.openNow(); }
    }
    document.addEventListener('keydown', escReviewGesture);
    document.addEventListener('mousedown', escReviewGesture);
    document.addEventListener('touchend', escReviewGesture);
    var _v44_cdo2 = Scene_Map.prototype.createDisplayObjects;
    Scene_Map.prototype.createDisplayObjects = function() {
        _v44_cdo2.apply(this, arguments);
        if (!EscapeManager.isActive()) return;
        this._escReview = new Window_EscReview();
        this.addChild(this._escReview);
    };
    // 엔딩의 후기 단계를 후기 화면으로 바꿈
    var _v44_finish = EscapeManager.finishGame;
    EscapeManager.finishGame = function(success) {
        _v44_finish.apply(this, arguments);
        var review = this._data.review;
        if (!review || !review.url || !this._queue) return;
        for (var i = 0; i < this._queue.length; i++) {
            var s = this._queue[i];
            if (s && s.openUrl === review.url) { this._queue[i] = { reviewPage: true }; break; }
        }
    };
    var _v44_ps2 = EscapeManager.processStep;
    EscapeManager.processStep = function(s) {
        if (s && typeof s === 'object' && s.reviewPage) {
            var sc = this._scene, self = this, review = this._data.review || {};
            this.hideCloseup();
            if (!sc || !sc._escReview) return;
            this._waiting = true; this._gameOpen = true;
            sc._escReview.setup(review, function() { self._gameOpen = false; self.resume(); });
            return;
        }
        return _v44_ps2.apply(this, arguments);
    };
    var _v44_modal = EscapeManager.escModalVisible;
    EscapeManager.escModalVisible = function() {
        var sc = this._scene;
        if (sc && sc._escReview && (sc._escReview.isOpen() || sc._escReview.isOpening())) return true;
        return _v44_modal.apply(this, arguments);
    };
    // 엔딩(phase 'ending')에서도 끝나지 않는 기다림을 풀어 주기 (후기 화면은 제외)
    var _v44_wd = EscapeManager.escWatchdog;
    EscapeManager.escWatchdog = function() {
        _v44_wd.apply(this, arguments);
        var sc = this._scene;
        if (!sc || !(sc instanceof Scene_Map) || this._phase !== 'ending') return;
        if (this._waiting && !this.escModalVisible() && !sc.isBusy()) {
            this._endWd = (this._endWd || 0) + 1;
            if (this._endWd > 180) { this._endWd = 0; console.warn('[EscapeRoom] 안전장치: 엔딩 기다림을 풀었어요'); this.resume(); }
        } else this._endWd = 0;
    };
    EscapeManager.escVersion = ESC_VERSION;


    //=========================================================================
    // v4.5 (알렉산드리아의 두루마리)
    //  · seat 묶음 규칙: "groups": [[0,1,2],[3,4,5]] (자리 번호 묶음), "kinds": ['해안','내륙',...] (사람마다 종류)
    //    → 모든 자리가 차고, 묶음마다 종류가 하나씩 다르면 정답 (답이 여러 가지여도 됨). "answer"는 [정답 보기]용 한 가지
    //  · seat "table": "none" 이면 가운데 탁자를 그리지 않음
    //=========================================================================
    var _v45_isSolved = Window_EscGame.prototype.isSolved;
    Window_EscGame.prototype.isSolved = function() {
        var d = this._def;
        if (this._type === 'seat' && d.groups && d.kinds) {
            var kinds = toArray(d.kinds), seat = this._seat, ok = true;
            for (var i = 0; i < seat.length; i++) if (seat[i] < 0) return false;
            toArray(d.groups).forEach(function(g) {
                var seen = {};
                toArray(g).forEach(function(si) { var k = kinds[seat[si]]; if (seen[k]) ok = false; seen[k] = true; });
            });
            return ok;
        }
        return _v45_isSolved.apply(this, arguments);
    };
    //=========================================================================
    // 타이틀 그림 위의 조각들 (화면 너비에 맞춰 놓음 · 넓은 화면/좁은 화면 모두 잘리지 않게)
    //  "titleLayers": [{ "image": "Cw_TitleBoard", "x": "center", "y": 60 },
    //                  { "image": "Cw_TitleThermo", "side": "left", "margin": 26, "y": 90, "clear": 362 },   ← 가운데 판(반너비 clear)과 겹치면 숨김
    //                  { "image": "Cw_TitlePeople", "x": "center", "bottom": 4, "fit": 12 }]                 ← 화면보다 넓으면 줄여서 다 보이게
    //=========================================================================
    var _tl_createBackground = Scene_Title.prototype.createBackground;
    Scene_Title.prototype.createBackground = function() {
        _tl_createBackground.apply(this, arguments);
        var d = escData(), self = this;
        if (!d || !this._escTitleImage) return;
        toArray(d.titleLayers).forEach(function(L) {
            if (!L || !hasAsset('title', L.image)) return;
            var bmp = ImageManager.loadTitle1(L.image), sp = new Sprite(bmp);
            sp.visible = false; self.addChild(sp);
            bmp.addLoadListener(function() {
                var W = Graphics.width, H = Graphics.height, sc = 1, bw = bmp.width, bh = bmp.height;
                if (L.fit != null && bw > W - 2 * Number(L.fit)) sc = (W - 2 * Number(L.fit)) / bw;
                sp.scale.x = sp.scale.y = sc; bw *= sc; bh *= sc;
                var m = Number(L.margin || 0), x;
                if (L.side === 'left') x = m;
                else if (L.side === 'right') x = W - m - bw;
                else x = (W - bw) / 2 + Number(L.dx || 0);
                var y = L.bottom != null ? H - Number(L.bottom) - bh : Number(L.y || 0);
                if (L.clear != null) {
                    var c0 = W / 2 - Number(L.clear), c1 = W / 2 + Number(L.clear);
                    if (x < c1 && x + bw > c0) return;      // 가운데 판과 겹칠 만큼 좁은 화면이면 그리지 않음
                }
                sp.x = Math.round(x); sp.y = Math.round(y); sp.visible = true;
            });
        });
    };
    //=========================================================================
    // 읽기 쉬운 글씨 (퍼즐 창 · 후기 화면)
    //  · 한국어 MV 프로젝트의 기본 창 글꼴(돋움)은 작은 글씨가 흐리게 보여서, 퍼즐 창에는 fonts/EscReadable-Medium.ttf
    //    (Noto Sans KR Medium, OFL 무료 글꼴 · 한글 · 영어 · 러시아어 포함)를 씀. 파일이 없으면 원래 글꼴로 그림.
    //  · 밝은 카드 위 어두운 글씨에 검은 테두리가 번지지 않게, 퍼즐 창 글씨에는 테두리를 쓰지 않음
    //  · 글씨가 칸보다 길면 칸에 맞게 줄임
    //=========================================================================
    var ESC_READ_FONT = 'EscReadable';
    var escReadReady = false;
    (function() {
        try {
            var st = document.createElement('style');
            st.textContent = '@font-face { font-family: "' + ESC_READ_FONT + '"; src: url("fonts/EscReadable-Medium.ttf"); }';
            document.getElementsByTagName('head')[0].appendChild(st);
            if (document.fonts && document.fonts.load) {
                document.fonts.load('20px "' + ESC_READ_FONT + '"').then(function() { escReadReady = true; }, function() { escReadReady = true; });
            } else escReadReady = true;
        } catch (e) { escReadReady = true; }
    })();
    var _read_bootReady = Scene_Boot.prototype.isReady;
    Scene_Boot.prototype.isReady = function() {
        if (!escReadReady) { this._escReadWait = (this._escReadWait || 0) + 1; if (this._escReadWait < 360) return false; }   // 최대 6초만 기다림
        return _read_bootReady.apply(this, arguments);
    };
    function escReadFace(base) { return '"' + ESC_READ_FONT + '", ' + base; }
    function escFlatText(bmp) { if (bmp) { bmp.outlineColor = 'rgba(0,0,0,0)'; bmp.outlineWidth = 1; } }
    Window_EscGame.prototype.standardFontFace = function() { return escReadFace(Window_Base.prototype.standardFontFace.call(this)); };
    // 알림 · 힌트 글씨: 다른 글씨와 겹치지 않게 맨 마지막에 어두운 띠 위에 그림 (길면 3줄까지 · 읽을 시간 넉넉히)
    Window_EscGame.prototype.say = function(text, col) {
        this._msg = text; this._msgCol = col || '#ffffff';
        this._msgT = Math.min(900, Math.max(180, String(text || '').length * 9));
    };
    Window_EscGame.prototype.drawMsg = function(y) { this._msgY = y; };
    Window_EscGame.prototype.drawMsgBanner = function() {
        var c = this.contents; if (!c) return;
        if (!this._msg || (this._msgT <= 0 && !this._end)) return;
        var w = this.contentsWidth(), h = this.contentsHeight(), y = this._msgY == null ? h - 74 : this._msgY;
        var fs = 17; c.fontSize = fs;
        var lines = escWrap(c, this._msg, w - 90);
        while (lines.length > 3 && fs > 13) { fs--; c.fontSize = fs; lines = escWrap(c, this._msg, w - 90); }
        lines = lines.slice(0, 3);
        var lh = fs + 6, bh = lines.length * lh + 16, top = y >= h - 120 ? h - 52 - bh : y;
        roundRect(c, 30, top, w - 60, bh, 10, 'rgba(18,13,8,0.97)', 'rgba(255,233,168,0.7)', 2);
        c.textColor = this._msgCol;
        for (var i = 0; i < lines.length; i++) c.drawText(lines[i], 45, top + 8 + i * lh, w - 90, lh, 'center');
        this.resetTextColor();
    };
    // 확인 단추가 없는 게임은 '나중에' 단추를 가운데에
    var _read_btnRects = Window_EscGame.prototype.btnRects;
    Window_EscGame.prototype.btnRects = function() {
        var b = _read_btnRects.apply(this, arguments);
        if (this._noOk) { b.later = { x: this.contentsWidth() / 2 - 80, y: b.later.y, w: 160, h: b.later.h }; b.ok = { x: -9999, y: -9999, w: 0, h: 0 }; }
        return b;
    };
    var _read_drawButtons = Window_EscGame.prototype.drawButtons;
    Window_EscGame.prototype.drawButtons = function(okLabel, focused) {
        this._noOk = !!(okLabel && !String(okLabel).replace(/[\s\u3000]/g, ''));
        return _read_drawButtons.apply(this, arguments);
    };
    var _read_gameRefresh = Window_EscGame.prototype.refresh;
    Window_EscGame.prototype.refresh = function() {
        if (this.contents && this.contents.fontFace.indexOf(ESC_READ_FONT) < 0) this.contents.fontFace = this.standardFontFace();
        escFlatText(this.contents);
        var c = this.contents, self = this;
        if (c && !c._escFit) {     // 칸 너비(maxWidth)를 넘는 글씨는 줄여서 그림 (늘어뜨려 찌그러지지 않게)
            c._escFit = true;
            var _dt = c.drawText;
            c.drawText = function(text, x, y, maxWidth, lineHeight, align) {
                var fs = this.fontSize, t = String(text);
                if (maxWidth > 8) { while (this.fontSize > 11 && this.measureTextWidth(t) > maxWidth) this.fontSize--; }
                _dt.call(this, t, x, y, maxWidth, lineHeight, align);
                this.fontSize = fs;
            };
        }
        this._msgY = null;
        _read_gameRefresh.apply(this, arguments);
        if (this.drawMsgBanner) this.drawMsgBanner();
        escFlatText(this.contents);
    };
    if (typeof Window_EscReview !== 'undefined') {
        Window_EscReview.prototype.standardFontFace = Window_EscGame.prototype.standardFontFace;
        var _read_revRefresh = Window_EscReview.prototype.refresh;
        Window_EscReview.prototype.refresh = function() {
            if (this.contents) { this.contents.fontFace = this.standardFontFace(); escFlatText(this.contents); }
            _read_revRefresh.apply(this, arguments);
        };
    }
    // 글꼴이 늦게 불러지면 열린 퍼즐 창을 한 번 더 그림
    if (document.fonts && document.fonts.addEventListener) {
        document.fonts.addEventListener('loadingdone', function() {
            var sc = SceneManager._scene;
            if (sc && sc._escGame && sc._escGame._def && sc._escGame.isOpen()) sc._escGame.refresh();
            if (sc && sc._escReview && sc._escReview._def && sc._escReview.isOpen()) sc._escReview.refresh();
        });
    }
    // 테두리 굵기를 0으로 두면 캔버스가 이전 굵기를 그대로 써서 글씨가 번짐 → 0이면 테두리를 그리지 않음
    var _read_outline = Bitmap.prototype._drawTextOutline;
    Bitmap.prototype._drawTextOutline = function() {
        if (!(this.outlineWidth > 0)) return;
        _read_outline.apply(this, arguments);
    };


    //=========================================================================
    // v4.6 (「척화비 아래에서」)  새 퍼즐 (모두 시간 제한 없음)
    //  dial   다이얼 자물쇠      { type:'dial', wheels:4, symbols:[['0',...],...], answer:['1','8','6','3'], clues:[...], okLabel:'열기' }
    //  rub    탁본 뜨기(문지르기) { type:'rub', image:'kc_rub', need:0.82, grid:[30,18] }  다 문지르면 저절로 성공
    //  drill  대열 훈련(구령 짜기) { type:'drill', cols, rows, soldiers:[[x,y,'up']], targets:[[x,y]], blocks:[[x,y,'깃대']], commands:[...], max:8, solution:[0,1,...] }
    //  weigh  저울 두 번으로 무거운 자루 찾기 { type:'weigh', count:9, uses:2 }  (어느 자루가 무거운지는 플레이어가 운으로 맞힐 수 없게 정해짐)
    //  beacon 봉수 올리기        { type:'beacon', count:5, rounds:[{ text:'상황', answer:2, why:'설명' }], rules:[...] }
    //  seat   "image": 자리 뒤에 지도 그림
    //  방 "push"  : 돌 밀기 { stones:['stone1',...], targets:[[x,y],...], when:{조건}, flag:'끝 깃발', done:[단계] }
    //               단계 { "pushReset": true } 로 돌을 처음 자리로
    //  방 "watchTurn": true  : 감시(watchers)가 주인공이 한 칸 움직일 때만 한 칸 움직임 (차례 잠행)
    //=========================================================================
    Imported.EscapeRoom = '4.6.0';
    var V46_TYPES = { dial: 1, rub: 1, drill: 1, weigh: 1, beacon: 1 };
    var DIR4 = { up: 0, right: 1, down: 2, left: 3 };
    var _v46_setup = Window_EscGame.prototype.setup;
    Window_EscGame.prototype.setup = function(def) {
        var d = def, i, self = this;
        this._def = def;
        switch (String(def.type)) {
        case 'dial':
            this._syms = this.dialSymbols(d);
            this._dv = this._syms.map(function(s, k) { var st = toArray(d.start)[k]; var j = st !== undefined ? s.indexOf(String(st)) : 0; return j < 0 ? 0 : j; });
            break;
        case 'rub':
            var g = toArray(d.grid).length ? toArray(d.grid) : [30, 18];
            this._rg = [Number(g[0]), Number(g[1])]; this._rub = []; for (i = 0; i < this._rg[0] * this._rg[1]; i++) this._rub.push(false);
            this._bx = Math.floor(this._rg[0] / 2); this._by = Math.floor(this._rg[1] / 2);
            this._img = ImageManager.loadPicture(String(d.image || '')); this._rubDone = false;
            break;
        case 'drill':
            this._prog = []; this._run = null; this._drPos = this.drillStart(); this._drMsg = '';
            break;
        case 'weigh': this.weighReset(); this._row = 0; break;
        case 'beacon':
            this._lit = []; for (i = 0; i < Number(d.count || 5); i++) this._lit.push(false);
            this._round = 0; this._rfail = 0;
            break;
        case 'seat':
            this._img = d.image ? ImageManager.loadPicture(String(d.image)) : null;
            break;
        }
        _v46_setup.apply(this, arguments);
        if (V46_TYPES[this._type] && this.contents) { this.contents.outlineWidth = 0; this.refresh(); }
    };
    var _v46_refresh = Window_EscGame.prototype.refresh;
    Window_EscGame.prototype.refresh = function() {
        var flat = this.contents && V46_TYPES[this._type];
        if (flat) this.contents.outlineWidth = 0;
        _v46_refresh.apply(this, arguments);
        var self = this, bm = this._img;
        if (V46_TYPES[this._type] || this._type === 'seat') {
            if (bm && !bm.isReady() && !bm._escHooked && bm.addLoadListener) { bm._escHooked = true; bm.addLoadListener(function() { if (self._def) self.refresh(); }); }
        }
    };
    var _v46_isSolved = Window_EscGame.prototype.isSolved;
    Window_EscGame.prototype.isSolved = function() {
        var d = this._def, ans = toArray(d.answer), i, self = this;
        switch (this._type) {
        case 'dial':
            for (i = 0; i < this._dv.length; i++) if (this._syms[i][this._dv[i]] !== String(ans[i])) return false;
            return true;
        case 'rub': return this.rubCover() >= Number(d.need || 0.82);
        case 'drill': return this.drillOk(this._drPos);
        case 'weigh': return this._cand.length === 1 && this._sel === this._cand[0];
        case 'beacon': return this.litCount() === Number(toArray(d.rounds)[this._round].answer);
        }
        return _v46_isSolved.apply(this, arguments);
    };
    var _v46_showAnswer = Window_EscGame.prototype.showAnswer;
    Window_EscGame.prototype.showAnswer = function() {
        var d = this._def, ans = toArray(d.answer), self = this;
        switch (this._type) {
        case 'dial': this._dv = this._syms.map(function(s, k) { return Math.max(0, s.indexOf(String(ans[k]))); }); return;
        case 'rub': this._rub = this._rub.map(function() { return true; }); return;
        case 'drill':
            this._prog = toArray(d.solution).map(Number); this._run = null;
            var r = this.drillSim(this._prog); this._drPos = r.pos; return;
        case 'weigh':
            this._log = toArray(d.answerLog).length ? toArray(d.answerLog).map(String) :
                ['1) 세 자루씩 셋으로 나눠 두 묶음을 달아요 → 기울면 무거운 쪽, 수평이면 남은 묶음에 모래 자루가 있어요.',
                 '2) 그 세 자루 가운데 두 자루를 달아요 → 기울면 무거운 쪽, 수평이면 남은 한 자루!'];
            return;
        case 'beacon':
            var n = Number(toArray(d.rounds)[this._round].answer);
            this._lit = this._lit.map(function(v, k) { return k < n; }); return;
        }
        return _v46_showAnswer.apply(this, arguments);
    };
    // 실패 공통 (힌트 · 정답 보여 주기)
    Window_EscGame.prototype.v46Fail = function(msg) {
        var d = this._def;
        this._fails++;
        SoundManager.playBuzzer();
        if (this._fails >= Number(d.autoAfter || 3)) { this.showAnswer(); this.finish(true, true); return true; }
        if (this._fails >= Number(d.hintAfter || 2) && d.hint) this.say((msg ? escSub(msg) + ' · ' : '') + '힌트: ' + escSub(d.hint), '#ffe9a8');
        else this.say(escSub(msg || d.wrongMsg || '아직 아니에요. 다시 살펴봐요.'), '#ff9a8a');
        return false;
    };
    var _v46_submit = Window_EscGame.prototype.submit;
    Window_EscGame.prototype.submit = function() {
        if (this._end) return;
        var d = this._def;
        if (this._type === 'drill') {
            if (this._run) return;
            if (!this._prog.length) { this.say('먼저 구령 카드를 놓아요.', '#ffe9a8'); SoundManager.playBuzzer(); return; }
            this._drPos = this.drillStart(); this._run = { k: -1, t: 0, pos: this._drPos.map(function(p) { return p.slice(); }) };
            SoundManager.playOk(); return;
        }
        if (this._type === 'weigh') {
            if (this._sel < 0) { this.say('모래가 든 것 같은 자루를 먼저 골라요 (자루 아래 [고르기]).', '#ffe9a8'); SoundManager.playBuzzer(); return; }
            if (this.isSolved()) { this.finish(true); return; }
            var c = this._cand, msg;
            if (c.indexOf(this._sel) < 0) msg = '저울 결과를 보면 ' + (this._sel + 1) + '번 자루는 무게가 정상이에요. 처음부터 다시 달아 봐요.';
            else msg = '아쉬워요! 모래는 다른 자루에 있었어요. 저울 두 번으로 한 자루만 남게 해 봐요.';
            this.weighReset();
            this.v46Fail(msg); return;
        }
        if (this._type === 'beacon') {
            var rounds = toArray(d.rounds), R = rounds[this._round];
            if (this.litCount() === Number(R.answer)) {
                if (this._round >= rounds.length - 1) { this.finish(true); return; }
                this.say(escSub(R.why || '맞았어요!'), '#9dffb0'); if (!playSafeSe(SE_SOLVE, 60, 120)) SoundManager.playRecovery();
                this._round++; this._rfail = 0; this._lit = this._lit.map(function() { return false; }); return;
            }
            this._rfail++; SoundManager.playBuzzer();
            if (this._rfail >= Number(d.autoAfter || 3)) {
                this.say('정답은 ' + R.answer + '개였어요. ' + escSub(R.why || ''), '#ffe9a8');
                if (this._round >= rounds.length - 1) { this.showAnswer(); this.finish(true, true); return; }
                this._round++; this._rfail = 0; this._lit = this._lit.map(function() { return false; }); return;
            }
            if (this._rfail >= Number(d.hintAfter || 2) && (R.hint || d.hint)) this.say('힌트: ' + escSub(R.hint || d.hint), '#ffe9a8');
            else this.say('봉수 개수가 상황과 맞지 않아요. 규칙 판을 다시 봐요.', '#ff9a8a');
            return;
        }
        return _v46_submit.apply(this, arguments);
    };

    // ----- dial ---------------------------------------------------------------------------
    Window_EscGame.prototype.dialSymbols = function(d) {
        var n = Number(d.wheels || toArray(d.answer).length || 4), out = [], digits = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'];
        for (var i = 0; i < n; i++) { var s = toArray(d.symbols)[i]; out.push(s ? toArray(s).map(String) : digits.slice()); }
        return out;
    };
    Window_EscGame.prototype.dialRects = function() {
        var w = this.contentsWidth(), n = this._syms.length, ww = Math.min(92, (w - 80) / n - 14), gap = 16, tot = n * ww + (n - 1) * gap, x0 = (w - tot) / 2, y0 = 100;
        var R = [];
        for (var i = 0; i < n; i++) { var x = x0 + i * (ww + gap); R.push({ box: { x: x, y: y0 + 40, w: ww, h: 90 }, up: { x: x, y: y0, w: ww, h: 36 }, dn: { x: x, y: y0 + 134, w: ww, h: 36 } }); }
        return R;
    };
    Window_EscGame.prototype.dialTurn = function(i, k) {
        var n = this._syms[i].length; this._dv[i] = (this._dv[i] + k + n) % n; SoundManager.playCursor();
    };
    Window_EscGame.prototype.update_dial = function() {
        var n = this._syms.length;
        if (Input.isRepeated('right')) { this._cur = (this._cur + 1) % (n + 1); SoundManager.playCursor(); }
        if (Input.isRepeated('left')) { this._cur = (this._cur + n) % (n + 1); SoundManager.playCursor(); }
        if (this._cur < n && Input.isRepeated('up')) this.dialTurn(this._cur, -1);
        if (this._cur < n && Input.isRepeated('down')) this.dialTurn(this._cur, 1);
        if (Input.isTriggered('ok')) {
            if (this._cur === n) { SoundManager.playOk(); this.submit(); } else { this._cur++; SoundManager.playCursor(); }
        }
        if (TouchInput.isTriggered()) {
            var p = this.local(), R = this.dialRects();
            for (var i = 0; i < R.length; i++) {
                if (this.inside(R[i].up, p)) { this._cur = i; this.dialTurn(i, -1); return; }
                if (this.inside(R[i].dn, p) || this.inside(R[i].box, p)) { this._cur = i; this.dialTurn(i, 1); return; }
            }
            this.touchButtons();
        }
    };
    Window_EscGame.prototype.draw_dial = function() {
        var c = this.contents, w = this.contentsWidth(), d = this._def, R = this.dialRects(), i, self = this;
        this.drawHeader();
        for (i = 0; i < R.length; i++) {
            var r = R[i], cur = this._cur === i && !this._end, s = this._syms[i], v = this._dv[i];
            escBox(c, { x: r.box.x - 4, y: r.up.y - 4, w: r.box.w + 8, h: r.dn.y + r.dn.h - r.up.y + 8 }, 'rgba(70,52,34,0.9)', cur ? '#ffffff' : '#c8a060', cur ? 3 : 2);
            escBox(c, r.up, 'rgba(255,255,255,0.12)', 'rgba(255,255,255,0.3)'); escBox(c, r.dn, 'rgba(255,255,255,0.12)', 'rgba(255,255,255,0.3)');
            c.fontSize = 20; c.textColor = '#ffe9b0'; c.drawText('▲', r.up.x, r.up.y + 4, r.up.w, 28, 'center'); c.drawText('▼', r.dn.x, r.dn.y + 4, r.dn.w, 28, 'center');
            escBox(c, r.box, 'rgba(246,236,206,0.98)', '#8a6a40', 2);
            c.fontSize = 14; c.textColor = '#a89878';
            c.drawText(s[(v + s.length - 1) % s.length], r.box.x, r.box.y + 2, r.box.w, 20, 'center');
            c.drawText(s[(v + 1) % s.length], r.box.x, r.box.y + r.box.h - 22, r.box.w, 20, 'center');
            escFit(c, s[v], r.box.w - 10, 40, 16); c.textColor = '#2a1a06'; c.drawText(s[v], r.box.x + 5, r.box.y + 24, r.box.w - 10, 44, 'center');
        }
        var y = R.length ? R[0].dn.y + 52 : 300, clues = toArray(d.clues);
        if (clues.length) {
            var box = { x: 40, y: y, w: w - 80, h: Math.min(this.contentsHeight() - y - 108, 26 + clues.length * 24) };
            escBox(c, box, 'rgba(246,236,206,0.95)', '#c8a060', 2);
            var yy = box.y + 8;
            clues.forEach(function(t) { c.fontSize = 16; c.textColor = '#3a2a18'; escWrap(c, escSub(t), box.w - 24).forEach(function(l) { if (yy < box.y + box.h - 18) c.drawText(l, box.x + 12, yy, box.w - 24, 22, 'left'); yy += 22; }); });
        }
        this.footer('← → 바퀴 고르기 · ↑ ↓ 돌리기 · 클릭(톡): ▲▼ 또는 숫자 칸 · 다 맞추면 [' + (d.okLabel || '열기') + ']');
        this.drawButtons(d.okLabel || '열기', this._cur === R.length);
    };

    // ----- rub (탁본) -----------------------------------------------------------------------
    Window_EscGame.prototype.rubFrame = function() {
        var a = this.areaRect(84), img = this._img, iw = img && img.width || 600, ih = img && img.height || 360;
        var sc = Math.min(a.w / iw, (a.h - 26) / ih), fw = iw * sc, fh = ih * sc;
        return { x: a.x + (a.w - fw) / 2, y: a.y + 24 + (a.h - 26 - fh) / 2, w: fw, h: fh, s: sc, iw: iw, ih: ih };
    };
    Window_EscGame.prototype.rubCover = function() {
        var n = 0; for (var i = 0; i < this._rub.length; i++) if (this._rub[i]) n++;
        return n / Math.max(1, this._rub.length);
    };
    Window_EscGame.prototype.rubAt = function(cx, cy, r) {
        var G = this._rg, ch = false;
        for (var y = cy - r; y <= cy + r; y++) for (var x = cx - r; x <= cx + r; x++) {
            if (x < 0 || y < 0 || x >= G[0] || y >= G[1]) continue;
            if ((x - cx) * (x - cx) + (y - cy) * (y - cy) > r * r + 1) continue;
            var k = y * G[0] + x; if (!this._rub[k]) { this._rub[k] = true; ch = true; }
        }
        if (ch && this._t % 6 === 0) SoundManager.playCursor();
        return ch;
    };
    Window_EscGame.prototype.update_rub = function() {
        var G = this._rg, d = this._def, br = Number(d.brush || 2);
        if (Input.isRepeated('right')) { this._bx = Math.min(G[0] - 1, this._bx + 1); this.rubAt(this._bx, this._by, br); }
        if (Input.isRepeated('left')) { this._bx = Math.max(0, this._bx - 1); this.rubAt(this._bx, this._by, br); }
        if (Input.isRepeated('down')) { this._by = Math.min(G[1] - 1, this._by + 1); this.rubAt(this._bx, this._by, br); }
        if (Input.isRepeated('up')) { this._by = Math.max(0, this._by - 1); this.rubAt(this._bx, this._by, br); }
        if (Input.isTriggered('ok')) this.rubAt(this._bx, this._by, br + 1);
        var F = this.rubFrame();
        if (TouchInput.isPressed()) {
            var p = this.local();
            if (this.inside(F, p)) {
                this._bx = Math.floor((p.x - F.x) / F.w * G[0]); this._by = Math.floor((p.y - F.y) / F.h * G[1]);
                this.rubAt(this._bx, this._by, br + 1);
            } else if (TouchInput.isTriggered()) this.touchButtons();
        }
        if (!this._rubDone && this.isSolved()) {
            this._rubDone = true; this._rub = this._rub.map(function() { return true; });
            this.finish(true);
        }
    };
    Window_EscGame.prototype.draw_rub = function() {
        var c = this.contents, d = this._def, F = this.rubFrame(), G = this._rg, img = this._img, x, y;
        this.drawHeader();
        var ctx = ctxOf(c);
        ctx.fillStyle = d.paper || '#efe6cf'; ctx.fillRect(F.x, F.y, F.w, F.h);
        ctx.strokeStyle = 'rgba(120,96,60,0.35)'; ctx.lineWidth = 1;
        for (y = 1; y < 6; y++) { ctx.beginPath(); ctx.moveTo(F.x, F.y + F.h * y / 6); ctx.lineTo(F.x + F.w, F.y + F.h * y / 6 + 3); ctx.stroke(); }
        setDirty(c);
        if (img && img.isReady()) {
            var cw = F.iw / G[0], chh = F.ih / G[1], dw = F.w / G[0], dh = F.h / G[1];
            for (y = 0; y < G[1]; y++) for (x = 0; x < G[0]; x++) {
                if (!this._rub[y * G[0] + x]) continue;
                c.blt(img, x * cw, y * chh, cw, chh, F.x + x * dw, F.y + y * dh, dw + 0.6, dh + 0.6);
            }
        }
        if (!this._end) {
            var bx = F.x + (this._bx + 0.5) * F.w / G[0], by = F.y + (this._by + 0.5) * F.h / G[1];
            ctx.strokeStyle = 'rgba(255,214,90,0.95)'; ctx.lineWidth = 3; ctx.beginPath(); ctx.arc(bx, by, Math.max(10, F.w / G[0] * 2.4), 0, Math.PI * 2); ctx.stroke(); setDirty(c);
        }
        var pc = Math.round(this.rubCover() * 100), need = Math.round(Number(d.need || 0.82) * 100);
        c.fontSize = 16; c.textColor = '#ffe9b0';
        c.drawText('탁본 ' + Math.min(100, Math.round(pc / need * 100)) + '%', F.x, F.y - 24, F.w, 22, 'center');
        this.footer('마우스를 누른 채(손가락으로) 종이를 문질러요 · 키보드: 방향키로 먹방망이를 움직이며 문지르기');
        this.drawButtons('　', false);
    };

    // ----- drill (대열 훈련) ------------------------------------------------------------------
    Window_EscGame.prototype.drillStart = function() {
        return toArray(this._def.soldiers).map(function(s) { return [Number(s[0]), Number(s[1]), DIR4[s[2]] !== undefined ? DIR4[s[2]] : Number(s[2] || 0)]; });
    };
    Window_EscGame.prototype.drillCmd = function(pos, cmd) {
        var name = String(toArray(this._def.commands)[cmd] || ''), d = this._def, bad = -1, self = this;
        var out = pos.map(function(p) { return p.slice(); });
        out.forEach(function(p, i) {
            if (/우향우/.test(name)) p[2] = (p[2] + 1) % 4;
            else if (/좌향좌/.test(name)) p[2] = (p[2] + 3) % 4;
            else if (/뒤로/.test(name)) p[2] = (p[2] + 2) % 4;
            else if (/앞으로/.test(name)) {
                var n = /두/.test(name) ? 2 : 1;
                for (var k = 0; k < n; k++) {
                    p[0] += [0, 1, 0, -1][p[2]]; p[1] += [-1, 0, 1, 0][p[2]];
                    if (p[0] < 0 || p[1] < 0 || p[0] >= Number(d.cols) || p[1] >= Number(d.rows)) bad = i;
                    toArray(d.blocks).forEach(function(b) { if (Number(b[0]) === p[0] && Number(b[1]) === p[1]) bad = i; });
                }
            }
        });
        return { pos: out, bad: bad };
    };
    Window_EscGame.prototype.drillSim = function(prog) {
        var pos = this.drillStart(), bad = -1, at = -1;
        for (var k = 0; k < prog.length; k++) { var r = this.drillCmd(pos, prog[k]); pos = r.pos; if (r.bad >= 0) { bad = r.bad; at = k; break; } }
        return { pos: pos, bad: bad, at: at };
    };
    Window_EscGame.prototype.drillOk = function(pos) {
        var T = toArray(this._def.targets);
        return T.every(function(t) { return pos.some(function(p) { return p[0] === Number(t[0]) && p[1] === Number(t[1]); }); });
    };
    Window_EscGame.prototype.drillLayout = function() {
        var a = this.areaRect(84), d = this._def, cols = Number(d.cols), rows = Number(d.rows);
        var gw = a.w * 0.56, cs = Math.floor(Math.min(gw / cols, (a.h - 4) / rows)), grid = { x: a.x + (gw - cs * cols) / 2, y: a.y + (a.h - cs * rows) / 2, w: cs * cols, h: cs * rows, cs: cs };
        var px = a.x + gw + 16, pw = a.w - gw - 16, cmds = toArray(d.commands), P = [];
        for (var i = 0; i < cmds.length; i++) P.push({ x: px + (i % 2) * (pw / 2), y: a.y + 22 + Math.floor(i / 2) * 46, w: pw / 2 - 6, h: 40 });
        var max = Number(d.max || 8), sy = a.y + 22 + Math.ceil(cmds.length / 2) * 46 + 30, S = [], sw = (pw - 6) / 4;
        for (i = 0; i < max; i++) S.push({ x: px + (i % 4) * sw, y: sy + Math.floor(i / 4) * 44, w: sw - 6, h: 38 });
        var clr = { x: px, y: sy + Math.ceil(max / 4) * 44 + 4, w: pw - 6, h: 34 };
        return { grid: grid, pal: P, slots: S, clear: clr, slotY: sy };
    };
    Window_EscGame.prototype.update_drill = function() {
        var d = this._def, cmds = toArray(d.commands), np = cmds.length, L, i;
        if (this._run) {      // 구령 실행 (한 구령씩 천천히)
            var R = this._run;
            if (++R.t < 22) return;
            R.t = 0; R.k++;
            if (R.k >= this._prog.length) {
                this._run = null;
                if (this.drillOk(this._drPos)) { this.finish(true); return; }
                this.v46Fail('대열이 표시된 자리에 다 서지 않았어요.'); this._drPos = this.drillStart(); return;
            }
            var r = this.drillCmd(this._drPos, this._prog[R.k]); this._drPos = r.pos; SoundManager.playCursor();
            if (r.bad >= 0) { this._run = null; this.v46Fail((R.k + 1) + '번째 구령에서 병사가 ' + (toArray(d.blockWord)[0] || '깃대나 훈련장 밖') + '에 부딪혀 대열이 흩어졌어요!'); this._drPos = this.drillStart(); }
            return;
        }
        var n = np + 2;      // 구령 카드들 · 지우기 · 실행
        if (Input.isRepeated('right') || Input.isRepeated('down')) { this._cur = (this._cur + 1) % n; SoundManager.playCursor(); }
        if (Input.isRepeated('left') || Input.isRepeated('up')) { this._cur = (this._cur + n - 1) % n; SoundManager.playCursor(); }
        if (Input.isTriggered('ok')) {
            if (this._cur < np) this.drillAdd(this._cur);
            else if (this._cur === np) this.drillPop(-1);
            else this.submit();
        }
        if (TouchInput.isTriggered()) {
            var p = this.local(); L = this.drillLayout();
            for (i = 0; i < L.pal.length; i++) if (this.inside(L.pal[i], p)) { this._cur = i; this.drillAdd(i); return; }
            for (i = 0; i < L.slots.length; i++) if (this.inside(L.slots[i], p) && i < this._prog.length) { this.drillPop(i); return; }
            if (this.inside(L.clear, p)) { this._prog = []; this._drPos = this.drillStart(); SoundManager.playCancel(); return; }
            this.touchButtons();
        }
    };
    Window_EscGame.prototype.drillAdd = function(i) {
        if (this._prog.length >= Number(this._def.max || 8)) { SoundManager.playBuzzer(); this.say('구령 칸이 꽉 찼어요. 칸을 눌러 빼거나 [모두 지우기].', '#ffe9a8'); return; }
        this._prog.push(i); this._drPos = this.drillStart(); SoundManager.playOk();
    };
    Window_EscGame.prototype.drillPop = function(i) {
        if (!this._prog.length) { SoundManager.playBuzzer(); return; }
        if (i < 0) this._prog.pop(); else this._prog.splice(i, 1);
        this._drPos = this.drillStart(); SoundManager.playCancel();
    };
    Window_EscGame.prototype.draw_drill = function() {
        var c = this.contents, d = this._def, L = this.drillLayout(), g = L.grid, cs = g.cs, cmds = toArray(d.commands), i, x, y;
        this.drawHeader();
        var ctx = ctxOf(c);
        ctx.fillStyle = '#b89a6a'; ctx.fillRect(g.x, g.y, g.w, g.h);
        ctx.strokeStyle = 'rgba(80,60,30,0.45)'; ctx.lineWidth = 1;
        for (x = 0; x <= Number(d.cols); x++) { ctx.beginPath(); ctx.moveTo(g.x + x * cs, g.y); ctx.lineTo(g.x + x * cs, g.y + g.h); ctx.stroke(); }
        for (y = 0; y <= Number(d.rows); y++) { ctx.beginPath(); ctx.moveTo(g.x, g.y + y * cs); ctx.lineTo(g.x + g.w, g.y + y * cs); ctx.stroke(); }
        ctx.strokeStyle = '#ffe070'; ctx.lineWidth = 3; ctx.setLineDash && ctx.setLineDash([6, 4]);
        toArray(d.targets).forEach(function(t) { ctx.strokeRect(g.x + Number(t[0]) * cs + 4, g.y + Number(t[1]) * cs + 4, cs - 8, cs - 8); });
        ctx.setLineDash && ctx.setLineDash([]);
        toArray(d.blocks).forEach(function(b) {
            var bx = g.x + Number(b[0]) * cs, by = g.y + Number(b[1]) * cs;
            ctx.fillStyle = '#6a4a2a'; ctx.fillRect(bx + cs * 0.44, by + 4, cs * 0.12, cs - 8);
            ctx.fillStyle = '#c83a30'; ctx.beginPath(); ctx.moveTo(bx + cs * 0.56, by + 6); ctx.lineTo(bx + cs * 0.9, by + cs * 0.22); ctx.lineTo(bx + cs * 0.56, by + cs * 0.38); ctx.fill();
        });
        this._drPos.forEach(function(p, k) {
            var sx = g.x + (p[0] + 0.5) * cs, sy = g.y + (p[1] + 0.5) * cs, r = cs * 0.34;
            ctx.fillStyle = '#2c3a5a'; ctx.beginPath(); ctx.arc(sx, sy, r, 0, Math.PI * 2); ctx.fill();
            ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 2; ctx.stroke();
            var a = [-Math.PI / 2, 0, Math.PI / 2, Math.PI][p[2]];
            ctx.fillStyle = '#ffd860'; ctx.beginPath();
            ctx.moveTo(sx + Math.cos(a) * r * 1.25, sy + Math.sin(a) * r * 1.25);
            ctx.lineTo(sx + Math.cos(a + 2.4) * r * 0.7, sy + Math.sin(a + 2.4) * r * 0.7);
            ctx.lineTo(sx + Math.cos(a - 2.4) * r * 0.7, sy + Math.sin(a - 2.4) * r * 0.7); ctx.fill();
        });
        setDirty(c);
        toArray(d.blocks).forEach(function(b) { if (b[2]) { c.fontSize = 12; c.textColor = '#ffffff'; c.drawText(escSub(b[2]), g.x + Number(b[0]) * cs - 10, g.y + Number(b[1]) * cs + cs - 16, cs + 20, 16, 'center'); } });
        this._drPos.forEach(function(p, k) { c.fontSize = 13; c.textColor = '#ffffff'; c.drawText(String(k + 1), g.x + p[0] * cs, g.y + (p[1] + 0.5) * cs - 9, cs, 18, 'center'); });
        c.fontSize = 15; c.textColor = '#ffe9b0'; c.drawText('구령 카드 (눌러서 넣기)', L.pal[0].x, L.pal[0].y - 22, 300, 20, 'left');
        for (i = 0; i < cmds.length; i++) {
            var cur = this._cur === i && !this._end && !this._run;
            escBox(c, L.pal[i], 'rgba(246,236,206,0.97)', cur ? '#ffffff' : '#8a6a40', cur ? 3 : 1); escCardText(c, L.pal[i], escSub(cmds[i]), '#2a1a06', 16);
        }
        c.fontSize = 15; c.textColor = '#ffe9b0'; c.drawText('구령 순서 (칸을 누르면 빼기)', L.slots[0].x, L.slotY - 22, 300, 20, 'left');
        var runK = this._run ? this._run.k : -1;
        for (i = 0; i < L.slots.length; i++) {
            var has = i < this._prog.length;
            escBox(c, L.slots[i], has ? (i === runK ? 'rgba(255,214,100,0.98)' : 'rgba(220,232,250,0.95)') : 'rgba(255,255,255,0.08)', has ? '#5a6a8a' : 'rgba(255,255,255,0.25)', i === runK ? 3 : 1);
            if (has) escCardText(c, L.slots[i], (i + 1) + '. ' + escSub(cmds[this._prog[i]]), '#1a2238', 13);
            else { c.fontSize = 13; c.textColor = 'rgba(255,255,255,0.5)'; c.drawText(String(i + 1), L.slots[i].x, L.slots[i].y + 8, L.slots[i].w, 20, 'center'); }
        }
        var cc = this._cur === cmds.length && !this._end;
        escBox(c, L.clear, 'rgba(255,255,255,0.14)', cc ? '#ffffff' : 'rgba(255,255,255,0.4)', cc ? 3 : 1);
        c.fontSize = 15; c.textColor = '#ffffff'; c.drawText('모두 지우기 (마지막 하나 빼기: Enter)', L.clear.x, L.clear.y + 6, L.clear.w, 22, 'center');
        this.footer('병사들은 모두 같은 구령을 함께 따라요 · 노란 점선 칸에 모두 서게 하면 성공');
        this.drawButtons(d.okLabel || '구령 시작!', this._cur === cmds.length + 1 && !this._run);
    };

    // ----- weigh (저울 두 번) -------------------------------------------------------------------
    Window_EscGame.prototype.weighReset = function() {
        var n = Number(this._def.count || 9), i;
        this._pan = []; this._cand = []; for (i = 0; i < n; i++) { this._pan.push(0); this._cand.push(i); }
        this._used = 0; this._log = []; this._sel = -1; this._tilt = 0;
    };
    Window_EscGame.prototype.weighLayout = function() {
        var w = this.contentsWidth(), n = this._pan.length, bw = Math.min(70, (w - 40) / n - 8), x0 = (w - n * (bw + 8) + 8) / 2, y0 = 214, B = [];
        for (var i = 0; i < n; i++) B.push({ bag: { x: x0 + i * (bw + 8), y: y0, w: bw, h: 62 }, pick: { x: x0 + i * (bw + 8), y: y0 + 68, w: bw, h: 28 } });
        var by = y0 + 104, bt = [{ x: w / 2 - 250, y: by, w: 160, h: 36 }, { x: w / 2 - 80, y: by, w: 160, h: 36 }, { x: w / 2 + 90, y: by, w: 160, h: 36 }];
        return { bags: B, btns: bt, logY: by + 44 };
    };
    Window_EscGame.prototype.weighDo = function() {
        var L = [], R = [], i, self = this;
        for (i = 0; i < this._pan.length; i++) { if (this._pan[i] === 1) L.push(i); if (this._pan[i] === 2) R.push(i); }
        if (this._used >= Number(this._def.uses || 2)) { this.say('저울은 ' + (this._def.uses || 2) + '번만 쓸 수 있어요. 이제 자루를 골라요!', '#ffe9a8'); SoundManager.playBuzzer(); return; }
        if (!L.length || L.length !== R.length) { this.say('양쪽 접시에 같은 수의 자루를 올려야 공평하게 잴 수 있어요.', '#ffe9a8'); SoundManager.playBuzzer(); return; }
        var c = this._cand, cl = c.filter(function(k) { return L.indexOf(k) >= 0; }), cr = c.filter(function(k) { return R.indexOf(k) >= 0; }),
            co = c.filter(function(k) { return L.indexOf(k) < 0 && R.indexOf(k) < 0; });
        var res = 0, best = co;      // 0 수평 · -1 왼쪽 무거움 · 1 오른쪽 무거움 (가장 많이 남는 쪽을 고름)
        if (cl.length > best.length) { res = -1; best = cl; }
        if (cr.length > best.length) { res = 1; best = cr; }
        this._cand = best; this._used++; this._tilt = res;
        var nm = function(a) { return a.map(function(k) { return k + 1; }).join(','); };
        this._log.push(this._used + '번째: 왼쪽(' + nm(L) + ') ' + (res === 0 ? '＝ 수평 ＝' : res < 0 ? '＞ 왼쪽이 무거움' : '＜ 오른쪽이 무거움') + ' 오른쪽(' + nm(R) + ')');
        SoundManager.playOk();
    };
    Window_EscGame.prototype.update_weigh = function() {
        var n = this._pan.length, L, i;
        var rowLen = [n, n, 3];
        if (Input.isRepeated('down')) { this._row = (this._row + 1) % 3; this._cur = Math.min(this._cur, rowLen[this._row] - 1); SoundManager.playCursor(); }
        if (Input.isRepeated('up')) { this._row = (this._row + 2) % 3; this._cur = Math.min(this._cur, rowLen[this._row] - 1); SoundManager.playCursor(); }
        if (Input.isRepeated('right')) { this._cur = (this._cur + 1) % rowLen[this._row]; SoundManager.playCursor(); }
        if (Input.isRepeated('left')) { this._cur = (this._cur + rowLen[this._row] - 1) % rowLen[this._row]; SoundManager.playCursor(); }
        if (Input.isTriggered('ok')) this.weighPress(this._row, this._cur);
        if (TouchInput.isTriggered()) {
            var p = this.local(); L = this.weighLayout();
            for (i = 0; i < L.bags.length; i++) {
                if (this.inside(L.bags[i].bag, p)) { this._row = 0; this._cur = i; this.weighPress(0, i); return; }
                if (this.inside(L.bags[i].pick, p)) { this._row = 1; this._cur = i; this.weighPress(1, i); return; }
            }
            for (i = 0; i < 3; i++) if (this.inside(L.btns[i], p)) { this._row = 2; this._cur = i; this.weighPress(2, i); return; }
            this.touchButtons();
        }
    };
    Window_EscGame.prototype.weighPress = function(row, k) {
        if (row === 0) { this._pan[k] = (this._pan[k] + 1) % 3; SoundManager.playCursor(); }
        else if (row === 1) { this._sel = this._sel === k ? -1 : k; SoundManager.playCursor(); }
        else if (k === 0) this.weighDo();
        else if (k === 1) { this._pan = this._pan.map(function() { return 0; }); SoundManager.playCancel(); }
        else { SoundManager.playOk(); this.submit(); }
    };
    Window_EscGame.prototype.draw_weigh = function() {
        var c = this.contents, w = this.contentsWidth(), d = this._def, L = this.weighLayout(), i, self = this;
        this.drawHeader();
        var ctx = ctxOf(c), cx = w / 2, cy = 126, ang = this._tilt * 0.18;
        ctx.save(); ctx.translate(cx, cy);
        ctx.fillStyle = '#6a5030'; ctx.fillRect(-6, 0, 12, 62); ctx.fillRect(-40, 58, 80, 8);
        ctx.rotate(ang); ctx.fillStyle = '#c8a060'; ctx.fillRect(-170, -4, 340, 8);
        ctx.strokeStyle = '#8a6a40'; ctx.lineWidth = 2;
        [-150, 150].forEach(function(px) { ctx.beginPath(); ctx.moveTo(px, 0); ctx.lineTo(px - 30, 34); ctx.moveTo(px, 0); ctx.lineTo(px + 30, 34); ctx.stroke(); ctx.fillStyle = '#d8c8a0'; ctx.fillRect(px - 42, 34, 84, 8); });
        ctx.restore(); setDirty(c);
        var nl = 0, nr = 0; for (i = 0; i < this._pan.length; i++) { if (this._pan[i] === 1) nl++; if (this._pan[i] === 2) nr++; }
        c.fontSize = 15; c.textColor = '#ffe9b0';
        c.drawText('왼쪽 접시: ' + nl + '자루', cx - 260, cy + 50, 180, 20, 'center'); c.drawText('오른쪽 접시: ' + nr + '자루', cx + 80, cy + 50, 180, 20, 'center');
        c.fontSize = 16; c.textColor = this._used >= Number(d.uses || 2) ? '#ff9a8a' : '#ffffff';
        c.drawText('남은 저울질: ' + Math.max(0, Number(d.uses || 2) - this._used) + '번', 0, cy - 40, w, 20, 'center');
        for (i = 0; i < L.bags.length; i++) {
            var B = L.bags[i], pan = this._pan[i], cur0 = this._row === 0 && this._cur === i && !this._end, cur1 = this._row === 1 && this._cur === i && !this._end;
            var col = pan === 1 ? 'rgba(170,210,255,0.98)' : pan === 2 ? 'rgba(255,190,170,0.98)' : 'rgba(236,220,180,0.98)';
            escBox(c, B.bag, col, cur0 ? '#ffffff' : '#7a5a30', cur0 ? 3 : 1);
            c.fontSize = 18; c.textColor = '#2a1a06'; c.drawText((i + 1) + '번', B.bag.x, B.bag.y + 6, B.bag.w, 24, 'center');
            c.fontSize = 13; c.drawText(pan === 1 ? '왼쪽' : pan === 2 ? '오른쪽' : '내림', B.bag.x, B.bag.y + 34, B.bag.w, 20, 'center');
            var sel = this._sel === i;
            escBox(c, B.pick, sel ? 'rgba(255,214,90,0.98)' : 'rgba(255,255,255,0.1)', cur1 ? '#ffffff' : 'rgba(255,255,255,0.35)', cur1 ? 3 : 1);
            c.fontSize = 13; c.textColor = sel ? '#2a1a06' : '#ffffff'; c.drawText(sel ? '이 자루!' : '고르기', B.pick.x, B.pick.y + 4, B.pick.w, 20, 'center');
        }
        var labels = ['저울에 달아 보기', '접시 모두 비우기', '고른 자루로 정하기'];
        for (i = 0; i < 3; i++) {
            var cur2 = this._row === 2 && this._cur === i && !this._end;
            escBox(c, L.btns[i], i === 2 ? 'rgba(255,200,70,0.92)' : 'rgba(255,255,255,0.16)', cur2 ? '#ffffff' : 'rgba(255,255,255,0.45)', cur2 ? 3 : 1);
            c.fontSize = 16; c.textColor = i === 2 ? '#2a1a06' : '#ffffff'; c.drawText(labels[i], L.btns[i].x, L.btns[i].y + 6, L.btns[i].w, 24, 'center');
        }
        var y = L.logY;
        this._log.forEach(function(t) { c.fontSize = 15; c.textColor = '#d8f0ff'; escWrap(c, t, w - 40).forEach(function(l) { if (y < self.contentsHeight() - 120) c.drawText(l, 20, y, w - 40, 20, 'center'); y += 20; }); });
        this.footer('자루를 누르면 내림 → 왼쪽 → 오른쪽 · 자루 아래 [고르기]로 답 고르기 · 키보드: ↑↓ 줄, ← → 칸, Enter');
        this.drawButtons('　', false);
    };

    // ----- beacon (봉수) ---------------------------------------------------------------------
    Window_EscGame.prototype.litCount = function() { var n = 0; for (var i = 0; i < this._lit.length; i++) if (this._lit[i]) n++; return n; };
    Window_EscGame.prototype.beaconLayout = function() {
        var a = this.areaRect(84), d = this._def, n = this._lit.length, rw = Math.min(220, a.w * 0.3);
        var scene = { x: a.x, y: a.y + 70, w: a.w - rw - 12, h: a.h - 70 }, rules = { x: a.x + a.w - rw, y: a.y, w: rw, h: a.h };
        var T = [], cw = scene.w / n;
        for (var i = 0; i < n; i++) T.push({ x: scene.x + i * cw + cw * 0.18, y: scene.y + scene.h * 0.28, w: cw * 0.64, h: scene.h * 0.62 });
        return { text: { x: a.x, y: a.y, w: a.w - rw - 12, h: 62 }, scene: scene, rules: rules, fires: T };
    };
    Window_EscGame.prototype.update_beacon = function() {
        var n = this._lit.length;
        if (Input.isRepeated('right')) { this._cur = (this._cur + 1) % (n + 1); SoundManager.playCursor(); }
        if (Input.isRepeated('left')) { this._cur = (this._cur + n) % (n + 1); SoundManager.playCursor(); }
        if (Input.isTriggered('ok')) {
            if (this._cur === n) { SoundManager.playOk(); this.submit(); }
            else { this._lit[this._cur] = !this._lit[this._cur]; SoundManager.playCursor(); }
        }
        if (TouchInput.isTriggered()) {
            var p = this.local(), L = this.beaconLayout();
            for (var i = 0; i < L.fires.length; i++) if (this.inside(L.fires[i], p)) { this._cur = i; this._lit[i] = !this._lit[i]; SoundManager.playCursor(); return; }
            this.touchButtons();
        }
    };
    Window_EscGame.prototype.draw_beacon = function() {
        var c = this.contents, d = this._def, L = this.beaconLayout(), S = L.scene, rounds = toArray(d.rounds), R = rounds[Math.min(this._round, rounds.length - 1)], i, self = this;
        this.drawHeader();
        escBox(c, L.text, 'rgba(246,236,206,0.97)', '#c8a060', 2);
        c.fontSize = 14; c.textColor = '#7a2a18'; c.drawText('상황 ' + (this._round + 1) + ' / ' + rounds.length, L.text.x + 10, L.text.y + 4, 200, 18, 'left');
        var lines = escWrap(c, escSub(R.text), L.text.w - 20); c.fontSize = 16; lines = escWrap(c, escSub(R.text), L.text.w - 20);
        c.textColor = '#2a1a06'; for (i = 0; i < Math.min(2, lines.length); i++) c.drawText(lines[i], L.text.x + 10, L.text.y + 20 + i * 20, L.text.w - 20, 20, 'left');
        var ctx = ctxOf(c), grd = ctx.createLinearGradient(0, S.y, 0, S.y + S.h);
        grd.addColorStop(0, '#1c2440'); grd.addColorStop(1, '#3a3a4a'); ctx.fillStyle = grd; ctx.fillRect(S.x, S.y, S.w, S.h);
        ctx.fillStyle = '#2e3a2a'; ctx.beginPath(); ctx.moveTo(S.x, S.y + S.h); ctx.lineTo(S.x, S.y + S.h * 0.86);
        ctx.quadraticCurveTo(S.x + S.w / 2, S.y + S.h * 0.66, S.x + S.w, S.y + S.h * 0.86); ctx.lineTo(S.x + S.w, S.y + S.h); ctx.fill();
        L.fires.forEach(function(f, k) {
            var lit = self._lit[k], cur = self._cur === k && !self._end;
            var bx = f.x + f.w * 0.2, bw = f.w * 0.6, top = f.y + f.h * 0.38, bot = f.y + f.h * 0.92;
            ctx.fillStyle = '#8a8070'; ctx.fillRect(bx, top, bw, bot - top);
            ctx.fillStyle = '#6a6052'; for (var yy = top + 6; yy < bot; yy += 10) ctx.fillRect(bx, yy, bw, 2);
            ctx.fillStyle = '#5a5044'; ctx.fillRect(bx - 4, top - 6, bw + 8, 8);
            if (lit) {
                var fl = 0.8 + 0.2 * Math.sin((Graphics.frameCount + k * 13) / 5);
                ctx.fillStyle = 'rgba(255,150,40,0.95)'; ctx.beginPath(); ctx.moveTo(bx, top - 4); ctx.quadraticCurveTo(bx + bw / 2, top - f.h * 0.42 * fl, bx + bw, top - 4); ctx.fill();
                ctx.fillStyle = 'rgba(255,230,120,0.95)'; ctx.beginPath(); ctx.moveTo(bx + bw * 0.25, top - 4); ctx.quadraticCurveTo(bx + bw / 2, top - f.h * 0.24 * fl, bx + bw * 0.75, top - 4); ctx.fill();
                ctx.fillStyle = 'rgba(180,180,190,0.35)'; ctx.beginPath(); ctx.arc(bx + bw / 2, top - f.h * 0.5, bw * 0.45, 0, Math.PI * 2); ctx.fill();
            }
            if (cur) { ctx.strokeStyle = '#ffffff'; ctx.lineWidth = 3; ctx.strokeRect(f.x, f.y, f.w, f.h); }
        });
        setDirty(c);
        L.fires.forEach(function(f, k) { c.fontSize = 13; c.textColor = '#ffe9b0'; c.drawText((k + 1) + '번 굴뚝', f.x - 6, f.y + f.h - 4, f.w + 12, 18, 'center'); });
        c.fontSize = 16; c.textColor = '#ffffff'; c.drawText('지금 올린 봉수: ' + this.litCount() + '개', S.x, S.y + 6, S.w, 22, 'center');
        escBox(c, L.rules, 'rgba(246,236,206,0.95)', '#c8a060', 2);
        var y = L.rules.y + 8; c.fontSize = 16; c.textColor = '#7a2a18'; c.drawText(escSub(d.rulesTitle || '봉수 규칙'), L.rules.x, y, L.rules.w, 22, 'center'); y += 30;
        toArray(d.rules).forEach(function(t) { c.fontSize = 15; c.textColor = '#3a2a18'; escWrap(c, escSub(t), L.rules.w - 18).forEach(function(l) { c.drawText(l, L.rules.x + 9, y, L.rules.w - 18, 20, 'left'); y += 20; }); y += 6; });
        this.footer('굴뚝을 눌러 불을 켜고 끄기 · 키보드: ← → 고르기, Enter 켜기/끄기');
        this.drawButtons(d.okLabel || '봉수 올리기', this._cur === this._lit.length);
    };

    // ----- seat + 지도 그림 -------------------------------------------------------------------
    var _v46_drawSeat = Window_EscGame.prototype.draw_seat;
    Window_EscGame.prototype.draw_seat = function() {
        var d = this._def;
        if (d.image && this._img && this._img.isReady()) {
            var L = this.seatLayout(), tb = L.table, img = this._img, sc = Math.min(tb.w / img.width, tb.h / img.height);
            var fw = img.width * sc, fh = img.height * sc;
            this.contents.blt(img, 0, 0, img.width, img.height, tb.x + (tb.w - fw) / 2, tb.y + (tb.h - fh) / 2, fw, fh);
        }
        return _v46_drawSeat.apply(this, arguments);
    };

    //=========================================================================
    // 방 "push": 돌 밀기 (소코반)
    //=========================================================================
    var _v46_setupWatchers = EscapeManager.setupWatchers;
    EscapeManager.setupWatchers = function() {
        _v46_setupWatchers.apply(this, arguments);
        var room = this.currentRoom(), self = this;
        this._push = null; this._wtLast = null;
        if (!room || !room.push) return;
        var P = room.push, evs = [];
        toArray(P.stones).forEach(function(id) {
            var ev = $gameMap.events().filter(function(e) { return String(e.event().name).trim() === String(id); })[0];
            if (ev) evs.push(ev);
        });
        var home = evs.map(function(e) { return [e.x, e.y]; });
        this._push = { def: P, evs: evs, home: home, done: !!(P.flag && this._flags[P.flag]) };
        if (this._push.done) {
            toArray(P.targets).forEach(function(t, k) { if (evs[k]) evs[k].locate(Number(t[0]), Number(t[1])); });
        }
    };
    EscapeManager.pushOnTarget = function() {
        var P = this._push; if (!P) return false;
        var T = toArray(P.def.targets);
        return T.every(function(t) { return P.evs.some(function(e) { return e.x === Number(t[0]) && e.y === Number(t[1]); }); });
    };
    EscapeManager.pushReset = function() {
        var P = this._push; if (!P) return;
        P.evs.forEach(function(e, k) { e.locate(P.home[k][0], P.home[k][1]); });
    };
    var _v46_moveStraight = Game_Player.prototype.moveStraight;
    Game_Player.prototype.moveStraight = function(d) {
        var M = EscapeManager, P = M._push;
        if (P && !P.done && M.isActive() && M._phase === 'play' && !M.isBusy() && M.checkCond(P.def.when) && !this.isMoving()) {
            var x2 = $gameMap.roundXWithDirection(this.x, d), y2 = $gameMap.roundYWithDirection(this.y, d);
            var st = P.evs.filter(function(e) { return e.x === x2 && e.y === y2; })[0];
            if (st) {
                var x3 = $gameMap.roundXWithDirection(x2, d), y3 = $gameMap.roundYWithDirection(y2, d);
                var blockedByStone = P.evs.some(function(e) { return e !== st && e.x === x3 && e.y === y3; });
                if (!blockedByStone && st.canPass(x2, y2, d)) {
                    st.setMoveSpeed(4); st.setDirectionFix(true); st.moveStraight(d);
                    if (st.isMovementSucceeded()) {
                        $gameTemp.clearDestination();
                        if (!playSafeSe('Push', 70, 100)) SoundManager.playEquip();
                        _v46_moveStraight.call(this, d);
                        if (M.pushOnTarget()) {
                            P.done = true;
                            var steps = [];
                            if (P.def.flag) steps.push({ flag: P.def.flag });
                            steps = steps.concat(toArray(P.def.done));
                            M._waitCount = Math.max(M._waitCount || 0, 20);
                            M.insertSteps(steps);
                        }
                        return;
                    }
                }
                this.setDirection(d); this.checkEventTriggerTouchFront(d);
                return;
            }
        }
        return _v46_moveStraight.apply(this, arguments);
    };
    var _v46_processStep = EscapeManager.processStep;
    EscapeManager.processStep = function(s) {
        if (s && typeof s === 'object' && s.pushReset) {
            this.pushReset();
            if (s.text === undefined) return;
            s = this.stepWithout ? this.stepWithout(s, ['pushReset']) : s;
        }
        return _v46_processStep.call(this, s);
    };

    //=========================================================================
    // 방 "watchTurn": 차례 잠행 (주인공이 한 칸 가면 감시자도 한 칸)
    //=========================================================================
    var _v46_updWatch = EscapeManager.updateWatchers;
    EscapeManager.updateWatchers = function() {
        var room = this.currentRoom();
        if (!(room && room.watchTurn && this._watch)) return _v46_updWatch.apply(this, arguments);
        if (this.updateWalkers) this.updateWalkers();
        if (this._phase !== 'play' || this._cine || this._focus) return;
        if (!this.watchActive()) return;
        if ($gamePlayer.isTransferring() || this._waitTransfer) return;
        var frozen = this.isBusy() && !this._mission;
        var pk = $gamePlayer.x + ',' + $gamePlayer.y, self = this;
        if (this._wtLast === null || this._wtLast === undefined) this._wtLast = pk;
        if (this._watch.cool > 0) this._watch.cool--;
        if (!frozen && pk !== this._wtLast) {
            this._wtLast = pk;
            this._watch.list.forEach(function(w) {
                if (w.ev._erased || w.ev._escHidden) return;
                var route = toArray(w.def.route);
                if (!route.length) {
                    var dirs = toArray(w.def.look || [2, 4, 8, 6]);
                    w.idx = (w.idx + 1) % dirs.length; w.ev.setDirection(Number(dirs[w.idx])); return;
                }
                var tgt = route[w.idx % route.length];
                if (w.ev.x === Number(tgt[0]) && w.ev.y === Number(tgt[1])) { w.idx = (w.idx + 1) % route.length; tgt = route[w.idx]; }
                var dx = Number(tgt[0]) - w.ev.x, dy = Number(tgt[1]) - w.ev.y;
                var d = Math.abs(dx) >= Math.abs(dy) ? (dx > 0 ? 6 : 4) : (dy > 0 ? 2 : 8);
                if (dx === 0 && dy === 0) return;
                w.ev.setMoveSpeed(Number(w.def.speed || 4));
                w.ev.setThrough(true); w.ev.moveStraight(d); w.ev.setThrough(false);
                if (w.ev.x === Number(tgt[0]) && w.ev.y === Number(tgt[1])) {
                    var nx = route[(w.idx + 1) % route.length];
                    var ndx = Number(nx[0]) - w.ev.x, ndy = Number(nx[1]) - w.ev.y;
                    w.turnTo = Math.abs(ndx) >= Math.abs(ndy) ? (ndx > 0 ? 6 : 4) : (ndy > 0 ? 2 : 8);
                } else w.turnTo = 0;
            });
        }
        this._watch.list.forEach(function(w) { if (w.turnTo && !w.ev.isMoving()) { w.ev.setDirection(w.turnTo); w.turnTo = 0; } });
        if (frozen || this._watch.cool > 0) return;
        var px = $gamePlayer.x, py = $gamePlayer.y;
        for (var i = 0; i < this._watch.list.length; i++) {
            var w = this._watch.list[i];
            if (w.ev._erased || w.ev._escHidden) continue;
            var near = w.ev.x === px && w.ev.y === py;
            var seen = near || this.sightTiles(w).some(function(t) { return t[0] === px && t[1] === py; });
            if (seen) { this._wtLast = null; this.onCaught(w); return; }
        }
    };


    // v4.6: 게이지 모양 "style": "level" (온도 대신 0~최대 눈금, 단위 "unit")
    if (typeof Sprite_EscGauge !== 'undefined') {
        var _v46_gaugeRedraw = Sprite_EscGauge.prototype.redraw;
        Sprite_EscGauge.prototype.redraw = function() {
            var d = this._def;
            if (!d || d.style !== 'level') return _v46_gaugeRedraw.apply(this, arguments);
            var b = this.bitmap, mn = Number(d.min || 0), mx = Number(d.max || 10), v = this._val;
            b.clear();
            roundRect(b, 0, 0, 70, 230, 10, 'rgba(24,16,10,0.78)', 'rgba(230,190,120,0.7)', 2);
            b.fontSize = 12; b.textColor = '#ffe9b0'; b.drawText(d.label || '', 0, 4, 70, 18, 'center');
            var tx = 26, ty = 30, th = 166, f = Math.max(0, Math.min(1, (v - mn) / (mx - mn)));
            b.fillRect(tx, ty, 18, th, 'rgba(255,255,255,0.15)');
            var col = f < 0.4 ? '#7ad07a' : f < 0.7 ? '#f0c040' : '#e85a40';
            b.fillRect(tx + 2, ty + th * (1 - f), 14, th * f, col);
            for (var k = 1; k < 5; k++) b.fillRect(tx - 4, ty + th * k / 5, 6, 1, 'rgba(255,255,255,0.6)');
            b.fontSize = 14; b.textColor = '#ffffff'; b.drawText(f < 0.4 ? '차분' : f < 0.7 ? '팽팽' : '험악', 0, 204, 70, 20, 'center');
        };
    }

})();
