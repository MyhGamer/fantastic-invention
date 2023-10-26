import requests
import csv
import json
from config import Authorization,address


url = f"https://prod-api.kosetto.com/portfolio/{address}"


headers = {
    "Authorization": Authorization
}

def wei_to_ether(wei_value):
    ether_value = float(wei_value) / (10 ** 18)
    return format(ether_value, '.18f')
try:
    response = requests.get(url, headers=headers)
    #print("Response status code:", response.status_code)

    if response.status_code == 200:
        data = response.json()
        #print("Response data:", data)
        # Extracting holdings data
        holdings = data.get('holdings', [])
        portfolio_value_ether = wei_to_ether(data.get('portfolioValueWei', 0))
        txt = input(("Write Y to save all addresses in wallets.txt or N to save only in csv: "))
        if txt.lower() == "y":
            with open('wallets.txt', 'w', newline='', encoding='utf-8') as file:
                for item in holdings:
                    chatRoomId = item.get('chatRoomId', '')
                    file.write(f"{chatRoomId}\n")  # Save each chatRoomId in a new line in wallets.txt

        csv_data = []
        for item in holdings:
            csv_data.append({
                'username': item.get('username', ''),
                'chatRoomId': item.get('chatRoomId', ''),
                'price (Ether)': wei_to_ether(item.get('price', 0)),
                'balance': item.get('balance', ''),
                'balanceEthValue (Ether)': wei_to_ether(item.get('balanceEthValue', 0))
            })

        print(f"Length of csv_data: {len(csv_data)}")

        # Write data to CSV
        with open('output.csv', 'w', newline='', encoding='utf-8') as file:
            fieldnames = ['username', 'chatRoomId', 'price (Ether)', 'balance', 'balanceEthValue (Ether)']

            writer = csv.DictWriter(file, fieldnames=fieldnames)

            writer.writeheader()
            for row in csv_data:
                writer.writerow(row)
            print("CSV file has been written.")

    else:
        print(f"Unexpected status code: {response.status_code}. Response text: {response.text}")

except Exception as e:
    print(f"An exception occurred: {e}")