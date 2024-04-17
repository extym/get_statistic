"""
Ozon api lib
"""

from typing import Tuple, Dict, List

import requests
import json
import datetime
import logging
import os

from cred import OZON_HEADERS, ANY_OZON_HEADERS

DATE_FORMAT = "%Y-%m-%dT%H:00:00.000Z"
host = 'https://api-seller.ozon.ru'


def check_api():
    url = f"https://api-seller.ozon.ru/v1/actions"
    try:
        resp = requests.get(url, headers=OZON_HEADERS)
        print(resp.text)
    except:
        return False

    return resp.ok


def get_smth(metod, params):
    link = host + metod
    response = requests.get(link, headers=params)
    print('get_smth_on', metod, response, response.json())
    return response


def post_get_assortment(headers):
    proxy = []
    requesting = True
    link = host + '/v2/product/list'
    last_id = ''
    while requesting:
        data_send = {
            "last_id": last_id
        }
        response = requests.post(link, headers=headers, json=data_send)
        data = response.json()
        result = data['result'].get('items')
        last_id = data['result'].get('last_id')
        if len(result) < 1000:
            requesting = False
        proxy.extend(result)

    print('post_get_assortment_oson', len(proxy))

    return proxy


def get_stocks():
    url = f"https://api-seller.ozon.ru/v1/analytics/stock_on_warehouses"
    offset = 0
    per_request = 100
    res = []
    while True:
        data = {
            "limit": per_request,
            "offset": offset
        }
        resp = requests.post(url, headers=OZON_HEADERS, json=data)
        try:
            res_list = json.loads(resp.text)["wh_items"]
        except:
            break
        if not res_list:
            break
        res.extend(res_list)
        offset += per_request
    return res


def get_reports_list(delta_days=7, headers=ANY_OZON_HEADERS):
    url = 'https://api-seller.ozon.ru/v1/report/list'
    data = {
        "page": 1,
        "page_size": 1000,
        "report_type": "ALL"
    }
    answer = requests.post(url=url, headers=headers, json=data)

    print(answer.json())


get_reports_list()


def report_product_create(delta_days=7, headers=ANY_OZON_HEADERS):
    url = 'https://api-seller.ozon.ru/v1/report/products/create'
    data = {
        "language": "DEFAULT",
        "offer_id": [],
        "search": "",
        "sku": [],
        "visibility": "ALL"
    }
    answer = requests.post(url=url, headers=headers, json=data)

    print(answer.json())  # {'result':
    # {'code': 'REPORT_seller_products_any_1709521529_fdfb12e1-5d87-42a0-9b4f-0f432095df86'}}


def report_returns_create(delta_days=7, headers=ANY_OZON_HEADERS):
    url = 'https://api-seller.ozon.ru/v1/report/returns/create'
    data = {
        "filter": {
            "delivery_schema": "fbs",
            "order_id": 0,
            "status": ""
        },
        "language": "DEFAULT"
    }
    answer = requests.post(url=url, headers=headers, json=data)

    print(answer.json())


def report_postings_create(delta_days=7, headers=ANY_OZON_HEADERS):
    url = 'https://api-seller.ozon.ru/v1/report/postings/create'
    dt = datetime.datetime.now() - datetime.timedelta(days=delta_days)
    date = dt.strftime("%Y-%m-%dT%H:00:00.000Z")
    date_now = datetime.datetime.now().strftime("%Y-%m-%dT%H:00:00.000Z")
    data = {
        "filter": {
            "processed_at_from": date,
            "processed_at_to": date_now,
            "delivery_schema": [
                "fbo"
            ],
            "sku": [],
            "cancel_reason_id": [],
            "offer_id": "",
            "status_alias": [],
            "statuses": [],
            "title": ""
        },
        "language": "DEFAULT"
    }

    answer = requests.post(url=url, headers=headers, json=data)

    print(answer.json())  # {'result': 
    # {'code': 'REPORT_seller_postings_any_1709522189_cfa094ee-d7b5-4076-b4a2-4db2f771eed2'}}


def report_finance_get(delta_days=7, headers=ANY_OZON_HEADERS):
    url = 'https://api-seller.ozon.ru/v1/finance/cash-flow-statement/list'
    dt = datetime.datetime.now() - datetime.timedelta(days=delta_days)
    date = dt.strftime("%Y-%m-%dT%H:00:00.000Z")
    date_now = datetime.datetime.now().strftime("%Y-%m-%dT%H:00:00.000Z")
    data = {
        "date": {
            "from": date,
            "to": date_now
        },
        "with_details": True,
        "page": 1,
        "page_size": 1
    }
    answer = requests.post(url=url, headers=headers, json=data)
    # {'result': {'cash_flows': [{'period': {'id': 11796523085490, 'begin': '2024-01-01T00:00:00Z',
    # 'end': '2024-01-15T00:00:00Z'}, 'orders_amount': 100822, 'returns_amount': 0, 'commission_amount': -16440.71,
    # 'services_amount': -2869.97, 'item_delivery_and_return_amount': -4135.59, 'currency_code': 'RUB'}],
    # 'page_count': 1, 'details': [{'period': {'id': 11796523085490, 'begin': '2024-01-01T00:00:00Z',
    # 'end': '2024-01-15T00:00:00Z'}, 'begin_balance_amount': 60335.73, 'payments': [{'payment': -59849.92,
    # 'currency_code': 'RUB'}], 'delivery': {'total': 81235.7, 'amount': 84381.29, 'delivery_services': {'total':
    # -3145.59, 'items': [{'name': 'MarketplaceServiceItemDirectFlowLogisticSum', 'price': -1366},
    # {'name': 'MarketplaceServiceItemDelivToCustomer', 'price': -1419.59}, {'name': 'MarketplaceServiceItemDropoff',
    # 'price': -360}]}}, 'return': {'total': -990, 'amount': 0, 'return_services': {'total': -990, 'items': [{'name':
    # 'MarketplaceServiceItemRedistributionReturnsPVZ', 'price': -60}, {'name':
    # 'MarketplaceServiceItemReturnNotDelivToCustomer', 'price': -100}, {'name':
    # 'MarketplaceServiceItemReturnFlowLogistic', 'price': -630}, {'name':
    # 'MarketplaceServiceItemReturnPartGoodsCustomer', 'price': -200}]}}, 'loan': 0, 'invoice_transfer': 77115.72,
    # 'rfbs': {'total': 0, 'transfer_delivery': 0, 'transfer_delivery_return': 0, 'compensation_delivery_return': 0,
    # 'partial_compensation': 0, 'partial_compensation_return': 0}, 'services': {'total': -2869.97, 'items': [{
    # 'name': 'MarketplaceServiceItemPremiumSubscribtion', 'price': -2495}, {'name':
    # 'MarketplaceReturnStorageServiceAtThePickupPointFbsItem', 'price': -300}, {'name':
    # 'MarketplaceServiceItemDefectRateDetailed', 'price': -74.97}]}, 'others': {'total': -745.82, 'items': [{'name':
    # 'MarketplaceRedistributionOfAcquiringOperation', 'price': -745.82}]}, 'end_balance_amount': 77115.72}]}}
    print(answer.json())


def report_finance_realisation(delta_days=7, headers=ANY_OZON_HEADERS):
    url = 'https://api-seller.ozon.ru/v1/finance/realization'
    data = {
        "date": "2024-01"
    }
    answer = requests.post(url=url, headers=headers, json=data)
    data = answer.json()
    print(data)
    return data


# report_finance_realisation()

def get_orders(delta_days, headers=OZON_HEADERS):
    url = "https://api-seller.ozon.ru/v2/posting/fbo/list"
    offset = 0
    per_request = 100
    res = []
    dt = datetime.datetime.now() - datetime.timedelta(days=delta_days)
    date_since = dt.strftime("%Y-%m-%dT%H:00:00.000Z")
    date_to = datetime.datetime.now().strftime("%Y-%m-%dT%H:00:00.000Z")
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    while True:
        data = {
            "limit": per_request,
            "offset": offset,
            "filter": {
                "since": date_since,
                "to": date_to
            },
            "with": {
                "analytics_data": True,
                "financial_data": True
            }
        }
        resp = requests.post(url, headers=headers, json=data)

        try:
            res_list = json.loads(resp.text)["result"]
        except:
            break
        if not res_list:
            break

        res.extend(res_list)
        offset += per_request
    return res


def get_orders_v2(delta, headers=OZON_HEADERS, schema='fbs'):
    url = f"https://api-seller.ozon.ru/v3/posting/{schema}/list"
    offset = 0
    per_request = 100
    res = []
    dt = datetime.datetime.now() - datetime.timedelta(hours=delta)
    date_since = dt.strftime(DATE_FORMAT)
    date_to = datetime.datetime.now().strftime(DATE_FORMAT)
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    while True:
        data = {
            "limit": per_request,
            "offset": offset,
            "filter": {
                "since": date_since,
                "to": date_to,
                "status": ""
            },
            "with": {
                "analytics_data": True,
                "financial_data": True
            }
        }
        resp = requests.post(url, headers=headers, json=data)
        # print(resp.text)
        try:
            res_list = json.loads(resp.text)["result"]["postings"]
        except:
            break
        if not res_list:
            break

        res.extend(res_list)
        offset += per_request
    return res


def get_orders_v3(delta, headers=OZON_HEADERS, schema='fbs'):
    url = f"https://api-seller.ozon.ru/v3/posting/{schema}/list"
    offset = 0
    per_request = 100
    res = []
    dt = datetime.datetime.now() - datetime.timedelta(hours=delta)
    date_since = dt.strftime(DATE_FORMAT)
    date_to = datetime.datetime.now().strftime(DATE_FORMAT)
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    while True:
        data = {
            "limit": per_request,
            "offset": offset,
            "filter": {
                "since": date_since,
                "to": date_to,
                "status": "awaiting_packaging"
            },
            "with": {
                "analytics_data": True,
                "financial_data": True
            }
        }
        resp = requests.post(url, headers=headers, json=data)
        # print(resp.text)
        try:
            res_list = json.loads(resp.text)["result"]["postings"]
        except:
            break
        if not res_list:
            break

        res.extend(res_list)
        offset += per_request
    return res


def get_transactions_moments(delta_days=5):
    """
    Dict {order_number: transaction_date}
    """
    url = "https://api-seller.ozon.ru/v3/finance/transaction/list"
    page = 1
    per_request = 100
    res = {}
    dt = datetime.datetime.now() - datetime.timedelta(days=delta_days)
    date = dt.strftime("%Y-%m-%dT%H:00:00.000Z")
    date_now = datetime.datetime.now().strftime("%Y-%m-%dT%H:00:00.000Z")
    while True:
        data = {
            "page_size": per_request,
            "page": page,
            "filter": {
                "date": {
                    "from": date,
                    "to": date_now
                },
                "transaction_type": "orders"
            }
        }
        resp = requests.post(url, headers=OZON_HEADERS, json=data)
        # print(resp.text)
        try:
            res_list = json.loads(resp.text)["result"]["operations"]
        except:
            break
        if not res_list:
            break
        # print(res_list)
        for elem in res_list:
            res[elem['posting']["posting_number"]] = elem["operation_date"].split()[0]

        page += 1
    return res


def get_transactions_moments_period(from_dt, to_dt):
    """
    Dict {order_number: transaction_date}
    """
    url = "https://api-seller.ozon.ru/v3/finance/transaction/list"
    page = 1
    per_request = 100
    res = {}
    date = from_dt.strftime("%Y-%m-%dT%H:00:00.000Z")
    date_now = to_dt.strftime("%Y-%m-%dT%H:00:00.000Z")
    while True:
        data = {
            "page_size": per_request,
            "page": page,
            "filter": {
                "date": {
                    "from": date,
                    "to": date_now
                },
                "transaction_type": "orders"
            }
        }
        resp = requests.post(url, headers=OZON_HEADERS, json=data)
        # print(resp.text)
        try:
            res_list = json.loads(resp.text)["result"]["operations"]
        except:
            break
        if not res_list:
            break
        # print(res_list)
        for elem in res_list:
            res[elem['posting']["posting_number"]] = elem["operation_date"].split()[0]

        page += 1
    return res


def get_order_transactions(posting_number):
    url = "https://api-seller.ozon.ru/v3/finance/transaction/list"
    data = {
        "page_size": 1000,
        "page": 1,
        "filter": {
            "posting_number": posting_number,
            "transaction_type": "all"
        }
    }
    OZON_HEADER = {'Client-Id': str(OZON_HEADERS['Client-Id']), 'Api-Key': OZON_HEADERS['Api-Key'],
                   'Content-Type': OZON_HEADERS['Content-Type'], 'Accept': OZON_HEADERS['Accept']}
    resp = requests.post(url, headers=OZON_HEADER, json=data)
    # print(resp.text)
    if not resp.ok:
        return {}
    try:
        res_dict = json.loads(resp.text)
    except:
        return {}
    return res_dict


def get_transactions_moments_v2(delta_days=5) -> Tuple:
    """
    Dict {order_number: (transaction_date,MarketplaceServiceItemDirectFlowLogistic,OperationMarketplaceServicePremiumCashback)}
    """
    url = "https://api-seller.ozon.ru/v3/finance/transaction/list"
    page = 1
    per_request = 100
    res = {}
    dt = datetime.datetime.now() - datetime.timedelta(days=delta_days)
    date = dt.strftime("%Y-%m-%dT%H:00:00.000Z")
    date_now = datetime.datetime.now().strftime("%Y-%m-%dT%H:00:00.000Z")
    while True:
        data = {
            "page_size": per_request,
            "page": page,
            "filter": {
                "date": {
                    "from": date,
                    "to": date_now
                },
                "transaction_type": "all"
            }
        }
        resp = requests.post(url, headers=OZON_HEADERS, json=data)
        # print(resp.text)
        try:
            res_list = json.loads(resp.text)["result"]["operations"]
        except:
            break
        if not res_list:
            break
        # print(res_list)
        for elem in res_list:
            logistics = None
            cashback = None
            moment = elem["operation_date"].split()[0]
            posting_number = elem['posting']["posting_number"]
            if elem['operation_type'] == 'OperationAgentDeliveredToCustomer':
                services = elem["services"]
                logistics = None
                for service in services:
                    if service['name'] == 'MarketplaceServiceItemDirectFlowLogistic':
                        try:
                            logistics = float(service['price'])
                        except:
                            logistics = 0
                        break
            elif elem['operation_type'] == 'OperationMarketplaceServicePremiumCashback':
                try:
                    cashback = float(elem['amount'])
                except:
                    cashback = 0
            if posting_number in res:
                if moment:
                    res[posting_number][0] = moment
                if logistics:
                    res[posting_number][1] = logistics
                if cashback:
                    res[posting_number][2] = cashback
            else:
                res[posting_number] = [moment, logistics, cashback]

        page += 1
    return res


def get_stores(headers=OZON_HEADERS):
    url = "https://api-seller.ozon.ru/v1/warehouse/list"
    resp = requests.post(url, headers=headers, json={})
    res = {}
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    if not resp.ok:
        return res
    try:
        res_list = json.loads(resp.text)['result']
    except:
        return res
    for elem in res_list:
        res[str(elem['warehouse_id'])] = elem['name']
    return res


def get_products_dict(headers=OZON_HEADERS):
    url = "https://api-seller.ozon.ru/v2/product/list"
    last_id = ''
    sum = 0
    result = {}
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    while True:
        data = {
            'limit': 1000,
            'last_id': last_id
        }
        resp = requests.post(url, headers=headers, json=data)
        if not resp.ok:
            break
        try:
            res = json.loads(resp.text)['result']
        except:
            break
        if 'items' not in res or not res['items']:
            break
        last_id = res['last_id']
        sum += len(res['items'])
        total = res['total']
        for elem in res['items']:
            result[elem['product_id']] = elem['offer_id']
        if sum >= total:
            break

    return result


def get_product_dict(product_id: int, headers=OZON_HEADERS):
    url = "https://api-seller.ozon.ru/v2/product/info"
    data = {
        "product_id": product_id,
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    if not resp.ok:
        return {}
    try:
        res = json.loads(resp.text)['result']
    except:
        return {}
    return res


def prepare_products_for_ship(products: List[Dict]):
    package_products = []
    for product in products:
        package_product = {
            "exemplar_info": [
                {
                    "is_gtd_absent": True,
                }
            ],
            "product_id": product['sku'],
            "quantity": product['quantity']
        }
        mark = product.get("mark")
        if mark:
            package_product['exemplar_info'][0]['mandatory_mark'] = mark
        package_products.append(package_product)
    return package_products


def order_status_ship(posting_number: str, package_products: List, headers=OZON_HEADERS) -> bool:
    """
    Собрать заказ 'status': 'awaiting_packaging'
    """
    url = f"https://api-seller.ozon.ru/v3/posting/fbs/ship"
    data = {
        "packages": [{
            "products": package_products
        }],
        "posting_number": posting_number
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    # print(data)
    resp = requests.post(url, headers=headers, json=data)
    # print(resp.text)
    return resp.ok


def prepare_products_for_ship_v2(products: List[Dict]):
    package_products = []
    for product in products:
        package_product = {
            "sku": product['sku'],
            "quantity": product['quantity']
        }
        mark = product.get("mark")
        if mark:
            package_product['mandatory_mark'] = [mark]
        package_products.append(package_product)
    return package_products


def order_status_ship_v2(posting_number: str, package_products: List, headers=OZON_HEADERS) -> bool:
    """
    Собрать заказ 'status': 'awaiting_packaging'
    """
    url = "https://api-seller.ozon.ru/v4/posting/fbs/ship"
    data = {
        "packages": [{
            "products": package_products
        }],
        "posting_number": posting_number,
        "with": {
            "additional_data": True
        }
    }
    # print(data)
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    print(44444, resp.text)
    return resp.ok


def order_label(posting_number: str, file_path: str, headers=OZON_HEADERS) -> bool:
    # print('file_path', file_path)
    url = f"https://api-seller.ozon.ru/v2/posting/fbs/package-label"
    data = {
        "posting_number": [
            posting_number
        ]
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    if resp.ok:
        # print(resp.content)
        # label_url = json.loads(resp.text)['content']
        # response = requests.get(label_url, headers=headers)
        res_content = resp.content
        with open(file_path, "wb") as outfile:
            outfile.write(res_content)
    else:
        print('order_label', resp.text, posting_number)
    return resp.ok


def order_status_awaiting_delivery(posting_number: str, headers=OZON_HEADERS) -> bool:
    """
    'status': 'awaiting_delivery'
    """
    url = f"https://api-seller.ozon.ru/v2/posting/fbs/awaiting-delivery"
    data = {
        "posting_number": [
            posting_number
        ]
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    try:
        return json.loads(resp.text)['result'][0]['result']
    except:
        logging.info(f"Ozon api result change status to 'awaiting-delivery' order {posting_number}")
        logging.info(resp.text)
        return False


def order_status_delivery(posting_number: str, headers=OZON_HEADERS) -> bool:
    """
    'status': 'delivery'
    """
    url = f"https://api-seller.ozon.ru/v2/fbs/posting/delivering"
    data = {
        "posting_number": [
            posting_number
        ]
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    try:
        return json.loads(resp.text)['result'][0]['result']
    except:
        logging.info(f"Ozon api result change status to 'delivering' order {posting_number}")
        logging.info(resp.text)
        return False


def order_status_last_mile(posting_number: str, headers=OZON_HEADERS) -> bool:
    """
    'status': 'last-mile'
    """
    url = f"https://api-seller.ozon.ru/v2/fbs/posting/last-mile"
    data = {
        "posting_number": [
            posting_number
        ]
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    try:
        return json.loads(resp.text)['result'][0]['result']
    except:
        logging.info(f"Ozon api result change status to 'last-mile' order {posting_number}")
        logging.info(resp.text)
        return False


def order_status_delivered(posting_number: str, headers=OZON_HEADERS) -> bool:
    """
    'status': 'delivered'
    """
    url = f"https://api-seller.ozon.ru/v2/fbs/posting/delivered"
    data = {
        "posting_number": [
            posting_number
        ]
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    try:
        return json.loads(resp.text)['result'][0]['result']
    except:
        logging.info(f"Ozon api result change status to 'delivered' order {posting_number}")
        logging.info(resp.text)
        return False


def get_fbs_order_v3(posting_number, headers=OZON_HEADERS):
    url = "https://api-seller.ozon.ru/v3/posting/fbs/get"
    data = {
        "posting_number": posting_number,
        "translit": True,
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    # headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'], 'Content-Type': headers['Content-Type'], 'Accept' : headers['Accept']}
    if not resp.ok:
        return {}
    try:
        res_dict = json.loads(resp.text)
        return res_dict
    except:
        return {}


def get_fbs_order_v4(posting_number, header):
    url = "https://api-seller.ozon.ru/v3/posting/fbs/get"
    data = {
        "posting_number": posting_number,
        "with": {
            "financial_data": True,
            "translit": True
        }
    }
    headers = {'Client-Id': str(header['Client-Id']), 'Api-Key': header['Api-Key'],
               'Content-Type': header['Content-Type'], 'Accept': header['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    # headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'], 'Content-Type': headers['Content-Type'], 'Accept' : headers['Accept']}
    if not resp.ok:
        return {}
    try:
        res_dict = json.loads(resp.text)
        return res_dict.get("result")
    except:
        return {}


def get_fbs_order_barcode(posting_number, headers=OZON_HEADERS):
    url = "https://api-seller.ozon.ru/v3/posting/fbs/get"
    data = {
        "posting_number": posting_number,
        "translit": True,
        "with": {
            "barcodes": True
        }
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    # print(resp.text)
    if not resp.ok:
        return ()
    try:
        res_dict = json.loads(resp.text)['result']
        barcodes = res_dict.get('barcodes')
        # print(barcodes)
        if barcodes:
            return (barcodes['upper_barcode'], barcodes['lower_barcode'])
    except:
        return ()
    return ()


def is_order_cansel(posting_number, headers=OZON_HEADERS):
    url = "https://api-seller.ozon.ru/v3/posting/fbs/get"
    data = {
        "posting_number": posting_number,
        "translit": True,
        "with": {
            "barcodes": True
        }
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    # print(resp.text)
    if not resp.ok:
        return False
    try:
        res_dict = json.loads(resp.text)['result']
        barcodes = res_dict.get('barcodes')
        # print(barcodes)
        if barcodes:
            return True
    except:
        return False
    return True


def get_act(sklad_id: int, headers=OZON_HEADERS):
    url = "https://api-seller.ozon.ru/v2/posting/fbs/act/create"
    data = {
        'delivery_method_id': sklad_id
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    print('get_act', resp.text)
    if not resp.ok:
        print("API error get act")
        return None
    try:
        res_dict = json.loads(resp.text)
        return res_dict['result']['id']
    except:
        print("API error load text get act")
        return None


def get_act_document_sign(sklad_id: int, type: str, headers=OZON_HEADERS):
    url = "https://api-seller.ozon.ru/v2/posting/fbs/digital/act/document-sign"
    data = {
        'delivery_method_id': sklad_id,
        'type': type
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    print('get_act', resp.text)
    if not resp.ok:
        print("API error get_act_document_sign")
        logging.warning('API get_act_document_sign not OK')
        return None
    try:
        answer = resp.json()
        result = answer['result']
        return result
    except Exception as err:
        print("API error get_act_document_sign")
        logging.error('get_act_document_sign {}'.format(err))
        return None


def get_act_today(sklad_id: int, headers=OZON_HEADERS):
    url = "https://api-seller.ozon.ru/v2/posting/fbs/act/create"
    data = {
        'delivery_method_id': sklad_id,
        "departure_date": datetime.datetime.now()
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    print('get_act', resp.text)
    if not resp.ok:
        print("API error")
        return None
    try:
        res_dict = json.loads(resp.text)
        return res_dict['result']['id']
    except:
        print("API error")
        return None


def get_delivery_methods(headers=OZON_HEADERS):
    url = "https://api-seller.ozon.ru/v1/delivery-method/list"
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json={'limit': 10})
    res = {}
    if not resp.ok:
        return res
    try:
        res = json.loads(resp.text)
    except:
        return res
    return res


def get_act_by_code(code, headers=OZON_HEADERS):
    url = "https://api-seller.ozon.ru/v2/posting/fbs/act/get-pdf"
    data = {
        "id": code
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    # print(resp.text)
    if not resp.ok:
        # print("API error")
        return None
    try:
        res_dict = json.loads(resp.text)
        return res_dict['content']
    except:
        # print("API error")
        return None


def get_act_orders(code, headers=OZON_HEADERS):
    url = "https://api-seller.ozon.ru/v2/posting/fbs/act/check-status"
    data = {
        "id": code
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    print('get_act_orders', resp.text)
    if not resp.ok:
        print("API error get_act_orders ", code, headers)
        return None
    try:
        res_dict = json.loads(resp.text)
        return res_dict['result']['added_to_act']
    except:
        # print("API error")
        return None


def get_digital_act_status(code, headers=OZON_HEADERS):  # TODO
    url = "https://api-seller.ozon.ru/v2/posting/fbs/digital/act/check-status"
    data = {
        "id": code
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    print('get_digital_act_orders', resp.text)
    if not resp.ok:
        print("API error get_digital_act_status ", code, headers)
        logging.warning('get_digital_act_status not OK', code)
        return None
    try:
        res_dict = resp.json()
        status = res_dict['status']
        return status
    except Exception as er:
        logging.error('get_digital_act_status {}'.format(er))
        print("API error get_digital_act_status")
        return None


def get_file(file_url, dir_path, headers=OZON_HEADERS):
    url = file_url
    file_name = file_url.split('/')[-1]
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.get(url, headers=headers)
    # print(resp.text)
    if not resp.ok:
        print("API error")
        return None
    try:
        with open(os.path.join(dir_path, file_name), 'wb') as f:
            f.write(resp.content)
        return file_name
    except:
        print("API error")
        return None


def get_act_by_code_v2(code, dir_path, headers=OZON_HEADERS):
    url = "https://api-seller.ozon.ru/v2/posting/fbs/act/get-pdf"
    data = {
        "id": code
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    # print(resp.text)
    if not resp.ok:
        print("API error get_act_by_code_v2")
        return None
    file_name = f"{code}.pdf"
    try:
        with open(os.path.join(dir_path, file_name), 'wb') as f:
            f.write(resp.content)
        return file_name
    except:
        # print("API error")
        return None


def get_digital_act_by_code(code, dir_path, headers=OZON_HEADERS):  # TODO
    url = "https://api-seller.ozon.ru/v2/posting/fbs/digital/act/get-pdf"
    data = {
        "id": code,
        "doc_type": "act_of_acceptance"
    }
    header = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
              'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=header, json=data)
    # print(resp.text)
    if not resp.ok:
        print("API error get_digital_act_by_code")
        return None
    file_name = f"{code}.pdf"
    try:
        with open(os.path.join(dir_path, file_name), 'wb') as f:
            f.write(resp.content)
        return file_name
    except:
        # print("API error")
        return None


def get_edo_act_by_code(code, dir_path, headers=OZON_HEADERS):
    url = "https://api-seller.ozon.ru/v2/posting/fbs/digital/act/get-pdf"
    data = {
        "id": code
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    # print(resp.text)
    if not resp.ok:
        # print("API error")
        return None
    file_name = f"edo_{code}.pdf"
    try:
        with open(os.path.join(dir_path, file_name), 'wb') as f:
            f.write(resp.content)
        return file_name
    except:
        # print("API error")
        return None


def get_fbs_order_status(posting_number, headers=OZON_HEADERS):
    url = "https://api-seller.ozon.ru/v3/posting/fbs/get"
    data = {
        "posting_number": posting_number,
        "with": {
            "analytics_data": False,
            "financial_data": False
        }
    }
    headers = {'Client-Id': str(headers['Client-Id']), 'Api-Key': headers['Api-Key'],
               'Content-Type': headers['Content-Type'], 'Accept': headers['Accept']}
    resp = requests.post(url, headers=headers, json=data)
    if not resp.ok:
        return {}
    try:
        status = json.loads(resp.text)['result']['status']
    except:
        return {}
    return status
