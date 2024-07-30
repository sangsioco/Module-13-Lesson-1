from typing import List
import datetime
from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column
from models.orderProduct import order_product

class Order(Base):
    __tablename__ = 'Orders'
    id: Mapped[int] = mapped_column(primary_key=True)
    date: Mapped[datetime.date] = mapped_column(db.Date, nullable = False)
    customer_id: Mapped[int] = mapped_column(db.ForeignKey('Customers.id'))
   
    customer: Mapped["Customer"] = db.relationship(back_populates="orders")
   
    products: Mapped[List["Products"]] = db.relationship(secondary=order_product)