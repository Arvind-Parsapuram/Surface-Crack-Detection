---
title: Surface Crack Detection
emoji: 🚀
colorFrom: red
colorTo: red
sdk: streamlit
sdk_version: "1.58.0"
app_file: app.py
pinned: false
tags:
- streamlit
- computer-vision
- deep-learning
---

# 🏗️ Surface Crack Detection

> **Bootcamp Project** — Multi-class classification of road/bridge surface defects using Computer Vision  
> **Domain:** Manufacturing & Computer Vision  
> **Framework:** PyTorch

---

## 📋 Overview

Classify surface images into **4 defect categories** using transfer learning:

| Class           | Images  | % of Total |
| --------------- | ------- | ---------- |
| Cracks          | 73      | 23.9%      |
| Patch           | 42      | 13.7%      |
| Potholes        | 91      | 29.7%      |
| Surface Defects | 100     | 32.7%      |
| **Total**       | **306** | **100%**   |

---

## 🏗️ Architecture

**Primary:** ResNet50 / EfficientNet-B0 (transfer learning, ImageNet weights)  
**Baseline (optional):** 3-layer CNN

```
Input (3×224×224)
  → Pretrained Backbone (frozen → unfreeze last 2 blocks)
  → Global Avg Pool → Dropout → Linear(256) → ReLU → Dropout → Linear(4)
  → Output: [Cracks, Patch, Potholes, Surface Defects]
```

---

## 🔧 Pipeline

```
Raw Images (306, varied resolutions)
  → Resize(256) → CenterCrop(224) → Normalize(ImageNet μ,σ)
  → Stratified Split (70/15/15)
  → Train: ~214 images | Val: ~46 images | Test: ~46 images
  → Train Augmentation: RandomHorizontalFlip, RandomRotation, ColorJitter
```

---

## 🏋️ Training Strategy

| Phase         | Backbone               | Epochs | LR   | Optimizer |
| ------------- | ---------------------- | ------ | ---- | --------- |
| 1 — Warmup    | Frozen                 | 5–10   | 1e-3 | AdamW     |
| 2 — Fine-tune | Unfreeze last 2 blocks | 15–25  | 1e-5 | AdamW     |

- **Loss:** Weighted CrossEntropy (inverse class frequency)
- **Scheduler:** CosineAnnealingLR
- **Callbacks:** EarlyStopping (patience=7), ModelCheckpoint (val F1)
- **Mixed Precision:** `torch.cuda.amp` (if GPU available)

---

## 📁 Project Structure

```
bootcamp/
├── app.py                        # Streamlit entry point
├── pages/                        # Streamlit pages
├── backend/                      # Backend logic (auth, prediction)
├── data/                         # Processed dataset (train/val/test)
├── src/                          # Source code
│   ├── config.py                 # Hyperparameters
│   ├── dataset.py                # Dataset + transforms
│   ├── model.py                  # ResNet50 / baseline CNN
│   ├── train.py                  # Training loop
│   ├── evaluate.py               # Evaluation + metrics
│   ├── utils.py                  # Helpers
│   └── prepare_data.py           # Data splitting
├── notebooks/
│   ├── 01_eda.ipynb              # Exploratory Data Analysis
│   └── 02_results.ipynb          # Results visualization
├── models/                       # Saved checkpoints
├── reports/                      # Figures, logs, metrics
├── migrations/                   # Database migrations
├── Dockerfile                    # Docker support
├── PLAN.md                       # Technical plan
├── TEAM_ROADMAP.md               # Team roles & sprint plan
└── README.md                     # ← You are here
```

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run Streamlit app
streamlit run app.py

# 3. Prepare dataset (stratified split)
python src/prepare_data.py

# 4. Train model
python src/train.py

# 5. Evaluate
python src/evaluate.py
```

---

## 🌐 Deploy

**Hugging Face Spaces** (Streamlit SDK) — no sleep, free tier:  
`https://huggingface.co/spaces/amruthjakku/surface-crack-detection`

**Alternative:** Docker — build and run:
```bash
docker build -t crack-detection .
docker run -p 8501:8501 crack-detection
```
