from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__, template_folder="../templates")

CURRENCY_API_URL = "https://open.er-api.com/v6/latest"

def get_rates(base="USD"):
    try:
        url = f"{CURRENCY_API_URL}/{base}"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return data.get("rates", {})
    except Exception as e:
        print("Exception occurred:", e)
    return {}

@app.route("/", methods=["GET", "POST"])
def index():
    currencies = []
    result = None
    amount = 1
    from_currency = "USD"
    to_currency = "EUR"

    rates = get_rates()
    if rates:
        currencies = sorted(rates.keys())

    if request.method == "POST":
        amount = float(request.form.get("amount", 1))
        from_currency = request.form.get("from_currency", "USD")
        to_currency = request.form.get("to_currency", "EUR")

        rates = get_rates(from_currency)
        rate = rates.get(to_currency)
        if rate:
            result = amount * rate

    return render_template(
        "index.html",
        currencies=currencies,
        result=result,
        amount=amount,
        from_currency=from_currency,
        to_currency=to_currency
    )

# Vercel will look for 'app'
# No if __name__ == "__main__": block needed!