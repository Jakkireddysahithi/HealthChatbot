import json
import os
from dateutil import parser as dt_parser

session = {
    "appointment_stage": None,
    "appointment_data": {}
}

def extract_date_time(user_input):
    try:
        user_input = user_input.lower().replace("schedule", "").replace("appointment", "")
        dt = dt_parser.parse(user_input, fuzzy=True)
        date_str = dt.strftime("%Y-%m-%d")
        time_str = dt.strftime("%H:%M")
        return date_str, time_str
    except Exception:
        return None, None

def start_booking():
    session["appointment_stage"] = "name"
    session["appointment_data"] = {}
    return "Let's start booking your appointment. What is your name?"

def handle_booking_input(user_input):
    stage = session.get("appointment_stage")
    data = session.get("appointment_data", {})

    if stage == "name":
        data["name"] = user_input
        date_guess = session.pop("pre_date", None)
        time_guess = session.pop("pre_time", None)

        if date_guess and time_guess:
            data["date"] = date_guess
            data["time"] = time_guess
            session["appointment_stage"] = "doctor"
            session["appointment_data"] = data
            return f"Got it! Booking for {date_guess} at {time_guess}. Do you have a preferred doctor👨? If not, type 'no':"
        else:
            session["appointment_stage"] = "date"
            session["appointment_data"] = data
            return "Please enter the preferred date📅 (YYYY-MM-DD):"

    elif stage == "date":
        data["date"] = user_input
        session["appointment_stage"] = "time"
        session["appointment_data"] = data
        return "Please enter the preferred time🕜 (e.g., 14:30):"

    elif stage == "time":
        data["time"] = user_input
        session["appointment_stage"] = "doctor"
        session["appointment_data"] = data
        return "Do you have a preferred doctor👨‍⚕️? If not, type 'no':"

    elif stage == "doctor":
        data["doctor"] = user_input if user_input.lower() != "no" else "Any available"

        file_path = "appointments.json"
        if os.path.exists(file_path):
            with open(file_path, "r") as f:
                appointments = json.load(f)
        else:
            appointments = []

        appointments.append(data)
        with open(file_path, "w") as f:
            json.dump(appointments, f, indent=4)

        session["appointment_stage"] = None
        session["appointment_data"] = {}
        return "Your appointment has been booked successfully😀!"

def is_booking_in_progress():
    return session.get("appointment_stage") in {"name", "date", "time", "doctor"}