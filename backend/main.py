from fastapi import FastAPI
from database import Base, engine, SessionLocal
from routers import user, leave

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
api_prefix = "/api"
# Include routers
app.include_router(user.router, prefix=api_prefix)
app.include_router(leave.router, prefix=api_prefix)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
