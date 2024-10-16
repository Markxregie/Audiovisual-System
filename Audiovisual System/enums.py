from enum import Enum

class RentalStatus(Enum):
    ACTIVE = "Active"
    RETURNED = "Returned"
    DELETED = "Deleted"

class PaymentStatus(Enum):
    PENDING = "Pending"
    PAID = "Paid"

