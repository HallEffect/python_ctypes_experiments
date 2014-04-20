/*
 * clib.cpp
 *
 *  Created on: 11 апр. 2014 г.
 *      Author: a.teleshov
 *
 *  DLL для питоновского скрипта
 */

#include <new>

struct foo
{
        int x;
        float y;
        int mas[10];
        int* p;
};



/*
 * Глобальные переменные, экспортируемые в питоновский скрипт
 */
int some_var = 666;
int* some_pointer = &some_var;



/*
 * Функция возвращает указатель на динамический массив размера x
 */
extern "C" int* test(int x)
{
    int* p = new int[x];

    for (int i = 0; i < x; i++)
        p[i] = i;
    return p;
}



/*
 * Функция возвращает адрес четвертого элемента динамического массива.
 * Массив передается через указатель, foo str - пока не используется
 */
extern "C" int* bar(struct foo str, int* pointer_pamameter)
{
    int k = *pointer_pamameter;
    k += 3;
    return &k;
}




/*
 * Функция выполняет питоновскую функцию, переданную через указатель
 */
typedef void (*callback)();	                // Определяем указатель callback на функцию, возвращающую void
extern "C" void mainfunction(void *F)
{
    ((callback) F)();						// Вызываем функцию
}




/*
 * Класс, новые объекты которого создаются в питоне
 */
class Myclass
{
    public:
        Myclass(int);
        int Add(int, int);
        const static int z=10;
    private:
        int c_;
};



int Myclass::Add(int a, int b)
{
    return (a/b)*c_;                            // Проверим работу исключений при делении на 0
}

Myclass::Myclass(int c)                         //Конструктор
{
    c_=c;
}

extern "C" Myclass* new_Myclass(int c)          // Функция для экспортирования в питон, для выделения памяти под новый объект класса
{
    return new Myclass(c);
}

extern "C" int MyAdd(Myclass* My,int a, int b)  // Функция для экспортирования в питон, метод класса
{
    return My->Add(a, b);
}

extern "C" int returnz()                         // Функция для экспорта переменной-члена z
{
    return Myclass::z;
}

/*
 *  Если z объявлена не как const static int z=10;
 */
//extern "C" int returnz(Myclass* My)             // Функция для экспорта переменной-члена z
//{
//    return My->z;
//}
