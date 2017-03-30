# script which creates a csv file containing players and theier average emotion by channel
import os
import sys
import re
import csv

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


    with open(file_path) as f:

        tsvin = csv.reader(f, delimiter='\t');
        i = 0

        cur_row = ["Player_" + str(Current_ID), new_file_name, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        for line in tsvin:

            if i > 0:
                for j in range(2, 14):

                    cur_val = line[19 + (2 * (j - 2))]
                    if(cur_val and float(cur_val) > 0):
                        cur_row[j] = (float(cur_val) + cur_row[j])/2;
                    elif(cur_val):
                        cur_row[j] = (0 + cur_row[j]) / 2;


            i = i + 1

        single_file_columns.append(cur_row)
        """
        f_o = open("CleanOut/" + new_file_name[:-4] + ".tsv", 'w')
        for row in single_file_columns:
            write_line = ""

            write_line += row
            f_o.write(write_line)
        """

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
            recordSingleLog(file_path, count)
            count = count + 1
            print(file_path)

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
