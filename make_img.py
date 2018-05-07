from mandelbrot import *

# 4K  3840  x 2160
# 8K  7680  x 4320
# 16K 15360 x 8640 
image_width = 3000 
image_height = 3000
maxIter = 500
    
files_content = list()
for l in range(0,3000, 500):
    files_content=files_content+open('data_%s.txt' % l).readlines()

print('Store data')
data_dict=dict()
for l in files_content:
    pix = l.split()
    print('Line %s\r' % pix[0]),
    data_dict[int(pix[0])] = [int(count) for count in pix[1:]]

# write image
print('Build image')
my_bmp=BmpImage('composed_2.bmp',image_width,image_height,1)
lines = data_dict.keys()
lines.sort()
for l in lines:    
    print('Line %s\r' % l),
    for count in data_dict[l]:
        grey = getGreyLevel(int(count), maxIter)
        my_bmp.write_pixel_bw(grey)
my_bmp.close()
