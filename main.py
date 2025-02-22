import cv2
import mediapipe as mp
import pyautogui
import math

pyautogui.FAILSAFE = False

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

camera = cv2.VideoCapture(0)

def distance(p1, p2):
    """ ngitung jarak antara dua titik """
    return math.sqrt((p1.x - p2.x)**2 + (p1.y - p2.y)**2)

def to_pixel_coords(landmark, frame_width, frame_height):
    """ konversikan koordinat normalisasi (0-1) ke koordinat pixel """
    return int(landmark.x * frame_width), int(landmark.y * frame_height)

with mp_hands.Hands(
    model_complexity=0,
    max_num_hands=2,  
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5
) as hands:

    gesture_text = "TIDAK DIKENALI"
    last_gesture = ''

    while True:
        sts, frame = camera.read()
        if not sts:
            break

        frame = cv2.flip(frame, 1)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame_rgb)

        frame_height, frame_width, _ = frame.shape 

        tangan_kanan = []
        tangan_kiri = []

        if result.multi_hand_landmarks and len(result.multi_hand_landmarks) == 2:
            hand1 = result.multi_hand_landmarks[0]
            hand2 = result.multi_hand_landmarks[1]

            label1 = result.multi_handedness[0].classification[0].label
            label2 = result.multi_handedness[1].classification[0].label

            if label1 == 'Right':
                right_hand, left_hand = hand1, hand2
            else:
                right_hand, left_hand = hand2, hand1

            right_thumb = right_hand.landmark[4]
            left_thumb = left_hand.landmark[4]
            right_index = right_hand.landmark[8]
            left_index = left_hand.landmark[8]

            thumb_distance = distance(right_thumb, left_thumb)
            index_distance = distance(right_index, left_index)
            thumb_index_right = distance(right_thumb, right_index)
            thumb_index_left = distance(left_thumb, left_index)

            right_thumb_px = to_pixel_coords(right_thumb, frame_width, frame_height)
            left_thumb_px = to_pixel_coords(left_thumb, frame_width, frame_height)
            right_index_px = to_pixel_coords(right_index, frame_width, frame_height)
            left_index_px = to_pixel_coords(left_index, frame_width, frame_height)

            
            if thumb_distance < 0.08 and index_distance < 0.08 and \
               (thumb_index_right > thumb_distance and thumb_index_left > index_distance):
                gesture_text = "ULTI NOLAN"
                tangan_kanan = [right_thumb_px, right_index_px]
                tangan_kiri = [left_thumb_px, left_index_px]

        
        if result.multi_hand_landmarks:
            tangan_kanan = []
            tangan_kiri = []

            for hand_idx, hand_landmarks in enumerate(result.multi_hand_landmarks):
                label = result.multi_handedness[hand_idx].classification[0].label
                mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
                points = []  

                for idx in [2, 3, 4, 5, 6, 7, 8]:  
                    landmark = hand_landmarks.landmark[idx]
                    x, y = int(landmark.x * frame.shape[1]), int(landmark.y * frame.shape[0])
                    points.append((x, y))

                if label == 'Right':
                    tangan_kanan = points.copy()  
                else:
                    tangan_kiri = points.copy()

            
            if gesture_text == "ULTI NOLAN" and tangan_kanan and tangan_kiri:
                cv2.line(frame, tangan_kanan[0], tangan_kanan[1], (255, 0, 255), 6)
                cv2.line(frame, tangan_kanan[1], tangan_kanan[2], (255, 0, 255), 6)
                cv2.line(frame, tangan_kanan[3], tangan_kanan[4], (255, 0, 255), 6)
                cv2.line(frame, tangan_kanan[4], tangan_kanan[5], (255, 0, 255), 6)
                cv2.line(frame, tangan_kanan[5], tangan_kanan[6], (255, 0, 255), 6)

                cv2.line(frame, tangan_kiri[0], tangan_kiri[1], (255, 0, 255), 6)
                cv2.line(frame, tangan_kiri[1], tangan_kiri[2], (255, 0, 255), 6)
                cv2.line(frame, tangan_kiri[3], tangan_kiri[4], (255, 0, 255), 6)
                cv2.line(frame, tangan_kiri[4], tangan_kiri[5], (255, 0, 255), 6)
                cv2.line(frame, tangan_kiri[5], tangan_kiri[6], (255, 0, 255), 6)


                cv2.line(frame, tangan_kanan[2], tangan_kiri[2], (255, 0, 255), 6)
                cv2.line(frame, tangan_kanan[6], tangan_kiri[6], (255, 0, 255), 6)



        if gesture_text != last_gesture:
            if gesture_text == "ULTI NOLAN":
                pyautogui.press('u')  
        
        last_gesture = gesture_text


        cv2.putText(frame, gesture_text, (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 255), 3, cv2.LINE_AA)

        cv2.imshow('Deteksi Gestur Ulti Nolan', frame)
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

camera.release()
cv2.destroyAllWindows()
