# Personal Expense Tracker

A Python application to record income and expenses, manage transactions, and understand spending patterns.

## Features
- Add income and expense transactions
- View, search, and filter transaction history
- Edit and delete transactions
- View total income, total expenses, and current balance
- Visualize expenses by category
- Compare monthly income and expenses
- Store records locally with SQLite

## Tech Stack
Python, Streamlit, SQLite, Pandas, Plotly

## Project Structure
```text
Expense-Tracker/
├── app.py
├── database.py
├── expense_service.py
├── analytics.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Run the project
1. Open this folder in VS Code.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the app:
   ```bash
   streamlit run app.py
   ```
4. Open the local URL shown in the terminal.

The `expenses.db` database is created automatically and is excluded from Git to keep personal transaction data private.

This is a local learning project. Do not enter sensitive banking information.
