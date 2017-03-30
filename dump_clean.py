import os
import sys
import re

walk_dir = sys.argv[1]
#save_dir = sys.argv[2]

print('walk_dir = ' + walk_dir)

columns = []


# If your current working directory may change during script execution, it's recommended to
# immediately convert program arguments to an absolute path. Then the variable root below will
# be an absolute path as well. Example:
# walk_dir = os.path.abspath(walk_dir)
print('walk_dir (absolute) = ' + os.path.abspath(walk_dir))

Current_ID = 0

#parse individual file
def recordSingleLog(file_path, Current_ID):

    row = [Current_ID, 0, 0, 0, 0, 0, 0, False]
    line_count = 0
    row_count = 0

    m_f_name = re.search('([^\\\\]+)$', file_path)

    new_file_name = ''

    if (m_f_name):
        new_file_name = m_f_name.group(0)




    single_file_columns = ['StudyName	ExportDate	Name	Age	Gender	StimulusName	SlideType	EventSource	Timestamp	MediaTime	PostMarker	Annotation	FrameNo	FrameTime	NoOfFaces	FaceRect X	FaceRect Y	FaceRect Width	FaceRect Height	Joy Evidence	Joy Intensity	Anger Evidence	Anger Intensity	Surprise Evidence	Surprise Intensity	Fear Evidence	Fear Intensity	Contempt Evidence	Contempt Intensity	Disgust Evidence	Disgust Intensity	Sadness Evidence	Sadness Intensity	Confusion Evidence	Confusion Intensity	Frustration Evidence	Frustration Intensity	Neutral Evidence	Neutral Intensity	Positive Evidence	Positive Intensity	Negative Evidence	Negative Intensity	AU1 Evidence	AU2 Evidence	AU4 Evidence	AU5 Evidence	AU6 Evidence	AU7 Evidence	AU9 Evidence	AU10 Evidence	AU12 Evidence	AU14 Evidence	AU15 Evidence	AU17 Evidence	AU18 Evidence	AU20 Evidence	AU23 Evidence	AU24 Evidence	AU25 Evidence	AU26 Evidence	AU28 Evidence	AU43 Evidence	HasGlasses Probability	IsMale Probability	Yaw Degrees	Pitch Degrees	Roll Degrees	LEFT_EYE_LATERAL X	LEFT_EYE_LATERAL Y	LEFT_EYE_PUPIL X	LEFT_EYE_PUPIL Y	LEFT_EYE_MEDIAL X	LEFT_EYE_MEDIAL Y	RIGHT_EYE_MEDIAL X	RIGHT_EYE_MEDIAL Y	RIGHT_EYE_PUPIL X	RIGHT_EYE_PUPIL Y	RIGHT_EYE_LATERAL X	RIGHT_EYE_LATERAL Y	NOSE_TIP X	NOSE_TIP Y	7 X	7 Y	LiveMarker	KeyStroke	MarkerText	SceneType	SceneOutput	SceneParent']

    with open(file_path) as f:
        i = 0
        for line in f:
            if i > 7:
                columns.append(line)
                single_file_columns.append(line)
            i = i + 1

        f_o = open("CleanOut/"+ new_file_name[:-4] +".tsv", 'w')
        for row in single_file_columns:
            write_line = ""

            write_line += row
            f_o.write(write_line)

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
	
        if ".txt" in filename:
            recordSingleLog(file_path, count)
            count = count + 1
            print(file_path)

#write to whatever
#write one mondo file
"""
f_o = open("CleanOut/EmotionData.tsv", 'w')
for row in columns:
    write_line = ""

    write_line += row
    f_o.write(write_line)
"""

print('Total FIles Oppend: ' + str(count))

#f_o.close()