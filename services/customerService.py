from sqlalchemy.orm import Session
from database import db
from models.customer import Customer
from circuitbreaker import circuit
from sqlalchemy import select, func
from models.order import Order

def fallback_function(customer):
    return None

@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(customer_data):
    try:
        if customer_data['name'] == "Failure":
            raise Exception("Failure condition triggered")
        
        with Session(db.engine) as session:
            with session.begin():
                new_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
                session.add(new_customer)


                savepoint = session.begin_nested()
                new_nested_customer = Customer(name=customer_data['name'], email=customer_data['email'], phone=customer_data['phone'])
                session.add(new_nested_customer)

                savepoint.rollbacl()

            session.refresh(new_customer)
            return new_customer
    
    except Exception as e:
        raise e
    
def find_all():
    query = select(Customer)
    customers = db.session.execute(query).scalars().all()
    return customers

def find_total_order_value(threshold: float):
    with Session(db.engine) as session:
        # Query to calculate the total value of orders placed by each customer
        total_order_value_query = (
            session.query(
                Customer.name,
                func.sum(Order.total_value).label('total_order_value')
            )
            .join(Order, Customer.id == Order.customer_id)
            .group_by(Customer.name)
            .having(func.sum(Order.total_value) >= threshold)
            .order_by(func.sum(Order.total_value).desc())  # Optional: order by total value
        )

        results = total_order_value_query.all()
        return results
