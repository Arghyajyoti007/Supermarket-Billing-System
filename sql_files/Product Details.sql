
-- Product Details Table
create table p_details (
	pid int primary key auto_increment,
    p_name text not null,
    p_price decimal(10,4) not null,
    p_stock int not null default 0
);

INSERT INTO p_details (p_name, p_price, p_stock)
VALUES 
    ('Gaming Mouse', 45.5000, 120),
    ('UltraWide Monitor', 350.0000, 15),
    ('USB-C Hub', 25.0000, 200),
    ('Noise Cancelling Headphones', 199.9500, 30);
    


