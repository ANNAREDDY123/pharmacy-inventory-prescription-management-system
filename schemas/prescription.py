from datetime import date

from pydantic import BaseModel


class PrescriptionCreate(BaseModel):
    customer_id: int
    doctor_name: str
    prescription_date: date
    status: str


class PrescriptionUpdate(BaseModel):
    customer_id: int
    doctor_name: str
    prescription_date: date
    status: str


class PrescriptionResponse(BaseModel):
    id: int
    customer_id: int
    doctor_name: str
    prescription_date: date
    status: str

    class Config:
        from_attributes = True
