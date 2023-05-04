import telebot
import nn
import os
from time import sleep


TOKEN = 'TOKEN'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.from_user.id, "Привет, пользователь!")

@bot.message_handler(commands=['help'])
def help_handler(message):
    bot.send_message(message.from_user.id, "Ты можешь присылать мне картинки, чтобы я определил, кошка или собака на ней")

@bot.message_handler(commands=['calc'])
def calc_handler(message):
    text = message.text[6:]

    bot.reply_to(message, text)

@bot.message_handler(content_types=['photo'])
def photo_handler(message):
    
    path = r'C:\Users\V\Documents\images'
    directory = path + f'{message.from_user.id}/'
    
    if os.path.exists(directory) == False:
        os.mkdir(directory)
    
    photo = message.photo[-1]
    file_id = photo.file_id
    file_path = bot.get_file(file_id).file_path
    name = file_id + ".jpg"
    downloaded_file = bot.download_file(file_path)
    new_file = open(directory + name, mode='wb')
    new_file.write(downloaded_file)
    new_file.close()
        
    res = nn.predict_img_from_dir(directory, name)
    reply = 'На картинке изображена {} с уверенностью в {}%'
    if res['собака'] > res['кошка']:
        label, sureness = 'собака', res['собака']
    else:
        label, sureness = 'кошка', res['кошка']
    
    sureness *= 100
    bot.reply_to(message, reply.format(label, sureness))
    
@bot.message_handler(content_types=['voice'])
def handler(message):
    bot.send_message(message.chat.id, 'Напиши словами, я не могу слушать')

@bot.message_handler(func=lambda m: True)
def all_handler(message):
    text = message.text
    if 'привет' or 'как дела' in text.lower():
        if 'привет' in text.lower():
            bot.send_message(message.from_user.id, "приветики")
        if 'как дела' in text.lower():
            bot.send_message(message.from_user.id, "хорошо)")
    else:
        bot.send_message(message.from_user.id, "Я могу принимать только картинки")

@bot.message_handler(content_types=['dice'])
def dice_handler(message):
    dice = message.dice
    value = dice.value
    sleep(6)
    bot.send_message(message.from_user.id, "Вам выпадает {}".format(value))
    if value <= 3:
        bot.send_message(message.from_user.id, "Ha!!!")
        bot.send_message(message.from_user.id, "Loser!")
    else:
        bot.send_message(message.from_user.id, "Wow!!!")
        bot.send_message(message.from_user.id, "You won")

bot.polling()
