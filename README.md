# 💼 AI Salary Prediction System

## 📄 PROJECT OVERVIEW
This project predicts AI-related salaries based on multiple factors such as job role, experience level, company size, and economic indicators.

It demonstrates a **complete end-to-end Machine Learning workflow**, including:
- Advanced preprocessing using pipelines
- Model training, evaluation and hyperparameter tuning
- Model comparison and automatic best model selection
- Production-ready REST API with full input validation
- Interactive frontend built with Streamlit

---

## 🗂 DATASET
**Source:** Global AI Jobs Dataset

**Description:**
The dataset contains features such as:
- Country, Job Role, Industry, AI Specialization
- Experience Level, Company Size, Work Mode
- AI Adoption Score, Economic Indicators
- Work-life Balance, Job Security, Career Growth, etc.

**Target Variable:**
`salary_usd`

---

## 🧰 PROJECT FILES
- `Jobs_Salary_Prediction.py` → Main ML pipeline: training, tuning, evaluation, model saving
- `app.py` → FastAPI REST API with Pydantic validation and prediction endpoint
- `predict.py` → Model loading and prediction helper
- `user_input.py` → Pydantic schema with custom field and model validators
- `config.yml` → Model hyperparameters and training settings
- `streamlit_app.py` → Streamlit frontend UI
- `model.pkl` → Saved best model (Random Forest, tuned)
- `Dataset/global_ai_jobs.csv` → Dataset (excluded via `.gitignore`)
- `Dockerfile` → Container image for API + Streamlit
- `start.sh` → Startup script that runs both services in Docker
- `requirements.txt` → Project dependencies
- `README.md` → Project documentation

---

## 🔧 KEY TECHNIQUES USED

### 📊 DATA PREPROCESSING
- One-Hot Encoding for nominal categorical features (`country`, `job_role`, `industry`, etc.)
- Ordinal Encoding for ordered features (`experience_level`, `company_size`)
- Log Transformation for skewed data (`bonus_usd`)
- Feature Scaling using `StandardScaler` (for linear models only)

---

### 🤖 MODELING
- Linear Regression
- Support Vector Machine (LinearSVR)
- Decision Tree Regressor
- Random Forest Regressor ← **Best Model**

---

### ⚙️ HYPERPARAMETER TUNING
- GridSearchCV (SVM, Decision Tree)
- RandomizedSearchCV (Random Forest)
- K-Fold Cross Validation

---

### 📈 EVALUATION METRICS
- R² Score
- Mean Absolute Error (MAE)
- Mean Squared Error (MSE)
- Root Mean Squared Error (RMSE)

---

## 📊 MODEL COMPARISON
All models are evaluated **before and after tuning** and compared based on R² Score. The best model is selected and saved automatically.

---

## 🏆 BEST MODEL
**Random Forest Regressor (Tuned)**
Selected automatically based on highest R² Score across all trained models.

---

## 🚀 HOW TO RUN

### Step 1 — Install dependencies
```bash
pip install -r requirements.txt
```

### Step 2 — Train and save the model
```bash
python Jobs_Salary_Prediction.py
```
This will train all models, compare them, and save the best one as `model.pkl`.

### Step 3 — Start the FastAPI backend
```bash
uvicorn app:app --reload
```
API will be running at `http://127.0.0.1:8000`

### Step 4 — Start the Streamlit frontend
Open a **new terminal** and run:
```bash
streamlit run streamlit_app.py
```
UI will open automatically in your browser at `http://localhost:8501`

> ⚠️ Make sure FastAPI is running before using the Streamlit UI — both must run at the same time in separate terminals.

---

## 🐳 DOCKER

Run the API and Streamlit UI in a single container. The startup script launches FastAPI on port **8000** and Streamlit on port **8501**.

### Build the image
```bash
docker build -t ai-salary-predictor .
```

### Run the container
```bash
docker run -p 8000:8000 -p 8501:8501 ai-salary-predictor
```

| Service | URL |
|---|---|
| FastAPI (Swagger) | http://localhost:8000/docs |
| Streamlit UI | http://localhost:8501 |

> Ensure `model.pkl` is present in the project root before building or running the image.

---

## 🌐 REST API — FastAPI

### API Docs (Swagger UI)
```
http://127.0.0.1:8000/docs
```

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
    "hiring_difficulty_score": 65.0,
    "ai_adoption_score": 78.0,
    "economic_index": 35.0,
    "offer_acceptance_rate": 72.0,
    "tax_rate_percent": 28.0,
    "skill_demand_score": 80.0,
    "automation_risk": 38.0,
    "job_security_score": 70.0,
    "career_growth_score": 75.0,
    "work_life_balance_score": 62.0,
    "promotion_speed": 58.0,
    "salary_percentile": 75.0,
    "employee_satisfaction": 68.0,
    "bonus_usd": 12000.0
}
```

**Sample Response:**
```json
{
    "predicted_salary_usd": 134500.00,
    "model_used": "Random Forest (Tuned)"
}
```

### Validation Rules
| Field | Rule |
|---|---|
| `country`, `job_role`, `ai_specialization`, `industry`, `education_required` | Non-empty, 2–100 characters |
| `weekly_hours` | Between 1 and 168 |
| All score fields | Between 0.0 and 100.0 |
| `economic_index` | Between -100.0 and 100.0 |
| `bonus_usd` | Non-negative, max $10,000,000 |
| `offer_acceptance_rate` | Cannot be 0 for Senior/Lead roles |

---

## 💡 LEARNING OUTCOMES
- Built an **end-to-end ML pipeline using Pipeline & ColumnTransformer**
- Learned difference between **linear and tree-based models**
- Applied **feature engineering and transformation techniques**
- Implemented **hyperparameter tuning with cross-validation**
- Compared models and selected the best one automatically
- Deployed the model as a **production-ready REST API using FastAPI**
- Applied **Pydantic v2 custom validators** for robust input validation
- Built an **interactive frontend using Streamlit**

---

## 🚀 FUTURE IMPROVEMENTS
- Feature importance analysis using SHAP
- Add Gradient Boosting / XGBoost
- Deploy to cloud (AWS / Render / Railway)

---

## 🛠 TECH STACK
- Python
- pandas, NumPy
- scikit-learn
- FastAPI
- Pydantic v2
- Joblib
- Uvicorn
- Streamlit

---

## 📁 PROJECT STRUCTURE
```
AI_Job_Prediction/
├── Dataset/
│   └── global_ai_jobs.csv
├── Jobs_Salary_Prediction.py
├── analysis.ipynb
├── app.py
├── config.yml
├── predict.py
├── user_input.py
├── streamlit_app.py
├── model.pkl
├── Dockerfile
├── start.sh
├── requirements.txt
└── README.md
```

---

## 👤 AUTHOR
**Inam Ur Rehman**
BS Computer Engineering
Focus: Machine Learning | Deep Learning | AI Engineering