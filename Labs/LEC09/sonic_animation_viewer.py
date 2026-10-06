"""소닉 애니메이션 뷰어: PRD의 단계별 구현."""

from pathlib import Path
from dataclasses import dataclass
import sys

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800
SPRITE_PATH = Path(__file__).resolve().with_name('sonic-sprite.png')


@dataclass(frozen=True)
class Frame:
    left: int
    top: int
    width: int
    height: int


FIRST_FRAME = Frame(1, 39, 29, 39)


@dataclass(frozen=True)
class Animation:
    name: str
    frames: tuple[Frame, ...]


ANIMATIONS = (
    Animation('걷기와 몸 낮추기', tuple(Frame(*rect) for rect in (
        (1, 39, 29, 39), (31, 40, 26, 38), (58, 39, 29, 39),
        (87, 40, 29, 38), (118, 40, 30, 38), (150, 40, 30, 38),
        (182, 40, 30, 38), (212, 39, 29, 38), (241, 39, 28, 38),
        (270, 45, 24, 32), (302, 51, 29, 26),
    ))),
)


def draw_frame(sprite, frame):
    """위쪽 기준 원본 좌표를 pico2d 좌표로 바꾸어 출력한다."""
    bottom = sprite.h - frame.top - frame.height
    sprite.clip_draw(frame.left, bottom, frame.width, frame.height,
                     CANVAS_WIDTH // 2, CANVAS_HEIGHT // 2)


def load_sprite(pico2d):
    """작업 디렉터리와 관계없이 같은 폴더의 이미지를 읽는다."""
    if not SPRITE_PATH.is_file():
        raise FileNotFoundError(f'스프라이트 파일을 찾을 수 없습니다: {SPRITE_PATH}')
    try:
        return pico2d.load_image(str(SPRITE_PATH))
    except OSError as error:
        raise OSError(f'스프라이트 이미지를 읽을 수 없습니다: {SPRITE_PATH} ({error})') from error


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
        try:
            sprite = load_sprite(pico2d)
        except OSError as error:
            print(error, file=sys.stderr)
            return 1
        while handle_events(pico2d):
            pico2d.clear_canvas()
            draw_frame(sprite, ANIMATIONS[0].frames[0])
            pico2d.update_canvas()
            pico2d.delay(0.01)
    finally:
        pico2d.close_canvas()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
