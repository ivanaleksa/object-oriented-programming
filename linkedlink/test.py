from LinkedList import ListAll, ListObj

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
lst.swap(0, lst.get_count())

print(*lst.get_data(), sep="\n")