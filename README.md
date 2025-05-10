Healthcare & Mental Wellness Chatbot

This project is a conversational AI assistant designed to simulate real-world hospital and clinic interactions. It can help users check symptoms, suggest possible diseases, recommend precautions, check doctor availability by department, and book appointments — all through natural language conversation.
 Features
Intent Detection: Classifies user input using a TF-IDF + Naive Bayes pipeline.

Symptom-Based Disease Prediction: Uses custom-trained models to detect illnesses based on described symptoms.

Precaution Suggestion: Offers medical precautions based on recognized conditions.

Doctor Availability: Guides the user to select a department (e.g., cardiology, neurology), then displays available doctors and schedules.

Appointment Booking: Extracts times/dates from text (via regex-based entity recognition) and simulates appointment scheduling.

Spelling & Grammar Correction: Fixes errors in user input when prediction confidence is low (using TextBlob and a T5 model).

Mental Health Tracker: Tracks mood over conversations and supports journaling and visualization.

Technologies Used

Python 3
Scikit-learn: For intent classification and disease prediction (Naive Bayes, SVM, Random Forest)
Natural Language Toolkit (NLTK): For preprocessing (tokenization, stemming, stopword removal)
Regex-based NER: For extracting time and appointment-related entities
TextBlob / T5 Model: For spelling and grammar correction
JSON / CSV: Stores intent patterns, symptom data, doctor availability, and user mood logs
