🛒 Supermarket Billing System (Python & MySQL)
==============================================

A robust, database-driven **Point of Sale (POS)** application that manages customer registration, real-time inventory tracking, and complex transactional analytics. This project demonstrates the integration of Python logic with a relational database to solve real-world retail challenges.

🚀 Project Roadmap & Evolution
------------------------------

### **Phase 1: Foundation & Customer Auth**

The initial phase focused on the **Data Layer** and establishing a secure connection between Python and MySQL.

*   **Database Connectivity:** Established using mysql.connector with secure credential handling.
    
*   **Customer Verification:** Logic to check if a customer exists via phone number lookup.
    
*   **Dynamic Registration:** Workflow to register new customers without interrupting the sales flow.
    

### **Phase 2: Core Billing Engine**

The second phase introduced the "Engine" of the application, focusing on the math and product lookup logic.

*   **Product Retrieval:** Implementation of product\_details\_retrieve(pid) to fetch real-time pricing.
    
*   **Billing Loop:** A continuous while loop allowing cashiers to scan multiple items.
    
*   **Live Totals:** Real-time calculation of item prices and the overall running total.
    

### **Phase 3: Inventory Management & Analytics (Current)**

The most advanced update transforms the script into a professional multi-table relational system.

*   **Relational Schema:** Expanded to 4 tables (cust\_details, p\_details, analytics\_table, billing\_details).
    
*   **Stock Management:** Automatically decrements inventory in the p\_details table upon purchase.
    
*   **Data Integrity:** Implemented stock validation to prevent selling unavailable items.
    
*   **Sales Analytics:** Separate logging of master transaction totals and granular itemized receipts.
    
*   **Tax Integration:** Dynamic GST calculation and mathematical rounding using the math library.
    

🛠️ Tech Stack
--------------

*   **Language:** Python 3.x
    
*   **Database:** MySQL
    
*   **Core Libraries:** mysql.connector, math, python-dotenv
    

📊 Database Architecture
------------------------
```

-- Main tables used in this project:
1. cust_details    -- User profiles and contact info.
2. p_details       -- Inventory, prices, and stock levels.
3. analytics_table -- Master bill records (ID, Total, Tax, Timestamp).
4. billing_details -- Granular list of every item per bill.

```

🔮 Future Improvement Plans
---------------------------

*   **GUI Development:** Transitioning from the Command Line Interface (CLI) to a modern Desktop App using **Tkinter** or **PyQt**.
    
*   **Invoice Generation:** Automatically generating and saving **PDF receipts** for customers.
    
*   **Sales Dashboard:** Visualizing sales trends using libraries like **Matplotlib** or **Seaborn**.
    
*   **Barcode Scanning:** Integrating hardware support for physical barcode scanners.
    
*   **Admin Panel:** A secure login for managers to update product prices and stock levels directly.
    

🤝 Connect with Me
------------------

Developed by **Arghyajyoti**. Feel free to reach out for collaboration!

*   **GitHub:** [Arghyajyoti007](https://www.google.com/search?q=https://github.com/Arghyajyoti007)
    
*   **LinkedIn:** [Arghyajyoti Samui](https://www.linkedin.com/in/arghyajyoti-samui/)
    
*   **Twitter/X:** [@Im\_Arghya\_](https://www.google.com/search?q=https://x.com/Im_Arghya_)
    
*   **Instagram:** [@jyoti.arghya](https://www.instagram.com/jyoti.arghya)
