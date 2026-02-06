import streamlit as st
import pandas as pd
import billing_application_for_supermarket as backend
import pdf_generator
import time
import base64

st.set_page_config(page_title="Star Mart POS", layout="wide")

# ---------- UI HEADER ----------
st.markdown(
    "<h1 style='text-align:center;color:white;'>⭐ Star Mart POS Terminal</h1>",
    unsafe_allow_html=True
)

st.image("logo.png", width=120)

# ---------- BACKGROUND ----------
def add_bg(image):
    with open(image, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpg;base64,{encoded}");
            background-size: cover;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

add_bg("bg1.jpg")

# ---------- CLOUD QR NOTICE ----------
st.info("📷 QR scanning works only in local desktop mode (camera access disabled on cloud).")

# ---------- SESSION STATE ----------
if "cart" not in st.session_state: st.session_state.cart = []
if "customer" not in st.session_state: st.session_state.customer = None
if "total" not in st.session_state: st.session_state.total = 0.0

left, right = st.columns([1,2])

with left:
    st.subheader("👤 Customer")
    ph = st.text_input("Phone Number", max_chars=10)

    if st.button("Identify"):
        user = backend.data_retrieve(ph)
        st.session_state.customer = user if user else "NEW"

    if st.session_state.customer == "NEW":
        name = st.text_input("Name")
        addr = st.text_area("Address")
        if st.button("Register"):
            backend.customer_entry(name, addr, ph)
            time.sleep(1)
            st.session_state.customer = backend.data_retrieve(ph)
            st.rerun()

    if isinstance(st.session_state.customer, tuple):
        backend.check_conn()
        backend.cur_obj.execute("SELECT pid,p_name,p_price,p_stock FROM p_details")
        products = backend.cur_obj.fetchall()

        prod = st.selectbox("Select Item", products, format_func=lambda x: f"{x[1]} ₹{x[2]}")
        qty = st.number_input("Qty", 1, prod[3], 1)

        if st.button("Add"):
            st.session_state.cart.append({
                "PID": prod[0],
                "Item": prod[1],
                "Qty": qty,
                "Total": prod[2]*qty
            })
            st.session_state.total += prod[2]*qty
            backend.update_stock(prod[0], prod[3]-qty)
            st.rerun()

with right:
    if st.session_state.cart:
        df = pd.DataFrame(st.session_state.cart)
        st.dataframe(df, hide_index=True)

        gst = st.number_input("GST %", 0, 100, 18)
        subtotal = st.session_state.total
        total = subtotal + (subtotal*gst/100)

        st.metric("Subtotal", f"₹{subtotal:.2f}")
        st.metric("Grand Total", f"₹{total:.2f}")

        if st.button("Finalize & Print"):
            bill_id = backend.data_analysis_entry(ph, subtotal, total)
            for i in st.session_state.cart:
                backend.bill_data_entry(
                    bill_id,
                    st.session_state.customer[0],
                    i["PID"],
                    i["Qty"]
                )

            pdf = pdf_generator.generate_bill_pdf(bill_id)
            if pdf:
                st.success("Bill Generated")
                st.session_state.cart = []
                st.session_state.total = 0
                st.rerun()
