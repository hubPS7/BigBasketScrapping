from selectorlib import Extractor
import json
import io
import requests
import csv

fields = ['Brand', 'Saleprice', 'MRP', 'Weight', 'ProductType', 'Rating', 'ProductDetails', 'Description']
out_file = open('bigbasket.csv', 'w', encoding='utf-8')
csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)
csvwriter.writeheader()

def scrape(url):

    headers = {
        'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.bigbasket.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8',
    }

    # Download the page using requests
    # print("Downloading %s"%url)
    r = requests.get(url, headers=headers)
    # Simple check to check if page was blocked (Usually 503)
    if r.status_code > 500:
        if "To discuss automated access to Amazon data please contact" in r.text:
            print("Page %s was blocked by Amazon. Please try using better proxies\n" % url)
        else:
            print("Page %s must have been blocked by Amazon as the status code was %d" % (url, r.status_code))
        return None
    # Pass the HTML of the page and create
    return json.loads(r.text)

page_number = 2
service_count = 1

while True:
    # Check if reached end of result
    if page_number > 21:
        break
    url = 'https://www.bigbasket.com/product/get-products/?slug=organic&page=' + str(
        page_number) + '&tab_type=[%22all%22]&sorted_on=relevance&listtype=ps'
    print(url)
    Data = scrape(url)
    Data = Data["tab_info"]["product_map"]["all"]["prods"]
    if Data:
        for product in Data:
            dict_service = {}

            dict_service['Brand'] = product['p_brand']
            dict_service['Saleprice'] = product['sp']
            dict_service['MRP'] = product['mrp']
            dict_service['Weight'] = product['w']
            dict_service['ProductType'] = product['p_type']

            ratingArray = product['rating_info']
            dict_service['Rating'] = ratingArray.get('avg_rating')

            dict_service['ProductDetails'] = product['tlc_n']
            dict_service['Description'] = product['p_desc']


            # Write row to CSV
            csvwriter.writerow(dict_service)

    page_number += 1
out_file.close()


#https://youtu.be/fNHLdrScPog