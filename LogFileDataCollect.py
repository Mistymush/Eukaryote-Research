import os
import sys
import re

walk_dir = sys.argv[1]
#save_dir = sys.argv[2]

print('walk_dir = ' + walk_dir)

columns = [['"Id"', '"Progression"', '"Level"', '"TimeBegin"', '"TimeEnd"', '"Tries"', '"TimeTaken"', '"CompletedGame"', '"IMotionsID"']]


# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

Current_ID = 0

#parse individual file
def recordSingleLog(file_path, Current_ID):

    stripped_id = file_path[len(walk_dir) + 1:]
    m_ID = re.search('^([^\\\\]+)', stripped_id)

    IMotions_ID = ''

    if (m_ID):
        IMotions_ID = m_ID.group(0)

    row = [Current_ID, 0, 0, 0, 0, 0, 0, False, IMotions_ID]
    line_count = 0
    row_count = 0

    with open(file_path) as f:
        for line in f:
            m_int = re.search('(\d+)$', line)
            m_bool = re.search('(\S+)$', line)

            val = 0

            if (m_int):
                val = m_int.group(0)

            elif(m_bool):
                val = m_bool.group(0)


            if(val):
                row[line_count + 1] = val
                line_count += 1
                if(line_count > 6):
                    line_count = 0
                    columns.append(row)
                    row_count += 1
                    row = [Current_ID, 0, 0, 0, 0, 0, 0, False, IMotions_ID]

        finished = False;

        if(int(columns[len(columns) - 1][1])  == 1 and  int(columns[len(columns) - 1][2]) == 7 ):
            finished = True
        elif(int(columns[len(columns) - 1][1])  == 0 and  int(columns[len(columns) - 1][2]) == 9 ):
            finished = True

        for i in range (0 , row_count):
            columns[len(columns) - 1 - i][7] = finished



count = 0

#Recursive walk folders
for root, subdirs, files in os.walk(walk_dir):
    #print('--\nroot = ' + root)
    #list_file_path = os.path.join(root, 'my-directory-list.txt')
    #print('list_file_path = ' + list_file_path)

    #with open(list_file_path, 'rb') as list_file:
        #for subdir in subdirs:
            #print('\t- subdirectory ' + subdir)

    for filename in files:
        file_path = os.path.join(root, filename)
	
        if filename == "stat_log.txt":
            recordSingleLog(file_path, count)
            count = count + 1
            print(file_path)

        # if filename ==

#write to whatever
f_o = open("StatLogData.csv", 'w')
for row in columns:
    write_line = ""
    for field in row:
        write_line += str(field) + ','
    f_o.write(write_line[:-1] + '\n')
print('Total FIles Oppend: ' + str(count))

f_o.close()