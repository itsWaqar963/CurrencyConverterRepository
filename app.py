from flask import Flask, render_template, request
import requests

app = Flask(__name__)

CURRENCY_API_URL = "https://open.er-api.com/v6/latest"

def get_rates(base="USD"):
    try:
        url = f"{CURRENCY_API_URL}/{base}"
        print("Requesting:", url)
        response = requests.get(url, timeout=10)
        print("Status code:", response.status_code)
        print("Response text:", response.text[:500])
        if response.status_code == 200:
            data = response.json()
            # The rates are under the "rates" key
            return data.get("rates", {})
        else:
            print("Failed to get rates, status:", response.status_code)
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

if __name__ == "__main__":
    app.run(debug=True)