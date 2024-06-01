from bs4 import BeautifulSoup
import os
import pandas as pd
import json


def parse_data(input_html) -> json:
    soup = BeautifulSoup(input_html, "html.parser")

    jcar = {}

    auction_date = soup.find(class_='psa-tabs-content')
    auction_date = auction_date.find_all('tr')[-1]
    final_bid = auction_date.find(class_='status price')
    jcar['final_bid'] = final_bid.text.replace('$', '').replace(',', '').replace('---', '0')
    sold = auction_date.find(class_='status sold')
    if sold:
        sold = sold.text.strip()
        jcar['Sold'] = sold
    else:
        jcar['Sold'] = "Not Sold"


    seller = auction_date.find_all('td')[-1].text.strip()
    jcar['Seller'] = seller
    auction_date = auction_date.find('td').text.strip()
    jcar['Auction_date'] = auction_date


    header = soup.find(class_="header-content")
    title = header.find('h1').text.replace(',', '').split()
    jcar['Year'] = title[0]
    jcar['Make'] = title[1]

    info = header.find(class_='vin-info')
    jcar['vin'] = info.find(class_='vin-drop').text

    condition_details = soup.find(id='condition-details')
    condition_details = condition_details.find(class_='options-list')
    condition_details = condition_details.find_all(class_='option')

    for _ in condition_details:
        value = _.find('span').text.strip()
        param = _.text.replace(value, '').strip()
        jcar[param] = value

    vehicle_details = soup.find(id='car-details')
    vehicle_details = vehicle_details.find(class_='options-list')
    vehicle_details = vehicle_details.find_all('div')

    for _ in vehicle_details:
        value = _.find('span').text.strip()
        param = _.text.replace(value, '').strip()
        jcar[param] = value

    additional_info = soup.find(id='info-destination')
    additional_info = additional_info.find(class_='options-list')
    additional_info = additional_info.find_all(class_='option-trip')[3]
    price = additional_info.find_all('div')

    for _ in price:
        param = _.find('span').text.strip()
        value = _.text.replace(param, '').strip()
        jcar[param] = value

    if 'Odometer' in jcar:
        odo = jcar['Odometer'].split('(')
        jcar['Odometer_km'] = odo[1].replace('km)', '').replace(' ', '')

    if 'Cylinders' in jcar:
        jcar['Cylinders'] = jcar['Cylinders'].split()[0]

    if 'ACV' in jcar:
        jcar['Actual_cash_value'] = jcar['ACV'].replace('$', '').replace(',', '')

    if 'ERC' in jcar:
        jcar['Estimated_repair_cost'] = jcar['ACV'].replace('$', '').replace(',', '')

    if 'Engine' in jcar:
        jcar['Eng_L'] = jcar['Engine'].split('L')[0]
        hp = jcar['Engine'].split()
        jcar['Eng_HP'] = hp[len(hp) - 1].replace('HP', '')

    not_needed = ['VIN', 'Photos', 'Airbag checked', 'Restraint System', 'Odometer', 'Engine', 'ACV', 'ERC']
    for _ in not_needed:
        if _ in jcar:
            del jcar[_]

    return jcar


def read_files(path):
    for root, dirnames, filenames in os.walk(path):
        for filename in filenames:
            path = os.path.join(root, filename)

            with open(path) as file:
                # print(path)
                if path != 'resources/.DS_Store':
                    full_text = file.read()
                    car = parse_data(full_text)

            yield car


df = pd.DataFrame(read_files("resources"))
df.to_csv('data/data.csv', index=False)

print(df)
