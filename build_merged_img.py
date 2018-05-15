#!/bin/env python

''' Create BitMap from "merged" data file
'''
from mandelbrot import *
from glob import glob

# get list of merged data files in current working directory
print('Get merged data files list')
all_files = glob('data_merged_*.txt')

# read all the files
print('Read all %s data files' % len(all_files))
files_content = list()
for one_file in all_files:
    files_content = files_content + open(one_file).readlines()

# ingest data into a dictionnary
print('Ingest data')
data_dict=dict()
for l in files_content:
    pix = l.split()
    print('Line %s\r' % pix[0]),
    data_dict[int(pix[0])] = [int(count) for count in pix[1:]]

# write image
print('Build image')
# have to know this one in advance
maxIter = 1000
# image size guessed from data
lines = data_dict.keys()
lines.sort()
image_height = len(lines)
image_width = len(data_dict[lines[0]])
my_bmp=BmpImage('merged_image.bmp', image_width, image_height, 1)
for l in lines:
    print('Line %s\r' % l),
    for count in data_dict[l]:
        grey = getGreyLevel(int(count), maxIter)
        my_bmp.write_pixel_bw(grey)
my_bmp.close()
