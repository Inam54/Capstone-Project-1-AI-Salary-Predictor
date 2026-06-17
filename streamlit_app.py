import os

import requests
import streamlit as st

API_URL = "capstone-project-1-ai-salary-predictor.onrender.com"

st.set_page_config(page_title="AI Salary Predictor", page_icon="💼")

st.title("AI Salary Predictor")
st.write("Fill in the details below to predict an AI job salary.")
st.divider()

# Job Info
st.subheader("Job Information")
country = st.text_input("Country")
job_role = st.text_input("Job Role")
ai_specialization = st.text_input("AI Specialization")
industry = st.text_input("Industry")
education_required = st.text_input("Education Required")
work_mode = st.selectbox("Work Mode", ["Remote", "Hybrid", "On-site"])

st.divider()

# Role Details
st.subheader("Role Details")
experience_level = st.selectbox("Experience Level", ["Entry", "Mid", "Senior", "Lead"])
company_size = st.selectbox("Company Size", ["Startup", "Small", "Medium", "Large", "Enterprise"])

st.divider()

# Work & Compensation
st.subheader("Work & Compensation")
weekly_hours = st.number_input("Weekly Hours", min_value=1, max_value=168, value=40)
bonus_usd = st.number_input("Bonus (USD)", min_value=0, max_value=10000000, value=5000, step=500)

st.divider()

# Scores
st.subheader("Scores (0 - 100)")
hiring_difficulty_score = st.slider("Hiring Difficulty", 0, 100, 50)
ai_adoption_score = st.slider("AI Adoption", 0, 100, 60)
offer_acceptance_rate = st.slider("Offer Acceptance Rate", 0, 100, 70)
skill_demand_score = st.slider("Skill Demand", 0, 100, 75)
automation_risk = st.slider("Automation Risk", 0, 100, 30)
job_security_score = st.slider("Job Security", 0, 100, 65)
career_growth_score = st.slider("Career Growth", 0, 100, 70)
work_life_balance_score = st.slider("Work-Life Balance", 0, 100, 60)
promotion_speed = st.slider("Promotion Speed", 0, 100, 55)
salary_percentile = st.slider("Salary Percentile", 0, 100, 50)
employee_satisfaction = st.slider("Employee Satisfaction", 0, 100, 65)
tax_rate_percent = st.slider("Tax Rate %", 0, 100, 25)
economic_index = st.slider("Economic Index", -100, 100, 30)

st.divider()

# Predict
if st.button("Predict Salary"):

    if any(len(x.strip()) < 2 for x in [country, job_role, ai_specialization, industry, education_required]):
        st.error("All text fields must have at least 2 characters.")
        st.stop()

    else:
        payload = {
            "country": country,
            "job_role": job_role,
            "ai_specialization": ai_specialization,
            "industry": industry,
            "work_mode": work_mode,
            "education_required": education_required,
            "experience_level": experience_level,
            "company_size": company_size,
            "weekly_hours": float(weekly_hours),
            "hiring_difficulty_score": float(hiring_difficulty_score),
            "ai_adoption_score": float(ai_adoption_score),
            "economic_index": float(economic_index),
            "offer_acceptance_rate": float(offer_acceptance_rate),
            "tax_rate_percent": float(tax_rate_percent),
            "skill_demand_score": float(skill_demand_score),
            "automation_risk": float(automation_risk),
            "job_security_score": float(job_security_score),
            "career_growth_score": float(career_growth_score),
            "work_life_balance_score": float(work_life_balance_score),
            "promotion_speed": float(promotion_speed),
            "salary_percentile": float(salary_percentile),
            "employee_satisfaction": float(employee_satisfaction),
            "bonus_usd": float(bonus_usd)
        }

        try:
            response = requests.post(f"{API_URL}/predict", json=payload, timeout=60)

            if response.status_code == 200:
                data = response.json()
                st.success(f"Predicted Salary: ${data['predicted_salary_usd']:,.2f} / year")
                st.caption(f"Model: {data['model_used']}")

            elif response.status_code == 422:
                errors = response.json().get("detail", [])
                for e in errors:
                    st.error(e["msg"])

            else:
                body = response.json()
                error = body.get("detail") or body.get("error") or "Something went wrong."
                st.error(error)

        except requests.exceptions.ConnectionError:
            st.error(f"Could not connect to API at {API_URL}. Check that the FastAPI service is running.")
        except requests.exceptions.Timeout:
            st.error(f"API request timed out. The service at {API_URL} may be waking up — try again in a moment.")
