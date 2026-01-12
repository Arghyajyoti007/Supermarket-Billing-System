import mysql.connector


conn_obj = mysql.connector.connect(host="localhost", user="root", password="Arghya@123", database="Billing_Application") # to connect with MySql
cur_obj = conn_obj.cursor() # to execute the sql qeuries, hit SQL

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


# For the Billing of the user
def billing_function(customer_name):
    print("Starting the billing.")
    total_payble = 0
    count = 0
    stop_option = ""
    while True:
        if count>0:
            stop_option = input("Press 's' Enter to stop billing. Otherwise press any other key to continue.")

        if stop_option == "s":
            break
        else:
            count += 1
            pid = int(input("Enter the Product ID: "))
            p_details = product_details_retrieve(pid)
            if p_details:
                p_price = p_details[2]
                p_name = p_details[1]
                print(f"Product {p_name} has Price of  {p_price} ")
                p_quantiy = int(input("Enter the Product Quantity Customer Brought: "))
                total_price = p_price * p_quantiy
                print("Total Price : ", total_price)
                total_payble = total_payble + total_price
                print("Total Payable: ", total_payble)
            else:
                print("No Product Details Found")

    print(f"Hi {customer_name}! Your total bill amount : {total_payble}")


def main():
    cust_phone_num = input("Enter Customer Phone Number: ")
    existing_user = data_retrieve(cust_phone_num)

    if existing_user:
        # For Existing user start billing
        print(f"Hi {existing_user[1]}, Welcome to Star Super Market!!")
        billing_function(existing_user[1])
    else:
        # Register User for Non Existing user
        print("To start billing we need to register your Mobile Number")
        cust_full_name = input("Enter Full Name: ")
        cust_address = input("Enter Address: ")
        customer_entry(cust_full_name, cust_address, cust_phone_num)
        billing_function()

# Entry Point of the Code
main()

conn_obj.close()
