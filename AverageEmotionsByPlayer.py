# script which creates a csv file containing players and theier average emotion by channel
import os
import sys
import re
import csv
import numpy as np
import math
from scipy import stats

walk_dir = sys.argv[1]
# save_dir = sys.argv[2]

print('walk_dir = ' + walk_dir)

columns = []

# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

single_file_columns = [['"Display Name"','"File Name"','"Joy Evidence"','"Anger Evidence"','"Surprise Evidence"','"Fear Evidence"','"Contempt Evidence"','"Disgust Evidence"','"Sadness Evidence"','"Confusion Evidence"','"Frustration Evidence"','"Neutral Evidence"','"Positive Evidence"', '"Negative Evidence"']]


# parse individual file
def recordSingleLog(file_path, Current_ID):
    row = [Current_ID, 0, 0, 0, 0, 0, 0, False]
    line_count = 0
    row_count = 0

    m_f_name = re.search('([^\\\\]+)$', file_path)

    new_file_name = ''

    if (m_f_name):
        new_file_name = m_f_name.group(0)

    #open current tst file
    with open(file_path) as f:
        tsvin = csv.reader(f, delimiter='\t');

        #filter data for columns with floats and rows that are defined
        #NOTE: Should reject files under a certain threshold of data.

        imotions_tsv_sliced = []
        imotions_tsv_unsliced = []

        header = True;

        undefined_frame_indexs = []

        count = 0
        for line in tsvin:
            if header:
                header = False
                count += 1
            else:
                for i in range (19, 83):
                    if line[i]:
                        line[i] = float(line[i])
                if line[19]:
                    imotions_tsv_sliced.append(line[19:83])
                    imotions_tsv_unsliced.append(line)
                else:
                    undefined_frame_indexs.append(count);
                    imotions_tsv_unsliced.append(line)
                count += 1


        #Create Numpy array
        numpy_imotions_tsv = np.array(imotions_tsv_sliced)

        means = np.mean(numpy_imotions_tsv, axis=0)
        #standard_deviations = np.std(numpy_imotions_tsv, axis=0)

        cur_row = ["Player_" + str(Current_ID), new_file_name, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        if isinstance(means, np.ndarray):
            for i in range (0, 12):
                cur_row[i + 2] = means[i * 2]


        single_file_columns.append(cur_row)



count = 1

# Recursive walk folders
for root, subdirs, files in os.walk(walk_dir):
    # print('--\nroot = ' + root)
    # list_file_path = os.path.join(root, 'my-directory-list.txt')
    # print('list_file_path = ' + list_file_path)

    # with open(list_file_path, 'rb') as list_file:
    # for subdir in subdirs:
    # print('\t- subdirectory ' + subdir)

    for filename in files:
        file_path = os.path.join(root, filename)

        if ".tsv" in filename:
            print(file_path)
            recordSingleLog(file_path, count)
            count = count + 1


# write to whatever
# write one mondo file

f_o = open("EmotionAverages.csv", 'w')
for row in single_file_columns:
    write_line = ""
    for field in row:
        write_line += str(field) + ','
    f_o.write(write_line[:-1] + '\n')


print('Total FIles Oppend: ' + str(count))

f_o.close()
