import cv2
import mediapipe as mp
 
mp_hands = mp.solutions.hands.Hands()

cap = cv2.VideoCapture(0)

while True:
    # Frame
    ret, frame = cap.read()
    frame = cv2.flip(frame, 1)
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = mp_hands.process(frame_rgb)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp.solutions.drawing_utils.draw_landmarks(frame, hand_landmarks, mp.solutions.hands.HAND_CONNECTIONS)

    cv2.imshow('Hand Detection', frame)

    if cv2.waitKey(1) == ord('0'):
        break

cap.release()
cv2.destroyAllWindows()