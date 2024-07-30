from sqlalchemy import Column, Integer, Date, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Production(Base):
    __tablename__ = 'productions'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity_produce = Column(Integer, nullable=False)
    date_produce = Column(Date, nullable=False)

    product = relationship('Product', back_populates='productions')