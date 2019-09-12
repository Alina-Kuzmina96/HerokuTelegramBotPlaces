import pymysql.cursors


def create_connection():
    return pymysql.connect(
        host='localhost',
        db='users',
        user='root',
        password='passw',
        cursorclass=pymysql.cursors.DictCursor
    )

def update(user_id, place_name, place_adress, place_latitude, place_longitude, place_image):
	connection = create_connection()
	try:
		cursor = connection.cursor()
		cursor.execute("INSERT INTO place (id, name, adress, latitide, longitude, image) VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" % (user_id, place_name, place_adress, place_latitude, place_longitude, place_image))
		connection.commit()
	finally:
		connection.close()

def list_places(message):
	connection = create_connection()
	try:
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM place WHERE id={}".format(str(message.chat.id)))
		results = cursor.fetchall()
	finally:
		connection.close()

	return results

def places(message, name):
	connection = create_connection()
	try:
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM place WHERE id='%s' AND name='%s'" % (message.chat.id, name))
		results = cursor.fetchall()
	finally:
		connection.close()
	return results

def search_place(message):
	connection = create_connection()
	try:
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM place WHERE id='%s' AND name='%s'" % (message.chat.id, message.text[7:]))
		results = cursor.fetchall()
	finally:
		connection.close()
	return results

def del_place(message):
	connection = create_connection()
	try:
		cursor = connection.cursor()
		cursor.execute("DELETE FROM place WHERE id='%s' AND name='%s'" % (message.chat.id, message.text[7:]))
		connection.commit()
	finally:
		connection.close()

def del_list(message):
	connection = create_connection()
	try:
		cursor = connection.cursor()
		cursor.execute("DELETE FROM place WHERE id='%s'" % message.chat.id)
		connection.commit()
	finally:
		connection.close()

def near_places(message):
	connection = create_connection()
	try:
		cursor = connection.cursor()
		cursor.execute("SELECT name, latitide, longitude FROM place WHERE id={}".format(str(message.chat.id)))
		results = cursor.fetchall()
	finally:
		connection.close()

	return results
