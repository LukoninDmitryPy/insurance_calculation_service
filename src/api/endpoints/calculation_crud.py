from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime
from typing import List

from api.schemas import rate_schema, calculation_schema
from db import models
from db.connection import get_db
from api.utils.kafka import log_action

calc_router = APIRouter()

@calc_router.post("/calculate/")
async def calculate_insurance(
    calculation: calculation_schema.InsuranceCalculation, 
    db: AsyncSession = Depends(get_db)
):
    query = select(models.Tariff).where(
        models.Tariff.cargo_type == calculation.cargo_type,
        models.Tariff.date == calculation.date
    )
    result = await db.execute(query)
    tariff = result.scalar_one_or_none()
    
    if not tariff:
        raise HTTPException(status_code=404, detail="No valid tariff found")
    
    insurance_cost = calculation.declared_value * tariff.rate
    log_action(None, f"Calculated insurance for cargo type: {calculation.cargo_type}")
    return {"insurance_cost": insurance_cost}