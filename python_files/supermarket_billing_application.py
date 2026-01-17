import math

import mysql.connector


conn_obj = mysql.connector.connect(host="localhost", user="root", password="YOUR DATABASE PASSWORD", database="Billing_Application") # to connect with MySql
cur_obj = conn_obj.cursor() # to execute the sql queries, hit SQL

# To retrieve user data based on Phone Number from Customer Details Table
def data_retrieve(ph_no):
    query = f"select * from cust_details where c_ph_no = {ph_no}"
    result = None
    try:    
        cur_obj.execute(query) # To run the given query
        result = cur_obj.fetchone()  # limit 1 in SQL
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()  # it is used if the operation is failed then it will not reflect in your database
    return result


# To Create new user in the Customer Details table in Database
def customer_entry(cust_full_name, cust_address, cust_phone_num):
    query = f"insert into cust_details (c_full_name, c_address, c_ph_no) values (%s, %s, %s);"
    data = (cust_full_name, cust_address, cust_phone_num)

    try:
        cur_obj.execute(query,data)
        print("Custom Details Inserted")
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()


# To retrieve product details based on product ID from Product Details Table
def product_details_retrieve(pid):
    query = f"select * from p_details where pid = {pid}"
    result = None
    try:
        cur_obj.execute(query) # To run the given query
        result = cur_obj.fetchone()  # limit 1 in SQL
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()
    return result


# To update the Product Stock in Database
def update_stock(pid, p_quantity_new):
    query = f"update p_details set p_stock = {p_quantity_new} where pid = {pid}"

    try:
        cur_obj.execute(query)
        print("Product Details Updated")
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error updating data from MySQL:", e)
        conn_obj.rollback()

# To Entry new data in Analytics Table
def data_analysis_entry(cust_phone_num,calculated_amount, gst_price):
    cust_details = data_retrieve(cust_phone_num)
    query = f"insert into analytics_table (c_id, c_name, c_ph_no, total_bill_value, total_amount_payble_after_tax) values (%s,%s,%s,%s,%s);"
    values = (cust_details[0],cust_details[1],cust_details[3],calculated_amount,gst_price)
    try:
        cur_obj.execute(query,values) # To run the given query
        print("Analytics Table Data Inserted")
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()


# To retrieve Bill ID from Bill Details table
def bill_id_retrieve_Analytics_table():
    query = "select bill_id from analytics_table order by bill_id desc limit 1"
    bill_id = 0
    try:
        cur_obj.execute(query)
        bill_id = cur_obj.fetchone()
        conn_obj.commit()
    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()
    return bill_id


# To Entry new Bill Data in bill_details table
def bill_data_entry(cust_id, cust_name, p_id, p_quantity):
    bill_id_db = bill_id_retrieve_Analytics_table()
    print(bill_id_db)
    if bill_id_db is not None:
        new_bill_id = bill_id_db[0]+1
    else:
        new_bill_id = 1
    query = f"insert into billing_details (bill_id, cust_id, cust_name, p_id, p_quantity) values ({new_bill_id}, {cust_id}, \"{cust_name}\", {p_id}, {p_quantity});"

    try:
        cur_obj.execute(query)
        print("Bill Data Inserted Successfully ")
        conn_obj.commit()

    except mysql.connector.Error as e:
        print("Error retrieving data from MySQL:", e)
        conn_obj.rollback()


# For the Billing of the user
def billing_function(cust_phone_num):
    print("Starting the billing.")
    total_payable = 0.0
    count = 0
    stop_option = ""
    while True:
        if count>0:
            stop_option = input("Press 's'/'S' Enter to Stop Billing. Press Any Other Key to Continue. ======> ").lower()
            print("----------------------------------------------------------------------------------------------")
        if stop_option == "s":
            break
        else:
            count += 1
            pid = int(input("Enter the Product ID: "))
            print("----------------------------------------------------------------------------------------------")

            p_details = product_details_retrieve(pid)
            if p_details:
                p_price = p_details[2]
                p_name = p_details[1]
                p_stock_db = p_details[3]
                print(f"Product Name ===> {p_name} ")
                print("----------------------------------------------------------------------------------------------")

                print(f"Product Price ===>  {p_price} ")
                print("----------------------------------------------------------------------------------------------")

                print(f"Product Stock ===> {p_stock_db} ")
                print("----------------------------------------------------------------------------------------------")

                p_quantity = int(input("Enter the Product Quantity Customer Brought: "))
                print("----------------------------------------------------------------------------------------------")

                # in case product is not available we will not consider it
                if p_stock_db < p_quantity or p_stock_db==0:
                    print("Product is not available in Stock!")
                    print(
                        "----------------------------------------------------------------------------------------------")

                # otherwise continue calculating
                else:
                    total_price = float(p_price) * p_quantity
                    print("Total Price : ", total_price)
                    print(
                        "----------------------------------------------------------------------------------------------")

                    total_payable = total_payable + total_price
                    print(f"Total Calculated Amount: {total_payable}")
                    print(
                        "----------------------------------------------------------------------------------------------")

                    update_stock(pid, (p_stock_db-p_quantity))

                    # to find the customer details to pass into bill data entry method
                    c_details = data_retrieve(cust_phone_num)

                    # To entry bill data in bill details table
                    bill_data_entry(c_details[0], c_details[1], pid, p_quantity)


            else:
                print("No Product Details Found.")
                print("----------------------------------------------------------------------------------------------")

    gst_value = input("Enter the GST value if applicable: ")
    print("----------------------------------------------------------------------------------------------")

    if gst_value=="":
        gst_value = 0
    else:
        gst_value = float(gst_value)
    total_payable_after_gst = total_payable + total_payable * (gst_value / 100)
    math.ceil(total_payable_after_gst)
    print(f"Total Payable after {gst_value}% GST Tax:  {total_payable_after_gst}")
    print("----------------------------------------------------------------------------------------------")

    data_analysis_entry(cust_phone_num, total_payable, total_payable_after_gst)

    return float(total_payable)


# Main Entry Point
def main():
    cust_phone_num = input("Enter Customer Phone Number: ")
    existing_user = data_retrieve(cust_phone_num)
    total_payable = 0.0
    if existing_user:
        # For Existing user start billing
        print(f"Hi {existing_user[1]}, Welcome to Star Super Market!!")
        total_payable = billing_function(cust_phone_num)
    else:
        # Register User for Non Existing user
        print("To start billing we need to register your Mobile Number")
        cust_full_name = input("Enter Full Name: ")
        cust_address = input("Enter Address: ")
        customer_entry(cust_full_name, cust_address, cust_phone_num)
        total_payable = billing_function(cust_phone_num)


# Entry Point of the Code
main()

conn_obj.close()
