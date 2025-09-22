from service import chat_service
from dto import ChatRequest 
from fastapi import FastAPI
import uvicorn
from service import chat_service_streaming
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def read_root():
    return FileResponse("static/index.html")

@app.post("/chat")
def chat_endpoint(request: ChatRequest):
    return chat_service(request)
    
@app.post("/chat/stream")
def chat_stream_endpoint(request: ChatRequest):
    return chat_service_streaming(request)    

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)