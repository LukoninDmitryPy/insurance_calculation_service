from pydantic import BaseModel, RootModel, Field
from datetime import date as dt
from typing import Dict, List
from typing import Optional

class TariffBase(BaseModel):
    cargo_type: str
    rate: float
    date: dt


class TariffUpdate(BaseModel):
    cargo_type: Optional[str] = None
    rate: Optional[float] = None
    date: Optional[dt] = None

class Tariff(TariffBase):
    id: int

    class Config:
        orm_mode = True

class TariffItem(BaseModel):
    cargo_type: str
    rate: float

class TariffDate(BaseModel):
    date: dt

class TariffCreate(RootModel):
    root: Dict[str, List[TariffItem]]
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "2024-06-01": [
                        {"cargo_type": "Glass", "rate": "0.01"},
                        {"cargo_type": "Other", "rate": "0.5"}
                    ]
                }
            ]
        }
    }

class TariffResponse(BaseModel):
    id: int
    cargo_type: str
    rate: float
    date: dt

    class Config:
        from_attributes = True