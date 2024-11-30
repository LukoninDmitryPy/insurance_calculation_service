from fastapi import FastAPI

from api.endpoints.rates_crud import rates_router
from api.endpoints.calculation_crud import calc_router

app = FastAPI(
    title="Task Management API",
    description="An API for managing tasks and communicating with a scheduler",
    version="1.0.0",
)

# Подключение маршрутов
app.include_router(rates_router, prefix="/tariffs", tags=["Tariff"])
app.include_router(calc_router, prefix="/calculate", tags=["Calculation"])
