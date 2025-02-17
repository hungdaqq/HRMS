import streamlit as st
import cv2
import numpy as np
import pandas as pd
from deepface import DeepFace
from PIL import Image
from api.user import register, update_user_image, get_all_users

CSV_FILE = "/home/hungdq30/Dev/HRMS/face_db/face_embeddings.csv"


# Load stored face embeddings from CSV
def load_embeddings():
    try:
        success, result = get_all_users()
        df = pd.read_csv(CSV_FILE)
        df.rename(columns={"0": "id"}, inplace=True)
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
            print(merged_df)
        else:
            merged_df = df
            st.error(result["message"])
        return merged_df
    except FileNotFoundError:
        print("No stored embeddings found.")
        return None


# Compare captured face with stored embeddings
def recognize_face(face_img, known_embeddings):
    try:
        # Extract embedding for captured face
        embedding = DeepFace.represent(face_img, model_name="Facenet")[0]["embedding"]

        best_match = None
        best_distance = float("inf")

        for index, row in known_embeddings.iterrows():
            user_id = row.iloc[1]  # First column is name
            stored_embedding = np.array(row.iloc[1:].astype(float))

            # Compute Euclidean distance
            distance = np.linalg.norm(embedding - stored_embedding)

            if distance < best_distance and distance < 10:  # Threshold for face match
                best_distance = distance
                best_match = user_id

        return best_match if best_match else "Unknown"
    except Exception as e:
        print(f"Face recognition error: {e}")
        return "Error"


def face_detection():
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
            identity = recognize_face(face_img, known_embeddings)

            # Draw bounding box & name
            color = (0, 255, 0) if identity != "Unknown" else (0, 0, 255)
            cv2.rectangle(frame_rgb, (x, y), (x + w, y + h), color, 2)
            cv2.putText(
                frame_rgb,
                identity,
                (x, y - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.8,
                color,
                2,
            )

        frame_holder.image(frame_rgb, channels="RGB", caption="Webcam Feed")

        if cv2.waitKey(1) & 0xFF == ord("q"):  # Press 'q' to quit
            break

    cap.release()
    cv2.destroyAllWindows()


face_detection()
