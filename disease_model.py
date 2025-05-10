import pandas as pd
import numpy as np
import joblib
import warnings
from utils import symptoms_to_features, extract_symptoms

model = None
symptom_columns = None
last_predicted_disease = None  # 🌍 Global variable

def load_disease_model():
    global model, symptom_columns
    model = joblib.load("models/disease_model.pkl")
    symptom_columns = joblib.load("models/symptom_columns.pkl")

def predict_disease_from_text(user_input, synonym_map):
    global last_predicted_disease

    extracted = extract_symptoms(user_input, synonym_map)
    features = symptoms_to_features(extracted, symptom_columns)
    input_df = pd.DataFrame([features], columns=symptom_columns)

    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=UserWarning)
        predicted = model.predict(input_df)[0]

    last_predicted_disease = predicted  # Store result

    print(f"🩺 Based on what you told me, it *could* be: **{predicted}**! 🤔")
    print("💡 I’d still recommend seeing a doctor to be 100% sure. Stay strong, you’ve got this! 💪")

    return predicted


