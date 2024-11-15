from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

# Define the base URLs for the different systems

systems = []

@app.get("/api/v1/{system_name}")
async def get_data(system_name: str):
    if system_name not in systems:
        raise HTTPException(status_code=404, detail="System not found")

    if system_name == "system1":
        return {"data": "data from system1"}
    
    if system_name == "system2":
        return {"data": "data from system2"}
    
    if system_name == "system3":
        return {"data": "data from system3"}
    
    