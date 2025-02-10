import streamlit as st
from api.leave import create_leave, get_leave


def leave():
    st.title("Leave Management")
    st.write("Manage your leave requests")

    # Apply for Leave
    st.subheader("Apply for Leave")
    with st.form("apply_leave_form"):
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        reason = st.text_area("Reason for Leave")
        submit_button = st.form_submit_button("Submit Leave Request")
        if submit_button:
            success, data = create_leave(start_date, end_date, reason)
            if success:
                st.success(data["message"])
                st.rerun()
            else:
                st.error(data["message"])

    # Placeholder for Leave Tracking
    st.subheader("Leave Tracker")
    st.write("All leave request statuses")
    success, leave_requests = get_leave()
    print(leave_requests)
    if success:
        st.write(leave_requests["data"])
    else:
        st.error(leave_requests["message"])


leave()
