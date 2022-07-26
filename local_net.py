from copy import copy

class Router:
	instance = None  # ссылка на объект роутера
	connected_servers = list()  # список подкюченных серверов

	def __new__(cls, *args, **kwargs):
		""" в случае, если будет попытка создать второй объект класса, то он не будет создан, а будет ссылаться
		на уже существующий объект """
		
		if cls.instance == None:
			cls.instance = super().__new__(cls)
		return cls.instance

	def __init__(self):
		self.buffer = list()  # буффер роутера, содержит объекты класса Data

	@classmethod
	def link(cls, server):
		""" метод добавляет сервер в список подключенных серверов в случае, если он уже на находится там """
		
		if server not in cls.connected_servers:
			cls.connected_servers.append(server)
			print(f"Сервер {server} подключен к роутеру")
		else:
			print(f"Сервер {server} уже был подключен к серверу")

	@classmethod
	def unlink(cls, server):
		""" метод удаляет сервер из списка подключенных серверов, в случае если он поключен к роутеру """
		
		if server in cls.connected_servers:
			del cls.connected_servers[cls.connected_servers.index(server)]
			print(f"Сервер {server} был отключен от роутера")
		else:
			print(f"Сервер {server} не был подключен к роутеру")

	def send_data(self):
		new_buffer = copy(self.buffer)
		self.buffer.clear()
		for server in Router.connected_servers:
			for message in new_buffer:
				if message.ip == server.get_ip():
					server.add_in_buffer(message)
		print("Все сообщения были отправлены")

	def add_in_buffer(self, data):
		self.buffer.append(data)

	@classmethod
	def get_connected_servers(cls):
		return cls.connected_servers



class Server:
	k = 0

	def __new__(cls):
		cls.k += 1
		return super().__new__(cls)

	def __init__(self):
		self.buffer = list()
		self.ip = Server.k

	def send_data(self, data):
		if self in Router.get_connected_servers():
			Router.add_in_buffer(Router.instance, data)
			print(f"Добавил {data.data} в буфер роутера")

	def get_data(self):
		datas = copy(self.buffer)
		self.buffer.clear()
		return datas

	def get_ip(self):
		return self.ip

	def add_in_buffer(self, data):
		self.buffer.append(data)


class Data:
	""" Объект класса Data содержит поля data и ip сервера, на который нужно доставить информацию """

	def __init__(self, data, ip):
		self.data = data
		self.ip = ip


""" тест работы классов """

# создание роутера и трёх серверов
router = Router()
server1 = Server()
print(f"ip сервера 1: {server1.ip}")
server2 = Server()
print(f"ip сервера 2: {server2.ip}")
server3 = Server()
print(f"ip сервера 3: {server3.ip}")

# подключение трёх созданных серверов к роутеру
router.link(server1)
router.link(server2)
router.link(server3)
router.link(server3)

# отправка сообщений от сервера к роутеру
server1.send_data(Data("сообщение от сервера 1", server3.get_ip()))
server1.send_data(Data("сообщение от сервера 2", server3.get_ip()))
print(f"Буфферо роутера, после получения двух сообщений {router.buffer}")
print(f"Буффер 3 сервера до отправки роутером сообщений {server3.buffer}")

# отправка сообщений от роутера серверам
router.send_data()

# получение сообщений с сервера
print(f"Буфферо роутера, после отправки двух сообщений {router.buffer}")
print(f"Буффер 3 сервера после отправки роутером сообщений {server3.buffer}")
print(server3.get_data())
print(f"Буффер 3 сервера после получения сообщений {server3.buffer}")