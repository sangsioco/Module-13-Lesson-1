from database import db, Base
from sqlalchemy.orm import Mapped, mapped_column

class Employee(Base):
    __tablename__ = 'Employees'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(255), nullable=False)
    position: Mapped[str] = mapped_column(db.String(255))

    # adding relationship between employee and production for m13l2 assginment
    productions: Mapped[list["Production"]] = db.relationship("Production", back_populates="employee")