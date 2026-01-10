-- Create Customer Details table
create table cust_details (
	c_id int auto_increment primary key,
    c_full_name text not null,
    c_address text not null,
    c_ph_no varchar(10) unique not null,
    date_created timestamp default current_timestamp
);

-- View the Table Data
select * from cust_details;

