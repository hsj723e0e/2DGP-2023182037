# 소닉 애니메이션 뷰어

Python과 pico2d로 만든 자동 재생 뷰어다. `sonic-sprite.png`의 소닉 12개 동작 묶음, 76프레임을 4배 확대하여 보여준다.

## 실행

Python 3.10 이상과 pico2d 실행 환경이 필요하다. 개발 검증은 Windows의 Python 3.13.15에서 진행했다. 소스와 `sonic-sprite.png`를 같은 폴더에 둔다.

저장소 루트에서:

```powershell
python Labs/LEC09/sonic_animation_viewer.py
```

이미 `Labs/LEC09` 폴더에 있다면:

```powershell
python sonic_animation_viewer.py
```

## 동작

- 1200 × 800 창에서 자동으로 첫 동작을 재생한다.
- 프레임당 0.1초로 각 동작을 5회 재생한다.
- 마지막 프레임에서 1초 쉬고 다음 동작으로 전환한다.
- 마지막 동작 다음에는 첫 동작으로 돌아가 계속 반복한다. 전체 한 순환은 50초다.
- 첫 동작의 재생은 5.5초이며, 정지를 포함해 실행 후 약 6.5초에 두 번째 동작으로 넘어간다.
- Esc 또는 창 닫기로 종료한다.

화면과 배율, 재생 시간은 Python 파일 상단의 `CANVAS_WIDTH`, `CANVAS_HEIGHT`, `DISPLAY_SCALE`, `FRAME_DURATION`, `REPEAT_COUNT`, `PAUSE_DURATION` 상수로 정의한다. 변경하면 PRD의 요구사항 및 검증 기준과 일치하는지 확인한다.

## 개발 및 검증

- [요구사항과 단계별 커밋 기록](PRD.md)
- [검증 결과](VALIDATION.md)

실제 창에서 두 번 순환하고 24회 정지하는 것을 검증했다. 최대 정지 시간 오차는 0.0098초였다. 3~24단계는 한글 커밋 메시지로 기록한다.

```powershell
git log --oneline -- Labs/LEC09
```

이미지를 찾을 수 없으면 같은 폴더의 파일명과 위치를 확인한다. pico2d 관련 오류가 나오면 사용 중인 Python 환경에 pico2d와 필요한 SDL 실행 환경이 준비되어 있는지 확인한다.
