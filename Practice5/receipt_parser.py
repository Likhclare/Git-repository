import re
import json
import os

file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "raw.txt")

try:
    with open(file_path, "r", encoding="utf-8") as file:
        receipt = file.read()
except FileNotFoundError:
    print(f"Файл не найден: {file_path}")
    exit()

prices = re.findall(r"\d[\d ]*,\d{2}", receipt)

prices_clean = []
for p in prices:
    for part in p.split():
        prices_clean.append(float(part.replace(" ", "").replace(",", ".")))

products = re.findall(r"\d+\.\s(.+?)(?=\n\d+\.|\n$)", receipt, re.DOTALL)
products = [p.strip() for p in products]

total_amount = sum(prices_clean)

datetime_match = re.search(r"Время:\s*(\d{2}\.\d{2}\.\d{4}) (\d{2}:\d{2}:\d{2})", receipt)
if datetime_match:
    date, time = datetime_match.groups()
else:
    date, time = None, None

payment_match = re.search(r"(Банковская карта|Наличные):", receipt)
payment_method = payment_match.group(1) if payment_match else None

parsed_receipt = {
    "products": products,
    "prices": prices_clean,
    "total_amount": total_amount,
    "date": date,
    "time": time,
    "payment_method": payment_method
}

print(json.dumps(parsed_receipt, ensure_ascii=False, indent=4))