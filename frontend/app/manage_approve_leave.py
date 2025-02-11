import streamlit as st
from api.leave import get_new_leave, update_leave_request
import pandas as pd


def approve_leave():
    st.title("Approve Leave")
    st.write("This page allows you to approve or decline leave requests.")

    success, leave_requests = get_new_leave()
    if success:
        if leave_requests["data"]:
            for leave in leave_requests["data"]:
                with st.expander(f"Leave Request of {leave['full_name']}"):
                    st.write(f"**Employee ID:** {leave['id']}")
                    st.write(f"**Date:** {leave['date']}")
                    st.write(f"**Reason:** {leave['reason']}")
                    st.write(f"**Status:** {leave['status']}")

                    # Approval button for each leave request
                    approve_button = st.button(
                        f"Approve Leave",
                        key=f"approve_{leave['id']}",
                    )
                    if approve_button:
                        success, _ = update_leave_request(leave["id"], "Approved")
                        if success:
                            st.rerun()
                        else:
                            st.error("Failed to approve leave request.")
                    # Rejection button for each leave request
                    reject_button = st.button(
                        f"Reject Leave",
                        key=f"reject_{leave['id']}",
                    )
                    if reject_button:
                        success, _ = update_leave_request(leave["id"], "Rejected")
                        if success:
                            st.rerun()
                        else:
                            st.error("Failed to reject leave request.")

        else:
            st.info("No new leave requests.")
    else:
        st.info(leave_requests["message"])


approve_leave()
