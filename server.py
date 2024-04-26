from gevent import monkey

monkey.patch_all()

import json
import random
import string

import requests
from flask import Flask, request
from gevent.pywsgi import WSGIServer
import pytz
from datetime import datetime, timedelta
from cred import *
# from proxy import proxy_onon

import urllib3

urllib3.disable_warnings()


def write_json(smth_json):
    try:
        with open(DIR_EXCEL + '/test_json.json', 'w') as file:
            json.dump(smth_json, file)
    except:
        with open('test_json.json', 'w') as file:
            json.dump(smth_json, file)


def write_smth_date():
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    try:
        f = open(DIR_EXCEL + '/test_txt.txt', 'w')
        f.write(str(time) + '\n')
        f.close()
    except:
        f = open('test_txt.txt', 'w')
        f.write(str(time) + '\n')
        f.close()


def write_smth(smth):
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    try:
        f = open(DIR_EXCEL + '/no_test.txt', 'a')
        f.write(str(time) + str(smth) + '\n')
        f.close()
    except:
        f = open('no_test.txt', 'a')
        f.write(str(time) + str(smth) + '\n')
        f.close()


write_smth(' start ')



def token_generator(size=10, chars=string.digits):  # string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def reverse_time(time):
    t = time.split('-')
    t.reverse()
    result = '-'.join(t)

    return result


def proxy_time_1():
    dt = datetime.now().date() + timedelta(days=1)
    d = str(dt).split('-')
    d.reverse()
    pt = '-'.join(d)

    return pt





def data_summary():
    with open(DIR_EXCEL + "/orders.json", 'r') as file:
        data_orders = json.load(file)

    return data_orders




def proxy_time():
    dt = datetime.now().date() + timedelta(days=2)
    d = str(dt).split('-')
    d.reverse()
    pt = '-'.join(d)

    return pt



async def send_post(data):
    answer = requests.post(url_address=None, data=json.dumps(data),
                           headers=ANY_OZON_HEADERS, verify=False)
    write_smth(answer)
    write_smth(data)
    # result = answer.text
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    print('answer1', str(time), answer, data)
    # return result


app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def bay_bay():
    response = app.response_class(
        status=403
    )
    return response


common_comfirm_response = {"result": True}
common_error = {'error': {
    "code": "ERROR_UNKNOWN",
    "message": "Неизвестный метод",
    "details": None}}
common_product_error = {'error': {
    "code": "ERROR_UNKNOWN",
    "message": "Product not found",
    "details": None}}


@app.route('/test', methods=['GET'])
def test():
    return "OK"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # #Debug/Development
    ##run app in debug mode on port 5000
    # app.run(debug=True, host='0.0.0.0', port=5000)
    # Production
    http_server = WSGIServer(('', 7000), app)
    http_server.serve_forever()
