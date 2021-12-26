import pandas as pd


def get_price(sk, code):
    df = pd.read_excel(r"./static/assets/tool_price.xlsx")
    if sk == "11" or sk==11:
        ask = "1B"

    elif sk == "10" or sk==10:
        ask = "1A"


    search_str = ask+ " " +code
    print(search_str)

    price = df[df["CODE NO"] == search_str]["AIPL Selling"]
    if price.empty:

        search_str = sk + " " + code
        alt_price = df[df["CODE NO"] == search_str]["AIPL Selling"]

        if alt_price.empty:
            price=0
            return price
        else:
            return float(price)
    else:

        return round(price,2)
