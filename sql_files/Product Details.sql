
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
    
INSERT INTO p_details (p_name, p_price, p_stock)
VALUES 
    ('Mechanical Keyboard', 89.99, 45),
    ('Webcam 1080p', 59.50, 60),
    ('External SSD 1TB', 129.00, 25),
    ('Laptop Stand', 34.95, 80),
    ('Microphone Arm', 42.00, 15),
    ('Ring Light', 29.99, 50),
    ('Graphics Card RTX 4070', 599.99, 8),
    ('DDR5 RAM 32GB', 115.00, 40),
    ('CPU Cooler', 65.00, 35),
    ('Power Supply 750W', 110.00, 20),
    ('HDMI Cable 2.1', 15.99, 150),
    ('Vertical Mouse', 49.00, 30),
    ('Bluetooth Speaker', 75.00, 55),
    ('Gaming Chair', 249.00, 10),
    ('Desk Mat XL', 22.50, 100),
    ('Wireless Earbuds', 129.99, 65),
    ('Smart Watch', 199.00, 40),
    ('Tablet 10-inch', 299.00, 18),
    ('Smartphone Tripod', 19.99, 90),
    ('Ethernet Cable 10ft', 9.50, 200),
    ('Thunderbolt Dock', 180.00, 12),
    ('Portable Power Bank', 45.00, 75),
    ('Internal HDD 4TB', 85.00, 30),
    ('Gaming Controller', 55.00, 50),
    ('Capture Card', 140.00, 15),
    ('Wi-Fi Router 6', 150.00, 25),
    ('Motherboard Z790', 210.00, 14),
    ('Soundbar', 120.00, 22),
    ('Drawing Tablet', 79.99, 30),
    ('Thermal Paste', 7.99, 300),
    ('PC Case ATX', 95.00, 18),
    ('Green Screen', 60.00, 10),
    ('Monitor Mount', 45.00, 40),
    ('Trackball Mouse', 65.00, 20),
    ('VR Headset', 499.00, 5),
    ('Laser Printer', 180.00, 12),
    ('Paper Shredder', 55.00, 25),
    ('USB Flash Drive 128GB', 18.00, 120),
    ('SD Card 256GB', 35.00, 85),
    ('Blue Light Glasses', 15.00, 150),
    ('Cable Management Clips', 12.00, 500),
    ('Uninterruptible Power Supply', 160.00, 10),
    ('Fingerprint Scanner', 40.00, 45),
    ('Barcode Scanner', 70.00, 20),
    ('Projector 4K', 850.00, 4),
    ('Projector Screen', 110.00, 8),
    ('Smart Plug 4-Pack', 35.00, 60),
    ('Electric Standing Desk', 450.00, 7),
    ('Foot Rest', 28.00, 40),
    ('Cleaning Slime for Keyboard', 8.50, 250);
    





