import mediapipe as mp
import cv2

video = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils   
hands = mp_hands.Hands() 

def fingers_up(hand_landmarks):

    fingers = []
    finger_tips = [4,8,12,16,20]

    if hand_landmarks.landmark[finger_tips[0]].x < hand_landmarks.landmark[finger_tips[0]-1].x:
        fingers.append(1)
    else:
        fingers.append(0)

    for tips in finger_tips[1:]:
        if hand_landmarks.landmark[tips].y < hand_landmarks.landmark[tips-2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    if fingers == [0,0,0,0,0]:
        return 0 
    elif fingers == [0,1,0,0,0]:
        return 1
    elif fingers == [0,1,1,0,0]:
        return 2
    elif fingers == [0,1,1,1,0]:
        return 3
    elif fingers == [0,1,1,1,1]:
        return 4
    elif fingers == [1,0,0,0,0]:
        return 5
    elif fingers == [1,1,0,0,0]:
        return 6
    elif fingers == [1,1,1,0,0]:
        return 7
    elif fingers == [1,1,1,1,0]:
        return 8
    elif fingers == [1,1,1,1,1]:
        return 9
        
while True:
    ret, frame = video.read()
    if not ret:
        print("Could not capture frame")
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:

        hand_landmarks = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)
        detected_gesture = fingers_up(hand_landmarks)

        cv2.putText(frame, f"The number is: {detected_gesture}", (10,80),
                        cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 1)
        
    cv2.imshow("Abascus App", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()

