class SalesCollection:
    def __init__(self, sales):
        self.sales = sales

    def sales_by_client(self, client_id):
        return [sale for sale in self.sales if sale.client_id == client_id]

    def total_amount_by_client(self, client_id):
        return sum(sale.amount for sale in self.sales_by_client(client_id))

    def total_amount_by_category(self, category):
        return sum(sale.amount for sale in self.sales if sale.category == category)

    def average_sale_by_client(self, client_id):
        client_sales = self.sales_by_client(client_id)
        if not client_sales:
            return 0
        return round(
            sum(sale.amount for sale in client_sales) / len(client_sales),
            2,
        )
