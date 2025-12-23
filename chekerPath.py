from geopy.geocoders import Nominatim
from geopy.distance import geodesic


def get_distance_geopy(city1, city2):
    geolocator = Nominatim(user_agent="distance_calculator")

    location1 = geolocator.geocode(city1)
    location2 = geolocator.geocode(city2)

    if not location1 or not location2:
        return None

    coords1 = (location1.latitude, location1.longitude)
    coords2 = (location2.latitude, location2.longitude)

    return int(geodesic(coords1, coords2).km)

def cheker(Paths, checkerDict):
    result = []

    for i in Paths:
        #print(i.cityTo())
        print(f"Проверка на город: {i.cityTo().split(' ')[0]}")
        if(i.cityTo().split(' ')[0] in checkerDict.keys()):
            print(f'Предлагаемая цена > Нужная цена {i.getPriceNDS()} > {checkerDict[i.cityTo().split(' ')[0]]}', )
            if(i.getPriceNDS() > checkerDict[i.cityTo().split(' ')[0]] and  i.getnp() < 5):
                result.append(i)
        else:
            # Здесь должно быть добавленее неизвестного нп в файл city_price.txt и его цены
            checkerDict[i.cityTo().split(' ')[0]] = appendCityPrice(i.cityTo().split(' ')[0])
            if (i.getPriceNDS() > checkerDict[i.cityTo().split(' ')[0]] and i.getnp() < 5):
                result.append(i)

    return result


def appendCityPrice(city):
    listDistance = []
    counter = 0
    with open('baseCity.txt',encoding='utf-8', mode='r') as f:
        for i in f.readlines():
            buff = i.split(' ')
            listDistance.append(buff)
            print(city, buff[0])
            listDistance[counter].append(get_distance_geopy(city, buff[0]))
            counter += 1
    need = min(listDistance, key=lambda x: x[2])
    print(need)
    file = open('city_price.txt',encoding='utf-8',mode='a')
    file.write(f'{city} {need[1]}')
    file.close()
    file = open('debug.txt', encoding='utf-8', mode='a')
    file.write(f'{city} {need[2]}\n')
    file.close()
    return int(need[1])


#print(get_distance_geopy("горячий-ключ", 'пятигорская'))