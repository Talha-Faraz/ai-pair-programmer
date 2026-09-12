import os
from PIL import Image
from google import genai
from google.genai import types

class AIPairProgrammer:
    def __init__(self, api_key=None):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("API Key missing. Set GEMINI_API_KEY in your environment.")
        
        self.client = genai.Client(api_key=self.api_key)
        
        self.system_instruction = (
            "You are an expert AI Pair Programmer. Look at the provided screenshot of the user's screen/IDE. "
            "1. If they are writing code, point out any syntax errors, logical bugs, or missing imports. "
            "2. Keep your answers concise, direct, and helpful. "
            "3. If there are no errors, simply say 'Code looks good!' or answer the user's specific question."
        )

    def analyze_code_screenshot(self, image_path, user_query="Check this screen for any errors or issues."):
        try:
            img = Image.open(image_path)
            
            # Model updated to the latest available version according to the API error
            response = self.client.models.generate_content(
                model='gemini-3.6-flash',
                contents=[user_query, img],
                config=types.GenerateContentConfig(
                    system_instruction=self.system_instruction
                )
            )
            return response.text
            
        except Exception as e:
            return f"AI Processing Error: {str(e)}"
