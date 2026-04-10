import cv2
import mediapipe as mp
import random
import time

mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils
hands = mp_hands.Hands()

video = cv2.VideoCapture(0)

score = 0
instruction_start = time.time()
reaction_time = 2
round_time = time.time()
instruction_delay = 4
target_score = 5
current_instruction = None
result_message = ""
hold_time = 2
stable_gesture = None
stable_since = None
locked = False
user_choice = None
game_over = False
final_message = ""



def finger_gestures(hand_landmarks):
    
    fingers = []
    finger_tip = [8,12,16,20]

    for tip in finger_tip:

        if hand_landmarks.landmark[tip].y < hand_landmarks.landmark[tip-2].y:
            fingers.append(1)
        else:
            fingers.append(0)

    if fingers == [0,0,0,0]:
        return "Rock"
    
    elif fingers == [1,1,0,0]:
        return "Scissor"
    
    elif fingers == [1,1,1,1]:
        return "Paper"
    
    else:
        return "Unknown"
    
instructions = ["Rock", "Paper", "Scissors",
                "Simon says Rock", "Simon says Paper",
                "Simon says Scissors"]

while True:

    ret, frame = video.read()

    if not ret:
        print("Could not capture frame")
        break

    frame = cv2.flip(frame, 1)

    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb_frame)

    if time.time() - round_time > instruction_delay:
        current_instruction = random.choice(instructions)
        round_time = time.time()
        instruction_start = time.time()
        result_message = ""
        locked = False
        user_choice = None

    if results.multi_hand_landmarks:

        hand_landmarks = results.multi_hand_landmarks[0]
        mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

        detected_gesture = finger_gestures(hand_landmarks)

        if detected_gesture != stable_gesture:
            stable_gesture = detected_gesture
            stable_since = time.time()
            locked = False

        else:
            if stable_gesture != "Unknown":

                if (
                    time.time() - stable_since >= hold_time 
                    and not locked
                    and time.time() - instruction_start >= reaction_time
                ):
                    locked = True
                    user_choice = stable_gesture

                    if current_instruction:
                        if "Simon says" in current_instruction:
                            target = current_instruction.split()[-1]

                            if user_choice == target:
                                result_message = "Correct!"
                                score += 1
                            else:
                                result_message = "Wrong move!"
                                score -= 1
                        else:
                            if user_choice in ["Rock", "Paper", "Scissors"]:
                                result_message = "Simon didn't say!"
                                score -= 1
                
            
    if score >= target_score:
        game_over = True
        final_message = "YOU WIN!"
    elif score < 0:
        game_over = True
        finale_message = "YOU LOSE!"
    
    cv2.putText(frame, f"Simon: {current_instruction}", (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 255), 2)

    cv2.putText(frame, f"Your move: {user_choice}", (10, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    cv2.putText(frame, result_message, (10, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

    cv2.putText(frame, f"Score: {score}/{target_score}", (10, 160),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
    remaining = int(reaction_time - (time.time() - instruction_start))
    if remaining > 0:
        cv2.putText(frame, f"Get Ready: {remaining}", (10, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,255), 2)
    
    if game_over:
        cv2.putText(frame, final_message, (200, 240),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 255), 3)
    
    cv2.imshow("Simon Says", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()