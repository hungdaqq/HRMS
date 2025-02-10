import streamlit as st


def leave():
    st.title("Leave Management")
    st.write("This page allows you to manage leave requests.")

    # Apply for Leave
    st.subheader("Apply for Leave")
    with st.form("apply_leave_form"):
        employee_name = st.text_input("Employee Name")
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        reason = st.text_area("Reason for Leave")
        submit_button = st.form_submit_button("Submit Leave Request")
        if submit_button:
            st.success(f"Leave request for {employee_name} submitted successfully!")

    # Placeholder for Leave Tracking
    st.subheader("Leave Tracker")
    st.info("This section will display all leave requests and their statuses.")


leave()
