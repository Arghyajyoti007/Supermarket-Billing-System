import streamlit as st
import pandas as pd
import billing_application_for_supermarket as backend
import pdf_generator
import web_qr_scanner
import time
import base64
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Star Mart POS", layout="wide")

# ---------------- UTILS ----------------
def load_image_base64(filename):
    current_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(current_dir, filename)
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode()

# ---------------- HEADER ----------------
st.markdown(
    "<h1 style='text-align:center;color:white;'>⭐ Star Mart POS Terminal</h1>",
    unsafe_allow_html=True
)

# -------- LOGO (FIXED: Base64, Cloud-safe) --------
try:
    logo_base64 = load_image_base64("logo.png")
    st.markdown(
        f"""
        <div style="text-align:center; margin-bottom: 10px;">
            <img src="data:image/png;base64,{logo_base64}" width="120">
        </div>
        """,
        unsafe_allow_html=True
    )
except Exception:
    st.warning("Logo not found. Continuing without logo.")

# ---------------- BACKGROUND (FIXED) ----------------
try:
    bg_base64 = load_image_base64("bg2.jpg")
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{bg_base64}");
            background-size: cover;
            background-position: center;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )
except Exception:
    st.warning("Background image not found.")

# ---------------- SESSION STATE ----------------
if "cart" not in st.session_state:
    st.session_state.cart = []
if "customer" not in st.session_state:
    st.session_state.customer = None
if "total" not in st.session_state:
    st.session_state.total = 0.0

left, right = st.columns([1, 2], gap="large")

# ================= LEFT PANEL =================
with left:
    st.subheader("👤 Customer")
    ph = st.text_input("Customer Phone Number", max_chars=10)

    if st.button("Identify Customer"):
        user = backend.data_retrieve(ph)
        st.session_state.customer = user if user else "NEW"

    if st.session_state.customer == "NEW":
        st.warning("Customer not found. Register below.")
        name = st.text_input("Full Name")
        addr = st.text_area("Address")
        if st.button("Register Customer"):
            backend.customer_entry(name, addr, ph)
            time.sleep(1)
            st.session_state.customer = backend.data_retrieve(ph)
            st.rerun()

    # ---------------- QR SCANNING (WEB ENABLED) ----------------
    if isinstance(st.session_state.customer, tuple):
        st.divider()
        st.subheader("📷 Scan Product QR (Web & Local)")

        qr_image = st.camera_input("Scan QR Code")

        scanned_pid = None
        if qr_image:
            qr_data = web_qr_scanner.decode_qr_from_image(qr_image.getvalue())
            if qr_data:
                st.success(f"QR Detected: {qr_data}")
                scanned_pid = qr_data
            else:
                st.error("No QR detected. Try again.")

        # ---------------- PRODUCT SELECTION ----------------
        backend.check_conn()
        backend.cur_obj.execute(
            "SELECT pid, p_name, p_price, p_stock FROM p_details"
        )
        products = backend.cur_obj.fetchall()

        product_map = {str(p[0]): p for p in products}

        selected_pid = scanned_pid or st.selectbox(
            "Select Product",
            options=["-- Select --"] + list(product_map.keys())
        )

        if selected_pid and selected_pid != "-- Select --":
            prod = product_map.get(str(selected_pid))
            if prod:
                if prod[3] <= 0:
                    st.error("Out of Stock")
                else:
                    qty = st.number_input(
                        "Quantity", 1, prod[3], 1
                    )
                    if st.button("Add to Cart"):
                        cost = float(prod[2]) * qty
                        st.session_state.cart.append({
                            "PID": prod[0],
                            "Item": prod[1],
                            "Price": float(prod[2]),
                            "Qty": qty,
                            "Total": cost
                        })
                        st.session_state.total += cost
                        backend.update_stock(prod[0], prod[3] - qty)
                        st.rerun()

# ================= RIGHT PANEL =================
with right:
    st.subheader("🛒 Current Bill")

    if st.session_state.cart:
        df = pd.DataFrame(st.session_state.cart)
        st.dataframe(df, hide_index=True)

        st.divider()
        gst = st.number_input("GST %", 0, 100, 18)

        subtotal = st.session_state.total
        gst_amt = (subtotal * gst) / 100
        grand_total = subtotal + gst_amt

        c1, c2, c3 = st.columns(3)
        c1.metric("Subtotal", f"₹{subtotal:.2f}")
        c2.metric("GST", f"₹{gst_amt:.2f}")
        c3.metric("Grand Total", f"₹{grand_total:.2f}")

        if st.button("🏁 Finalize & Print Bill"):
            bill_id = backend.data_analysis_entry(ph, subtotal, grand_total)

            for item in st.session_state.cart:
                backend.bill_data_entry(
                    bill_id,
                    st.session_state.customer[0],
                    st.session_state.customer[1],  # customer name
                    item["PID"],
                    item["Qty"]
                )

            pdf = pdf_generator.generate_bill_pdf(bill_id)
            if pdf:
                st.success("Invoice Generated Successfully")
                st.session_state.cart = []
                st.session_state.total = 0.0
                st.session_state.customer = None
                time.sleep(1)
                st.rerun()
    else:
        st.info("Cart is empty. Add products to continue.")

