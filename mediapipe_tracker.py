import os
import cv2
import mediapipe as mp
import numpy as np
from pythonosc import udp_client

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_drawing = mp.solutions.drawing_utils

client = udp_client.SimpleUDPClient("127.0.0.1", 12345)

cap = cv2.VideoCapture(0)

def calculate_inclination(landmarks):
    x1, y1 = landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].x, landmarks[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    x2, y2 = landmarks[mp_hands.HandLandmark.WRIST].x, landmarks[mp_hands.HandLandmark.WRIST].y
    return np.arctan2(y2 - y1, x2 - x1)

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)

    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(results.multi_hand_landmarks):
            mp_drawing.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)
            index_finger_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            hand_label = results.multi_handedness[idx].classification[0].label
            if hand_label == 'Right':
                inclination = calculate_inclination(hand_landmarks.landmark)
                client.send_message("/right_hand/inclination", inclination)
                print("/right_hand/inclination", inclination)
                #print(f"Sent /right_hand/inclination{inclination}")
            elif hand_label == 'Left':
                inclination = calculate_inclination(hand_landmarks.landmark)
                client.send_message("/left_hand/inclination", inclination)
                print("/left_hand/inclination", inclination)
                #print(f"Sent /left_hand/inclination {inclination}")

    cv2.imshow('MediaPipe Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
