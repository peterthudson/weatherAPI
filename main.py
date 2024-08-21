from fastapi import FastAPI

app = FastAPI()

# Routes
@app.get("/")
def root():
    return {"message": "Weather API"}