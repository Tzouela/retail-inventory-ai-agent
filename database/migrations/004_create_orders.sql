-- Migration 004: Create orders table
CREATE TABLE IF NOT EXISTS orders (
    order_id INT AUTO_INCREMENT PRIMARY KEY,
    stock_id INT NOT NULL,
    quantity_ordered INT NOT NULL,
    approved_by VARCHAR(255),
    status ENUM('pending', 'approved', 'placed', 'cancelled') NOT NULL DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    approved_at DATETIME,
    FOREIGN KEY (stock_id) REFERENCES stock(stock_id)
);