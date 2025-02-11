import streamlit as st


def manage_add_employees():
    st.title("Manage Employees")
    st.write("This page allows you to add new employee.")
    st.subheader("Add New Employee")
    with st.form("add_employee_form"):
        name = st.text_input("Name")
        email = st.text_input("Email")
        title = st.selectbox("Engineer or Worker ", ["Engineer", "Worker"])
        salary = st.number_input("Salary", min_value=1000.0)

        submit_button = st.form_submit_button("Add Employee")
        if submit_button:
            st.success(f"Employee {name} added successfully!")


manage_add_employees()
