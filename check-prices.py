import requests
from colorama import Fore, Back, Style
import urllib.parse

# List of cards separated in the format [CARD_NAME, DESIRED_PRICE]
cards=[
    ['lost jitte', 9],
    ['liliana, the last', 4],
    ['shalai and', 5],
]

def get_card_prices(card):
    card_name = card[0]
    target_price = card[1]
    
    encoded = urllib.parse.quote(card_name)
    split_card_name = encoded.split()
    q = ('+').join(split_card_name)
    url = f"https://mp-search-api.tcgplayer.com/v1/search/request?q={q}&isList=true&mpfev=2399"

    filters = {
    "algorithm": "sales_synonym_v2",
    "from": 0,
    "size": 10,
    "filters": {
        "term": {
        "productLineName": [
            "magic"
        ],
        "productTypeName": [
            "Cards"
        ]
        },
        "range": {},
        "match": {}
    },
    "listingSearch": {
        "context": {
        "cart": {}
        },
        "filters": {
        "term": {
            "sellerStatus": "Live",
            "channelId": 0,
            # 
            "printing": [
            "Foil"
            ],
            "language": [
            "English"
            ],
            "condition": [
            "Lightly Played",
            "Near Mint"
            ]
        },
        "range": {
            "quantity": {
            "gte": 1
            }
        },
        "exclude": {
            "channelExclusion": 0
        }
        }
    },
    "context": {
        "cart": {},
        "shippingCountry": "US",
        "userProfile": {}
    },
    "settings": {
        "useFuzzySearch": True,
        "didYouMean": {}
    },
    "sort": {}
    }


    response = requests.post(
        url,
        headers={
            'Content-type':'application/json', 
            'Accept':'application/json'
        },
        params={"q": "", "isList": True},
        json=filters
    ).json()

    data = response['results'][0]

    results = data['results']

    more_to_see = data['totalResults'] > filters['from'] + 10

    while more_to_see:
        filters['from'] += 10
        response = requests.post(
            url,
            headers={
                'Content-type':'application/json', 
                'Accept':'application/json'
            },
            params={"q": "", "isList": True},
            json=filters
        ).json() 
        data = response['results'][0]

        new_results = data['results']

        results += new_results

        more_to_see = data['totalResults'] > filters['from'] + 10

    new_results = []
    for result in results:
        if ('Art Series' not in result['setName']) \
            and ('Emblem' not in result['productName']) \
            and ('Token' not in result['productName']):
            new_results.append(result)
        
    mins = []

    for result in new_results:
        prices = [listing['price'] + listing['shippingPrice'] for listing in result['listings']]
        if prices:
            productId = result['productId']
            sorted_prices = sorted(prices)
            cheapest = round(sorted_prices[0], 2)
            if len(sorted_prices) > 1:
                second_cheapest = round(sorted_prices[1], 2)
                diff = round(second_cheapest - cheapest, 2)
                # print(sorted_prices)
            else:
                diff = 0
            mins.append([
                cheapest,
                # diff,
                result['productName'],
                result['setName'], 
                
                # f'https://product-images.tcgplayer.com/fit-in/200x279/{productId}.jpg'
            ])

    # for min_el in mins:
        # print(min_el)
    if mins:
        min_of_mins = list(sorted(mins, key=lambda x: x[0]))[0] #smallest first
        if min_of_mins[0] < target_price:
            print(Fore.GREEN)
        else:
            print(Fore.RED)
        print(min_of_mins)

for card in cards:
    get_card_prices(card)