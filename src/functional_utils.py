from functools import reduce


def filter_sales_by_category(sales, category):
    return list(filter(lambda sale: sale.category == category, sales))


def filter_sales_by_date(sales, date_value):
    return list(filter(lambda sale: sale.date == date_value, sales))


def map_sales_amounts(sales):
    return list(map(lambda sale: sale.amount, sales))


def reduce_total_amount(sales):
    return reduce(lambda acc, sale: acc + sale.amount, sales, 0)
