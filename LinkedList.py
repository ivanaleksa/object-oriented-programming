""" Представление двусвязного списка двумя классами ListObj - отдельный элемент списка, ListAll - структура данных """

class ListObj:
	""" Есть два приватных локальных атрибута: next - ссылка на следующий элемент, prev - ссылка на пред. элемент.
	Обращение к ним происходит при помощи интерфейсных классов NameObj.next и NameObj.prev """
	
	def __init__(self, data):
		self.__prev = None
		self.__next = None
		self.__data = data
		self.__indx = 0

	@property
	def prev(self):
		return self.__prev
	@prev.setter
	def prev(self, obj):
		if type(obj) is ListObj or obj == None:
			self.__prev = obj
		else:
			raise ValueError("Sorry, object must be ListObj")
	
	@property
	def next(self):
		return self.__next
	@next.setter
	def next(self, obj):
		if type(obj) is ListObj or obj == None:
			self.__next = obj
		else:
			raise ValueError("Sorry, object must be ListObj")

	@property
	def data(self):
		return self.__data
	@data.setter
	def data(self, data):
		self.__data = data
	
	@property
	def indx(self):
		return self.__indx
	@indx.setter
	def indx(self, indx):
		self.__indx = indx

	


class ListAll:
	""" Основной класс, работающий с объектами класса ListObj
	Методы класса: add_obj - добавляет элемент в конец списка, pop - удаляет элемент с конца списка из возвращает его,
	find - возвращает элемент по его индексу, get_data - возвращает все объекты из списка, get_count - возвращает
	размер списка, insert - добавляет элемент в список по идексу, delete - удаляет элемент по индексу, swap - 
	меняет два элемента местами """
	
	def __init__(self):
		self.__head = None
		self.__tail = None
		self.__count = 0

	def add_obj(self, obj):
		if self.__head == None:
			self.__head = self.__tail = obj
			self.__head.indx = self.__count
			self.__count += 1
		else:
			self.__tail.next = obj
			obj.prev = self.__tail
			self.__tail = obj
			self.__tail.next = None
			self.__tail.indx = self.__count
			self.__count += 1

	def pop(self):
		info = self.__tail
		self.__tail = self.__tail.prev
		return info

	def find(self, indx):
		tmp = self.__head
		while True:
			try:
				if tmp.indx == indx:
					return tmp
				tmp = tmp.next
			except:
				raise IndexError("Вы ввели недопустимый индекс")

	def get_data(self):
		res = list()
		tmp = self.__head
		while True:
			try:
				res.append((tmp.data, tmp.indx))
				tmp = tmp.next
			except:
				break
		return res

	def get_count(self):
		return self.__count

	def insert(self, indx, obj):
		if indx > self.__count or indx < 0:
			raise IndexError("Вы ввели неверный индекс")
		elif indx == self.__count:
			obj.prev = self.__tail
			obj.indx = indx
			self.__tail.next = obj
			self.__count += 1
		elif indx == 0:
			self.__head.prev = obj
			obj.next = self.__head
			self.__head = obj
			self.__head.indx = -1
			self.__count += 1
			tmp = self.__head
			while True:
				tmp.indx += 1
				if tmp.next is None:
					break
				tmp = tmp.next
		else:
			i = 0
			tmp = self.__head
			self.__count += 1
			while i < self.__count:
				if i == indx:
					obj.prev = tmp.prev
					obj.next = tmp
					obj.indx = indx
					tmp.prev.next = obj
					tmp.prev = obj
					while True:
						tmp.indx += 1
						if tmp.next is None:
							break
						tmp = tmp.next
					break
				tmp = tmp.next
				i += 1

	def delete(self, indx):
		pass

	def swap(self, indx1, indx2):
		pass


lst = ListAll()
obj1 = ListObj("One")
obj2 = ListObj("Two")

lst.add_obj(obj1)
lst.add_obj(obj2)
lst.add_obj(ListObj("Hi there!"))
lst.add_obj(ListObj("Hi there! second"))

print(lst.get_data())
lst.insert(1, ListObj("i was inserted"))
lst.insert(0, ListObj("I was inserted! zero"))
lst.insert(lst.get_count(), ListObj("I was inserted! last"))

print(*lst.get_data(), sep="\n")