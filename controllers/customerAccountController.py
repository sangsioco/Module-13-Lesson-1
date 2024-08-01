from models.schemas.customerAccountSchema import customer_accounts_schema
from services import customerAccountService

def find_all():
    customer_accounts = customerAccountService.find_all()
    return customer_accounts_schema.jsonify(customer_accounts), 200