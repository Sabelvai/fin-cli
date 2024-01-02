import requests
from bs4 import BeautifulSoup as bs
import re
from dateutil.parser import parse
import fake_useragent
from api import dbapi
from rich.console import Console
from rich.text import Text

def convert_currency_xe(src, dst, amount):
    def get_digits(text):
        """Returns the digits and dots only from an input `text` as a float
        Args:
            text (str): Target text to parse
        """
        new_text = ""
        for c in text:
            if c.isdigit() or c == ".":
                new_text += c
        return float(new_text)

    user = fake_useragent.UserAgent().random

    header = {'user-agent': user}

    url = f"https://www.xe.com/currencyconverter/convert/?Amount={amount}&From={src}&To={dst}"
    content = requests.get(url).content
    soup = bs(content, "html.parser")
    exchange_rate_html = soup.find_all("p")[2]
    currency_price = soup.find_all("p")[3]
    last_updated_datetime = parse(re.search(r"Last updated (.+)", exchange_rate_html.parent.parent.find_all("div")[-2].text).group()[12:])
    return last_updated_datetime, get_digits(exchange_rate_html.text), currency_price.text,

def check(source_currency, destination_currency, amount, prushpare_price):
    last_updated_datetime, exchange_rate ,currency_price = convert_currency_xe(source_currency,
    destination_currency, amount)

    console = Console()
    console_width = console.width

    left_text = f"{amount} {source_currency} = {round(exchange_rate, 2)} {destination_currency}"
    right_text = f"Last updated datetime: {last_updated_datetime}"

    padding_width = console_width - len(left_text) - len(right_text)

    formatted_line = f"{left_text}{' ' * padding_width}{right_text}"

    console.print(formatted_line)
    print(f"{currency_price}\n")

    new_price = float(re.search(r'=\s*([-+]?\d*\.\d+|\d+)', currency_price).group(1)) if re.search(r'=\s*([-+]?\d*\.\d+|\d+)', currency_price) else None
    percentage_change = ((new_price - prushpare_price) / abs(prushpare_price)) * 100

    if new_price > prushpare_price:
        console.print(f"The value increased by [bold]{percentage_change:.2f}%")
    elif new_price < prushpare_price:
        console.print(f"The value decreased by [bold]{percentage_change:.2f}%")
    else:
        print("The value is fixed")

    up_value = round(exchange_rate - (prushpare_price * amount))
    console.print(f"Your currency increased by [bold]{up_value} {destination_currency}")
