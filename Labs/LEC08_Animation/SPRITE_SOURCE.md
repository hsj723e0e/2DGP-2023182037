# Kyo animation viewer

- Source: https://spritedatabase.net/file/5276
- Original PNG: https://spritedatabase.net/files/neogeo/848/Sprite/Kyo02.png
- Game / character: The King of Fighters 2002 / Kyo Kusanagi
- Original game artwork: SNK; sprite sheet contributor: Ashimura.
- Sprite Database provides these materials for private or non-commercial use;
  the artwork remains the property of its original copyright holders.

## 실행

`python Labs/LEC08_Animation/animation_viewer.py`

실행에 필요한 외부 라이브러리는 기존 수업 코드와 같은 `pico2d`입니다.
VS Code에서 animation_viewer.py를 열고 Python 파일 실행 버튼으로 실행해도 됩니다.
이미지 경로는 소스 파일 기준이므로 작업 폴더에 영향을 받지 않습니다.
ESC 또는 창 닫기로 종료합니다.

## 구현 내용

- 걷기 11프레임 → 뛰기 6프레임 → 점프 8프레임 → 공격 10프레임.
- 각 동작은 5회 완전히 재생한 뒤 마지막 프레임에서 1초 정지합니다.
  이후 다음 동작으로 넘어가며, 공격 이후 다시 걷기로 무한 반복합니다.
- 원본의 각 프레임을 실제 그림 경계로 잘라 너비와 높이가 서로 다릅니다.
  `kyo_animation.json`의 프레임별 x, y, w, h로 시트를 잘라 그립니다.
- 1000×800 화면 중앙에 공통 5배 배율로 표시합니다.
  가장 작은 프레임도 높이 400픽셀로 화면 높이의 절반이며,
  가장 큰 프레임도 화면 안에 들어옵니다.
- 재생 시간은 실제 경과 시간으로 계산합니다.
- 원본 자홍색 배경을 투명하게 바꾸고 선택한 프레임을
  `kyo_animation.png`에 모았습니다. 원본은 `kyo_original.png`입니다.

`prepare_kyo_sheet.py`는 시트를 다시 만들 때만 사용하는 도구입니다.
이 도구에는 Pillow가 필요하며, 일반 뷰어 실행에는 필요하지 않습니다.

과제 제출 시 프레임별 가변 크기와 동작별 가변 프레임 수 지원을 설명하세요.
커밋 20개 이상 조건은 별도입니다. 이 구현은 자동으로 커밋을 만들지 않습니다.
