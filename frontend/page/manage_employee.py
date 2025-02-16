import streamlit as st
from api.user import get_all_users
import pandas as pd
from PIL import Image
from io import BytesIO
import base64


def get_thumbnail(path: str) -> Image:
    img = Image.open(path)
    img.thumbnail((100, 100))
    return img


def image_to_base64(img_path: str) -> str:
    img = get_thumbnail(img_path)
    with BytesIO() as buffer:
        img.save(buffer, "png")  # or 'jpeg'
        return base64.b64encode(buffer.getvalue()).decode()


def image_formatter(img_path: str) -> str:
    return f'<img src="data:image/png;base64,{image_to_base64(img_path)}">'


@st.cache_data
def convert_df(input_df):
    # IMPORTANT: Cache the conversion to prevent computation on every rerun
    return input_df.to_html(
        escape=False, formatters=dict(profile_image=image_formatter)
    )


def manage_employees():
    st.title("Manage Employees")
    st.write("This page allows you to manage employee information.")

    # Mock data
    success, employees = get_all_users()
    # Display employees
    st.subheader("Employee List")
    if not success:
        st.error("Failed to fetch employees.")
    else:
        df = pd.DataFrame(employees["data"]).drop(["id", "updated_at"], axis=1)
        st.dataframe(
            df,
            column_config={
                "created_at": st.column_config.DateColumn(
                    "Created At", format="DD MMM YYYY"
                ),
                "profile_image": st.column_config.LinkColumn("Profile Image"),
            },
            use_container_width=True,
        )


manage_employees()
