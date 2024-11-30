from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from datetime import datetime as dt

from api.schemas import rate_schema
from db import models
from db.connection import get_db
from api.utils.kafka import log_action

rates_router = APIRouter()


@rates_router.post("/tariffs/", response_model=rate_schema.TariffCreate)
async def create_tariff(tariff_data: rate_schema.TariffCreate, db: AsyncSession = Depends(get_db)):
    for date_str, tariffs in tariff_data.model_dump().items():
        tariff_date = dt.strptime(date_str, '%Y-%m-%d').date()
        print(f"Processing date: {tariffs}")
        for tariff_item in tariffs:
            print(f"Processing tariff: {tariff_item['cargo_type']} - {tariff_item['rate']}")
            db_tariff = models.Tariff(
                date=tariff_date,
                cargo_type=tariff_item['cargo_type'],
                rate=float(tariff_item['rate'])
            )
            db.add(db_tariff)
    await db.commit()
    return tariff_data

@rates_router.get("/tariffs/", response_model=List[rate_schema.Tariff])
async def get_tariffs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(models.Tariff))
    log_action(None, "Retrieved all tariffs")
    return result.scalars().all()

@rates_router.put("/tariffs/{tariff_id}", response_model=rate_schema.Tariff)
async def update_tariff(tariff_id: int, tariff: rate_schema.TariffUpdate, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(models.Tariff).filter(models.Tariff.id == tariff_id))
    db_tariff = query.scalar_one_or_none()
    if not db_tariff:
        raise HTTPException(status_code=404, detail="Tariff not found")
    
    for key, value in tariff.dict(exclude_unset=True).items():
        setattr(db_tariff, key, value)
    
    await db.commit()
    log_action(None, f"Updated tariff ID: {tariff_id}")
    return db_tariff

@rates_router.delete("/tariffs/{tariff_id}")
async def delete_tariff(tariff_id: int, db: AsyncSession = Depends(get_db)):
    query = await db.execute(select(models.Tariff).where(models.Tariff.id == tariff_id))
    db_tariff = query.scalar_one_or_none()
    if not db_tariff:
        raise HTTPException(status_code=404, detail="Tariff not found")
    
    db.delete(db_tariff)
    db.commit()
    log_action(None, f"Deleted tariff ID: {tariff_id}")
    return {"message": "Tariff deleted"}