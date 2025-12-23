import requests
import json

import chekerPath
from classPath import Paths, Path


def getPage():
    cookies = {
        'uicult2': 'ru',
        '_ym_uid': '175252010013417501',
        '_ym_d': '1752520100',
        'did': 'jO80FASy9vR4tCEpsvTEMcHruLPRlvMdULL6agI4r0k%3D',
        '_ymab_param': 's78AwxG_kiU-YWGJJgFb1LlIDu4hbFZuk_7sf3bWpx43uRVp8-zyKMGlKeul8CMnoFgGEG6qV82tlhlfKFHTO1o_K7o',
        'wasCookieAccepted': 'true',
        '_ga_4PYZX6X847': 'GS2.1.s1752827448$o1$g0$t1752827448$j60$l0$h0',
        'ati_theme': 'default-theme',
        'amp_7d2cee': 'uB71sqJlrYEkrt70ZemYrD.NzM2NTQ5Mi4x..1j1dvrnlg.1j1e14dkk.0.0.0',
        'itemsPerPage': '10',
        '_gcl_au': '1.1.1165995094.1760621151',
        'startpage': 'atisu',
        'anoncou': 'RU',
        '_ym_isad': '1',
        '_gid': 'GA1.2.309521280.1766483476',
        '_ym_visorc': 'b',
        'auth_visit': '1',
        'anymouse_id': 'e634619d-4309-4449-9fa3-b36b43f38e39',
        'sid': '86e9f1e5dbe8404cb6733ed537163add',
        'gotoreg': 'show',
        'lastpage': 'loadsatisu',
        '_ga_Z6YM1FRK5D': 'GS2.2.s1766483476$o46$g1$t1766485023$j60$l0$h0',
        '_ga_14VPSGD0HN': 'GS2.1.s1766483475$o58$g1$t1766485826$j59$l0$h0',
        '_ga': 'GA1.2.2044529891.1752520100',
        '_dc_gtm_UA-224067-1': '1',
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'ru,en;q=0.9,en-GB;q=0.8,en-US;q=0.7',
        'content-type': 'application/json',
        'origin': 'https://loads.ati.su',
        'priority': 'u=1, i',
        'referer': 'https://loads.ati.su/',
        'sec-ch-ua': '"Not;A=Brand";v="99", "Microsoft Edge";v="139", "Chromium";v="139"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'traceparent': '00-c189a62106617228d3bbee90954f0d32-9cef210247b659a3-01',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36 Edg/139.0.0.0',
        # 'cookie': '_gcl_au=1.1.1626094567.1752814837; uicult2=ru; _ym_uid=1752814837516262017; _ym_d=1752814837; tmr_lvid=f5568e55a17593e63380c7c24a17eac7; tmr_lvidTS=1752814837470; did=SafksCkvSmPRw29K%2BKfJrPOxmmCAmSSNrrKkORasEK4%3D; wasCookieAccepted=true; _ymab_param=cYFBZft6pZ85z6qC4YfHqtA6X_FDF2L8-kszaMyn-iTyh4WK6P5iYFNC3jSZ2WYYT5s8b-NC_QhqN0j_mvxmq2KwXQY; ati_theme=default-theme; sid=529813d973234dae8322232e4cdf8bb2; itemsPerPage=100; region_id=15; startpage=atisu; anoncou=RU; _gid=GA1.2.1193623622.1755688317; _ym_isad=2; _ym_visorc=b; atisuReferrer=utm_source=header; billing_cart_updated=y; billing_cart_last=3; auth_visit=1; lastpage=loadsatisu; domain_sid=pXE9NUR_EjXRzkCBtmXfm%3A1755688660085; _ga_14VPSGD0HN=GS2.1.s1755688316$o21$g1$t1755688747$j59$l0$h0; _ga=GA1.2.554426167.1752814837; _dc_gtm_UA-224067-1=1; _ga_Z6YM1FRK5D=GS2.2.s1755688317$o17$g1$t1755688748$j60$l0$h0; tmr_detect=0%7C1755688751400',
    }

    json_data = {
        'exclude_geo_dicts': True,
        'page': 1,
        'items_per_page': 100,
        'filter': {
            'from': {
                'id': 120,
                'type': 2,
                'radius': 100,
                'exact_only': True,
            },
            'to': {
                'id': 40,
                'type': 1,
                'exact_only': True,
            },
            'dates': {
                'date_option': 'today-plus',
            },
            'weight': {
                'max': 2.5,
            },
            'length': {
                'max': 4,
            },
            'width': {
                'max': 2,
            },
            'volume': {
                'max': 15,
            },
            'truck_type': '91',
            'loading_type': '6',
            'height': {
                'max': 2,
            },
            'pallets': 5,
            'extra_params': 2049,
            'exclude_tenders': False,
            'rate': {
                'currency_id': 1,
                'rate_total': 25,
            },
            'sorting_type': 2,
        },
    }

    response = requests.post('https://loads.ati.su/webapi/v1.0/loads/search', cookies=cookies, headers=headers,
                             json=json_data)

    with open(f"data.json", 'w', encoding="utf-8") as file:
        json.dump(response.json(), file)

def getTotalElement():
    with open(f'data.json', 'r') as f:
        data = json.load(f)
    return data['totalItems']

def getData():
    getPage()
    result = Paths()
    totalElement = getTotalElement()
    for i in range(totalElement):
        with open(f'data.json', 'r') as f:
            data = json.load(f)
            a = Path(data, i, 120)
            result.add_element(a)
    return result

#print(chekerPath.cheker(getData()))

