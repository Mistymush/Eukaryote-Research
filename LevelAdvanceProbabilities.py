
#script which calculates probabilities of success on next level based on reaching current level.
import csv

dataFile = "Study4_StatLog.csv"


def calculateProbabilities(file_path):

    ##################-2 -1  0  1  2  3  4  5  6  7
    FinishedCoutns = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    FailedCoutns = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

    with open(file_path) as f:
        reader = csv.reader(f)

        old_id = 0
        row_index = 0
        num_prog_1 = 0
        num_prog_2 = 0

        for row in reader:
            if(row_index == 0):
                header = row;
            else:
                current_id = row[0]
                if(old_id != current_id):
                    old_id = current_id
                    print(old_id)

                    if (row[1] == "0"):
                        num_prog_1 += 1

                    if (row[1] == "1"):
                        num_prog_2 += 1



                #if a line is last level of current id, and it is not the last level in progression then increment failed count
                #otherwise incriment Finished count


                #print(row[0] +"," +row[1] + ","  + row[2] + "," + row[1])

            row_index += 1


        #print results
        print("num prog 1:" + str(num_prog_1))
        print("num prog 2:" + str(num_prog_2))


    #iterate accross counts to get probabilities.

calculateProbabilities(dataFile);

