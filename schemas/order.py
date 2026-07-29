from pydantic import BaseModel, Field


class OrderCreate(BaseModel):
    prescription_id: int
    medicine_id: int
    quantity: int = Field(gt=0)


class OrderResponse(BaseModel):
    id: int
    prescription_id: int
    medicine_id: int
    quantity: int
    total_amount: float
    payment_status: str

    class Config:
        from_attributes = True
