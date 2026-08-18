import csv
import json
from pathlib import Path

import pandas as pd

try:
    from src.client import Client
    from src.client_collection import ClientCollection
    from src.sale import Sale
    from src.sales_collection import SalesCollection
except ModuleNotFoundError:
    from client import Client
    from client_collection import ClientCollection
    from sale import Sale
    from sales_collection import SalesCollection


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"


def _load_clients():
    with (DATA_DIR / "clients.json").open("r", encoding="utf-8") as f:
        clients_data = json.load(f)
    return [
        Client(
            client_id=item["client_id"],
            name=item["name"],
            country=item["country"],
            signup_date=item["signup_date"],
        )
        for item in clients_data
    ]


def _load_sales():
    sales = []
    with (DATA_DIR / "sales.csv").open("r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            sales.append(
                Sale(
                    sale_id=row["sale_id"],
                    client_id=int(row["client_id"]),
                    product=row["product"],
                    category=row["category"],
                    amount=float(row["amount"]),
                    date=row["date"],
                )
            )
    return sales


def generate_report(min_spending=500, category_focus="Electronics"):
    clients = _load_clients()
    sales = _load_sales()

    client_collection = ClientCollection(clients)
    sales_collection = SalesCollection(sales)

    total_revenue = round(sum(sale.amount for sale in sales), 2)

    clients_report = []
    for client in clients:
        total_spent = round(sales_collection.total_amount_by_client(client.client_id), 2)
        sale_count = len(sales_collection.sales_by_client(client.client_id))
        average_sale = round(total_spent / sale_count, 2) if sale_count else 0
        clients_report.append(
            {
                "client_id": client.client_id,
                "name": client.name,
                "total_spent": total_spent,
                "sale_count": sale_count,
                "average_sale": average_sale,
            }
        )

    top_client_by_country = {}
    countries = sorted({client.country for client in clients})
    for country in countries:
        country_clients = client_collection.clients_by_country(country)
        if not country_clients:
            continue
        top_client = max(
            country_clients,
            key=lambda client: sales_collection.total_amount_by_client(client.client_id),
        )
        top_client_by_country[country] = top_client.name

    sales_df = pd.read_csv(DATA_DIR / "sales.csv")
    sales_by_category_series = sales_df.groupby("category")["amount"].sum()
    sales_by_category = {
        category: round(float(value), 2)
        for category, value in sales_by_category_series.items()
    }

    high_spending_clients = [
        client.name
        for client in clients
        if sales_collection.total_amount_by_client(client.client_id) > min_spending
    ]

    sales_df["date"] = pd.to_datetime(sales_df["date"])
    sales_df["month"] = sales_df["date"].dt.to_period("M").astype(str)
    monthly_series = sales_df.groupby("month")["amount"].sum()
    monthly_sales = {
        month: round(float(value), 2) for month, value in monthly_series.items()
    }

    # Cálculo explícito para cumplir requisito de uso funcional + cruce:
    # cliente con más ventas en una categoría específica.
    top_client_in_focus_category = max(
        clients,
        key=lambda client: len(
            [
                sale
                for sale in sales_collection.sales_by_client(client.client_id)
                if sale.category == category_focus
            ]
        ),
    )

    return {
        "summary": {
            "total_clients": len(clients),
            "total_sales": len(sales),
            "total_revenue": total_revenue,
        },
        "clients": clients_report,
        "top_client_by_country": top_client_by_country,
        "sales_by_category": sales_by_category,
        "top_client_in_category": {
            category_focus: top_client_in_focus_category.name
        },
        "high_spending_clients": high_spending_clients,
        "monthly_sales": monthly_sales,
    }


if __name__ == "__main__":
    report = generate_report()
    output_path = BASE_DIR / "final_report.json"
    with output_path.open("w", encoding="utf-8") as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
