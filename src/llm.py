from langchain_ollama import ChatOllama

MODEL_NAME = "llama3.1:8b"

def get_llm():
    
    
    return ChatOllama(
        model=MODEL_NAME,
        temperature=0.3
    )