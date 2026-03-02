SELECT * FROM pizza_db.sales;
-- MAKE EXPLORATORY DATA ANALYSIS REPORT --
-- ANSWERING BUSINESS PROBLEMS -- KPIS --
SELECT SUM(total_price) as Total_Revenue from sales;
Select count(pizza_id) as Total_Pizzas_made from sales;
select count(distinct order_id) as total_orders from sales;
select ROUND(SUM(total_price) / COUNT(DISTINCT order_id), 2) 
AS avg_order_value
FROM sales;
select sum(quantity) from sales;
select round(sum(quantity) / count(distinct order_id),0) as Avg_Pizzas_per_Order from sales;
select cast(sum(quantity) * 1.0 / count(distinct order_id) as decimal (10,2))
as AVERAGE_PIZZAS_PER_ORDER
from sales;

-- BUSINESS PROBLEM STATEMENTS -- CHART REQUIREMENTS --
-- 1. Daily Trend for Total Orders

-- SELECT 
--     DAYNAME(order_date) AS Order_Days,
--     COUNT(DISTINCT order_id) AS Total_Orders
-- FROM sales
-- GROUP BY Order_Days
-- ORDER BY DAYOFWEEK(order_date);


-- 1. Daily Trend for Orders
SELECT 
    DAYNAME(order_date) AS Order_Days, 
    COUNT(DISTINCT order_id) AS Total_Orders
FROM sales
GROUP BY Order_Days, DAYOFWEEK(order_date) -- Adding this solves the error
ORDER BY DAYOFWEEK(order_date);

-- 2. Hourly Trend for Orders
Select
	hour(order_time) as Order_Hours,
    count(distinct order_id) as Orders,
    sum(quantity) as Pizzas_Ordered
from sales
group by hour(order_time)
order by Pizzas_Ordered desc;

-- 3. Percentage of Sales by Pizza category
SELECT * FROM pizza_db.sales;
select 
	coalesce(pizza_category, 'Total') as Category,
    sum(total_price) as Sales,
    cast((sum(total_price)* 100) / (select sum(total_price) from sales) as decimal (10 ,2)) as Sales_Percent
from sales
group by pizza_category with rollup;
-- order by Sales_Percent desc

-- 4. Percentage of Sales by Pizza Size
select 
	coalesce(pizza_size, 'Total') as Pizza_Size,
    sum(total_price) as Sales,
    cast((sum(total_price)* 100) / (select sum(total_price) from sales) as decimal (10 ,2)) as Sales_Percent
from sales
group by pizza_size with rollup;

-- 5. Top 5 Best Seller by Total Pizzas Sold
select 
	pizza_name_id as Pizza,
    sum(quantity) as Pizzas_Sold,
    cast(sum(total_price) as decimal (10, 2)) as Total_Sales 
from sales
group by pizza_name_id
order by Pizzas_Sold desc
LIMIT 5;

-- 6. Worst 5 Bottom Seller by Total Pizzas Sold
select 
	pizza_name_id as Pizza,
    sum(quantity) as Pizzas_Sold,
    cast(sum(total_price) as decimal (10, 2)) as Total_Sales 
from sales
group by pizza_name_id
order by Pizzas_Sold
LIMIT 5;





