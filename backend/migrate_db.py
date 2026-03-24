import sqlalchemy as sa
from database import engine

def apply_migrations():
    """Adds new columns to ingredients table safely."""
    try:
        with engine.begin() as conn:
            # Check what dialect we are using
            dialect = engine.dialect.name
            
            # Syntax differs slightly for alter table. Postgres/SQLite standard:
            conn.execute(sa.text("ALTER TABLE ingredients ADD COLUMN name_ar VARCHAR(200);"))
            conn.execute(sa.text("ALTER TABLE ingredients ADD COLUMN is_golden BOOLEAN DEFAULT FALSE;"))
            conn.execute(sa.text("ALTER TABLE ingredients ADD COLUMN popularity_score FLOAT DEFAULT 1.0;"))
            
            # Create indexes for the new columns
            conn.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_ingredients_name_ar ON ingredients (name_ar);"))
            conn.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_ingredients_is_golden ON ingredients (is_golden);"))
            conn.execute(sa.text("CREATE INDEX IF NOT EXISTS ix_ingredients_pop_score ON ingredients (popularity_score);"))
            
            print("Successfully added new Golden Food columns to ingredients table.")
    except sa.exc.OperationalError as e:
        print(f"Migration error (columns might exist already): {e}")
        pass
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    apply_migrations()
