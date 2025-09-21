import streamlit as st
import pandas as pd
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

# --- Configuration ---
st.set_page_config(page_title="NutriChat", page_icon="🍎", layout="centered")

# --- Model and Data Loading ---
@st.cache_resource
def load_model_and_data():
    """Loads the fine-tuned model, tokenizer, and food database."""
    model_path = "./my-food-chatbot-model-v3"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)
    food_db = pd.read_csv('foods.csv')
    return model, tokenizer, food_db

model, tokenizer, food_db = load_model_and_data()

# --- Core Functions ---

def generate_response(prompt):
    """Generates a response from the fine-tuned model."""
    try:
        # --- FIX 1: Use the tokenizer directly, not tokenizer.encode ---
        # This creates a dictionary containing both 'input_ids' and the 'attention_mask'.
        inputs = tokenizer(prompt, return_tensors="pt")
        
        # --- FIX 2: Unpack the dictionary into the generate function using ** ---
        # This passes both input_ids and attention_mask to the model correctly.
        outputs = model.generate(
            **inputs, 
            max_new_tokens=60,
            num_return_sequences=1,
            no_repeat_ngram_size=2,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id,
            temperature=0.7,
            top_k=50
        )
        
        # We only need to decode the newly generated tokens
        response_text = tokenizer.decode(outputs[0][inputs['input_ids'].shape[-1]:], skip_special_tokens=True)
        
        return response_text.strip()
    except Exception as e:
        return f"An error occurred during generation: {e}"

def get_food_recommendation_info(query, condition):
    """Finds food in query and gets its basic recommendation info from the CSV."""
    all_foods = food_db['FoodName'].unique()
    found_food = None
    for food in all_foods:
        if food.lower() in query.lower():
            found_food = food
            break
            
    if not found_food:
        return None, None, None
        
    result = food_db[
        (food_db['FoodName'] == found_food) & 
        (food_db['Condition'] == condition)
    ]
    
    if result.empty:
        return found_food, None, None
        
    return found_food, result.iloc[0]['Recommendation'], result.iloc[0]['Explanation']

# --- Streamlit User Interface ---

st.title("🍎 NutriChat: Your Smart Food Guide")
st.markdown("I'm an AI assistant trained to provide dietary advice. Ask me questions like, 'Are apples good for hypertension?'")

# Get a unique, sorted list of conditions from the dataframe
conditions_list = sorted(food_db['Condition'].unique())

user_condition = st.selectbox(
    'First, select your primary health condition:',
    conditions_list,
    key='condition_selector'
)

user_query = st.text_input('Ask your food-related question here:', key='query_input')

if st.button('Get Advice', key='get_advice_button'):
    if user_query and user_condition:
        with st.spinner('Thinking...'):
            food, recommendation, base_explanation = get_food_recommendation_info(user_query, user_condition)
            
            if not food:
                st.warning("I couldn't identify a food in your question. Please try rephrasing.")
            elif not recommendation:
                st.info(f"I don't have specific data for '{food}' regarding '{user_condition}' in my base knowledge.")
            else:
                prompt = (
                    f"A user with {user_condition} asks about eating {food}. "
                    f"The recommendation is '{recommendation}'. "
                    f"Explain why in a helpful, conversational tone, based on this key fact: '{base_explanation}'"
                    f"\n\nHelpful Advice: "
                )
                
                generated_completion = generate_response(prompt)
                
                st.subheader(f"Advice for eating '{food}' with '{user_condition}':")
                st.markdown(f"*Base Recommendation:* {recommendation}")
                st.markdown("*Generated Advice:*")
                if generated_completion:
                    st.info(generated_completion)
                else:
                    st.warning("The model did not generate a specific reason. This might be a rare case or require more training data.")
    else:
        st.error("Please select a condition and ask a question.")