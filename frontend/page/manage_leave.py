import streamlit as st
from api.leave import get_leave
import pandas as pd


def leave():
    st.title("Leave Management")
    st.write("This page allows you to manage leave requests.")
    success, leave_requests = get_leave()
    if success:
        if leave_requests["data"]:
            st.dataframe(
                pd.DataFrame(leave_requests["data"]).drop(
                    ["id", "employee_id"], axis=1
                ),
                use_container_width=True,
                # hide_index=True,
            )
        else:
            st.info("No leave requests found.")
    else:
        st.error(leave_requests["message"])


leave()
