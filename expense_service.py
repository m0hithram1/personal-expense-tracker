import pandas as pd
from database import get_connection

def add_transaction(transaction_type, amount, category, description, transaction_date):
    with get_connection() as connection:
        connection.execute(
            "INSERT INTO transactions (type, amount, category, description, transaction_date) VALUES (?, ?, ?, ?, ?)",
            (transaction_type, float(amount), category, description.strip(), transaction_date)
        )

def get_transactions():
    with get_connection() as connection:
        rows = connection.execute("SELECT * FROM transactions ORDER BY transaction_date DESC, id DESC").fetchall()
    return pd.DataFrame([dict(row) for row in rows], columns=["id","type","amount","category","description","transaction_date"])

def update_transaction(transaction_id, transaction_type, amount, category, description, transaction_date):
    with get_connection() as connection:
        connection.execute(
            "UPDATE transactions SET type=?, amount=?, category=?, description=?, transaction_date=? WHERE id=?",
            (transaction_type, float(amount), category, description.strip(), transaction_date, int(transaction_id))
        )

def delete_transaction(transaction_id):
    with get_connection() as connection:
        connection.execute("DELETE FROM transactions WHERE id=?", (int(transaction_id),))

def get_summary():
    with get_connection() as connection:
        income = connection.execute("SELECT COALESCE(SUM(amount),0) FROM transactions WHERE type='Income'").fetchone()[0]
        expenses = connection.execute("SELECT COALESCE(SUM(amount),0) FROM transactions WHERE type='Expense'").fetchone()[0]
    return {"income": float(income), "expenses": float(expenses), "balance": float(income-expenses)}

def get_monthly_summary():
    with get_connection() as connection:
        rows = connection.execute("""
            SELECT strftime('%Y-%m-01', transaction_date) AS month,
                   SUM(CASE WHEN type='Income' THEN amount ELSE 0 END) AS income,
                   SUM(CASE WHEN type='Expense' THEN amount ELSE 0 END) AS expenses
            FROM transactions GROUP BY strftime('%Y-%m', transaction_date) ORDER BY month
        """).fetchall()
    return pd.DataFrame([dict(row) for row in rows], columns=["month","income","expenses"])
