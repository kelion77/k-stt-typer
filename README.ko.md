# STT Typer - Whisper.cpp

Mac에서 **단축키 하나로** 음성을 텍스트로 변환하는 도구 - 99개 이상 언어 지원

> 이 프로젝트는 [vertuzz/stt-typer](https://github.com/vertuzz/stt-typer)와 [whisper.cpp](https://github.com/ggml-org/whisper.cpp)를 기반으로 만들어졌습니다.

**[English Documentation](README.md)**

## 특징

- **이중 단축키**: `⌃⌥Space` 또는 `⇧⌘,` - 편한 키를 선택하세요
- **완전 무료**: Whisper.cpp 로컬 실행, API 비용 없음
- **프라이버시**: 모든 처리가 로컬에서, 인터넷 불필요
- **다국어 지원**: 99개 이상 언어 지원 (한국어, 영어, 일본어, 중국어 등)
- **GPU 가속**: Apple Silicon (M1/M2/M3/M4) Metal 자동 활성화
- **자동 붙여넣기**: 커서 위치에 자동 입력

## 빠른 시작

### 사전 요구사항

설치 전에 다음을 준비해주세요:

1. **Homebrew** 설치 ([https://brew.sh](https://brew.sh))
   ```bash
   /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
   ```

2. **PortAudio** 라이브러리 (PyAudio에 필수)
   ```bash
   brew install portaudio
   ```

3. **uv** 패키지 매니저 (없으면 자동 설치됨)
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```

### 설치

```bash
# 저장소 클론
git clone https://github.com/kelion77/k-stt-typer.git
cd k-stt-typer

# Python 의존성 설치 (uv가 없으면 자동 설치됨)
# "command not found: uv" 에러가 나면: $HOME/.local/bin/uv sync 실행
uv sync

# Whisper.cpp + 모델 설치
./install_whisper.sh

# Hammerspoon (단축키) 설치
./setup_global_hotkey.sh
```

### 권한 설정

#### 1. 접근성 권한 (필수)
Hammerspoon 실행 시 **접근성 권한** 부여:
- 시스템 설정 → 개인 정보 보호 및 보안 → 손쉬운 사용
- **Hammerspoon** 찾아서 활성화
- 자물쇠 아이콘을 클릭해 변경 권한 필요할 수 있음

#### 2. 마이크 권한 (필수)
음성 녹음을 위해 **마이크 권한** 부여:
- 시스템 설정 → 개인 정보 보호 및 보안 → 마이크
- **Python** 또는 **터미널** 활성화 (실행 방식에 따라)
- "is a is is" 같은 이상한 결과가 나온다면 이 권한을 먼저 확인하세요

#### 3. Hammerspoon 실행
설치 후 Hammerspoon이 자동으로 실행됩니다. 안 되면:
```bash
open -a Hammerspoon
```
메뉴 바에서 Hammerspoon 아이콘(🔨)을 확인하세요.

### 사용

```
1. 아무 앱에서나 (VS Code, Notes, Chrome 등)
2. ⌃⌥Space 또는 ⇧⌘, 한 번 → 녹음 시작
3. 한국어로 말하기 (예: "안녕하세요")
4. 같은 단축키 다시 → 자동으로 입력됨!
```

**사용 가능한 단축키:**
- `⌃⌥Space` (Control + Option + Space) - 주 단축키
- `⇧⌘,` (Shift + Command + Period) - 보조 단축키

## 작동 방식

```
⌃⌥Space (Hammerspoon)
  ↓
toggle_whisper.sh
  ↓
main_whisper.py (녹음)
  ↓
⌃⌥Space (중지)
  ↓
Whisper.cpp (한글 전사)
  ↓
pynput (Cmd+V 자동 실행)
  ↓
커서 위치에 입력!
```

## 주요 파일

```
k-stt-typer/
├── main_whisper.py           # 메인 앱 (녹음 + 전사 + 붙여넣기)
├── whisper_transcriber.py    # Whisper.cpp 통합 모듈
├── toggle_whisper.sh         # 토글 스크립트
├── install_whisper.sh        # Whisper.cpp 설치
├── setup_global_hotkey.sh    # Hammerspoon 설치
└── whisper.cpp/              # Whisper.cpp (로컬 STT)
    ├── models/
    │   ├── ggml-base.bin           # Whisper 모델 (141MB)
    │   └── ggml-silero-v5.1.2.bin  # VAD 모델
    └── build/bin/whisper-cli       # CLI 도구
```

## 단축키 변경

기본 단축키는 `⌃⌥Space` (Control + Option + Space)입니다. 변경하려면:

1. **Hammerspoon 설정 파일 열기**:
   ```bash
   open ~/.hammerspoon/init.lua
   ```

2. **단축키 바인딩 수정** (8번째 줄 근처):
   ```lua
   -- 현재: Ctrl + Alt + Space
   hs.hotkey.bind({"ctrl", "alt"}, "space", function()

   -- 예시:
   -- Ctrl + Alt + . (마침표)
   hs.hotkey.bind({"ctrl", "alt"}, ".", function()

   -- Cmd + Shift + Space
   hs.hotkey.bind({"cmd", "shift"}, "space", function()

   -- F13 키 (수식키 없이)
   hs.hotkey.bind({}, "f13", function()
   ```

3. **Hammerspoon 재시작**:
   ```bash
   killall Hammerspoon && open -a Hammerspoon
   ```

### 사용 가능한 수식키
- `cmd` - Command (⌘)
- `ctrl` - Control (⌃)
- `alt` - Option (⌥)
- `shift` - Shift (⇧)
- 여러 개 조합: `{"cmd", "shift", "ctrl"}`

### 사용 가능한 키
- 문자: `"a"`, `"b"`, `"c"` 등
- 펑션키: `"f1"`, `"f2"`, ..., `"f20"`
- 특수키: `"space"`, `"return"`, `"escape"`, `"tab"`
- 전체 목록: [Hammerspoon 키 코드](https://www.hammerspoon.org/docs/hs.hotkey.html)

## 언어 설정

언어는 [main_whisper.py:70](main_whisper.py#L70)에서 설정됩니다.

### 현재 설정: 한국어
```python
recorder = WhisperRecorder(language="ko")
```

### 언어 변경 방법

[main_whisper.py](main_whisper.py) 파일을 수정하세요:

```python
# 영어 전용
recorder = WhisperRecorder(language="en")

# 자동 감지 (다국어 사용자에게 추천)
recorder = WhisperRecorder(language="auto")

# 일본어
recorder = WhisperRecorder(language="ja")

# 중국어
recorder = WhisperRecorder(language="zh")
```

### 중요 사항

1. **언어 고정 모드** (`language="ko"`):
   - Whisper가 항상 한국어로 전사 시도
   - 영어로 말해도 → 한국어 음성 전사 (부정확)
   - 단일 언어 사용 시 빠르고 정확

2. **자동 감지 모드** (`language="auto"`):
   - Whisper가 말한 언어를 자동으로 감지
   - 다국어 사용자에게 적합
   - 언어 고정 모드보다 약간 느림

3. **번역은 지원되지 않습니다**:
   - Whisper는 말한 언어 그대로 전사합니다
   - 한국어로 말하기 → 한국어 텍스트만 가능
   - 영어로 말하기 → 영어 텍스트만 가능
   - 한국어 음성을 영어 텍스트로 변환 불가능

### 지원 언어

Whisper는 99개 이상의 언어를 지원합니다:
- 한국어(ko), 영어(en), 일본어(ja), 중국어(zh)
- 스페인어(es), 프랑스어(fr), 독일어(de), 러시아어(ru)
- 그 외 다수...

전체 목록은 [whisper.cpp 언어 코드](https://github.com/ggml-org/whisper.cpp)를 참조하세요.

## 사용 예시

### VS Code에서 주석 작성
```
1. 코드에서 주석 위치에 커서
2. ⌃⌥Space
3. "이 함수는 사용자 인증을 처리합니다"
4. ⌃⌥Space
→ // 이 함수는 사용자 인증을 처리합니다
```

### Notes에서 긴 문장
```
1. ⌃⌥Space
2. "오늘 할 일은 프로젝트 문서 작성하고, 팀 미팅 참석하고, 코드 리뷰 완료하기"
3. ⌃⌥Space
→ 전체 문장 자동 입력!
```

## 문제 해결

### 이상한 텍스트가 나올 때 (예: "is a is is is")

음성 대신 무의미한 텍스트가 출력되면:

1. **마이크 권한 확인** (가장 흔한 원인)
   - 시스템 설정 → 개인 정보 보호 및 보안 → 마이크
   - **Python** 또는 **터미널** 활성화
   - 권한 부여 후 앱 재시작

2. **마이크 작동 확인**
   - 음성 메모 앱에서 녹음 테스트
   - 시스템 설정 → 사운드 → 입력에서 입력 레벨 확인

3. **로그 확인**
   ```bash
   tail -f /tmp/stt_whisper.log
   ```

### 설치 문제

#### `command not found: uv`
uv 패키지 매니저를 PATH에서 찾을 수 없습니다. 전체 경로로 실행:
```bash
$HOME/.local/bin/uv sync
```

또는 PATH에 추가:
```bash
echo 'export PATH="$HOME/.local/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

#### `fatal error: 'portaudio.h' file not found`
PortAudio 라이브러리가 없어 PyAudio 빌드 실패:
```bash
brew install portaudio
uv sync  # 재시도
```

### 성능 문제 (인텔 맥)

**참고**: 이 도구는 Apple Silicon Mac (M1/M2/M3/M4)에서 Metal GPU 가속으로 최적의 성능을 발휘합니다.

**인텔 맥**에서 전사가 느리다면:
- CPU 전용 처리로 느림 (Metal GPU 미지원)
- `small` 대신 `base` 모델 사용 권장 (더 빠름)
- 전사 시간이 1-2초 대신 5-10초 걸릴 수 있음

base 모델로 전환:
```bash
# 1. base 모델 다운로드
cd whisper.cpp
bash ./models/download-ggml-model.sh base

# 2. whisper_transcriber.py 27번째 줄 수정
# 변경: WHISPER_MODEL = WHISPER_CPP_DIR / "models" / "ggml-base.bin"
```

### 마이크 아이콘이 계속 켜져 있을 때

주황색 마이크가 녹음 중지 후에도 사라지지 않으면:

```bash
# 긴급 정지 스크립트 실행
./stop_all.sh
```

**원인**: 프로세스가 중복 실행되었거나 제대로 종료되지 않음
**해결**: 위 스크립트가 모든 프로세스를 정리하고 마이크 아이콘이 사라집니다

수동으로 확인하려면:
```bash
# 실행 중인 프로세스 확인
ps aux | grep main_whisper

# 수동 종료
pkill -9 -f main_whisper.py
rm -f /tmp/stt_whisper.pid
```

### 붙여넣기가 안 될 때
→ 시스템 설정 → 개인 정보 보호 및 보안 → 손쉬운 사용
→ **Hammerspoon** 활성화

### 전사 정확도가 낮을 때
→ 조용한 환경에서 마이크에 가까이 말하기
→ 마이크 권한 확인 (위 참조)
→ 또는 더 큰 모델 사용 (small, medium)

### Hammerspoon이 실행되지 않을 때
```bash
# 수동 실행
open -a Hammerspoon

# 설치 확인
ls -la /Applications/Hammerspoon.app
```

### 로그 확인
```bash
# 메인 로그
tail -f /tmp/stt_whisper.log

# 토글 디버그 로그
tail -f /tmp/stt_whisper_toggle_debug.log
```

## 모델 비교

| 모델 | 크기 | 속도 | 정확도 | 추천 |
|------|------|------|--------|------|
| base | 141MB | 빠름 | 보통 | 빠른 응답 필요 시 |
| **small** | **466MB** | **중간** | **우수** | **현재 사용 중** |
| medium | 1.5GB | 느림 | 최고 | 최고 정확도 |

### 모델 변경하기

다른 모델로 바꾸려면:
```bash
# 1. 모델 다운로드
cd whisper.cpp
bash ./models/download-ggml-model.sh medium  # 또는 base, large

# 2. whisper_transcriber.py 수정
# WHISPER_MODEL = WHISPER_CPP_DIR / "models" / "ggml-medium.bin"
```

## 핵심 기술

1. **Whisper.cpp** - OpenAI Whisper의 C++ 포팅
   - Metal GPU 가속 (M1/M2/M3/M4 자동 인식)
   - CPU만 사용 대비 3-4배 빠름
2. **Hammerspoon** - macOS 자동화, 전역 단축키
3. **pynput** - Python 키보드 제어, 자동 붙여넣기
4. **VAD (Voice Activity Detection)** - 음성 자동 감지

## GPU 가속 확인

실행 로그에서 확인 가능:
```bash
tail -f /tmp/stt_whisper.log | grep -i "gpu\|metal"
```

성공적으로 GPU 사용 중이면:
```
use gpu    = 1
GPU name:   Apple M3 Max
ggml_metal_device_init: ...
```

## 라이선스

MIT License

## 기반 프로젝트 및 참고

### 기반 프로젝트
- [**vertuzz/stt-typer**](https://github.com/vertuzz/stt-typer) - 원본 프로젝트 (Google Gemini API 기반)
- [**whisper.cpp**](https://github.com/ggml-org/whisper.cpp) - OpenAI Whisper의 C++ 포팅 (로컬 실행)

### 사용 도구
- [Hammerspoon](https://www.hammerspoon.org/) - macOS 자동화 및 전역 단축키
- [pynput](https://pypi.org/project/pynput/) - Python 키보드 제어

