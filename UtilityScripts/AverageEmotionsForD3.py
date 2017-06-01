# script which creates a csv file containing players and their average emotion by channel
#This script is inteded to be used for D3 vis only, and needs updating to be that.
#To date it contains legacy code from averageEmotionsByLevel.


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

single_file_columns = [['"Display Name"','"File Name"','"Joy Evidence"', "Weight", '"Anger Evidence"', "Weight", '"Surprise Evidence"', "Weight", '"Fear Evidence"', "Weight", '"Contempt Evidence"', "Weight",
                        '"Disgust Evidence"', "Weight", '"Sadness Evidence"', "Weight", '"Confusion Evidence"', "Weight", '"Frustration Evidence"', "Weight", '"Neutral Evidence"', "Weight", '"Positive Evidence"', "Weight",  '"Negative Evidence"']]


# parse individual file
def getLogSummaryStats(file_path, Current_ID):
    row = [Current_ID, 0, 0, 0, 0, 0, 0, False]

    #Cutt os file path away from file ID for recording
    m_f_name = re.search('([^\\\\]+)$', file_path)

    new_file_name = ''

    if (m_f_name):
        new_file_name = m_f_name.group(0)

    #open current log file
    with open(file_path) as f:
        tsvin = csv.reader(f, delimiter='\t');


        #filter data for columns with floats and rows that are defined
        #NOTE: Should reject files under a certain threshold of data.

        imotions_tsv_sliced = []
        imotions_tsv_unsliced = []

        undefined_frame_indexs = []

        line_count = 0
        for line in tsvin:
            if (line_count < 6):
                pass

            else:
                for i in range (19, 83):
                    if line[i]:
                        line[i] = float(line[i])
                if line[19]:
                    imotions_tsv_sliced.append(line[19:83])
                    imotions_tsv_unsliced.append(line)
                else:
                    undefined_frame_indexs.append(line_count);
                    imotions_tsv_unsliced.append(line)

            line_count += 1


        #Create Numpy array
        numpy_imotions_tsv = np.array(imotions_tsv_sliced)

        mean = np.mean(numpy_imotions_tsv, axis=0)
        #standard_deviations = np.std(numpy_imotions_tsv, axis=0)

        cur_row = ["Player_" + str(Current_ID), new_file_name, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        if isinstance(mean, np.ndarray):
            for i in range (0, 12):
                cur_row[(i * 2) + 2] = mean[i * 2]
                cur_row[(i * 2) + 3] = line_count


        single_file_columns.append(cur_row)


# Recursive walk folders

for root, subdirs, files in os.walk(walk_dir):
    # print('--\nroot = ' + root)
    # list_file_path = os.path.join(root, 'my-directory-list.txt')
    # print('list_file_path = ' + list_file_path)

    # with open(list_file_path, 'rb') as list_file:
    # for subdir in subdirs:
    # print('\t- subdirectory ' + subdir)
    file_count = 1

    for filename in files:
        file_path = os.path.join(root, filename)

        if ".tsv" in filename:
            print(file_path)
            getLogSummaryStats(file_path, file_count)
            file_count = file_count + 1

    print('Total FIles Oppend: ' + str(file_count))

###########################################################################
#Calculate Average Emotions accross all players in each progression
###########################################################################

sum_average_and_weight_p0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sumOfWeights_p0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

sum_average_and_weight_p1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
sumOfWeights_p1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]


count = 0
for row in single_file_columns:
    if(count > 0):

        #Determine which progression this row belongs too.
        player_progression = 2

        with open("Study6_logdata.csv") as f:
            tsvin_log = csv.reader(f);

            for line in tsvin_log:

                player_file_name =  row[1]



                player_file_name = player_file_name[8:]
                imotions_id = player_file_name[:-4]

                if line[8] == imotions_id:
                    player_progression = line[1]

        if(player_progression == 2):
            print("error, imotions dump not found in log data.")
            sys.exit()


        #Add to the correct sum array
        for i in range(0, 12):
            value = row[(i* 2) + 2]
            weight = row[(i* 2) + 3];

            if(int(player_progression) == 0):
                sum_average_and_weight_p0[i] = sum_average_and_weight_p0[i] + (value * weight)
                sumOfWeights_p0[i] = sumOfWeights_p0[i] + weight

            if(int(player_progression) == 1):
                sum_average_and_weight_p1[i] = sum_average_and_weight_p1[i] + (value * weight)
                sumOfWeights_p1[i] = sumOfWeights_p1[i] + weight


    count += 1


#compute final averages
final_averages_p0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
final_averages_p1 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for i in range(0, len(final_averages_p0)):
    final_averages_p0[i] = sum_average_and_weight_p0[i] / sumOfWeights_p0[i]
    final_averages_p1[i] = sum_average_and_weight_p1[i] / sumOfWeights_p1[i]

#Print out final statistics.

#array of tags for printing
channels = ['"Joy Evidence"', '"Anger Evidence"', '"Surprise Evidence"',  '"Fear Evidence"', '"Contempt Evidence"', '"Disgust Evidence"',  '"Sadness Evidence"',  '"Confusion Evidence"',  '"Frustration Evidence"',  '"Neutral Evidence"',  '"Positive Evidence"',  '"Negative Evidence"']

print("Averages for progression 0:")
for i in range(0, len(final_averages_p0)):
    print("Average of " + channels[i] + " Equals: " + str(final_averages_p0[i]))

print("Averages for progression 1:")
for i in range(0, len(final_averages_p1)):
    print("Average of " + channels[i] + " Equals: " + str(final_averages_p1[i]))



# Write EmotionAverages.csv for use by visualization (typically toggled off)
"""
f_o = open("EmotionAverages.csv", 'w')
for row in single_file_columns:
    write_line = ""

    count = 0
    for field in row:
        if(count < 2 or count % 2 == 0):
            write_line += str(field) + ','
        count += 1

    f_o.write(write_line[:-1] + '\n')

f_o.close()
"""