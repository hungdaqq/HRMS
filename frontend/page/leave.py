import streamlit as st
from api.leave import create_leave, get_leave
import pandas as pd


def leave():
    st.title("Leave Management")
    st.write("Manage your leave requests")

    # Apply for Leave
    st.subheader("Apply for Leave")
    with st.form("apply_leave_form"):
        date = st.date_input("Leave date")
        reason = st.text_area("Reason for Leave")
        submit_button = st.form_submit_button("Submit Leave Request")
        if submit_button:
            success, data = create_leave(str(date), reason)
            if success:
                st.success(data["message"])
                st.rerun()
            else:
                st.error(data["message"])

    # Placeholder for Leave Tracking
    st.subheader("Leave Tracker")
    st.write("All leave request statuses")
    success, leave_requests = get_leave()
    if success:
        st.dataframe(
            pd.DataFrame(leave_requests["data"]),
            use_container_width=True,
            hide_index=True,
        )
    else:
        st.error(leave_requests["message"])


leave()
