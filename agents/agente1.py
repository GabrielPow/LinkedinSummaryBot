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
    '''
    Based on what it receives, will generate an summary based on what it receives, can be an article or anything it receives
    '''
    try:
        response = client.models.generate_content(
            model=model_id,
            contents=f"""
            You are an expert at analyzing articles and extracting key information.
            
            Read the following article and create a concise summary with bullet points covering:
                - The main topic or thesis
                - Key facts, statistics, or findings
                - Important arguments or perspectives presented
                - Notable quotes or expert opinions (if any)
                - Practical implications or takeaways
                
                Focus on the most important and actionable information. Each bullet point should be 1-2 sentences maximum.
                
                Format your response as clear, scannable bullet points using • or - symbols.
                
                Article:
                    {url}
                    
                    Summary:
                        """,
                        config=GenerateContentConfig(
                            tools=tools,
                            )
                        )
    except Exception as e:
        return f"Error generating summary: {str(e)}"
        
    for each in response.candidates[0].content.parts:
        print(each.text)
    
    # For verification, you can inspect the metadata to see which URLs the model retrieved
    print(response.candidates[0].url_context_metadata)
    return response.text
