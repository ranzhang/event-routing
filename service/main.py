from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

# Define the base URLs for the different systems

systems = ["fire", "burglary", "earthquake", "health"]

@app.get("/api/v1/{category}")
async def get_data(category: str):
    if category not in systems:
        raise HTTPException(status_code=404, detail="System not found")

    if category == "fire":
        return {"data": "data from fire"}
    
    if category == "burglary":
        return {"data": "data from burglary"}
    
    if category == "earthquake":
        return {"data": "data from earthquake"}
    
    if category == "health":
        return {"data": "data from health"}
