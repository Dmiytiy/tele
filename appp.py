import telebot
import math
import threading

from telebot import types

bot = telebot.TeleBot('6538226896:AAEYiZJ5b2BWOelXPENo4I4h2Hsq3tCqZuo')

# Кеш для хранения уже вычисленных факториалов
# factorial_cache = {}


tasks = {
    "Сумма1": [
        {"task": "150 + 150", "answer": "300"},
        {"task": "433 + 433", "answer": "866"}],
    "Сумма2": [
        {"task": "100 + 101", "answer": "201"},
        {"task": "1.2 + 2", "answer": "3.2"}
    ],
    "Разность1": [
        {"task": "300 - 150", "answer": "150"},
        {"task": "433 - 200", "answer": "233"}],
    "Разность2": [
        {"task": "100 - 99", "answer": "1"},
        {"task": "5.5 - 3", "answer": "2.5"}
    ],
    "Умножение1": [
        {"task": "5 * 5", "answer": "25"},
        {"task": "10 * 15", "answer": "150"}],
    "Умножение2": [
        {"task": "3 * 8", "answer": "24"},
        {"task": "0 * 7", "answer": "0"}
    ],
    "Деление1": [
        {"task": "100 / 25", "answer": "4"},
        {"task": "45 / 5", "answer": "9"}],
    "Деление2":[
        {"task": "81 / 9", "answer": "9"},
        {"task": "12 / 4", "answer": "3"}
    ],
    "Площадь1": [
        {"task": "Площадь квадрата со стороной 4?", "answer": "16"},
        {"task": "Площадь прямоугольника 5x8?", "answer": "40"}],
    "Площадь2":[
        {"task": "Площадь треугольника с основанием 6 и высотой 10?", "answer": "30"},
        {"task": "Площадь круга радиусом 7?", "answer": "154"}
    ],
    "Корень1": [
        {"task": "Квадратный корень из 25?", "answer": "5"},
        {"task": "Квадратный корень из 100?", "answer": "10"}],
    "Корень2": [
        {"task": "Квадратный корень из 49?", "answer": "7"},
        {"task": "Квадратный корень из 16?", "answer": "4"}
    ],
    "Среднее арифметическое1": [
        {"task": "Среднее арифметическое 3, 4 и 5?", "answer": "4"},
        {"task": "Среднее арифметическое 10, 20 и 30?", "answer": "20"}],
    "Среднее арифметическое2": [
        {"task": "Среднее арифметическое 7, 10 и 13?", "answer": "10"},
        {"task": "Среднее арифметическое 15, 15 и 15?", "answer": "15"}
    ],
    "Факториал1": [
        {"task": "Факториал числа 5?", "answer": "120"},
        {"task": "Факториал числа 4?", "answer": "24"}],
    "Факториал2": [
        {"task": "Факториал числа 6?", "answer": "720"},
        {"task": "Факториал числа 0?", "answer": "1"}
    ]
}

count = 0  # User's score

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет! Погнали посмотрим что у тебя с математикой ?')
    bot.register_next_step_handler(message, sum)

def sum(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item_sum = types.InlineKeyboardButton('Сумма', callback_data='sum')
    markup.add(item_sum)
    bot.send_message(message.chat.id, 'Выбери навык:', reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == 'sum')#Эта строка определяет обработчик запроса  'sum'
def handle_sum_skill(call):
    task_list = tasks["Сумма1"]
    task = task_list.pop(0)#начинается с получения списка заданий для навыка "Сумма" и вывода на экран первого задания.
    bot.send_message(call.message.chat.id, task["task"])
    # Затем бот отправляет сообщение в чат с содержанием задачи и ожидает ответа пользователя.
    bot.register_next_step_handler(call.message, lambda message, task=task, task_list=task_list: check_sum1_answer(message, task, task_list))


#Далее определяется check_sum_answer функция, которая отвечает за сверку ответа пользователя с правильным ответом по Сумма1
def check_sum1_answer(message, current_task, task_list):
    global count
    if message.text == current_task["answer"]:
        count += 1
        bot.send_message(message.chat.id, f"Правильно! Твой счет: {count}")
    else:
        bot.send_message(message.chat.id, f"Неправильно! Твой счет: {count}")

    if task_list:
        task = task_list.pop(0)
        bot.send_message(message.chat.id, task["task"])
        bot.register_next_step_handler(message, lambda message, task=task, task_list=task_list: check_sum1_answer(message, task, task_list))
    else:
        bot.send_message(message.chat.id, "Продолжить на этом навыке?", reply_markup=generate_continue_markup())
        bot.register_next_step_handler(message, handle_sum1_continue_response)

#условие после 2 задач
def handle_sum1_continue_response(message):
    if message.text.lower() == "да":
        task_list = tasks["Сумма2"]
        task = task_list.pop(0)
        bot.send_message(message.chat.id, task["task"])
        bot.register_next_step_handler(message, lambda message, task=task, task_list=task_list: check_sum2_answer(message, task, task_list))
    else:
        bot.send_message(message.chat.id, f"Твой итоговый счет: {count} ")

def check_sum2_answer(message, current_task, task_list):
    global count
    if message.text == current_task["answer"]:
        count += 1
        bot.send_message(message.chat.id, f"Правильно! Твой счет: {count}")
    else:
        check_square_answer(message)

    if task_list:
        task = task_list.pop(0)
        bot.send_message(message.chat.id, task["task"])
        bot.register_next_step_handler(message, lambda message, task=task, task_list=task_list: check_sum2_answer(message, task, task_list))
    else:
        bot.send_message(message.chat.id, "Продолжить в этом навыке?", reply_markup=generate_continue_markup())
        bot.register_next_step_handler(message, handle_continue_response)

def handle_sum_skill(call):
    task_list = tasks["Сумма"]
    task_1 = task_list.pop(0)
    task_2 = task_list.pop(0)

    bot.send_message(call.message.chat.id, task_1["task"])
    bot.register_next_step_handler(call.message, lambda message, task=task_1, task_list=task_list: check_answer(message, task, task_list, task_2))

def check_answer(message, task_list):
    global count
    current_task = task_list.pop(0)
    if message.text == current_task["answer"]:
        count += 1
        bot.send_message(message.chat.id, f"Правильно! Твой счет: {count}")
    else:
        bot.send_message(message.chat.id, f"Неправильно! Твой счет: {count}")

    if task_list:
        bot.send_message(message.chat.id, "Продолжить в этом навыке?", reply_markup=generate_continue_markup())
        bot.register_next_step_handler(message, handle_continue_response)
    else:
        bot.send_message(message.chat.id, "Вопросы закончились.")

def generate_continue_markup():
    markup = types.InlineKeyboardMarkup(row_width=2)
    item_yes = types.InlineKeyboardButton('Да', callback_data='yes')
    item_no = types.InlineKeyboardButton('Нет', callback_data='no')
    markup.add(item_yes, item_no)
    return markup


def handle_continue_response(message):
    if message.text.lower() == "да":
        difference_skill(message)
    else:
        handle_square_skill(message)


@bot.callback_query_handler(func=lambda call: call.data == 'square')
def handle_square_skill(call):
    task_list = tasks["Корень"]
    task = task_list.pop(0)
    bot.send_message(call.message.chat.id, task["task"])
    bot.register_next_step_handler(call.message, lambda message, task=task, task_list=task_list: check_square_answer(message, task, task_list))

def check_square_answer(message, current_task, task_list):
    global count
    if message.text == current_task["answer"]:
        count += 1
        bot.send_message(message.chat.id, f"Правильно! Твой счет: {count}")
    else:
        bot.send_message(message.chat.id, f"Неправильно! Твой счет: {count}")

    if task_list:
        task = task_list.pop(0)
        bot.send_message(message.chat.id, task["task"])
        bot.register_next_step_handler(message, lambda message, task=task, task_list=task_list: check_square_answer(message, task, task_list))
    else:
        bot.send_message(message.chat.id, "Продолжить в этом навыке?", reply_markup=generate_continue_markup())
        bot.register_next_step_handler(message, handle_continue_response)

@bot.callback_query_handler(func=lambda call: call.data == 'difference')
def difference_skill(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    item_difference = types.InlineKeyboardButton('Разность', callback_data='difference')
    markup.add(item_difference)
    bot.send_message(message.chat.id, 'Следующий навык навык:', reply_markup=markup)

bot.polling(none_stop=True)




# # Function for the "Умножение" skill
# def multiplication_skill(message):
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     item_multiplication = types.InlineKeyboardButton('Умножение', callback_data='multiplication')
#     markup.add(item_multiplication)
#     bot.send_message(message.chat.id, 'Следующий навык навык:', reply_markup=markup)
#
#
# # Function for the "Деление" skill
# def division_skill(message):
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     item_division = types.InlineKeyboardButton('Деление', callback_data='division')
#     markup.add(item_division)
#     bot.send_message(message.chat.id, 'Следующий навык навык:', reply_markup=markup)
#
#
# # Function for the "Площадь" skill
# def area_skill(message):
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     item_area = types.InlineKeyboardButton('Площадь', callback_data='area')
#     markup.add(item_area)
#     bot.send_message(message.chat.id, 'Следующий навык навык:', reply_markup=markup)
#
#
# # Function for the "Корень" skill
# def square_skill(message):
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     item_square= types.InlineKeyboardButton('Корень', callback_data='square')
#     markup.add(item_square)
#     bot.send_message(message.chat.id, 'Следующий навык навык:', reply_markup=markup)
#
#
# # Function for the "Среднее арифметическое" skill
# def average_skill(message):
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     item_average = types.InlineKeyboardButton('Среднее арифметическое', callback_data='average')
#     markup.add(item_average)
#     bot.send_message(message.chat.id, 'Следующий навык навык:', reply_markup=markup)
#
#
# # Function for the "Факториал" skill
# def factorial_skill(message):
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     item_factorial = types.InlineKeyboardButton('Факториал', callback_data='factorial')
#     markup.add(item_factorial)
#     bot.send_message(message.chat.id, 'Следующий навык навык:', reply_markup=markup)






# @bot.message_handler(commands=['start'])
# def start(message):
#     bot.send_message(message.chat.id, 'Привет! Погнали посмотрим что у тебя с математикой ?')
#     bot.register_next_step_handler(message, sum)
# def handle_subtraction_skill(message):
#     markup = types.InlineKeyboardMarkup(row_width=2)
#     item_handle_subtraction_skill = types.InlineKeyboardButton('Разность', callback_data='handle_subtraction_skill')
#     markup.add(item_handle_subtraction_skill)
#     bot.send_message(message.chat.id, 'Следующий навык навык:', reply_markup=markup)
#
# @bot.callback_query_handler(func=lambda call: call.data == 'handle_subtraction_skill')
# def handle_subtraction_skill(call):
#     task_list = tasks["Разность"]
#     task = task_list.pop(0)
#     bot.send_message(call.message.chat.id, task["task"])
#     bot.register_next_step_handler(call.message, lambda message, task=task, task_list=task_list: check_subtraction_answer(message, task, task_list))
#
# def check_subtraction_answer(message, current_task, task_list):
#     global count
#     if message.text == current_task["answer"]:
#         count += 1
#         bot.send_message(message.chat.id, f"Правильно! Твой счет: {count}")
#     else:
#         bot.send_message(message.chat.id, f"Неправильно! Твой счет: {count}")
#
#     if task_list:
#         task = task_list.pop(0)
#         bot.send_message(message.chat.id, task["task"])
#         bot.register_next_step_handler(message, lambda message, task=task, task_list=task_list: check_subtraction_answer(message, task, task_list))
#     else:
#         bot.send_message(message.chat.id, "Продолжить в этом навыке?", reply_markup=generate_continue_markup())
#         bot.register_next_step_handler(message, handle_continue_response)
#
# # Добавьте аналогичную обработку для остальных навыков (Умножение, Деление и т.д.)
# # ...
#
# # Определение генерации клавиатуры "Продолжить"
# def generate_continue_markup():
#     markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
#     markup.add(types.KeyboardButton("Да"), types.KeyboardButton("Нет"))
#     return markup
#
# def handle_continue_response(message):
#     if message.text.lower() == "да":
#         # Вернуть пользователя к выбору навыка
#         sum(message)
#     else:
#         bot.send_message(message.chat.id, f"Твой итоговый счет: {count}")
#         # Здесь можно добавить логику для завершения бота или предоставления других опций
#
# # Запуск бота
# if __name__ == '__main__':
#     bot.polling(none_stop=True)