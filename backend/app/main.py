from fastapi import FastAPI
from .routers import users, leagues

app = FastAPI()

# Include routers
app.include_router(users.router)
app.include_router(leagues.router)


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI Web App"}
