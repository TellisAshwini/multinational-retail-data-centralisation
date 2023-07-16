#Milestone 3
order_table_updates ='''
ALTER TABLE orders_table ALTER COLUMN date_uuid TYPE uuid 
USING date_uuid::uuid;
ALTER TABLE orders_table ALTER COLUMN user_uuid TYPE uuid 
USING user_uuid::uuid;
ALTER TABLE orders_table ALTER COLUMN card_number TYPE varchar(19);
ALTER TABLE orders_table ALTER COLUMN store_code TYPE varchar(12);
ALTER TABLE orders_table ALTER COLUMN product_code TYPE varchar(11);
ALTER TABLE orders_table ALTER COLUMN product_quantity TYPE smallint;
'''

dim_users_updates = '''
ALTER TABLE dim_users ALTER COLUMN first_name TYPE varchar(255);
ALTER TABLE dim_users ALTER COLUMN last_name TYPE varchar(255);
ALTER TABLE dim_users ALTER COLUMN date_of_birth TYPE DATE;
ALTER TABLE dim_users ALTER COLUMN country_code TYPE varchar(2);
ALTER TABLE dim_users ALTER COLUMN user_uuid TYPE uuid 
USING user_uuid::uuid;
ALTER TABLE dim_users ALTER COLUMN join_date TYPE DATE;
'''
dim_store_updates ='''
ALTER TABLE dim_store_details ALTER COLUMN longitude TYPE float using longitude::float;
ALTER TABLE dim_store_details ALTER COLUMN locality TYPE varchar(255);
ALTER TABLE dim_store_details ALTER COLUMN store_code TYPE varchar(12);
ALTER TABLE dim_store_details ALTER COLUMN staff_numbers TYPE smallint using staff_numbers::smallint;
ALTER TABLE dim_store_details ALTER COLUMN opening_date TYPE date;
ALTER TABLE dim_store_details ALTER COLUMN store_type TYPE VARCHAR (255);
ALTER TABLE dim_store_details ALTER COLUMN latitude TYPE float using latitude::float;
ALTER TABLE dim_store_details ALTER COLUMN country_code TYPE VARCHAR (2);
ALTER TABLE dim_store_details ALTER COLUMN continent TYPE VARCHAR (255);
'''


dim_products_updates = '''
ALTER TABLE dim_products add column weight_class varchar(14)
update dim_products set weight_class =
case 
when weight < 2 then 'Light'
when (weight >= 2  and weight < 40) then 'Mid_Sized'
when (weight >= 40  and weight < 140) then 'Heavy'
when weight >= 140 then 'Truck_Required'
end;

ALTER TABLE dim_products RENAME COLUMN removed TO still_available;
alter table dim_products
alter column still_available
set data type boolean
using case
    when still_available = 'Still_avaliable' then true
    when still_available = 'Removed' then false
    else null
end;

ALTER TABLE dim_products ALTER COLUMN product_price TYPE float using product_price::float;
ALTER TABLE dim_products ALTER COLUMN weight TYPE float using weight::float;
ALTER TABLE dim_products RENAME COLUMN "EAN" TO EAN;
ALTER TABLE dim_products ALTER COLUMN EAN TYPE VARCHAR (17);
ALTER TABLE dim_products ALTER COLUMN product_code TYPE VARCHAR (11);
ALTER TABLE dim_products ALTER COLUMN date_added TYPE date;
ALTER TABLE dim_products ALTER COLUMN uuid TYPE uuid 
USING uuid::uuid;
ALTER TABLE dim_products ALTER COLUMN weight_class TYPE VARCHAR (14);
'''

dim_date_times_updates = '''
ALTER TABLE dim_date_times ALTER COLUMN month TYPE VARCHAR (2);
ALTER TABLE dim_date_times ALTER COLUMN year TYPE VARCHAR (4);
ALTER TABLE dim_date_times ALTER COLUMN day TYPE VARCHAR (2);
ALTER TABLE dim_date_times ALTER COLUMN time_period TYPE VARCHAR (10);
ALTER TABLE dim_date_times ALTER COLUMN date_uuid TYPE uuid 
USING date_uuid::uuid;
'''
dim_card_updates = '''
ALTER TABLE dim_card_details ALTER COLUMN  expiry_date TYPE VARCHAR (5);
ALTER TABLE dim_card_details ALTER COLUMN  card_number TYPE VARCHAR (22);
ALTER TABLE dim_card_details ALTER COLUMN date_payment_confirmed TYPE date;
'''
primary_key_updates = '''
ALTER TABLE dim_date_times ADD PRIMARY KEY (date_uuid);
ALTER TABLE dim_users ADD PRIMARY KEY (user_uuid);
ALTER TABLE dim_card_details ADD PRIMARY KEY (card_number);
ALTER TABLE dim_store_details ADD PRIMARY KEY (store_code);
ALTER TABLE dim_products ADD PRIMARY KEY (product_code);
'''
foriegn_key_updates = '''
ALTER TABLE orders_table ADD FOREIGN KEY (date_uuid) REFERENCES dim_date_times(date_uuid);
ALTER TABLE orders_table ADD FOREIGN KEY (user_uuid) REFERENCES dim_users(user_uuid);
ALTER TABLE orders_table ADD FOREIGN KEY (card_number) REFERENCES dim_card_details (card_number);
ALTER TABLE orders_table ADD FOREIGN KEY (store_code) REFERENCES dim_store_details(store_code);
ALTER TABLE orders_table ADD FOREIGN KEY (product_code) REFERENCES dim_products(product_code);
'''


#Milestone_4
task_1 = '''
select country_code country, count(*) total_no_stores 
from dim_store_details 
where store_type != 'Web Portal'
group by country_code order by 2 desc;
'''

task_2 = '''
select locality, count(*) total_no_stores 
from dim_store_details 
group by locality 
having count(*) >= 10
order by 2 desc;
'''

task_3 = '''
with sales_table as 
		(select 
		round(cast(sum(o.product_quantity*p.product_price)AS numeric),2) as total_sale, 
		d.month 
		from dim_date_times d
		inner join orders_table o on d.date_uuid = o.date_uuid
		inner join dim_products p on p.product_code = o.product_code
		group by month order by 1 desc)
		
select * from sales_table where total_sale > (select avg(total_sale) from sales_table)
'''

task_4 = '''
select count(o.*) numbers_of_sales,sum(o.product_quantity) product_quantity_count,
case 
when store_type = 'Web Portal' then 'Web'
when store_type <> 'Web Portal' then 'Offline'
end as location
from dim_store_details s
inner join orders_table o
on s.store_code = o.store_code
group by location
order by 1;
'''

task_5 = '''
with sales_table as 
	(select s.store_type as store_type, sum(o.product_quantity*p.product_price) total_sales
	from dim_store_details s
	inner join orders_table o on s.store_code = o.store_code
	inner join dim_products p on p.product_code = o.product_code
	group by s.store_type order by 2 desc)
	
select store_type, 
round(cast(total_sales as numeric), 2) as total_sales,
round(cast(total_sales*100/total as numeric), 2) as percentage
from (select st.*, sum(total_sales) over() as total from sales_table st)st
'''

task_6 = '''
select round(cast(sum(o.product_quantity*p.product_price)as numeric),2) as total_sales, 
d.year as year,
d.month as month	
from orders_table o 
inner join dim_date_times d on o.date_uuid = d. date_uuid 
inner join dim_products p on p.product_code = o.product_code
group by d.month , d.year
order by total_sales desc limit 10
'''

task_7 = '''
select sum(staff_numbers) total_staff_numbers,
country_code
from dim_store_details
group by 2
order by 1 desc;
'''

task_8 = '''
select round(cast(sum(o.product_quantity*p.product_price) as numeric), 2) total_sales,s.store_type, 
max(country_code) as country_code from dim_store_details  s
inner join orders_table o on o.store_code = s.store_code
inner join dim_products p on o.product_code = p.product_code
where s.country_code = 'DE' group by s.store_type
'''

task_9 = '''
with date_table as 
	(select d.year as year,
	cast(concat(d.year,'-',d.month, '-', d.day, ' ', timestamp) as timestamp) as date
	from dim_date_times d 
	inner join orders_table o on d.date_uuid = o.date_uuid
	inner join dim_store_details s on s.store_code = o.store_code
	order by date)
	
select year,
concat('hours: ', cast(round(avg(EXTRACT(HOUR FROM time_diff))) as text), 
	   ', minutes: ', cast(round(avg(EXTRACT(MINUTE FROM time_diff))) as text), 
	   ', seconds: ', cast(round(avg(EXTRACT(SECOND FROM time_diff))) as text)) 
	   as actual_time_taken

from
(select year, date, lead(date) over(partition by year) as lead_date,
lead(date) over(partition by year)-date as time_diff from date_table )date_table2
group by year
order by 2 desc
'''