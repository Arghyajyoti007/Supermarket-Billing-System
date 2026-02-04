<img width="500" height="500" alt="logo" src="https://github.com/user-attachments/assets/034b0bbd-702d-4f76-a2b5-29c2244cd37f" />

🛒 Supermarket Billing System (Python & MySQL)
==============================================

A robust, database-driven **Point of Sale (POS)** application that manages customer registration, real-time inventory tracking, and complex transactional analytics. This project demonstrates the integration of Python logic with a relational database to solve real-world retail challenges.

## 📺 Video Tutorials
Follow the step-by-step build on YouTube:
* **Full Series Playlist:** [Supermarket Billing System Playlist](https://www.youtube.com/playlist?list=PLsR48r3j5coUn0cu66ujQj1_e4d7OtLhJ)

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
    

### **Phase 3: Inventory Management & Analytics**

The most advanced update transforms the script into a professional multi-table relational system.

* **Relational Schema:** Expanded to 4 tables (`cust_details`, `p_details`, `analytics_table`, `billing_details`).
* **Stock Management:** Automatically decrements inventory in the `p_details` table upon purchase using the `update_stock()` function.
* **Data Integrity:** Implemented stock validation to prevent selling unavailable items, ensuring the system never records negative inventory.
* **Sales Analytics:** Separate logging of master transaction totals and granular itemized receipts for better business intelligence.
* **Tax Integration:** Dynamic GST calculation and mathematical rounding using the `math.ceil` library for professional financial accuracy.


### **Phase 4: Hardware Integration & Professional Reporting**

This phase bridges the gap between software and hardware by introducing Computer Vision and automated document generation.

#### 🚀 Phase 4 Highlights
We’ve moved beyond manual terminal entries. The system now supports:
* **Computer Vision:** Scan product QR codes using your webcam to fetch details instantly.
* **Automated Invoicing:** Professional PDF generation for every transaction.
* **Smart UI Logic:** Automatic "Open-on-Finish" PDF functionality for immediate printing.

#### 🛠️ Key Components & Documentation

**🔍 1. QR Code Scanner (OpenCV)**
Instead of typing Product IDs, the system uses **OpenCV** to detect and decode QR codes in real-time. 
* **Implementation:** Uses `cv2.QRCodeDetector()` to capture frames from the default webcam.
* **Use Case:** Faster checkout and zero human error during product selection.
* 👉 [**View QR Scanner Documentation & Logic**](python_files/QR-Scanning_readme.md)

**📄 2. PDF Invoice Generator (FPDF)**
A custom-built billing engine that pulls data from the `analytics_table` and `billing_details` using **SQL JOINS** to create a formatted Cash Memo.
* **Implementation:** Uses the `FPDF` library to generate a structured table including description, price, quantity, and total tax-inclusive amounts.
* **Use Case:** Provides customers with a downloadable, printable, and professional receipt.
* 👉 [**View PDF Generator Documentation & Logic**](python_files/Bill_generator_readme.md)

#### 🏗️ System Architecture (Updated)
1. **Hardware Layer:** Webcam captures QR Code using OpenCV.
2. **Logic Layer:** Python decodes ID → Fetches Price/Name from MySQL → Calculates Tax.
3. **Database Layer:** Updates inventory and logs transaction analytics.
4. **Output Layer:** FPDF generates `Bill_ID.pdf` and opens it automatically using the `subprocess` or `os` modules.

#### 📦 Prerequisites
To run Phase 4, ensure you have installed the following:
```bash
pip install opencv-python fpdf mysql-connector-python
```

🛠️ Tech Stack
------------------------

*   **Language:** Python 3.x
    
*   **Database:** MySQL (Relational Database Management)
    
*   **Computer Vision:** opencv-python (For real-time QR code detection and decoding)
    
*   **Document Generation:** fpdf (For creating structured, printable PDF invoices)
    
*   **Database Connectivity:** mysql-connector-python (For executing SQL queries and managing transactions)
    
*   **Core Utilities:** \* math: Used for financial rounding (math.ceil) and tax calculations.
    
    *   python-dotenv: For secure management of database credentials.
        
    *   os & subprocess: For cross-platform file handling and automated PDF launching.


    

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
