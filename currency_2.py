import requests
import tkinter as tk
from tkinter import ttk, messagebox

API_KEY = 'fca_live_Rz3PY28YPF3ezMFdIIew4IvKDLGNtz5mkBRXcUmz'
BASE_URL = f'https://api.freecurrencyapi.com/v1/latest?apikey={API_KEY}'
CURRENCIES = ['USD', 'AUD', 'CAD', 'EUR', 'INR', 'JPY', 'GBP', 'CHF', 'CNY', 'NZD']

def convert_currency(base, currencies):
    currencies_string = ",".join(currencies)
    url = f'{BASE_URL}&base_currency={base}&currencies={currencies_string}'
    try:
        response = requests.get(url)
        data = response.json()
        return data["data"]
    except Exception as e:
        print('Invalid currency or API request failed.', e)
        return None

def perform_conversion():
    base = base_currency_var.get()
    selected_currencies = [currency for currency, var in currency_variable.items() if var.get()]

    if not selected_currencies:
        messagebox.showwarning("Input Error", "Please select at least one currency to convert to.")
        return

    data = convert_currency(base, selected_currencies)
    if not data:
        messagebox.showerror("API Error", "Failed to retrieve currency data.")
        return

    result.delete('1.0', tk.END)
    if base in data:
        del data[base]
    for ticker, value in data.items():
        result.insert(tk.END, f"{ticker}: {value}\n")

# For creating the main window
root = tk.Tk()
root.title("Currency Converter")

# Selection of base currency
tk.Label(root, text="Select base currency:").grid(row=0, column=0, padx=10, pady=10)
base_currency_var = tk.StringVar()
base_currency_dropdown = ttk.Combobox(root, textvariable=base_currency_var, values=CURRENCIES, state="readonly")
base_currency_dropdown.grid(row=0, column=1, padx=10, pady=10)
base_currency_dropdown.current(0)  # Default value of base currency

# Currencies to convert to
tk.Label(root, text="Select currencies to convert to:").grid(row=1, column=0, padx=10, pady=10)
currency_variable = {currency: tk.BooleanVar() for currency in CURRENCIES}
for idx, (currency, var) in enumerate(currency_variable.items()):
    tk.Checkbutton(root, text=currency, variable=var).grid(row=2 + idx // 3, column=idx % 3, padx=5, pady=5)

# Convert button
convert_button = tk.Button(root, text="Convert", command=perform_conversion)
convert_button.grid(row=6, column=0, columnspan=3, pady=20)

# Display the result
result = tk.Text(root, width=50, height=10)
result.grid(row=7, column=0, columnspan=3, padx=10, pady=10)

root.mainloop()