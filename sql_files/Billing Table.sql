-- Billing Details (Stores Every Single Product that Customer Brought)
-- security and performance rule: every table must have a Primary Key
CREATE TABLE billing_details (
    entry_id INT AUTO_INCREMENT PRIMARY KEY,
    bill_id INT NOT NULL,
    cust_id INT NOT NULL,
    cust_name VARCHAR(50) NOT NULL,
    p_id INT NOT NULL,
    p_quantity INT NOT NULL,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select * from billing_details;
