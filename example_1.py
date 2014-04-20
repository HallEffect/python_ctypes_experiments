#-*- coding:utf-8 -*-
from ctypes import *                    # Для работы с си
import pdb                              # Модуль отладчика


###################################################
#
# Примеры работы с сишными типами в питоне
#
###################################################
print "\n\n======= Работы с сишными типами в питоне =======\n"

c_int_pointer = POINTER(c_int)                  # Объявляем тип указатель на c_int
c_int_null_pointer = POINTER(c_int)()           # Создание пустого указателя
c_pointer_pointer = POINTER(POINTER(c_int))     # Объявляем тип указатель на указатель на c_int

#Объявляем стуктуру
class c_Foo(Structure):
    """docstring for c_Foo"""
    _fields_ = [("x", c_int),
                ("y", c_float),
                ("mas", c_int * 10),             # Объявление массива вида  c_type * количество_элементов
                ("p", c_int_pointer)]

#pdb.set_trace()
i = c_int(1)                                     # Переменной типа c_int присваиваем 1
print i                                          # On platforms where sizeof(int) == sizeof(long) it is an alias to c_long.
print i.value + 23                               # Для работы с сишными типами нужно вызывать атрибут value
print u"Адрес переменной: ", pointer(i), "\n"    # Адрес переменной
g = c_int_pointer(i)                             # Объявляем указатель g, присваиваем адрес i
p = pointer(g)                                   # Указатель на указатель g

# Указатели ссылаются на разные области памяти, т.е.
# p.contents != g, но p.contents.contents == g.contents

print u"Адрес через тип указатель на c_int: ", g, "\n"
print u"Доступ через указатель: ",p.contents.contents     # Доступ к содержимому через указатель на указатель

print u"Вывод содержимого по адресу разными способами: ", g[0], g.contents, g.contents.value, "\n"
# Вывод содержимого по адресу разными способами:  1 c_long(1) 1

g.contents=c_int(10)                             # Изменение содержимого по адресу через преобразование типа
g[0]=100                                         # Изменение содержимого по адресу



# x=0
# while (1):                                     # Ничего не происходит
#     g[x]=x
#     x=+1

# Инициализируем переменную типа c_Foo
struc = c_Foo(5,
              15,
              (2, 4, 6, 8),
              pointer(i)
)

print u"Адрес массива объявленного в структуре:", struc.mas, "\n"
print u"4-й элемет массива объявленного в структуре:", struc.mas[3]




###################################################
#
# Примеры вызова и работы с сишными функциями
#
###################################################
print u"\n\n\n======= Вызов и работы с сишными функциями =======\n"

# Подключаем библиотеку
c_testlib = CDLL('clib.dll')
# Объявляем функции
c_test = c_testlib.test
c_bar = c_testlib.bar

# Объявляем "прототипы" функций
c_test.restype = c_int_pointer      # Что возвращаем
c_test.argtype = c_int              # Что передаем

c_bar.restype = c_int_pointer
c_bar.argtypes = c_Foo, c_int_pointer

# Вызываем функцию, которая возвращает указатель на динамически созданный массив из 15 элементов
arr = c_test(15)
print u"Указатель на массив, cозданный в плюсовой библиотеке: ", arr

# Создаем список, содержащий элементы созданного в плюсовой библиотеке массива.
list = [arr[x] for x in xrange(0, 15)]
print u"Созданный в плюсовой библиотеке массив:", list

# Функция возвращает указатель на 4 элемент созданного в плюсовой библиотеке clib.cpp динамического массива
# через указатель arr
blabla = c_bar(struc, arr)
#Печатаем содержимое по указанному адресу
print u"Четвертый элемент массива, полученный через указатель в плюсовой библиотеке", blabla.contents.value




###################################################
#
# Пример работы с передачей питоновской функции в качестве
# аргумента для сишной функции
#
###################################################
print u"\n\n\n======= Работы с передачей питоновской функции в качестве аргумента для сишной функции =======\n"

def somefunction():
    print u"\nCall function from python\n"

CWRAPPER = CFUNCTYPE(None)                      # Определяем прототип функции в соответствии с определением в clib.cpp
wrapped_py_func = CWRAPPER(somefunction)        # Создаем обертку для питоновской функции в соответстви с прототипом
print u"Адрес функции:",wrapped_py_func
c_testlib.mainfunction(wrapped_py_func)         # Вызываем функцию из clib.cpp, которой передаем указатель
                                                # на питоновскую функцию




###################################################
#
# Примеры импорта и работы с глобальными переменными
#
###################################################
print u"\n\n\n======= Импорт и работа с глобальными переменными =======\n"

c_some_var=c_int.in_dll(c_testlib, "some_var")                   # тип_переменной.in_dll(библиотека, "переменная")
print u"Импортированная глобальная переменная: ",c_some_var.value
c_some_pointer=c_int_pointer.in_dll(c_testlib, "some_pointer")
print u"Импортированные указатель на глобальную переменную",c_some_pointer
print u"Значение через импортированный указатель",c_some_pointer.contents.value




###################################################
#
# Примеры работы с сишными классами
#
###################################################
print u"\n\n\n======= Работа с классами =======\n"

class c_Myclass(object):                                    # Определяем класс в соответствии с Myclass в clib.cpp
    def __init__(self,x):
        # Конструктор
        c_testlib.new_Myclass.argtype = c_int               # Что передаем
        c_testlib.new_Myclass.restype = c_void_p            # Что возвращаем (указатель)

        # Метод
        c_testlib.MyAdd.argtypes = c_void_p,c_int,c_int
        c_testlib.MyAdd.restype = c_int

        self.obj = c_testlib.new_Myclass(x)                 # Получение указателя на новый объект класса

       # self.z = c_testlib.returnz(self.obj)               # Если z объявлена как int z без модификаторов
                                                            # static, const в классе в clib.cpp


    z = c_testlib.returnz()                                 # Получение значения переменной-члена z
                                                            # Определена как const static int z = 10;

    def FunAdd(self, a, b):
        return c_testlib.MyAdd(self.obj, a, b)

my_obj = c_Myclass(4)
print my_obj.FunAdd(10,2)                                   # Возвращает (10/2)*4 = 20
print my_obj.z                                              # Возвращает 10

my_new_obj = c_Myclass(4)
print my_new_obj.z                                          # Возвращает 10

my_new_obj.z = 555
print my_new_obj.z                                          # Возвращает 555
print my_new_obj.__class__.z                                # Возвращает 10

my_new_obj.__class__.z=999

print my_new_obj.__class__.z                                # Возвращает 999
print my_obj.__class__.z                                    # Возвращает 999







###################################################
#
# Обработка сишных исключений
#
###################################################
print u"\n\n\n======= Работа с исключениями =======\n"

my_another_class = c_Myclass(4)
try:                                                        # Проверка обработки исключения деления на ноль (10/0)*4
    var = my_another_class.FunAdd(10,0)                     # Должны передавать две переменные типа int

except OSError:                                             # Системные ошибки. Ошибка вида:
                                                            # "WindowsError: exception: integer divide by zero"
    print u"Деление на 0"
except ArgumentError:                                       # Если передаем переменную неправильного типа
    print u"Неправильный тип данных"
except Exception:                                           # Если неизветное исключение
    print u"Какая-то неизвестная ошибка"
else:                                                       # Выполняется если исключений нет
    print u"Ошибок нет"
finally:                                                    # Выполняется всегда
    print u"Все ошибки обработаны"
