# 💼 AI Salary Prediction System

> End-to-end Machine Learning system that predicts AI job salaries based on real-world job and economic features — trained, served via REST API, and deployed to the cloud.

## 📄 Project Overview

This project demonstrates a **complete production ML workflow**, including:

- Data preprocessing with `Pipeline` and `ColumnTransformer`
- Multiple ML model training, evaluation, and comparison
- Hyperparameter tuning with `GridSearchCV` and `RandomizedSearchCV`
- Automatic best model selection and persistence via `joblib`
- Production-ready REST API with full input validation (FastAPI + Pydantic v2)
- Interactive prediction frontend (Streamlit)
- Cloud deployment on **Render**

---

## 🗂 Dataset

**Source:** Global AI Jobs Dataset

**Features include:**
- Country, Job Role, Industry, AI Specialization
- Experience Level, Company Size, Work Mode
- AI Adoption Score, Economic Index
- Job Security, Career Growth, Work-Life Balance Scores

**Target Variable:** `salary_usd`

---

## 🧠 Machine Learning Pipeline

### Preprocessing
| Step | Technique |
|---|---|
| Categorical (nominal) | OneHotEncoding |
| Categorical (ordinal) | OrdinalEncoding |
| Skewed features | Log Transformation (`bonus_usd`) |
| Numerical (linear models) | StandardScaler |
| Automation | `ColumnTransformer` + `Pipeline` |

### Models Trained
- Linear Regression
- Linear SVR
- Decision Tree Regressor
- **Random Forest Regressor** ← Best Model ✅

### Hyperparameter Tuning
- `GridSearchCV` — SVM, Decision Tree
- `RandomizedSearchCV` — Random Forest
- `K-Fold Cross Validation`

### Evaluation Metrics
- R² Score · MAE · MSE · RMSE

---

## 🚀 REST API — FastAPI

### Prediction Endpoint
```
POST /predict
```

**Sample Request:**
```json
{
  "country": "United States",
  "job_role": "Machine Learning Engineer",
  "ai_specialization": "Natural Language Processing",
  "industry": "Technology",
  "work_mode": "Remote",
  "education_required": "Bachelor",
  "experience_level": "Senior",
  "company_size": "Large",
  "weekly_hours": 45,
  "ai_adoption_score": 78.0,
  "economic_index": 35.0,
  "bonus_usd": 12000.0
}
```

**Sample Response:**
```json
{
  "predicted_salary_usd": 134500.0,
  "model_used": "Random Forest (Tuned)"
}
```

### Validation Rules
| Field | Rule |
|---|---|
| `country`, `job_role`, `industry`, etc. | Non-empty, 2–100 characters |
| `weekly_hours` | Between 1 and 168 |
| All score fields | Between 0.0 and 100.0 |
| `economic_index` | Between -100.0 and 100.0 |
| `bonus_usd` | Non-negative, max $10,000,000 |
| `offer_acceptance_rate` | Cannot be 0 for Senior/Lead roles |

---

## 🎨 Frontend — Streamlit

Interactive UI for real-time salary prediction.

```
User → Streamlit Form → FastAPI /predict → ML Model → Predicted Salary
```

---

## ☁️ Deployment — Render

Both the API and frontend are deployed as separate Render Web Services.

### FastAPI Backend
```
Build Command:  pip install -r requirements.txt
Start Command:  uvicorn app:app --host 0.0.0.0 --port $PORT
```

### Streamlit Frontend
```
Build Command:  pip install -r requirements.txt
Start Command:  streamlit run streamlit_app.py --server.address 0.0.0.0 --server.port $PORT
```

> ⚠️ Make sure `model.pkl` is committed to the repo before deploying — Render builds from source and won't have it otherwise.

---

## 🐳 Docker

### Pull and Run (Docker Hub — recommended)

The image is published on Docker Hub, so you can run it without cloning the repo or building anything locally:

```bash
docker pull inam54/ai-salary-predictor:latest
docker run -p 8000:8000 -p 8501:8501 inam54/ai-salary-predictor:latest
```

## 🐳 Docker (Local Alternative)

Run both services locally in a single container:

```bash
docker build -t ai-salary-predictor .
docker run -p 8000:8000 -p 8501:8501 ai-salary-predictor
```

| Service | URL |
|---|---|
| FastAPI Swagger | http://localhost:8000/docs |
| Streamlit UI | http://localhost:8501 |

---

## 🏃 Run Locally (Without Docker)

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Train and save the model
python Jobs_Salary_Prediction.py

# 3. Start FastAPI (Terminal 1)
uvicorn app:app --reload

# 4. Start Streamlit (Terminal 2)
streamlit run streamlit_app.py
```

---

## 📁 Project Structure

```
AI_Job_Prediction/
├── Dataset/
│   └── global_ai_jobs.csv
├── Jobs_Salary_Prediction.py   # ML pipeline: training, tuning, evaluation
├── app.py                      # FastAPI REST API
├── predict.py                  # Model loading & prediction helper
├── user_input.py               # Pydantic v2 schema & validators
├── streamlit_app.py            # Streamlit frontend
├── config.yml                  # Hyperparameters & settings
├── model.pkl                   # Saved best model
├── Dockerfile                  # Container image
├── start.sh                    # Startup script (Docker)
├── requirements.txt
└── README.md
```

---

## 🛠 Tech Stack

| Layer | Tools |
|---|---|
| ML | scikit-learn, pandas, NumPy |
| API | FastAPI, Pydantic v2, Uvicorn |
| Frontend | Streamlit |
| Persistence | Joblib |
| Deployment | Render, Docker |
| Language | Python |

---

## 💡 Key Learnings

- Designed a full end-to-end ML system with production-quality code
- Applied feature engineering, encoding strategies, and log transformation
- Compared multiple models and selected the best automatically
- Built and validated a REST API with Pydantic v2 custom validators
- Integrated a Streamlit frontend with a live FastAPI backend
- Deployed a real ML product to the cloud on Render

---

## 👤 Author

**Inam Ur Rehman**  
BS Computer Engineering — Information Technology University, Lahore  
Focus: Machine Learning · AI Systems · Full Stack ML Deployment