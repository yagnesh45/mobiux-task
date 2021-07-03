import csv
from datetime import datetime
import json


date_format = "%b-%Y"


def parse_data(file_data):
    """Parses Data and stores it in proper dictionary

    :args:\
        file_data(list of string lines from file)

    :returns:\
        sales_data(parsed and stored data in form of dictionary)
    """

    iterated_heading = False  # to ignore first heading row
    sales_data = []
    for row in file_data:
        if not iterated_heading:
            iterated_heading = True
        else:
            try:
                sales_row = {}
                sales_row["sales_date"] = datetime.strptime(row[0], "%Y-%m-%d")
                sales_row["SKU"] = row[1]
                sales_row["unit_price"] = float(row[2])
                sales_row["quantity"] = int(row[3])
                sales_row["total_price"] = float(row[4])
                sales_data.append(sales_row)
            except Exception as ex:
                print(
                    "ERROR: in File Parsing, please check your file to meet "
                    "specified requirements \nMore Info:",
                    ex,
                )
                exit(1)

    return sales_data


def calculate_total_sales():
    """Calculates Total Sales in total for all the sales items

    :returns:\
        total_sales(total number of sales => sum of total_price of items)
    """

    total_sales = 0
    for sales_object in parsed_sales_data:
        total_sales += sales_object["total_price"]

    return total_sales


def calculate_month_wise_total_sales():
    """Calculates Month wise sum of total sales for all the items"""

    global month_wise_total_sales
    month_wise_total_sales = {}
    for sales_object in parsed_sales_data:
        # get the date from sales_data for each item
        parse_date = sales_object["sales_date"].strftime(date_format)

        # perform sum of total_price for items month wise
        month_wise_total_sales[parse_date] = (
            month_wise_total_sales.get(parse_date, 0)
            + sales_object["total_price"]
        )


def calculate_total_sales_for_items_per_month():
    """Calculates Month wise total sales of each item

    :returns:\
        month_wise_items: month wise each items total sales
    """

    month_wise_items = {}
    global month_wise_popular_items
    month_wise_popular_items = {}
    for month in month_wise_total_sales.keys():
        month_wise_items[month] = {}
        month_wise_popular_items[month] = {}

    for sales_object in parsed_sales_data:
        # get the date from sales_data for each item
        parse_date = sales_object["sales_date"].strftime(date_format)

        # perform sum of sales for each item month wise
        month_wise_items[parse_date][sales_object["SKU"]] = (
            month_wise_items[parse_date].get(sales_object["SKU"], 0)
            + sales_object["quantity"]
        )

    return month_wise_items


def calculate_month_wise_popular_items():
    """Calculates Month wise most popular item according to quantities sold"""

    # get total sales of each items month wise
    month_wise_items_total_sale = calculate_total_sales_for_items_per_month()

    global month_wise_popular_items

    for month_key in month_wise_items_total_sale.keys():
        # get item with maximum number of total_sales each month
        popular_item = max(
            month_wise_items_total_sale[month_key],
            key=month_wise_items_total_sale[month_key].get,
        )

        # store the item and total_quantity sold in key of month
        month_wise_popular_items[month_key]["item"] = popular_item
        month_wise_popular_items[month_key][
            "total_quantity"
        ] = month_wise_items_total_sale[month_key][popular_item]


def calculate_month_wise_items_revenue():
    """Calculates Month wise item with most revenue according to
    Sum of total sales
    """

    month_wise_items = {}
    global month_wise_revenue_of_items
    month_wise_revenue_of_items = {}

    # store unique month as keys with empty values for initialization
    for month in month_wise_total_sales.keys():
        month_wise_items[month] = {}
        month_wise_revenue_of_items[month] = {}

    # store sum of total_price for each item month wise in month_wise_items
    for sales_object in parsed_sales_data:
        parse_date = sales_object["sales_date"].strftime(date_format)
        month_wise_items[parse_date][sales_object["SKU"]] = (
            month_wise_items[parse_date].get(sales_object["SKU"], 0)
            + sales_object["total_price"]
        )

    # Get the item with maximum revenue and store it in
    #   month_wise_revenue_of_items in key of month
    for month_key in month_wise_items.keys():
        most_revenue_item = max(
            month_wise_items[month_key],
            key=month_wise_items[month_key].get,
        )
        month_wise_revenue_of_items[month_key]["item"] = most_revenue_item
        month_wise_revenue_of_items[month_key][
            "total_revenue"
        ] = month_wise_items[month_key][most_revenue_item]


def calculate_month_wise_min_max_avg_popular_item():
    """Calculates Min, Max and Average number of quantities sold
    month wise for most popular item"""

    # get popular items month wise
    global min_max_avg_popular_item
    min_max_avg_popular_item = month_wise_popular_items

    for sales_object in parsed_sales_data:
        parse_date = sales_object["sales_date"].strftime(date_format)

        # check if the current iterating item is most popular item for
        #   the given month or not
        if sales_object["SKU"] == min_max_avg_popular_item[parse_date]["item"]:
            # initially store the no_of_order = 1 and min,max = quantity
            #   of item then, increment no_of_order and calculate min,max and
            #   average as most popular items appear in sales_data again
            if (
                min_max_avg_popular_item[parse_date].get("no_of_order", None)
                is None
            ):
                min_max_avg_popular_item[parse_date]["no_of_order"] = 1
                min_max_avg_popular_item[parse_date][
                    "min_quantity"
                ] = sales_object["quantity"]
                min_max_avg_popular_item[parse_date][
                    "max_quantity"
                ] = sales_object["quantity"]
                min_max_avg_popular_item[parse_date][
                    "avg_quantity"
                ] = sales_object["quantity"]
            else:

                # calculate average as total_quantity / total number orders
                min_max_avg_popular_item[parse_date]["no_of_order"] += 1
                min_max_avg_popular_item[parse_date]["avg_quantity"] = (
                    min_max_avg_popular_item[parse_date]["total_quantity"]
                    / min_max_avg_popular_item[parse_date]["no_of_order"]
                )
                if (
                    min_max_avg_popular_item[parse_date]["min_quantity"]
                    >= sales_object["quantity"]
                ):
                    min_max_avg_popular_item[parse_date][
                        "min_quantity"
                    ] = sales_object["quantity"]
                if (
                    min_max_avg_popular_item[parse_date]["max_quantity"]
                    < sales_object["quantity"]
                ):
                    min_max_avg_popular_item[parse_date][
                        "max_quantity"
                    ] = sales_object["quantity"]


def display_formatted_items(items):
    """Display Items in dictionary with proper indentation for better view"""
    print(json.dumps(items, indent=3))


def main():

    with open("sales-data.csv", "r") as sales_data_file:
        file_content = csv.reader(sales_data_file)
        global parsed_sales_data
        parsed_sales_data = parse_data(file_content)

    # 1. Total Sales of the store
    print(
        "\n1. Total Sales of the store: " + str(calculate_total_sales()) + " ₹"
    )

    # 2. Month-wise sales total
    calculate_month_wise_total_sales()
    print("\n2.Month wise Total Sales:")
    display_formatted_items(month_wise_total_sales)

    # 3. Month wise most popular item (most quantity sold)
    calculate_month_wise_popular_items()
    print("\n3.Month wise most popular items:")
    display_formatted_items(month_wise_popular_items)

    # 4. Month wise Items with most revenue
    calculate_month_wise_items_revenue()
    print("\n4.Month wise items with most revenue: ")
    display_formatted_items(month_wise_revenue_of_items)

    # 5. For the most popular item, find the min, max and average number of
    #    orders each month
    calculate_month_wise_min_max_avg_popular_item()
    print("\n5. Min, Max and Average sales of Most Popular Item:")
    display_formatted_items(min_max_avg_popular_item)


if __name__ == "__main__":
    main()
