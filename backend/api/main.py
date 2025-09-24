from fastapi import FastAPI
from backend.api.aritmetica import router as aritmetica_router

app = FastAPI()

app.include_router(aritmetica_router, prefix="/aritmetica")
