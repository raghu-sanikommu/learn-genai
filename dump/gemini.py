import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
model = genai.GenerativeModel(
    "gemini-1.5-flash-latest",
)


def completion(user_input):
    try:
        response = model.generate_content(user_input)
        print(response.text)
        return response.text
    except Exception as e:
        print("ERR at Gemini Completion :: ", e)
        raise RuntimeError("ERR at Gemini Completion")


completion("Hi")
