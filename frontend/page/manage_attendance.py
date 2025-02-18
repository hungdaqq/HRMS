import streamlit as st
from api.attendance import get_attendance
import pandas as pd


def attendance_management():
    st.title("Attendance Management")
    st.write("This page allows you to track attendance.")
    # Mock data
    success, result = get_attendance()
    # Display employees
    st.subheader("Attendance List")
    if not success:
        st.error("Failed to fetch employees.")
    else:
        if not result["data"]:
            st.warning("No attendance records found.")
        else:
            df = pd.DataFrame(result["data"]).drop(["id"], axis=1)
            st.dataframe(
                df,
                column_config={
                    "created_at": st.column_config.DateColumn(
                        "Created At", format="DD MMM YYYY"
                    ),
                },
                use_container_width=True,
            )


attendance_management()
