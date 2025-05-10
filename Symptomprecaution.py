import json
import joblib

# Load symptom keywords (from SVM model)
symptom_keywords = joblib.load("C:\\Documents\\projects\\NewChatbot\\models\\symptom_columns.pkl")


# Load extroverted precautions with UTF-8 encoding
with open("C:\\Documents\\projects\\NewChatbot\\data\\precautions.json", "r", encoding="utf-8") as file:
    precautions_data = json.load(file)

# Load symptom synonyms with UTF-8 encoding
with open("C:\\Documents\\projects\\NewChatbot\\data\\synonyms.json", "r", encoding="utf-8") as file:
    synonyms_data = json.load(file)

# Normalize synonyms
normalized_synonyms = {
    key.lower(): [syn.lower() for syn in value]
    for key, value in synonyms_data.items()
}

# Extract symptoms from input
def extract_symptoms(user_input):
    user_input = user_input.lower()
    matched_symptoms = set()

    # Match from actual symptoms
    for symptom in symptom_keywords:
        if symptom in user_input:
            matched_symptoms.add(symptom)

    # Match from synonyms
    for main_symptom, synonyms in normalized_synonyms.items():
        if any(syn in user_input for syn in synonyms):
            matched_symptoms.add(main_symptom)

    return list(matched_symptoms)

# Get extroverted precautions
def get_precautions_response(user_input):
    detected_symptoms = extract_symptoms(user_input)

    if detected_symptoms:
        response = {
            "status": "symptoms_matched",
            "detected_symptoms": list(detected_symptoms),
            "precautions": {}
        }

        for symptom in detected_symptoms:
            if symptom in precautions_data:
                response["precautions"][symptom] = precautions_data[symptom]

        # Combine the detected symptoms and precautions into a single message
        precautions_message = "\n".join(
            [f"{symptom}: {response['precautions'].get(symptom, 'No precautions available')}" for symptom in detected_symptoms]
        )

        response["combined_message"] = f"Detected Symptoms and Precautions:\n{precautions_message}"

        return response

    else:
        return {
            "status": "no_symptoms_found",
            "message": "Oops! I couldn't spot any symptoms. Can you describe what you're feeling in a bit more detail? 😊"
        }



