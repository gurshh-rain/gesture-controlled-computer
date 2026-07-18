import cv2 as cv
import mediapipe as mp
import time
import autopy
import numpy as np
import pyautogui

class handDetector():
    def __init__(self, mode=False, max_hands=2, min_detection_confidence=0.5, min_tracking_confidence=0.5):
        self.mode = mode
        self.max_hands = max_hands
        self.min_detection_confidence = min_detection_confidence
        self.min_tracking_confidence = min_tracking_confidence

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.min_detection_confidence,
            min_tracking_confidence=self.min_tracking_confidence
        )
        self.mpDraw = mp.solutions.drawing_utils

    def findHands(self, frame, draw=True):
        imgRGB = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(imgRGB)

        #print(results.multi_hand_landmarks)

        if self.results.multi_hand_landmarks:
            for handLm in self.results.multi_hand_landmarks:
                for id, lm in enumerate(handLm.landmark):
                    if draw:    
                        self.mpDraw.draw_landmarks(frame, handLm, self.mpHands.HAND_CONNECTIONS)

        return frame

    def findPosition(self, frame, handNum = 0, draw=True):
        lmlist = []
        
        if self.results.multi_hand_landmarks:
            myHand = self.results.multi_hand_landmarks[handNum]

            for id, lm in enumerate(myHand.landmark):
                h,w,c = frame.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmlist.append([id,cx,cy])
                if draw:
                    cv.circle(frame, (cx,cy), 10, (255,0,255), cv.FILLED)

        return lmlist



    


def main():
    pTime = 0
    cTime = 0
    capture = cv.VideoCapture(0)
    detector = handDetector()
    screen_w, screen_h = autopy.screen.size()
    SMOOTHING = 6
    FRAME_REDUCTION = 50
    cam_w, cam_h = 640, 480
    capture.set(3, cam_w)
    capture.set(4, cam_h)
    prev_x, prev_y = 0, 0

    prev_dist_y = 0
    prev_time = time.time()
    prev_velocity = 0
    SCROLL_SCALE = 1.2
    SCROLL_COOLDOWN = 0.4
    while True:
        success, frame = capture.read()

        if not success:
            break

        current_time = time.time()
        dt = current_time - prev_time

        frame = cv.flip(frame, 1)
        frame = detector.findHands(frame)
        lmlist = detector.findPosition(frame)

        if len(lmlist) != 0:
            if lmlist[8][2] < lmlist[7][2]:
                print('up')
                screen_x = np.interp(lmlist[8][1], [FRAME_REDUCTION, cam_w - FRAME_REDUCTION], [0, screen_w])
                screen_y = np.interp(lmlist[8][2], [FRAME_REDUCTION, cam_h - FRAME_REDUCTION], [0, screen_h])

                curr_x = prev_x + (screen_x - prev_x) / SMOOTHING
                curr_y = prev_y + (screen_y - prev_y) / SMOOTHING

                autopy.mouse.move(
                    min(max(curr_x, 0), screen_w - 1),
                    min(max(curr_y, 0), screen_h - 1)
                )
                prev_x, prev_y = curr_x, curr_y        
                distance = np.sqrt((pow(lmlist[8][1] - lmlist[4][1],2)) + (pow(lmlist[4][2] - lmlist[8][2],2)))

                #print(distance)
                if distance <= 35:
                    autopy.mouse.toggle(autopy.mouse.Button.LEFT,True)
                    distance = np.sqrt((pow(lmlist[8][1] - lmlist[4][1],2)) + (pow(lmlist[4][2] - lmlist[8][2],2)))

                else:
                    autopy.mouse.toggle(autopy.mouse.Button.LEFT, False)

            else:
                print('not')    
                autopy.mouse.toggle(autopy.mouse.Button.LEFT,False)
            
            distance_middle = np.sqrt((pow(lmlist[12][1] - lmlist[8][1],2)) + (pow(lmlist[8][2] - lmlist[12][2], 2)))
            last_scroll_time = 0

            if distance_middle <= 25:

                current_y = lmlist[8][2]
                

                delta_y = current_y - prev_dist_y

                prev_dist_y = current_y

                velocity = delta_y / dt

                acceleration = (velocity - prev_velocity) / dt
                last_scroll_time = 0
                print(acceleration)
                if acceleration >= 0.0005 and lmlist[12][2] < lmlist[10][2]:
                    scroll_amount = max(5, int(abs(velocity) * SCROLL_SCALE))
                    pyautogui.scroll(-scroll_amount)
                    last_scroll_time = current_time 

                if acceleration <= 0 and lmlist[12][2] > lmlist[10][2]:
                    scroll_amount = max(5, int(abs(velocity) * SCROLL_SCALE))
                    pyautogui.scroll(scroll_amount)
                    last_scroll_time = current_time 




        cTime = time.time()
        fps = 1/(cTime-pTime)
        pTime = cTime

        cv.putText(frame, str(int(fps)), (10, 70), cv.FONT_HERSHEY_PLAIN, 3, (255, 255, 0), 2)
        cv.imshow("image", frame)
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

main()
 