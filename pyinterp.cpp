/*
 * pyinterp.cpp
 *
 *  Created on: 15 апр. 2014 г.
 *      Author: a.teleshov
 *
 *  Программа вызывает интерпритатор питона и выполняет переданные скрипты
 */

#include "C:\Python27\include\Python.h"
#include <iostream>

void run_script(char *scrpt);

int main(int argc, char *argv[])
{
    int x;

    Py_SetProgramName(argv[0]); /* optional but recommended */
    Py_Initialize();

    run_script("example_2_power.py");

    std::cout<<"\n\n=========  Next script =========\n\n";

    run_script("example_1.py");

    Py_Finalize();

    std::cin >> x;
    return 0;
}

void run_script(char *scrpt)
{
    PyObject* PyFileObject = PyFile_FromString(scrpt, "r");
    if (PyFileObject)
    {
        if(!PyRun_SimpleFile(PyFile_AsFile(PyFileObject), scrpt))
            std::cout<<"=========  All right =========";
        else
            std::cout<<"=========== Some errors ==========";

    }
    else
    {
        std::cout << "Cannot open file\n";
    }
}
