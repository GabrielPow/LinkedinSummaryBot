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

articles = pd.read_excel("./data/articles.xlsx",header=0,usecols="B:E", dtype="object")

index_val = articles.index[-1]

#%%

articles.loc[index_val,"Agent_1"] = "Test"

#%%

with open("./data/linkedin_example_post_1.txt") as f:
    linkedin_ex1 = f.read()

del f    

#%%
url = articles.iloc[index_val,0]
#%%
agent1_response = build_search(url)
print(agent1_response)

articles.loc[index_val,"Agent_1"] = agent1_response
#%%

agent2_response = build_summary(agent1_response)
print(agent2_response)

articles.loc[index_val,"Agent_2"] = agent2_response
#%%
articles.loc[index_val,"Processed"] = "Yes"
#%%
with pd.ExcelWriter("./data/articles.xlsx", mode = 'a', engine = 'openpyxl', if_sheet_exists="replace") as writer:
    articles.to_excel(writer)
#%%
document = Document()

document.add_paragraph(agent2_response)

document.save('./output/response.docx')