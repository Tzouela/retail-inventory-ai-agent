import logging
from strands import tool
from tools.db.db_client import execute_query

logger = logging.getLogger(__name__)


@tool
def check_low_stock() -> list:
    """Check current inventory and return all products with stock below minimum quantity.
    
    Returns a list of stock entries where quantity has fallen below the minimum
    threshold, including product name, brand, size, colour, current quantity,
    and minimum required quantity. Use this to identify products that need reordering.
    
    Returns:
        List of dictionaries containing low stock items with their details.
    """
    logger.info("Checking low stock levels...")
    
    query = """
        SELECT 
            p.product_id,
            p.name,
            p.brand,
            p.category,
            s.stock_id,
            s.size,
            s.colour,
            s.quantity,
            s.minimum_quantity,
            (s.minimum_quantity - s.quantity) as units_needed
        FROM stock s
        JOIN products p ON s.product_id = p.product_id
        WHERE s.quantity < s.minimum_quantity
        ORDER BY s.quantity ASC, p.name ASC
    """
    
    results = execute_query(query)
    logger.info(f"Found {len(results)} low stock entries")
    return results


@tool
def get_sales_velocity() -> list:
    """Calculate average daily sales velocity for each product over the last 60 days.
    
    Analyzes sales history to determine how quickly each product sells on average.
    This helps prioritize reorder quantities — fast-selling products need larger
    reorders than slow-selling ones.
    
    Returns:
        List of dictionaries with product name, brand, total units sold,
        number of days with sales, and average daily sales rate.
    """
    logger.info("Calculating sales velocity...")
    
    query = """
        SELECT 
            p.product_id,
            p.name,
            p.brand,
            p.category,
            SUM(sa.quantity_sold) as total_sold,
            COUNT(DISTINCT DATE(sa.date_sold)) as days_with_sales,
            ROUND(SUM(sa.quantity_sold) / 60, 2) as avg_daily_sales,
            ROUND(SUM(sa.quantity_sold) / 60 * 7, 2) as avg_weekly_sales
        FROM sales sa
        JOIN stock s ON sa.stock_id = s.stock_id
        JOIN products p ON s.product_id = p.product_id
        WHERE sa.date_sold >= DATE_SUB(NOW(), INTERVAL 60 DAY)
        GROUP BY p.product_id, p.name, p.brand, p.category
        ORDER BY avg_daily_sales DESC
    """
    
    results = execute_query(query)
    logger.info(f"Calculated velocity for {len(results)} products")
    return results