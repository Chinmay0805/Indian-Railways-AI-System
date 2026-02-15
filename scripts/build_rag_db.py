import os
import torch  # We import torch to check for CUDA
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv

load_dotenv()

PDF_DIR = "data/reference_docs"
DB_DIR = "chroma_db"

def build_vector_db():
    print("1. Checking for PDFs...")
    if not os.path.exists(PDF_DIR) or not os.listdir(PDF_DIR):
        print(f"❌ Error: No PDFs found in {PDF_DIR}.")
        return

    documents = []
    for file in os.listdir(PDF_DIR):
        if file.endswith(".pdf"):
            print(f"   📖 Loading: {file}")
            loader = PyPDFLoader(os.path.join(PDF_DIR, file))
            documents.extend(loader.load())

    if not documents:
        print("❌ No PDF content loaded.")
        return

    print(f"   Loaded {len(documents)} pages.")

    print("2. Splitting text...")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    texts = text_splitter.split_documents(documents)
    print(f"   Created {len(texts)} text chunks.")

    # --- GPU ACCELERATION CONFIGURATION ---
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"3. Creating Vector Database using {device.upper()} (Speed Mode)...")
    
    model_kwargs = {'device': device}
    encode_kwargs = {'normalize_embeddings': False}
    
    # We use a standard, high-performance model
    embeddings = HuggingFaceEmbeddings(
        model_name="all-MiniLM-L6-v2",
        model_kwargs=model_kwargs,
        encode_kwargs=encode_kwargs
    )
    
    vector_db = Chroma.from_documents(
        documents=texts, 
        embedding=embeddings,
        persist_directory=DB_DIR
    )
    print(f"✅ Success! Vector DB saved to: {DB_DIR}")

if __name__ == "__main__":
    build_vector_db()