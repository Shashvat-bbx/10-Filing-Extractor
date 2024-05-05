import os 
from dotenv import load_dotenv
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings, StorageContext
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
import torch
from llama_index.llms.huggingface import HuggingFaceLLM
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import PromptTemplate

## Run these before running the script
# %pip install llama-index-llms-huggingface
# %pip install llama-index-embeddings-huggingface
company_ticker=input("Enter the company ticker which was provided earlier")
LLAMA2_7B_CHAT = "meta-llama/Llama-2-7b-chat-hf"
selected_model = LLAMA2_7B_CHAT
PATH_TO_DOCUMENTS=f'{company_ticker}'


SYSTEM_PROMPT = """
    - You are a Quantitative Trader. 
    - You have to analyze the provided documents and provide me just the numbers and least amount of text as response.
    - Give me insights based on the tabular data on the company's 10-K fillings.
    - Your response should  ontain the utmost important tabular data to make finance decisions on it. 
    -Some important data points are listed below.
    Revenue,   Net Income,  Earnings Per Share (EPS),Cash and Cash Equivalents,Total Assets,    Total Liabilities,  Shareholders' Equity,  Operating Income,    Gross Profit,    Net Profit Margin,   Return on Assets (ROA),,  Return on Equity (ROE),    Debt-to-Equity Ratio
    """

query_wrapper_prompt = PromptTemplate(
    "[INST]<<SYS>>\n" + SYSTEM_PROMPT + "<</SYS>>\n\n{query_str}[/INST] "
)

llm = HuggingFaceLLM(
    context_window=4096,
    max_new_tokens=1024,
    generate_kwargs={"temperature": 0.3, "do_sample": False},
    query_wrapper_prompt=query_wrapper_prompt,
    tokenizer_name=selected_model,
    model_name=selected_model,
    device_map="cpu",
    # change these settings below depending on your GPU
    model_kwargs={"torch_dtype": torch.float16, "load_in_8bit": True},
    
)


#This is the embedding model used indexing 
embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5")



## LLAMA2 7B 
Settings.llm = llm
Settings.embed_model = embed_model

documents = SimpleDirectoryReader(PATH_TO_DOCUMENTS).load_data()

# Creates embeddings of the documents.
index = VectorStoreIndex.from_documents(documents=documents)
query_engine = index.as_query_engine()
response = query_engine.query("")

print("RESPONSE : \t" , response)