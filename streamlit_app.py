import streamlit as st
import google.generativeai as genai
import json
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="AI Recipe Generator",
    page_icon="🍳",
    layout="centered"
)

# Configure Gemini API
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        background-color: #2ecc71;
        color: white;
    }
    .stButton>button:hover {
        background-color: #27ae60;
    }
    .ingredient-item {
        background-color: #f0f0f0;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.2rem;
        display: inline-block;
    }
    </style>
    """, unsafe_allow_html=True)

# Title and description
st.title("🍳 AI Recipe Generator")
st.markdown("Turn your available ingredients into delicious meals!")

# Initialize session state for ingredients
if 'ingredients' not in st.session_state:
    st.session_state.ingredients = []

# Ingredient input
col1, col2 = st.columns([3, 1])
with col1:
    ingredient = st.text_input("Enter an ingredient:", key="ingredient_input")
with col2:
    if st.button("Add"):
        if ingredient and ingredient not in st.session_state.ingredients:
            st.session_state.ingredients.append(ingredient)
            st.session_state.ingredient_input = ""  # Clear input
            st.experimental_rerun()

# Display ingredients
if st.session_state.ingredients:
    st.markdown("### Your Ingredients:")
    for i, item in enumerate(st.session_state.ingredients):
        st.markdown(f"""
            <div class="ingredient-item">
                {item} <span onclick="remove_ingredient({i})" style="cursor: pointer;">❌</span>
            </div>
            """, unsafe_allow_html=True)
    
    if st.button("Clear All"):
        st.session_state.ingredients = []
        st.experimental_rerun()

# Dietary preferences
st.markdown("### Dietary Preferences")
dietary_preference = st.selectbox(
    "Select any dietary restrictions:",
    ["None", "Vegetarian", "Vegan", "Gluten-free", "Keto", "Low-carb", "Dairy-free", "Paleo"]
)

# Generate recipe button
if st.button("Generate Recipe", type="primary"):
    if not st.session_state.ingredients:
        st.error("Please add at least one ingredient!")
    else:
        with st.spinner("Creating your perfect recipe..."):
            prompt = f"""
            Create a recipe using these ingredients: {', '.join(st.session_state.ingredients)}
            Dietary preferences: {dietary_preference}
            
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
            
            try:
                response = model.generate_content(prompt)
                recipe_data = json.loads(response.text)
                
                # Display recipe
                st.markdown(f"## 📖 {recipe_data['name']}")
                
                # Ingredients
                st.markdown("### 🥗 Ingredients")
                for ing in recipe_data['ingredients']:
                    st.markdown(f"- {ing}")
                
                # Instructions
                st.markdown("### 📝 Instructions")
                for i, step in enumerate(recipe_data['instructions'], 1):
                    st.markdown(f"{i}. {step}")
                
                # Nutrition
                st.markdown("### 📊 Nutrition Information")
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Calories", recipe_data['nutrition']['calories'])
                with col2:
                    st.metric("Protein", recipe_data['nutrition']['protein'])
                with col3:
                    st.metric("Carbs", recipe_data['nutrition']['carbs'])
                with col4:
                    st.metric("Fat", recipe_data['nutrition']['fat'])
                
            except Exception as e:
                st.error("Failed to generate recipe. Please try again.")
                st.exception(e)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and Google's Gemini AI") 