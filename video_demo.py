import sys
sys.path.insert(0, 'python')
import cv2
import model
import util
from hand import Hand
from body import Body
import matplotlib.pyplot as plt
import copy
import numpy as np

body_estimation = Body('model/body_pose_model.pth')
hand_estimation = Hand('model/hand_pose_model.pth')
test_image = 'images/demo.jpg'
oriImg = cv2.imread(test_image)  # B,G,R order
def parse_image(cv_image):

    candidate, subset = body_estimation(cv_image)

    canvas = copy.deepcopy(cv_image)
    canvas = util.draw_bodypose(canvas, candidate, subset)
    # detect hand
    hands_list = util.handDetect(candidate, subset, cv_image)

    all_hand_peaks = []
    for x, y, w, is_left in hands_list:
        peaks = hand_estimation(cv_image[y:y+w, x:x+w, :])
        peaks[:, 0] = np.where(peaks[:, 0]==0, peaks[:, 0], peaks[:, 0]+x)
        peaks[:, 1] = np.where(peaks[:, 1]==0, peaks[:, 1], peaks[:, 1]+y)
        all_hand_peaks.append(peaks)

    canvas = util.draw_handpose(canvas, all_hand_peaks)
    rgb_image=canvas
    skeleton=[(-1,-1)]*18
    for i in range(18):
        for n in range(len(subset)):
            index = int(subset[n][i])
            if index == -1:
                continue
            x, y = candidate[index][0:2]
            skeleton[i]=(x,y)

    return rgb_image,skeleton,[peaks.tolist() for peaks in all_hand_peaks]
file_name="afjorddance"
file_extension=".mp4"
cap = cv2.VideoCapture(file_name+file_extension)
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
skeleton,parsed_movie=[],[]
i=0
start=0.0
end=1
fps = cap.get(cv2.CAP_PROP_FPS)
#set to 1 to not skip any frames
skip_frames=50

while (cap.isOpened()):
    ret, frame = cap.read()
    i += 1

    if i % skip_frames is not 0:
        continue
    if i/length<=start:
        continue
    if i/length>=end:
        break
    print("frame: ", i, ", decode at length: ", i/ length)
    #in the format width,height
    parsed_img,bones,hands=parse_image(frame)
    parsed_movie.append(parsed_img)
    skeleton.append((bones,hands))
    size = parsed_img.shape[:2][::-1]


print("finished conversion: now saving")
import json
json = json.dumps(skeleton)
with open(file_name+"_skeleton.json", "w") as json_file:
    json_file.write(json)
#

out_name=file_name+"_parsed.mp4"
out_0 = cv2.VideoWriter(out_name,cv2.VideoWriter_fourcc(*'mp4v'),fps/skip_frames , size)
# out_1 = cv2.VideoWriter('plot_skeleton.avi', cv2.VideoWriter_fourcc(*'DIVX'), 15, size)
#
for i in range(len(parsed_movie)):
    out_0.write(parsed_movie[i])
#     out_1.write(plot_skeleton[i])
out_0.release()
# out_1.release()

