import streamlit as st
import pandas as pd
import billing_application_for_supermarket as backend
import pdf_generator
import time
import base64

# --- THEME COLORS ---
TEAL_DARK = "#005461"
MINT_DARK = "#249E94"
MINT_LIGHT = "#3BC1A8"

st.set_page_config(page_title="Star Mart POS", layout="wide")

# Helper to trigger a browser pop-up for the PDF
def open_pdf_popup(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    js = f"""
    <script>
        var base64 = "{base64_pdf}";
        var bin = atob(base64);
        var len = bin.length;
        var arr = new Uint8Array(len);
        for (var i = 0; i < len; i++) {{
            arr[i] = bin.charCodeAt(i);
        }}
        var blob = new Blob([arr], {{type: 'application/pdf'}});
        var url = URL.createObjectURL(blob);
        var win = window.open(url, '_blank');
        if (win) {{
            win.focus();
        }} else {{
            alert('Please allow pop-ups for this website to view the bill.');
        }}
    </script>
    """
    st.components.v1.html(js, height=0)

# --- CSS STYLING ---
# Note: Ensure bg1.jpg and logo.png exist in your repo
bg_style = f'''
<style>
    .stApp {{
        background-color: {TEAL_DARK};
        color: white;
    }}
    .stButton>button {{
        background-color: {MINT_DARK} !important; color: white !important;
        border: none !important; font-weight: bold; width: 100%;
    }}
    [data-testid="stMetricValue"] {{ color: {MINT_LIGHT} !important; }}
</style>
'''
st.markdown(bg_style, unsafe_allow_html=True)

# --- SESSION STATE ---
if 'cart' not in st.session_state: st.session_state.cart = []
if 'customer' not in st.session_state: st.session_state.customer = None
if 'total' not in st.session_state: st.session_state.total = 0.0
if 'active_item' not in st.session_state: st.session_state.active_item = None

left, right = st.columns([1, 2], gap="large")

with left:
    st.subheader("👤 Customer Session")
    ph = st.text_input("Customer Phone", max_chars=10, key="cust_ph")

    if st.button("Identify Customer"):
        if len(ph) == 10:
            user = backend.data_retrieve(ph)
            if user:
                st.session_state.customer = user
                st.success(f"Welcome Back {user[1]}!")
            else:
                st.session_state.customer = "NEW"
        else:
            st.error("Enter a valid 10-digit number")

    # REGISTRATION LOGIC
    if st.session_state.customer == "NEW":
        st.warning("Customer not found!")
        with st.expander("📝 Register New Customer", expanded=True):
            new_name = st.text_input("Full Name", key="reg_name")
            new_addr = st.text_area("Address", key="reg_addr")
            if st.button("Complete Registration"):
                if new_name and new_addr:
                    success = backend.customer_entry(new_name, new_addr, ph)
                    if success:
                        time.sleep(1) # Sync time for Aiven
                        user = backend.data_retrieve(ph)
                        if user:
                            st.session_state.customer = user
                            st.rerun()
                else:
                    st.error("Please fill all details")

    # PRODUCT SECTION
    if isinstance(st.session_state.customer, tuple):
        st.divider()
        st.write(f"**Billing for:** {st.session_state.customer[1]}")
        
        backend.check_conn()
        backend.cur_obj.execute("SELECT pid, p_name, p_price, p_stock FROM p_details")
        all_products = backend.cur_obj.fetchall()
        prod_options = {f"{p[1]} (₹{p[2]})": p for p in all_products}

        selected_prod_name = st.selectbox("Search Product", options=["-- Select Item --"] + list(prod_options.keys()))

        if selected_prod_name != "-- Select Item --":
            prod_data = prod_options[selected_prod_name]
            if prod_data[3] <= 0:
                st.error("Out of Stock!")
            else:
                if st.button(f"Add {prod_data[1]}"):
                    st.session_state.active_item = prod_data

        if st.session_state.active_item:
            item = st.session_state.active_item
            with st.form("qty_form", clear_on_submit=True):
                st.write(f"Selected: **{item[1]}**")
                qty = st.number_input("Quantity", 1, int(item[3]), 1)
                if st.form_submit_button("Confirm Add"):
                    cost = float(item[2]) * qty
                    st.session_state.cart.append(
                        {"PID": item[0], "Item": item[1], "Price": float(item[2]), "Qty": qty, "Total": cost})
                    st.session_state.total += cost
                    backend.update_stock(item[0], item[3] - qty)
                    st.session_state.active_item = None
                    st.rerun()

with right:
    st.subheader("🛒 Current Bill")
    if st.session_state.cart:
        df = pd.DataFrame(st.session_state.cart)
        # 2026 Compliant: width='stretch' replaces use_container_width
        st.dataframe(df, width='stretch', hide_index=True)

        st.divider()
        gst_percent = st.number_input("Enter GST %", min_value=0, max_value=100, value=18)

        subtotal = st.session_state.total
        gst_amount = (subtotal * gst_percent) / 100
        grand_total = subtotal + gst_amount

        c1, c2, c3 = st.columns(3)
        c1.metric("Subtotal", f"₹{subtotal:,.2f}")
        c2.metric(f"GST ({gst_percent}%)", f"₹{gst_amount:,.2f}")
        c3.metric("Grand Total", f"₹{grand_total:,.2f}")

        if st.button("🏁 FINALIZE & PRINT"):
            # 1. Update Analytics Table (Using ph from text_input)
            real_bill_id = backend.data_analysis_entry(ph, subtotal, grand_total)
            
            if real_bill_id:
                # 2. Update Billing Details
                for item in st.session_state.cart:
                    backend.bill_data_entry(real_bill_id, item['PID'], item['Qty'])

                # 3. Generate PDF
                generated_file = pdf_generator.generate_bill_pdf(real_bill_id)
                
                if generated_file:
                    st.balloons()
                    open_pdf_popup(generated_file)
                    
                    # 4. Reset State
                    st.session_state.cart = []
                    st.session_state.total = 0.0
                    st.session_state.customer = None
                    time.sleep(2)
                    st.rerun()
                else:
                    st.error("PDF generation failed. Check pdf_generator.py logic.")
    else:
        st.info("The cart is empty. Identify a customer to begin.")
