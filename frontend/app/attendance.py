import streamlit as st


def attendance_management():
    st.title("Attendance Management")
    st.write("This page allows you to track attendance.")

    # Manual Entry
    st.subheader("Manual Attendance")
    with st.form("manual_attendance_form"):
        employee_name = st.text_input("Employee Name")
        date = st.date_input("Date")
        hours_worked = st.number_input("Hours Worked", min_value=0.0, step=0.5)
        submit_button = st.form_submit_button("Submit Attendance")
        if submit_button:
            st.success(f"Attendance for {employee_name} recorded successfully!")


attendance_management()
