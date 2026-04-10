import cv2
import mediapipe as mp
import pyautogui

video = cv2.VideoCapture(0)

mp_hands = mp.solutions.hands
mp_drawings = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands = 1)

width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

screen_width, screen_height = pyautogui.size()

draw_points = []

while True:
    ret, frame = video.read()
    if not ret:
        print("Could not read frame")
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    hand_landmarks = results.multi_hand_landmarks

    if hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_drawings.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            landmarks = hand_landmarks.landmark

            index_x = int(landmarks[8].x * width)
            index_y = int(landmarks[8].y * height)

            cv2.circle(frame, (index_x, index_y), 5, (0, 255, 0), 2)

            draw_points.append((index_x, index_y))

    for i in range(1, len(draw_points)):
        cv2.line(frame, draw_points[i-1], draw_points[i], (0,255,0), 5)

    cv2.imshow("Air Drawing", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

    if key == ord("c"):
        draw_points = []

video.release()
cv2.destroyAllWindows()

