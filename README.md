# 🍎 NutriChat: Your Smart AI Food Guide

An intelligent chatbot that provides personalized dietary advice for various health conditions, powered by a fine-tuned language model. This project was developed for the *Confluentia Hackathon*.



## ## About The Project

Navigating dietary restrictions for health conditions like Diabetes or Hypertension can be confusing. NutriChat aims to solve this by providing a simple, form-based interface where users can select their health condition and ask about specific foods to receive instant, personalized, and easy-to-understand nutritional advice.

The chatbot leverages a knowledge base of over 100 food-condition combinations and uses a fine-tuned GPT-2 model to generate helpful, human-like explanations.

---
## ## Features

* *Simple User Interface:* Select a health condition from a dropdown list and type in a food name.
* *Personalized Advice:* Get recommendations tailored to a wide range of health conditions.
* *AI-Powered Explanations:* The chatbot uses a fine-tuned language model to explain why a food is good, bad, or should be eaten in moderation.
* *Extensible Knowledge Base:* The chatbot's knowledge can be easily expanded by adding new data to its CSV files.
* *Interactive Web App:* Built with Streamlit for a clean and user-friendly experience.

---
## ## Tech Stack

* *Backend:* Python
* *Web Framework:* Streamlit
* *Machine Learning:* Hugging Face Transformers, PyTorch
* *Data Handling:* Pandas

---
## ## Getting Started

To get a local copy up and running, follow these simple steps.

### ### Prerequisites

Make sure you have Python 3.9 or higher installed on your system.

### ### Installation

1.  *Clone the repository:*
    sh
    git clone [https://github.com/your-username/nutrichat-app.git](https://github.com/your-username/nutrichat-app.git)
    
2.  *Navigate to the project directory:*
    sh
    cd nutrichat-app
    
3.  *Install the required packages:*
    sh
    pip install -r requirements.txt
    
4.  *Run the Streamlit app:*
    sh
    streamlit run app.py
    
The application will open in your web browser.

---
## ## How It Works

1.  *User Input:* The user selects a health condition from the dropdown menu and types a food name into the text input box.
2.  *Keyword Matching:* The app identifies the food name from the user's input.
3.  *Knowledge Retrieval:* It looks up the identified food and the selected condition in its factual database (foods.csv) to get a base recommendation (e.g., "Good", "Avoid") and a key reason.
4.  *Prompt Engineering:* The retrieved information is constructed into a detailed prompt for the AI model.
5.  *Response Generation:* The fine-tuned GPT-2 model receives the prompt and generates a new, conversational, and detailed explanation.
6.  *Display:* The final advice is displayed to the user in the Streamlit interface.
