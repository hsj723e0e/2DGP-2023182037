"""소닉 애니메이션 뷰어: PRD의 단계별 구현."""

from pathlib import Path
from dataclasses import dataclass
import sys
from time import perf_counter
from math import isfinite

CANVAS_WIDTH = 1200
CANVAS_HEIGHT = 800
DISPLAY_SCALE = 4
ANCHOR_X = CANVAS_WIDTH // 2
ANCHOR_Y = CANVAS_HEIGHT // 2 - 80
FRAME_DURATION = 0.1
REPEAT_COUNT = 5
PAUSE_DURATION = 1.0
EDGE_MARGIN = 24
SPRITE_PATH = Path(__file__).resolve().with_name('sonic-sprite.png')


@dataclass(frozen=True)
class Frame:
    left: int
    top: int
    width: int
    height: int
    anchor_x: float | None = None
    anchor_y: float | None = None


@dataclass(frozen=True)
class Animation:
    name: str
    frames: tuple[Frame, ...]
    speed: float = 0.0  # 재생 중 이동 속도 (화면 픽셀/초), 0이면 제자리


ANIMATIONS = (
    Animation('걷기와 몸 낮추기', tuple(Frame(*rect) for rect in (
        (1, 39, 29, 39), (31, 40, 26, 38), (58, 39, 28, 39),
        (86, 40, 30, 38), (118, 40, 30, 38), (150, 40, 30, 38),
        (182, 40, 29, 38), (211, 39, 29, 38), (240, 39, 29, 38),
        (270, 45, 24, 32), (302, 51, 29, 26),
    )), speed=110.0),
    Animation('빠른 걷기', tuple(Frame(*rect) for rect in (
        (8, 80, 26, 37), (37, 80, 27, 37), (65, 80, 31, 38),
        (97, 80, 37, 37), (135, 80, 32, 35), (170, 79, 32, 38),
        (206, 79, 26, 38), (238, 80, 24, 37), (263, 80, 30, 37),
        (295, 80, 36, 37), (334, 80, 32, 36), (370, 79, 29, 38),
    )), speed=180.0),
    Animation('질주 자세', tuple(Frame(*rect) for rect in (
        (1, 124, 33, 40), (39, 124, 35, 39), (89, 125, 35, 38),
        (130, 121, 34, 42), (181, 122, 34, 41), (228, 122, 33, 40),
    )), speed=300.0),
    Animation('몸 말기', tuple(Frame(*rect, anchor_y=rect[3] / 2 + 20) for rect in (
        (1, 169, 29, 30), (35, 167, 29, 31), (67, 169, 30, 29),
        (98, 169, 31, 29), (131, 168, 29, 30), (162, 168, 29, 31),
        (193, 170, 30, 29), (230, 170, 31, 29), (268, 170, 30, 30),
    ))),
    Animation('구르기', tuple(Frame(*rect, anchor_y=rect[3] / 2 + 20) for rect in (
        (1, 206, 30, 27), (36, 206, 29, 27), (70, 206, 29, 27),
        (105, 206, 29, 27), (139, 206, 29, 27), (174, 206, 29, 27),
    )), speed=240.0),
    Animation('팔을 굽힌 질주', tuple(Frame(*rect) for rect in (
        (1, 239, 29, 35), (36, 239, 30, 35), (74, 239, 31, 35),
        (111, 238, 31, 36), (149, 239, 30, 35), (186, 238, 31, 36),
    )), speed=320.0),
    Animation('낮은 질주', tuple(
        Frame(*rect, anchor_x=rect[2] / 2 if index < 2 else rect[2] - 15)
        for index, rect in enumerate((
        (1, 283, 29, 35), (36, 283, 30, 35), (72, 286, 39, 31),
        (123, 285, 39, 32), (172, 286, 39, 31), (218, 285, 38, 32),
    ))), speed=360.0),
    Animation('세로 회전', tuple(Frame(*rect, anchor_y=rect[3] / 2 + 20) for rect in (
        (1, 326, 24, 45), (31, 327, 29, 44), (65, 327, 20, 44),
        (90, 327, 25, 43), (119, 327, 25, 43), (149, 327, 20, 44),
    ))),
    Animation('옆으로 눕는 자세', tuple(Frame(*rect, anchor_y=rect[3] / 2 + 20) for rect in (
        (184, 341, 40, 28), (232, 341, 39, 27),
    ))),
    Animation('앞을 향한 걷기', tuple(Frame(*rect) for rect in (
        (1, 379, 27, 38), (31, 379, 31, 36), (64, 379, 31, 36),
        (99, 377, 33, 38), (136, 379, 32, 36), (176, 379, 33, 36),
        (217, 379, 33, 36), (254, 378, 33, 36),
    )), speed=120.0),
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
    x: float = float(ANCHOR_X)
    y: float = float(ANCHOR_Y)
    direction: int = 1

    @property
    def animation(self):
        return self.animations[self.animation_index]

    @property
    def frame(self):
        return self.animation.frames[self.frame_index]

    def next_animation(self):
        self.animation_index = (self.animation_index + 1) % len(self.animations)
        self.frame_index = 0
        self.frame_elapsed = 0.0
        self.pause_elapsed = 0.0
        self.completed_repeats = 0
        self.state = 'playing'
        self.x = float(ANCHOR_X)
        self.y = float(ANCHOR_Y)
        self.direction = 1

    def move(self, elapsed):
        """프레임 전환 사이에도 경과 시간에 비례하여 이동한다."""
        if self.animation.speed == 0:
            return
        left, right = movement_bounds(self.animation)
        span = right - left
        offset = self.x - left
        phase = offset if self.direction == 1 else 2 * span - offset
        phase = (phase + self.animation.speed * elapsed) % (2 * span)
        if phase < span:
            self.x = left + phase
            self.direction = 1
        else:
            self.x = right - (phase - span)
            self.direction = -1

    def update(self, elapsed):
        """프레임·정지·동작 경계를 넘은 시간도 다음 상태에 반영한다."""
        if not isfinite(elapsed) or elapsed < 0:
            raise ValueError('경과 시간은 유한한 0 이상의 값이어야 합니다.')
        while elapsed > 0:
            if self.state == 'paused':
                remaining = PAUSE_DURATION - self.pause_elapsed
                if elapsed + 1e-12 < remaining:
                    self.pause_elapsed += elapsed
                    return
                elapsed = max(0.0, elapsed - remaining)
                self.next_animation()
                continue
            remaining = FRAME_DURATION - self.frame_elapsed
            if elapsed + 1e-12 < remaining:
                self.move(elapsed)
                self.frame_elapsed += elapsed
                return
            self.move(remaining)
            elapsed = max(0.0, elapsed - remaining)
            self.frame_elapsed = 0.0
            if self.frame_index == len(self.animation.frames) - 1:
                self.completed_repeats += 1
                if self.completed_repeats == REPEAT_COUNT:
                    self.state = 'paused'
                    self.pause_elapsed = 0.0
                else:
                    self.frame_index = 0
            else:
                self.frame_index += 1


def movement_bounds(animation):
    """전체 프레임과 좌우 반전의 폭을 고려한 안전 이동 구간."""
    radius = max(max(
        frame.width / 2 if frame.anchor_x is None else frame.anchor_x,
        frame.width / 2 if frame.anchor_x is None else frame.width - frame.anchor_x,
    ) * DISPLAY_SCALE for frame in animation.frames)
    left, right = EDGE_MARGIN + radius, CANVAS_WIDTH - EDGE_MARGIN - radius
    if left >= right or not left <= ANCHOR_X <= right:
        raise ValueError(f'{animation.name}: 프레임이 안전 이동 구간에 들어가지 않습니다.')
    return left, right


def draw_frame(sprite, frame, position_x=ANCHOR_X, position_y=ANCHOR_Y, direction=1):
    """위쪽 기준 원본 좌표를 pico2d 좌표로 바꾸어 출력한다."""
    bottom = sprite.h - frame.top - frame.height
    anchor_x = frame.width / 2 if frame.anchor_x is None else frame.anchor_x
    anchor_y = frame.height if frame.anchor_y is None else frame.anchor_y
    x = position_x + direction * (frame.width / 2 - anchor_x) * DISPLAY_SCALE
    y = position_y + (anchor_y - frame.height / 2) * DISPLAY_SCALE
    if direction == -1:
        sprite.clip_composite_draw(frame.left, bottom, frame.width, frame.height,
                                   0, 'h', x, y,
                                   frame.width * DISPLAY_SCALE, frame.height * DISPLAY_SCALE)
    else:
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
        if not isfinite(animation.speed) or animation.speed < 0:
            raise ValueError(f'{animation.name}: 이동 속도가 올바르지 않습니다.')
        for index, frame in enumerate(animation.frames, start=1):
            if (frame.left < 0 or frame.top < 0
                    or frame.width <= 0 or frame.height <= 0
                    or frame.left + frame.width > image_width
                    or frame.top + frame.height > image_height):
                raise ValueError(f'{animation.name} {index}번 프레임: 이미지 범위 오류 {frame}')
            for anchor in (frame.anchor_x, frame.anchor_y):
                if anchor is not None and not isfinite(anchor):
                    raise ValueError(f'{animation.name} {index}번 프레임: 기준점 오류')
        movement_bounds(animation)


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
    try:
        import pico2d
    except ImportError as error:
        print(f'pico2d 실행 환경을 확인해주세요: {error}', file=sys.stderr)
        return 1

    pico2d.open_canvas(CANVAS_WIDTH, CANVAS_HEIGHT)
    sprite = None
    try:
        pico2d.hide_lattice()
        try:
            sprite = load_sprite(pico2d)
            validate_animations(ANIMATIONS, sprite.w, sprite.h)
        except (OSError, ValueError) as error:
            print(error, file=sys.stderr)
            return 1
        run_viewer(pico2d, sprite)
    except KeyboardInterrupt:
        return 0
    finally:
        # SDL 렌더러를 닫기 전에 이미지의 텍스처를 해제한다.
        sprite = None
        pico2d.close_canvas()
    return 0


def run_viewer(pico2d, sprite):
    """재생·정지·전환 중 동일한 순서로 종료 이벤트를 처리한다."""
    player = Player()
    previous_time = perf_counter()
    while handle_events(pico2d):
        current_time = perf_counter()
        player.update(current_time - previous_time)
        previous_time = current_time
        pico2d.clear_canvas()
        draw_frame(sprite, player.frame, player.x, player.y, player.direction)
        pico2d.update_canvas()
        pico2d.delay(0.01)


if __name__ == '__main__':
    raise SystemExit(main())
