# -*- coding: utf-8 -*-
"""
Created on Fri Feb 13 08:18:00 2026

@author: gabri
"""

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

def build_translation(language: str, text: str) -> str:
    '''
    Translate the response into language specified
    '''
    content = f"""
    Please translate this text into {language}. 
    
    Here is the article:
    {text}
    """
    
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=content,
            )
    except Exception as e:
        return f"Error generating article: {str(e)}"
    
    for each in response.candidates[0].content.parts:
        print(each.text)
    
    # For verification, you can inspect the metadata to see which URLs the model retrieved
    print(response.candidates[0].url_context_metadata)
    return response.text
    #with open("./data/linkedin_example_post_1.txt") as f:
    #    linkedin_art = f.read()
