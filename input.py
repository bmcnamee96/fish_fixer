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
    # Function to clean data and remove empty or irrelevant values
    def clean_data(d):
        return {k: v for k, v in d.items() if v not in [None, '', [], {}]}

    # Clean the input data
    cleaned_data = clean_data({
        "waterType": data.get("waterType"),
        "species": data.get("species"),
        "age": data.get("age"),
        "length": data.get("length"),
        "weight": data.get("weight"),
        "number_affected": data.get("number_affected"),
        "symptoms": ", ".join(data.get("symptoms", [])) if data.get("symptoms") else None,
        "behavioralChanges": data.get("behavioralChanges"),
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
            "recentChanges": data.get("recentChanges"),
            "feedingHabits": data.get("feedingHabits"),
            "otherSpecies": data.get("otherSpecies"),
            "maintenanceRoutine": data.get("maintenanceRoutine")
        }),
        "history": clean_data({
            "pastIllness": data.get("pastIllness"),
            "currentTreatments": data.get("currentTreatments")
        })
    })

    # Remove nested dictionaries if they are empty
    cleaned_data = {k: v for k, v in cleaned_data.items() if v}

    # Construct the prompt dynamically
    prompt_sections = []

    if "waterType" in cleaned_data:
        prompt_sections.append(f"Water Type: {cleaned_data['waterType']}")
    if "species" in cleaned_data:
        prompt_sections.append(f"Species: {cleaned_data['species']}")
    if "age" in cleaned_data:
        prompt_sections.append(f"Approximate Age: {cleaned_data['age']}")
    if "length" in cleaned_data:
        prompt_sections.append(f"Approximate Length: {cleaned_data['length']}")
    if "weight" in cleaned_data:
        prompt_sections.append(f"Approximate Weight: {cleaned_data['weight']}")
    if "number_affected" in cleaned_data:
        prompt_sections.append(f"Number of Fish Affected: {cleaned_data['number_affected']}")
    if "symptoms" in cleaned_data:
        prompt_sections.append(f"Symptoms: {cleaned_data['symptoms']}")
    if "behavioralChanges" in cleaned_data:
        prompt_sections.append(f"Behavioral Changes: {cleaned_data['behavioralChanges']}")
    if "lengthOfSickness" in cleaned_data:
        prompt_sections.append(f"Length of Sickness: {cleaned_data['lengthOfSickness']}")
    if "severity" in cleaned_data:
        prompt_sections.append(f"Severity: {cleaned_data['severity']}")
    
    if "waterQuality" in cleaned_data:
        water_quality = cleaned_data["waterQuality"]
        water_quality_section = "\n".join([f"{k.capitalize()}: {v}" for k, v in water_quality.items()])
        prompt_sections.append(f"Water Quality Parameters:\n{water_quality_section}")
    
    if "environment" in cleaned_data:
        environment = cleaned_data["environment"]
        environment_section = "\n".join([f"{k.replace('type', 'Type').capitalize()}: {v}" for k, v in environment.items()])
        prompt_sections.append(f"Environment:\n{environment_section}")
    
    if "history" in cleaned_data:
        history = cleaned_data["history"]
        history_section = "\n".join([f"{k.replace('pastIllness', 'Past Illness').replace('currentTreatments', 'Current Treatments')}: {v}" for k, v in history.items()])
        prompt_sections.append(f"History:\n{history_section}")

    # Combine all sections into the final prompt
    final_prompt = "Here is the fish health information:\n\n" + "\n\n".join(prompt_sections) + "\n\nPlease provide a detailed diagnosis and up to 4 treatment options."
    
    return final_prompt

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
    "otherParameters": "",
    "environmentType": "Tank",
    "size": "20 gallons",
    "waterChangeSchedule": "Weekly 25% water change",
    "recentChanges": "Recently added a new plant",
    "feedingHabits": "Fed twice daily with flakes",
    "otherSpecies": "None",
    "maintenanceRoutine": "",
    "pastIllness": "None",
    "currentTreatments": "No treatments administered yet"
}

print(generate_prompt(data))