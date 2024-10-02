import cv2
import mediapipe as mp
import time
import numpy as np
import PoseEstimation as at
import pyttsx3
# 540 480
cap = cv2.VideoCapture('PoseVideos/11.mp4')
# cap = cv2.VideoCapture(0)
detector = at.poseDetector()
sound = pyttsx3.init()
count = 0
dir = 0
rep=0
while True:
    success, img = cap.read()
    # img = cv2.imread("PoseVideos/img2.jpg")
    img = cv2.resize(img, (1280, 720))
    img = detector.findPose(img,False)
    lmList = detector.findPosition(img, draw=False)
    if len(lmList) != 0:
        # #Right Arm
        # detector.findAngle(img, 12, 14, 16)
        #Left Arm
        angle = detector.findAngle(img, 11, 13, 15)
        per = np.interp(angle, (210, 310), (0, 100))
        bar = np.interp(angle, (210, 310), (650, 100))

        if per == 100:
            if dir == 0:
                count += 0.5
                dir = 1
        if per == 0:
            if dir == 1:
                count += 0.5
                dir = 0
        print(count)

        cv2.rectangle(img, (1100, 100), (1175, 650), (0, 255, 0), 3)
        cv2.rectangle(img, (1100, int(bar)), (1175, 650), (0, 255, 0), cv2.FILLED)
        cv2.putText(img, f'{int(per)}%', (1100, 75), cv2.FONT_HERSHEY_PLAIN, 4, (0, 255, 0), 4)
        cv2.putText(img, f'{int(count)}', (50, 100), cv2.FONT_HERSHEY_PLAIN, 5, (255, 0, 0), 5)

        if rep==count:
            # rep=count
            sound.say(str(int(count)))
            sound.runAndWait()
            if rep==count:
                rep+=1
        if count==5:
            sound.say("Good Job")
            sound.runAndWait()
            count=0
            rep=0
        # sound.say(str(int(count)))
        # sound.runAndWait()



    cv2.imshow("Image", img)
    cv2.waitKey(1)