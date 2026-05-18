# Import necessary libraries
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from user_input import UserInput
from predict import model, predict_output
import pandas as pd
    
app = FastAPI()
@app.get("/")
def root():
    return {"message": "AI Salary Predictor API is running."}

@app.get("/health")
def health():
    return {
        "status": "ok",
        "model_loaded": model is not None,
        "model_type": "Random Forest (Tuned)"
    }

# Prediction Endpoint
@app.post("/predict")
def predict(data: UserInput):
    if model is None:
        return HTTPException(
            status_code=503,
            detail={"error": "Model not loaded. Ensure model.pkl exists."}
        )

    input_df = pd.DataFrame([data.model_dump()])

    try:
        prediction = predict_output(input_df)
    except Exception as e:
        return HTTPException(
            status_code=500,
            detail={"error": f"Prediction error: {str(e)}"}
        )

    return JSONResponse(
        status_code=200,
        content={
            "predicted_salary_usd": round(float(prediction), 2),
            "model_used": "Random Forest (Tuned)"
        }
    )