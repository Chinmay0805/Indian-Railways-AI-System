import os
import sqlite3
import torch
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from langchain.agents import initialize_agent, Tool, AgentType

# Load Keys
load_dotenv()

# --- CONFIGURATION ---
DB_PATH = "railways.db"
CHROMA_PATH = "chroma_db"

# 1. Setup SQL Tool (For Train Schedules)
def query_sql_db(query):
    """Useful for finding train numbers, sources, and destinations."""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Simple Logic: Search for station names in the query
        # (In a real app, we would use an LLM to write the SQL)
        words = query.lower().split()
        search_term = next((w for w in words if len(w) > 3), "")
        
        sql = f"SELECT train_number, train_name, source_station_name, destination_station_name FROM trains WHERE source_station_name LIKE '%{search_term}%' OR destination_station_name LIKE '%{search_term}%' LIMIT 5"
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        
        if not rows:
            return "No trains found in the database for that station."
        
        return str(rows)
    except Exception as e:
        return f"Database Error: {e}"

# 2. Setup PDF Tool (For Rules)
def query_rules(query):
    """Useful for answering questions about rules, refunds, and penalties."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    embedding_function = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': device}
    )
    vector_db = Chroma(persist_directory=CHROMA_PATH, embedding_function=embedding_function)
    
    llm = ChatGoogleGenerativeAI(model="models/gemini-flash-latest", temperature=0.3)
    
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=vector_db.as_retriever(search_kwargs={"k": 3})
    )
    return qa_chain.invoke({"query": query})['result']

# 3. Initialize the Agent
# ... (imports and tool definitions remain the same) ...

# RENAME THIS FUNCTION
def initialize_agent_system():
    # Use the safe model alias
    llm = ChatGoogleGenerativeAI(model="models/gemini-flash-latest", temperature=0)

    tools = [
        Tool(
            name="Train Schedule DB",
            func=query_sql_db,
            description="Use this to find train numbers, routes, and schedules."
        ),
        Tool(
            name="Railway Rules",
            func=query_rules,
            description="Use this to look up rules about refunds, luggage, and tatkal."
        )
    ]

    # Initialize and RETURN the agent
    return initialize_agent(
        tools, 
        llm, 
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
        verbose=True
    )

# REMOVE the "while True" loop from here!
if __name__ == "__main__":
    agent = initialize_agent_system()
    print("Agent is ready for testing...")
    # You can add a temporary loop here if you want to test in terminal