import os
import torch
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import RetrievalQA
from dotenv import load_dotenv

# Load API Keys
load_dotenv()

# Configuration
DB_DIR = "chroma_db"

def chat_bot():
    print("1. Loading Vector Database...")
    if not os.path.exists(DB_DIR):
        print("❌ Error: DB not found. Run build_rag_db.py first.")
        return

    # 1. Load the "Brain" (Embeddings) - MUST match the build script!
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"   Using Device: {device.upper()}")
    
    embedding_function = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs={'device': device}
    )

    # 2. Connect to the Database
    vector_db = Chroma(persist_directory=DB_DIR, embedding_function=embedding_function)
    print("   Database Loaded.")

    # 3. Setup the LLM (Google Gemini)
    # We use Gemini Pro for the actual "Thinking"
    if not os.getenv("GOOGLE_API_KEY"):
        print("❌ Error: GOOGLE_API_KEY not found in .env")
        return
        
    llm = ChatGoogleGenerativeAI(
        model="models/gemini-flash-latest",
        temperature=0.3, # Low temp = more factual, less creative
        convert_system_message_to_human=True
    )

    # 4. Create the Chain (The "Manager")
    # This chain does the following:
    #   a. User asks question -> b. Search DB for 3 relevant chunks -> c. Send chunks + question to Gemini -> d. Gemini answers
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff", # "Stuff" means "stuff all found documents into the prompt"
        retriever=vector_db.as_retriever(search_kwargs={"k": 3}), # Get top 3 relevant facts
        return_source_documents=True # Show us WHERE the answer came from
    )

    print("\n🚆 Railway AI Assistant is Ready! (Type 'exit' to stop)")
    print("-" * 50)

    while True:
        query = input("\nYou: ")
        if query.lower() in ["exit", "quit", "bye"]:
            print("Chatbot: Safe travels! 🚆")
            break
            
        if not query.strip():
            continue

        print("   🔍 Searching rules...")
        try:
            # Run the chain
            response = qa_chain.invoke({"query": query})
            
            # Print the Answer
            print(f"AI: {response['result']}")
            
            # (Optional) Print Sources for debugging
            # print("\n   (Source: " + response['source_documents'][0].metadata['source'] + ")")
            
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    chat_bot()