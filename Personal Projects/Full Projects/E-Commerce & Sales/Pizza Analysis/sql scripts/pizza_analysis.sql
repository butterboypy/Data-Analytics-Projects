CREATE DATABASE Pizza_DB;
USE Pizza_DB
CREATE TABLE sales (
	pizza_id INT,
	order_id INT,
	pizza_name_id TEXT,
	quantity TINYINT,
	order_date TEXT,
	order_time TIME,
	unit_price DECIMAL(10,2),
	total_price DECIMAL(10,2),
	pizza_size VARCHAR(5),
	pizza_category VARCHAR(50),
	pizza_ingredients TEXT,
	pizza_name TEXT
);

-- Clear out any previous partial data
-- TRUNCATE TABLE sales;

-- This will now work because the service has been restarted!
LOAD DATA INFILE "E:/PROJECTS/Datasets Practice/pizza/pizza_sales.csv"
INTO TABLE sales
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 ROWS;

-- The moment of truth: should return 48,620
SELECT COUNT(*) FROM sales;

-- 1. Turn off the safety switch
SET SQL_SAFE_UPDATES = 0;

-- 2. Run your date conversion again
UPDATE sales 
SET order_date = STR_TO_DATE(order_date, '%d-%m-%Y');

-- 3. Permanently change the column type to DATE
ALTER TABLE sales MODIFY COLUMN order_date DATE;

-- 4. Turn the safety switch back on (optional but recommended)
SET SQL_SAFE_UPDATES = 1;

select * from sales


