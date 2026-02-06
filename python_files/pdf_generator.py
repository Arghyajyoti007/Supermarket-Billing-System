from fpdf import FPDF
import mysql.connector
import streamlit as st

def generate_bill_pdf(bill_id):
    # Establish cloud connection using Streamlit Secrets
    try:
        conn = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            port=int(st.secrets["mysql"]["port"]),
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"]
        )
        cur = conn.cursor()

        # 1. Fetch Analytics Data (Header Info)
        cur.execute(
            "SELECT bill_id, c_ph_no, total_bill_value, total_amount_payble_after_tax, timestamp FROM analytics_table WHERE bill_id = %s",
            (bill_id,)
        )
        analytics = cur.fetchone()

        if not analytics:
            cur.close()
            conn.close()
            return None

        # Fetch Customer Name separately
        cur.execute("SELECT c_full_name FROM cust_details WHERE c_ph_no = %s", (analytics[1],))
        cust_name = cur.fetchone()
        customer_display_name = cust_name[0] if cust_name else "Valued Customer"

        # -----------------------------------
        # 2. Fetch Product Details
        # CHANGED FROM 'bill_data' TO 'billing_details' TO MATCH YOUR SCHEMA
        query = """
            SELECT p.p_name, p.p_price, b.p_quantity, (p.p_price * b.p_quantity) as total
            FROM billing_details b
            JOIN p_details p ON b.p_id = p.pid
            WHERE b.bill_id = %s
        """
        cur.execute(query, (bill_id,))
        items = cur.fetchall()
        # -------------------------------------

        if not items:
            cur.close()
            conn.close()
            return None

        # --- PDF GENERATION ---
        pdf = FPDF()
        pdf.add_page()

        # Header Section
        pdf.set_font("Arial", 'B', 20)
        pdf.set_text_color(0, 84, 97) 
        pdf.cell(200, 15, "STAR MART", ln=True, align='C')
        
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(200, 8, "PREMIUM INVOICE", ln=True, align='C')
        pdf.ln(5)

        # Invoice Metadata
        pdf.set_font("Arial", '', 10)
        pdf.cell(100, 7, f"Bill No: {analytics[0]}", 0)
        pdf.cell(100, 7, f"Date: {analytics[4]}", 0, 1, 'R')
        pdf.cell(100, 7, f"Customer: {customer_display_name}", 0)
        pdf.cell(100, 7, f"Phone: {analytics[1]}", 0, 1, 'R')
        pdf.ln(10)

        # Table Header
        pdf.set_fill_color(36, 158, 148) 
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(80, 10, " Description", 1, 0, 'L', True)
        pdf.cell(30, 10, "Price", 1, 0, 'C', True)
        pdf.cell(30, 10, "Qty", 1, 0, 'C', True)
        pdf.cell(40, 10, "Total", 1, 1, 'C', True)

        # Table Rows
        pdf.set_text_color(0, 0, 0)
        pdf.set_font("Arial", '', 11)
        for row in items:
            pdf.cell(80, 10, f" {str(row[0])}", 1)
            pdf.cell(30, 10, f"{float(row[1]):.2f}", 1, 0, 'C')
            pdf.cell(30, 10, str(row[2]), 1, 0, 'C')
            pdf.cell(40, 10, f"{float(row[3]):.2f}", 1, 1, 'C')

        # Totals Section
        pdf.ln(5)
        pdf.set_font("Arial", 'B', 11)
        pdf.cell(140, 10, "Subtotal", 0, 0, 'R')
        pdf.cell(40, 10, f"Rs. {float(analytics[2]):.2f}", 1, 1, 'C')
        
        pdf.set_fill_color(240, 240, 240)
        pdf.cell(140, 10, "Grand Total (Inc. GST)", 0, 0, 'R')
        pdf.cell(40, 10, f"Rs. {float(analytics[3]):.2f}", 1, 1, 'C', True)

        # Footer
        pdf.ln(20)
        pdf.set_font("Arial", 'I', 10)
        pdf.cell(200, 10, "Thank you for shopping at Star Mart!", 0, 0, 'C')

        # Save PDF
        file_name = f"Bill_{bill_id}.pdf"
        pdf.output(file_name)
        
        cur.close()
        conn.close()
        return file_name

    except Exception as e:
        st.error(f"PDF Generation Error: {e}")
        return None
