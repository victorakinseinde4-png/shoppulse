
import streamlit as st

st.set_page_config(
    page_title="ShopPulse",
    page_icon="📊",
    layout="centered"
)

st.title("📊 ShopPulse")
st.subheader("Smart Business Management")
st.write("Manage your products, sales and profits.")

st.divider()

st.header("💰 Sales & Profit Calculator")

product = st.text_input("Product name")

buying_price = st.number_input(
    "Buying price (₦)",
    min_value=0.0,
    step=100.0
)

selling_price = st.number_input(
    "Selling price (₦)",
    min_value=0.0,
    step=100.0
)

quantity = st.number_input(
    "Quantity sold",
    min_value=0,
    step=1
)

if st.button("Calculate Profit"):
    if not product.strip():
        st.error("Please enter a product name.")

    elif buying_price <= 0 or selling_price <= 0 or quantity <= 0:
        st.error("Enter valid prices and quantity.")

    else:
        revenue = selling_price * quantity
        cost = buying_price * quantity
        profit = revenue - cost

        st.success("Sales calculation complete!")

        st.metric("Total Revenue", f"₦{revenue:,.2f}")
        st.metric("Total Cost", f"₦{cost:,.2f}")
        st.metric("Total Profit", f"₦{profit:,.2f}")

        if profit < 0:
            st.warning("You made a loss on this sale.")

st.divider()

st.caption("ShopPulse © 2026 | Built for smarter businesses.")
