from tabulate import tabulate
import math
from itertools import combinations


radius = 50

####Параметры машины:
maxVolume = 12
maxLength = 4
maxWidth = 1.75
maxHeight = 1.95
maxWeight = 2.5
maxPogruzWidth = 1.5
maxPogruzHeight = 1.7
maxPalletCount = 5
####

def summ(sublist):
    lenSublist = len(sublist)
    if lenSublist == 0:
        return
    else:
        summa = sublist[0]
        for i in range(1, lenSublist):
            summa += sublist[i]
    return summa




class Path:
    def __init__(self, dataJson = 'no_data', number = 0, Area = 0):
        self.listKey = ['distance' , 'from', 'lat1', 'lon1', 'firstDate', 'lastDate', 'to', 'lat2', 'lon2', 'volume', 'weight', 'diameter', 'width', 'length', 'height', 'priceNDS', 'idFrom', 'idTo', 'idArea', 'phone']
        self.dataJson = dataJson
        self.number = number
        self.Area = Area
        if(dataJson == 'no_data'):
            self.dataWay = {}
            self.dataWay['volume'] = 0
            self.dataWay['weight'] = 0
            self.dataWay['diameter'] = 0
            self.dataWay['width'] = 0
            self.dataWay['length'] = 0
            self.dataWay['height'] = 0
        self.dataWay = {}
        self.extraLoadings = False
        if (len(dataJson['loads']) == 0 or number >= len(dataJson['loads'])):
            dataWay = []
        else:
            #extraLoadings
            loads = dataJson['loads'][number]
            self.dataWay['loadNumber'] = loads['loadNumber']
            self.dataWay['id'] = loads['id']
            self.dataWay['distance'] = loads['route'].get('distance')
            self.dataWay['from'] = loads['loading']['location'].get('city')
            self.dataWay['lat1'] = loads['loading']['location'].get('lat')
            self.dataWay['lon1'] = loads['loading']['location'].get('lon')
            self.dataWay['firstDate'] = loads['loading'].get('firstDate')
            self.dataWay['lastDate'] = loads['loading'].get('lastDate')
            self.dataWay['to'] = loads['unloading']['location'].get('city')
            self.dataWay['lat2'] = loads['unloading']['location'].get('lat')
            self.dataWay['lon2'] = loads['unloading']['location'].get('lon')
            if(loads['unloading'].get("extraLoadings")):
                self.extraLoadings = True
            self.dataWay['volume'] = float(loads['load'].get('volume', 0))  # объём
            self.dataWay['weight'] = float(loads['load'].get('weight', 0))  # Вес
            self.dataWay['diameter'] = float(loads['load'].get('diameter', 0))  # Диаметр
            self.dataWay['width'] = float(loads['load'].get('width', 0))  # Ширина
            self.dataWay['length'] = float(loads['load'].get('length', 0))  # Длина
            self.dataWay['height'] = float(loads['load'].get('height', 0))  # Высота
            self.dataWay['palletCount'] = float(loads['load'].get('palletCount', 0))  # Количество палетов
            self.dataWay['priceNDS'] = loads['rate'].get('priceNoNds', 0)  # цена
            self.dataWay['idFrom'] = loads['loading']['location'].get('geoCode')[2:]
            try:
                self.dataWay['idTo'] = loads['unloading']['location'].get('geoCode')[2:]
            except:
                self.dataWay['idTo'] = 'Error'
            self.dataWay['idArea'] = Area
            if loads.get('firm'):
                self.dataWay['phone'] = loads['firm']['contacts'][0]['phones'][0].get('number')
                self.dataWay['np'] = loads['firm'].get('unfairPartner', 0)
            else:
                self.dataWay['phone'] = 'Нет номера'


    def __str__(self):
        return (
            f"{self.dataWay.get('from', 'N/A')} -> {self.dataWay.get('to', 'N/A')} | "
            f"{self.dataWay.get('distance', 0)} км | "
            f"Цена: {self.dataWay.get('priceNDS', 0)} руб"
            f'https://loads.ati.su/loadinfo/{self.dataWay['id']}?utm_source=site'
            f'Телефон: {self.dataWay.get('phone')}'
        )

    def __repr__(self):
        return f"{self.dataWay.get('from', 'N/A')}->{self.dataWay.get('to', 'N/A')}>"

    def __add__(self, other):
        newPath = Path(self.dataJson, self.number, self.Area)
        newPath.setVolume(self.volume() + other.volume())
        newPath.setWeight(self.weight() + other.weight())
        newPath.setPriceNDS(self.priceNDS() + other.priceNDS())
        newPath.setPalletCount(self.palletCount() + other.palletCount())

        return newPath

    def __eq__(self, other):
        result = 0
        if(self.dataWay['loadNumber'] == other.dataWay['loadNumber']):
            return True
        for key in self.listKey:
            result += self.dataWay[key] == other.dataWay[key]
        return result == len(self.listKey)

    def checkSize(self):
        if(self.volume() > maxVolume or self.length() > maxLength or self.width() > maxWidth or self.height() > maxHeight or self.weight() > maxWeight or self.palletCount() > maxPalletCount):
            return False
        elif(self.volume() == 0 and self.length() == 0 and self.width() == 0 and self.height() == 0 and self.weight() == 0):
            return False
        else:
            return True

    def loadNumber(self):
        return self.dataWay['loadNumber']

    def palletCount(self):
        return self.dataWay['palletCount']

    def setPalletCount(self, value):
        self.dataWay['palletCount'] = value

    def setVolume(self, value):
        self.dataWay['volume'] = value

    def setLength(self, value):
        self.dataWay['length'] = value

    def setWidth(self, value):
        self.dataWay['width'] = value

    def setHeight(self, value):
        self.dataWay['height'] = value

    def setWeight(self, value):
        self.dataWay['weight'] = value

    def setPriceNDS(self, value):
        self.dataWay['priceNDS'] = value

    def getVolume(self):
        return self.volume

    def getPhone(self):
        return self.dataWay['phone']

    def getPriceNDS(self):
        return self.dataWay['priceNDS']

    def getLength(self):
        return self.length

    def getId(self):
        return self.dataWay['id']

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getWeight(self):
        return self.weight

    def cityFrom(self):
        return self.dataWay['from']

    def cityTo(self):
        return self.dataWay['to']

    def distance(self):
        return self.dataWay['distance']

    def ifFrom(self):
        return self.dataWay['ifFrom']

    def idTo(self):
        #print(self.dataWay['idTo'])
        return self.dataWay['idTo']

    def ExtraLoadings(self):
        return self.extraLoadings

    def idArea(self):
        return self.dataWay['idArea']

    def lat1(self):
        return self.dataWay['lat1']
    def lat2(self):
        return self.dataWay['lat2']
    def lon1(self):
        return self.dataWay['lon1']
    def lon2(self):
        return self.dataWay['lon2']
    def getnp(self):
        return self.dataWay['np']

    def volume(self):
        return self.dataWay['volume']

    def length(self):
        return self.dataWay['length']
    def width(self):
        return self.dataWay['width']
    def height(self):
        return self.dataWay['height']
    def weight(self):
        return self.dataWay['weight']
    def priceNDS(self):
        return self.dataWay['priceNDS']


class Paths:
    def __init__(self):
        self.listDataWay = []

    def __str__(self):
        if not self.listDataWay:
            return "Нет данных для отображения"
        result = ''
        for i in self.listDataWay:
            result += f'{i}'
        return result

    def add_element(self, a):
        if(a.ExtraLoadings()):
            return
        self.listDataWay.append(a)

        # Преобразуем каждый Path в его строковое представление
        paths_str = [str(path) for path in self.listDataWay]
        return "\n".join(paths_str)

    def print_table(self):
        """Альтернативный метод для красивого табличного вывода"""
        if not self.listDataWay:
            print("Нет данных для отображения")
            return

        headers = ["№", "Откуда", "Куда", "Расстояние", "Цена", "ID от", "ID до", "Особенности", "idArea"]
        table_data = []

        for idx, path in enumerate(self.listDataWay, 1):
            table_data.append([
                idx,
                path.dataWay.get('from', 'N/A'),
                path.dataWay.get('to', 'N/A'),
                f"{path.dataWay.get('distance', 0)} км",
                f"{path.dataWay.get('priceNDS', 0)} руб",
                path.dataWay.get('idFrom', 'N/A'),
                path.dataWay.get('idTo', 'N/A'),
                "Несколько" if path.extraLoadings else "Одна",
                path.dataWay.get('idArea', "N/A")
            ])

        print(tabulate(table_data, headers=headers, tablefmt="grid"))

    def __add__(self, other):
        self.listDataWay += other.listDataWay
        return self

    def __len__(self):
        return len(self.listDataWay)

    def __iter__(self):
        """Позволяет итерироваться по путям"""
        return iter(self.listDataWay)

    def __getitem__(self, index):
        """Доступ к путям по индексу"""
        return self.listDataWay[index]

    def removeRepeat(self):
        newList = []
        for i in self.listDataWay:
            #if(not (i in newList) and i.palletCount() < maxPalletCount):
            if(not (i in newList)):
                newList.append(i)
        return newList

    def getListDataWay(self):
        return self.listDataWay

    def analysis(self):
        #self.print_table()
        self.listDataWay = self.removeRepeat()
        #self.print_table()
        readyPaths = []
        result = []
        needPaths = []
        lenPaths = len(self)
        for i in range(lenPaths):
            result.append([self[i]])
            for j in range(i+1, lenPaths):
                # туда
                #print(self[i].cityTo(), self[j].cityTo(), " = ", self.haversine(self[i].lat2(), self[i].lon2(), self[j].lat2(), self[j].lon2()), self.haversine(self[i].lat2(), self[i].lon2(), self[j].lat2(), self[j].lon2()) < radius)
                if(self[i].idArea() == self[j].idArea() and self.haversine(self[i].lat2(), self[i].lon2(), self[j].lat2(), self[j].lon2()) < radius):
                    result[i].append(self[j])
                #
            for j in range(i + 1, lenPaths):
                # оттуда
                if(self[i].idTo() == self[j].idArea()):
                    result[i].append(self[j])
        lenFirstResult = len(result)
        countIter = 0
        for i in range(lenFirstResult):
            similarPathFrom = []
            similarPathTo = []
            for j in result[i]:
                if(result[i][0].idArea() == j.idArea()):
                    similarPathFrom.append(j)
                else:
                    similarPathTo.append(j)
            lenSimilarFromPaths = len(similarPathFrom)
            lenSimilarToPaths = len(similarPathTo)
            #print(similarPathFrom)
            needPaths.append(find_valid_sublists(similarPathFrom))
            needPaths.append(find_valid_sublists(similarPathTo))
            countIter += 1
            #print(countIter)
            for gen1, gen2 in zip(needPaths[i * 2], needPaths[i * 2 + 1]):
                readyPaths.append(list(gen1) + list(gen2))
        return readyPaths

    def printAnalysis(self, result):
        for i in result:
            for j in i:
                print(j, end=" ")
            print('')

    def haversine(self, lat1, lon1, lat2, lon2):
        """
        Вычисляет расстояние между двумя точками на Земле по формуле Хаверсина
        :param lat1: Широта первой точки в градусах
        :param lon1: Долгота первой точки в градусах
        :param lat2: Широта второй точки в градусах
        :param lon2: Долгота второй точки в градусах
        :return: Расстояние между точками в километрах
        """
        lat1 = float(lat1)
        lon1 = float(lon1)
        lat2 = float(lat2)
        lon2 = float(lon2)
        # Радиус Земли в километрах
        R = 6371.0

        # Преобразование градусов в радианы
        lat1_rad = math.radians(lat1)
        lon1_rad = math.radians(lon1)
        lat2_rad = math.radians(lat2)
        lon2_rad = math.radians(lon2)

        # Разница между координатами
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad

        # Формула Хаверсина
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

        distance = R * c
        return distance


class SizeGruz:

    def __init__(self, path):
        self.volume = path.volume()  # Объем
        self.length = path.length()  # Длина
        self.width = path.width()  # Ширина
        self.height = path.height()  # высота
        self.weight = path.weight()  # Вес
        self.path = path

    def __add__(self, other):
        a = SizeGruz(self.path)
        a.setVolume(self.volume + other.volume)
        a.setWeight(self.weight + other.weight)

        return a
    def __str__(self):
        return f'{self.volume}, {self.length}, {self.width}, {self.height}, {self.weight}'

    def checkSize(self):
        if(self.volume > maxVolume or self.length > maxLength or self.width > maxWidth or self.height > maxHeight or self.weight > maxWeight):
            return False
        elif(self.volume == 0 and self.length == 0 and self.width == 0 and self.height == 0 and self.weight == 0):
            return False
        else:
            return True
    def setVolume(self, value):
        self.volume = value
        return self.volume
    def setLength(self, value):
        self.length = value
    def setWidth(self, value):
        self.width = value
    def setHeight(self, value):
        self.height = value
    def setWeight(self, value):
        self.weight = value

    def getVolume(self):
        return self.volume
    def getLength(self):
        return self.length
    def getWidth(self):
        return self.width
    def getHeight(self):
        return self.height
    def getWeight(self):
        return self.weight



def find_valid_sublists(lst, min_length=1, max_length=None):
    """
    Генерирует все подсписки, удовлетворяющие условиям:
    - сумма элементов < maxValue
    - длина между min_length и max_length

    :param lst: исходный список
    :param maxValue: максимальная сумма
    :param min_length: минимальная длина подсписка (по умолчанию 1)
    :param max_length: максимальная длина подсписка (по умолчанию длина lst)
    :return: генератор подсписков
    """
    if max_length is None:
        max_length = len(lst)

    for length in range(min_length, max_length + 1):
        for sublist in combinations(lst, length):
            #print("sublist = ", sublist)
            if(sublist == None):
                continue
            #print('summ = ', summ(sublist))
            if summ(sublist).checkSize():
                yield list(sublist)

'''dataWay['distance'] = loads['route'].get('distance')
dataWay['from'] = loads['loading']['location'].get('city')
dataWay['firstDate'] = loads['loading'].get('firstDate')
dataWay['lastDate'] = loads['loading'].get('lastDate')
dataWay['to'] = loads['unloading']['location'].get('city')
dataWay['volume'] = loads['load'].get('volume')  # объём
dataWay['weight'] = loads['load'].get('weight')  # Вес
dataWay['diameter'] = loads['load'].get('diameter')  # Диаметр
dataWay['width'] = loads['load'].get('width')  # Ширина
dataWay['length'] = loads['load'].get('length')  # Длина
dataWay['height'] = loads['load'].get('height')  # Высота
dataWay['priceNDS'] = loads['rate'].get('priceNds')  # цена'''