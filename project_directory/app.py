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
    data = request.json
    
    # Generate the prompt
    prompt = generate_prompt(data)
    
    try:
        # Make the API request using the updated method
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
    )

def generate_prompt(data):
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
