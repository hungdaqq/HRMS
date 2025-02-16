import streamlit as st


def manage_salary():
    st.title("Salary Management")
    st.write("This page allows you to calculate and view employee salaries.")

    # Salary Calculation
    st.subheader("Calculate Salary")
    with st.form("salary_calculation_form"):
        employee_name = st.text_input("Employee Name")
        days_worked = st.number_input("Days Worked", min_value=0, step=1)
        daily_wage = st.number_input("Daily Wage", min_value=0.0, step=0.1)
        submit_button = st.form_submit_button("Calculate Salary")
        if submit_button:
            total_salary = days_worked * daily_wage
            st.success(f"Total Salary for {employee_name}: ${total_salary:.2f}")


manage_salary()
