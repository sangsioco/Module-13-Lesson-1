from database import db
from models.customer import Customer
from models.customerAccount import CustomerAccount
from sqlalchemy import select
    
def find_all():
    query = select(CustomerAccount).join(Customer).where(Customer.id == CustomerAccount.customer_id)
    customer_accounts = db.session.execute(query).scalars().all()
    return customer_accounts