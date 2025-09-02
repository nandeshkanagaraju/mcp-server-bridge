from fastapi import APIRouter
from sqlalchemy import text
from config.database import SessionLocal

router = APIRouter()

@router.get("/health")
def health_check():
    db = SessionLocal()
    try:
        db.execute(text("SELECT 1"))  # ✅ Works for MySQL
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": "Database not reachable"}
    finally:
        db.close()
