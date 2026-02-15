import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("❌ Error: API Key not found in .env")
else:
    print(f"🔑 Using Key: ...{api_key[-4:]}")
    try:
        genai.configure(api_key=api_key)
        
        print("\n--- AVAILABLE MODELS FOR YOU ---")
        found_any = False
        for m in genai.list_models():
            # We only care about models that can generate text
            if 'generateContent' in m.supported_generation_methods:
                print(f"✅ {m.name}")
                found_any = True
        
        if not found_any:
            print("❌ No text generation models found. Check if API is enabled in Google Console.")
            
    except Exception as e:
        print(f"❌ Connection Error: {e}")