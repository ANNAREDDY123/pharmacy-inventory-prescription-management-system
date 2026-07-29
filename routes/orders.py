from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.medicine import Medicine
from models.order import Order
from models.prescription import Prescription
from schemas.order import OrderCreate
from services.pharmacy_service import (
    calculate_total_amount,
    medicine_not_expired,
    reduce_stock,
    stock_available,
    valid_payment_status,
    verified_prescription
)

router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_order(
    order: OrderCreate,
    db: Session = Depends(get_db)
):

    prescription = db.query(Prescription).filter(
        Prescription.id == order.prescription_id
    ).first()

    if not prescription:
        raise HTTPException(
            status_code=404,
            detail="Prescription not found."
        )

    medicine = db.query(Medicine).filter(
        Medicine.id == order.medicine_id
    ).first()

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found."
        )

    if not verified_prescription(
        prescription.status
    ):
        raise HTTPException(
            status_code=400,
            detail="Prescription must be verified."
        )

    if not medicine_not_expired(
        medicine.expiry_date
    ):
        raise HTTPException(
            status_code=400,
            detail="Expired medicine cannot be sold."
        )

    if not stock_available(
        medicine.stock_quantity,
        order.quantity
    ):
        raise HTTPException(
            status_code=400,
            detail="Insufficient stock."
        )

    total = calculate_total_amount(
        medicine.unit_price,
        order.quantity
    )

    reduce_stock(
        medicine,
        order.quantity
    )

    db_order = Order(
        prescription_id=order.prescription_id,
        medicine_id=order.medicine_id,
        quantity=order.quantity,
        total_amount=total,
        payment_status="Pending"
    )

    db.add(db_order)

    db.commit()

    db.refresh(db_order)

    return db_order


@router.get("/")
def get_orders(
    payment_status: str = None,
    customer_id: int = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Order)

    if payment_status:
        query = query.filter(
            Order.payment_status == payment_status
        )

    if customer_id:
        query = query.join(
            Prescription
        ).filter(
            Prescription.customer_id == customer_id
        )

    total = query.count()

    orders = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": orders
    }


@router.get("/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):

    order = db.query(Order).filter(
        Order.id == order_id
    ).first()

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found."
        )

    return order
