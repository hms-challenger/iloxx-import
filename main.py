import requests
import json
import csv
from datetime import date
from config import *


iloxxTemplate = {
    'Firma': '',
    'Name': '',
    'Straße': '',
    'Adresszusatz': '',
    'Postleitzahl': '',
    'Ort': '',
    'Land': '',
    'Telefon': '',
    'E-Mail': '',
    'Kundennummer': '',
    'Referenz': '',
    'Inhalt': '',
    'Gewicht': '',
    'Nachnamebetrag': ''
}


i = 0
offset = 0
# get data from ecwid api and store to json
print("getting ecwid data...")
while True:
    response = requests.get("https://app.ecwid.com/api/v3/"+str(id)+"/orders?offset="+str(offset)+"&limit=100&token="+str(token))
    data = response.json()
    json_object = json.dumps(data, indent=4, ensure_ascii=False)
    with open("data"+str(i)+".json", "w") as outfile:
        outfile.write(json_object)
    print(data)
    i += 1
    offset += 100
    if offset == 500:
        break
outfile.close()

with open("iloxxImport.csv", "w", encoding='UTF8', newline='') as csvfile:
    writer = csv.writer(csvfile, delimiter= ';')
    writer.writerow(iloxxTemplate.keys())
csvfile.close()

v = 0
countOrders = 1
i = 0

while True:
    with open("data"+str(i)+".json", "r") as infile:
        data = json.loads(infile.read())
        count = data['count']
        for v in range(count):
            if data['items'][v]['paymentStatus'] == 'PAID' and data['items'][v]['fulfillmentStatus'] == 'AWAITING_PROCESSING':
                if data['items'][v]['subtotal'] >= 19:
                    # print(countOrders, data['items'][v]['invoices'][0]['created'], data['items'][v]['subtotal'], data['items'][v]['email'], data['items'][v]['id'])
                    iloxxTemplate['Name'] = data['items'][v]['billingPerson']['name'] # name
                    iloxxTemplate['Straße'] = data['items'][v]['billingPerson']['street'] # straße
                    iloxxTemplate['Postleitzahl'] = data['items'][v]['billingPerson']['postalCode'] # plz
                    iloxxTemplate['Ort'] = data['items'][v]['billingPerson']['city'] # ort
                    if data['items'][v]['billingPerson']['countryCode'] == "DE":
                        iloxxTemplate['Land'] = "DEU" # land
                    else:
                        print("Land konnte nicht zugeordnet werden!")
                        iloxxTemplate['Land'] = ""
                    iloxxTemplate['E-Mail'] = data['items'][v]['email'] # email
                    iloxxTemplate['Referenz'] = "Minimusiker-Bestellung"
                    iloxxTemplate['Inhalt'] = "Buch"
                    # print(data['items'][v]['billingPerson']['name']) # firma
                    # print(data['items'][v]['invoices'][0]['created']) # telefon
                    # print(data['items'][v]['invoices'][0]['created']) # kundennummer
                    # print(data['items'][v]['invoices'][0]['created']) # nachnamebetrag
                    with open('iloxxImport.csv', 'a', encoding='UTF8') as csvfile:
                        writer = csv.writer(csvfile, delimiter=';')
                        writer.writerow(iloxxTemplate.values())
                        csvfile.close()
                    countOrders += 1
                    v += 1
    if i == 1:
        break
    i += 1
    infile.close()