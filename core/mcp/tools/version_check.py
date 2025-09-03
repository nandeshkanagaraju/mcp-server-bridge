import mysql.connector
from config.logger import logger

def run_version_check(db_config: dict):
    logger.info("Checking MySQL server version...")
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
        cursor.execute("SELECT VERSION()")
        version = cursor.fetchone()[0]
        cursor.close()
        conn.close()
        logger.info(f"✅ MySQL Server Version: {version}")
        return {"status": "success", "version": version}
    except Exception as e:
        logger.error(f"❌ Failed to get MySQL version: {e}")
        return {"status": "error", "message": str(e)}
