import json
import re
import os

# Load synonym_map from JSON file
with open("data/synonyms.json", "r", encoding="utf-8") as f:
    synonym_map = json.load(f)

def extract_symptoms(user_input, synonym_map):
    user_input = user_input.lower()
    user_input = re.sub(r'[^a-zA-Z\s]', '', user_input)
    matched_symptoms = set()

    for symptom, synonyms in synonym_map.items():
        all_terms = [symptom.replace('_', ' ')] + [s.lower() for s in synonyms]
        for term in all_terms:
            if term in user_input:
                matched_symptoms.add(symptom)
                break
    return list(matched_symptoms)

def symptoms_to_features(symptom_list, symptom_columns):
    return [1 if symptom in symptom_list else 0 for symptom in symptom_columns]


