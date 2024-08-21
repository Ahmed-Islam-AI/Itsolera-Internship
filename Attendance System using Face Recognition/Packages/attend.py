import cv2
import pathlib
import face_recognition
import json
import mysql.connector
from datetime import datetime
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr
import os

def process_attendance():
    # Define paths and database configuration inside the function
    image_path = "D:\\Student_Attendance_System_using_face_recognition\\images"
    data_path = "D:\\Student_Attendance_System_using_face_recognition\\JsonData\\member_ids.json"
    haarcascade_path = "D:\\opencv\\haarcascade_frontalface_default.xml"
    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': 'Arham1234@',
        'database': 'centralized_hub'
    }

    # Email configuration
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587
    smtp_user = 'ak06598909@gmail.com'

    # Load image paths
    pathlib_path = pathlib.Path(image_path)
    img_list = [str(img) for img in pathlib_path.glob("*")]

    # Load known face encodings
    Known_Face_Encoding = []

    for img_path in img_list:
        image = face_recognition.load_image_file(img_path)
        encodings = face_recognition.face_encodings(image)
        if encodings:
            Known_Face_Encoding.append(encodings[0])

    # Load known face IDs
    with open(data_path, 'r') as f:
        data_dict = json.load(f)

    known_face_ids = list(data_dict.values())

    # Connect to the MySQL database
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return

    # Initialize video capture
    video = cv2.VideoCapture(0)

    # Haarcascade frontal face detector
    face_deect = cv2.CascadeClassifier(haarcascade_path)

    while True:
        # Capture frame from video
        ret, frame = video.read()
        if not ret:
            print("Failed to grab frame")
            break

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_deect.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        for (x, y, w, h) in faces:
            # Draw rectangle directly around the detected face
            x_start = x
            y_start = y
            x_end = x + w
            y_end = y + h
            
            crop_image = frame[y_start:y_end, x_start:x_end]

            if crop_image.size == 0:
                print(f"Skipping empty crop: ({x_start}, {y_start}, {x_end}, {y_end})")
                continue

            try:
                rgb_crop_image = cv2.cvtColor(crop_image, cv2.COLOR_BGR2RGB)
            except cv2.error as e:
                print(f"Error converting crop image to RGB: {e}")
                continue

            face_encodings = face_recognition.face_encodings(rgb_crop_image)

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(Known_Face_Encoding, face_encoding)
                name = "Unknown"
                person_id = None

                if True in matches:
                    match_index = matches.index(True)
                    name = known_face_ids[match_index]
                    person_id = list(data_dict.keys())[match_index]

                    try:
                        # Get current date
                        today = datetime.now().date()

                        # Check if a record already exists for this student on the current date
                        cursor.execute("SELECT * FROM attendance WHERE   ID=%s and date=%s" , ( person_id,today,))
                        existing_record = cursor.fetchone()

                        if not existing_record:
                            # Fetch record from the student_info table
                            cursor.execute("SELECT * FROM student_info WHERE ID = %s", (person_id,))
                            record = cursor.fetchone()

                            if record:
                                # Insert record into attendance table with current timestamp
                                cursor.execute(
                                    "INSERT INTO attendance (id, student_name, time, date, marked) VALUES (%s, %s, %s, %s, %s)",
                                    (record[0], record[1], datetime.now(), today, "Present")
                                )
                                conn.commit()
                                print(f"Record for ID {person_id} inserted into attendance table.")
                                
                                # Prepare and send email
                                subject = "Attendance Notification"
                                body = f"Hello,\n\n{record[1]} is present today.\n\nBest regards,\nAttendance System"
                                
                                try:
                                    msg = MIMEMultipart()
                                    msg['From'] = formataddr(('Attendance System', smtp_user))
                                    msg['To'] = record[3]  # Email of the student
                                    msg['Subject'] = subject

                                    msg.attach(MIMEText(body, 'plain'))
                                    
                                    with smtplib.SMTP(smtp_server, smtp_port) as server:
                                        server.starttls()
                                        server.login(smtp_user, "wykn uaph kpju cmbu")
                                        server.send_message(msg)
                                    print(f"Attendance email sent to {record[3]}")
                                
                                except smtplib.SMTPException as e:
                                    print(f"Failed to send email: {e}")

                        else:
                            print(f"Record for ID {person_id} already exists for today. Skipping.")

                    except mysql.connector.Error as e:
                        print(f"Database error: {e}")

                # Draw rectangle and put text on the frame
                cv2.rectangle(frame, (x_start, y_start), (x_end, y_end), (50, 50, 255), 2)
                cv2.putText(frame, f"Name: {name}", (x_start, y_start - 10), cv2.FONT_HERSHEY_COMPLEX, 1, (50, 50, 255), 2)

        # Display the frame
        cv2.imshow('Video', frame)

        # Break loop on 'q' key press
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # Release resources
    video.release()
    cv2.destroyAllWindows()
    conn.close()

