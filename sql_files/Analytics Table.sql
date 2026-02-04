-- Analytics Table
CREATE TABLE analytics_table (
    bill_id INT AUTO_INCREMENT PRIMARY KEY,
    c_id INT not null,
    c_name VARCHAR(100) not null,
    c_ph_no VARCHAR(10) not null,
    total_bill_value DECIMAL(10,2) not null,
    total_amount_payble_after_tax DECIMAL(10,2) not null,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

select * from analytics_table;
