# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import argparse
import numpy as np
import soundfile as sf
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description='Hackathon BABYYYYYYYY')
parser.add_argument('file', type=str, help='Name of input file')

args=parser.parse_args()
file=args.file
bpm=120
measure=4
beats=4

data, samplerate = sf.read(file)

bps=bpm/60
spb=1/bps
tolerance = .2 * samplerate * spb
npb = spb * samplerate

npb_over = npb+tolerance
npb_under = npb-tolerance


data=np.array(data[:,0])
xer = np.arange(1,len(data)+1)

data_rectify = np.abs(data)
data_plot = np.ma.masked_less(data_rectify, 0.4)

plt.style.use('classic')
plt.rc('axes')
plt.rc('lines', linewidth=1)
fig=plt.figure()
plt.ylim((-1,1))
#plt.xlim((65000,66000))
plt.plot(xer, data_plot)

#spike_data = np.array([])
spike_time = np.array([])
flag = False
check = 0
for n,x in zip(xer,data_plot):
    if n > (check+(.05*samplerate)):
        flag = False    
    if x and not flag:
        #spike_data = np.append(spike_data, x)
        spike_time = np.append(spike_time, n)
        flag = True
        check = n

spike_time = np.subtract(spike_time, spike_time[0])

info = "\\header{ title=\""+file+"\"}\n\\relative{\\time 4/4\n"



total=0
for x in range(len(spike_time)-1):
    info = info + "c"
    if x == 0:
        info = info + "''"
    gap = spike_time[x+1]-spike_time[x]
    if (gap > npb_under*4) and (gap < npb_over*4):
        info = info + "1"
        total += 4
    elif (gap > npb_under*2) and (gap < npb_over*2):
        info = info + "2"
        total += 2
    elif (gap > npb_under) and (gap < npb_over):
        info = info + "4"
        total += 1
    elif (gap > npb_under*.5) and (gap < npb_over*.5):
        info = info + "8"
        total += .5
    elif (gap > npb_under*.25) and (gap < npb_over*.25):
        info = info + "16"
        total += .25
    info = info + " "
    
if (total%4 != 0):
    rmdr = 4-(total%4)
    if rmdr == 2:
        info = info + "c2"
    elif rmdr == 1:
        info = info + "c4"
    elif rmdr == .5:
        info = info + "c8"
    elif rmdr == .25:
        info = info + "c16"
        
info = info + "}"
    
print(info)
#plt.show()