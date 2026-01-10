# Super-Billing-Core: Customer & Database Management System

<img width="1024" height="819" alt="Gemini_Generated_Image_ai6n45ai6n45ai6n" src="https://github.com/user-attachments/assets/532335ac-c5ed-40d9-859f-56126a28706f" />

A robust, lightweight desktop application designed to streamline the checkout process and inventory management for retail environments. This application provides a seamless interface for cashiers to process transactions, manage stock levels, and generate digital invoices.


### **🔄 System Workflow: Customer Authentication**

The application follows a linear validation path to ensure every transaction is linked to a customer profile.

#### **1\. Initiation & Input**

*   The program starts at the main() function.
    
*   The user (cashier) is prompted to enter the **Customer Phone Number**. This acts as the Unique Identifier (Primary Key) for the session.
    

#### **2\. Data Retrieval (Verification)**

*   The data\_retrieve() function triggers a SELECT query to the cust\_details table in the MySQL database.
    
*   **Database Logic:**
    
    *   If a record matches the phone number, it returns the user data.
        
    *   If no record is found, it returns None.
        

#### **3\. Conditional Branching**

*   **Existing User:** If data is found, the system skips registration and proceeds directly to the billing\_function().
    
*   **New User:** If no data is found, the system triggers a registration flow:
    
    *   Prompts for **Full Name** and **Address**.
        
    *   Calls customer\_entry() to perform an INSERT operation into the MySQL table.
        
    *   Uses conn\_obj.commit() to save the new record permanently.
        

#### **4\. Billing Transition**

*   Regardless of whether the user was pre-existing or just registered, the flow culminates in the billing\_function(), where the actual product scanning and total calculation will occur.
    

#### **5\. Exception Handling & Security**

*   **Transaction Integrity:** Every database call is wrapped in a try-except block.
    
*   **Rollback Mechanism:** If a database error occurs (e.g., connection loss or invalid data), conn\_obj.rollback() is called to prevent partial or corrupted data from being saved.
