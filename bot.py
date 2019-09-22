# -*- coding: utf-8 -*-

import telebot
from collections import defaultdict
from haversine import haversine


token = "972477502:AAG7SKlkGW7nKRPtiARgMgMXRJDywsyogBU" 
START, NAME, ADDRESS, LOCATION, PHOTO = range(5) #для очередности команд
USER_STATE = defaultdict(lambda: START)
PLACES = dict() #пока для списка мест

def get_state(message):
	#для получения статуса
	return USER_STATE[message.chat.id]

def update_state(message, state):
	#для обновления статуса
	USER_STATE[message.chat.id] = state

def update_place(user_id, val):
	#поиск мест, с неполными данными и добавление новых
	for key in PLACES:
		if key == user_id:
			l = 0
			for place in PLACES[key]:
				if len(place) < 5:
					l +=1
					place.append(val)
			if l == 0:
				PLACES[key].append([val])


bot = telebot.TeleBot(token)

@bot.message_handler(commands=['add']) #вызывается по команде
def handle_message(message):
	bot.send_message(message.chat.id,text='Напиши название твоего любимого места.')
	update_state(message, NAME)

@bot.message_handler(func=lambda message: get_state(message) == NAME) #вызывается только на определнном шаге
def handle_name(message):
	bot.send_message(message.chat.id,text='Укажи адрес.')
	update_state(message, ADDRESS)
	if message.chat.id not in PLACES:
		PLACES[message.chat.id] = [] #создаем ключ
	update_place(message.chat.id, message.text)

@bot.message_handler(func=lambda message: get_state(message) == ADDRESS)
def handle_address(message):
	bot.send_message(message.chat.id,text='Отправь свою локацию или слово "нет".')
	update_state(message, LOCATION)
	update_place(message.chat.id, message.text)

@bot.message_handler(func=lambda message: get_state(message) == LOCATION, content_types=['location', 'text'])
def handle_location(message):
	if message.text == None:
		loc = message.location #локация и далее координаты
		lat = loc.latitude
		lon = loc.longitude
		bot.send_message(message.chat.id,text='Отправь, по желанию, фото. Или слово "нет".')
		update_state(message, PHOTO)
		update_place(message.chat.id, lat)
		update_place(message.chat.id, lon)
	else:
		if message.text.lower() == 'нет':
			lat = 'нет'
			lon = 'нет'
			bot.send_message(message.chat.id,text='Отправь, по желанию, фото. Или слово "нет".')
			update_state(message, PHOTO)
			update_place(message.chat.id, lat)
			update_place(message.chat.id, lon)
		else:
			bot.send_message(message.chat.id,text='Неправильно введенные данные. Попробуй снова.')

	
@bot.message_handler(func=lambda message: get_state(message) == PHOTO, content_types=['photo', 'text'])
def handle_photo(message):
	if message.text == None:
		file_info = bot.get_file(message.photo[0].file_id)
		downloaded_file = bot.download_file(file_info.file_path)

		src = "images\\" + str(message.photo[0].file_id)
		with open(src, 'wb') as new_file:
			new_file.write(downloaded_file)
		update_place(message.chat.id, str(message.photo[0].file_id))
		bot.send_message(message.chat.id,text='Ваше любимое место сохранено.')
		update_state(message, START)
	else:
		if message.text.lower() == 'нет':
			update_place(message.chat.id, 'нет')
			bot.send_message(message.chat.id,text='Ваше любимое место сохранено.')
			update_state(message, START)
		else:
			bot.send_message(message.chat.id,text='Неправильно введенные данные. Попробуй снова.')


@bot.message_handler(commands=['list']) 
def handle_message(message):
	if message.chat.id in PLACES:
		if len(PLACES[message.chat.id]) != 0:
			for lst in PLACES[message.chat.id]:
				bot.send_message(message.chat.id,text=lst[0])
		else:
			bot.send_message(message.chat.id,text='Список мест пуст')
	else:
		bot.send_message(message.chat.id,text='Список мест пуст')


@bot.message_handler(commands=['place'])
def handle_message(message):
	name = message.text[7:]
	if message.chat.id in PLACES:
		if len(PLACES[message.chat.id]) != 0:
			for lst in PLACES[message.chat.id]:
				if lst[0] == name:
					bot.send_message(message.chat.id,text="адрес: " + lst[1])
					if lst[2] != 'нет':
						bot.send_location(message.chat.id, float(lst[2]), float(lst[3]))
					if lst[4] != 'нет':
						photo = open("images\\" + lst[4], 'rb')
						bot.send_photo(message.chat.id, photo)
				else:
					bot.send_message(message.chat.id,text='Такое место не найдено.')
	else:
		bot.send_message(message.chat.id,text='Такое место не найдено.')


@bot.message_handler(commands=['reset'])
def handle_message(message):
	if len(message.text) > 6:
		name = message.text[7:]
		if message.chat.id in PLACES:
			if len(PLACES[message.chat.id]) != 0:
				del_lst = -1
				for i in range(len(PLACES[message.chat.id])):
					if PLACES[message.chat.id][i][0] == name:
						del_lst = i
				if del_lst != -1:
					PLACES[message.chat.id].pop(del_lst)
					bot.send_message(message.chat.id,text='Место {} удалено.'.format(name))
				else:
					bot.send_message(message.chat.id,text='Такое место не найдено.')
	else:
		if message.chat.id in PLACES:
			PLACES[message.chat.id].clear()
		bot.send_message(message.chat.id,text='Список мест очищен.')

@bot.message_handler(content_types=['location'])
def handle_location(message):
		loc = message.location #локация и далее координаты
		lat1 = loc.latitude
		lon1 = loc.longitude
		i = 0
		if message.chat.id in PLACES:
			if len(PLACES[message.chat.id]) != 0:
				for row in PLACES[message.chat.id]:
					if row[2] != 'нет':
						i += 1
						lat2 = row[2]
						lon2 = row[3]
						if haversine(lat1, lon1, lat2, lon2) <= 1:
							bot.send_message(message.chat.id,text=row[0])
			else:
				bot.send_message(message.chat.id,text='Ваш список мест пуст.')
		if i == 0:
			bot.send_message(message.chat.id,text='Ближайших мест не найдено.')

@bot.message_handler()
def handle_message(message):
	#вызывается, на любое сообщение кроме команд
	bot.send_message(message.chat.id,text='Возможности нашего бота:\n/add - добавить любимое место;\
		\n/list - список мест;\n/place название - подробная информация по заданному месту;\n/reset -\
		удаление всех мест;\n/reset название - удаление конкретного места;\nОтправьте свою геопозицию и получите список ближайщих к вам мест.')



bot.polling()