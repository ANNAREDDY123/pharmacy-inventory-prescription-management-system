from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database import SessionLocal
from models.medicine import Medicine
from schemas.medicine import MedicineCreate, MedicineUpdate
from services.pharmacy_service import (
    duplicate_batch_exists,
    nearing_expiry
)

router = APIRouter(
    prefix="/medicines",
    tags=["Medicines"]
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
def create_medicine(
    medicine: MedicineCreate,
    db: Session = Depends(get_db)
):

    existing = db.query(Medicine).filter(
        Medicine.batch_number == medicine.batch_number
    ).first()

    if duplicate_batch_exists(existing):
        raise HTTPException(
            status_code=400,
            detail="Batch number already exists."
        )

    db_medicine = Medicine(
        **medicine.model_dump()
    )

    db.add(db_medicine)
    db.commit()
    db.refresh(db_medicine)

    return db_medicine


@router.get("/")
def get_medicines(
    medicine_name: str = None,
    batch_number: str = None,
    near_expiry: bool = False,
    page: int = 1,
    limit: int = 10,
    db: Session = Depends(get_db)
):

    medicines = db.query(Medicine).all()

    if medicine_name:
        medicines = [
            m for m in medicines
            if medicine_name.lower()
            in m.medicine_name.lower()
        ]

    if batch_number:
        medicines = [
            m for m in medicines
            if batch_number.lower()
            in m.batch_number.lower()
        ]

    if near_expiry:
        medicines = [
            m for m in medicines
            if nearing_expiry(m.expiry_date)
        ]

    total = len(medicines)

    start = (page - 1) * limit
    end = start + limit

    return {
        "total_records": total,
        "current_page": page,
        "limit": limit,
        "data": medicines[start:end]
    }


@router.get("/{medicine_id}")
def get_medicine(
    medicine_id: int,
    db: Session = Depends(get_db)
):

    medicine = db.query(Medicine).filter(
        Medicine.id == medicine_id
    ).first()

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found."
        )

    return medicine


@router.put("/{medicine_id}")
def update_medicine(
    medicine_id: int,
    medicine: MedicineUpdate,
    db: Session = Depends(get_db)
):

    db_medicine = db.query(Medicine).filter(
        Medicine.id == medicine_id
    ).first()

    if not db_medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found."
        )

    duplicate = db.query(Medicine).filter(
        Medicine.batch_number == medicine.batch_number,
        Medicine.id != medicine_id
    ).first()

    if duplicate:
        raise HTTPException(
            status_code=400,
            detail="Batch number already exists."
        )

    for key, value in medicine.model_dump().items():
        setattr(db_medicine, key, value)

    db.commit()
    db.refresh(db_medicine)

    return db_medicine


@router.delete("/{medicine_id}")
def delete_medicine(
    medicine_id: int,
    db: Session = Depends(get_db)
):

    medicine = db.query(Medicine).filter(
        Medicine.id == medicine_id
    ).first()

    if not medicine:
        raise HTTPException(
            status_code=404,
            detail="Medicine not found."
        )

    db.delete(medicine)
    db.commit()

    return {
        "message": "Medicine deleted successfully."
    }


@router.get("/reports/low-stock")
def low_stock_report(
    db: Session = Depends(get_db)
):

    medicines = db.query(Medicine).filter(
        Medicine.stock_quantity <= 10
    ).all()

    return medicines
