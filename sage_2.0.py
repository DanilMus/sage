import json
import pyttsx3
import speech_recognition as sr
import time
import random


# робот: понимать и говорить
# говорить
def sage_says(phrase):
    sage = pyttsx3.init()

    print(phrase)
    # sage.say('Коку!')
    # sage.runAndWait()
    # time.sleep(0.05)
    sage.say(phrase)
    sage.runAndWait()
    time.sleep(0.1)

# понимать
recognizer = sr.Recognizer()
micro = sr.Microphone(device_index= 1)
with micro as source:
    recognizer.adjust_for_ambient_noise(source)
def sage_hear():
    global recognizer, micro
    try:
        with micro as audio:
            voice = recognizer.listen(audio)
        query = recognizer.recognize_google(voice, language= 'ru-RU') # query = запрос
        print(query)
        return str(query).lower() # обязательно надо указывать str, иначе будет NoneType
    except sr.UnknownValueError:
        sage_says('Голос не распознан, повторите пожалуйста.')
        sage_hear()

# говорить и понимать в одной фунции
def sage_is_talking(what_need_to_say):
    sage_says(what_need_to_say)
    answer = sage_hear()
    return str(answer) # тут точно так же надо str



# функции робота
# поиск по каталогу продуктов
with open('sage/data/sorted_calories_of_products.json',encoding='utf-8') as file:
    products_data = json.load(file)

def search():
    global what_did_search
    what_search = sage_is_talking('Что вас интересует?')
    what_did_search = {} # храние поиска
    schet = 0
    what_search = str(what_search).split()
    num_of_words = len(what_search)

    for product,calories in products_data.items():
        for word in what_search: # проверяем каждое слово, которое сказал пользователь
            if word in product: # чтобы оно было в названии продукта
                schet += 1
                if schet >= num_of_words: # когда все слова встретились, тогда закидываем в ответ
                    what_did_search[product] = calories
                continue
        schet = 0 # обновляем для следующих названий продуктов
    
    sage_says('Произвожу поиск...')

    for product,calories in what_did_search.items():
        schet += 1
        print(f'{schet}. {product} : {calories}')
    if schet == 0:
        sage_says('Извините, ничего не нашла.')

def search_with_comparsion(): # comparsion = сравнение
    global what_did_search

    def search_with_comparsion_help():
        search()

        comand = sage_is_talking('Выбирите продукт для сравнения и скажите его цифру. Цифру! Подчеркиваю!')
        comand = int(comand)

        schet = 0
        for product,calories in what_did_search.items():
            schet += 1
            if schet == comand:
                return product, calories
    
    sage_says('Выберите первый продукт')
    product1,calories1 = search_with_comparsion_help()
    sage_says('Выберите второй продукт')
    product2,calories2 = search_with_comparsion_help()

    calories1 = int(calories1.split()[0])
    calories2 = int(calories2.split()[0])

    r = random.randint(0,9)

    if (calories1 < calories2) and (r != 0):
        print(product1)
        sage_says('Я думаю, первый вариант лучше подойдет, ведь в нем меньше калорий.')
    elif (calories1 > calories2) and (r != 0):
        print(product2)
        sage_says('Я думаю, второй вариант лучше подойдет, ведь в нем меньше калорий.')
    elif (calories1 < calories2):
        print(product1)
        sage_says('Я думаю, вы можете позволить себе отдохнуть и взять первый вариант.')
    elif (calories1 > calories2): 
        print(product1)
        sage_says('Я думаю, вы можете позволить себе отдохнуть и взять первый вариант.')

def school_in_ass():
    sage_says('В жопу школу!')
    sage_says('Я свободен!')

# анализ команд
def reconise_comand(comand):
    comands = {
        'search': ('поиск','найти','найди'),
        'search_with_comparsion': 'сравнить', # comparsion = сравнение
        'school_in_ass': 'школ'
    }
    
    for word in comands['search']:
        # print(f'word = {word} comand = {comand}')
        if word in comand:
            cmd = 'search'
            return cmd

    if comands['search_with_comparsion'] in comand:
        cmd = 'search_with_comparsion'
        return cmd
    
    if comands['school_in_ass'] in comand:
        cmd = 'school_in_ass'
        return cmd

def execute_comand(cmd): # execute = исполнять
    if cmd == 'search':
        search()
    elif cmd == 'search_with_comparsion':
        search_with_comparsion()
    elif cmd == 'school_in_ass':
        school_in_ass()
    



# работа мудреца
answer = sage_is_talking("Здравствуйте!")
# если человек в первый раз, то он не знает, как зовут Мудреца
if 'мудрец' not in answer:
    sage_says('Вы у меня первый раз, да?')
    answer = sage_hear()
    if 'да' in answer:
        sage_says('Я так и знала, вот функции, которые я умею...')
        sage_says('Я знаю 12339 продуктов и их калории и могу найти их для вас. Просто скажите:"найти"')
        sage_says('А так же новинка, я могу сравнить калорийность двух продуктов и подсказать, что вам выбрать. Просто скажите:"сравнить"')
    else:
        sage_says('Видимо, я ошиблась. Если вас не затруднит называйте меня Мудрец в следующие разы.')

answer = sage_is_talking('Что хотите сделать?')
comand = reconise_comand(answer)
execute_comand(comand)
answer = sage_is_talking('Вам что-то еще нужно?')

while 'да' in answer:
    answer = sage_is_talking('Что хотите сделать?')
    comand = reconise_comand(answer)
    execute_comand(comand)
    answer = sage_is_talking('Вам что-то еще нужно?')

sage_says('До свидания!')