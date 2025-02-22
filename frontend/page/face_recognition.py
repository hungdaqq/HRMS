import streamlit as st
import cv2
import numpy as np
import pandas as pd
from deepface import DeepFace
from PIL import Image
from api.user import register, update_user_image, get_all_users
from api.attendance import create_attendance
import datetime

CSV_FILE = "/home/hung/Dev/HRMS/face_db/face_embeddings.csv"


detected_users = set()
last_reset_date = datetime.datetime.now()


# Load stored face embeddings from CSV
def load_embeddings():
    try:
        success, result = get_all_users()
        df = pd.read_csv(CSV_FILE)
        if success:
            db_df = pd.DataFrame(result["data"])
            db_df = db_df.drop(
                columns=[
                    "email",
                    "salary",
                    "title",
                    "is_admin",
                    "updated_at",
                    "created_at",
                    "profile_image",
                ]
            )
            merged_df = pd.merge(df, db_df, on="id", how="left")
        else:
            merged_df = df
            st.error(result["message"])
        return merged_df
    except FileNotFoundError:
        st.error("No stored embeddings found.")
        return None


# Compare captured face with stored embeddings
def recognize_face(face_img, known_embeddings):
    try:
        # Extract embedding for captured face
        embedding = DeepFace.represent(face_img, model_name="Facenet")[0]["embedding"]

        best_match = None
        best_distance = float("inf")
        for _, row in known_embeddings.iterrows():
            username = row.iloc[129]  # First column is name
            # user_id = row.iloc[0]  # Second column is user_id
            stored_embedding = np.array(row.iloc[1:129].astype(float))

            # Compute Euclidean distance
            distance = np.linalg.norm(embedding - stored_embedding)

            if distance < best_distance and distance < 10:  # Threshold for face match
                best_distance = distance
                best_match = username

        return best_match if best_match else "Unknown"

    except Exception as e:
        print(f"Face recognition error: {e}")
        return "Error"


def face_detection():
    global detected_users, last_reset_date
    st.title("Manage Employees with Face Detection")
    st.write("Face Detection and Recognition")

    st.subheader("Live Feed")
    cap = cv2.VideoCapture(-1)

    if not cap.isOpened():
        print("Could not open webcam.")
        return

    known_embeddings = load_embeddings()
    if known_embeddings is None:
        print("No stored embeddings found. Add employees first.")
        return

    frame_holder = st.empty()

    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to capture image.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB

        # Detect faces using DeepFace
        faces = DeepFace.extract_faces(frame_rgb, detector_backend="opencv")
        for face in faces:
            face_area = face["facial_area"]
            x = face_area["x"]
            y = face_area["y"]
            w = face_area["w"]
            h = face_area["h"]

            face_img = frame_rgb[y : y + h, x : x + w]  # Extract face region

            # Recognize face
            username = recognize_face(face_img, known_embeddings)

            # Draw bounding box & name
            color = (0, 255, 0) if username != "Unknown" else (255, 0, 0)
            cv2.rectangle(frame_rgb, (x, y), (x + w, y + h), color, 2)
            cv2.putText(
                frame_rgb,
                username,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2,
            )

            if username != "Unknown" and username != "Error":
                send_attendance_request(username)

        frame_holder.image(frame_rgb, channels="RGB", caption="Webcam Feed")

    cap.release()
    cv2.destroyAllWindows()


def send_attendance_request(username):
    global detected_users, last_reset_date

    now = datetime.datetime.now()
    elapsed_time = (now - last_reset_date).total_seconds() / 60
    # Reset tracking only once per day (before checking the username)
    # Reset every 15 minutes
    if elapsed_time >= 15:
        detected_users.clear()
        last_reset_date = now
        print("Reset detected users after 15 minutes.")

    # Check if the user is already marked
    if username not in detected_users:
        print(f"Detected: {username}")
        # print(f"Previously detected users: {detected_users}")

        success, result = create_attendance(username, "Present")
        print(result)
        if success:
            detected_users.add(username)
            print(f"Attendance recorded for {username}")
        else:
            print(f"Failed to record attendance for {username}")
    else:
        print(f"{username} is already marked present in this period.")


face_detection()
