from models.production import Production
from database import session

def save(production_data):
    try:
        production = Production(
            product_id=production_data['product_id'],
            quantity_produce=production_data['quantity_produce'],
            date_produce=production_data['date_produce']
        )
        
        session.add(production)
        session.commit()
        return production
    except Exception as e:
        session.rollback()  # Roll back the transaction in case of an error
        # Optionally, log the error
        print(f"Error saving production: {e}")
        raise ValueError(f"Error saving production: {str(e)}")
    finally:
        session.remove()  # Ensure session is properly closed

def find_all():
    try:
        # Query all production records from the database
        productions = session.query(Production).all()
        return productions
    except Exception as e:
        # Optionally, log the error
        print(f"Error retrieving productions: {e}")
        raise ValueError(f"Error retrieving productions: {str(e)}")
    finally:
        session.remove()  # Ensure session is properly closed
