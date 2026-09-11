from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Smart Fridge & Nutrition Coach"}