from pydantic import BaseModel
from datetime import date

class InsuranceCalculation(BaseModel):
    cargo_type: str
    declared_value: float
    date: date