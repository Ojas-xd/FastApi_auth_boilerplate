from fastapi import FastAPI
from app.api.routes.auth import router
from app.database import Base,engine
Base.metadata.create_all(bind=engine)
app=FastAPI()
app.include_router(router)
@app.get("/")
def root():
    return {"message":"server is running"}