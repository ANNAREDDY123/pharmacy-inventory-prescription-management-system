from fastapi import FastAPI

from database import Base, engine

from models.user import User
from models.medicine import Medicine
from models.prescription import Prescription
from models.order import Order

from routes.auth import router as auth_router
from routes.medicines import router as medicines_router
from routes.prescriptions import router as prescriptions_router
from routes.orders import router as orders_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Pharmacy Inventory & Prescription Management System"
)

app.include_router(auth_router)
app.include_router(medicines_router)
app.include_router(prescriptions_router)
app.include_router(orders_router)


@app.get("/")
def home():
    return {
        "message": "Pharmacy Inventory & Prescription Management System API"
    }
