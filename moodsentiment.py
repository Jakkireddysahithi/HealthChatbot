from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
import csv
from datetime import datetime

class HealthcareMentalHealthBot:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
        self.model = AutoModelForSequenceClassification.from_pretrained("cardiffnlp/twitter-roberta-base-sentiment")
        self.labels = ['negative', 'neutral', 'positive']
        self.mood = "neutral"

    def get_mood(self):
        return {"positive": "happy", "negative": "sad", "neutral": "neutral"}[self.mood]

    def update_mood(self, sentence):
        encoded_input = self.tokenizer(sentence, return_tensors='pt')#sentence here converted into tokens
        output = self.model(**encoded_input)#process the tokenized input returns raw prediction score
        scores = output[0][0].detach().numpy()#output model converted into numpy array
        scores = torch.nn.functional.softmax(torch.tensor(scores), dim=0).numpy()#this is for overall conversation until certain point
        #it will take the cumulative probability
        self.mood = self.labels[np.argmax(scores)] #max probability score gets the highest probability

    def process_input(self, sentence):
        if "mood" in sentence.lower():
            return f"Your current mood is: {self.get_mood()}"
        self.update_mood(sentence)
        return f"Sentiment detected! Your mood is updated to: {self.get_mood()}"
    
    def log_mood(self, filename="C:\\Documents\\projects\\NewChatbot\\data\\mood_journal.csv"):
        with open(filename, mode='a', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            # Log the current timestamp and mood to save into mymood file 
            writer.writerow([timestamp, self.get_mood()])  

    
