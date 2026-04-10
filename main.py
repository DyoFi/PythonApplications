import cv2
import time
import random
import pygame

pygame.init()

video = cv2.VideoCapture(0, cv2.CAP_DSHOW)
face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
)  #Using pre-trained model

waiting_sound_played = False
last_count = None

face_detected = False
start_time = None
countdown_dura = 3 #seconds
waiting_sound = pygame.mixer.Sound("elevator_2jN6tnc.mp3")
yayy_sound = pygame.mixer.Sound("yayying.mp3")

while True:
    ret, frame = video.read()
    copy_frame = frame.copy()
    if not ret:
        print("Failed to grab frame")
        break

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray_frame, 1.2, 5)

    # print(len(faces))

    if len(faces) < 3:
        # print("Face is detected")
        cv2.putText(frame, f"Waiting...({len(faces)} detected)",  (10,30), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,255), 0)

        count = len(faces)

        if count == last_count:
            if not waiting_sound_played:
                waiting_sound.play()
                waiting_sound_played = True

        else:
            waiting_sound.stop()
            waiting_sound_played = False
        
        last_count = count

    if len(faces) >= 3:
        cv2.putText(frame, "YAAAYYY!!! Capturing..", (10,30), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,255), 0)
        

        if not face_detected:
            face_detected = True
            start_time = time.time()
            yayy_sound.play()
            print(start_time)  #1741824000 seconds = ~56 years,  January 1st 1970 to March 5th 2026

        else:
            # print("No face is detected")
            elapsed_time = time.time() - start_time
            remaining_time = int(countdown_dura - elapsed_time)
            if remaining_time > 0:
                cv2.putText(frame, str(remaining_time), (10,30), cv2.FONT_HERSHEY_DUPLEX, 1, (0,0,255), 0)

            if elapsed_time > countdown_dura:
                rand_num = random.randint(0,999)
                save_file = f"SelfieCamImg{rand_num}.png"
                cv2.imwrite(save_file, copy_frame)
                print("Image saved")
                break
        
    else:
        face_detected = False
        start_time = None

    cv2.imshow("Selfie Cam", frame)

    key = cv2.waitKey(1)
    if key == ord("q"):
        break

video.release()
cv2.destroyAllWindows()