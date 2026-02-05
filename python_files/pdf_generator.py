from fpdf import FPDF
import mysql.connector
import os
import sys
import subprocess

# Establish MySQL database connection
conn_obj = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Arghya@123",
    database="Billing_Application"
)

# Cursor object to execute SQL queries
cur_obj = conn_obj.cursor()


# ---------------- BILL PDF GENERATION FUNCTION ----------------
def generate_bill_pdf(cust_phone_num):
    # Fetch latest bill summary for the given customer phone number
    query = """
        SELECT bill_id, c_name, c_ph_no,
               total_bill_value,
               total_amount_payble_after_tax,
               timestamp
        FROM analytics_table
        WHERE c_ph_no = %s
        ORDER BY bill_id DESC
        LIMIT 1
    """
    cur_obj.execute(query, (cust_phone_num,))
    bill_summary = cur_obj.fetchone()

    # If no bill data exists, exit function
    if not bill_summary:
        print("No billing data found to generate PDF.")
        return

    # Unpack bill summary data
    bill_id, cust_name, ph_no, total_amt, final_amt, bill_date = bill_summary

    # Fetch item-wise purchase details for the bill
    query = """
        SELECT p.p_name, p.p_price, b.p_quantity
        FROM billing_details b
        JOIN p_details p ON b.p_id = p.pid
        WHERE b.bill_id = %s
    """
    cur_obj.execute(query, (bill_id,))
    items = cur_obj.fetchall()

    # ---------------- PDF CREATION ----------------
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Supermarket title
    pdf.set_font("Arial", "B", 20)
    pdf.cell(0, 10, "STAR MART", ln=True, align="C")

    # Cash memo heading
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "CASH MEMO", ln=True, align="C")


    # Bill metadata
    pdf.ln(5)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, f"Bill No: {bill_id}", ln=True)
    pdf.cell(0, 8, f"Date: {bill_date.strftime('%d-%m-%Y %H:%M')}", ln=True)


    # Customer details
    pdf.ln(5)
    pdf.cell(0, 8, f"Customer Name: {cust_name}", ln=True)
    pdf.cell(0, 8, f"Phone Number: {ph_no}", ln=True)

    pdf.ln(8)

    # ---------------- TABLE HEADER ----------------
    pdf.set_font("Arial", "B", 10)
    pdf.cell(80, 8, "Description", border=1)
    pdf.cell(30, 8, "Price", border=1)
    pdf.cell(30, 8, "Quantity", border=1)
    pdf.cell(40, 8, "Amount", border=1, ln=True)

    # ---------------- TABLE ROWS ----------------
    pdf.set_font("Arial", size=10)
    for name, price, qty in items:
        amount = float(price) * qty

        pdf.cell(80, 8, name, border=1)
        pdf.cell(30, 8, f"{price}", border=1)
        pdf.cell(30, 8, str(qty), border=1)
        pdf.cell(40, 8, f"{amount:.2f}", border=1, ln=True)

    pdf.ln(5)

    # ---------------- TOTALS ----------------
    pdf.cell(140, 8, "Total", border=1)
    pdf.cell(40, 8, f"{total_amt:.2f}", border=1, ln=True)

    pdf.cell(140, 8, "Total Payable (After GST)", border=1)
    pdf.cell(40, 8, f"{final_amt:.2f}", border=1, ln=True)

    # Footer message
    pdf.ln(10)
    pdf.cell(0, 8, "Thank you for shopping with us!", ln=True, align="C")

    # ---------------- SAVE PDF ----------------
    file_name = f"Bill_{bill_id}.pdf"
    pdf.output(file_name)
    print(f"PDF generated successfully: {file_name}")

    # ---------------- AUTO-OPEN PDF ----------------
    try:
        if sys.platform.startswith("win"):
            os.startfile(file_name)       # Windows
        elif sys.platform.startswith("darwin"):
            subprocess.call(["open", file_name])  # macOS
        else:
            subprocess.call(["xdg-open", file_name])  # Linux
    except Exception as e:
        print("PDF generated but could not be auto-opened:", e)
