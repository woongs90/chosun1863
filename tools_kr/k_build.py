"""척화비 아래에서 한 번에 만들기
 python tools_kr/k_build.py <MV 프로젝트 폴더> [--no-movie] [--no-music]
 순서: 인물 → 초상화 → 지도 9장 → 카드 → 데이터 → 타이틀 → 음악 → 인트로 영상
"""
import os, sys, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)

def run(script, *args):
    print('>>', script, *args)
    subprocess.run([sys.executable, os.path.join(HERE, script)] + list(args), check=True)

if __name__ == '__main__':
    root = sys.argv[1]; opts = sys.argv[2:]
    run('k_chars.py', os.path.join(root, 'img', 'characters'))
    run('k_portraits.py', os.path.join(root, 'img', 'pictures'))
    run('k_mg.py', root)
    run('k_cards.py', root)
    run('k_data.py', root)
    run('k_title.py', root)
    if '--no-music' not in opts: run('k_music.py', root)
    if '--no-movie' not in opts: run('k_intro.py', root)
    print('완료:', root)
