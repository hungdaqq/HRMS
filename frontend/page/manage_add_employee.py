import streamlit as st
import cv2
import numpy as np
import pandas as pd
from deepface import DeepFace
from PIL import Image

CSV_FILE = "face_embeddings.csv"


# Function to extract face embeddings and save to CSV
def save_embedding(name, email, title, salary, image):
    try:
        image_path = f"captured_face_{name}.jpg"
        Image.fromarray(image).save(image_path)  # Save image

        # Generate face embedding
        embedding = DeepFace.represent(img_path=image_path, model_name="Facenet")[0][
            "embedding"
        ]

        # Save employee info + embedding to CSV
        df = pd.DataFrame([[name, email, title, salary] + embedding])
        df.to_csv(
            CSV_FILE,
            mode="a",
            header=not pd.io.common.file_exists(CSV_FILE),
            index=False,
        )

        st.success(f"Employee {name} added successfully with face embedding!")
    except Exception as e:
        st.error(f"Error processing face: {e}")


# Streamlit UI
st.title("Manage Employees with Face Detection")

st.subheader("Add New Employee")

# Capture button
if st.button("Capture Face"):

    cap = cv2.VideoCapture(-1)  # Open webcam

    if not cap.isOpened():
        st.error("Could not open webcam.")

    captured_face = None

    while True:
        ret, frame = cap.read()
        if not ret:
            st.error("Failed to capture image.")
            break

        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # Convert OpenCV BGR to RGB

        # Perform face detection using DeepFace
        try:
            faces = DeepFace.extract_faces(frame_rgb, detector_backend="mtcnn")
        except Exception as e:
            st.error(f"DeepFace Error: {e}")
            faces = []

        # Draw bounding boxes around detected faces
        for face in faces:
            region = face["facial_area"]
            x, y, w, h = region["x"], region["y"], region["w"], region["h"]
            cv2.rectangle(frame_rgb, (x, y), (x + w, y + h), (0, 255, 0), 2)

        cv2.imshow("Press 'C' to Capture", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("c"):  # Capture on 'C' key press
            image_path = "captured_face.jpg"
            cv2.imwrite(image_path, frame)
            cap.release()
            cv2.destroyAllWindows()

        cap.release()
        cv2.destroyAllWindows()


with st.form("add_employee_form"):
    name = st.text_input("Name")
    email = st.text_input("Email")
    title = st.selectbox("Engineer or Worker", ["Engineer", "Worker"])
    salary = st.number_input("Salary", min_value=1000.0)
    capture_button = st.form_submit_button("Add Employee", type="primary")

    if capture_button:
        captured_img = frame_rgb
        if captured_img is not None:
            st.image(
                captured_img, caption="Captured Face", use_column_width=True
            )  # Show captured face
            save_embedding(name, email, title, salary, captured_img)
