SELECT * from customer_transactions_project2 LIMIT 100;

SELECT Region, count(DISTINCT Customer_ID) as customers, SUM(Amount) as Revnue from customer_transactions_project2
GROUP BY `Region`
ORDER BY Revnue DESC LIMIT 100;

SELECT Customer_Name , City,COUNT(*) as Perchases, SUM(Amount) as Total_spent from customer_transactions_project2
GROUP BY `Customer_ID`,`Customer_Name`,`City` 
ORDER BY Total_Spent DESC
LIMIT 10;

SELECT * from customer_transactions_project2 LIMIT 100;

SELECT Region, count(DISTINCT Customer_ID) as customers, SUM(Amount) as Revnue from customer_transactions_project2
GROUP BY `Region`
ORDER BY Revnue DESC LIMIT 100;

SELECT * from customer_transactions_project2 LIMIT 100;

select Product_Category,count(*) as Transactions , sum(Amount) as Revenue from customer_transactions_project2
GROUP BY Product_Category
ORDER BY Revenue DESC LIMIT 100;

SELECT * from customer_transactions_project2 LIMIT 100;

SELECT 
    CASE 
        WHEN purchase_count = 1 THEN 'One-Time'
        ELSE 'Repeat'
    END as Type,
    COUNT(*) as Customers
FROM (
    SELECT 
        Customer_ID, 
        COUNT(*) as purchase_count
    FROM customer_transactions_project2
    GROUP BY Customer_ID
) AS customer_counts    -- ADD THIS ALIAS!
GROUP BY Type LIMIT 100;

--;

SELECT Customer_ID, COUNT(*) as purchases
FROM customer_transactions_project2 
GROUP BY Customer_ID
ORDER BY purchases LIMIT 100;

SELECT 
    CASE 
        WHEN purchase_count = 1 THEN 'One-Time'
        ELSE 'Repeat'
    END as Type,
    COUNT(*) as Customers
FROM (
    SELECT 
        Transaction_ID, 
        COUNT(*) as purchase_count
    FROM customer_transactions_project2
    GROUP BY Transaction_ID
) AS customer_counts  
GROUP BY Type LIMIT 100;
SELECT 
    CASE 
        WHEN purchase_count = 1 THEN 'One-Time'
        ELSE 'Repeat'
    END as Type,
    COUNT(*) as Customers
FROM (
    SELECT 
        Customer_ID, 
        COUNT(*) as purchase_count
    FROM customer_transactions_project2
    GROUP BY Customer_ID
) AS customer_counts 