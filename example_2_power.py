#-*- coding: cp866 -*-
from ctypes import *
import random
import pdb
def power(a,b):
    print "power(",a,b,")=",a**b
foo=100
pdb.set_trace()
a=[random.randint(1,5) for x in range(0,10)]
b=[random.randint(1,5) for x in range(0,10)]

for x in  range(0,10):
    power(a[x],b[x])
