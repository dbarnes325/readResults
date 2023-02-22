# -*- coding: utf-8 -*-
"""
Created on Wed Feb 08 23:00:21 2017

@author: dbarn
"""

import numpy as np
import math
import matplotlib.pyplot as plt
import re

# None on USA Swimming ID number:
# Format is:
# date of birth + first 3 letters
#	  of legal first name + middle initial + first 4 letters of last 
#	  name. In the event that there is no middle initial or not enough
#	  letters in the first or last name to fill the field, an asterisk
#	  will be used. Special characters are removed. 
#	  Examples: Catherine A. Durance = 011553CATADURA
#		    Cy V. Young          = 091879CY*VYOUN
#		    Thomas Chu           = 020981THO*CHU*
#		    Ty Lee               = 011873TY**LEE*
#		    Dave T. O'Neil       = 030367DAVTONEI


# create container classes
class Swimmer:
    def __init__(self):
        self.name = ''
        self.uss = ''
        self.attached =''
        self.citizen = ''
        self.bdate =''
        self.ageClass = ''
        self.mf = ''

    def print(self):
        print(f'----- Swimmer Record: -----')
        print(f'Name:  {self.name}')
        print(f'USS:   {self.uss}')
        print(f'ATT:   {self.attached}')
        print(f'CIT:   {self.citizen}')
        print(f'BDate: {self.bdate}')
        print(f'Age:   {self.ageClass}')
        print(f'M/F:   {self.mf}')
        
# STROKE Code 012   Event Stroke code
#	       1    Freestyle
#	       2    Backstroke
#	       3    Breaststroke
#	       4    Butterfly
#	       5    Individual Medley
#	       6    Freestyle Relay
#	       7    Medley Relay
        
class Event:
    def __init__(self):
        self.distance = 0
        self.stroke = 0 
        self.course = 0 # 1 or S SCM, 2 or Y SCY, 3 or L LCM
        self.mfe = ''
        self.minAge = 0
        self.maxAge = 0
        
#    def __init__(self,dist,stroke,course,mfe):
#        self.distance = dist
#        self.stroke = stroke 
#        self.course = course # 1 or S SCM, 2 or Y SCY, 3 or L LCM
#        self.mfe = mfe
        
    def print(self):
        print(f'----- Event Record: -----')
        print(f'Distance:    {self.distance}')
        print(f'Stroke:      {self.stroke}')
        print(f'Course:      {self.course}')
        print(f'Male/Female: {self.mfe}')
        print(f'Min Age:     {self.minAge}')
        print(f'Max Age:     {self.maxAge}')
        
class Swim:
    def __init__(self):
        self.swimDate = ''
        self.swimYear = 0
        self.swimMonth = 0
        self.swimDay = 0
        self.seedTime = ''
        self.seedTimeS = 0
        self.prelimTime = ''
        self.prelimTimeS = ''
        self.courseP = ''
        self.swimOffTime = ''
        self.swimOffTimeS = 0
        self.courseSO = ''
        self.finalTime = ''
        self.finalTimeS = 0
        self.courseF = ''
        self.heatPrelims = 0
        self.lanePrelims = 0
        self.heatFinals = 0
        self.laneFinals = 0
        self.rankPrelims = 0
        self.rankFinals = 0
        self.PointsFinals = 0.0
        self.evttimeclass = ''
        self.fltstatus = ''   
       
    def print(self):
        print(f'----- Swim Record -----')
        print(f'Date:       {self.swimDate}')
        print(f'Year:       {self.swimYear}')
        print(f'Month:      {self.swimMonth}')
        print(f'Day:        {self.swimDay}')
        print(f'Seed:       {self.seedTime}')
        print(f'Seed (s):   {self.seedTimeS}')
        print(f'Prelim:     {self.prelimTime}')
        print(f'Prelim (s): {self.prelimTimeS}')
        print(f'Course (p): {self.courseP}')
        print(f'Swim-off:   {self.swimOffTime}')
        print(f'Swim-off (s):{self.swimOffTimeS}')
        print(f'Course (so):{self.courseSO}')
        print(f'Final:      {self.finalTime}')
        print(f'Final (s):  {self.finalTimeS}')
        print(f'Course (f): {self.courseF}')
        print(f'Heat (p):   {self.heatPrelims}')
        print(f'Lane (p):   {self.lanePrelims}')
        print(f'Heat (f):   {self.heatFinals}')
        print(f'Lane (f):   {self.laneFinals}')
        print(f'Rank (p):   {self.rankPrelims}')
        print(f'Rank (f):   {self.rankFinals}')
        print(f'Points (f): {self.PointsFinals}')
        print(f'Time Class: {self.evttimeclass}')
        print(f'Flt Status: {self.fltstatus}')  
        
# ORG Code
#	       1    USS                        6    NCAA Div III
#	       2    Masters                    7    YMCA
#	       3    NCAA                       8    FINA
#	       4    NCAA Div I                 9    High School
#	       5    NCAA Div II
        
class Team:
    def __init__(self):
        self.code = 0
        self.codeT = ''
        self.teamCode = ''
        self.teamName = ''
        self.teamAbre = ''
        self.teamAdd1 = ''
        self.teamAdd2 = ''
        self.teamCity = ''
        self.teamState = ''
        self.teamZip = ''
        self.teamCounry = ''
        self.teamRegion = ''
    
    def print(self):
        print(f'----- Team Record: -----')
        print(f'Code:        {self.code}')
        print(f'Code (txt):  {self.codeT}')
        print(f'Team code:   {self.teamCode}')
        print(f'Team name:   {self.teamName}')  

         
#readSD3
def StrT2float(x):
    minutes = x[0:2]

    if (minutes=='  '):
        minutes='00'
    seconds = x[3:8]    

    if (seconds=='     '):
        seconds = 0.00
    timeS = float(minutes)*60.0+float(seconds)
    return timeS

# define the parsers for different formats
def D0(x):
    # An individual swim 
#0-12-------3---------------------------4-----------56--7-------8-90
#01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789    
#D01        CUTLER, HAYDEN J                        AUSA0625200412FF 1004  85111212042016 1:06.15Y 1:03.93Y          1:02.95Y 1 1 2 6 12  1                      
#           [name            ][uss        ][]  
#    aa=1;
#    print "Parse D0\n"
    code =x[2:3];             #3/1      M2     CODE   ORG Code 001, table checked                 1
    # swimmer info to object
    new_s = Swimmer()
                              #	  4/8                    future use                                             2
    new_s.name = x[11:29]     #12/28    M1     NAME   swimmer name                               3
    new_s.uss = x[39:51]      #40/12    M2     ALPHA  USS#                                        4
    new_s.attached = x[51:52] #52/1            CODE   ATTACH Code 016, table checked             5
    new_s.citizen = x[52:55]  #53/3            CODE   CITIZEN Code 009, table checked            6
    new_s.bdate = x[55:63]    #56/8     M2     DATE   swimmer birth date                       7 
    new_s.ageClass = x[63:65] #64/2            ALPHA  swimmer age or class (such as Jr or Sr)   8
    new_s.mf = x[65:66]       #66/1     M1     CODE   SEX Code 010, table checked                 9
    
    new_e = Event()  
    new_e.mfe = x[66:67]
    new_e.distance = int(x[67:71])
    new_e.stroke = int(x[71:72]) 
    new_e.course = x[96:97] # 1 or S SCM, 2 or Y SCY, 3 or L LCM
    new_e.minAge = x[76:78]
    new_e.maxAge = x[78:80]
    
#    mfe =  #67/1     M1#    CODE   EVENT SEX Code 011, table checked          0
#    dist =  #68/4     M1#    INT    event distance                            1
#    stroke =  #72/1     M1#    CODE   STROKE Code 012, table checked: 
#    	   1    Freestyle
#	       2    Backstroke
#	       3    Breaststroke
#	       4    Butterfly
#	       5    Individual Medley
#	       6    Freestyle Relay
#	       7    Medley Relay

    new_w = Swim()
    new_w.swimDate = x[80:88]
    new_w.swimYear = int(x[84:88])
    new_w.swimMonth = int(x[82:84])
    new_w.swimDay = int(x[80:82])
    new_w.seedTime = x[88:96]

    new_w.seedTimeS = StrT2float(x[88:96])   
    new_w.prelimTime = x[97:105]
    if new_w.prelimTime[0:2] != 'SC' and new_w.prelimTime[0:2] != 'DQ' and new_w.prelimTime[0:2] != 'NS':
        new_w.prelimTimeS = StrT2float(new_w.prelimTime) 
    new_w.courseP = x[105:106]
    new_w.swimOffTime = x[106:114]
    if new_w.swimOffTime[0:2] != 'SC' and new_w.swimOffTime[0:2] != 'DQ' and new_w.swimOffTime[0:2] != 'NS':
        new_w.swimOffTimeS = StrT2float(new_w.swimOffTime) 

    new_w.courseSO = x[114:115]
    new_w.finalTime = x[115:123]
    if new_w.finalTime[0:2] != 'SC' and new_w.finalTime[0:2] != 'DQ' and new_w.finalTime[0:2] != 'NS':
        new_w.finalTimeS = StrT2float(new_w.finalTime) 
    new_w.courseF = ''
    new_w.heatPrelims = 0
    new_w.lanePrelims = 0
    new_w.heatFinals = 0
    new_w.laneFinals = 0
    new_w.rankPrelims = 0
    new_w.rankFinals = 0
    new_w.PointsFinals = 0.0
    new_w.evttimeclass = ''
    new_w.fltstatus = ''  
#----------------------------------        
    
#    <> = x[:] #73/4                   future use
    evtag = x[76:80] #77/4     M1#    CODE   EVENT AGE Code 025, table checked
    swdate = x[80:88] #81/8     M2     DATE   date of swim
    seedt = x[88:96] #89/8            TIME   seed time
#    courses =  #97/1      *     CODE   COURSE Code 013, table checked
    timepr = x[97:105] #98/8            TIME   prelim time
    courser = x[105:106] #106/1     *     CODE   COURSE Code 013, table checked
    fimeso = x[106:114] #107/8           TIME   swim-off time
    courseso = x[114:115] #115/1     *     CODE   COURSE Code 013, table checked
    timefi = x[115:123] #116/8           TIME   finals time
    coursefi = x[123:124] #124/1     *     CODE   COURSE Code 013, table checked
    heatpre = x[124:126] #125/2           INT    prelim heat number
    lanepre = x[126:128] #127/2           INT    prelim lane number
    heatfi = x[128:130] #129/2           INT    finals heat number
    lanefi = x[130:132] #131/2           INT    finals lane number
    rankpre = x[132:135] #133/3     **    INT    prelim place ranking
    rankfi = x[135:138] #136/3     **    INT    finals place ranking
    ptsfi = x[138:142] #139/4     **    DEC    points scored from finals
    evttimeclass = x[142:144] #143/2           CODE   EVENT TIME CLASS Code 014, table checked
    fltstatus = x[144:145] #145/1           ALPHA  flight status of swimmer (subdivision

    if (new_s.name[0:5]=="BARNE"):
#    if (att[0]=="U"):
    #        print('--%s--',sid)
#            print('00000000001111111111222222222233333333334444444444555555555566666666667777777777888888888899999999990000000000')
#            print('01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789')
            print(x)
            print(f'code:    {code:10}')
            print('*****Printing Objects:*****')
            new_s.print()
            new_e.print()
            new_w.print()
            print('^^^^^Printing Objects:^^^^^')
            
#            print(f'mfe:     {mfe}') #.format(mfe)
#            print(f'dist:    {dist}') #.format(dist)
#            print(f'stroke:  {stroke}') #.format(stroke) 
            print(f'evtag:   {evtag}') #.format(evtag)  
            print(f'swdate:  {swdate}') #.format(swdate)  
            print(f'seedt:   {seedt}') #.format(seedt) 
#            print(f'courses: {courses}') #.format(courses) 
            print(f'timepr:  {timepr}') #.format(timepr)  
            print(f'courser: {courser}') #.format(courser)  
            print(f'fimeso:  {fimeso}') #.format(fimeso)  
            print(f'courseso:{courseso}') #.format(courseso) 
            print(f'timefi:  {timefi}') #.format(timefi)
            print(f'coursefi:{coursefi}') #.format(coursefi) 
            print(f'heatpre: {heatpre}') #.format(heatpre)
            print(f'lanepre: {lanepre}')
            print(f'heatfi:  {heatfi}')
            print(f'lanefi:  {lanefi}') 
            print(f'rankpre: {rankpre}') 
            print(f'rankfi:  {rankfi}')
            print(f'ptsfi:   {ptsfi}')
            print(f'evttimeclass:  {evttimeclass}')
            print(f'fltstatus:{fltstatus}')
          #  print('sh: {0}').format(sh)
            
"""
        1/2      M1     CONST  "D0"
	  3/1      M2     CODE   ORG Code 001, table checked
	  4/8                    future use
	  12/28    M1     NAME   swimmer name 
	  40/12    M2     ALPHA  USS#
	  52/1            CODE   ATTACH Code 016, table checked
	  53/3            CODE   CITIZEN Code 009, table checked
	  56/8     M2     DATE   swimmer birth date
	  64/2            ALPHA  swimmer age or class (such as Jr or Sr)
	  66/1     M1     CODE   SEX Code 010, table checked
	  67/1     M1#    CODE   EVENT SEX Code 011, table checked
	  68/4     M1#    INT    event distance
	  72/1     M1#    CODE   STROKE Code 012, table checked
	  73/4                   future use
	  77/4     M1#    CODE   EVENT AGE Code 025, table checked
	  81/8     M2     DATE   date of swim
	  89/8            TIME   seed time
	  97/1      *     CODE   COURSE Code 013, table checked
	  98/8            TIME   prelim time
	  106/1     *     CODE   COURSE Code 013, table checked
	  107/8           TIME   swim-off time
	  115/1     *     CODE   COURSE Code 013, table checked
	  116/8           TIME   finals time
	  124/1     *     CODE   COURSE Code 013, table checked
	  125/2           INT    prelim heat number
	  127/2           INT    prelim lane number
	  129/2           INT    finals heat number
	  131/2           INT    finals lane number
	  133/3     **    INT    prelim place ranking
	  136/3     **    INT    finals place ranking
	  139/4     **    DEC    points scored from finals
	  143/2           CODE   EVENT TIME CLASS Code 014, table checked
	  145/1           ALPHA  flight status of swimmer (subdivision
				 of Time Standard)
	  146/15                 future use  
	  *  This field is mandatory IF the immediately preceeding time
	     field is NOT blank
	  
	  ** This field is mandatory (M1) if a championship meet 
	     (MEET Code 005 - 6,7)         

	  #  Event age code 025, event sex code 011, event distance, 
	     stroke code 012 and seed time are not mandatory (M1) 
	     for relay only swimmers.          

	  Note - An additional record type will be used for open water
		  swimming.  Multiple swim offs require multiple records.

"""
    
def A0(x):
    aa=1;
#    print "Parse A0\n"

def C1(x):
    
#    print('00000000001111111111222222222233333333334444444444555555555566666666667777777777888888888899999999990000000000')
#    print('01234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890123456789')
#    print(x)
    
    new_t = Team()        
    new_t.code = x[2:3]
    new_t.codeT = ''
    new_t.teamCode = x[11:17]
    new_t.teamName = x[17:48]
    new_t.teamAbre = ''
    new_t.teamAdd1 = ''
    new_t.teamAdd2 = ''
    new_t.teamCity = ''
    new_t.teamState = ''
    new_t.teamZip = ''
    new_t.teamCounry = ''
    new_t.teamRegion = ''
    
#    new_t.print()
    
    
def G0(x):
    aa=1;
#    print "Parse G0\n"
    
def default(x):
    aa=1;
#    print "default\n"

def D3(x):
    # An individual swim 
    sid=x[2:16]
    sname=x[16:31]
    seth=x[31:32]
    jh=x[33:34]
    sh=x[34:35]
    y=x[35:36]
    c=x[36:37]
    p=x[37:38]
    sl=x[38:39]
    cc=x[39:40]
    m=x[40:41]
    d=x[41:42]
    w=x[42:43]
    if (1):
        if (sname[0:5]=="LINDS"):
    #        print('--%s--',sid)
            print('0123456789012345678901234567890123456789')
            print(x)
            print(f'ID:  {sid}')
            print(f'SN:  {sname}')
            print(f'jh:  {jh} ')
            print(f'sh:  {sh} ')
"""    
D3030903MEL*ZHOUMELISSA HANLIN
1/2      M1     CONST   "D3"
3/14     M2     USSNUM  USS# (new)
17/15           ALPHA   prefered first name
32/2      *     CODE    ethnicity code 026
34/1      *     LOGICAL Junior High School                
35/1      *     LOGICAL Senior High School
36/1      *     LOGICAL YMCA/YWCA
37/1      *     LOGICAL College
38/1      *     LOGICAL Park and Rec.
39/1      *     LOGICAL Summer League
40/1      *     LOGICAL Country Club
41/1      *     LOGICAL Masters
42/1      *     LOGICAL Disabled Sports Organizations
43/1      *     LOGICAL Water Polo
44/117                  future use
"""
    
# map the inputs to the function blocks
parsers = {'D0' : D0,
           'A0' : A0,
           'G0' : G0,
           'B1' : default,
           'B2' : default,
           'C1' : C1,
           'C2' : default,
           'E0' : default,
           'F0' : default,
           'D3' : D3,
           'Z0' : default,
}
file_name = "../../testData/0719tera_jos.sd3"; #20161204_JO_result.sd3";

f = open(file_name,'r');

curr_evt_id = -1;

for line in f:
    x = line;
    #look at the 1st 2 characters which define the line format
    
    val = x[0:2]
    parsers[val](x);
     
    
f.close();
print('Done\n');