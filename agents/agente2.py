import os
from dotenv import load_dotenv
from google import genai

# Load API key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("Missing GEMINI_API_KEY in .env file")

# Configure Gemini
model_id = "gemini-2.5-flash-preview-09-2025"
client = genai.Client(api_key = api_key)


def build_summary(article: str) -> str:
    response = client.models.generate_content(
        model=model_id,
        contents=f"Write a linkedin style post given the provided article, creating a digestible and factual analysis of the article {article}",
    )
    
    for each in response.candidates[0].content.parts:
        print(each.text)
    
    # For verification, you can inspect the metadata to see which URLs the model retrieved
    print(response.candidates[0].url_context_metadata)
    return response.text