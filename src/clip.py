import ntpath
import os

detectedGoalList = []
f = open("detected.csv", "r")
for x in f:
    tup = x.replace("\"[", "").replace("]\"", "").split(", ")
    detectedGoalList.append([tup[0], tup[1]])


for dg in detectedGoalList:
    print(dg[0])
    input_file = "\"{}\"".format(dg[0].replace("'", ""))
    output_path = "../clips/" + ntpath.basename(dg[0]).replace("'", "").replace(
        ".mp4", "").replace("Rocket League®_", "").replace("Rocket League™_", "").replace("Rocket League_", "") + ".clipped.mp4"
    start = (int(dg[1]) - int(30 * 10)) / 30
    if start < 0:
        start = 0
    end = (int(dg[1]) / 30) - 3
    duration = end - start

    os.system("ffmpeg -ss {} -i {} -t {} -c copy {}".format(start, input_file,
                                                            duration, output_path))