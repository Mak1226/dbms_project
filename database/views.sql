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
    select p.name, s.name, sells.price, sells.stock from sells 
    natural join product as p
    natural join seller as s
);

CREATE or replace VIEW product_price_avg AS (
SELECT pname, cast(AVG(sells.price) as integer) AS average_price
FROM Product
LEFT JOIN sells ON Product.product_id = sells.product_id
GROUP BY Product.product_id, pname);
