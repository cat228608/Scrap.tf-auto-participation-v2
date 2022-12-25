import requests
from lxml import etree
import json
import time

tg_id = "169412"
token_bot = "5926702328:AAFe-EMcopoF0nQs-I"
text_bot = "У вас новое уведомление на сайте scrap.tf"

cookies = {
    '_pbjs_userid_consent_data': '3524770',
    '_ga': 'GA1.1.1594540899.1671731491',
    'scr_session': 'bG9naW5fcmVkaXJlY3R8czoxNzoiaHR0cHM6Ly9zYY0MDdlNDM1ZWNkNTE5MDM2Y2UyM2U2NDM0MmVjMzliNWQyNTZhYmVjNGY5Ijs2NzBmYmM4YWFkMWRjODllOTdkZWNjYmIzMWIyYTlkOTBhMDlkMDcxNGQ1M2ZhZDE0NGIyNDg1ZjhiNDZiN2Y0MzQxNmE3NWUyZjdjOWUyNzdkNWUwMmY5MjQ0ZTNjMWFiNTdmZjkwNTAxZWVlYjI2Njc1NTYxZDdiNDNhMzdjYg%3D%3D',
    '_ga_CRS9KN52XK': 'GS1.1.167132711.0.0.0',
    '__cf_bm': '1W5LVvQDs4NOD9dyG3Ou23k7bCvni3OfcL5ISvEDiHk-1671732737-0Y41NDY/rwR0golm2D71vHbElc1y+nXm10Bkhz4/Q3GaSz6eHLonjTjrjv3gC2ivfcJMq99VTXkFIKV4z5CE8XOTnEEtSPXTK83T3QsV2WW8QpXDw='
}

headers = {
    'authority': 'scrap.tf',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    'referer': 'https://scrap.tf/raffles',
    'sec-ch-ua': '"Chromium";v="108", "Opera";v="94", "Not)A;Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.9 Safari/537.36',
}
def parsing():
    print("Начинаю парсинг...")
    pars_req = requests.get(f'https://scrap.tf/raffles', cookies=cookies, headers=headers)
    html = pars_req.text
    htmlparser = etree.HTMLParser()
    tree = etree.XML(html,htmlparser)
    m = 1
    my_list = []
    try:
        check_win = tree.xpath('//*[@id="notices-menu"]/a/span/text()')[0]
        if check_win != '0':
            requests.post(f"https://api.telegram.org/bot{token_bot}/sendMessage", data = {'chat_id': f'{tg_id}', 'text': f'{text_bot}'})
    except:
        print("Данные для бота неверны!")
    while True:
        try:
            pars = tree.xpath(f'//html/body/div[4]/div[2]/div[3]/div[1]/div[{int(m)}]/div[1]/div[1]/a/@href')[0]
            my_list.append(pars)
            m = m + 1
            continue
        except:
            break
            
    z = 0
    while True:
        try:
            result = enter_raffel(my_list[z])
            print(f"Результат: {result}")
            z = z + 1
            time.sleep(3)
        except Exception as e:
            print("Я закончил. Ухожу спать на 15 минут")
            if z == len(my_list):
                time.sleep(900)
                break
    parsing()

def enter_raffel(code):
    try:
        req = requests.get(f'https://scrap.tf{code}', cookies=cookies, headers=headers)
        html = req.text
        htmlparser = etree.HTMLParser()
        tree = etree.XML(html,htmlparser)
        token = tree.xpath('//html/body/script[16]/text()')[0]
        token_two = tree.xpath('//*[@id="main-container"]/div/div[2]/div[5]/div[2]/button[2]/@onclick')[0]
        token_two_revers = token_two.split(", ")[1] 
        token_two_revers_two = token_two_revers.replace("'", "") #csrf
        token_revers = token.split('ScrapTF.User.Hash = "')[1]
        token_revers_two = token_revers.split('";')[0] #hash
        data = {
        'raffle': f'{code.split("/")[2]}',
        'captcha': '',
        'hash': f'{token_two_revers_two}',
        'flag': 'false',
        'csrf': f'{token_revers_two}',
        }
        response = requests.post('https://scrap.tf/ajax/viewraffle/EnterRaffle', cookies=cookies, headers=headers, data=data)
        result = json.loads(response.text)
        return f"https://scrap.tf{code} - {result['message']}"
    except Exception as er:
        return f"Ошибка обработки - {er}"
        
parsing()
#c = input("Укажите код: ")
#enter_raffel(c)