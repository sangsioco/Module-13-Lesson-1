from sqlalchemy.orm import Session
from database import db
from models.employee import Employee
from circuitbreaker import circuit
from sqlalchemy import select, func
from models.production import Production  
from circuitbreaker import circuit

def fallback_function(employee):
    return None

@circuit(failure_threshold=1, recovery_timeout=10, fallback_function=fallback_function)
def save(employee_data):
    try:
        if employee_data['name'] == "Failure":
            raise Exception("Failure condition triggered")

        with Session(db.engine) as session:
            with session.begin():
                new_employee = Employee(name=employee_data['name'], position=employee_data['position'])
                session.add(new_employee)
                session.commit()
            session.refresh(new_employee)
            return new_employee

    except Exception as e:
        raise e

def find_all():
    query = select(Employee)
    employees = db.session.execute(query).scalars().all()
    return employees

# added for for employee performance group by name m13l2 objective 2
def find_by_name(name: str):
    with Session(db.engine) as session:
        employee_production_query = (
            session.query(
                Employee.name,
                func.sum(Production.quantity_produced).label('total_quantity_produced')
            )
            .join(Production, Employee.id == Production.employee_id)
            .filter(Employee.name == name)
            .group_by(Employee.name)
        )

        result = employee_production_query.one_or_none()
        return result