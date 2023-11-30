import telebot
from telebot import types
import random

participants_id = []
participants_info = {}

f = open('Participants_info.txt', 'r')

participants_id = list(map(int, f.readline().split()))

if participants_id != []:
    for i in f.read().split('\n'):
        info = i.split()
        participants_info[int(info[0])] = info[1]

f.close()
    
TOKEN = "6519373439:AAFHXcpoZSf04lEifthTh587SEFWjYdEFuQ"
admin_id = 1405904438

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    markup = types.InlineKeyboardMarkup()
    participate_button = types.InlineKeyboardButton("Участвовать", callback_data='participate')
    decline_button = types.InlineKeyboardButton("Отказаться", callback_data='decline')
    markup.add(participate_button, decline_button)

    bot.send_message(user_id, 'Нажмите на кнопку, чтобы участвовать в тайном Санте или отказаться от участия.', reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == 'participate')
def participate(message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    if user_id in participants_id:
        bot.send_message(user_id, "Вы уже участвует в тайном санте")
    else:
        participants_id.append(user_id)
        participants_info[user_id] = username
        
        bot.send_message(user_id, "Вы успешно зарегистрированы для участия в тайном Санте!")
        if user_id != admin_id:
            bot.send_message(admin_id, f"Пользователь @{username} зарегистрирован для учатия в Тайном Санте")
        
        f = open('Participants_info.txt', 'w')
        f.write(' '.join(list(map(str, participants_id))) + "\n")
        f.write("\n".join([str(i) + " " + participants_info[i] for i in participants_id]))
        f.close()
        
    print(participants_id)

@bot.callback_query_handler(func=lambda call: call.data == 'decline')
def decline(message):
    user_id = message.from_user.id
    username = message.from_user.username
    
    if user_id == admin_id:
        bot.send_message(user_id, "Ты че охуела?")
    elif (user_id in participants_id) and user_id != admin_id:
        participants_id.remove(user_id)
        participants_info.pop(user_id)
        
        bot.send_message(user_id, "Вы больше не участвуете в Тайном Санте")
        if user_id != admin_id:
            bot.send_message(admin_id, f"Пользователь @{username} больше не участвует в Тайном Санте")
        
        f = open('Participants_info.txt', 'w')
        f.write(' '.join(list(map(str, participants_id))) + "\n")
        f.write("\n".join([str(i) + " " + participants_info[i] for i in participants_id]))
        f.close()
    else: 
        bot.send_message(user_id, "Вы и так не участвуете в Тайном Санте")

@bot.message_handler(commands=['info'])
def info(message):
    user_id = message.from_user.id
    print(participants_info)
    if user_id == admin_id:
        bot.send_message(admin_id, "В тайном санте участвуют: \n" + 
                         "\n".join([str(i) + ": @" + participants_info[i] for i in participants_id]))
    else:
        bot.send_message(user_id, "У вас нет на это прав")
        
@bot.message_handler(commands=['SecretSanta'])
def start(message):
    user_id = message.from_user.id
    if user_id == admin_id:
        if len(participants_id) == 1:
            bot.send_message(admin_id, "Слишком мало человек для проведения Тайного Санта") 
        
        else:
            shuffled_list = random.sample(participants_id, len(participants_id))

            f = open('SecretSanta.txt', 'w')
            for i in range(len(shuffled_list)):
                bot.send_message(shuffled_list[i], f"Поздравляю тебе достался @{participants_info[shuffled_list[(i + 1) % len(shuffled_list)]]}")
                f.write(str(shuffled_list[i]) + '\n')
            f.close()
        
    else:
        bot.send_message(user_id, "У вас нет на это прав")
    
bot.polling()