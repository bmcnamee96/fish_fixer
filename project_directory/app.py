from flask import Flask, request, jsonify, send_from_directory
import openai
import json
import re
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

MODEL = "gpt-3.5-turbo"

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
    # Define the system message with the diagnosis guidelines
    return (
        "You are a fish health expert. Your job is to analyze the provided information to diagnose the fish’s condition and recommend treatments. Follow these guidelines:\n"
        "1. **Diagnosis**:\n"
        "- Provide the most likely diagnosis based on the provided symptoms, water quality, and environment.\n"
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
