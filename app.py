import streamlit as st
import pandas as pd
import sqlite3
import subprocess
import sys
from datetime import datetime

DB_PATH = "database/attendance.db"

st.set_page_config(
    page_title="Hospital Attendance System",
    layout="wide"
)

# -------------------- STYLES --------------------
st.markdown("""
<style>
body { background-color: #f6f8fb; }

.card {
    background: #ffffff;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}

.kpi {
    font-size: 26px;
    font-weight: 700;
}

.label {
    color: #6c757d;
    font-size: 14px;
}

.badge-in {
    background: #d1f7e3;
    color: #0f5132;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 600;
}

.badge-out {
    background: #fde2e2;
    color: #842029;
    padding: 6px 14px;
    border-radius: 20px;
    font-weight: 600;
}

.header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #ffffff;
    padding: 14px 22px;
    border-radius: 14px;
    margin-bottom: 20px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.05);
}
</style>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
st.sidebar.markdown("## 🏥 HOSPITAL+")
page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Register Employee", "Attendance"]
)

# -------------------- DB HELPERS --------------------
def fetch_attendance():
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql(
        "SELECT name, timestamp, status FROM attendance ORDER BY timestamp DESC",
        conn
    )
    conn.close()
    return df


def today_summary():
    df = fetch_attendance()
    today = datetime.now().strftime("%Y-%m-%d")
    today_df = df[df["timestamp"].str.startswith(today)]

    punch_in = len(today_df[today_df["status"] == "Punch-In"])
    punch_out = len(today_df[today_df["status"] == "Punch-Out"])

    return punch_in, punch_out


# -------------------- HEADER --------------------
st.markdown("""
<div class="header">
    <strong>Hospital Attendance Dashboard</strong>
    <span>👤 Admin</span>
</div>
""", unsafe_allow_html=True)

# -------------------- DASHBOARD --------------------
if page == "Dashboard":
    st.subheader("Overview")

    punch_in, punch_out = today_summary()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.markdown(
            "<div class='card'><div class='label'>Employees</div>"
            "<div class='kpi'>1233</div></div>",
            unsafe_allow_html=True
        )

    with c2:
        st.markdown(
            f"<div class='card'><div class='label'>Punch-In Today</div>"
            f"<div class='kpi'>{punch_in}</div></div>",
            unsafe_allow_html=True
        )

    with c3:
        st.markdown(
            f"<div class='card'><div class='label'>Punch-Out Today</div>"
            f"<div class='kpi'>{punch_out}</div></div>",
            unsafe_allow_html=True
        )

    with c4:
        st.markdown(
            "<div class='card'><div class='label'>System Status</div>"
            "<div class='kpi'>Active</div></div>",
            unsafe_allow_html=True
        )

    st.markdown("### Recent Attendance")
    st.dataframe(fetch_attendance().head(8), width="stretch")

# -------------------- REGISTER --------------------
elif page == "Register Employee":
    st.subheader("Register New Employee")

    employee_name = st.text_input("Employee Name")

    if st.button("Register Face"):
        if not employee_name.strip():
            st.warning("Please enter employee name")
        else:
            st.info("Camera opened. Please face the camera.")
            subprocess.run(
                [sys.executable, "register_face.py", employee_name]
            )
            st.success(f"{employee_name} registered successfully")

# -------------------- ATTENDANCE --------------------
elif page == "Attendance":
    st.subheader("Attendance System")

    col1, col2 = st.columns([1, 2])

    with col1:
        if st.button("Start Attendance"):
            st.info("Attendance camera started. Press ESC to stop.")
            subprocess.run([sys.executable, "recognize_face.py"])

    with col2:
        st.markdown("""
        <div class="card">
            <strong>Instructions</strong><br><br>
            • Stand in front of the camera<br>
            • System handles Punch-In / Punch-Out automatically<br>
            • Duplicate entries are prevented
        </div>
        """, unsafe_allow_html=True)

    st.markdown("### Attendance Records")
    data = fetch_attendance()

    if not data.empty:
        data["Status"] = data["status"].apply(
            lambda s: "<span class='badge-in'>Punch-In</span>"
            if s == "Punch-In"
            else "<span class='badge-out'>Punch-Out</span>"
        )

        st.write(
            data[["name", "timestamp", "Status"]]
            .to_html(escape=False, index=False),
            unsafe_allow_html=True
        )
    else:
        st.info("No attendance records available")
