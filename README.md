# 💆‍♀️ AI Skin Analyzer

A real-time AI-powered skin analysis system that uses computer vision and machine learning to assess skin health, visualize problem areas, and generate personalized skincare recommendations.

---

## 🚀 Features

* 🎥 Live webcam-based skin analysis
* 🧠 Patch-based skin evaluation (texture, wrinkles, pigmentation)
* 🔥 Heatmap visualization of skin health
* 🎯 Head tilt–based capture system (>60° yaw)
* 🤖 AI-generated skincare recommendations (Gemini API)
* 📊 Real-time + final captured report

---

## 🛠️ Tech Stack

* Python
* OpenCV
* MediaPipe (Face Mesh)
* NumPy
* PyTorch + TorchVision (CLIP model)
* Gradio (UI)
* Google Gemini API (LLM recommendations)

---

## 📦 Project Structure

```id="proj_struct"
skin-analyser/
│
├── app.py
├── skin_heatmap.py
├── face_regions.py
├── patch_analyzer.py
├── clip_skin_analyzer.py
├── head_pose.py
├── skin_condition_interpreter.py
├── llm_recommender.py
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation & Setup

### 1️⃣ Clone the repository

```id="clone"
git clone <your-repo-link>
cd skin-analyser
```

---

### 2️⃣ Install dependencies

```id="install"
pip install -r requirements.txt
```

---

### 3️⃣ Set Gemini API Key

Mac/Linux:

```id="api1"
export GEMINI_API_KEY="your_api_key_here"
```

Windows:

```id="api2"
set GEMINI_API_KEY=your_api_key_here
```

---

### 4️⃣ Run the application

```id="run"
python app.py
```

---

## 🎯 How It Works

1. 📷 Webcam starts → Live skin analysis begins
2. 🧠 AI continuously evaluates facial regions
3. 🔄 Heatmap updates in real-time
4. 🎯 Turn head (>60° yaw) → capture triggered
5. 📊 Final report generated
6. 🤖 AI recommendation generated once

---

## ⚠️ Important Notes

* Use **Python 3.10** for best compatibility
* Ensure webcam access is enabled
* Internet required for AI recommendations
* LLM is triggered only once to avoid API rate limits

---

## 🧠 Design Highlights

* Hybrid system:

  * Rule-based skin analysis (fast + stable)
  * AI-based recommendation (LLM)
* Optimized for real-time performance
* Avoids API overuse using controlled triggering

---

## 📌 Future Improvements

* Skin type classification
* Product database integration
* Mobile deployment
* Improved smoothing for stable scores

---

## 👩‍💻 Author

Developed as part of an AI-based dermatology analysis project.

---

## ⭐ Acknowledgement

* MediaPipe by Google
* OpenAI / Gemini APIs
* PyTorch ecosystem
