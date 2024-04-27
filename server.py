from gevent import monkey

monkey.patch_all()

import json
import random
import string

import requests
from flask import Flask, request, flash, redirect, url_for, render_template, send_from_directory
from gevent.pywsgi import WSGIServer
import pytz
from datetime import datetime, timedelta
from cred import *
# from proxy import proxy_onon

import urllib3

urllib3.disable_warnings()

now = datetime.strftime(datetime.now(), "%d-%h-%Y_%H:%M:%S")
print(now)


def write_keys(smth_json, market):
    now = datetime.strftime(datetime.now(), "%d-%h-%Y_%H:%M:%S")
    with open(DIR_CRED + f'/{market}_{now}.json', 'w') as file:
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


def write_smth_data(smth):
    time = datetime.now(pytz.timezone("Africa/Nairobi")).isoformat()
    f = open(DIR_CRED + '/no_test.txt', 'a')
    f.write(str(time) + str(smth) + '\n')
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


app = Flask(__name__,
            template_folder='templates/')
app.secret_key = import_key


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

@app.route('/index', methods=['get', 'post'])
def index():
    if request.method == 'POST':
        data = request.form.to_dict()
        id  = data.get('id')
        key = data.get('key')
        market = data.get('market')
        ip = request.headers.get('X-Forwarded-For')
        data['ip'] = ip
        time = datetime.strftime(datetime.now(), "%Y-%m-%d")
        if market == 'wb' and key:
            url = ''
            headers = {
                "Authorization": key
            }

            date_from = {
                "dateFrom":time
            }
            answer = requests.get(url=url, headers=headers, params=date_from)
            if answer.ok:
                name = f'super-file_{time}.xlsx'
                write_keys(data, market)
                flash(f'Данные удачно сохранены. Запущено формирование отчетов. '
                      f'\n Файл будет доступен по адресу {request.url}{name}', 'success')
            else:
                write_smth_data(data)
                flash('Данные некорректны. Проверьте правильность введенных данных', 'error')

        if market == "oson" and id and key:
                headers = {
                    "Client-Id": id,
                    "Api-Key": key
                }

                url = 'https://api-seller.ozon.ru/v1/warehouse/list'
                answer = requests.post(url=url, headers=headers)
                if answer.ok:
                    write_keys(data, market)
                    name = f'super-file_{time}.xlsx'
                    flash(f'Данные удачно сохранены. Запущено формирование отчетов. '
                          f'\n Файл будет доступен по адресу {request.url}{name}', 'success')
                else:
                    write_smth_data(data)
                    flash('Данные некорректны. Проверьте правильность введенных данных', 'error')
        # print(222222, data, request.url)
        return redirect(request.url)

    return render_template('index.html')

@app.route('/test', methods=['GET'])
def test():
    return "OK"


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    # #Debug/Development
    ##run app in debug mode on port 5000
    # app.run(debug=True, host='0.0.0.0', port=5000)
    # Production
    http_server = WSGIServer(('', 7700), app)
    http_server.serve_forever()
