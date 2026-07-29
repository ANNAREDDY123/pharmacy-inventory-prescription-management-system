from datetime import date

from pydantic import BaseModel, Field


class MedicineCreate(BaseModel):
    medicine_name: str
    batch_number: str
    manufacturer: str
    expiry_date: date
    unit_price: float = Field(gt=0)
    stock_quantity: int = Field(gt=0)


class MedicineUpdate(BaseModel):
    medicine_name: str
    batch_number: str
    manufacturer: str
    expiry_date: date
    unit_price: float = Field(gt=0)
    stock_quantity: int = Field(gt=0)


class MedicineResponse(BaseModel):
    id: int
    medicine_name: str
    batch_number: str
    manufacturer: str
    expiry_date: date
    unit_price: float
    stock_quantity: int

    class Config:
        from_attributes = True
