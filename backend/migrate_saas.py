import logging
from sqlalchemy import text
from database import engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("migrate_saas")

def migrate():
    with engine.connect() as conn:
        try:
            logger.info("Adding is_pro_user column...")
            conn.execute(text("ALTER TABLE users ADD COLUMN is_pro_user BOOLEAN DEFAULT FALSE;"))
            
            logger.info("Adding stripe_customer_id column...")
            conn.execute(text("ALTER TABLE users ADD COLUMN stripe_customer_id VARCHAR(100);"))
            
            logger.info("Adding subscription_end_date column...")
            conn.execute(text("ALTER TABLE users ADD COLUMN subscription_end_date TIMESTAMP WITHOUT TIME ZONE;"))
            
            conn.commit()
            logger.info("SaaS migration fully completed successfully!")
            
        except Exception as e:
            if "already exists" in str(e).lower() or "duplicate column" in str(e).lower():
                logger.info(f"Skipping migration - columns may already exist: {e}")
            else:
                conn.rollback()
                logger.error(f"Migration error: {e}")
                raise

if __name__ == "__main__":
    migrate()
