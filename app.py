import streamlit as st
import pandas as pd

from theme import apply_theme

from pages.dashboard import show_dashboard
from pages.validations import show_validations
from pages.reminders import show_reminders
from pages.reports import show_reports


# ==================================
# Page Configuration
# ==================================

st.set_page_config(
    page_title="KeyBank",
    page_icon="🔑",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==================================
# Apply Theme
# ==================================

apply_theme()

# ==================================
# Load Validation Data
# ==================================

try:
    df = pd.read_csv("data/validation_data.csv")

    # Remove leading/trailing spaces from column names
    df.columns = df.columns.str.strip()

except FileNotFoundError:
    st.error(
        "validation_data.csv not found in data folder."
    )
    df = pd.DataFrame()

except Exception as e:
    st.error(
        f"Error loading validation data: {e}"
    )
    df = pd.DataFrame()

# ==================================
# Custom Header
# ==================================

st.markdown(
    """
    <div style="
         background:white;
         padding:25px;
         border-radius:15px;
         margin-bottom:20px;
         box-shadow:0px 4px 15px rgba(0,0,0,0.10);
         border-left:6px solid #C00000;
    ">
         <h1 style="
             color:#C00000;
             text-align:center;
             margin-bottom:10px;
             font-size:48px;
             font-weight:bold;
         ">
             Finance App Support Validation Dashboard 📈
         </h1>
    </div>
    """,
    unsafe_allow_html=True
)

# ==================================
# Sidebar
# ==================================

st.sidebar.image(
    "https://1000logos.net/wp-content/uploads/2019/12/KeyBank.jpg",
    use_container_width=True
)

st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "",
    [
        "Dashboard",
        "Validations",
        "Reminders",
        "Reports"
    ]
)

# ==================================
# Page Routing
# ==================================

if menu == "Dashboard":

    if not df.empty:
        show_dashboard(df)
    else:
        st.warning("No validation data available.")

elif menu == "Validations":

    if not df.empty:
        show_validations(df)
    else:
        st.warning("No validation data available.")

elif menu == "Reminders":

    if not df.empty:
        show_reminders(df)
    else:
        st.warning("No validation data available.")

elif menu == "Reports":

    if not df.empty:
        show_reports(df)
    else:
        st.warning("No validation data available.")

# ==================================
# Footer
# ==================================

st.markdown("---")

st.markdown(
    """
    <div style='text-align:center;color:gray'>
         KeyBank 🔑
    </div>
    """,
    unsafe_allow_html=True
)
