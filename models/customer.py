from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column

class Customer(Base):
    __tablename__ = 'Customers'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    email: Mapped[str] = mapped_column(db.String(320))
    phone: Mapped[str] = mapped_column(db.String(12))
    
    customer_account: Mapped["CustomerAccount"] = db.relationship("CustomerAccount", back_populates="customer")

