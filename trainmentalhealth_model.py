import json
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import classification_report
import joblib

# Load intent data
with open("C:\\Documents\\projects\\NewChatbot\\data\\mentalhealthintent.json", 'r', encoding='utf-8') as f:
    data = json.load(f)

sentences = []
labels = []

# Process data
for intent in data['intents']:
    for pattern in intent['patterns']:
        sentences.append(pattern)
        labels.append(intent['tag'])

# Split data into train/test
X_train, X_test, y_train, y_test = train_test_split(sentences, labels, test_size=0.2, random_state=42)

# Create and train model
model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB())
])
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
print("Evaluation Report:\n")
print(classification_report(y_test, y_pred))

model_path = "C:\\Documents\\projects\\NewChatbot\\models\\mental_health_model.pkl"

# Save model
joblib.dump(model, model_path)