import mysql.connector
from config.logger import logger

def run_health_check(db_config: dict):
    logger.info("Running health check for database...")
    try:
        conn = mysql.connector.connect(**db_config)
        conn.close()
        logger.info("✅ Database connection healthy.")
        return {"status": "healthy"}
    except Exception as e:
        logger.error(f"❌ Database health check failed: {e}")
        return {"status": "unhealthy", "message": str(e)}
