"""시간의 문 - 한 번에 만들기
사용법:  python build_all.py <MV 프로젝트 폴더> [단계 ...]
  단계를 적지 않으면 전부 만듭니다. 일부만: python build_all.py 프로젝트 rooms data
  단계: chars closeups icons review rooms maps data title music intro
필요: Python 3, pip install pillow numpy scipy segno, 그리고 ffmpeg (music/intro 단계)
"""
import os, sys, subprocess, tempfile, shutil, glob

HERE = os.path.dirname(os.path.abspath(__file__))
REVIEW_URL = 'https://forms.gle/a4upZPjJ71bLr1by6'
ORDER = ['chars', 'closeups', 'icons', 'review', 'rooms', 'maps', 'data', 'title', 'music', 'intro']

def run(*args):
    print('  >', ' '.join(os.path.basename(a) if i == 0 else a for i, a in enumerate(args)))
    subprocess.run([sys.executable] + list(args), check=True, cwd=HERE)

def main():
    if len(sys.argv) < 2:
        print(__doc__); return
    root = os.path.abspath(sys.argv[1])
    steps = sys.argv[2:] or ORDER
    tmp = tempfile.mkdtemp(prefix='timegate_')
    P = lambda *a: os.path.join(root, *a)
    for st in ORDER:
        if st not in steps: continue
        print('[%s]' % st)
        if st == 'chars':    run(os.path.join(HERE, 'hd_chars.py'), P('img', 'characters'), tmp)
        if st == 'closeups': run(os.path.join(HERE, 'make_closeups.py'), P('img', 'pictures'))
        if st == 'icons':    run(os.path.join(HERE, 'hd_icons.py'), P('img', 'pictures'))
        if st == 'review':   run(os.path.join(HERE, 'make_review.py'), REVIEW_URL, P('img', 'pictures', 'cu_review.png'))
        if st == 'rooms':    run(os.path.join(HERE, 'hd_wide.py'), P('img', 'parallaxes'))
        if st == 'maps':     run(os.path.join(HERE, 'wide_maps.py'), root)
        if st == 'data':     run(os.path.join(HERE, 'build_data.py'), P('data', 'EscapeData.json'))
        if st == 'title':    run(os.path.join(HERE, 'hd_title.py'), root)
        if st == 'music':
            wav = os.path.join(tmp, 'music')
            run(os.path.join(HERE, 'make_music.py'), wav)
            os.makedirs(P('audio', 'bgm'), exist_ok=True)
            for w in glob.glob(os.path.join(wav, '*.wav')):
                name = os.path.splitext(os.path.basename(w))[0]
                subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', w, '-c:a', 'libvorbis', '-q:a', '5', P('audio', 'bgm', name + '.ogg')], check=True)
                subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-i', w, '-c:a', 'aac', '-b:a', '160k', P('audio', 'bgm', name + '.m4a')], check=True)
                print('    bgm', name)
        if st == 'intro':    run(os.path.join(HERE, 'make_intro.py'), root, tmp)
    shutil.rmtree(tmp, ignore_errors=True)
    print('완료:', root)

if __name__ == '__main__':
    main()
