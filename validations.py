import streamlit as st
from servicenow_client import get_validations

def show_validations():
  st.title("Validation Records")

  df = get_validations()

  status = st.selectbox(
     "Filter by Status",
     ["All","Failed","Open"]
  )

  if status != "All":
    df = df[df["status"] == status]

  st.dataframe(
     df,
     use_container_width=True
  )
