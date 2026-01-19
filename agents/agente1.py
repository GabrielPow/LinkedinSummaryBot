import os
from dotenv import load_dotenv
from google import genai
from google.genai.types import Tool, GenerateContentConfig

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Missing GEMINI_API_KEY in .env file")

# Configure Gemini
model_id = "gemini-2.5-flash"
client = genai.Client(api_key=api_key)

tools = [
  {"url_context": {}},
]

def build_search(url: str) -> str:
    response = client.models.generate_content(
        model=model_id,
        contents=f"Summarize the most important facts and developments within the article given below {url}",
        config=GenerateContentConfig(
            tools=tools,
            )
    )
    for each in response.candidates[0].content.parts:
        print(each.text)
    
    # For verification, you can inspect the metadata to see which URLs the model retrieved
    print(response.candidates[0].url_context_metadata)
    return response.text