import os
import logging
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)


def get_connection():
    """Create and return a MySQL database connection."""
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "mysql-db"),
            port=int(os.getenv("DB_PORT", "3306")),
            database=os.getenv("DB_NAME", "inventory_db"),
            user=os.getenv("DB_USER", "inventory_user"),
            password=os.getenv("DB_PASSWORD", "inventory_pass")
        )
        if connection.is_connected():
            logger.info("Successfully connected to MySQL database")
            return connection
    except Error as e:
        logger.error(f"Error connecting to MySQL: {e}")
        raise


def execute_query(query: str, params: tuple = None) -> list:
    """Execute a SELECT query and return results as a list of dictionaries."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(query, params or ())
        results = cursor.fetchall()
        return results
    except Error as e:
        logger.error(f"Error executing query: {e}")
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()

def execute_write(query: str, params: tuple = None) -> int:
    """Execute an INSERT, UPDATE, or DELETE query and return affected rows."""
    connection = None
    cursor = None
    try:
        connection = get_connection()
        cursor = connection.cursor()
        cursor.execute(query, params or ())
        connection.commit()
        affected_rows = cursor.rowcount
        logger.info(f"Write query affected {affected_rows} rows")
        return affected_rows
    except Error as e:
        logger.error(f"Error executing write query: {e}")
        if connection:
            connection.rollback()
        raise
    finally:
        if cursor:
            cursor.close()
        if connection and connection.is_connected():
            connection.close()