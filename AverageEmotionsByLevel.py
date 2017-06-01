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
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))


def getPlayerLogData(player_file_name):

    player_file_name = player_file_name[8:]
    imotions_id = player_file_name[:-4]

    player_log_data = []

    with open("Study6_logdata.csv") as f:
        tsvin_log = csv.reader(f);

        for line in tsvin_log:
            if line[8] == imotions_id:
                player_log_data.append(line)

    return player_log_data


CollectedMeansAndWeights = []

# parse individual file
def getEmotionSummaryStats(file_path, Current_ID):
    #Cutt os file path away from file ID for recording
    m_f_name = re.search('([^\\\\]+)$', file_path)

    new_file_name = ''

    if (m_f_name):
        new_file_name = m_f_name.group(0)

    level_4_start_time = 0

    player_log_data = getPlayerLogData(new_file_name)
    for line in player_log_data:
        if(int(line[2]) == 4):
            level_4_start_time = float(line[3])

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
                if line[19] and (float(line[13]) > level_4_start_time):
                    imotions_tsv_sliced.append(line[19:83])
                    imotions_tsv_unsliced.append(line)
                elif (float(line[13]) > level_4_start_time):
                    undefined_frame_indexs.append(line_count);
                    imotions_tsv_unsliced.append(line)

            line_count += 1

        #Create Numpy array
        numpy_imotions_tsv = np.array(imotions_tsv_sliced)

        mean = np.mean(numpy_imotions_tsv, axis=0)
        #standard_deviations = np.std(numpy_imotions_tsv, axis=0)

        cur_row = ["Player_" + str(Current_ID), new_file_name, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

        if isinstance(mean, np.ndarray) and len(imotions_tsv_sliced) > 5:
            for i in range (0, 12):
                cur_row[i + 2] = mean[i * 2]

        #ignore mean calculations that did not work (bad file or didnt reach last level)
        if(cur_row[3] != 0):
            CollectedMeansAndWeights.append(cur_row)

#Open up each log file from the given study
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
            getEmotionSummaryStats(file_path, file_count)
            file_count = file_count + 1

    print('Total FIles Oppend: ' + str(file_count))

###########################################################################
#Calculate Average Emotions accross all players by progression
###########################################################################

averages_p0 = []
averages_p1 = []

sum_rows_p0 = 0
sum_rows_p1 = 0

for row in CollectedMeansAndWeights:
    #Determine which progression this row belongs too.
    player_progression = 2

    player_log_data = getPlayerLogData(row[1])

    player_progression = int(player_log_data[0][1])

    if(player_progression == 0):
        sum_rows_p0 += 1

    elif(player_progression == 1):
        sum_rows_p1 += 1

    else:
        print("error, imotions dump not found in log data.")
        sys.exit()

    #Add to the correct sum array
    for i in range(0, 12):
        if(player_progression == 0):
            averages_p0.append(row[2:])

        elif(player_progression == 1):
            averages_p1.append(row[2:])


#compute final averages
final_averages_p0 = np.mean(averages_p0, axis=0)
final_averages_p1 = np.mean(averages_p1, axis=0)

t_test = stats.ttest_ind(averages_p0, averages_p1, axis=0)

#Array of tags for printing
channels = ['"Joy Evidence"', '"Anger Evidence"', '"Surprise Evidence"',  '"Fear Evidence"', '"Contempt Evidence"', '"Disgust Evidence"',  '"Sadness Evidence"',  '"Confusion Evidence"',  '"Frustration Evidence"',  '"Neutral Evidence"',  '"Positive Evidence"',  '"Negative Evidence"']

#Print out final statistics
print("Averages for progression 0:")
for i in range(0, len(final_averages_p0)):
    print("Average of " + channels[i] + " Equals: " + str(final_averages_p0[i]))

print("Averages for progression 1:")
for i in range(0, len(final_averages_p1)):
    print("Average of " + channels[i] + " Equals: " + str(final_averages_p1[i]))

print("t-test Results by emotion")
for i in range(0, len(final_averages_p1)):
    print("t-test result of " + channels[i] + " results: t-statistic: " + str(t_test[0][i]) + ", p-value: " + str(t_test[1][i]))