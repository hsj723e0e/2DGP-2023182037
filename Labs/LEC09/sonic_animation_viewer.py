"""소닉 애니메이션 뷰어: PRD의 단계별 구현."""

from pathlib import Path

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800
SPRITE_PATH = Path(__file__).resolve().with_name('sonic-sprite.png')


def load_sprite(pico2d):
    """작업 디렉터리와 관계없이 같은 폴더의 이미지를 읽는다."""
    return pico2d.load_image(str(SPRITE_PATH))


def handle_events(pico2d):
    """창 닫기 또는 Esc 입력이면 실행을 종료한다."""
    for event in pico2d.get_events():
        if event.type == pico2d.SDL_QUIT:
            return False
        if event.type == pico2d.SDL_KEYDOWN and event.key == pico2d.SDLK_ESCAPE:
            return False
    return True


def main():
    """직접 실행할 때만 뷰어를 시작한다."""
    import pico2d

    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    try:
        sprite = load_sprite(pico2d)
        while handle_events(pico2d):
            pico2d.clear_canvas()
            # 이미지 표시와 애니메이션은 이후 단계에서 추가한다.
            pico2d.update_canvas()
            pico2d.delay(0.01)
    finally:
        pico2d.close_canvas()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
