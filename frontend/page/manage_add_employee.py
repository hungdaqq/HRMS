import streamlit as st
import cv2
import numpy as np
import pandas as pd
from deepface import DeepFace
from PIL import Image
from api.user import register, update_user_image

CSV_FILE = "/home/hung/Dev/HRMS/face_db/face_embeddings.csv"


# Function to extract face embeddings and save to CSV
def save_embedding(user_id, image):
    try:
        image_path = f"/home/hung/Dev/HRMS/face_db/images/{user_id}.jpg"
        image = Image.open(image)
        Image.fromarray(np.array(image)).save(image_path)  # Save image

        # Generate face embedding
        embedding = DeepFace.represent(img_path=image_path, model_name="Facenet")[0][
            "embedding"
        ]
        columns = ["id"] + [str(i) for i in range(len(embedding))]
        # Save employee info + embedding to CSV
        df = pd.DataFrame([[user_id] + embedding], columns=columns)
        df.to_csv(
            CSV_FILE,
            mode="a",
            header=not pd.io.common.file_exists(CSV_FILE),
            index=False,
        )
        print("Embedding saved to CSV.")
        return image_path

    except Exception as e:
        print(e)
        return None


# Streamlit UI
st.title("Manage Employees with Face Detection")

st.subheader("Add New Employee")

enable = st.checkbox("Enable camera")

picture = st.camera_input("Take a profile picture", disabled=not enable)


with st.form("add_employee_form"):
    username = st.text_input("Username")
    email = st.text_input("Email")
    title = st.selectbox("Engineer or Worker", ["Engineer", "Worker"])
    salary = st.number_input("Salary", min_value=10000000)
    password = st.text_input("Password", type="password")
    full_name = st.text_input("Full Name")
    if picture:
        st.write("Profile Picture")
        st.image(picture, width=300)
    add_button = st.form_submit_button("Add Employee", type="primary")
    if add_button:
        success, result = register(
            username,
            email,
            password,
            salary,
            title,
            full_name,
        )
        if success:
            user_id = result["id"]
            image_path = save_embedding(user_id, picture)
            if image_path:
                update_user_image(image_path, user_id)
                st.success(f"Employee {user_id} added successfully!")
            else:
                st.error("Failed to register.")

        else:
            st.error(result)
