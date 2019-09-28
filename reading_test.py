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

print(file)

data, samplerate = sf.read(file)

data=np.array(data[:,0])
xer = np.arange(1,len(data)+1)

print(samplerate)
print(data.shape[0]/samplerate)

plt.style.use('classic')
plt.rc('axes')
plt.rc('lines', linewidth=1)
fig=plt.figure()

plt.plot(xer, data)

plt.show()