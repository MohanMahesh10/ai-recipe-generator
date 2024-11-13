from flask import Flask, render_template, request, jsonify
import google.generativeai as genai
from config import GEMINI_API_KEY
import json

app = Flask(__name__)

# Configure Gemini API
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/generate_recipe', methods=['POST'])
def generate_recipe():
    data = request.get_json()
    ingredients = data.get('ingredients', [])
    dietary_preferences = data.get('dietary_preferences', '')
    
    prompt = f"""
    Create a recipe using these ingredients: {', '.join(ingredients)}
    Dietary preferences: {dietary_preferences}
    
    Please provide the recipe in this JSON format:
    {{
        "name": "Recipe Name",
        "ingredients": ["ingredient1", "ingredient2"],
        "instructions": ["step1", "step2"],
        "nutrition": {{
            "calories": "xxx",
            "protein": "xxx",
            "carbs": "xxx",
            "fat": "xxx"
        }}
    }}
    """
    
    response = model.generate_content(prompt)
    try:
        recipe_data = json.loads(response.text)
        return jsonify(recipe_data)
    except:
        return jsonify({"error": "Failed to generate recipe"}), 400

if __name__ == '__main__':
    app.run(debug=True) 