from fastapi import FastAPI, HTTPException, status
from .routers import databases, system, projectmanager

# App construction and routers
app = FastAPI()
app.include_router(databases.router)
app.include_router(system.router)
app.include_router(projectmanager.router)

# Online check
@app.get('/')
async def root():
    return {"message": "Hello World!!"}