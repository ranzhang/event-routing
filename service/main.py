from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

# Define the base URLs for the different systems

systems = ["fire", "flooding", "earthquake", "burglary", "crime", , "safety", "health"]

@app.get("/api/v1/{system_name}")
async def get_data(system_name: str):
    if system_name not in systems:
        raise HTTPException(status_code=404, detail="System not found")

    if system_name == "fire":
        return {"data": "data from fire"}
    
    if system_name == "flooding":
        return {"data": "data from flooding"}
    
    if system_name == "earthquake":
        return {"data": "data from earthquake"}
    
    if system_name == "burglary":
        return {"data": "data from burglary"}
    
    if system_name == "crime":
        return {"data": "data from crime"}
    
    if system_name == "safety":
        return {"data": "data from safety"}
    
    if system_name == "health":
        return {"data": "data from health"}
    
