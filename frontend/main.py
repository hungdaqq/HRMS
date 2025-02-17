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
        st.write(f"**Employee ID:** {user['id']}")
        st.write(f"**Username:** {user['username']}")
        st.write(f"**Email:** {user['email']}")
        st.write(f"**Is Admin:** {user['is_admin']}")
        st.write(f"**Created At:** {user['created_at']}")
        st.image(user["profile_image"], width=200)
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.rerun()


signin = st.Page(login_page, title="Log in", icon=":material/login:")
account = st.Page(
    account_information, title="Account Information", icon=":material/article_person:"
)

face_recognition = st.Page(
    "page/face_recognition.py",
    title="Face Recognition",
    icon=":material/face_unlock:",
)
manage_employee = st.Page(
    "page/manage_employee.py", title="Manage Employee", icon=":material/people:"
)

manage_add_employee = st.Page(
    "page/manage_add_employee.py", title="Add Employee", icon=":material/person_add:"
)
attendance = st.Page("page/attendance.py", title="Attendance", icon=":material/today:")

leave = st.Page("page/leave.py", title="Leave", icon=":material/check_in_out:")

manage_leave = st.Page(
    "page/manage_leave.py", title="Manage Leave", icon=":material/check_in_out:"
)

manage_approve_leave = st.Page(
    "page/manage_approve_leave.py",
    title="Approve Leave",
    icon=":material/check_in_out:",
)

manage_salary = st.Page(
    "page/manage_salary.py", title="Manage Salary", icon=":material/attach_money:"
)

if st.session_state.logged_in:
    if st.session_state.is_admin:
        pg = st.navigation(
            {
                "Live Feed": [face_recognition],
                "Account": [account],
                "Employee": [manage_employee, manage_add_employee],
                "Leave": [manage_leave, manage_approve_leave],
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
