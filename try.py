import telebot
from telebot import types
import pandas as pd
import chardet
import csv
from random import randint

# создаем бота
# возможность редактирования! нужно удалить запись о пользователе - удаляется ли?


bot = telebot.TeleBot(token='6629936372:AAHfcPCZf1b3wzp5BvuVlSX9IAAKkEHXG8c')

#состояния пользователей
'''users_info = {}
states = {}

start = range(1)
sign = range(1)
help = range(1)
text = range(1)
get_photo = range(1)'''


# строка которую добавим в df
users_dict = pd.DataFrame(
    {'user_id': None, 'gender': None, 'age': None, 'city': None, 'additional info': None, 'name': None,
     'user_name': None}, index=[0])
dogs_dict = pd.DataFrame(
    {'dog_id': None, 'name': None, 'gender': None, 'age': None, 'city': None, 'additional info': None, 'size': None,
     'dog_name': None}, index=[0])
likes_dict = pd.DataFrame({'who liked': None, 'whom liked': None, 'mutuality': None}, index=[0])

# проверяем кодировку
with open('database_dogs.csv', 'rb') as f:
    res_d = chardet.detect(f.read())

with open('database_users.csv', 'rb') as f:
    res_u = chardet.detect(f.read())

with open('database_likes.csv', 'rb') as f:
    res_l = chardet.detect(f.read())

# базы данных
db_users = pd.read_csv('database_users.csv', encoding=res_u['encoding'], sep=';')
db_dogs = pd.read_csv('database_dogs.csv', encoding=res_d['encoding'], sep=';')
db_likes = pd.read_csv('database_likes.csv', encoding=res_l['encoding'], sep=',')

#сохраняем данные в базы
'''u_col = ['user_id', 'name', 'gender', 'age', 'city', 'additional info', 'user_name']
writer_u = csv.DictWriter(db_users, fieldnames=u_col)
writer_u.writeheader()

d_col = ['dog_id', 'name', 'gender', 'age', 'city', 'additional info', 'size', 'dog_name']
writer_d = csv.DictWriter(db_users, fieldnames=d_col)
writer_d.writeheader()

l_col = ['who liked', 'whom liked', 'mutuality']
writer_l = csv.DictWriter(db_users, fieldnames=l_col)
writer_l.writeheader()'''

extn = '.png'

# отфильтрованные базы данных
db_dogs1 = pd.DataFrame(columns=['dog_id', 'name', 'gender', 'age', 'city', 'additional info', 'size', 'dog_name'])
db_dogs2 = pd.DataFrame(columns=['dog_id', 'name', 'gender', 'age', 'city', 'additional info', 'size', 'dog_name'])
db_users1 = pd.DataFrame(columns=['user_id', 'gender', 'age', 'city', 'additional info', 'name', 'user_name'])

# кто кого лайкнул
db_likes1 = pd.DataFrame(columns=['who liked', 'whom liked', 'mutuality'])
db_likes2 = pd.DataFrame(columns=['who liked', 'whom liked', 'mutuality'])
db_likes12 = pd.DataFrame(columns=['who liked', 'whom liked', 'mutuality'])
db_mut_likes = pd.DataFrame(columns=['who liked', 'whom liked', 'mutuality'])
# флаги
doggy = False
human = False
last_photo_name = None

# мой юзер
class User:
    def __init__(self, name=None):
        self.name = name
        self.age = 0
        self.gender = None
        self.city = None
        self.info = None
        self.id = None
        self.size = None
        self.nick_name = None
user = User()

# обработчик команды start
@bot.message_handler(commands=['start'])
def start_message(message):
    '''global start, users_info, states
    secret = randint(1,49494985894939494944)
    states[secret] = start
    users_info[message.chat.id] = secret'''
    bot.send_message(message.chat.id,
                     f"Привет {message.chat.first_name}, я бот для поиска хозяев бездомным собакам. \n\n"
                     f"Здесь пользователи выкладывают анкеты найденных собак или свои, если хотят взять одного из питомцев себе.\n"
                     f"Юзер отмечает 'подходит' или 'не подходит', просматривая анкеты.\n"
                     f"В случае взаимной симпатии вы получите контакты друг друга, чтобы продолжить общение в лс.\n"
                     f"Напиши /help, чтобы узнать, что я умею.")


# обработчик команды help
@bot.message_handler(commands=['help'])
def start_message(message):
    '''global help, users_info, states'''
    bot.send_message(message.chat.id, 'Бот предназначен для обмена анкетами бездомных собак и потенциальных хозяев.')
    #states[users_info[message.chat.id]] = help
    bot.send_message(message.chat.id,
                                      "После нажатия команды /sign можно:\n"
                                      "'Зарегистрировать собаку' или 'Зарегистрироваться самому'\n"
                                      "'Смотреть анкеты' - после регистрации\n"
                                      "'Создать анкету заново' - чтобы внести в анкету изменения\n"
                                      "'Мои лайки' - узнай кому понравилась твоя анкета\n"
                                      "'Взаимные лайки' - ваши взаимные симпатии с пользователями \n"
                                      "Вызывай /help, если запутался и выбирай то, что тебе нужно"
                                        , parse_mode='HTML')
    bot.send_message(message.chat.id, "Если в процессе использования ты захочешь оценить меня "
    "перейди по ссылке: https://forms.gle/8S78gexkMAtgeT3D9 ")


@bot.message_handler(commands=['sign'])
def button_message(message):
    '''global sign, users_info, states
    states[users_info[message.chat.id]] = sign'''
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    search_pr = types.KeyboardButton("Смотреть анкеты")
    sign_dog = types.KeyboardButton("Зарегистрировать собаку")
    sign_me = types.KeyboardButton("Зарегистрироваться самому")
    one_more = types.KeyboardButton("Создать анкету заново")
    my_likes = types.KeyboardButton("Мои лайки")
    mutual_likes = types.KeyboardButton("Взаимные лайки")

    markup.add(search_pr, sign_me, sign_dog, my_likes, mutual_likes, one_more)
    bot.send_message(message.chat.id, 'Выбери, что хочешь сделать', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def message_reply(message):
    global doggy, human, \
        db_users1, db_dogs1, db_dogs2, db_likes1, db_likes2,\
        db_likes12, db_mut_likes, likes_dict, db_likes,\
        user, last_photo_name
        #global text, users_info, states
    #states[users_info[message.chat.id]] = text
    if message.text == "Смотреть анкеты":
        # если анкета есть
        if f'{message.chat.id}' in db_users['user_id'].values or f'{message.chat.id}' in db_dogs['dog_id'].values:
            if f'{message.chat.id}' in db_users['user_id'].values:
                human = True
            else:
                doggy = True
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            yes = types.KeyboardButton('Да')
            no = types.KeyboardButton('Нет')
            markup.add(yes, no)
            bot.send_message(message.chat.id, 'Важен ли тебе город поиска?', reply_markup=markup)

        # если анкеты нет
        if f'{message.chat.id}' not in db_users['user_id'].values and f'{message.chat.id}' not in db_dogs[
            'dog_id'].values:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            sign_d = types.KeyboardButton('Зарегистрировать собаку')
            sign_u = types.KeyboardButton('Зарегистрироваться самому')
            markup.add(sign_u, sign_d)
            bot.send_message(message.chat.id, 'Сначала нужно создать анкету', reply_markup=markup)


    # если заходит значит анкета точно есть
    elif message.text == "Да" or message.text == "Нет":
        if human:  # сократить базу данных собак до твоего города
            if message.text == 'Да':
                if db_dogs.shape[0] > 0:
                    ind = db_users.index[db_users['user_id'] == f'{message.chat.id}'].tolist()[0]
                    val_city = db_users['city'].iloc[[ind]]
                    db_dogs1 = db_dogs.loc[db_dogs['city'] == val_city]
            else:
                db_dogs1 = db_dogs
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            big = types.KeyboardButton('большой')
            small = types.KeyboardButton('маленький')
            average = types.KeyboardButton('средний')
            no = types.KeyboardButton('не важно')
            markup.add(big, small, average, no)
            bot.send_message(message.chat.id, 'Какого размера ты хочешь собаку?', reply_markup=markup)

        elif doggy:  # сократить базу данных людей до твоего города
            if message.text == "Да":
                if db_users.shape[0] > 0:
                    ind = db_dogs.index[db_dogs['dog_id'] == f'{message.chat.id}'].tolist()[0]
                    val_city = db_dogs['city'].iloc[[ind]]
                    db_users1 = db_users.loc[db_users['city'] == val_city]
            else:
                db_users1 = db_users
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            start = types.KeyboardButton('Да, погнали')
            markup.add(start)
            bot.send_message(message.chat.id, 'Начинаем поиск?', reply_markup=markup)

    elif message.text == "Зарегистрироваться самому" or message.text == "Зарегистрировать собаку" or message.text == "Создать анкету заново":
        # если анкета есть - понимаем для кого создаем
        if message.text == "Создать анкету заново":
            if f'{message.chat.id}' in db_users['user_id'].values:
                doggy = False
                human = True
                ind = db_users.index[db_users['user_id'] == f'{message.chat.id}'].tolist()[0]
                #удалить из scv файла строку
                db_users.drop(index=ind)
                #db_users.to_csv("database_users")
            elif f'{message.chat.id}' in db_dogs['dog_id'].values:
                human = False
                doggy = True
                ind = db_dogs.index[db_dogs['dog_id'] == f'{message.chat.id}'].tolist()[0]
                #удалить из csv файла стрноку
                db_dogs.drop(index=ind)
                #db_dogs.to_csv("database_dogs")
        elif message.text == "Зарегистрироваться самому":
            doggy = False
            human = True
        else:
            human = False
            doggy = True

        bot_ans = bot.reply_to(message, 'Как тебя зовут? Если регистрируешь питомца пиши от его имени')
        bot.register_next_step_handler(bot_ans, process_name)




    elif message.text == "Мои лайки":
        if f'{message.chat.id}' in db_likes['whom liked'].values:
            db_likes1 = db_likes.loc[db_likes['whom liked'] == f'{message.chat.id}']
        if f'{message.chat.id}' in db_likes['who liked'].values:
            db_likes2 = db_likes.loc[db_likes['who liked'] == f'{message.chat.id}']

        # объединение баз данных где упоминался юзер
        db_likes12 = pd.concat([db_likes1, db_likes2], ignore_index=True)

        if db_likes12.shape[0] == 0:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            search = types.KeyboardButton('Смотреть анкеты')
            markup.add(search)
            bot.send_message(message.chat.id, f'Вашу анкету никто не отметил. Смотреть анкеты?\n'
                                              f'Если хочешь вернуться на главную панель нажми /help',
                             reply_markup=markup)
        else:
            bot.send_message(message.chat.id, f'Ваша анкета понравилась {db_likes12.shape[0]} людям')

            for row in db_likes12.itertuples(index=False):
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                dislike = types.KeyboardButton('дальше')
                like = types.KeyboardButton('подходит')
                markup.add(like, dislike)

                if human:
                    if row[0] == f'{message.chat.id}':
                        ind = db_dogs.index[db_dogs['dog_id'] == f'{row[1]}'].tolist()[0]
                        photo_name = row[1]
                    else:
                        ind = db_dogs.index[db_dogs['dog_id'] == f'{row[0]}'].tolist()[0]
                        photo_name = row[0]
                    d_name = db_dogs['name'].iloc[[ind]]
                    d_age = db_dogs['age'].iloc[[ind]]
                    d_city = db_dogs['city'].iloc[[ind]]
                    d_gender = db_dogs['gender'].iloc[[ind]]
                    d_size = db_dogs['size'].iloc[[ind]]
                    d_info = db_dogs['additional info'].iloc[[ind]]

                    # работа с фото
                    photo = open(f'dogs_photos/{photo_name}', 'rb')
                    # dog id
                    last_photo_name = photo_name
                    bot.send_photo(message.from_user.id, photo, caption=
                    f'{d_name}, {d_age}, {d_city}\n\n'
                    f'Пол: <i>{d_gender}</i>\n'
                    f'Размер: <i>{d_size}</i>\n'
                    f'О себе: <i>{d_info}</i>',
                                   parse_mode="HTML", reply_markup=markup)

                if doggy:
                    if row[0] == f'{message.chat.id}':
                        ind = db_dogs.index[db_dogs['dog_id'] == f'{row[1]}'].tolist()[0]
                        photo_name = row[1]
                    else:
                        ind = db_dogs.index[db_dogs['dog_id'] == f'{row[0]}'].tolist()[0]
                        photo_name = row[0]
                    u_name = db_users['name'].iloc[[ind]]
                    u_age = db_users['age'].iloc[[ind]]
                    u_city = db_users['city'].iloc[[ind]]
                    u_gender = db_users['gender'].iloc[[ind]]
                    u_info = db_users['additional info'].iloc[[ind]]
                    # работа с фото
                    photo = open(f'dogs_photos/{photo_name}', 'rb')
                    # user id
                    last_photo_name = photo_name
                    bot.send_photo(message.from_user.id, photo, caption=
                    f'{u_name}, {u_age}, {u_city}\n\n'
                    f'Пол: <i>{u_gender}</i>\n'
                    f'О себе: <i>{u_info}</i>',
                                   parse_mode="HTML", reply_markup=markup)


    elif message.text == "Взаимные лайки":
        db_likes1 = db_likes.loc[db_likes['whom liked'] == f'{message.chat.id}']
        db_likes2 = db_likes.loc[db_likes['who liked'] == f'{message.chat.id}']

        # объединение баз данных где упоминался юзер
        db_likes12 = pd.concat([db_likes2, db_likes1], ignore_index=True)
        db_mut_likes = db_likes12.loc[db_likes12['mutuality'] == '+']
        if db_likes12.shape[0] == 0:
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            search = types.KeyboardButton('Смотреть анкеты')
            markup.add(search)
            bot.send_message(message.chat.id,
                             f'Пока взаимных симпатий нет. Смотреть анкеты?\n'
                             f'Если хочешь вернуться на главную панель нажми /help', reply_markup=markup)
        else:
            # показ анкеты взаимности
            for row in db_mut_likes.itertuples(index=False):
                # извлекаем значение из  собачьей анкеты
                if human:
                    if row[0] == f'{message.chat.id}':
                        ind = db_dogs.index[db_dogs['dog_id'] == f'{row[1]}'].tolist()[0]
                        photo_name = row[1]
                    else:
                        ind = db_dogs.index[db_dogs['dog_id'] == f'{row[0]}'].tolist()[0]
                        photo_name = row[0]
                    d_name = db_dogs['name'].iloc[[ind]]
                    d_age = db_dogs['age'].iloc[[ind]]
                    d_city = db_dogs['city'].iloc[[ind]]
                    d_gender = db_dogs['gender'].iloc[[ind]]
                    d_size = db_dogs['size'].iloc[[ind]]
                    d_info = db_dogs['additional info'].iloc[[ind]]
                    d_dogname = db_dogs['dog_name'].iloc[[ind]]
                    # работа с фото
                    photo = open(f'dogs_photos/{photo_name}', 'rb')
                    bot.send_photo(message.from_user.id, photo, caption=
                    f'{d_name}, {d_age}, {d_city}\n\n'
                    f'Пол: <i>{d_gender}</i>\n'
                    f'Размер: <i>{d_size}</i>\n'
                    f'О себе: <i>{d_info}</i>',
                                   parse_mode="HTML")
                    bot.send_message(message.chat.id,
                                     f'Поздравляю! У вас взаимная симпатия c пользлователем {d_dogname}. Напиши ему')
                if doggy:
                    if row[0] == f'{message.chat.id}':
                        ind = db_dogs.index[db_dogs['dog_id'] == f'{row[1]}'].tolist()[0]
                        photo_name = row[1]
                    else:
                        ind = db_dogs.index[db_dogs['dog_id'] == f'{row[0]}'].tolist()[0]
                        photo_name = row[0]
                    u_name = db_users['name'].iloc[[ind]]
                    u_age = db_users['age'].iloc[[ind]]
                    u_city = db_users['city'].iloc[[ind]]
                    u_gender = db_users['gender'].iloc[[ind]]
                    u_info = db_users['additional info'].iloc[[ind]]
                    u_username = db_users['user_name'].iloc[[ind]]
                    # работа с фото
                    photo = open(f'dogs_photos/{photo_name}', 'rb')
                    bot.send_photo(message.from_user.id, photo, caption=
                    f'{u_name}, {u_age}, {u_city}\n\n'
                    f'Пол: <i>{u_gender}</i>\n'
                    f'О себе: <i>{u_info}</i>',
                                   parse_mode="HTML")
                    bot.send_message(message.chat.id,
                                     f'Поздравляю! У вас взаимная симпатия c пользователем {u_username}. Напиши ему')


    elif message.text == 'Да, погнали':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        like = types.KeyboardButton('подходит')
        dislike = types.KeyboardButton('дальше')
        stop = types.KeyboardButton('достаточно')
        markup.add(like, dislike, stop)
        if doggy:
            l = db_users1.shape[0]

            if l != 0:
                order = list(range(l))
            else:
                order = []
            print(order)
            while order:
                photo_name = db_users1['user_id'].iloc[[order[-1]]]
                order.pop()
                photo = open(f'dogs_photos/{photo_name}', 'rb')
                ind = db_users1.index[db_users['user_id'] == f'{photo_name}'].tolist()[0]
                u_name = db_users['name'].iloc[[ind]]
                u_age = db_users['age'].iloc[[ind]]
                u_city = db_users['city'].iloc[[ind]]
                u_gender = db_users['gender'].iloc[[ind]]
                u_info = db_users['additional info'].iloc[[ind]]
                bot.send_photo(message.chat.id, photo, caption=f'{u_name}, {u_age}, {u_city}\n\n'
                                                               f'Пол: <i>{u_gender}</i>\n'
                                                               f'О себе: <i>{u_info}</i>', parse_mode="HTML",
                               reply_markup=markup)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                one_more = types.KeyboardButton('Создать анкету заново')
                likes = types.KeyboardButton('Мои лайки')
                m_likes = types.KeyboardButton('Взаимные лайки')
                markup.add(one_more, likes, m_likes)
                bot.send_message(message.chat.id, 'Нет активных анкет в данной категории. Заходи в следующий раз!\n'
                                                  'Если ты отметил кого-то "подходит" дождись его ответа.'
                                                  'Возможно у вас взаимная симпатия:)\n Пока можешь посмотреть свои лайки '
                                                  'или создать анкету заново, если хочешь что-то в ней поменять',
                               reply_markup=markup)

        if human:
            l = db_dogs2.shape[0]

            if l != 0:
                order = list(range(l))
            else:
                order = []
            while order:
                photo_name = db_users1['user_id'].iloc[[order[-1]]]
                order.pop()
                photo = open(f'dogs_photos/{photo_name}', 'rb')
                ind = db_dogs2.index[db_dogs2['dog_id'] == f'{photo_name}'].tolist()[0]
                d_name = db_dogs['name'].iloc[[ind]]
                d_age = db_dogs['age'].iloc[[ind]]
                d_city = db_dogs['city'].iloc[[ind]]
                d_gender = db_dogs['gender'].iloc[[ind]]
                d_size = db_dogs['size'].iloc[[ind]]
                d_info = db_dogs['additional info'].iloc[[ind]]
                bot.send_photo(message.chat.id, photo, caption=f'{d_name}, {d_age}, {d_city}\n\n'
                                                               f'Пол: <i>{d_gender}</i>\n'
                                                               f'Размер: <i>{d_size}</i>\n'
                                                               f'О себе: <i>{d_info}</i>', parse_mode="HTML",
                               reply_markup=markup)

            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                one_more = types.KeyboardButton('Создать заново')
                likes = types.KeyboardButton('Мои лайки')
                m_likes = types.KeyboardButton('Взаимные лайки')
                markup.add(one_more, likes, m_likes)
                bot.send_message(message.chat.id, 'Больше нет активных анкет. Заходи в следующий раз!\n'
                                                  'Если ты отметил кого-то "подходит" дождись его ответа.'
                                                  'Возможно у вас взаимная симпатия:)\n Пока можешь посмотреть свои лайки '
                                                  'или создать анкету заново, если хочешь что-то в ней поменять',
                               reply_markup=markup)



    # обработка симпатии в анкетах
    elif message.text == 'подходит':
        # db_likes12 - база лайков про конкретного юзера
        likes_dict['who liked'] = f'{message.chat.id}'
        likes_dict['whom liked'] = f'{last_photo_name}'
        ind_who = 0
        ind_whom = 0
        if last_photo_name in db_likes['who liked'].values:
            ind_whom = db_likes.index[db_likes['who liked'] == f'{last_photo_name}'].tolist()[0]
        if f'{message.chat.id}' in db_likes['whom liked'].values:
            ind_who = db_dogs.index[db_dogs['whom liked'] == f'{message.chat.id}'].tolist()[0]
        # проверка на mutuality
        if ind_who == ind_whom and ind_who != 0:
            likes_dict['mutuality'] = '+'
            #db_likes.to_csv("database_likes")
            '''csv.writer_u.writerow({'who liked': f'{message.chat.id}', 'whom liked': f'{last_photo_name}', 'mutuality': '+'})'''
        elif ind_who != ind_whom:
            likes_dict['mutuality'] = '-'
            db_likes = pd.concat([db_likes, likes_dict], ignore_index=True)
            #db_likes.to_csv('database_likes')
            '''csv.writer_u.writerow({'who liked': f'{message.chat.id}', 'whom liked': f'{last_photo_name}', 'mutuality':'-'})'''
            likes_dict = pd.DataFrame(
                {'who liked': None, 'whom liked': None, 'mutuality': None}, index=[0])  #индекс = номер будущей строки

    elif message.text == 'дальше':
        pass

    elif message.text == 'хватит':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        search_pr = types.KeyboardButton("Смотреть анкеты")
        sign_dog = types.KeyboardButton("Зарегистрировать собаку")
        sign_me = types.KeyboardButton("Зарегистрироваться самому")
        my_likes = types.KeyboardButton("Мои лайки")
        mutual_likes = types.KeyboardButton("Взаимные лайки")
        markup.add(search_pr, sign_me, sign_dog, my_likes, mutual_likes)

        bot.send_message(message.chat.id, 'Выбери, что хочешь сделать', reply_markup=markup)

    if message.text == "большой" or message.text == "маленький" or message.text == "средний" or message.text == "не важно":
        # отфильтровать базу данных по слову
        if message.text == 'большой':
            db_dogs2 = db_dogs1.loc[db_dogs1['size'] == 'большой']
        elif message.text == 'средний':
            db_dogs2 = db_dogs1.loc[db_dogs1['size'] == 'средний']
        elif message.text == 'маленький':
            db_dogs2 = db_dogs1.loc[db_dogs1['size'] == 'маленький']
        else:
            db_dogs2 = db_dogs1
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        start = types.KeyboardButton('Да, погнали')
        markup.add(start)
        bot.send_message(message.chat.id, 'Окей, сейчас подыщу нужные анкеты. Начинаем?', reply_markup=markup)


# обработка анкеты:
def process_name(message):
    global user, users_dict, dogs_dict
    user_id = f'{message.chat.id}'
    name = message.text
    user.name = name
    if doggy:
        dogs_dict['name'] = name
        dogs_dict['dog_id'] = user_id
        dogs_dict['dog_name'] = message.chat.username
    if human:
        users_dict['name'] = name
        users_dict['user_id'] = user_id
        users_dict['user_name'] = message.chat.username
    user.nick_name = message.chat.username
    bot_ans = bot.reply_to(message, 'Сколько тебе лет?')
    bot.register_next_step_handler(bot_ans, process_age)


def process_age(message):
    global user, users_dict, dogs_dict
    age = message.text
    age1 = str(age).split()
    if not age1[0].isdigit():
        msg = bot.reply_to(message, 'Возраст должен быть числом. Попробуй ввести заново')
        bot.register_next_step_handler(msg, process_age)
        return
    user.age = age
    if doggy:
        dogs_dict['age'] = age
    if human:
        users_dict['age'] = age
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    markup.add('мужской', 'женский')
    msg = bot.reply_to(message, 'Какой у тебя пол', reply_markup=markup)
    bot.register_next_step_handler(msg, process_gender)


def process_gender(message):
    global user, users_dict, dogs_dict
    gender = message.text
    user.gender = gender
    '''if (gender == u'мужской') or (gender == u'женский'):
        user.sex = gender
    else:
        raise Exception()'''
    msg = bot.reply_to(message,
                       'Приятно познакомиться, ' + user.name + '!\n Возраст: ' + str(
                           user.age) + '\n Пол: ' + user.gender)

    msg2 = bot.reply_to(msg, "Откуда ты? Введи название города, например: Москва")
    bot.register_next_step_handler(msg2, process_city)


def process_city(message):
    global user, users_dict, dogs_dict
    city = message.text
    user.city = city
    if doggy:
        dogs_dict['city'] = city.lower()
        bot_ans = bot.reply_to(message, 'Расскажи о себе. Любишь гулять? Какие знаешь команды?')
    if human:
        users_dict['city'] = city.lower()
        bot_ans = bot.reply_to(message, 'Расскажи о себе. Почему хочешь взять собаку? Какого питомца ищешь?')

    bot.register_next_step_handler(bot_ans, process_info)


def process_info(message):
    global user, users_dict, dogs_dict

    info = message.text
    user.info = info
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    big = types.KeyboardButton('большой')
    small = types.KeyboardButton('маленький')
    average = types.KeyboardButton('средний')
    markup.add(big, small, average)
    if doggy:
        dogs_dict['additional info'] = info
        bot_ans = bot.reply_to(message, 'Какой ты по размеру?', reply_markup=markup)
    if human:
        users_dict['additional info'] = info
        bot_ans = bot.reply_to(message, 'Важен ли тебе размер питомца?')

    bot.register_next_step_handler(bot_ans, process_size)


def process_size(message):
    global user, users_dict, dogs_dict
    size = message.text
    user.size = size
    if doggy:
        dogs_dict['size'] = size
    bot_ans = bot.reply_to(message, "Почти закончили, остался последний шаг. Прикрепи свою фотографию")

    bot.register_next_step_handler(bot_ans, get_photo)


# обработчик фотографий
@bot.message_handler(content_types=['photo'])
def get_photo(message):
    global extn
    #get_photo, states, users_info
    #states[users_info[message.chat.id]] = sign
    # скачивание файла
    if message.photo:
        file_info = bot.get_file(message.photo[len(message.photo) - 1].file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        extn = '.' + str(file_info.file_path).split('.')[-1]
        if doggy:
            file_name = f'dogs_photos/{message.chat.id}{extn}'
        elif human:
            file_name = f'users_photos/{message.chat.id}{extn}'

        with open(file_name, 'wb') as new_file:
            new_file.write(downloaded_file)
        # клавиатура
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        watch = types.KeyboardButton('Давай')
        markup.add(watch)
        msg = bot.reply_to(message, 'Ваша анкета готова. Посмотреть как она будет выглядеть для других пользователей?',
                           reply_markup=markup)
        bot.register_next_step_handler(msg, send_photo)


def send_photo(message):
    global user, users_dict, dogs_dict,\
        extn, doggy, human, db_users, db_dogs

    # показываем анкету самому себе
    if doggy:
        photo = open(f'dogs_photos/{message.chat.id}{extn}', 'rb')
        bot.send_photo(message.chat.id, photo, caption=f'{user.name}, {user.age}, {user.city}\n\n'
                                                       f'Пол: <i>{user.gender}</i>\n'
                                                       f'Размер: <i>{user.size}</i>\n'
                                                       f'О себе: <i>{user.info}</i>', parse_mode='HTML')
        db_dogs = pd.concat([db_dogs, dogs_dict], ignore_index=True)
        '''csv.writer_d.writerow({'dog_id': f'{message.chat.id}', 'name': user.name, 'gender': user.gender,
                               'age': user.age, 'city': user.city,
                               'additional info': user.info, 'size': user.size, 'dog_name': user.nick_name})'''
        #db_dogs.to_csv("database_dogs.csv")
        dogs_dict = pd.DataFrame(
            {'dog_id': None, 'name': None, 'gender': None, 'age': None, 'city': None, 'additional info': None,
             'size': None, 'dog_name': None}, index=[0])

    elif human:
        photo = open(f'users_photos/{message.chat.id}{extn}', 'rb')
        bot.send_photo(message.chat.id, photo, caption=f'{user.name}, {user.age}, {user.city}\n\n'
                                                       f'Пол: <i>{user.gender}</i>\n'
                                                       f'О себе: <i>{user.info}</i>', parse_mode='HTML')
        db_users = pd.concat([db_users, users_dict], ignore_index=True)
        #db_users.to_csv("database_users.csv")
        '''csv.writer_u.writerow({'user_id': f'{message.chat.id}', 'gender': user.gender,
                               'age': user.age, 'city': user.city,
                               'additional info': user.info, 'name': user.name, 'user_name': user.nick_name})'''

        users_dict = pd.DataFrame(
            {'user_id': None, 'gender': None, 'age': None, 'city': None, 'additional info': None, 'name': None, 'user_name': None},
            index=[0])

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    search = types.KeyboardButton('Смотреть анкеты')
    markup.add(search)
    bot.send_message(message.chat.id, 'Если захочешь создать анкету заново используй команду /sign.\n'
                                      'Через нее ты получишь доступ к кнопке "Создать анкету заново"\n'
                                      'Если ты готов смотреть анкеты нажимай "Смотреть анкеты"', reply_markup=markup)


bot.enable_save_next_step_handlers(delay=2)
bot.load_next_step_handlers()
bot.polling(none_stop=True)

# bot.infinity_polling()

# если метч случится вот nickname = bot.message.chat.username
