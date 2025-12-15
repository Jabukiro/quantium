import csv
FILENAMES = ["data/daily_sales_data_0.csv","data/daily_sales_data_1.csv", "data/daily_sales_data_2.csv"]
NEWFILENAME = "data/processed_data.csv"

def filter_pink_morsels(productName: str):
    return productName == "pink morsel"
def calc_sales(price, quantity):
    return float(price[1:-1]) * int(quantity)




def main():
    processedData=[["product","sales","date","region"]]

    for filename in FILENAMES:
        with open(filename) as csvfile:
            filereader = csv.DictReader(csvfile)
            for row in filereader:
                if filter_pink_morsels(row["product"]):
                    sales = calc_sales(row["price"], row["quantity"])
                    processedData.append([row['product'], str(sales), row['date'], row['region']])

    with open(NEWFILENAME, mode="w") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(processedData)

main()