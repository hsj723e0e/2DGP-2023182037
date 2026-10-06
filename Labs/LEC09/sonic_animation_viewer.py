"""소닉 애니메이션 뷰어: PRD의 단계별 구현."""

from pathlib import Path
from dataclasses import dataclass
import sys
from time import perf_counter

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800
DISPLAY_SCALE = 4
ANCHOR_X = CANVAS_WIDTH // 2
ANCHOR_Y = CANVAS_HEIGHT // 2 - 80
FRAME_DURATION = 0.1
REPEAT_COUNT = 5
PAUSE_DURATION = 1.0
SPRITE_PATH = Path(__file__).resolve().with_name('sonic-sprite.png')


@dataclass(frozen=True)
class Frame:
    left: int
    top: int
    width: int
    height: int
    anchor_x: float | None = None
    anchor_y: float | None = None


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
    Animation('빠른 걷기', tuple(Frame(*rect) for rect in (
        (8, 80, 26, 37), (37, 80, 27, 37), (65, 80, 31, 38),
        (97, 80, 37, 37), (135, 80, 32, 35), (170, 79, 32, 38),
        (206, 79, 26, 38), (238, 80, 24, 37), (263, 80, 30, 37),
        (295, 80, 36, 37), (334, 80, 32, 36), (370, 79, 29, 38),
    ))),
    Animation('질주 자세', tuple(Frame(*rect) for rect in (
        (1, 124, 33, 40), (39, 124, 35, 39), (89, 125, 35, 38),
        (130, 121, 34, 42), (181, 122, 34, 41), (228, 122, 33, 40),
    ))),
    Animation('몸 말기', tuple(Frame(*rect) for rect in (
        (1, 169, 29, 30), (35, 168, 29, 30), (67, 169, 30, 29),
        (98, 169, 31, 29), (131, 168, 29, 30), (162, 168, 29, 31),
        (193, 170, 30, 29), (230, 170, 31, 29), (268, 170, 30, 30),
    ))),
    Animation('구르기', tuple(Frame(*rect) for rect in (
        (1, 206, 30, 27), (36, 206, 29, 27), (70, 206, 29, 27),
        (105, 206, 29, 27), (139, 206, 29, 27), (174, 206, 29, 27),
    ))),
    Animation('팔을 굽힌 질주', tuple(Frame(*rect) for rect in (
        (1, 239, 29, 35), (36, 239, 30, 35), (74, 239, 31, 35),
        (111, 238, 31, 36), (149, 239, 30, 35), (186, 238, 31, 36),
    ))),
    Animation('낮은 질주', tuple(Frame(*rect) for rect in (
        (1, 283, 29, 35), (36, 283, 30, 35), (72, 286, 39, 31),
        (123, 285, 39, 32), (172, 286, 39, 31), (218, 285, 38, 32),
    ))),
    Animation('세로 회전', tuple(Frame(*rect) for rect in (
        (1, 326, 24, 45), (31, 327, 29, 44), (65, 327, 20, 44),
        (90, 327, 25, 43), (119, 327, 25, 43), (149, 327, 20, 44),
    ))),
    Animation('옆으로 눕는 자세', tuple(Frame(*rect) for rect in (
        (184, 341, 40, 28), (232, 341, 39, 27),
    ))),
    Animation('앞을 향한 걷기', tuple(Frame(*rect) for rect in (
        (1, 379, 27, 38), (31, 379, 31, 36), (64, 379, 31, 36),
        (99, 378, 33, 37), (136, 379, 32, 36), (176, 379, 33, 36),
        (217, 379, 33, 36), (254, 378, 33, 36),
    ))),
    Animation('팔 들기', tuple(Frame(*rect) for rect in (
        (6, 429, 34, 40), (49, 426, 34, 43),
    ))),
    Animation('정지 자세', tuple(Frame(*rect) for rect in (
        (96, 427, 23, 39), (125, 427, 23, 39),
    ))),
)


@dataclass
class Player:
    animations: tuple[Animation, ...] = ANIMATIONS
    animation_index: int = 0
    frame_index: int = 0
    frame_elapsed: float = 0.0
    completed_repeats: int = 0
    state: str = 'playing'
    pause_elapsed: float = 0.0

    @property
    def animation(self):
        return self.animations[self.animation_index]

    @property
    def frame(self):
        return self.animation.frames[self.frame_index]

    def next_animation(self):
        if self.animation_index + 1 >= len(self.animations):
            self.state = 'ready'
            return
        self.animation_index += 1
        self.frame_index = 0
        self.frame_elapsed = 0.0
        self.pause_elapsed = 0.0
        self.completed_repeats = 0
        self.state = 'playing'

    def update(self, elapsed):
        if self.state == 'paused':
            self.pause_elapsed += elapsed
            if self.pause_elapsed + 1e-12 >= PAUSE_DURATION:
                self.next_animation()
            return
        if self.state != 'playing':
            return
        self.frame_elapsed += elapsed
        while self.frame_elapsed + 1e-12 >= FRAME_DURATION:
            self.frame_elapsed -= FRAME_DURATION
            if self.frame_index == len(self.animation.frames) - 1:
                self.completed_repeats += 1
                if self.completed_repeats == REPEAT_COUNT:
                    self.state = 'paused'
                    self.pause_elapsed = 0.0
                    break
                self.frame_index = 0
            else:
                self.frame_index += 1


def draw_frame(sprite, frame):
    """위쪽 기준 원본 좌표를 pico2d 좌표로 바꾸어 출력한다."""
    bottom = sprite.h - frame.top - frame.height
    anchor_x = frame.width / 2 if frame.anchor_x is None else frame.anchor_x
    anchor_y = frame.height if frame.anchor_y is None else frame.anchor_y
    x = ANCHOR_X + (frame.width / 2 - anchor_x) * DISPLAY_SCALE
    y = ANCHOR_Y + (anchor_y - frame.height / 2) * DISPLAY_SCALE
    sprite.clip_draw(frame.left, bottom, frame.width, frame.height,
                     x, y,
                     frame.width * DISPLAY_SCALE, frame.height * DISPLAY_SCALE)


def load_sprite(pico2d):
    """작업 디렉터리와 관계없이 같은 폴더의 이미지를 읽는다."""
    if not SPRITE_PATH.is_file():
        raise FileNotFoundError(f'스프라이트 파일을 찾을 수 없습니다: {SPRITE_PATH}')
    try:
        return pico2d.load_image(str(SPRITE_PATH))
    except OSError as error:
        raise OSError(f'스프라이트 이미지를 읽을 수 없습니다: {SPRITE_PATH} ({error})') from error


def validate_animations(animations, image_width, image_height):
    """빈 동작과 이미지 범위를 벗어나는 프레임을 실행 전에 검출한다."""
    if not animations:
        raise ValueError('재생할 동작이 없습니다.')
    for animation in animations:
        if not animation.frames:
            raise ValueError(f'{animation.name}: 프레임이 없습니다.')
        for index, frame in enumerate(animation.frames, start=1):
            if (frame.left < 0 or frame.top < 0
                    or frame.width <= 0 or frame.height <= 0
                    or frame.left + frame.width > image_width
                    or frame.top + frame.height > image_height):
                raise ValueError(f'{animation.name} {index}번 프레임: 이미지 범위 오류 {frame}')


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
            validate_animations(ANIMATIONS, sprite.w, sprite.h)
        except (OSError, ValueError) as error:
            print(error, file=sys.stderr)
            return 1
        player = Player()
        previous_time = perf_counter()
        while handle_events(pico2d):
            current_time = perf_counter()
            player.update(current_time - previous_time)
            previous_time = current_time
            pico2d.clear_canvas()
            draw_frame(sprite, player.frame)
            pico2d.update_canvas()
            pico2d.delay(0.01)
    finally:
        pico2d.close_canvas()
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
