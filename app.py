import streamlit as st

from theme import apply_theme

from pages.dashboard import show_dashboard
from pages.validations import show_validations
from pages.reminders import show_reminders
from pages.reports import show_reports

#==================================
# Page Cofiguration
#==================================


st.set_page_config(
    page_title="Keybank",
    page_icon="🔑",
    layout="wide",
    initial_sidebar_state="expanded"
)

#====================================
# APPPLY THEME
#====================================

apply_theme()

#====================================
# CUSTOM HEADER
#====================================

st.markdown(
  """
  <div style="
       background:white;
       padding:25px;
       border-radius:15px;
       margin-bottom:20px
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
     Finance App support Validation Dashboard 📈
     </h1>
  """,
  unsafe_allow_html=True
)

#==========================================
# Sidebar
#==========================================

st.sidebar.image(
"https://1000logos.net/wp-content/uploads/2019/12/KeyBank.jpg",
use_container_width=True
)

st.sidebar.title("Navigation")

menu=st.sidebar.radio(
  "",
  [
    "Dashboard",
    "Validations",
    "Reminders",
    "Reports"
  ]
)

#===========================================
# Page Routing
#===========================================

if menu == "Dashboard":
  show_dashboard()

elif menu == "Validations":
  show_validations()

elif menu == "Reminders":
  show_reminders()

elif menu == "Reports":
  show_reports()


#=============================================
# Footer
#=============================================

st.markdown("---")

st.markdown(
  """
  <div style='text-align:center;color:gray'>
       Keybank 🔑
  </div>
  """,
  unsafe_allow_html=True
)
