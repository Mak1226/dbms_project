create or replace view customer_view_info as (
    select customer.customer_id, name, email, contact, DOB, (apartment || ' ' || street  || ' ' ||   city  || ' ' ||  state  || ' ' ||  pincode) as Address from customer natural join address
);

select * from customer_view_info;

call cust_view(101);

----------------------------------------------------

create or replace view cust_orders_view as (
    select * from orders
);

select * from cust_orders_view where customer_id = 110;

-------------------------------------------------

create or replace view seller_prod_view as
 (
    select * from sells order by stock desc
 );

 select * from seller_prod_view where seller_id = 518;

 ------------------------------------------------

 create or replace view order_product_view as (
    select * from contains
 );

 select * from order_product_view where order_id = 301;

--------------------------------------------------

create or replace view customer_product_details as (
    select product.pname as Product_Name, seller.sname as Seller_Name, sells.price, sells.stock from sells 
    natural join product     
    natural join seller     
);



CREATE or replace VIEW product_price_avg AS (
SELECT pname, cast(AVG(sells.price) as integer) AS average_price
FROM Product
LEFT JOIN sells ON Product.product_id = sells.product_id
GROUP BY Product.product_id, pname);

CREATE OR REPLACE VIEW sales_per_day AS
SELECT date, SUM(amount) AS total_sales
FROM orders
GROUP BY date;

CREATE OR REPLACE VIEW most_sold_items AS
SELECT s.seller_id, s.sname AS seller_name, SUM(c.counts * c.cost) AS total_sales
FROM seller s
JOIN sells sl ON s.seller_id = sl.seller_id
JOIN contains c ON sl.seller_id = c.seller_id AND sl.product_id = c.product_id
GROUP BY s.seller_id, s.sname
ORDER BY SUM(c.counts * c.cost) DESC;

