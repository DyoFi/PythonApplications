import cv2
import random
import time

video = cv2.VideoCapture(0)

adjectives = ["Intelligent", "Fantastic", "Awesome", "Brilliant", "Amazing"]

snapshot_timer = 0
change_interval = 2

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    )

start_time = time.time()
last_change = time.time()
current_adjective = random.choice(adjectives)

while True:
    ret, frame = video.read()
    if not ret:
        print("Could not capture frame")
        break

    current_time = time.time()

    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 7)
    if len(faces) > 0:

        if current_time - last_change >= change_interval:
            current_adjective = random.choice(adjectives)
            last_change = current_time

        for (x,y,w,h) in faces:
            cv2.rectangle(
                frame, (x,y), 
                (x+w, y+h), 
                (255,0,0),
                2
                )
            cv2.putText(frame, f"{current_adjective}", (x+5, y-20), cv2.FONT_HERSHEY_DUPLEX, 1, (0,255,0), 0)

    cv2.imshow("Cheer Cam App", frame)

    copy_frame = frame.copy()

    key = cv2.waitKey(1)
    if key == ord("q"):
        break
    if key == ord("s"):
        rand_num = random.randint(0,999)
        save_file = f"CheerCamImg{rand_num}.png"
        cv2.imwrite(save_file, copy_frame)
        print("Image saved")
        break

video.release()
cv2.destroyAllWindows()


