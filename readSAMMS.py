# -*- coding: utf-8 -*-
"""
Created on Tue Dec 20 20:08:25 2016

@author: dbarn
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import re

file_name = "../../testData/1216mako_jos.txt";

event_id = 73;

f = open(file_name,'r');

curr_evt_id = -1;

for line in f:
    x = line;
    a = x.find("S.A.M.M.S.");
#    if (a>-1):
        # this is the start of a new page
    

    b = x.find("EVENT");
    
    if (b>-1):
        # this is the start of a new event
        # get the event ID
#        xp = re.compile('EVENT\\s+\\d+\\s')
#        xp = re.compile('EVENT')
        xl = x;
        xp = re.search('\\s+\\d+\\s', x)
        xa = xp.group(0).strip()
        evt_id = int(xa)
#        aa = xp.match(x)
        if evt_id != curr_evt_id:
            print x
            print xa
            curr_evt_id = evt_id
   #     else: 
          #  print 'No match'
        

f.close();
print 'Done\n';