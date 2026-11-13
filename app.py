import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import date
from database import initialize_database
from expense_service import add_transaction, get_transactions, update_transaction, delete_transaction, get_summary, get_monthly_summary
from analytics import prepare_category_data

st.set_page_config(page_title="Personal Expense Tracker", page_icon="💰", layout="wide")
initialize_database()
st.title("💰 Personal Expense Tracker")
st.caption("Track your income, expenses, and monthly spending in one place.")

transactions = get_transactions()
summary = get_summary()
a, b, c = st.columns(3)
a.metric("Total Income", f"₹{summary['income']:,.2f}")
b.metric("Total Expenses", f"₹{summary['expenses']:,.2f}")
c.metric("Current Balance", f"₹{summary['balance']:,.2f}")

tab_add, tab_view, tab_analytics = st.tabs(["➕ Add Transaction", "📋 Transactions", "📊 Analytics"])

with tab_add:
    st.subheader("Add a transaction")
    with st.form("add_form", clear_on_submit=True):
        left, right = st.columns(2)
        with left:
            kind = st.selectbox("Type", ["Expense", "Income"])
            amount = st.number_input("Amount (₹)", min_value=0.01, step=100.0)
            category = st.selectbox("Category", ["Food", "Transport", "Shopping", "Bills", "Education", "Health", "Entertainment", "Salary", "Business", "Other"])
        with right:
            txn_date = st.date_input("Date", value=date.today())
            description = st.text_input("Description", placeholder="e.g. Lunch or monthly salary")
        if st.form_submit_button("Save transaction", type="primary"):
            add_transaction(kind, amount, category, description, txn_date.isoformat())
            st.success("Transaction added.")
            st.rerun()

with tab_view:
    st.subheader("Your transactions")
    if transactions.empty:
        st.info("No transactions yet. Add your first transaction.")
    else:
        f1, f2 = st.columns(2)
        kind_filter = f1.selectbox("Filter by type", ["All", "Income", "Expense"])
        search = f2.text_input("Search description or category")
        filtered = transactions.copy()
        if kind_filter != "All":
            filtered = filtered[filtered["type"] == kind_filter]
        if search.strip():
            filtered = filtered[
                filtered["description"].str.contains(search, case=False, na=False)
                | filtered["category"].str.contains(search, case=False, na=False)
            ]
        st.dataframe(filtered.rename(columns={"id":"ID","type":"Type","amount":"Amount (₹)","category":"Category","description":"Description","transaction_date":"Date"}), use_container_width=True, hide_index=True)
        if not filtered.empty:
            st.markdown("#### Edit or delete a transaction")
            chosen_id = st.selectbox("Choose transaction ID", filtered["id"].tolist())
            selected = transactions[transactions["id"] == chosen_id].iloc[0]
            with st.form("edit_form"):
                x, y = st.columns(2)
                edit_type = x.selectbox("Type", ["Expense", "Income"], index=["Expense", "Income"].index(selected["type"]))
                edit_amount = x.number_input("Amount (₹)", min_value=0.01, value=float(selected["amount"]), step=100.0)
                categories = ["Food", "Transport", "Shopping", "Bills", "Education", "Health", "Entertainment", "Salary", "Business", "Other"]
                edit_category = x.selectbox("Category", categories, index=categories.index(selected["category"]) if selected["category"] in categories else categories.index("Other"))
                edit_date = y.date_input("Date", value=date.fromisoformat(str(selected["transaction_date"])))
                edit_description = y.text_input("Description", value=str(selected["description"] or ""))
                if st.form_submit_button("Update transaction"):
                    update_transaction(chosen_id, edit_type, edit_amount, edit_category, edit_description, edit_date.isoformat())
                    st.success("Transaction updated.")
                    st.rerun()
            if st.button("Delete selected transaction"):
                delete_transaction(chosen_id)
                st.success("Transaction deleted.")
                st.rerun()

with tab_analytics:
    st.subheader("Spending analytics")
    if transactions.empty:
        st.info("Add transactions to see analytics.")
    else:
        expenses = transactions[transactions["type"] == "Expense"]
        if not expenses.empty:
            chart_data = prepare_category_data(expenses)
            st.plotly_chart(px.pie(chart_data, names="category", values="amount", title="Expenses by category", hole=0.4), use_container_width=True)
        else:
            st.info("No expenses available for category analysis.")
        monthly = get_monthly_summary()
        if not monthly.empty:
            monthly["month"] = pd.to_datetime(monthly["month"]).dt.strftime("%b %Y")
            st.plotly_chart(px.bar(monthly, x="month", y=["income", "expenses"], barmode="group", title="Monthly income vs expenses", labels={"value":"Amount (₹)","month":"Month"}), use_container_width=True)
            st.dataframe(monthly, use_container_width=True, hide_index=True)
