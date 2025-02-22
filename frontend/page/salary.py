import streamlit as st
from api.attendance import get_attendance
from api.leave import get_leave
from api.user import get_user_profile
import pandas as pd
import numpy as np

res = np.busday_count("2025-02", "2025-03")


def salary():
    st.title("Bảng lương")
    # Mock data
    _, attendances = get_attendance()
    _, leaves = get_leave()
    # Display employees
    st.subheader("Tổng công thực tế")
    if attendances["data"]:
        attendance_df = pd.DataFrame(attendances["data"]).drop(["id"], axis=1)
        if leaves["data"]:
            leave_df = pd.DataFrame(leaves["data"]).drop(["id"], axis=1)
            leave_df = leave_df[leave_df["status"] == "Approved"]
            leave_df["status"] = "Leave Approved"  # Mark as leave
            combined_df = pd.concat(
                [attendance_df, leave_df[["username", "date", "status"]]],
                ignore_index=True,
            )

        else:
            combined_df = attendance_df

        combined_df = combined_df.sort_values(by=["username", "date"]).reset_index(
            drop=True
        )
        combined_df["date"] = pd.to_datetime(combined_df["date"], format="mixed")
        combined_df["date"] = combined_df["date"].dt.date
        st.dataframe(
            combined_df.drop_duplicates(subset=["date"]),
            column_config={
                "date": st.column_config.DateColumn("Date", format="DD MMM YYYY"),
            },
            use_container_width=True,
        )
        work_day = len(combined_df.drop_duplicates(subset=["date"]))
        _, profile = get_user_profile()
        if profile:

            st.write(f"**Số ngày làm việc:** {work_day} days")
            st.write(f"**Lương tạm tính:** {work_day * profile['salary'] / res} VND")
        else:
            st.warning("Failed to fetch user profile.")
    else:
        st.warning("No attendance records found.")


salary()
