from sqlalchemy import Column, Date, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from database import Base


class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    customer_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False
    )

    doctor_name = Column(
        String,
        nullable=False
    )

    prescription_date = Column(
        Date,
        nullable=False
    )

    status = Column(
        String,
        nullable=False
    )

    customer = relationship("User")
