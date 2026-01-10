import mysql.connector


conn_obj = mysql.connector.connect(host="localhost", user="root", password="ENTER YOUR PASSWORD", database="ENTER YOUR DATABASE NAME") # to connect with MySql
cur_obj = conn_obj.cursor() # to execute the sql qeuries, hit SQL

# To retrieve user data based on Phone Number
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


# To Create new user in the Database
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


# For the Billing of the user
def billing_function():
    pass


def main():
    print("Welcome to Star Supermarket")
    cust_phone_num = input("Enter Customer Phone Number: ")
    existing_user = data_retrieve(cust_phone_num)

    if existing_user:
        # For Existing user start billing
        print("Custom Details Exist. Starting the billing.")
        billing_function()
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
