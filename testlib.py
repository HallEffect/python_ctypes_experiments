#-*- coding: utf-8 -*-
from ctypes import *

#Объявляем тип указатель на c_int
c_int_pointer = POINTER(c_int)

#Объявляем стуктуру
class c_Foo(Structure):
	"""docstring for c_Foo"""
	_fields_=[("x",c_int),
              ("y",c_float),
              ("mas",c_int*10),
              ("p",c_int_pointer)]


i=c_int(10) # Переменной типа c_int присваиваем 10
print "Адрес переменной ",pointer(i),"\n" #Адрес переменной
g=c_int_pointer(i)# Объявляем указатель g, присваиваем адрес i
print "Адрес через тип указатель на c_int ",g,"\n"

#инициализируем переменную типа c_Foo
struc=c_Foo(5,
	        10,
	        (2,4,6,8),
	        pointer(i))

print struc.x, struc.y,struc.p, "\n"
print "Адрес массива",struc.mas, "\n" #Адрес первого элемета массива
print "3-й элемет массива",struc.mas[3]


#Подключаем библиотеку
c_testlib = cdll.LoadLibrary('./testlib.so')
#Объявляем функции
c_test=c_testlib.test
c_bar=c_testlib.bar

#Объявляем прототипы функций
c_test.restype=c_int
c_test.argtype=c_int

c_bar.restype=c_int_pointer
c_bar.argtypes=c_Foo,c_int_pointer

#Вызываем функции
print c_test(40)

blabla=c_bar(struc,g)
print blabla.contents
