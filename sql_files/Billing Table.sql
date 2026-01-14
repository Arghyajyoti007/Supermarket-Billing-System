-- Billing Details (Stores Every Single Product that Customer Brought)
create table billing_details (
	bill_id int not null,
    cust_id int not null,
    cust_name varchar(50) not null,
    p_id int not null,
    p_quantity int not null,
    timestamp timestamp default current_timestamp
); 

select * from billing_details;
