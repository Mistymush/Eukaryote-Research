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
        standard_deviations = np.std(numpy_imotions_tsv, axis=0)

        zscored_vals = stats.zscore(numpy_imotions_tsv, axis=0)

        print(means)
        #print(standard_deviations)

        cur_row = ["Player_" + str(Current_ID), new_file_name, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        #imotions_id = new_file_name[8:]
        #imotions_id = imotions_id[:-4]

        #if(len(zscored_vals ) > 40):
        #   sample_Z_scores(zscored_vals, imotions_tsv_unsliced, imotions_id, undefined_frame_indexs)

        #quit()


count = 1

"""
#row of 64 nones, which is inserted into the zscored_vals array for each player to add back in undefined frames for sampling
junk_row = []
for i in range(0, 64):
    junk_row.append(None)

player_joy_bucket_means = []

#function which samples the Z-Scored values by log file level completion time.
def sample_Z_scores(zscored_vals, raw_data, imotions_id, undefined_frame_indexs):

    #Get log data for current player
    current_player_log = []

    with open("Study4_StatLog_WithID.csv") as f:
        tsvin_log = csv.reader(f);

        for line in tsvin_log:
            if line[8] == imotions_id:
                current_player_log.append(line);




    #Re-Add empty data rows to zscored data
    for val in undefined_frame_indexs:
        zscored_vals = np.insert(zscored_vals,val - 1, junk_row, axis=0)


    #at this point zscored vals is aligned with raw data other than header

    #Sample the zscore data using the frame times of the raw_data and times in the log file.
    level_index = 0
    frame_index = 0

    current_level_compleat_time = current_player_log[level_index][4]

    bucketed_joy = []


    for line in raw_data:
        if(float(current_level_compleat_time) < float(line[13])):

            #print("level " + str(level_index) + " found at time: " + str(line[13]))

            bucket = zscored_vals[frame_index - 10: frame_index];
            bucket_mean = np.mean(bucket, axis=0)[0]
            bucketed_joy.append(bucket_mean)

            if(level_index < len(current_player_log) - 1):
                level_index += 1
                current_level_compleat_time = current_player_log[level_index][4]

            else:
                break;

        #zscore of joy at that frame time
        #print(zscored_vals[frame_index][0])
        frame_index += 1

    #clean out nans
    clean_index = 0
    indexs_to_kill = []
    for val in bucketed_joy:
        if math.isnan(val):
            indexs_to_kill.append(clean_index)
        clean_index+=1

    bucketed_joy = np.delete(bucketed_joy, indexs_to_kill)

    if(len(bucketed_joy) > 0):
        player_joy_bucket_means.append(np.mean(bucketed_joy))

    if((len(zscored_vals)) != len(raw_data)):
        print("Error! Zscore and Data file did not line up")
"""

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

#print(np.mean(player_joy_bucket_means))

f_o.close()
