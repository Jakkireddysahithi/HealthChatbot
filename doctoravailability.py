department_options = {
    "1": "cardiology",
    "2": "neurology",
    "3": "urology",
    "4": "ent",
    "5": "radiology",
    "6": "nutrition",
    "7": "general_medicine",
    "8": "dermatology",
    "9": "mental_health",
    "10": "gynecology",
    "11": "pediatrics",
    "12": "orthopedics"
}

def get_department_prompt():
    return (
        "🏥 *Please choose a department by typing the number (1–12):*\n"
        "1. Cardiology\n2. Neurology\n3. Urology\n4. ENT\n5. Radiology\n6. Nutrition\n"
        "7. General Medicine\n8. Dermatology\n9. Mental Health\n10. Gynecology\n"
        "11. Pediatrics\n12. Orthopedics"
    )

def get_doctor_availability(user_input, doctor_data):
    user_choice = user_input.strip()
    
    if user_choice not in department_options:
        return "❗ Please enter a valid department number (1–12).", True

    department = department_options[user_choice]
    doctors = doctor_data.get(department, [])
    
    if not doctors:
        return f"❌ No doctors listed for *{department.title()}*.", False

    response = f"🩺 *Available doctors in {department.replace('_', ' ').title()}*:\n"
    for doc in doctors:
        schedule = "\n".join([f"   • {day}: {time}" for day, time in doc["availability"].items()])
        response += f"\n👨‍⚕️ *{doc['name']}*:\n{schedule}\n"
    
    return response, False
