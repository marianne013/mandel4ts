from mandelbrot import *

# 4K  3840  x 2160
# 8K  7680  x 4320
# 16K 15360 x 8640 
image_width = 7680
image_height = 4320
maxIter = 500
    
l0=open('data_0.txt').readlines()
l1=open('data_1000.txt').readlines()
l2=open('data_2000.txt').readlines()
l3=open('data_3000.txt').readlines()
l4=open('data_4000.txt').readlines()

print('Store data')
data_dict=dict()
for l in l0+l1+l2+l3+l4:
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
