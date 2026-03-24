from database import engine
from sqlalchemy import text
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("verify")

def verify():
    with engine.connect() as conn:
        res = conn.execute(text("SELECT column_name FROM information_schema.columns WHERE table_name='users' AND (column_name='is_pro_user' OR column_name='stripe_customer_id' OR column_name='subscription_end_date')")).fetchall()
        logger.info(f"Existing columns: {res}")
        
if __name__ == "__main__":
    verify()
