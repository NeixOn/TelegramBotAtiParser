import get
from chekerPath import cheker

def start():
    dictCityPrice = dict()
    with open('city_price.txt',encoding="utf-8",mode = 'r') as f:
        for i in f.readlines():
            buff = i.split(' ')
            city, price = buff[0], int(buff[1])
            dictCityPrice[city] = price
    #print(get.getData())
    result = cheker(get.getData(), dictCityPrice)
    print('_' * 10, '\n', result, '\n', '_' * 10)
    return result