import time
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://myuser:mypassword@db:5432/login_db"
)



# Retry logic
for i in range(5):
    try:
        engine = create_engine(DATABASE_URL)
        connection = engine.connect()
        connection.close()
        print("✅ Connected to DB")
        break
    except Exception as e:
        print("⏳ DB not ready, retrying...")
        time.sleep(5)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()