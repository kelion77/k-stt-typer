# Whisper Model Guide

**[한국어 문서](MODELS.ko.md)**

## Model Comparison

### Multilingual Models (Korean Support)

| Model | Size | Memory | Speed | Accuracy | Recommended Use |
|-------|------|--------|-------|----------|-----------------|
| **tiny** | 75MB | ~390MB | Very Fast | Fair | Testing, real-time needs |
| **base** | 141MB | ~500MB | Fast | Good | Daily use, quick response |
| **small** | 465MB | ~1GB | Medium | Excellent | **Balanced choice (current)** |
| **medium** | 1.5GB | ~2.6GB | Slow | Outstanding | High accuracy needs |
| **large-v1** | 2.9GB | ~4.7GB | Very Slow | Outstanding | Legacy version |
| **large-v2** | 2.9GB | ~4.7GB | Very Slow | Outstanding | Professional use |
| **large-v3** | 2.9GB | ~4.7GB | Very Slow | Outstanding | Maximum accuracy |
| **large-v3-turbo** | 1.6GB | ~3.1GB | Improved | Outstanding | **large + speed** |

---

## Model Selection Guide

### General Users
```
tiny    → Testing only
base    → Quick response needed
small   → Recommended! (current)
```

### Professional Use
```
medium  → Meeting transcripts, interviews
large-v3-turbo → Best accuracy + reasonable speed
large-v3 → Maximum accuracy (when speed doesn't matter)
```

---

## English-Only Models (.en)

If you don't use Korean:

| Model | Description |
|-------|-------------|
| tiny.en | English-only tiny |
| base.en | English-only base |
| small.en | English-only small |
| medium.en | English-only medium |

**Pros**: Slightly more accurate for English than multilingual models
**Cons**: No Korean support!

---

## Quantized Models (-q5_0, -q8_0)

Memory-saving versions:

| Model | Description | Size Reduction | Accuracy Loss |
|-------|-------------|----------------|---------------|
| -q5_0 | 5-bit quantization | ~50% | Slight |
| -q8_0 | 8-bit quantization | ~30% | Minimal |

**Examples:**
- `small-q5_1` = small model 5-bit version
- `large-v3-turbo-q8_0` = turbo model 8-bit version

**Recommendation**: Use only when memory is limited

---

## Speed Comparison (M3 Max, 10 seconds audio)

```
tiny:    ~1s     Very Fast
base:    ~2s     Fast
small:   ~3-4s   Medium  ← Current
medium:  ~8-10s  Slow
large-v3-turbo: ~12-15s Improved
large-v3: ~20-25s Very Slow
```

---

## Recommended Scenarios

### 1. Daily Voice Input (Current Setup)
```bash
small model (currently in use)
- Fast and accurate balance
- General conversation, notes, code comments
```

### 2. Real-time Response Needed
```bash
./switch_model.sh base
- Transcription within 2 seconds
- Slight accuracy tradeoff
```

### 3. Meeting Transcripts, Interviews
```bash
# Download
cd whisper.cpp
bash ./models/download-ggml-model.sh medium

# Switch
./switch_model.sh medium
- High accuracy
- 10 second wait acceptable
```

### 4. Best Accuracy + Reasonable Speed
```bash
# large-v3-turbo (recommended!)
cd whisper.cpp
bash ./models/download-ggml-model.sh large-v3-turbo

# Switch
./switch_model.sh large-v3-turbo
- large accuracy
- medium-level speed
```

### 5. Maximum Accuracy
```bash
# large-v3
cd whisper.cpp
bash ./models/download-ggml-model.sh large-v3

./switch_model.sh large-v3
- Maximum accuracy
- 20+ second wait
- Professional transcription work
```

---

## Model Download

```bash
cd /path/to/k-stt-typer/whisper.cpp

# Basic models
bash ./models/download-ggml-model.sh tiny
bash ./models/download-ggml-model.sh base
bash ./models/download-ggml-model.sh small      # Already installed
bash ./models/download-ggml-model.sh medium

# Large models
bash ./models/download-ggml-model.sh large-v2
bash ./models/download-ggml-model.sh large-v3
bash ./models/download-ggml-model.sh large-v3-turbo  # Recommended!

# Quantized versions
bash ./models/download-ggml-model.sh small-q8_0
bash ./models/download-ggml-model.sh large-v3-turbo-q8_0
```

---

## Model Switching

```bash
# Simple switch
./switch_model.sh [model-name]

# Examples
./switch_model.sh base
./switch_model.sh medium
./switch_model.sh large-v3-turbo
```

---

## Disk Space Requirements

View installed models:
```bash
ls -lh whisper.cpp/models/ggml-*.bin
```

Total space:
- tiny + base + small: ~700MB
- + medium: ~2.2GB
- + large-v3: ~5.1GB
- All: ~5GB

---

## Recommended Combinations

### Minimal Installation (Current)
```
small (465MB)
- Sufficient for most cases
```

### Balanced Installation
```
base (141MB) + small (465MB) + medium (1.5GB)
= 2.1GB
- Switch based on situation
```

### Professional Installation
```
small + medium + large-v3-turbo
= 3.6GB
- Daily: small
- Important: medium
- Professional: large-v3-turbo
```

---

## Check Installed Models

```bash
ls -lh whisper.cpp/models/ggml-*.bin

# Current model in use
grep "WHISPER_MODEL" whisper_transcriber.py
```

---

## Tips

1. **Daily use**: small is sufficient (current setup)
2. **Quick response**: Switch to base
3. **High accuracy**: Download medium
4. **Best quality**: large-v3-turbo recommended (faster than large-v3!)
5. **Low memory**: Use quantized versions (-q8_0)

---

## Latest Model: large-v3-turbo

Released 2024, **most recommended!**

**Advantages:**
- Same accuracy as large-v3
- **2x faster**
- Smaller size (1.6GB vs 2.9GB)

**Installation:**
```bash
cd whisper.cpp
bash ./models/download-ggml-model.sh large-v3-turbo
cd ..
./switch_model.sh large-v3-turbo
```

**Use Cases:**
- Professional meeting transcripts
- Interview transcription
- YouTube subtitle generation
- When maximum quality is needed
