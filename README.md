# STT Typer - Whisper.cpp

Mac에서 **단축키 하나로** 한국어 음성을 텍스트로 변환하는 도구

> 이 프로젝트는 [vertuzz/stt-typer](https://github.com/vertuzz/stt-typer)와 [whisper.cpp](https://github.com/ggml-org/whisper.cpp)를 기반으로 만들어졌습니다.

## ✨ 특징

- 🎤 **단축키 하나**: `⌃⌥Space` (Control + Option + Space)
- 🆓 **완전 무료**: Whisper.cpp 로컬 실행, API 비용 없음
- 🔒 **프라이버시**: 모든 처리가 로컬에서, 인터넷 불필요
- 🇰🇷 **한국어 완벽 지원**: Whisper 모델 자체가 다국어 지원
- ⚡ **GPU 가속**: Apple Silicon (M1/M2/M3/M4) Metal 자동 활성화
- ✅ **자동 붙여넣기**: 커서 위치에 자동 입력

## 🚀 빠른 시작

### 1. 설치 (5분)

```bash
# 저장소 클론
git clone https://github.com/kelion77/k-stt-typer.git
cd k-stt-typer

# Python 의존성 설치
uv sync

# Whisper.cpp + 모델 설치
./install_whisper.sh

# Hammerspoon (단축키) 설치
./setup_global_hotkey.sh
```

### 2. 권한 설정

Hammerspoon 실행 시 **접근성 권한** 요청:
- System Settings → Privacy & Security → Accessibility
- **Hammerspoon** ✅ 체크

### 3. 사용

```
1. 아무 앱에서나 (VS Code, Notes, Chrome 등)
2. ⌃⌥Space 한 번 → 녹음 시작
3. 한국어로 말하기 (예: "안녕하세요")
4. ⌃⌥Space 다시 → 자동으로 입력됨!
```

## 🔧 작동 방식

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
커서 위치에 입력! ✨
```

## 📁 주요 파일

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

## 💡 사용 예시

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

## 🔧 문제 해결

### 🎤 마이크 아이콘이 계속 켜져 있을 때 (중요!)

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
→ System Settings → Privacy & Security → Accessibility  
→ Python / Python.app ✅ 체크

### 전사 정확도가 낮을 때
→ 조용한 환경에서 마이크에 가까이 말하기  
→ 또는 더 큰 모델 사용 (small, medium)

### 로그 확인
```bash
tail -f /tmp/stt_whisper.log
```

## 📊 모델 비교

| 모델 | 크기 | 속도 | 정확도 | 추천 |
|------|------|------|--------|------|
| base | 141MB | 빠름 | ⭐⭐⭐⭐ | 빠른 응답 필요 시 |
| **small** | **466MB** | **중간** | **⭐⭐⭐⭐⭐** | **✅ 현재 사용 중** |
| medium | 1.5GB | 느림 | ⭐⭐⭐⭐⭐ | 최고 정확도 |

### 모델 변경하기

다른 모델로 바꾸려면:
```bash
# 1. 모델 다운로드
cd whisper.cpp
bash ./models/download-ggml-model.sh medium  # 또는 base, large

# 2. whisper_transcriber.py 수정
# WHISPER_MODEL = WHISPER_CPP_DIR / "models" / "ggml-medium.bin"
```

## 🎯 핵심 기술

1. **Whisper.cpp** - OpenAI Whisper의 C++ 포팅
   - Metal GPU 가속 (M1/M2/M3/M4 자동 인식)
   - CPU만 사용 대비 3-4배 빠름
2. **Hammerspoon** - macOS 자동화, 전역 단축키
3. **pynput** - Python 키보드 제어, 자동 붙여넣기
4. **VAD (Voice Activity Detection)** - 음성 자동 감지

## 💻 GPU 가속 확인

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

## 📝 라이선스

MIT License

## 🙏 기반 프로젝트 및 참고

### 기반 프로젝트
- [**vertuzz/stt-typer**](https://github.com/vertuzz/stt-typer) - 원본 프로젝트 (Google Gemini API 기반)
- [**whisper.cpp**](https://github.com/ggml-org/whisper.cpp) - OpenAI Whisper의 C++ 포팅 (로컬 실행)

### 사용 도구
- [Hammerspoon](https://www.hammerspoon.org/) - macOS 자동화 및 전역 단축키
- [pynput](https://pypi.org/project/pynput/) - Python 키보드 제어

