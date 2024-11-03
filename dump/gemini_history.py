import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(
    "gemini-1.5-flash-latest",
    system_instruction=[
        {"text": "You respond for every answer asked as 2 bullet points."}
    ],
)

conversation_history = []


def start_chat_with_history(history):
    chat = model.start_chat(history=history)
    return chat


def send_message(chat_session, user_input):
    response = chat_session.send_message(user_input)
    print(response.text)
    return response.text


chat_session = start_chat_with_history(conversation_history)

user_input = "Why to build muscles?"
response_text = send_message(chat_session, user_input)

user_input = "Can I do it if I have kidney issues?"
response_text = send_message(chat_session, user_input)

user_input = "How many days in a week is recommended to do it?"
response_text = send_message(chat_session, user_input)
