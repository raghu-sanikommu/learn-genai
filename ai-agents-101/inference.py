import os

import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()


class LLM:
    def __init__(self, system_instruction):
        genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
        self.model = genai.GenerativeModel(
            "gemini-1.5-flash-latest",
            system_instruction=[{"text": system_instruction}],
        )

    def completion(self, user_input):
        try:
            print("Initiating talk with LLM ...")
            print(".")
            print(".")
            print("Talking to LLM ...")
            print(".")
            print(".")
            response = self.model.generate_content(user_input)
            print("Response from LLM: ")
            print(response.text)
            print("-------------")
            return response.text
        except Exception as e:
            print("ERR at Gemini Completion :: ", e)
            raise RuntimeError("ERR at Gemini Completion")
