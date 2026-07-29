from sqlalchemy import Column, Date, Float, Integer, String

from database import Base


class Medicine(Base):
    __tablename__ = "medicines"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    medicine_name = Column(
        String,
        nullable=False
    )

    batch_number = Column(
        String,
        unique=True,
        nullable=False
    )

    manufacturer = Column(
        String,
        nullable=False
    )

    expiry_date = Column(
        Date,
        nullable=False
    )

    unit_price = Column(
        Float,
        nullable=False
    )

    stock_quantity = Column(
        Integer,
        nullable=False
    )
