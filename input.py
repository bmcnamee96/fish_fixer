def system_message():
    # Define the system message with the diagnosis guidelines
    return (
        "You are a fish health expert. Your job is to analyze the provided information to diagnose the fish’s condition and recommend treatments. Follow these guidelines:\n"
        "1. **Diagnosis**:\n"
        "- Provide the top most likely diagnosis based on the provided symptoms, water quality, and environment.\n"
        "- If there are multiple possible diagnoses, list the top ones with brief explanations.\n"
        "2. **Symptoms to Monitor**:\n"
        "- List any additional symptoms that could help confirm the diagnosis or indicate other issues.\n"
        "3. **Treatment Recommendations**:\n"
        "- Suggest up to 4 treatments or actions to address the diagnosis.\n"
        "- Include both medication options and other actions, such as changes to the environment or care routine.\n"
        "Use the provided data to make the best possible diagnosis and suggestions. Ensure recommendations are practical and based on common fish health practices."
    )

def generate_prompt(data):
    # Create the prompt with the user data
    return (
        "Here is the fish health information:\n\n"
        "Details:\n"
        f"Water Type: {data.get('waterType', 'N/A')}\n"
        f"Species: {data.get('species', 'N/A')}\n"
        f"Approximate Age: {data.get('age', 'N/A')}\n"
        f"Approximate Length: {data.get('length', 'N/A')}\n"
        f"Approximate Weight: {data.get('weight', 'N/A')}\n"
        f"Number of Fish Affected: {data.get('number_affected', 'N/A')}\n\n"
        "Symptoms:\n"
        f"{', '.join(data.get('symptoms', []))}\n\n"
        f"Behavioral Changes: {data.get('behavioralChanges', 'N/A')}\n"
        f"Length of Sickness: {data.get('lengthOfSickness', 'N/A')}\n"
        f"Severity: {data.get('severity', 'N/A')}\n\n"
        "Water Quality Parameters:\n"
        f"Temperature: {data.get('temperature', 'N/A')}\n"
        f"pH: {data.get('pH', 'N/A')}\n"
        f"Hardness: {data.get('hardness', 'N/A')}\n"
        f"Nitrite: {data.get('nitrite', 'N/A')}\n"
        f"Nitrate: {data.get('nitrate', 'N/A')}\n"
        f"Ammonia: {data.get('ammonia', 'N/A')}\n"
        f"Dissolved Oxygen: {data.get('dissolvedOxygen', 'N/A')}\n"
        f"Conductivity: {data.get('conductivity', 'N/A')}\n"
        f"Turbidity: {data.get('turbidity', 'N/A')}\n"
        f"Other Parameters: {data.get('otherParameters', 'N/A')}\n\n"
        "Environment:\n"
        f"Type: {data.get('environmentType', 'N/A')}\n"
        f"Size: {data.get('size', 'N/A')}\n"
        f"Water Change Schedule: {data.get('waterChangeSchedule', 'N/A')}\n"
        f"Recent Changes: {data.get('recentChanges', 'N/A')}\n"
        f"Feeding Habits: {data.get('feedingHabits', 'N/A')}\n"
        f"Other Species: {data.get('otherSpecies', 'N/A')}\n"
        f"Maintenance Routine: {data.get('maintenanceRoutine', 'N/A')}\n\n"
        "History:\n"
        f"Past Illness: {data.get('pastIllness', 'N/A')}\n"
        f"Current Treatments: {data.get('currentTreatments', 'N/A')}\n\n"
        "Please provide a detailed diagnosis and up to 4 treatment options."
    )

def preprocess_input(data):
    # Remove keys with no value (empty strings, None, or empty lists)
    def clean_data(d):
        return {k: v for k, v in d.items() if v not in [None, '', [], {}]}
    
    summary = clean_data({
        "waterType": data.get("waterType"),
        "species": data.get("species"),
        "age": data.get("age"),
        "length": data.get("length"),
        "weight": data.get("weight"),
        "number_affected": data.get("number_affected"),
        "symptoms": ", ".join(data.get("symptoms", []))[:100] if data.get("symptoms") else None,
        "behavioralChanges": data.get("behavioralChanges", "")[:100] if data.get("behavioralChanges") else None,
        "lengthOfSickness": data.get("lengthOfSickness"),
        "severity": data.get("severity"),
        "waterQuality": clean_data({
            "temperature": data.get("temperature"),
            "pH": data.get("pH"),
            "hardness": data.get("hardness"),
            "nitrite": data.get("nitrite"),
            "nitrate": data.get("nitrate"),
            "ammonia": data.get("ammonia"),
            "dissolvedOxygen": data.get("dissolvedOxygen"),
            "conductivity": data.get("conductivity"),
            "turbidity": data.get("turbidity")
        }),
        "environment": clean_data({
            "type": data.get("environmentType"),
            "size": data.get("size"),
            "waterChangeSchedule": data.get("waterChangeSchedule"),
            "recentChanges": data.get("recentChanges", "")[:100] if data.get("recentChanges") else None,
            "feedingHabits": data.get("feedingHabits"),
            "otherSpecies": data.get("otherSpecies"),
            "maintenanceRoutine": data.get("maintenanceRoutine")
        }),
        "history": clean_data({
            "pastIllness": data.get("pastIllness"),
            "currentTreatments": data.get("currentTreatments")
        })
    })
    
    # Remove nested dictionaries if they end up empty
    summary = {k: v for k, v in summary.items() if v}
    
    return summary


data = {
    "waterType": "Freshwater",
    "species": "Goldfish",
    "age": "2 years",
    "length": "",
    "weight": "",
    "number_affected": 3,
    "symptoms": ["lethargy", "loss of appetite", "swimming erratically"],
    "behavioralChanges": "The fish are staying near the bottom of the tank and avoiding food.",
    "lengthOfSickness": "1 week",
    "severity": "",
    "temperature": "72°F",
    "pH": "7.2",
    "hardness": "",
    "nitrite": "0",
    "nitrate": "20",
    "ammonia": "0",
    "dissolvedOxygen": "",
    "conductivity": "",
    "turbidity": "",
    "otherParameters": "None",
    "environmentType": "Tank",
    "size": "20 gallons",
    "waterChangeSchedule": "Weekly 25% water change",
    "recentChanges": "Recently added a new plant",
    "feedingHabits": "Fed twice daily with flakes",
    "otherSpecies": "None",
    "maintenanceRoutine": "Filter cleaned monthly, gravel vacuumed weekly",
    "pastIllness": "None",
    "currentTreatments": "No treatments administered yet"
}


print(preprocess_input(data))