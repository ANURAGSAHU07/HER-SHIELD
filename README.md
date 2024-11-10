# 🛡️ HERSHIELD - AI-Driven Women's Safety Analytics Software

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/downloads/) 
[![PyTorch](https://img.shields.io/badge/PyTorch-1.8.0-orange.svg)](https://pytorch.org/)
[![NVIDIA](https://img.shields.io/badge/NVIDIA-GPU-green.svg)](https://www.nvidia.com/en-us/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

### 💡 Overview
**HERSHIELD** is an innovative, AI-powered surveillance solution designed to enhance women’s safety through real-time monitoring of CCTV feeds. The system detects risky situations, like being alone at night or surrounded by men, and triggers instant alerts to ensure rapid police response. 

🔍 **Problem Statement**: Women's safety in public spaces is a significant issue today. **HERSHIELD** addresses this by combining advanced AI algorithms with continuous CCTV analysis, empowering authorities to act before harm occurs.

---

## 🚀 Features

- 🎥 **24/7 Video Monitoring**: Continuously monitors CCTV feeds for risk detection.
- 👩‍🦰 **Gender Classification**: Utilizes RCNN to identify individuals' gender and assess risk factors.
- ⚠️ **Real-Time Threat Detection**: Tracks male-to-female ratios, especially at night, to flag risky situations.
- 📊 **Risk Score Calculation**: Generates risk scores based on time, location, and environmental factors.
- 🔥 **Hotspot Identification**: Pinpoints high-risk zones through historical and real-time data.
- ✋ **Gesture Recognition**: Detects distress signals such as frantic waving or SOS gestures.
- 🚨 **Instant Alerts**: Sends immediate notifications to authorities, ensuring swift emergency response.

---

## 🛠️ Tech Stack

- **Python** 🐍: The primary language used for its versatility and large ecosystem.
- **PyTorch** 🔥: For neural network training and real-time model updates.
- **Mobile VNet** 🖼️: To generate detailed feature maps from CCTV frames.
- **Finetuned YOLO through Custom Dataset** 👤: For gender-based classification.
- **Vision Transformers (ViTs)** ⚡: Extract high-level features for identifying threats.
- **MediaPipe** 🎥: Framework for multimodal ML pipelines.
- **CUDA-Enabled GPUs** ⚙️: For accelerated real-time video processing.

---

## ⚙️ How It Works

1. **Frame Preprocessing**: CCTV frames are resized and normalized (640x640x3) for uniform input.
2. **Feature Extraction**: CSP-Darknet 53 generates detailed feature maps.
3. **Gender Detection**: RCNN classifies individuals into male or female, with bounding boxes around identified genders.
4. **Risk Assessment**: Calculates a risk score based on factors like time, location, and the number of males/females in the scene.
5. **Hotspot Detection**: The Hotspot Identification Algorithm tracks potential danger zones and raises alerts if necessary.
6. **Alerting System**: Immediate notifications are sent to police or authorities when violent gestures (e.g., SOS signals) are detected.

---

## ✨ Impact and Benefits

- **Women’s Safety First**: Contributes to a significant reduction in crime rates by enabling rapid detection and response.
- **Assists Law Enforcement**: Minimizes the need for physical patrols, saving manpower.
- **Cost-Effective**: Uses existing CCTV infrastructure to reduce hardware costs.
- **Highly Scalable**: Expandable to cover more extensive areas like schools, workplaces, and public transport.
- **Promotes Gender Equality**: By creating a safer environment, women can participate more confidently in public life.

---

## 🛠️ Installation

### Prerequisites
- Python 3.x 🐍
- PyTorch 🔥
- CUDA-enabled GPU ⚙️

Install the required dependencies:

```bash
pip install -r requirements.txt
```

### 🚀 Running the System

1. Clone the repository:

```bash
git clone https://github.com/yourusername/hershield.git
```

2. Navigate to the project folder:

```bash
cd hershield
```

3. Start the system:

```bash
python main.py
```


## 📧 Contact

For support, questions, or suggestions:

- Team: HERSHIELD
- Email: anuragsahu4328@gmail.com

---

