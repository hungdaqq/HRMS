import streamlit as st
from api.auth import login
from api.user import get_user_profile

st.set_page_config(page_title="HRMS", layout="wide")

st.title("HR Management System")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False


def login_page():
    st.subheader("Login your HRMS account")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Log in"):
        success, message = login(username, password)
        if success:
            st.session_state.access_token = message["access_token"]
            st.session_state.logged_in = True
            st.session_state.is_admin = message["is_admin"]
            st.rerun()
        else:
            st.error(message)


def account_information():
    st.subheader("Account Information")
    success, user = get_user_profile()
    if success:
        st.write("Id:", user["id"])
        st.write("Username:", user["username"])
        st.write("Email:", user["email"])
        st.write("Is Admin:", user["is_admin"])
        st.write("Created At:", user["created_at"])
        st.write("Updated At:", user["updated_at"])
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()


signin = st.Page(login_page, title="Log in", icon=":material/login:")
account = st.Page(
    account_information, title="Account Information", icon=":material/article_person:"
)
manage_employee = st.Page(
    "app/manage_employee.py", title="Employees", icon=":material/people:"
)
attendance = st.Page("app/attendance.py", title="Attendance", icon=":material/today:")
# manage_leave = st.Page(
#     "app/manage_leave.py", title="Leave", icon=":material/check_in_out:"
# )
leave = st.Page("app/leave.py", title="Leave", icon=":material/check_in_out:")
manage_salary = st.Page(
    "app/manage_salary.py", title="Salary", icon=":material/attach_money:"
)

if st.session_state.logged_in:
    if st.session_state.is_admin:
        pg = st.navigation(
            {
                "Account": [account],
                "Management": [manage_employee],
            }
        )
    else:
        pg = st.navigation(
            {
                "Account": [account],
                "Attendance": [attendance],
                "Leave": [leave],
                "Salary": [manage_salary],
            }
        )
else:
    pg = st.navigation([signin])

pg.run()
