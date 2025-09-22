import random
from faker import Faker
from sqlalchemy import (
    create_engine, MetaData, Table, Column, Integer,
    String, Date, DECIMAL, ForeignKey, text
)
from sqlalchemy.exc import OperationalError
from config.settings import settings
from config.logger import logger

# --- Configuration ---
DATABASE_URL = (
    f"mysql+pymysql://{settings.DB_USER}:{settings.DB_PASSWORD}@"
    f"{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}"
)

def setup_database():
    """
    Connects to the database, drops all existing tables to ensure a clean state,
    creates a new schema, and populates it with realistic fake data.
    """
    try:
        engine = create_engine(DATABASE_URL)
        metadata = MetaData()
        fake = Faker()
        logger.info("Successfully created database engine.")
    except Exception as e:
        logger.critical(f"❌ Failed to initialize database engine: {e}")
        logger.critical("Please check your database connection settings in the .env file.")
        return

    # --- Define Table Schema ---
    departments = Table(
        "departments", metadata,
        Column("dept_id", Integer, primary_key=True, autoincrement=True),
        Column("dept_name", String(100), nullable=False, unique=True),
    )
    employees = Table(
        "employees", metadata,
        Column("emp_id", Integer, primary_key=True, autoincrement=True),
        Column("first_name", String(50), nullable=False),
        Column("last_name", String(50), nullable=False),
        Column("email", String(100), nullable=False, unique=True),
        Column("phone_number", String(30)),
        Column("hire_date", Date, nullable=False),
        Column("job_title", String(100)),
        Column("salary", DECIMAL(10, 2)),
        Column("dept_id", Integer, ForeignKey("departments.dept_id")),
    )
    # ... (Add other table definitions like projects, assignments if needed)

    try:
        with engine.connect() as conn:
            with conn.begin() as trans: # Use a single transaction for the whole process
                logger.info("--- Starting Database Setup ---")
                
                logger.info("Dropping all existing tables...")
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))
                metadata.drop_all(conn, checkfirst=True)
                conn.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))
                logger.info("All tables dropped successfully.")

                logger.info("Creating new tables...")
                metadata.create_all(conn)
                logger.info("Tables created successfully.")

                logger.info("Populating database with sample data...")
                
                dept_names = ["Engineering", "Sales", "Marketing", "Human Resources", "Finance"]
                dept_data = [{"dept_name": name} for name in dept_names]
                conn.execute(departments.insert(), dept_data)

                emp_data = []
                for i in range(150):
                    emp_data.append({
                        "first_name": fake.first_name(),
                        "last_name": fake.last_name(),
                        "email": f"{fake.user_name()}{i}@mcp-corp.com",
                        "hire_date": fake.date_between(start_date="-5y", end_date="today"),
                        "job_title": fake.job(),
                        "salary": fake.pydecimal(left_digits=6, right_digits=2, min_value=40000),
                        "dept_id": random.randint(1, len(dept_names)),
                    })
                conn.execute(employees.insert(), emp_data)

            logger.info("✅ Database setup complete. Transaction committed.")

    except OperationalError as e:
        logger.critical(f"❌ DATABASE CONNECTION FAILED: {e.orig}")
        logger.critical("Please ensure the MySQL server is running and your .env credentials are correct.")
    except Exception as e:
        logger.critical(f"❌ An unexpected error occurred during database setup: {e}", exc_info=True)

if __name__ == "__main__":
    setup_database()