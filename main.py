
import telebot
from telebot import types

import requests
import time
import json

bot = telebot.TeleBot("5472577186:AAHN1SfBmOUWVkV0B0NDCEDIuis5YPD7ng8");

def getPromocodeFunction(message = None):
	if message != None:
		# load
		bot.send_message(message.chat.id, "Идет поиск промокода...", parse_mode='HTML')
		time.sleep(2)

		# promo get from website

		promo = requests.post('https://proorganic.info/api/getPromoCode', data={'chat_id': message.chat.id})
		link = requests.post('https://proorganic.info/api/getRefLink')

		if (promo.status_code == 200):
			if (promo.text != 'error'):

				# bots information send
				bot.send_message(message.chat.id,
								 "Ваш секретный прокод успешно найден! Он проверен, актуален и активен! Ваш промокод:",
								 parse_mode='HTML')
				bot.send_message(message.chat.id, '<b>' + promo.text + '</b>', parse_mode='HTML')

				inline_kb_full = types.InlineKeyboardMarkup(row_width=1)
				inline_kb_full.add(types.InlineKeyboardButton('Перейти на сайт', url=link.text))

				bot.send_message(message.chat.id,
								 "Для применения данного промокода необходимо: \n1️⃣ Скопируйте промокод, который вы получили в данном боте \n2️⃣ После того как вы собрали товары в корзину, в корзине в окне 'применить промокод' вставьте полученный промокод \n3️⃣  Нажмите кнопку 'Применить' для активации промокода \n4️⃣ Ваша скидка Активирована, можете дальше продолжить оформление заказа \n5️⃣ Данный промокод можно использовать на несколько заказов",
								 parse_mode='HTML', reply_markup=inline_kb_full)
				bot.send_message(message.chat.id, "Перейти на сайт IHerb: " + link.text, parse_mode='HTML')
			else:
				bot.send_message(message.chat.id,
								 "Извините, промокод не найден. Попробуйте позже!",
								 parse_mode='HTML')
		else:
			bot.send_message(message.chat.id,
							 "Извините во время поиска возникли проблемы, попробуйте воспользователься ботом через 15 минут",
							 parse_mode='HTML')


@bot.message_handler(commands=['promocode'])
def promocode(message):
	functionGet = getPromocodeFunction(message)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	check_phone_user = requests.post('https://proorganic.info/api/checkUserChatId', data= {'chat_id' : message.chat.id})

	if(check_phone_user.text == '200_New_User'):
		keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		button_phone = types.KeyboardButton(text="📞 Поделиться номером", request_contact=True)
		keyboard.add(button_phone)

		bot.send_message(message.chat.id, 'Привет, рады что Вы решили обратиться к нам. Мы - уникальная система промокодом IHerb, которая поможет тебе получить свой промокод для заказа на сайте и/или в приложение.', parse_mode='HTML');
		bot.send_message(message.chat.id, "Для начала давай проверим впервые ли Вы с нами, нажмите \"Поделиться номером\"", reply_markup=keyboard)

	else:
		keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		button_phone = types.KeyboardButton(text="✅ Получить промокод")
		keyboard.add(button_phone)

		bot.send_message(message.chat.id, 'Выберите что вас интересует?  Если вас интересует код на максимальную скидку нажмите кнопку <i>"Получить промокод"</i> или напишите <b>promo</b>',parse_mode='HTML', reply_markup=keyboard)

@bot.message_handler(content_types=["contact"])
def check(message):
	# # print(message.contact.phone_number)
	if(message.contact.phone_number.find('+') == -1):
		phone = '+' + message.contact.phone_number
	else:
		phone = message.contact.phone_number
	name = ''

	if(message.from_user.first_name): name += ' ' + message.from_user.first_name
	if(message.from_user.last_name): name += ' ' + message.from_user.last_name

	userData = {
		'phone'  : phone,
		'name'   : name,
		'user_id': message.from_user.id,
		'chat_id': message.chat.id
	}
	check_phone_user =  requests.post('https://proorganic.info/api/checkUser', data = userData)
	if(check_phone_user.text):
		keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
		button_phone = types.KeyboardButton(text="✅ Получить промокод")
		keyboard.add(button_phone)

		bot.send_message(message.chat.id, 'Выберите что вас интересует?  Если вас интересует код на максимальную скидку нажмите кнопку <i>"Получить промокод"</i> или напишите <b>promo</b>', parse_mode='HTML' , reply_markup=keyboard)

@bot.message_handler(content_types=["text"])
def textVallue(message):
	if(message.text == '✅ Получить промокод'):
		functionGet = getPromocodeFunction(message)

	elif (message.text.lower() == 'promo'):
		functionGet = getPromocodeFunction(message)
	else:
		bot.send_message(message.chat.id, "Извините я вас не понимаю, что вы имеете ввиду")


bot.infinity_polling()