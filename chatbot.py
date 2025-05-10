import json
import random
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import spacy
#this is for testing only
# ------------------ Load Intents ------------------ #
with open("C:/Documents/projects/NewChatbot/data/intent_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)


sentences = []
labels = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        sentences.append(pattern)
        labels.append(intent['tag'])

# ------------------ Train Classifier ------------------ #
X_train, X_test, y_train, y_test = train_test_split(sentences, labels, test_size=0.2, random_state=42)

model = Pipeline([
    ('tfidf', TfidfVectorizer()),
    ('clf', MultinomialNB())
])

model.fit(X_train, y_train)
y_pred = model.predict(X_test)

print("Evaluation Report:\n")
print(classification_report(y_test, y_pred))

# ------------------ Prediction Functions ------------------ #
def predict_intent(user_input):
    return model.predict([user_input])[0]

def get_response(intent_tag):
    for intent in data['intents']:
        if intent['tag'] == intent_tag:
            return random.choice(intent['responses'])

# ------------------ Chat Loop ------------------ #
print("🤖 Chatbot is ready! Type something (or 'exit' to quit)\n")
while True:
    user_input = input("You: ")
    if user_input.lower() == 'exit':
        print("Bot: Bye! Stay healthy 💖")
        break
    intent = predict_intent(user_input)
    response = get_response(intent)
    print(f"Bot: {response}")

    # ------------------ Optional Symptom Extraction ------------------ #
    # Use spaCy biomedical NER to extract symptoms
    try:
        med_ner = spacy.load("en_ner_bc5cdr_md")
        doc = med_ner(user_input)
        symptoms = [ent.text for ent in doc.ents if ent.label_ == "DISEASE"]
        if symptoms:
            print("🩺 Detected Symptoms:", symptoms)
    except:
        print("Note: Medical symptom extraction model not loaded.")
