import oson
from cred import DIR_EXCEL
# from oson import *
import pandas as pd
# pip install xlwt
# pip install openpyxl

def writer():
    pre_data = oson.report_finance_realisation().get('result').get('rows')
    data = {i.get('row_number'): i for i in pre_data}
    path = DIR_EXCEL + '/super_file.xlsx'
    # df = pd.DataFrame(data, columns=['No'
    #     'Артикул', 'Ozon SKU ID', 'Название', 'Цена до скидки, руб.',
    #     'цена для покупателя', 'Ваша цена', 'Скидка, %', 'Скидка, руб.',
    #     'Цена с учетом акции или стратегии, руб.', '% комиссии МП (вознаграждение) FBO',
    #     'комиссии МП (вознаграждение) FBO', 'экваринг FBO', 'логистика FBO',
    #     'последняя миля FBO', 'возврат или отмена FBO',
    #     '% комиссии МП (вознаграждение) FBS', 'комиссии МП (вознаграждение) FBS',
    #     'экваринг FBS', 'обработка отправления FBS', 'логистика FBS', 'последняя миля FBS',
    #     'возврат или отмена FBS', 'хранение', 'услуги, реклама', 'СПП',
    #     'дата поступления товара', 'кол-во на складе ozone', 'кол-во на складе FBS'])
    df = pd.DataFrame.from_dict(data, orient='index')
    df.to_excel(path, index=False)


def reader(file):
    df = pd.read_excel(file)
    for row in df.values:
        print(*row, sep="', '")


# reader('api затрат на МП_v2-2.xlsx')

# writer()