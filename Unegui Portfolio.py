from bs4 import BeautifulSoup
import requests
import codecs
import csv
from datetime import date

rooms = str(input('Enter room qty:'))
page_number_finder = ""
page_number = 0
url = f'https://www.unegui.mn/l-hdlh/l-hdlh-zarna/oron-suuts-zarna/{rooms}-r/ulan-bator/'
header = ['Шал:', 'Тагт:', 'Гараж:', 'Цонх:', 'Хаалга:', 'Цонхнытоо:', 'Барилгынявц', 'Ашиглалтандорсонон:', 'Барилгындавхар:', 'Талбай:', 'Хэдэндавхарт:', 'Лизингээравахболомж:', 'Дүүрэг:', 'Байршил:', 'Үзсэн:', 'Scraped_date:', 'Link:', 'Үнэ:', 'Өрөөний Тоо:', 'Зарын гарчиг:', 'Зарын Тайлбар:']
key_list = [0 for i in range(len(header))]
csv_list = []



def key_finder(key, index):
    for i in span_list:
        if str(key) in i:
            key_list[index] = (i.split(':')[1])
    if type(key_list[int(index)]) != str:
        key_list[int(index)] = 0



url_uruu = requests.get(url)
soup = BeautifulSoup(url_uruu.content, 'html.parser')


try:
    page_number_finder = soup.find('ul', class_='number-list').text.rstrip('\n').replace('\n', ',')
    page_number += int(page_number_finder[-2:].replace(',', ''))
except:
    pass
href_list = [a['href'] for a in soup.find_all('a', href=True)]
href_list_1 = [x.replace('/', '') for x in href_list]
for i in href_list_1:
    if len(i) == 0:
        href_list_1.remove(i)
main_list = []
for i in href_list_1:
    if i[0:3] == 'adv' and '_' in i:
        main_list.append(i[3:])

for x in range(2, page_number+1):
    page_url = f'https://www.unegui.mn/l-hdlh/l-hdlh-zarna/oron-suuts-zarna/{rooms}-r/ulan-bator/?page={x}'
    url_page = requests.get(page_url)
    soup_pages = BeautifulSoup(url_page.content, 'html.parser')
    href_list = [a['href'] for a in soup_pages.find_all('a', href=True)]
    href_list_1 = [x.replace('/', '') for x in href_list]
    for i in href_list_1:
        if len(i) == 0:
            href_list_1.remove(i)
    new_list = [i[3:] for i in href_list_1 if (i[0:3] == 'adv' and '_' in i)]
    main_list += new_list
main_list = list(set(main_list))
for i in main_list:
    html_text = requests.get(f'https://www.unegui.mn/adv/{i}/')
    soup = BeautifulSoup(html_text.content, 'html.parser')
    soup_all = soup.find('div', class_='announcement-characteristics clearfix').find_all('li')
    span_list = [i.text.replace('\n', '').replace(' ', '') for i in soup_all]
    # 'Шал'
    key_finder('Шал:', 0)
    # 'Тагт'
    key_finder('Тагт:', 1)
    # 'Гараж:'
    key_finder('Гараж:', 2)
    # 'Цонх:'
    key_finder('Цонх:', 3)
    # 'Хаалга:'
    key_finder('Хаалга:', 4)
    # 'Цонхнытоо:'
    key_finder('Цонхнытоо:', 5)
    # 'Барилгынявц'
    key_finder('Барилгынявц', 6)
    # 'Ашиглалтандорсонон'
    key_finder('Ашиглалтандорсонон:', 7)
    # 'Барилгындавхар:'
    key_finder('Барилгындавхар:', 8)
    # 'Талбай:'
    key_finder('Талбай:', 9)
    # 'Хэдэндавхарт:'
    key_finder('Хэдэндавхарт:', 10)
    # 'Лизингээравахболомж:'
    key_finder('Лизингээравахболомж:', 11)
    # 'Дүүрэг:'
    key_list[12] = soup.find('span', itemprop="address").text.split('—')[0]
    # 'Байршил:'
    key_list[13] = soup.find('span', itemprop="address").text.split('—')[1]
    # 'Үзсэн'
    key_list[14] = soup.find('span', class_='counter-views').text.rstrip('\n').strip(' ').replace(' ', '')
    # 'Scraped_date'
    key_list[15] = date.today().strftime("%d/%m/%Y")
    # 'link'
    key_list[16] = f'https://www.unegui.mn/adv/{i}/'
    'Үнэ'
    key_list[17] = soup.find('div', class_='announcement-price__cost').text.rstrip('\n').strip(' ').replace(' ', '')[3:]
    # 'ӨрөөнийТоо'
    key_list[18] = soup.find('div', class_='wrap js-single-item__location').find_all('span')[-1].text
    #Зарыг гарчиг
    key_list[19] = soup.find('h1', class_='title-announcement').text.rstrip('\n').strip(' ').replace('\n', '')
    # 'Зарын тайлбар'
    key_list[20] = soup.find('div', class_='announcement-description').text.rstrip('\n').strip(' ').replace('\n', '')
    sub_dic = dict(zip(header, key_list))
    csv_list.append(sub_dic)
#
with codecs.open(f'UNEGUI-{rooms} uruu.csv', 'w', 'utf-8-sig') as f:
    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()
    writer.writerows(csv_list)



