# 🚀 재부팅 후 시작 가이드

## ✅ 현재 상태

- ✅ Hammerspoon 메뉴바 아이콘 숨김 설정 완료
- ✅ 단축키 `⌃⌥Space`는 항상 작동

---

## 🔄 리부트 후 최초 실행

### 방법 1: Hammerspoon 자동 시작 (권장)

**한 번만 설정하면 끝!**

1. **Hammerspoon 열기**
   ```bash
   open -a Hammerspoon
   ```

2. **메뉴바에서 Hammerspoon 아이콘 클릭** (잠깐 보임)

3. **"Launch Hammerspoon at login" 체크** ✅

4. **완료!** 이제 재부팅해도 자동 시작
   - 메뉴바 아이콘은 보이지 않음 (이미 설정됨)
   - `⌃⌥Space` 단축키 바로 사용 가능

---

### 방법 2: 수동 시작

재부팅 후 Hammerspoon이 안 떠있으면:

```bash
open -a Hammerspoon
```

또는 Spotlight (`⌘Space`)에서 "Hammerspoon" 검색해서 실행

---

## 🎤 마이크 표시 이해하기

### 현재 동작:

1. **평소**: Hammerspoon 아이콘 안 보임 ✅
2. **⌃⌥Space 누르면**: 
   - macOS 시스템이 마이크 사용 감지
   - **제어 센터에 주황색 마이크 표시** 🎤
3. **녹음 중지하면**: 마이크 표시 사라짐

### 주황색 마이크 표시:

```
제어 센터 (오른쪽 위) → 🎤 주황색 점
```

이것은:
- ✅ **정상입니다!**
- macOS 보안 기능 (앱이 마이크 사용 중임을 표시)
- 녹음 중일 때만 나타남
- 이것은 **숨길 수 없습니다** (보안상)

---

## 🔧 완전 자동화 설정

### 1. Hammerspoon 로그인 시 자동 시작

```bash
# Hammerspoon 실행
open -a Hammerspoon

# 메뉴바 아이콘 클릭 → Preferences → "Launch Hammerspoon at login" ✅
```

### 2. 확인

재부팅 후:
```bash
# Hammerspoon이 실행 중인지 확인
ps aux | grep Hammerspoon | grep -v grep
```

실행 중이면 → 자동 시작 성공!
아무것도 안 나오면 → 수동으로 `open -a Hammerspoon`

---

## 📋 빠른 체크리스트

재부팅 후:

1. [ ] Hammerspoon 실행 중? 
   - 확인: `ps aux | grep Hammerspoon | grep -v grep`
   - 안 떠있으면: `open -a Hammerspoon`

2. [ ] 메뉴바에 Hammerspoon 아이콘 안 보임? ✅ (정상)

3. [ ] `⌃⌥Space` 작동?
   - Notes 열고 테스트
   - 작동 안 하면: Hammerspoon 재시작

---

## 🎯 예상 동작

### 정상 상태:
```
평소:
- 메뉴바: 깨끗함 (아이콘 없음)
- 단축키: 작동

녹음 중:
- 메뉴바: 🎤 주황색 마이크 표시 (macOS 시스템)
- 단축키: ⌃⌥Space로 중지

녹음 후:
- 메뉴바: 깨끗함 (마이크 표시 사라짐)
- 텍스트: 자동 입력됨
```

---

## 🐛 문제 해결

### 🎤 주황색 마이크 아이콘이 계속 켜져있을 때 (가장 흔함!)

**증상**: 녹음을 중지했는데도 제어 센터에 주황색 마이크가 계속 표시됨

**원인**: `main_whisper.py` 프로세스가 백그라운드에서 계속 실행 중

**즉시 해결**:
```bash
# 긴급 정지 스크립트 실행
cd k-stt-typer  # 또는 프로젝트 디렉토리
./stop_all.sh
```

**수동 해결**:
```bash
# 1. 실행 중인 프로세스 확인
ps aux | grep main_whisper

# 2. 모두 강제 종료
pkill -9 -f main_whisper.py

# 3. PID 파일 정리
rm -f /tmp/stt_whisper.pid /tmp/stt_whisper.status
```

**예방**: 최신 `toggle_whisper.sh`는 이 문제를 자동으로 방지합니다 ✅

---

### Hammerspoon 아이콘이 계속 보이면:

```bash
# 1. 설정 확인
cat ~/.hammerspoon/init.lua | grep menuIcon
# → hs.menuIcon(false) 가 있어야 함

# 2. Hammerspoon 재시작
killall Hammerspoon
open -a Hammerspoon

# 3. 아이콘 사라졌는지 확인
```

### 단축키가 작동 안 하면:

```bash
# Hammerspoon이 실행 중인지 확인
ps aux | grep Hammerspoon

# 안 떠있으면 실행
open -a Hammerspoon

# 로그 확인
tail -f /tmp/stt_whisper_toggle_debug.log
```

### 마이크 권한 오류:

```
System Settings → Privacy & Security → Microphone
→ Python / Terminal ✅ 체크
```

---

## 💡 팁

### 자동 시작 확인:

```bash
# 로그인 항목 확인
osascript -e 'tell application "System Events" to get the name of every login item'
```

"Hammerspoon"이 있으면 자동 시작 설정됨!

### Hammerspoon 완전 재시작:

```bash
killall Hammerspoon && sleep 1 && open -a Hammerspoon
```

---

## 📝 요약

### 한 번만 하면 됨:
1. ✅ `hs.menuIcon(false)` 설정 완료 (이미 됨)
2. Hammerspoon → "Launch at login" 체크

### 재부팅 후:
- Hammerspoon 자동 시작 (설정했으면)
- 아이콘 안 보임 ✅
- `⌃⌥Space` 바로 사용 가능
- 녹음 중에만 🎤 표시 (macOS 시스템)

---

## 🎉 완료!

이제:
- ✅ Hammerspoon 아이콘 안 보임
- ✅ 녹음 중에만 🎤 마이크 표시 (정상)
- ✅ 재부팅해도 자동 작동 (로그인 시 자동 시작 설정 시)

**주황색 마이크 표시는 macOS 보안 기능이므로 정상입니다!** 🎤

