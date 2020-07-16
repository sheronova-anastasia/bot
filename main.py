import config
import telebot
import lists

bot = telebot.TeleBot(config.token)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Приветствую, {}! \n'
                                      'Введи команду /help, '
                                      'чтобы открыть справку'.format(message.from_user.first_name))

@bot.message_handler(commands=['help'])
def help_message(message):
    bot.send_message(message.chat.id, 'Предлагаю тебе испытать свои знания в области географии! '
                                      'Введи команду /play и тебе предоставиться'
                                      'возможность выбрать режим игры - "Угадай страну" или "Угадай столицу".'
                                      'После выбора режима можно будет выбрать уровень сложности. В лёгком только самые '
                                      'известные страны и их столицы, а в сложном все страны мира!')

keyboard_play = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_play.row('Угадай страну', 'Угадай столицу')

keyboard_levels = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_levels.row('Легкий уровень', 'Сложный уровень')

keyboard_second_play = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard_second_play.row('С удовольствием!', 'Нет, надоело')

@bot.message_handler(commands=['play'])
def play(message):
   bot.send_message(message.chat.id, 'Выбери режим игры', reply_markup=keyboard_play)

entered_country = ''
entered_capital = ''
n = 1
result = 0

@bot.message_handler(content_types=['text'])

def choose_game(message):
    global game
    if message.text.lower() == 'угадай страну':
        game = 'угадай страну'
        bot.send_message(message.chat.id, 'Выбери уровень сложности', reply_markup=keyboard_levels)
    if message.text.lower() == 'угадай столицу':
        game = 'угадай столицу'
        bot.send_message(message.chat.id, 'Выбери уровень сложности', reply_markup=keyboard_levels)
    bot.register_next_step_handler(message, choose_difficulty)

def choose_difficulty(message):
    if message.text.lower() == 'легкий уровень' and game == 'угадай страну':
        guess_countryeasy(message)
    if message.text.lower() == 'сложный уровень' and game == 'угадай страну':
        guess_countryhard(message)
    if message.text.lower() == 'легкий уровень' and game == 'угадай столицу':
        guess_capitaleasy(message)
    if message.text.lower() == 'сложный уровень' and game == 'угадай столицу':
        guess_capitalhard(message)

def guess_countryeasy(message):
    global capital_in;
    if message.text == 'Легкий уровень' or entered_country != '' or 'С удовольствием!':
            capital_name = lists.random_easycapitals()
            capital_in = lists.easy_capitals.index(capital_name)
            bot.send_message(message.chat.id, capital_name)
            bot.register_next_step_handler(message, check_countryeasy)

def check_countryeasy(message):
    global entered_country
    global n;
    global result;
    entered_country = message.text
    if entered_country in lists.easy_countries:
        if capital_in == lists.easy_countries.index(message.text):
            result += 1
            bot.send_message(message.chat.id, 'Правильно!')
        else:
            bot.send_message(message.chat.id, 'Упс, неправильно! Это {}'.format(lists.easy_countries[capital_in]))
    else:
         bot.send_message(message.chat.id, 'Это не страна. Правильный ответ - {}'.format(lists.easy_countries[capital_in]))
    if n < 10:
        n = n + 1
        guess_countryeasy(message)
    else:
        bot.send_message(message.chat.id, 'Игра окончена, ваш результат: {} из 10'.format(result))
        bot.send_message(message.chat.id, 'Сыграем ещё раз?', reply_markup=keyboard_second_play)
        n = 1
        result = 0
        entered_country = ''
        bot.register_next_step_handler(message, end_game)

def guess_countryhard(message):
    global capital_in;
    if message.text == 'Сложный уровень' or entered_country != '' or 'С удовольствием!':
            capital_name = lists.random_capitals()
            capital_in = lists.capitals_list.index(capital_name)
            bot.send_message(message.chat.id, capital_name)
            bot.register_next_step_handler(message, check_countryhard)

def check_countryhard(message):
    global entered_country
    global n;
    global result;
    entered_country = message.text
    if entered_country in lists.countries_list:
        if capital_in == lists.countries_list.index(message.text):
            result += 1
            bot.send_message(message.chat.id, 'Правильно!')
        else:
            bot.send_message(message.chat.id, 'Упс, неправильно! Это {}'.format(lists.countries_list[capital_in]))
    else:
         bot.send_message(message.chat.id, 'Это не страна. Правильный ответ - {}'.format(lists.countries_list[capital_in]))
    if n < 10:
        n = n + 1
        guess_countryhard(message)
    else:
        bot.send_message(message.chat.id, 'Игра окончена, ваш результат: {} из 10'.format(result))
        bot.send_message(message.chat.id, 'Сыграем ещё раз?', reply_markup=keyboard_second_play)
        n = 1
        result = 0
        entered_country = ''
        bot.register_next_step_handler(message, end_game)


def guess_capitaleasy(message):
    global country_in;
    if message.text == 'Легкий уровень' or entered_capital != '' or 'С удовольствием!':
        country_name = lists.random_easycountries()
        country_in = lists.easy_countries.index(country_name)
        bot.send_message(message.chat.id, country_name)
        bot.register_next_step_handler(message, check_capitaleasy)

def check_capitaleasy(message):
    global entered_capital
    global n;
    global result;
    entered_capital = message.text
    if entered_capital in lists.easy_capitals:
        if country_in == lists.easy_capitals.index(message.text):
            result += 1
            bot.send_message(message.chat.id, 'Правильно!')
        else:
            bot.send_message(message.chat.id, 'Упс, неправильно! Это {}'.format(lists.easy_capitals[country_in]))
    else:
         bot.send_message(message.chat.id, 'Это не столица. Правильный ответ - {}'.format(lists.easy_capitals[country_in]))
    if n < 10:
        n = n + 1
        guess_capitaleasy(message)
    else:
        bot.send_message(message.chat.id, 'Игра окончена, ваш результат: {} из 10'.format(result))
        bot.send_message(message.chat.id, 'Сыграем ещё раз?', reply_markup=keyboard_second_play)
        n = 1
        result = 0
        entered_capital = ''
        bot.register_next_step_handler(message, end_game)

def guess_capitalhard(message):
    global country_in;
    if message.text == 'Сложный уровень' or entered_capital != '' or 'С удовольствием!':
        country_name = lists.random_countries()
        country_in = lists.countries_list.index(country_name)
        bot.send_message(message.chat.id, country_name)
        bot.register_next_step_handler(message, check_capitalhard)

def check_capitalhard(message):
    global entered_capital
    global n;
    global result;
    entered_capital = message.text
    if entered_capital in lists.capitals_list:
        if country_in == lists.capitals_list.index(message.text):
            result += 1
            bot.send_message(message.chat.id, 'Правильно!')
        else:
            bot.send_message(message.chat.id, 'Упс, неправильно! Это {}'.format(lists.capitals_list[country_in]))
    else:
         bot.send_message(message.chat.id, 'Это не столица. Правильный ответ - {}'.format(lists.capitals_list[country_in]))
    if n < 10:
        n = n + 1
        guess_capitalhard(message)
    else:
        bot.send_message(message.chat.id, 'Игра окончена, ваш результат: {} из 10'.format(result))
        bot.send_message(message.chat.id, 'Сыграем ещё раз?', reply_markup=keyboard_second_play)
        n = 1
        result = 0
        entered_capital = ''
        bot.register_next_step_handler(message, end_game)

def end_game(message):
    if message.text.lower() == 'нет, надоело':
        bot.send_message(message.chat.id, 'Хорошо, приходи в следующий раз!')
    if message.text.lower() == 'с удовольствием!':
        play(message)

bot.polling()