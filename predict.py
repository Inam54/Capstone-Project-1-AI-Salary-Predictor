# Import necessary libraries
import joblib

try:
    model = joblib.load('model.pkl')
except FileNotFoundError:
    model = None

def predict_output(input_df):
    return model.predict(input_df)[0]