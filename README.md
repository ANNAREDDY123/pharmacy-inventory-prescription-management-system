# pharmacy-inventory-prescription-management-system
A FastAPI-based Pharmacy Inventory &amp; Prescription Management System with JWT Authentication, Role-Based Authorization, Medicine Management, Prescription Management, Order Processing, Reports, Search, Pagination, SQLAlchemy ORM, Swagger Documentation, and Docker support.
# Pharmacy Inventory & Prescription Management System

## Features

- JWT Authentication
- Role-Based Authorization
- Medicine Management
- Prescription Management
- Order Processing
- Automatic Stock Reduction
- Automatic Total Calculation
- Search APIs
- Reports
- Pagination
- SQLAlchemy ORM
- SQLite Database
- Docker Support

## Tech Stack

- Python
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- JWT
- Uvicorn

## Installation


pip install -r requirements.txt


Run:


uvicorn main:app --reload


Swagger:


http://127.0.0.1:8000/docs


## Roles

- Admin
- Pharmacist
- Customer

## Business Rules

- Batch Number Unique
- Expired Medicines Cannot Be Sold
- Verified Prescription Required
- Automatic Stock Reduction
- Automatic Total Calculation
- Quantity > 0

## Modules

- Authentication
- Medicines
- Prescriptions
- Orders
- Reports
