import json
from os import replace


with open('sage/data/sorted_calories_of_products.json',encoding='utf-8') as file:
    src = json.load(file)

# перемещение в новый файл + сортировка, перевод в нижний регстр, переделывание кКална на кКал на, kentucky fried chicken на kfc,"'" на ''
# sorted_products = {}

# for product,calories in sorted(src.items()):
#     calories_new = calories.replace('кКална','кКал на')
#     product_new = product.lower()
#     if 'kentucky fried chicken' in product_new:
#         product_new = product_new.replace('kentucky fried chicken','kfc')
#     while "'" in product_new:
#         product_new = product_new.replace("'",'')
#     sorted_products[product_new] = calories_new

# убираю явные неточности с сайта
for product,calories in src.items():
    if '100 шт.' in calories:
        src[product] = calories.replace('100','1')
    if '100 порция' in calories:
        src[product] = calories.replace('100 порция','1 порцию')


with open('sage/data/sorted_calories_of_products.json','w',encoding='utf-8') as file:
    json.dump(src, file, indent= 4, ensure_ascii= False)
