import math
import mysql.connector
import qr_scanner
import pdf_generator

# Establish connection with reconnection logic
conn_obj = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Your Password for Database",
    database="Billing_Application",
    consume_results=True # Helps prevent "Unread result" errors
)
cur_obj = conn_obj.cursor()

def check_conn():
    """Wakes up the database if it went to sleep."""
    if not conn_obj.is_connected():
        conn_obj.reconnect(attempts=3, delay=2)

def data_retrieve(ph_no):
    check_conn()
    # Using parameterized query to handle VARCHAR(10) safely
    query = "SELECT * FROM cust_details WHERE c_ph_no = %s"
    try:
        cur_obj.execute(query, (ph_no,))
        return cur_obj.fetchone()
    except mysql.connector.Error as e:
        print("Error retrieving data:", e)
        return None

def customer_entry(cust_full_name, cust_address, cust_phone_num):
    check_conn()
    query = "INSERT INTO cust_details (c_full_name, c_address, c_ph_no) VALUES (%s, %s, %s)"
    try:
        cur_obj.execute(query, (cust_full_name, cust_address, cust_phone_num))
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error inserting customer:", e)
        conn_obj.rollback()

def product_details_retrieve(pid):
    check_conn()
    query = "SELECT * FROM p_details WHERE pid = %s"
    try:
        cur_obj.execute(query, (pid,))
        return cur_obj.fetchone()
    except mysql.connector.Error as e:
        print("Error retrieving product:", e)
        return None

def update_stock(pid, p_quantity_new):
    check_conn()
    query = "UPDATE p_details SET p_stock = %s WHERE pid = %s"
    try:
        cur_obj.execute(query, (p_quantity_new, pid))
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error updating stock:", e)
        conn_obj.rollback()

def data_analysis_entry(cust_phone_num, calculated_amount, gst_price):
    check_conn()
    cust_details = data_retrieve(cust_phone_num)
    query = "INSERT INTO analytics_table (c_id, c_name, c_ph_no, total_bill_value, total_amount_payble_after_tax) VALUES (%s, %s, %s, %s, %s)"
    values = (cust_details[0], cust_details[1], cust_details[3], calculated_amount, gst_price)
    try:
        cur_obj.execute(query, values)
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error in analytics:", e)
        conn_obj.rollback()

def bill_id_retrieve_Analytics_table():
    check_conn()
    query = "SELECT bill_id FROM analytics_table ORDER BY bill_id DESC LIMIT 1"
    try:
        cur_obj.execute(query)
        return cur_obj.fetchone()
    except:
        return None

def bill_data_entry(cust_id, cust_name, p_id, p_quantity):
    check_conn()
    bill_id_db = bill_id_retrieve_Analytics_table()
    new_bill_id = bill_id_db[0] + 1 if bill_id_db else 1
    query = "INSERT INTO billing_details (bill_id, cust_id, cust_name, p_id, p_quantity) VALUES (%s, %s, %s, %s, %s)"
    try:
        cur_obj.execute(query, (new_bill_id, cust_id, cust_name, p_id, p_quantity))
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error in billing entry:", e)
        conn_obj.rollback()

# --- IMPORTANT CLI WRAPPER ---
def main():
    # Your original CLI logic remains here for testing
    cust_phone_num = input("Enter Customer Phone Number: ")
    # ... rest of your original main code ...

if __name__ == "__main__":
    try:
        main()
    finally:
        # Close connection ONLY when running this file directly
        cur_obj.close()
        conn_obj.close()
