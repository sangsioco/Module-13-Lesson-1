from sqlalchemy.orm import Session
from database import db
from models.production import Production
from sqlalchemy import select, func
from models.product import Product


def save(production_data):
    with Session(db.engine) as session:
            new_production = Production(
                product_id=production_data['product_id'],
                quantity_produced=production_data['quantity_produced'],
                date_produced=production_data['date_produced']
            )
            session.add(new_production)
            session.commit()
            session.refresh(new_production)
            return new_production

def find_all():
    query = db.select(Production)
    production = db.session.execute(query).scalars().all()
    return production

def total_quantity_per_product_on_date(date: str):
    with Session(db.engine) as session:
        # Subquery to filter productions for the specified date
        subquery = (
            select(Production.product_id, func.sum(Production.quantity_produced).label('total_quantity'))
            .where(Production.date_produced == date)
            .group_by(Production.product_id)
            .subquery()
        )
        
        # Main query to join Product with the subquery and calculate total quantity
        query = (
            select(
                Product.name,
                func.coalesce(subquery.c.total_quantity, 0).label('total_quantity')
            )
            .join(subquery, Product.id == subquery.c.product_id)
            .order_by(Product.name)  # Optional: order by product name
        )
        
        results = session.execute(query).all()
        return results