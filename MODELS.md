# Whisper 모델 가이드

## 📊 전체 모델 비교

### 기본 다국어 모델 (한국어 지원)

| 모델 | 크기 | 메모리 | 속도 | 정확도 | 추천 용도 |
|------|------|--------|------|--------|-----------|
| **tiny** | 75MB | ~390MB | ⚡⚡⚡⚡⚡ 매우 빠름 | ⭐⭐ | 테스트, 실시간 필요 |
| **base** | 141MB | ~500MB | ⚡⚡⚡⚡ 빠름 | ⭐⭐⭐ | 일상 사용, 빠른 응답 |
| **small** ✅ | 465MB | ~1GB | ⚡⚡⚡ 중간 | ⭐⭐⭐⭐ | **균형잡힌 선택** |
| **medium** | 1.5GB | ~2.6GB | ⚡⚡ 느림 | ⭐⭐⭐⭐⭐ | 높은 정확도 필요 |
| **large-v1** | 2.9GB | ~4.7GB | ⚡ 매우 느림 | ⭐⭐⭐⭐⭐ | 구버전 |
| **large-v2** | 2.9GB | ~4.7GB | ⚡ 매우 느림 | ⭐⭐⭐⭐⭐ | 전문가용 |
| **large-v3** | 2.9GB | ~4.7GB | ⚡ 매우 느림 | ⭐⭐⭐⭐⭐ | 최고 정확도 |
| **large-v3-turbo** 🚀 | 1.6GB | ~3.1GB | ⚡⚡ 개선됨 | ⭐⭐⭐⭐⭐ | **large + 속도** |

---

## 🎯 모델 선택 가이드

### 일반 사용자
```
tiny    → 테스트용만
base    → 빠른 응답 필요
small   → ✅ 추천! (현재 사용 중)
```

### 전문가 사용
```
medium  → 회의록, 인터뷰
large-v3-turbo → 최고 정확도 + 합리적 속도
large-v3 → 절대 정확도 (속도 상관없을 때)
```

---

## 🌍 영어 전용 모델 (.en)

한국어 사용하지 않는다면:

| 모델 | 설명 |
|------|------|
| tiny.en | 영어 전용 tiny |
| base.en | 영어 전용 base |
| small.en | 영어 전용 small |
| medium.en | 영어 전용 medium |

**장점**: 다국어 모델보다 영어에서 약간 더 정확  
**단점**: 한국어 안 됨!

---

## ⚙️ 양자화 모델 (-q5_0, -q8_0)

메모리 절약 버전:

| 모델 | 설명 | 크기 감소 | 정확도 손실 |
|------|------|-----------|-------------|
| -q5_0 | 5-bit 양자화 | ~50% | 약간 |
| -q8_0 | 8-bit 양자화 | ~30% | 거의 없음 |

**예시:**
- `small-q5_1` = small 모델의 5-bit 버전
- `large-v3-turbo-q8_0` = turbo 모델의 8-bit 버전

**추천**: 메모리 부족할 때만 사용

---

## 🚀 속도 비교 (M3 Max, 10초 오디오 기준)

```
tiny:    ~1초    ⚡⚡⚡⚡⚡
base:    ~2초    ⚡⚡⚡⚡
small:   ~3-4초  ⚡⚡⚡  ← 현재
medium:  ~8-10초 ⚡⚡
large-v3-turbo: ~12-15초 ⚡⚡
large-v3: ~20-25초 ⚡
```

---

## 💡 추천 시나리오

### 1. 일상적 음성 입력 (현재 설정)
```bash
✅ small 모델 (현재 사용 중)
- 빠르고 정확한 균형
- 일반적인 대화, 메모, 코드 주석
```

### 2. 실시간 응답 필요
```bash
./switch_model.sh base
- 2초 안에 전사
- 약간의 정확도 희생
```

### 3. 회의록, 인터뷰 전사
```bash
# 다운로드
cd whisper.cpp
bash ./models/download-ggml-model.sh medium

# 전환
./switch_model.sh medium
- 높은 정확도
- 10초 정도 대기 가능
```

### 4. 최고 정확도 + 합리적 속도
```bash
# large-v3-turbo (추천!)
cd whisper.cpp
bash ./models/download-ggml-model.sh large-v3-turbo

# 전환
./switch_model.sh large-v3-turbo
- large 정확도
- medium 수준 속도
```

### 5. 절대 정확도
```bash
# large-v3
cd whisper.cpp
bash ./models/download-ggml-model.sh large-v3

./switch_model.sh large-v3
- 최고 정확도
- 20초+ 대기
- 전문적 전사 작업용
```

---

## 📥 모델 다운로드

```bash
cd /Users/sunglee/Documents/Scratch/stt-typer/whisper.cpp

# 기본 모델
bash ./models/download-ggml-model.sh tiny
bash ./models/download-ggml-model.sh base
bash ./models/download-ggml-model.sh small      # ✅ 이미 설치됨
bash ./models/download-ggml-model.sh medium

# large 모델
bash ./models/download-ggml-model.sh large-v2
bash ./models/download-ggml-model.sh large-v3
bash ./models/download-ggml-model.sh large-v3-turbo  # 추천!

# 양자화 버전
bash ./models/download-ggml-model.sh small-q8_0
bash ./models/download-ggml-model.sh large-v3-turbo-q8_0
```

---

## 🔄 모델 전환

```bash
# 간단 전환
./switch_model.sh [모델명]

# 예시
./switch_model.sh base
./switch_model.sh medium
./switch_model.sh large-v3-turbo
```

---

## 💾 디스크 공간 요구사항

설치된 모델들:
```bash
ls -lh whisper.cpp/models/ggml-*.bin
```

총 공간:
- tiny + base + small: ~700MB
- + medium: ~2.2GB
- + large-v3: ~5.1GB
- 전체: ~5GB

---

## 🎯 추천 조합

### 최소 설치 (현재)
```
✅ small (465MB)
- 대부분의 경우 충분
```

### 균형 설치
```
base (141MB) + small (465MB) + medium (1.5GB)
= 2.1GB
- 상황에 따라 전환
```

### 전문가 설치
```
small + medium + large-v3-turbo
= 3.6GB
- 일상: small
- 중요: medium
- 전문: large-v3-turbo
```

---

## 🔍 현재 설치된 모델 확인

```bash
ls -lh whisper.cpp/models/ggml-*.bin

# 현재 사용 중인 모델
grep "WHISPER_MODEL" whisper_transcriber.py
```

---

## 💡 팁

1. **일상 사용**: small로 충분 (현재 설정 ✅)
2. **빠른 응답**: base로 전환
3. **높은 정확도**: medium 다운로드
4. **최고 품질**: large-v3-turbo 추천 (large-v3보다 빠름!)
5. **메모리 부족**: 양자화 버전 (-q8_0) 사용

---

## 🚀 최신 모델: large-v3-turbo

2024년 출시, **가장 추천!**

**장점:**
- large-v3와 동일한 정확도
- **2배 빠른 속도**
- 크기도 작음 (1.6GB vs 2.9GB)

**설치:**
```bash
cd whisper.cpp
bash ./models/download-ggml-model.sh large-v3-turbo
cd ..
./switch_model.sh large-v3-turbo
```

**사용 시나리오:**
- 전문적인 회의록
- 인터뷰 전사
- 유튜브 자막 생성
- 최고 품질이 필요한 경우

