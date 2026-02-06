import math
import mysql.connector
import qr_scanner
import pdf_generator
import streamlit as st

# Establish connection with reconnection logic (Used while ran in local system)
# conn_obj = mysql.connector.connect(
#     host="localhost",
#     user="root",
#     password="Pasword",
#     database="Billing_Application",
#     consume_results=True # Helps prevent "Unread result" errors
# )
# cur_obj = conn_obj.cursor()

# --- INITIALIZE GLOBAL VARIABLES ---
conn_obj = None
cur_obj = None
# ----------------------------------

def check_conn():
    global conn_obj, cur_obj
    try:
        # Check if the connection exists and is still alive
        if conn_obj is None or not conn_obj.is_connected():
            conn_obj = mysql.connector.connect(
                host=st.secrets["mysql"]["host"],
                port=st.secrets["mysql"]["port"],
                user=st.secrets["mysql"]["user"],
                password=st.secrets["mysql"]["password"],
                database=st.secrets["mysql"]["database"]
            )
            cur_obj = conn_obj.cursor(buffered=True)
            # Optional: st.success("Connected to Cloud DB!") 
    except Exception as e:
        st.error(f"Database Connection Failed: {e}")



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
        # CRITICAL FIX: Get the ID of the row we JUST inserted
        return cur_obj.lastrowid
    except mysql.connector.Error as e:
        print("Error in analytics:", e)
        conn_obj.rollback()
        return None

def bill_id_retrieve_Analytics_table():
    check_conn()
    query = "SELECT bill_id FROM analytics_table ORDER BY bill_id DESC LIMIT 1"
    try:
        cur_obj.execute(query)
        return cur_obj.fetchone()
    except:
        return None

def bill_data_entry(bill_id, cust_id, cust_name, p_id, p_quantity):
    check_conn()
    # Now we pass the bill_id directly from the finalized analytics entry
    query = "INSERT INTO billing_details (bill_id, cust_id, cust_name, p_id, p_quantity) VALUES (%s, %s, %s, %s, %s)"
    try:
        cur_obj.execute(query, (bill_id, cust_id, cust_name, p_id, p_quantity))
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

def get_daily_sales_data():
    """Fetches hourly sales for the current day for the Streamlit chart."""
    check_conn()
    # This query groups sales by the hour to show the day's trend
    query = """
        SELECT HOUR(timestamp) as hour, SUM(total_amount_payble_after_tax) as sales 
        FROM analytics_table 
        WHERE DATE(timestamp) = CURDATE()
        GROUP BY HOUR(timestamp)
        ORDER BY hour
    """
    try:
        cur_obj.execute(query)
        result = cur_obj.fetchall()
        # Returns a list of tuples [(hour, sales), ...] or empty list
        return result if result else []
    except Exception as e:
        print(f"Database Chart Error: {e}")
        return []
