from fastapi import APIRouter
from backend.aritmetica import sumar, division

router = APIRouter()

@router.get("/suma")
def api_suma(a, b):
    return {"resultado": sumar(a, b)}

@router.get("/division")
def api_division(a, b):
    a = float(a)
    b = float(b)
    return {"resultado": division(a, b)}
