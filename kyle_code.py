# -*- coding: utf-8 -*-
"""
Created on Wed Jun  2 15:44:58 2021

@author: kfischer
"""

# run in data folder

import pandas as pd
from xml.dom import minidom
import os
import sys
import pickle
from tkinter import Tk
from tkinter.filedialog import askdirectory

# get filenames
path = askdirectory(title='Select Folder') # shows dialog box and return the path
Tk().destroy()
folder = os.path.basename(path)
CSVfilename = path + '\\' + folder + '_Cycle00001_VoltageRecording_001.csv'
XMLfilename = path + '\\' + folder + '.xml'

if not os.path.isfile(CSVfilename):
    print('CSV file does not exist.')
    sys.exit()

if not os.path.isfile(XMLfilename):
    print('XML file does not exist.')
    sys.exit()

data = {}

# read XML
print('Reading XML...')
file = minidom.parse(XMLfilename)
frames = file.getElementsByTagName('Frame')
data['FrameTimes'] = [round(float(frames[x].attributes['relativeTime'].value)*1000) for x in range(len(frames))]
print('Done.')

# read CSV
print('Reading CSV...')
df = pd.read_csv(CSVfilename)
print('Done.')
df = df.rename(columns=lambda x: x.strip())
df.pop('Time(ms)')

df = df > 2.5
df = df.astype(int)
df = df.diff()
df = df.fillna(0)

data['LickOn'] = df[df['Lick']==1].index.tolist()
data['LickOff'] = df[df['Lick']==-1].index.tolist()

data['AirpuffOn'] = df[df['Airpuff']==1].index.tolist()
data['AirpuffOff'] = df[df['Airpuff']==-1].index.tolist()

data['SpeakerOn'] = df[df['Speaker']==1].index.tolist()
data['SpeakerOff'] = df[df['Speaker']==-1].index.tolist()

data['LiquidOn'] = df[df['Liquid']==1].index.tolist()
data['LiquidOff'] = df[df['Liquid']==-1].index.tolist()

# save file
print('Saving Data.')
dataFilename = path + '\\' + folder + '_data.pkl'

outfile = open(dataFilename,'wb')
pickle.dump(data,outfile)
outfile.close()
