from datetime import date


def duplicate_batch_exists(medicine):

    return medicine is not None


def valid_prescription_status(status):

    return status in [
        "Pending",
        "Verified",
        "Dispensed"
    ]


def valid_payment_status(status):

    return status in [
        "Pending",
        "Paid",
        "Cancelled"
    ]


def medicine_not_expired(expiry_date):

    return expiry_date >= date.today()


def stock_available(stock_quantity, quantity):

    return stock_quantity >= quantity


def valid_quantity(quantity):

    return quantity > 0


def calculate_total_amount(unit_price, quantity):

    return unit_price * quantity


def verified_prescription(status):

    return status == "Verified"


def reduce_stock(medicine, quantity):

    medicine.stock_quantity -= quantity


def low_stock(stock_quantity):

    return stock_quantity <= 10


def nearing_expiry(expiry_date):

    remaining_days = (expiry_date - date.today()).days

    return remaining_days <= 30
