
import streamlit as st
import json
import os
from datetime import datetime

st.set_page_config(
    page_title="ShopPulse",
    page_icon="📊",
    layout="wide"
)

DATA_FILE = "shoppulse_data.json"


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as file:
                data = json.load(file)
                return data.get("products", {}), data.get("sales", [])
        except (json.JSONDecodeError, OSError):
            pass
    return {}, []


def save_data():
    with open(DATA_FILE, "w") as file:
        json.dump({
            "products": st.session_state.products,
            "sales": st.session_state.sales
        }, file, indent=4)


if "products" not in st.session_state:
    products, sales = load_data()
    st.session_state.products = products
    st.session_state.sales = sales


st.title("📊 ShopPulse")
st.subheader("Smart Business Management")
st.write("Manage your products, stock, sales and profits.")

st.divider()

menu = st.sidebar.radio(
    "MAIN MENU",
    [
        "Dashboard",
        "Add Product",
        "Inventory",
        "Record Sale",
        "Restock",
        "Sales History"
    ]
)

products = st.session_state.products
sales = st.session_state.sales


if menu == "Dashboard":
    st.header("Business Overview")

    revenue = sum(s["revenue"] for s in sales)
    profit = sum(s["profit"] for s in sales)
    stock_count = sum(p["stock"] for p in products.values())

    a, b, c, d = st.columns(4)

    a.metric("Total Products", len(products))
    b.metric("Items in Stock", stock_count)
    c.metric("Total Revenue", f"₦{revenue:,.2f}")
    d.metric("Total Profit", f"₦{profit:,.2f}")

    st.divider()
    st.subheader("Recent Sales")

    if sales:
        for sale in reversed(sales[-5:]):
            st.write(
                f"**{sale['product']}** — "
                f"{sale['quantity']} sold — "
                f"₦{sale['revenue']:,.2f} revenue"
            )
    else:
        st.info("No sales recorded yet.")


elif menu == "Add Product":
    st.header("Add a New Product")

    with st.form("add_product"):
        name = st.text_input("Product name")
        buying = st.number_input(
            "Buying price (₦)", min_value=0.0
        )
        selling = st.number_input(
            "Selling price (₦)", min_value=0.0
        )
        quantity = st.number_input(
            "Opening stock", min_value=0, step=1
        )

        submitted = st.form_submit_button("Save Product")

        if submitted:
            key = name.strip().lower()

            if not key:
                st.error("Enter a product name.")
            elif buying <= 0 or selling <= 0:
                st.error("Enter valid prices.")
            elif quantity <= 0:
                st.error("Opening stock must be greater than zero.")
            elif key in products:
                st.error("This product already exists.")
            else:
                products[key] = {
                    "name": name.strip(),
                    "buying_price": buying,
                    "selling_price": selling,
                    "stock": quantity
                }
                save_data()
                st.success("Product added successfully!")


elif menu == "Inventory":
    st.header("Product Inventory")

    if products:
        for key, p in products.items():
            st.write(
                f"**{p['name']}** | "
                f"Buying: ₦{p['buying_price']:,.2f} | "
                f"Selling: ₦{p['selling_price']:,.2f} | "
                f"Stock: {p['stock']}"
            )
    else:
        st.info("No products yet. Add your first product.")


elif menu == "Record Sale":
    st.header("Record a Sale")

    if products:
        with st.form("record_sale"):
            selected = st.selectbox(
                "Select product",
                list(products.keys()),
                format_func=lambda x: products[x]["name"]
            )

            quantity = st.number_input(
                "Quantity sold", min_value=1, step=1
            )

            submitted = st.form_submit_button("Complete Sale")

            if submitted:
                p = products[selected]

                if quantity > p["stock"]:
                    st.error("Not enough stock available.")
                else:
                    revenue = p["selling_price"] * quantity
                    cost = p["buying_price"] * quantity
                    profit = revenue - cost

                    p["stock"] -= quantity

                    sales.append({
                        "product": p["name"],
                        "quantity": quantity,
                        "revenue": revenue,
                        "profit": profit,
                        "date": datetime.now().strftime(
                            "%Y-%m-%d %H:%M:%S"
                        )
                    })

                    save_data()

                    st.success("Sale recorded successfully!")
                    st.metric("Revenue", f"₦{revenue:,.2f}")
                    st.metric("Profit", f"₦{profit:,.2f}")
    else:
        st.info("Add a product before recording a sale.")


elif menu == "Restock":
    st.header("Restock Products")

    if products:
        with st.form("restock"):
            selected = st.selectbox(
                "Select product",
                list(products.keys()),
                format_func=lambda x: products[x]["name"]
            )

            quantity = st.number_input(
                "Quantity to add", min_value=1, step=1
            )

            submitted = st.form_submit_button("Update Stock")

            if submitted:
                products[selected]["stock"] += quantity
                save_data()
                st.success("Stock updated successfully!")
    else:
        st.info("No products available to restock.")


elif menu == "Sales History":
    st.header("Sales History")

    if sales:
        for sale in reversed(sales):
            st.write(
                f"**{sale['product']}** | "
                f"Quantity: {sale['quantity']} | "
                f"Revenue: ₦{sale['revenue']:,.2f} | "
                f"Profit: ₦{sale['profit']:,.2f} | "
                f"{sale['date']}"
            )
    else:
        st.info("No sales have been recorded yet.")


st.divider()
st.caption("ShopPulse © 2026 | Built for smarter businesses.")
