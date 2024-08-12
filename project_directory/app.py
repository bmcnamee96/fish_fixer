from flask import Flask, request, jsonify, send_from_directory
import openai
import json
import re
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

MODEL = "gpt-4o"

app = Flask(__name__, static_folder='static')

user_free_uses = {}

@app.route('/use_service', methods=['POST'])
def use_service():
    # Extract form data and files
    data = request.form.to_dict()
    file = request.files.get('photo')
    
    # Process the file if it is uploaded
    if file:
        # Example of saving the file (you can adjust this as needed)
        file.save(f'/path/to/save/{file.filename}')
        print(f"File saved: {file.filename}")

    # Generate the prompt
    prompt = generate_prompt(data)
    
    try:
        # Make the API request
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Or any other model you are using
            messages=[
                {"role": "system", "content": system_message()},
                {"role": "user", "content": prompt}
            ],
            temperature=0.1,
            max_tokens=750
        )
        
        # Print the API response for debugging
        print('OpenAI response:', json.dumps(response, indent=2))  # Pretty-print JSON response
        
        # Extract the answer from the response
        choices = response.get('choices', [])
        if choices:
            content = choices[0]['message']['content']
            # Remove text within double quotes
            content = re.sub(r'\(.*?\)', '', content).strip()
            return jsonify({'success': True, 'response': content})
        else:
            raise ValueError("Unexpected response format")
            
    except Exception as e:
        # Print the error for debugging
        print('Error:', str(e))
        return jsonify({'success': False, 'message': str(e)}), 500

def system_message():
    # Define the system message with concise diagnosis guidelines
    return (
        "You are a fish health expert. Diagnose the fish’s condition and recommend treatments based on the provided information:\n\n"
        "**Diagnosis**:\n"
        "- Identify the most likely condition based on symptoms, water quality, and environment.\n"
        "- If relevant, list other possible diagnoses with brief explanations.\n\n"
        "**Symptoms to Monitor**:\n"
        "- Suggest additional symptoms to confirm the diagnosis or identify other issues.\n\n"
        "**Treatment Recommendations**:\n"
        "- Recommend up to 3 treatments or actions, including medications and environmental changes.\n\n"
        "Use the data to provide the best possible diagnosis and practical treatment options."
        "If not enough information is provided, please say 'I can not make a diagnosis with this information, please provide more.'"
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

    print(final_prompt)
    
    return final_prompt

@app.route('/subscribe', methods=['POST'])
def subscribe():
    user_id = request.json.get('user_id')
    # Handle subscription logic here
    return jsonify({"success": True, "message": "Subscription successful"})

@app.route('/')
def index():
    print("Index route accessed")
    return send_from_directory('static', 'index.html')

if __name__ == '__main__':
    app.run(debug=True)
