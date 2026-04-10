import mediapipe as mp
import cv2
import pyautogui
import math

video = cv2.VideoCapture(0)
frame_width = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
frame_height = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))

mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils
hands = mp_hands.Hands(max_num_hands = 1)

button_name = "JUMP"
button_x, button_y = 100,100
button_w, button_h = 200,100

pinch_flag = False
pinch_threshold = 40

def draw_button(frame):
    cv2.rectangle(frame, (button_x, button_y),
                  (button_x + button_w, button_y + button_h),
                  (0,0,0), -1)
    
    cv2.putText(frame, button_name,
                (button_x + 30, button_y + 65),
                cv2.FONT_HERSHEY_SIMPLEX,
                1, (255,0,0), 2)

def detect_pinch(index_tip, thumb_tip):
    global pinch_flag

    index_x, index_y = index_tip
    thumb_x, thumb_y = thumb_tip

    distance = math.sqrt((index_x - thumb_x)**2 + (index_y - thumb_y)**2)

    inside_button = (button_x < index_x < button_x + button_w and
                     button_y < index_y < button_y + button_h)
    
    if distance < pinch_threshold and inside_button:
        if not pinch_flag:
            pyautogui.press("space")
            pinch_flag = True
    
    else:
        pinch_flag = False

    
while True:
    ret, frame = video.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            height, width, space = frame.shape

            index_x = int(hand_landmarks.landmark[8].x * width)
            index_y = int(hand_landmarks.landmark[8].y * height)

            thumb_x = int(hand_landmarks.landmark[4].x * width)
            thumb_y = int(hand_landmarks.landmark[4].y * height)

            cv2.circle(frame, (index_x, index_y), 10, (0,255,0), -1)
            cv2.circle(frame, (thumb_x, thumb_y), 10, (0,255,0), -1)
            
            detect_pinch((index_x, index_y), (thumb_x, thumb_y))

    draw_button(frame)

    cv2.imshow("Dino game", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()