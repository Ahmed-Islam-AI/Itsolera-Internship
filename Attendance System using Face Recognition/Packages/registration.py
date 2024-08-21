import json
import cv2
import os

def Registeration(name, id):
    # Dictionary to store user information
    # Load existing data if available
    path="D:\\Student_Attendance_System_using_face_recognition\\JsonData\\member_ids.json"
    if os.path.exists(path):
        with open(path, 'r') as f:
            data_dic = json.load(f)
    
    # Update dictionary with new user information
    data_dic[id] = name
    with open(path, 'w') as f:
        json.dump(data_dic, f)
    # Define paths
    new_path = "D:\\Student_Attendance_System_using_face_recognition\\images"
    image_path = f"{new_path}//{id}.jpg"

    # Create directory if it doesn't exist
    if not os.path.exists(new_path):
        os.makedirs(new_path)

    # Open the camera
    video = cv2.VideoCapture(0)

    # Haarcascade frontal face detector
    face_deect = cv2.CascadeClassifier("D:\\opencv\\haarcascade_frontalface_default.xml")

    # Variable to track if an image is captured
    image_captured = False

    while True:
        # Reading frame from video
        rate, frame = video.read()
        if not rate:
            print("Failed to grab frame")
            break

        
        
        # Convert image to gray
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces using Haar cascade
        faces = face_deect.detectMultiScale(gray, 1.3, 5)
        
        # Flag to check if a face is detected
        face_detected = False
        
        # Loop through detected faces
        for (x, y, w, h) in faces:
            face_detected = True
            crop_image = frame[y:y+h, x:x+w]
            resize = cv2.resize(crop_image, (224, 224))
            
            # Draw rectangle and put text
            cv2.rectangle(frame, (x-50, y-100), (x+w+100, y+h+100), (50, 50, 255), 2)
            cv2.putText(frame, str(f"Name : {data_dic[id]} ID :{id}"), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)
        
        # Display the frame
        cv2.imshow("image", frame)
        
        # Check if 'q' key is pressed
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            if face_detected:
                # Save image when face is detected and 'q' is pressed
                cv2.imwrite(image_path, resize)
            break

    # Release the camera and close windows
    video.release()
    cv2.destroyAllWindows()


