# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import argparse
import numpy as np
#import soundfile as sf
from pydub import AudioSegment as As
#import matplotlib.pyplot as plt

def return_data(file):
    '''
    Input an audio file of any type and return a numpy array and the sample rate.
    '''
    dtype_dict = {
        1: np.int8,
        2: np.int16,
        4: np.int32
    }
    dtype = dtype_dict[file.sample_width]
    array = np.array(file.get_array_of_samples(), dtype=dtype)
    sample_rate = file.frame_rate * 2
    max = np.amax(array)
    array = np.divide(array, max)
    return array, sample_rate

parser = argparse.ArgumentParser(description='Something, I dunno, more useful')
parser.add_argument('file', type=str, help='Name of input file')
parser.add_argument('--tempo', type=int, default=120, help='Choose tempo of soundfile')
parser.add_argument('--meter', type=int, nargs=2, default=(4,4), help='Allows selection of the meter')

args=parser.parse_args()
file=args.file
file_b = As.from_file(file)
bpm=args.tempo
meter = args.meter

basis=meter[1] #bottom
beats=meter[0] #top

data, samplerate = return_data(file_b)
#data, samplerate = sf.read(file)
#data = np.array(data[:,0])

bps=bpm/60
spb=1/bps
tolerance = .2 * samplerate * spb
npb = spb * samplerate

npb_over = npb+tolerance
npb_under = npb-tolerance

data_rectify = np.abs(data)
data_plot = np.ma.masked_less(data_rectify, 0.4)


#plt.style.use('classic')
#plt.rc('axes')
#plt.rc('lines', linewidth=1)
#fig=plt.figure()
#plt.ylim((-1,1))
#plt.xlim((65000,66000))
#plt.plot(xer, data_plot)
#plt.show()

xer = np.arange(1,len(data)+1)
spike_time = np.array([])
flag = False
check = 0
for n,x in zip(xer,data_plot):
    if n > (check+(.05*samplerate)):
        flag = False    
    if x and not flag:
        spike_time = np.append(spike_time, n)
        flag = True
        check = n

spike_time = np.subtract(spike_time, spike_time[0])

info = "\\header{ title=\""+file+"\"}\n\\relative{\\time "+str(beats)+"/"+str(basis)+"\n"


total=0
for x in range(len(spike_time)-1):
    info = info + "c"
    if x == 0:
        info = info + "''"
    gap = spike_time[x+1]-spike_time[x]
    if (gap > npb_under*4) and (gap < npb_over*4):
        info = info + "1"
        total += 4
    elif (gap > npb_under*3) and (gap < npb_over*3):
        info = info + "2."
        total += 3
    elif (gap > npb_under*2) and (gap < npb_over*2):
        info = info + "2"
        total += 2
    elif (gap > npb_under*1.5) and (gap < npb_over*1.5):
        info = info + "1."
        total += 1.5
    elif (gap > npb_under) and (gap < npb_over):
        info = info + "4"
        total += 1
    elif (gap > npb_under*.75) and (gap < npb_over*.75):
        info = info + "4."
        total += .75
    elif (gap > npb_under*.5) and (gap < npb_over*.5):
        info = info + "8"
        total += .5
    elif (gap > npb_under*.375) and (gap < npb_over*.375):
        info = info + "16."
        total += .375
    elif (gap > npb_under*.25) and (gap < npb_over*.25):
        info = info + "16"
        total += .25
    info = info + " "
    
if (total%beats != 0):
    rmdr = beats-(total%beats)
    if rmdr == 4:
        info = info + "c1"
    elif rmdr == 3:
        info = info + "c2."
    elif rmdr == 2:
        info = info + "c2"
    elif rmdr == 1.5:
        info = info + "c4."
    elif rmdr == 1:
        info = info + "c4"
    elif rmdr == .75:
        info = info + "c4."
    elif rmdr == .5:
        info = info + "c8"
    elif rmdr == .375:
        info = info + "c16."
    elif rmdr == .25:
        info = info + "c16"
        
info = info + "}"
    
print(info)
