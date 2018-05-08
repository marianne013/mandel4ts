''' Merge all text files in current working directory
'''
from glob import glob

# get list of data files in current working directory
print('Get data files list')
all_files = glob('data_*.txt')

# read all the files
print('Read all data files')
files_content = list()
files_numbers = list()
for one_file in all_files:
    files_content = files_content + open(one_file).readlines()
    files_numbers.append(one_file.split('_')[-1].split('.txt')[0])

print('Ingest data')
data_dict=dict()
for l in files_content:
    pix = l.split()
    print('Line %s\r' % pix[0]),
    data_dict[int(pix[0])] = [int(count) for count in pix[1:]]

# write merged file
print('Write merged file')
out_name = 'data_merged'
for num in files_numbers:
    out_name = out_name + '_%s' % num
out_name = out_name + '.txt'

out_file = open(out_name, 'w')
lines = data_dict.keys()
lines.sort()
for l in lines:
    print('Line %s\r' % l),
    txt_line = '%s' % l
    for pix in data_dict[l]:
        txt_line = txt_line + ' %s' % pix
    out_file.write(txt_line+'\n')
