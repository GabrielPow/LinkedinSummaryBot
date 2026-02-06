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

def build_context(article: str,arttype: str) -> str:
    '''
    Builds the prompt based of the article type.
    '''
    #with open("./data/linkedin_example_post_1.txt") as f:
    #    linkedin_art = f.read()
    if (arttype == "Celebration") or (arttype == "Ce"):
        prompt = f"""
            Create a LinkedIn post celebrating this achievement or completed project.
            
            Summary of what was accomplished:
            {article}
            
            Guidelines:
                - Start with an engaging hook that conveys excitement
                - Highlight the journey, challenges overcome, or impact achieved
                - Express gratitude to team members, mentors, or supporters (if applicable)
                - End with a forward-looking statement or lesson learned
                - Keep it authentic and humble while celebrating the win
                - Use 1-2 relevant emojis maximum
                - Aim for 150-250 words
            
            Post:"""
    elif (arttype == "Certificate") or (arttype == "Cer"):
        prompt = f"""
            Create a LinkedIn post about this event I participated in.
            
            Event details and key takeaways:
            {article}

            Guidelines:
                - Open with what the event was and why you attended
                - Share 2-3 key insights, learnings, or memorable moments
                - Mention interesting people you met or conversations you had (if applicable)
                - Include your main takeaway or how it impacted your thinking
                - Make it valuable for readers who didn't attend
                - End with a reflection or call-to-action
                - Use 1-2 relevant emojis maximum
                - Aim for 200-300 words
            Post:"""
    elif (arttype == "Event") or (arttype == "Ev"):
        prompt = f"""
            Create a LinkedIn post announcing this certification I've completed.
            
            Certification details:
            {article}
            
            Guidelines:
                - Announce the certification clearly and proudly
                - Briefly explain what the certification covers and why it matters
                - Share what motivated you to pursue it
                - Highlight 1-2 key skills or knowledge areas you gained
                - Connect it to your professional goals or how you'll apply it
                - Thank instructors, organization, or supporters (if applicable)
                - Keep it professional but personable
                - Use 1 relevant emoji maximum
                - Aim for 150-200 words
            Post:"""
    elif (arttype == "Article") or (arttype == "Ar"):
        prompt = f"""
            Create an engaging LinkedIn post that summarizes this article and shares your perspective.
            
            Article summary:
                {article}
                
            Guidelines:
                - Open with a hook that explains why this article matters
                - Present the main points in a clear, digestible way (2-4 key points)
                - Add your own insight, reaction, or professional perspective
                - Make it valuable - what should your network take away from this?
                - End with a thought-provoking question or call-to-action to encourage engagement
                - Use 1-2 relevant emojis maximum
                - Aim for 200-300 words
                - Write in a conversational but professional tone
            Post:"""
    else:
        return "None"
    return prompt

def build_summary(article: str, arttype: str) -> str:
    '''
    Builds an article based of the article type, with different specifications.
    
    Types of article are: Article, Certification, Celebration, Event
    
    Article: Ar or Article
    Certification: Cer or Certificate
    Celebration: Ce or Celebration
    Event: Ev or Event
    '''
    content = build_context(article, arttype)
    if content == "None":
        print("No type specified or wrongly written, try again.")
        return
    
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