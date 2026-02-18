from fastapi import FastAPI
import os
from dotenv import load_dotenv
from chainlit.utils import mount_chainlit

load_dotenv()
app = FastAPI()

@app.get("/info")
def read_main():
    return {"message": "Hello, It's Thomas!! I am here to help you!"}

mount_chainlit(app=app, target="app_c.py", path="/chat")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("api:app", host="0.0.0.0", port=int(os.getenv("PORT", 8000)), reload=True)