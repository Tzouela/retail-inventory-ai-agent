-- Migration 003: Create sales table
CREATE TABLE IF NOT EXISTS sales (
    sale_id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT NOT NULL,
    quantity_sold INT NOT NULL,
    price_sold DECIMAL(10,2) NOT NULL,
    date_sold DATETIME NOT NULL,
    FOREIGN KEY (stock_id) REFERENCES stock(stock_id)
);