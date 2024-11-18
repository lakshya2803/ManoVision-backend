from flask import request, jsonify
import uuid
import google.generativeai as genai
import os
from dotenv import load_dotenv

# load_dotenv("config/config.env")

# Set up your API key
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")

chat_sessions = {}

def chat_with_ai():
    print("Welcome to the AI chatbot! Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        
        if user_input.lower() == 'exit':
            print("Chatbot: Goodbye!")
            break
        
        # Generate response from AI model
        response = model.generate_content(user_input)
        print("Chatbot:", response.text)

def classify_mental_health(text):
    try:
        classification_prompt = (
            f"Classify the following question as 'Mental Health' or 'Not Mental Health':\n\n"
            f"Question: {text}\n"
            f"Answer:"
        )
        # Use the model to classify the input
        classification_response = model.generate_content(classification_prompt)
        classification_result = classification_response.text.strip().lower()
        return "mental health" in classification_result
    except Exception as e:
        print(f"Error in classification: {str(e)}")
        return False

def chatbot():
    try:
        data = request.json
        user_input = data.get('message', '')

        # Generate a new session ID if not provided
        session_id = data.get('session_id', None)
        if not session_id:
            session_id = str(uuid.uuid4())

        
        # Fetch chat history for the session
        if session_id not in chat_sessions:
            chat_sessions[session_id] = []

        chat_history = chat_sessions[session_id]

        # Generate response from AI model using the entire chat history
        # # Initialize the conversation history
        full_conversation = "\n".join([f"{msg['sender']}: {msg['message']}" for msg in chat_history])
        full_conversation += f"\nUser: {user_input}\nMaddy (limit the response to 200 tokens)"

         # Check if the input is related to mental health using classification
        # if not classify_mental_health(user_input):
        #     bot_response = "Maddy: Please ask questions related to mental health. I'm here to support you!"
        #     return jsonify({"message":"enter valid question"}),404
        # else:
        #     # Generate response from AI model with a token limit of 200
        #     full_conversation = "\n".join([f"{msg['sender']}: {msg['message']}" for msg in chat_history])
        #     full_conversation += f"\nUser: {user_input}\nMaddy (limit the response to 200 tokens)"
            
        #     try:
        #         response = model.generate_content(
        #             full_conversation,
        #         )
        #         bot_response = f"Maddy: {response.text.strip()}"
        #     except Exception as e:
        #         print(f"Error generating response: {str(e)}")
        #         bot_response = "Maddy: Sorry, I'm having trouble responding right now. Please try again later."

        response = model.generate_content(
            full_conversation,
        )
        bot_response = f"{response.text.strip()}"

        # Append user and bot responses to chat history
        chat_history.append({"sender": "user", "message": user_input})
        chat_history.append({"sender": "maddy", "message": bot_response})

        # Update session history
        chat_sessions[session_id] = chat_history

        print(bot_response)

        return jsonify({
            "response": bot_response,
            "chat_history": chat_history,
            "session_id": session_id
        }),200
    except Exception as e:
        print(str(e))
        return jsonify({"success" : False, "error" : str(e)}), 500

