# -*- coding: utf-8 -*-
"""
Created on Thu May  1 22:02:07 2014
Project	:Python-Project
Version	:0.0.1
@author	:macrobull

"""

from pylab import *


tm = 65536
l = 1024

t = linspace(0,2*pi,l)

d = tm*(sin(t)*0.5+0.5)

d = array(d, dtype='int')

#for x in d: print x, ','

plot([(d[(i << 1) & 1023]>>9)+100 for i in xrange(0xffff)])

show()

