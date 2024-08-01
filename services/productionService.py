from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from database import db
from models.production import Production
from models.product import Product

def save(production_data):
    with Session(db.engine) as session:
        try:
            # Check if the product exists
            product = session.query(Product).filter_by(id=production_data['product_id']).first()
            if not product:
                raise ValueError(f"Product with ID {production_data['product_id']} does not exist.")

            # Create and add the new production record
            new_production = Production(
                product_id=production_data['product_id'],
                quantity_produced=production_data['quantity_produced'],
                date_produced=production_data['date_produced']
            )
            session.add(new_production)
            session.commit()
            session.refresh(new_production)
            return new_production
        except IntegrityError as e:
            session.rollback()
            raise
        except ValueError as e:
            raise
        except Exception as e:
            print(f"Error in save function: {e}")  # For debugging
            raise

def find_all():
    query = db.select(Production)
    productions = db.session.execute(query).scalars().all()
    return productions

