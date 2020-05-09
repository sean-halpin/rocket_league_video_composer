import cv2
import glob
import ffmpeg
import numpy as np
import pytesseract
import ntpath
from pytesseract import Output

# get grayscale image


def get_grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# noise removal


def remove_noise(image):
    return cv2.medianBlur(image, 5)

# thresholding


def thresholding(image):
    return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

# dilation


def dilate(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.dilate(image, kernel, iterations=1)

# erosion


def erode(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.erode(image, kernel, iterations=1)

# opening - erosion followed by dilation


def opening(image):
    kernel = np.ones((5, 5), np.uint8)
    return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

# canny edge detection


def canny(image):
    return cv2.Canny(image, 100, 200)

# skew correction


def deskew(image):
    coords = np.column_stack(np.where(image > 0))
    angle = cv2.minAreaRect(coords)[-1]
    if angle < -45:
        angle = -(90 + angle)
    else:
        angle = -angle
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    rotated = cv2.warpAffine(
        image, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)
    return rotated

# template matching


def match_template(image, template):
    return cv2.matchTemplate(image, template, cv2.TM_CCOEFF_NORMED)


# tesseract config
# some success : 1,3,4,5,6
# nothin: 0,2,7,8,9,10,11,12,13
custom_config = r'--oem 1 --psm 1'

# grab mp4 videos
mp4list = [f for f in glob.glob("/home/sean/Videos/rocketleague/*.mp4")]

detectedGoalList = []
videosAnalysed = 0
videosWithConfirmedGoal = 0

for v in mp4list:
    print(v)
    goalDetected = False
    vidcap = cv2.VideoCapture(v)
    success, image = vidcap.read()
    count = 0
    videosAnalysed += 1
    while (success and not goalDetected):
        if count > 990:
            break
        # cv2.imwrite("frame%d.jpg" % count, image) # save frame as JPEG file
        success, image = vidcap.read()
        # print('Read a new frame: ', success)
        if(success):
            count += 1
            if(count > 260 and count % 40 == 0):
                try:
                    img = image[650:702, 40:155]
                    img = (get_grayscale(img))
                    # Show Analysed Image
                    # cv2.imshow('img', img)
                    # cv2.waitKey(0)
                    d = pytesseract.image_to_data(
                        img, lang="eng", config=custom_config, output_type=Output.DICT)
                    print(d['text'])
                    n_boxes = len(d['text'])
                    for i in range(n_boxes):
                        matches = ["REPLAY", "REPL", "REP", "PLAY"]
                        if any(x in d['text'][i] for x in matches):
                            print("Goal scored detected at frame: {}".format(count))
                            goalDetected = True
                            videosWithConfirmedGoal += 1
                            detectedGoalList.append([v, count])
                            # Overlay Bounding Boxes
                            if int(d['conf'][i]) > 60:
                                (x, y, w, h) = (d['left'][i], d['top']
                                                [i], d['width'][i], d['height'][i])
                                img = cv2.rectangle(
                                    img, (x, y), (x + w, y + h), (255, 55, 0), 2)
                    print(count)
                except Exception as e:
                    print(e)
    print(detectedGoalList)
    print(videosAnalysed)
    print(videosWithConfirmedGoal)


for dg in detectedGoalList:
    print(dg[0])
    output_path = "../videos/" + ntpath.basename(dg[0]).replace(
        ".mp4", "").replace("Rocket League®_", "") + ".clipped.mp4"
    input_stream = ffmpeg.input(dg[0])
    start = (int(dg[1]) - (30 * 8)) / 30
    if start < 0:
        start = 0
    end = int(dg[1]) / 30

    input_stream = ffmpeg.input(dg[0])

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
