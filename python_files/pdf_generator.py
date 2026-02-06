from fpdf import FPDF
import mysql.connector
from datetime import datetime


def generate_bill_pdf(bill_id):
    # Establish connection
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Arghya@123",
        database="Billing_Application"
    )
    cur = conn.cursor()

    # 1. Fetch Analytics Data (Header Info)
    cur.execute(
        "SELECT bill_id, c_name, c_ph_no, total_bill_value, total_amount_payble_after_tax, timestamp FROM analytics_table WHERE bill_id = %s",
        (bill_id,))
    analytics = cur.fetchone()

    # 2. Fetch Product Details (Line Items)
    # We join with p_details to get the actual product names and prices
    query = """
        SELECT p.p_name, p.p_price, b.p_quantity, (p.p_price * b.p_quantity) as total
        FROM billing_details b
        JOIN p_details p ON b.p_id = p.pid
        WHERE b.bill_id = %s
    """
    cur.execute(query, (bill_id,))
    items = cur.fetchall()

    if not analytics or not items:
        print("No billing data found to generate PDF.")
        return

    # --- PDF GENERATION ---
    pdf = FPDF()
    pdf.add_page()

    # Header
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, "STAR MART - PREMIUM BILL", ln=True, align='C')
    pdf.set_font("Arial", '', 12)
    pdf.cell(200, 10, f"Bill No: {analytics[0]} | Date: {analytics[5]}", ln=True, align='C')
    pdf.cell(200, 10, f"Customer: {analytics[1]} ({analytics[2]})", ln=True, align='C')
    pdf.ln(10)

    # Table Header
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(80, 10, "Description", 1)
    pdf.cell(30, 10, "Price", 1)
    pdf.cell(30, 10, "Qty", 1)
    pdf.cell(40, 10, "Total", 1)
    pdf.ln()

    # Table Rows
    pdf.set_font("Arial", '', 12)
    for row in items:
        pdf.cell(80, 10, str(row[0]), 1)
        pdf.cell(30, 10, str(row[1]), 1)
        pdf.cell(30, 10, str(row[2]), 1)
        pdf.cell(40, 10, str(row[3]), 1)
        pdf.ln()

    # Totals
    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(140, 10, "Subtotal", 0)
    pdf.cell(40, 10, f"Rs. {analytics[3]}", 0)
    pdf.ln()
    pdf.cell(140, 10, "Total (Inc. GST 18%)", 0)
    pdf.cell(40, 10, f"Rs. {analytics[4]}", 0)



    # Save PDF
    file_name = f"Bill_{bill_id}.pdf"
    pdf.output(file_name)
    cur.close()
    conn.close()
    return file_name
