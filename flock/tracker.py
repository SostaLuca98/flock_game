import cv2
import mediapipe as mp
import numpy as np
from .config import args

class Tracker:

    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands    = self.mp_hands.Hands()
        self.mp_drawing = mp.solutions.drawing_utils
        self.cap = cv2.VideoCapture(0)

    def quit(self):
        self.cap.release()
        cv2.destroyAllWindows()

    def calculate_inclination(self, landmarks):
        x1, y1 = landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].x, landmarks[self.mp_hands.HandLandmark.INDEX_FINGER_TIP].y
        x2, y2 = landmarks[self.mp_hands.HandLandmark.WRIST].x,            landmarks[self.mp_hands.HandLandmark.WRIST].y
        return np.arctan2(y1 - y2, x1 - x2)*360/np.pi/2 +np.pi

    def track(self):
        success, image = self.cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            return

        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image.flags.writeable = False
        results = self.hands.process(image)

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        inclination = None
        if results.multi_hand_landmarks:
            for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
                self.mp_drawing.draw_landmarks(image, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)
                #index_finger_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
                hand_label = results.multi_handedness[idx].classification[0].label
                if hand_label == 'Right' or hand_label =='Left':
                    inclination = self.calculate_inclination(hand_landmarks.landmark)

        if args.CAMERA_FLAG:
            cv2.imshow('MediaPipe Hands', image)

        if inclination is not None: return int(inclination)