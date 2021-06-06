import json
import pyttsx3
import speech_recognition as sr
import time

# что должен сказать мудрец
def sage_says(phrase):
    sage = pyttsx3.init()
    sage.say('Коку!') # из "Слизи" пасхалка
    sage.runAndWait()
    print(phrase)
    sage = pyttsx3.init()
    sage.say(phrase)
    sage.runAndWait()
    time.sleep(0.05) # чтобы один (what_did_user_say()) не услышал другого (sage_says)


# узнаем, что говорит пользователь
def what_did_user_say():
    try:
        with micro as voice:
            audio = reco.listen(voice)

        query = reco.recognize_google(audio, language= 'ru-RU')
        print(query)
        return str(query).lower()

    except sr.UnknownValueError:
        sage_says('Голос не распознан. Повторите, пожалуйста.')
        what_did_user_say()
    
    except sr.RequestError:
        sage_says('Проверьте подключение к интернету и поробуйте перезайти.')


# ищем возможные варианты (конечно, лучше апгрейдить поиск)
def the_search():
    what_did_search = {} # храние поиска
    schet = 0

    for product,calories in src.items():
        for word in searching_words: # проверяем каждое слово, которое сказал пользователь
            if word in product: # чтобы оно было в названии продукта
                schet += 1
                if schet >= num_of_words: # когда все слова встретились, тогда закидываем в ответ
                    what_did_search[product] = calories
                continue
        schet = 0 # обновляем для следующих названий продуктов
    
    return what_did_search


# узнаем что хочет найти пользователь и извлекаем инф. из написанного
def what_do_user_want():
    # делаем глобальными, чтобы можно было воспользоваться в других функциях
    global searching_words 
    global num_of_words

    sage_says('Что хотите найти?')
    searching_word = what_did_user_say()
    searching_words = searching_word.split()
    num_of_words = int(len(searching_words))


# печатаем, что нашли
# (этой функции достаточно для поиcка, достаточно вызвать только ее для поиска)
def print_products():
    what_do_user_want()
    for product,calories in the_search().items():
        print(f'{product}: {calories}')


# загружаем каталог в переменную
with open('parsing/health-diet.ru/sorted_calories_of_products.json',encoding='utf-8') as file:
    src = json.load(file)


# подготовка робота слушать
reco = sr.Recognizer()
micro = sr.Microphone(device_index=1)
with micro as source:
    reco.adjust_for_ambient_noise(source)


# работа со всеми функциями
sage_says('Здравствуйте, я Мудрец! Я знаю 12337 продуктов и блюд, а также их калории.')
print_products()
sage_says('Вы нашли то, что хотели?')

if 'да' in what_did_user_say():
    sage_says('Рада была помочь. До свидания!')
else:
    sage_says('Попробуйте переформулировать.')
    print_products()
    sage_says('Надеюсь, теперь получилось найти?')
    if 'да' in what_did_user_say():
        sage_says('Отлично! До свидания!')
    else:
        sage_says('Будем, еще раз пробовать?')
        if 'да' in what_did_user_say():
            sage_says('У меня, к сожалению, не суперпродвинутый поиск, поэтому скажите попроще.')
            print_products()
            sage_says('Теперь смогла вам помочь?')
            if 'да' in what_did_user_say():
                sage_says('Ура! До свидания.')
            else:
                sage_says('Видимо я имею мало знаний, либо плохо сделана. Простите ( .')
        else:
            sage_says('Сожалею, что не помогла вам.')