from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

# Define the base URLs for the different systems

<<<<<<< HEAD
systems = ["fire", "flooding", "earthquake", "burglary", "crime", , "safety", "health"]
=======
systems = ["fire", "burglary", "earthquake", "health"]
>>>>>>> 573254038a5e190fdc6225994dc46c9de42038eb

@app.get("/api/v1/{category}")
async def get_data(category: str):
    if category not in systems:
        raise HTTPException(status_code=404, detail="System not found")

<<<<<<< HEAD
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
=======
    if category == "fire":
        return {"data": "data from fire"}
    
    if category == "burglary":
        return {"data": "data from burglary"}
    
    if category == "earthquake":
        return {"data": "data from earthquake"}
>>>>>>> 573254038a5e190fdc6225994dc46c9de42038eb
    
    if category == "health":
        return {"data": "data from health"}
