from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Manim server running"}
