from bs4 import BeautifulSoup # Cуп.
import requests # Помогает получить файл со сслыки.
import json # Это формат файла, который удобен для записи данных, к примеру, словарей (стандартный модуль)
import time
import random
import os

# Получаем файл с html кодом страницы. 
# url = 'https://health-diet.ru/table_calorie/?utm_source=leftMenu&utm_medium=table_calorie'
headers = {
    'Accept': '*/*',
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 OPR/73.0.3856.415'
}
# req = requests.get(url, headers= headers)
# src = req.text

# with open('sage/parsing/parsing.html','w',encoding='utf-8') as file:
#     file.write(src)


# Получаем файл.json с разделами и ссылками на них
with open('sage/parsing/parsing.html',encoding='utf-8') as file:
    src = file.read()

soup = BeautifulSoup(src, 'lxml')

# all_products_hrefs = soup.find_all(class_='mzr-tc-group-item-href')
# all_categories_dict = {}
# for item in all_products_hrefs:
#     item_text = item.text
#     item_href = 'https://health-diet.ru' + item.get('href')
#     all_categories_dict[item_text] = item_href

# with open('sage/parsing/parsing.json','w',encoding='utf-8') as file:
#     json.dump(all_categories_dict, file, indent= 3, ensure_ascii= False)


# Получаем файлы.html с кодами страниц разделов и вынимаем нужную для нас инфу: продукт, его калорийность и пищевую ценность.
with open('sage/parsing/parsing.json',encoding='utf-8') as file:
    all_categories = json.load(file)

count = 0
how_many = int(len(all_categories)) - 1
sings = [' ','-',"'",',','/','"','*','|','<','>','?',':',]
all_products = {}


# начинаем проход по каждой категории
# for category_name,category_href in all_categories.items():
for category_name in all_categories:

    # делаем правельные названия файлов
    for sing in sings:
        if sing in category_name:
            category_name = category_name.replace(sing,'_')

    # получаем файл с кодом станицы 
    # req = requests.get(url= category_href, headers= headers)
    # src = req.text

    # with open(f'sage/parsing/data/{count}_{category_name}.html','w',encoding='utf-8') as file:
    #     file.write(src)
    
    # Варим суп. 
    with open(f'sage/parsing/data/{count}_{category_name}.html','r',encoding='utf-8') as file:
        src = file.read()
        
    soup = BeautifulSoup(src,'lxml')

    # проверка страницы на пустоту
    prov = soup.find(class_='uk-alert-danger') # этот класс есть только на пустой странице 
    if prov is not None:
        count += 1
        continue
    
    # Достаем названия, калории и пищевую ценность, попутно засовывая все это в словарь.
    all_products_data = soup.find(class_='mzr-tc-group-table').find('tbody').find_all('tr')
    schet = 0
    for item in all_products_data:
        group_of_products = item.find_all('td')
        product = group_of_products[0].find('a').text
        calories = group_of_products[1].text


        # Достаем пищевую ценность (на 100г, на 1 порцию ...)
        product_for_path = product
        for word in product_for_path:
            if word in sings:
                product_for_path = product_for_path.replace(word,'_') 

        if not(os.path.exists(f'sage/parsing/data/{count}_{category_name}')):
            os.mkdir(f'sage/parsing/data/{count}_{category_name}')

        if not(os.path.exists(f'sage/parsing/data/{count}_{category_name}/{schet}_{product_for_path}.html')):
            prov_help = True
            # мы будем фактически очень сильно бомбить сайт запросами, поэтому в случае чего просто ждем
            while prov_help:
                try:
                    food_value_url ='https://health-diet.ru' + group_of_products[0].find('a').get('href')
                    req = requests.get(url= food_value_url, headers= headers)
                    src = req.text

                    product_for_path = product
                    for word in product_for_path:
                        if word in sings:
                            product_for_path = product_for_path.replace(word,'_')   

                    with open(f'sage/parsing/data/{count}_{category_name}/{schet}_{product_for_path}.html','w',encoding='utf-8') as file:
                        file.write(src)

                    prov_help = False

                except Exception:
                    print("Произошло отключение...")
                    time.sleep(60)


        with open(f'sage/parsing/data/{count}_{category_name}/{schet}_{product_for_path}.html','r',encoding='utf-8') as file:
            src = file.read()
        schet += 1

        soup = BeautifulSoup(src,'lxml')

        food_value = soup.find(class_='mzr-nutrition-value').find('div').text
        food_value = food_value.replace('Пищевая ценность ','')
        food_value = food_value.replace('штука','шт.')
        food_value = food_value.strip('\n ')


        # завсовываем все в словарь
        all_products[product] = calories + " " + food_value


    # Делаем красивую загрузку
    print(f'Раздел {count}_{category_name} обработан и успешно загружен.')

    if how_many-count == 0:
        print('Работа завершена, можете проверять calories_of_products.json')
        break

    print(f'Осталось зарузить еще {how_many - count}.')
    time.sleep(random.randrange(2,4))


    # Идем дальше
    count += 1



# Полученные данные засовываяем в файл.json для дальнейшего использования
with open('sage/calories_of_products.json','w',encoding='utf-8') as file:
    json.dump(all_products,file, indent= 4, ensure_ascii= False)
    

# Эксперимент: хотел все просмотреть в одном файле, но не получилось.
# Думаю это из-за каких-нибудь особенностей.
# Он просто просматривает 1 страницу с "Бараниной и дичью" и остальные не хочет смотреть.
# Видимо все надо рассматривать по отдельности.
# 
# with open('parsing/all_parsing.html',encoding='utf-8') as file:
#     src = file.read()
# soup = BeautifulSoup(src,'lxml')
# all_products_data = soup.find_all(class_='mzr-tc-group-table')
# 
# for a in all_products_data:
#     products_data = a.find('tbody').find_all('tr')
#     for item in products_data:
#         group_of_products = item.find_all('td')

#         product = group_of_products[0].find('a').text
#         print(product)