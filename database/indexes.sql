
-- If any one wants to see the product with certain price range then BTree index is used on that case
create index price_range on sells(price);

explain analyze select * from sells where price between 5 and 100;

-- For pattern matching, gin index will be used 
create extension pg_trgm;
create index trgm_idx on product using gin (pname gin_trgm_ops);

explain analyze select * from product where pname like '%con%';


-- For equality condition, hash index will be preferred
create index status_check on payment using hash(status);
explain analyze select * from payment where status = 'Accepted';
