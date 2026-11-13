def prepare_category_data(expenses):
    """Group expense amounts by category for charting."""
    return expenses.groupby("category", as_index=False)["amount"].sum().sort_values("amount", ascending=False)
