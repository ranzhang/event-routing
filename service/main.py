from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI()

# Define the base URLs for the different systems

systems = []

@app.get("/api/v1/{system_name}")
async def get_data(system_name: str):
    if system_name not in systems:
        raise HTTPException(status_code=404, detail="System not found")

    system_url = systems[system_name]
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(system_url)
            response.raise_for_status()
            return {"system": system_name, "data": response.json()}
        except httpx.HTTPStatusError as e:
            raise HTTPException(status_code=response.status_code, detail=str(e))
        except Exception as e:
            raise HTTPException(status_code=500, detail="Failed to connect or retrieve data")
