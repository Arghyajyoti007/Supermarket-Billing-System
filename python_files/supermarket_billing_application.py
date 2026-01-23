from fpdf import FPDF
from datetime import datetime

def generate_bill_pdf(cust_phone_num):
    # Fetch latest bill ID for this customer
    query = """
        SELECT bill_id, c_name, c_ph_no, total_bill_value, total_amount_payble_after_tax, timestamp
        FROM analytics_table
        WHERE c_ph_no = %s
        ORDER BY bill_id DESC
        LIMIT 1
    """
    cur_obj.execute(query, (cust_phone_num,))
    bill_summary = cur_obj.fetchone()

    if not bill_summary:
        print("No billing data found to generate PDF.")
        return

    bill_id, cust_name, ph_no, total_amt, final_amt, bill_date = bill_summary

    # Fetch item-wise details
    query = """
        SELECT p.p_name, p.p_price, b.p_quantity
        FROM billing_details b
        JOIN p_details p ON b.p_id = p.pid
        WHERE b.bill_id = %s
    """
    cur_obj.execute(query, (bill_id,))
    items = cur_obj.fetchall()

    # ---------------- PDF Creation ----------------
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()

    # Header
    pdf.set_font("Arial", "B", 16)
    pdf.cell(0, 10, "CASH MEMO", ln=True, align="C")

    pdf.ln(5)
    pdf.set_font("Arial", size=10)
    pdf.cell(0, 8, f"Bill No: {bill_id}", ln=True)
    pdf.cell(0, 8, f"Date: {bill_date.strftime('%d-%m-%Y %H:%M')}", ln=True)

    pdf.ln(5)
    pdf.cell(0, 8, f"Customer Name: {cust_name}", ln=True)
    pdf.cell(0, 8, f"Phone Number: {ph_no}", ln=True)

    pdf.ln(8)

    # Table Header
    pdf.set_font("Arial", "B", 10)
    pdf.cell(80, 8, "Description", border=1)
    pdf.cell(30, 8, "Price", border=1)
    pdf.cell(30, 8, "Quantity", border=1)
    pdf.cell(40, 8, "Amount", border=1, ln=True)

    # Table Rows
    pdf.set_font("Arial", size=10)
    for item in items:
        name, price, qty = item
        amount = float(price) * qty

        pdf.cell(80, 8, name, border=1)
        pdf.cell(30, 8, f"{price}", border=1)
        pdf.cell(30, 8, str(qty), border=1)
        pdf.cell(40, 8, f"{amount:.2f}", border=1, ln=True)

    pdf.ln(5)

    # Totals
    pdf.cell(140, 8, "Total", border=1)
    pdf.cell(40, 8, f"{total_amt:.2f}", border=1, ln=True)

    pdf.cell(140, 8, "Total Payable (After GST)", border=1)
    pdf.cell(40, 8, f"{final_amt:.2f}", border=1, ln=True)

    pdf.ln(10)
    pdf.cell(0, 8, "Thank you for shopping with us!", ln=True, align="C")

    # Save PDF
    file_name = f"Bill_{bill_id}.pdf"
    pdf.output(file_name)

    print(f"PDF generated successfully: {file_name}")
