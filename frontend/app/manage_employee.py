import streamlit as st
from api.user import get_all_users
import pandas as pd


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
        df = pd.DataFrame(employees["data"])
        st.write(df)
    # Add Employee
    st.subheader("Add New Employee")
    with st.form("add_employee_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        position = st.text_input("Position")
        submit_button = st.form_submit_button("Add Employee")
        if submit_button:
            st.success(f"Employee {name} added successfully!")


manage_employees()
