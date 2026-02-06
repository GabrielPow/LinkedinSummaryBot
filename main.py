import pandas as pd
import os
from dotenv import load_dotenv
from google import genai
#%%
from agents.agente1 import build_search
from agents.agente2 import build_summary
#%%
from docx import Document  
#%%
from agents.agente2 import build_context
#%%
tester = build_context("Ce")
#%%
def article_building(arttype: str) -> str:
    articles = pd.read_excel("./data/articles.xlsx",header=0,usecols="B:E", dtype="object")
    index_val = articles.index[-1]
    url = articles.iloc[index_val,0]
    
    agent1_response = build_search(url)
    print(agent1_response)
    articles.loc[index_val,"Agent_1"] = agent1_response
    
    agent2_response = build_summary(agent1_response, arttype)
    print(agent2_response)
    articles.loc[index_val,"Agent_2"] = agent2_response
    
    articles.loc[index_val,"Processed"] = "Yes"
    
    with pd.ExcelWriter("./data/articles.xlsx", mode = 'a', engine = 'openpyxl', if_sheet_exists="replace") as writer:
        articles.to_excel(writer)
    
    return agent2_response
#%%
response = article_building()
#%%
document = Document()

document.add_paragraph(response)

document.save('./output/response.docx')

#%%
url = "https://www.geekwire.com/2026/amazon-confirms-16000-more-job-cuts-bringing-total-layoffs-to-30000-since-october/"
agent1_response = build_search(url)
print(agent1_response)
#%%
agent2_response = build_summary(agent1_response,"Ar")
print(agent2_response)

