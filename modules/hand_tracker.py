import cv2
import mediapipe as mp
import numpy as np

class HandTracker:
    def __init__(self, min_detection_confidence=0.7, min_tracking_confidence=0.7, max_num_hands=1):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            min_detection_confidence=min_detection_confidence,
            min_tracking_confidence=min_tracking_confidence,
            max_num_hands=max_num_hands
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.results = None

    def find_hands(self, frame, draw=True):
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.results = self.hands.process(rgb)

        if self.results.multi_hand_landmarks and draw:
            for handLms in self.results.multi_hand_landmarks:
                self.mp_draw.draw_landmarks(frame, handLms, self.mp_hands.HAND_CONNECTIONS)

        return frame

    def get_finger_position(self, handLms, tip_id, frame_shape):
        h, w, c = frame_shape
        lm = handLms.landmark[tip_id]
        return int(lm.x * w), int(lm.y * h)

    # ✅ INDEX TIP (ID = 8)
    def get_index_finger_tip(self, handLms, frame_shape):
        return self.get_finger_position(handLms, 8, frame_shape)

    # ✅ ✅ THUMB TIP (ID = 4) — REQUIRED
    def get_thumb_finger_tip(self, handLms, frame_shape):
        return self.get_finger_position(handLms, 4, frame_shape)

    # ✅ Detect if ONLY index finger up
    def is_index_only_up(self, handLms):
        tips = [8, 12, 16, 20]
        pips = [6, 10, 14, 18]

        index_up = handLms.landmark[tips[0]].y < handLms.landmark[pips[0]].y
        others_down = all(
            handLms.landmark[tips[i]].y > handLms.landmark[pips[i]].y for i in range(1, 4)
        )

        return index_up and others_down

    def get_all_landmarks(self):
        if self.results and self.results.multi_hand_landmarks:
            return self.results.multi_hand_landmarks
        return None
