from models.product import Product
from database import db
from sqlalchemy.orm import Session
from sqlalchemy import select, func
from models.production import Production

def save(product_data):
    with Session(db.engine) as session:
        with session.begin():
            new_product = Product(name=product_data['name'], price=product_data['price'])
            session.add(new_product)
            session.commit()
        session.refresh(new_product)
        return new_product
    
def find_all():
    query = select(Product)
    products = db.session.execute(query).scalars().all()
    return products

# Adding pagination for orders
def find_all_pagination(page=1, per_page=10):
    products = db.paginate(select(Product), page=page, per_page=per_page)
    return products

def find_top_selling_products():
    with Session(db.engine) as session:
        # Query to find top-selling products based on total quantity ordered
        top_selling_query = (
            session.query(
                Product.name,
                func.sum(Production.quantity_produced).label('total_quantity_ordered')
            )
            .join(Production, Product.id == Production.product_id)
            .group_by(Product.name)
            .order_by(func.sum(Production.quantity_produced).desc())
        )

        results = top_selling_query.all()
        return results