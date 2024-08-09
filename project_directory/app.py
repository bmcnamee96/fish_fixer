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
    form_data = request.form.to_dict()
    file = request.files.get('photo')
    
    # Process the file if it is uploaded
    if file:
        # Example of saving the file (you can adjust this as needed)
        file.save(f'/path/to/save/{file.filename}')
        print(f"File saved: {file.filename}")

    # Generate the prompt
    prompt = generate_prompt(preprocess_data(form_data))
    
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

def preprocess_data(data):
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
        }),
        "image": data.get("image")  # Add image data handling
    })
    
    # Remove nested dictionaries if they end up empty
    summary = {k: v for k, v in summary.items() if v}
    
    return summary

summary = preprocess_data

def generate_prompt(summary):
    prompt = (
        "Here is the information provided:\n"
        f"**Water Type:** {summary.get('waterType', 'N/A')}\n"
        f"**Species:** {summary.get('species', 'N/A')}\n"
        f"**Age:** {summary.get('age', 'N/A')}\n"
        f"**Number Affected:** {summary.get('number_affected', 'N/A')}\n"
        f"**Symptoms:** {summary.get('symptoms', 'N/A')}\n"
        f"**Behavioral Changes:** {summary.get('behavioralChanges', 'N/A')}\n"
        f"**Length of Sickness:** {summary.get('lengthOfSickness', 'N/A')}\n"
        f"**Water Quality:**\n"
        f"  - **Temperature:** {summary.get('waterQuality', {}).get('temperature', 'N/A')}\n"
        f"  - **pH:** {summary.get('waterQuality', {}).get('pH', 'N/A')}\n"
        f"  - **Hardness:** {summary.get('waterQuality', {}).get('hardness', 'N/A')}\n"
        f"  - **Nitrite:** {summary.get('waterQuality', {}).get('nitrite', 'N/A')}\n"
        f"  - **Nitrate:** {summary.get('waterQuality', {}).get('nitrate', 'N/A')}\n"
        f"  - **Ammonia:** {summary.get('waterQuality', {}).get('ammonia', 'N/A')}\n"
        f"  - **Dissolved Oxygen:** {summary.get('waterQuality', {}).get('dissolvedOxygen', 'N/A')}\n"
        f"  - **Conductivity:** {summary.get('waterQuality', {}).get('conductivity', 'N/A')}\n"
        f"  - **Turbidity:** {summary.get('waterQuality', {}).get('turbidity', 'N/A')}\n"
        f"**Environment:**\n"
        f"  - **Type:** {summary.get('environment', {}).get('type', 'N/A')}\n"
        f"  - **Size:** {summary.get('environment', {}).get('size', 'N/A')}\n"
        f"  - **Water Change Schedule:** {summary.get('environment', {}).get('waterChangeSchedule', 'N/A')}\n"
        f"  - **Recent Changes:** {summary.get('environment', {}).get('recentChanges', 'N/A')}\n"
        f"  - **Feeding Habits:** {summary.get('environment', {}).get('feedingHabits', 'N/A')}\n"
        f"  - **Other Species:** {summary.get('environment', {}).get('otherSpecies', 'N/A')}\n"
        f"  - **Maintenance Routine:** {summary.get('environment', {}).get('maintenanceRoutine', 'N/A')}\n"
        f"**History:**\n"
        f"  - **Past Illness:** {summary.get('history', {}).get('pastIllness', 'N/A')}\n"
        f"  - **Current Treatments:** {summary.get('history', {}).get('currentTreatments', 'N/A')}\n"
    )
    
    return prompt

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
