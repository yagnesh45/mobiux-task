import csv

# from datetime import datetime

sales_dates_list = []
SKU_list = []
unit_price_list = []
quantity_list = []
total_price_list = []
iterate_count = 0

with open("sales-data.csv", "r") as sales_data_file:
    content_reader = csv.reader(sales_data_file)
    for row in content_reader:
        if iterate_count == 0:
            iterate_count += 1
            continue
        else:
            sales_dates_list.append(row[0])
            SKU_list.append(row[1])
            unit_price_list.append(int(row[2]))
            quantity_list.append(row[3])
            total_price_list.append(int(row[4]))


total_sales = sum(total_price_list)
print("Sum of Sales: " + str(total_sales) + " ₹")


print("Month-wise Sales:")
month_wise_sale_dict = {}
for index, date in zip(range(len(sales_dates_list)), sales_dates_list):
    parse_month = int(date.split("-")[1])
    month_wise_sale_dict[parse_month] = (
        month_wise_sale_dict.get(parse_month, 0) + total_price_list[index]
    )

print(month_wise_sale_dict)


month_wise_items = {}
month_wise_popular_items = {}
for month in month_wise_sale_dict.keys():
    month_wise_items[month] = {}
    month_wise_popular_items[month] = {}

# Most popular item (most quantity sold) in each month.

for index, date in zip(range(len(sales_dates_list)), sales_dates_list):
    parse_month = int(date.split("-")[1])
    month_wise_items[parse_month][SKU_list[index]] = month_wise_items[
        parse_month
    ].get(SKU_list[index], 0) + int(quantity_list[index])

print("Month wise popular items:")

for month_key in month_wise_items.keys():
    popular_item = max(
        month_wise_items[month_key], key=month_wise_items[month_key].get
    )
    month_wise_popular_items[month_key][popular_item] = month_wise_items[
        month_key
    ][popular_item]

print(month_wise_popular_items)
