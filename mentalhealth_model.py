import json
import random
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
import joblib

model = None
intent_data = None

def load_intent_data():
    global model, intent_data
    with open("C:\\Documents\\projects\\NewChatbot\\data\\mentalhealthintent.json", "r", encoding="utf-8") as f:
        intent_data = json.load(f)

    sentences = []
    labels = []

    for intent in intent_data['intents']:
        for pattern in intent['patterns']:
            sentences.append(pattern)
            labels.append(intent['tag'])

    model = Pipeline([
        ('tfidf', TfidfVectorizer()),
        ('clf', MultinomialNB())
    ])
    model.fit(sentences, labels)

def predict_intent(user_input, return_confidence=False):
    # Predict the intent
    predicted_label = model.predict([user_input])[0]

    if return_confidence:
        # Get the probability of the predicted label
        probabilities = model.predict_proba([user_input])[0]
        confidence = max(probabilities)
        return predicted_label, confidence

    return predicted_label


def get_response(intent_tag):
    for intent in intent_data['intents']:
        if intent['tag'] == intent_tag:
            return random.choice(intent['responses'])


