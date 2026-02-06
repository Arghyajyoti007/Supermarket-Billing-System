from fpdf import FPDF
import mysql.connector
import streamlit as st

def generate_bill_pdf(bill_id):
    try:
        # 1. Establish Cloud Connection
        conn = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            port=int(st.secrets["mysql"]["port"]),
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"]
        )
        cur = conn.cursor()

        # 2. Fetch Header Info from analytics_table
        # Columns based on your schema: bill_id, c_ph_no, total_bill_value, total_amount_payble_after_tax, timestamp
        cur.execute(
            "SELECT bill_id, c_ph_no, total_bill_value, total_amount_payble_after_tax, timestamp FROM analytics_table WHERE bill_id = %s",
            (bill_id,)
        )
        analytics = cur.fetchone()

        if not analytics:
            return None

        # 3. Fetch Line Items from billing_details joined with p_details
        # Joins on p_id = pid as per your schema
        query = """
            SELECT p.p_name, p.p_price, b.p_quantity, (p.p_price * b.p_quantity) as total
            FROM billing_details b
            JOIN p_details p ON b.p_id = p.pid
            WHERE b.bill_id = %s
        """
        cur.execute(query, (bill_id,))
        items = cur.fetchall()

        # --- PDF CONSTRUCTION ---
        pdf = FPDF()
        pdf.add_page()
        
        # Title
        pdf.set_font("Arial", 'B', 20)
        pdf.set_text_color(0, 84, 97) 
        pdf.cell(200, 15, "STAR MART", ln=True, align='C')
        
        pdf.set_font("Arial", 'B', 12)
        pdf.set_text_color(0, 0, 0)
        pdf.cell(200, 8, "OFFICIAL INVOICE", ln=True, align='C')
        pdf.ln(5)

        # Bill Metadata
        pdf.set_font("Arial", '', 10)
        pdf.cell(100, 7, f"Bill No: {analytics[0]}", 0)
        pdf.cell(100, 7, f"Date: {analytics[4]}", 0, 1, 'R')
        pdf.cell(100, 7, f"Phone: {analytics[1]}", 0, 1, 'L')
        pdf.ln(5)

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
        pdf.ln(15)
        pdf.set_font("Arial", 'I', 9)
        pdf.cell(200, 10, "Generated electronically. Thank you!", 0, 0, 'C')

        # Save and Close
        file_name = f"Bill_{bill_id}.pdf"
        pdf.output(file_name)
        
        cur.close()
        conn.close()
        return file_name

    except Exception as e:
        st.error(f"PDF Error: {str(e)}")
        return None
