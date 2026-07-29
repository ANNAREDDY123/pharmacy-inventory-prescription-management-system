from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.prescription import Prescription
from models.user import User
from schemas.prescription import (
    PrescriptionCreate,
    PrescriptionUpdate
)
from services.pharmacy_service import (
    valid_prescription_status
)

router = APIRouter(
    prefix="/prescriptions",
    tags=["Prescriptions"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_prescription(
    prescription: PrescriptionCreate,
    db: Session = Depends(get_db)
):

    customer = db.query(User).filter(
        User.id == prescription.customer_id
    ).first()

    if not customer:
        raise HTTPException(
            status_code=404,
            detail="Customer not found."
        )

    if customer.role != "Customer":
        raise HTTPException(
            status_code=400,
            detail="Invalid customer."
        )

    if not valid_prescription_status(
        prescription.status
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid prescription status."
        )

    db_prescription = Prescription(
        **prescription.model_dump()
    )

    db.add(db_prescription)
    db.commit()
    db.refresh(db_prescription)

    return db_prescription


@router.get("/")
def get_prescriptions(
    customer_id: int = None,
    status: str = None,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    query = db.query(Prescription)

    if customer_id:
        query = query.filter(
            Prescription.customer_id == customer_id
        )

    if status:
        query = query.filter(
            Prescription.status == status
        )

    total = query.count()

    prescriptions = query.offset(
        (page - 1) * limit
    ).limit(limit).all()

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": prescriptions
    }


@router.get("/{prescription_id}")
def get_prescription(
    prescription_id: int,
    db: Session = Depends(get_db)
):

    prescription = db.query(Prescription).filter(
        Prescription.id == prescription_id
    ).first()

    if not prescription:
        raise HTTPException(
            status_code=404,
            detail="Prescription not found."
        )

    return prescription


@router.put("/{prescription_id}")
def update_prescription(
    prescription_id: int,
    prescription: PrescriptionUpdate,
    db: Session = Depends(get_db)
):

    db_prescription = db.query(Prescription).filter(
        Prescription.id == prescription_id
    ).first()

    if not db_prescription:
        raise HTTPException(
            status_code=404,
            detail="Prescription not found."
        )

    if not valid_prescription_status(
        prescription.status
    ):
        raise HTTPException(
            status_code=400,
            detail="Invalid prescription status."
        )

    for key, value in prescription.model_dump().items():
        setattr(db_prescription, key, value)

    db.commit()
    db.refresh(db_prescription)

    return db_prescription
