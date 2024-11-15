from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

# Define the base URLs for the different systems

systems = ["fire", "flooding", "earthquake", "burglary", "crime",  "safety", "health"]

@app.get("/api/v1/{category}")
async def get_data(category: str):
    if category not in systems:
        raise HTTPException(status_code=404, detail="System not found")

    if category == "fire":
        return {"data": "data from fire"}
    
    if category == "flooding":
        return {"data": "data from flooding"}
    
    if category == "earthquake":
        return {"data": "data from earthquake"}
    
    if category == "burglary":
        return {"data": "data from burglary"}
    
    if category == "crime":
        return {"data": "data from crime"}
    
    if category == "safety":
        return {"data": "data from safety"}
    
    if category == "health":
        return {"data": "data from health"}
