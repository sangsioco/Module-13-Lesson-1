from models.customer import Customer
from models.order import Order
from models.product import Product
from database import db
from sqlalchemy import select
from sqlalchemy.orm import Session

def save(order_data):
    with Session(db.engine) as session:
        with session.begin():
            
            product_ids = [product['id'] for product in order_data['products']]
            products = session.execute(select(Product).where(Product.id.in_(product_ids))).scalars().all()

            customer_id = order_data['customer_id']
            customer = session.execute(select(Customer).where(Customer.id == customer_id)).scalars().first()

            if len(products) != len(product_ids):
                raise ValueError("One or more products do not exist")
            
            if not customer:
                raise ValueError(f"Customer with ID {customer_id} does not exist")
            
            print("Products:", products[0].name)
            new_order = Order(date=order_data['date'], customer_id=order_data['customer_id'], products=products)
            session.add(new_order)
            print("New Order ID (before commit):", new_order.id)
            session.flush()
            print("New Order ID (after commit):", new_order.id)
            session.commit()

        session.refresh(new_order)

        for product in new_order.products:
            session.refresh(product)
        
        return new_order
    
# GET display all order
def find_all():
    query = select(Order)
    orders = db.session.execute(query).scalars().all()
    return orders

# Adding pagination for orders
def find_all_pagination(page=1, per_page=10):
    orders = db.paginate(select(Order), page=page, per_page=per_page)
    return orders