-- Seed Data: Mock retail inventory for demo purposes
-- 10 products, stock per size/colour, 60 days of sales history

USE inventory_db;

-- =====================
-- PRODUCTS
-- =====================
INSERT INTO products (name, brand, category, sku, supplier, price, description) VALUES
('Air Max 90', 'Nike', 'Lifestyle', 'NK-AM90-001', 'Nike Distribution EU', 1299.00, 'Classic Nike Air Max 90 with visible Air unit'),
('Stan Smith', 'Adidas', 'Lifestyle', 'AD-SS-001', 'Adidas Nordic Supply', 899.00, 'Iconic Adidas Stan Smith leather sneaker'),
('Chuck Taylor All Star', 'Converse', 'Lifestyle', 'CV-CT-001', 'Converse Europe BV', 699.00, 'Classic high-top canvas sneaker'),
('Ultraboost 22', 'Adidas', 'Running', 'AD-UB22-001', 'Adidas Nordic Supply', 1799.00, 'High performance running shoe with Boost midsole'),
('React Infinity Run 3', 'Nike', 'Running', 'NK-RI3-001', 'Nike Distribution EU', 1599.00, 'Nike React foam for maximum cushioning'),
('Classic Leather', 'Reebok', 'Lifestyle', 'RB-CL-001', 'Reebok EMEA Supply', 799.00, 'Timeless Reebok Classic Leather sneaker'),
('Old Skool', 'Vans', 'Skate', 'VN-OS-001', 'Vans Europe Distribution', 749.00, 'Iconic Vans Old Skool with side stripe'),
('Gel-Kayano 29', 'ASICS', 'Running', 'AS-GK29-001', 'ASICS Europe BV', 1699.00, 'Stability running shoe with Gel cushioning'),
('Suede Classic', 'Puma', 'Lifestyle', 'PM-SC-001', 'Puma Nordic AB', 849.00, 'Iconic Puma Suede in premium materials'),
('Fresh Foam 1080v12', 'New Balance', 'Running', 'NB-FF1080-001', 'New Balance Europe', 1899.00, 'Premium daily trainer with Fresh Foam X midsole');

-- =====================
-- STOCK (per size and colour)
-- Some intentionally low to trigger reorder recommendations
-- =====================

-- Air Max 90 (product_id: 1) - HIGH SELLER, some sizes critically low
INSERT INTO stock (product_id, size, colour, quantity, minimum_quantity) VALUES
(1, '40', 'White/Grey', 2, 5),
(1, '41', 'White/Grey', 1, 5),
(1, '42', 'White/Grey', 8, 5),
(1, '43', 'White/Grey', 3, 5),
(1, '40', 'Black/Black', 6, 5),
(1, '42', 'Black/Black', 2, 5),
(1, '44', 'Black/Black', 1, 5);

-- Stan Smith (product_id: 2) - MODERATE SELLER, healthy stock
INSERT INTO stock (product_id, size, colour, quantity, minimum_quantity) VALUES
(2, '39', 'White/Green', 12, 5),
(2, '40', 'White/Green', 15, 5),
(2, '41', 'White/Green', 10, 5),
(2, '42', 'White/Green', 8, 5),
(2, '43', 'White/Green', 11, 5),
(2, '41', 'White/Navy', 9, 5),
(2, '42', 'White/Navy', 7, 5);

-- Chuck Taylor All Star (product_id: 3) - SLOW SELLER, overstocked
INSERT INTO stock (product_id, size, colour, quantity, minimum_quantity) VALUES
(3, '39', 'Black/White', 20, 5),
(3, '40', 'Black/White', 25, 5),
(3, '41', 'Black/White', 18, 5),
(3, '42', 'Black/White', 22, 5),
(3, '40', 'Red/White', 15, 5),
(3, '41', 'Red/White', 17, 5);

-- Ultraboost 22 (product_id: 4) - HIGH SELLER, critically low stock
INSERT INTO stock (product_id, size, colour, quantity, minimum_quantity) VALUES
(4, '40', 'Core Black', 1, 5),
(4, '41', 'Core Black', 2, 5),
(4, '42', 'Core Black', 1, 5),
(4, '43', 'Core Black', 3, 5),
(4, '42', 'Cloud White', 2, 5),
(4, '43', 'Cloud White', 1, 5),
(4, '44', 'Cloud White', 4, 5);

-- React Infinity Run 3 (product_id: 5) - MODERATE SELLER, some low
INSERT INTO stock (product_id, size, colour, quantity, minimum_quantity) VALUES
(5, '40', 'Black/White', 4, 5),
(5, '41', 'Black/White', 7, 5),
(5, '42', 'Black/White', 3, 5),
(5, '43', 'Black/White', 6, 5),
(5, '41', 'Blue/Silver', 8, 5),
(5, '42', 'Blue/Silver', 5, 5);

-- Classic Leather (product_id: 6) - SLOW SELLER, healthy stock
INSERT INTO stock (product_id, size, colour, quantity, minimum_quantity) VALUES
(6, '39', 'White/White', 14, 5),
(6, '40', 'White/White', 16, 5),
(6, '41', 'White/White', 12, 5),
(6, '42', 'White/White', 10, 5),
(6, '40', 'Black/White', 11, 5),
(6, '41', 'Black/White', 9, 5);

-- Old Skool (product_id: 7) - MODERATE SELLER, some low sizes
INSERT INTO stock (product_id, size, colour, quantity, minimum_quantity) VALUES
(7, '39', 'Black/White', 3, 5),
(7, '40', 'Black/White', 8, 5),
(7, '41', 'Black/White', 2, 5),
(7, '42', 'Black/White', 6, 5),
(7, '40', 'Navy/White', 4, 5),
(7, '41', 'Navy/White', 7, 5),
(7, '42', 'Navy/White', 3, 5);

-- Gel-Kayano 29 (product_id: 8) - HIGH SELLER, very low stock
INSERT INTO stock (product_id, size, colour, quantity, minimum_quantity) VALUES
(8, '40', 'Black/Gunmetal', 1, 5),
(8, '41', 'Black/Gunmetal', 2, 5),
(8, '42', 'Black/Gunmetal', 1, 5),
(8, '43', 'Black/Gunmetal', 3, 5),
(8, '41', 'Blue/Yellow', 2, 5),
(8, '42', 'Blue/Yellow', 1, 5);

-- Suede Classic (product_id: 9) - MODERATE SELLER, healthy stock
INSERT INTO stock (product_id, size, colour, quantity, minimum_quantity) VALUES
(9, '39', 'Navy/White', 10, 5),
(9, '40', 'Navy/White', 12, 5),
(9, '41', 'Navy/White', 9, 5),
(9, '42', 'Navy/White', 11, 5),
(9, '40', 'Red/White', 8, 5),
(9, '41', 'Red/White', 7, 5);

-- Fresh Foam 1080v12 (product_id: 10) - HIGH SELLER, critically low
INSERT INTO stock (product_id, size, colour, quantity, minimum_quantity) VALUES
(10, '40', 'Black/Thunder', 2, 5),
(10, '41', 'Black/Thunder', 1, 5),
(10, '42', 'Black/Thunder', 3, 5),
(10, '43', 'Black/Thunder', 2, 5),
(10, '41', 'White/Blue', 1, 5),
(10, '42', 'White/Blue', 4, 5),
(10, '44', 'White/Blue', 2, 5);

-- =====================
-- SALES (last 60 days)
-- High sellers: Air Max 90 (stock_ids 1-7), Ultraboost 22 (22-28),
--               Gel-Kayano 29 (50-55), Fresh Foam 1080v12 (56-62)
-- =====================

-- Air Max 90 sales (high velocity - explains low stock)
INSERT INTO sales (stock_id, quantity_sold, price_sold, date_sold) VALUES
(1, 2, 1299.00, DATE_SUB(NOW(), INTERVAL 58 DAY)),
(1, 3, 1299.00, DATE_SUB(NOW(), INTERVAL 50 DAY)),
(1, 2, 1199.00, DATE_SUB(NOW(), INTERVAL 42 DAY)),
(1, 4, 1299.00, DATE_SUB(NOW(), INTERVAL 35 DAY)),
(1, 3, 1299.00, DATE_SUB(NOW(), INTERVAL 25 DAY)),
(1, 2, 1299.00, DATE_SUB(NOW(), INTERVAL 15 DAY)),
(1, 3, 1299.00, DATE_SUB(NOW(), INTERVAL 7 DAY)),
(2, 3, 1299.00, DATE_SUB(NOW(), INTERVAL 55 DAY)),
(2, 4, 1299.00, DATE_SUB(NOW(), INTERVAL 45 DAY)),
(2, 3, 1299.00, DATE_SUB(NOW(), INTERVAL 30 DAY)),
(2, 5, 1299.00, DATE_SUB(NOW(), INTERVAL 18 DAY)),
(2, 4, 1299.00, DATE_SUB(NOW(), INTERVAL 8 DAY)),
(4, 2, 1299.00, DATE_SUB(NOW(), INTERVAL 52 DAY)),
(4, 3, 1299.00, DATE_SUB(NOW(), INTERVAL 38 DAY)),
(4, 4, 1299.00, DATE_SUB(NOW(), INTERVAL 22 DAY)),
(4, 3, 1299.00, DATE_SUB(NOW(), INTERVAL 10 DAY));

-- Stan Smith sales (moderate velocity)
INSERT INTO sales (stock_id, quantity_sold, price_sold, date_sold) VALUES
(8, 2, 899.00, DATE_SUB(NOW(), INTERVAL 55 DAY)),
(9, 3, 899.00, DATE_SUB(NOW(), INTERVAL 40 DAY)),
(10, 2, 899.00, DATE_SUB(NOW(), INTERVAL 28 DAY)),
(11, 1, 799.00, DATE_SUB(NOW(), INTERVAL 15 DAY)),
(12, 2, 899.00, DATE_SUB(NOW(), INTERVAL 5 DAY));

-- Chuck Taylor sales (slow velocity)
INSERT INTO sales (stock_id, quantity_sold, price_sold, date_sold) VALUES
(15, 1, 699.00, DATE_SUB(NOW(), INTERVAL 50 DAY)),
(16, 2, 699.00, DATE_SUB(NOW(), INTERVAL 30 DAY)),
(17, 1, 649.00, DATE_SUB(NOW(), INTERVAL 12 DAY));

-- Ultraboost 22 sales (very high velocity - explains critically low stock)
INSERT INTO sales (stock_id, quantity_sold, price_sold, date_sold) VALUES
(22, 3, 1799.00, DATE_SUB(NOW(), INTERVAL 57 DAY)),
(22, 4, 1799.00, DATE_SUB(NOW(), INTERVAL 48 DAY)),
(23, 3, 1799.00, DATE_SUB(NOW(), INTERVAL 40 DAY)),
(23, 5, 1799.00, DATE_SUB(NOW(), INTERVAL 30 DAY)),
(24, 4, 1799.00, DATE_SUB(NOW(), INTERVAL 22 DAY)),
(24, 3, 1699.00, DATE_SUB(NOW(), INTERVAL 14 DAY)),
(25, 5, 1799.00, DATE_SUB(NOW(), INTERVAL 7 DAY)),
(25, 4, 1799.00, DATE_SUB(NOW(), INTERVAL 2 DAY));

-- React Infinity Run 3 sales (moderate)
INSERT INTO sales (stock_id, quantity_sold, price_sold, date_sold) VALUES
(29, 2, 1599.00, DATE_SUB(NOW(), INTERVAL 45 DAY)),
(30, 3, 1599.00, DATE_SUB(NOW(), INTERVAL 28 DAY)),
(31, 2, 1499.00, DATE_SUB(NOW(), INTERVAL 12 DAY));

-- Old Skool sales (moderate)
INSERT INTO sales (stock_id, quantity_sold, price_sold, date_sold) VALUES
(43, 3, 749.00, DATE_SUB(NOW(), INTERVAL 50 DAY)),
(44, 2, 749.00, DATE_SUB(NOW(), INTERVAL 33 DAY)),
(45, 3, 749.00, DATE_SUB(NOW(), INTERVAL 18 DAY)),
(46, 2, 699.00, DATE_SUB(NOW(), INTERVAL 6 DAY));

-- Gel-Kayano 29 sales (very high velocity)
INSERT INTO sales (stock_id, quantity_sold, price_sold, date_sold) VALUES
(50, 3, 1699.00, DATE_SUB(NOW(), INTERVAL 56 DAY)),
(50, 4, 1699.00, DATE_SUB(NOW(), INTERVAL 46 DAY)),
(51, 3, 1699.00, DATE_SUB(NOW(), INTERVAL 36 DAY)),
(51, 5, 1699.00, DATE_SUB(NOW(), INTERVAL 26 DAY)),
(52, 4, 1699.00, DATE_SUB(NOW(), INTERVAL 16 DAY)),
(52, 3, 1699.00, DATE_SUB(NOW(), INTERVAL 6 DAY)),
(53, 5, 1699.00, DATE_SUB(NOW(), INTERVAL 3 DAY));

-- Suede Classic sales (moderate)
INSERT INTO sales (stock_id, quantity_sold, price_sold, date_sold) VALUES
(56, 2, 849.00, DATE_SUB(NOW(), INTERVAL 48 DAY)),
(57, 3, 849.00, DATE_SUB(NOW(), INTERVAL 30 DAY)),
(58, 2, 799.00, DATE_SUB(NOW(), INTERVAL 14 DAY));

-- Fresh Foam 1080v12 sales (high velocity)
INSERT INTO sales (stock_id, quantity_sold, price_sold, date_sold) VALUES
(63, 3, 1899.00, DATE_SUB(NOW(), INTERVAL 55 DAY)),
(63, 4, 1899.00, DATE_SUB(NOW(), INTERVAL 44 DAY)),
(64, 3, 1899.00, DATE_SUB(NOW(), INTERVAL 33 DAY)),
(64, 5, 1899.00, DATE_SUB(NOW(), INTERVAL 22 DAY)),
(65, 4, 1899.00, DATE_SUB(NOW(), INTERVAL 11 DAY)),
(65, 3, 1799.00, DATE_SUB(NOW(), INTERVAL 3 DAY));