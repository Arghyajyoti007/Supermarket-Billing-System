import streamlit as st
import pandas as pd
import billing_application_for_supermarket as backend
import qr_scanner
import time
import base64
import pdf_generator

# --- THEME COLORS ---
TEAL_DARK = "#005461"
MINT_DARK = "#249E94"
MINT_LIGHT = "#3BC1A8"

st.set_page_config(page_title="Star Mart POS", layout="wide")


# Helper to trigger a browser pop-up for the PDF
# Replace your existing open_pdf_popup with this:
def open_pdf_popup(file_path):
    with open(file_path, "rb") as f:
        base64_pdf = base64.b64encode(f.read()).decode('utf-8')

    # Improved JavaScript: Creates a Blob URL which is secure and fast
    js = f"""
    <script>
    function openPDF() {{
        var base64 = "{base64_pdf}";
        var bin = atob(base64);
        var len = bin.length;
        var arr = new Uint8Array(len);
        for (var i = 0; i < len; i++) {{
            arr[i] = bin.charCodeAt(i);
        }}
        var blob = new Blob([arr], {{type: 'application/pdf'}});
        var url = URL.createObjectURL(blob);

        // Open in a new window/tab
        var win = window.open(url, '_blank');
        if (win) {{
            win.focus();
        }} else {{
            alert('Please allow pop-ups for this website to view the bill.');
        }}
    }}
    openPDF();
    </script>
    """
    st.components.v1.html(js, height=0)


def get_base64(bin_file):
    try:
        with open(bin_file, 'rb') as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return ""


# --- CSS STYLING ---
bin_str = get_base64('bg1.jpg')
logo_str = get_base64('logo.png')

bg_style = f'''
<style>
    .stApp {{
        background-image: linear-gradient(rgba(0, 84, 97, 0.85), rgba(0, 84, 97, 0.95)), url("data:image/png;base64,{bin_str}");
        background-size: cover; color: white;
    }}
    header[data-testid="stHeader"] {{ visibility: hidden; }}
    .sticky-header {{
        position: fixed; top: 0; left: 0; width: 100%; height: 80px;
        background-color: {TEAL_DARK}; display: flex; align-items: center;
        padding: 0 50px; z-index: 1000; border-bottom: 3px solid {MINT_LIGHT};
    }}
    .main-content-wrapper {{ margin-top: 100px; }}
    .stButton>button {{
        background-color: {MINT_DARK} !important; color: white !important;
        border: none !important; font-weight: bold; width: 100%;
    }}
    [data-testid="stMetricValue"] {{ color: {MINT_LIGHT} !important; }}
</style>
<div class="sticky-header">
    <img src="data:image/png;base64,{logo_str}" height="50" style="margin-right:20px;">
    <h1 style="color:white; margin:0; font-family:sans-serif; letter-spacing:2px;">STAR MART | PREMIUM POS</h1>
</div>
<div class="main-content-wrapper"></div>
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
    ph = st.text_input("Customer Phone", max_chars=10)

    if st.button("Identify Customer"):
        user = backend.data_retrieve(ph)
        if user:
            st.session_state.customer = user
            st.success(f"Welcome Back {user[1]}!")
        else:
            st.session_state.customer = "NEW"

    if st.session_state.customer == "NEW":
        st.warning("Customer not found!")
        with st.expander("📝 Register New Customer", expanded=True):
            name = st.text_input("Full Name")
            addr = st.text_area("Address")
            if st.button("Complete Registration"):
                backend.customer_entry(name, addr, ph)
                st.session_state.customer = backend.data_retrieve(ph)
                st.rerun()

    if isinstance(st.session_state.customer, tuple):
        st.divider()
        st.subheader("📦 Product Availability")
        backend.check_conn()
        backend.cur_obj.execute("SELECT pid, p_name, p_price, p_stock FROM p_details")
        all_products = backend.cur_obj.fetchall()
        prod_options = {f"{p[1]} (Stock: {p[3]})": p for p in all_products}

        selected_prod_name = st.selectbox("Search Product", options=["-- Select Item --"] + list(prod_options.keys()))

        if selected_prod_name != "-- Select Item --":
            prod_data = prod_options[selected_prod_name]
            if prod_data[3] <= 0:
                st.error("Out of Stock!")
            else:
                if st.button(f"Add {prod_data[1]}"):
                    st.session_state.active_item = prod_data

        if st.button("🔍 SCAN QR"):
            data = qr_scanner.qr_code_scanner()
            if data:
                pid = data.split("\t")[0]
                p = backend.product_details_retrieve(pid)
                if p: st.session_state.active_item = p

        if st.session_state.active_item:
            item = st.session_state.active_item
            with st.form("qty_form", clear_on_submit=True):
                qty = st.number_input("Quantity", 1, int(item[3]), 1)
                if st.form_submit_button("Add to Cart"):
                    cost = float(item[2]) * qty
                    st.session_state.cart.append(
                        {"PID": item[0], "Item": item[1], "Price": item[2], "Qty": qty, "Total": cost})
                    st.session_state.total += cost
                    backend.update_stock(item[0], item[3] - qty)
                    st.session_state.active_item = None
                    st.rerun()

with right:
    st.subheader("🛒 Current Bill")
    if st.session_state.cart:
        st.dataframe(pd.DataFrame(st.session_state.cart), use_container_width=True, hide_index=True)

        # --- NEW: GST INPUT AND CALCULATION ---
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
            # Use grand_total with the custom GST entered
            real_bill_id = backend.data_analysis_entry(st.session_state.customer[3], subtotal, grand_total)
            if real_bill_id:
                for item in st.session_state.cart:
                    backend.bill_data_entry(real_bill_id, st.session_state.customer[0], st.session_state.customer[1],
                                            item['PID'], item['Qty'])

                # Generate and Open Pop-up
                file_name = f"Bill_{real_bill_id}.pdf"
                pdf_generator.generate_bill_pdf(real_bill_id)
                open_pdf_popup(file_name)

                st.balloons()
                st.session_state.cart, st.session_state.total, st.session_state.customer = [], 0.0, None
                time.sleep(2)
                st.rerun()
    else:
        st.info("Identify customer to start billing.")
