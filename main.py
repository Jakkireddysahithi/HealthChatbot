from intent_model import load_intent_data as load_health_intents, get_response as get_health_response, predict_intent as health_predict_intent
from disease_model import predict_disease_from_text, load_disease_model
from mentalhealth_model import load_intent_data as load_mh_intents, get_response as get_mh_response, predict_intent as mh_predict_intent
from utils import synonym_map
from moodsentiment import HealthcareMentalHealthBot
from Symptomprecaution import get_precautions_response
from spell_correction import HealthcareSpellGrammarCorrector
from doctoravailability import get_department_prompt, get_doctor_availability
import appointment_model as appt
import json
import random
from visualize import visualize_mood_journal

print("🤖 Health Chatbot Ready! Type your message (or 'exit' to quit)\n")

# Load models once
load_disease_model()
load_health_intents()
load_mh_intents()

# Instantiate classes
mood_bot = HealthcareMentalHealthBot()
corrector = HealthcareSpellGrammarCorrector()
# Load doctor data once
with open("C:\\Documents\\projects\\NewChatbot\\data\\doctoravailability.json") as f:
    doctor_data = json.load(f)

current_bot = "health"

while True:
    user_input = input("You: ")

    if user_input.lower() == 'exit':
        mood_bot.log_mood()
        visualize_mood_journal()
        print("Bot: Take care! 👋")
        break
    

    elif user_input.lower() == 'switch mental':
        current_bot = "mental"
        print("🧠 Switched to Mental Health Bot.\n")
        continue

    elif user_input.lower() == 'switch health':
        current_bot = "health"
        print("🏥 Switched to General Health Bot.\n")
        continue
    if appt.is_booking_in_progress():
        response = appt.handle_booking_input(user_input)
        print(f"Bot: {response}")
        continue

    if current_bot == "health":
        #if the intent confidence in low spell correction is used 
        intent, confidence = health_predict_intent(user_input, return_confidence=True)

        if confidence < 0.50:
            user_input = corrector.correct_grammar(user_input)
            intent, confidence = health_predict_intent(user_input, return_confidence=True)
 

        intent = health_predict_intent(user_input)
        response = get_health_response(intent)
        print(f"Bot (Health): {response}")

        if intent == "symptoms_check":
            disease = predict_disease_from_text(user_input, synonym_map)
            print(f"🩺 Predicted Disease: {disease}")

        elif intent == "precautions":
            while True:
                precaution_result = get_precautions_response(user_input)

                if precaution_result["status"] == "symptoms_matched":
                    print(precaution_result["combined_message"])
                    break
                else:
                    print(precaution_result["message"])
                    user_input = input("You: ")

        elif intent == "book_appointment":
            extracted_date, extracted_time = appt.extract_date_time(user_input)
            appt.session["pre_date"] = extracted_date
            appt.session["pre_time"] = extracted_time

            response = appt.start_booking()
            print(f"Bot: {response}")
            continue
        
        elif intent == "next_available_doctor":
            print(f"Bot: {get_department_prompt()}")
            while True:
                user_input = input("You: ")
                response, ask_again = get_doctor_availability(user_input, doctor_data)
                print(f"Bot: {response}")
                if not ask_again:
                    break 

    else:
        mh_intent, confidence = mh_predict_intent(user_input, return_confidence=True)

        if confidence < 0.60:
            user_input = corrector.correct_grammar(user_input)
            mh_intent, confidence = mh_predict_intent(user_input, return_confidence=True)

        # If intent is get_mood, respond using the tracked mood
        if mh_intent == "get_mood":
            mood = mood_bot.get_mood()
            mood_responses = [
                f"Ooooh, let me guess... 🧠 I think you're feeling: **{mood}**!",
                f"You’re totally radiating **{mood}** vibes! 😄",
                f"Let me check my mood radar... You’re feeling: **{mood}** 🔍"
            ]
            print(f"Bot (Mental): {random.choice(mood_responses)}")
        else:
            mood_bot.update_mood(user_input)  # Update mood on all non-mood-check messages
            mh_response = get_mh_response(mh_intent)
            print(f"Bot (Mental): {mh_response}")




