import pytz
import requests
from cred import *
import datetime

print(datetime.date.today() - datetime.timedelta(days=7))

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


def get_advertising_report(time_delta=7):
    '''
    :param date_to:
    :return:
    [{
    "updNum": 0,
    "updTime": "2023-07-31T12:12:54.060536+03:00",
    "updSum": 24,
    "advertId": 3355881,
    "campName": "лук лучок",
    "advertType": 6,
    "paymentType": "Баланс",
    "advertStatus": 9
    }]
    '''
    date_to = datetime.date.today()
    date_from = date_to - datetime.timedelta(days=time_delta)
    params = {
        "from": date_from,
        "to": date_to
    }
    url = 'https://advert-api.wb.ru/adv/v1/upd'
    answer = requests.get(url=url, headers=wb_adv_token, params=params)
    data = answer.json()

    return data



