import json

# перемещение в новый файл + сортировка, перевод в нижний регстр, переделывание кКална на кКал на, kentucky fried chicken на kfc,"'" на ''
with open('sage/sorted_calories_of_products.json',encoding='utf-8') as file:
    src = json.load(file)

sorted_products = {}

for product,calories in sorted(src.items()):
    calories_new = calories.replace('кКална','кКал на')
    product_new = product.lower()
    if 'kentucky fried chicken' in product_new:
        product_new = product_new.replace('kentucky fried chicken','kfc')
    while "'" in product_new:
        product_new = product_new.replace("'",'')
    sorted_products[product_new] = calories_new

with open('sage/sorted_calories_of_products.json','w',encoding='utf-8') as file:
    json.dump(sorted_products, file, indent= 4, ensure_ascii= False)