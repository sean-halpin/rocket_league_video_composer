import ffmpeg
import ntpath

detectedGoalList = []
f = open("detected.csv", "r")
for x in f:
  tup = x.replace("\"[","").replace("]\"","").split(", ")
  detectedGoalList.append([tup[0],tup[1]])


for dg in detectedGoalList:
    print(dg[0])
    output_path = "../clips/" + ntpath.basename(dg[0]).replace("'","").replace(
        ".mp4", "").replace("Rocket League®_", "").replace("Rocket League™_", "").replace("Rocket League_", "") + ".clipped.mp4"
    start = (int(dg[1]) - int(30 * 9)) / 30
    if start < 0:
        start = 0
    end = (int(dg[1]) / 30) - 2

    input_stream = ffmpeg.input("{}".format(dg[0].replace("'","")))

    vid = (
        input_stream.video
        .trim(start=start, end=end)
        .setpts('PTS-STARTPTS')
    )
    aud = (
        input_stream.audio
        .filter_('atrim', start=start, end=end)
        .filter_('asetpts', 'PTS-STARTPTS')
    )

    joined = ffmpeg.concat(vid, aud, v=1, a=1).node
    output = ffmpeg.output(joined[0], joined[1], output_path)
    output.run()
