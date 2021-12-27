from config import LocalDevelopmentConfig


def get_price(sk, code):

    if sk == "11" or sk==11:
        ask = "1B"

    elif sk == "10" or sk==10:
        ask = "1A"


    search_str = ask+ " " +code
    print(search_str)

    price = LocalDevelopmentConfig.DATA[LocalDevelopmentConfig.DATA["CODE NO"] == search_str]["AIPL Selling"]
    if price.empty:

        nsearch_str = sk + " " + code
        alt_price = LocalDevelopmentConfig.DATA[LocalDevelopmentConfig.DATA["CODE NO"] == nsearch_str]["AIPL Selling"]

        if alt_price.empty:
            price=0
            return price
        else:
            return float(alt_price)

    else:

        return round(price,2)
