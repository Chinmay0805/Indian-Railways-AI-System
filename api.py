from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
# 👇 THIS is the correct import now
from scripts.final_agent import initialize_agent_system

# Define the request format
class ChatRequest(BaseModel):
    message: str

app = FastAPI()

# Allow the frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the agent once when the server starts
print("🤖 Initializing Railway AI Agent...")
agent = initialize_agent_system()

@app.post("/chat")
async def chat(request: ChatRequest):
    try:
        # Ask the agent
        response = agent.invoke(request.message)
        # Handle different response types from LangChain
        output_text = response.get("output") if isinstance(response, dict) else str(response)
        return {"response": output_text}
    except Exception as e:
        print(f"❌ Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
def home():
    return {"message": "Railway AI API is running!"}