import streamlit as st
import plotly.express as px
from servicenow_client import get_validations

def show_dashboard():
  st.title("Validation Dahsboard")
  df = get_validations()

  total = len(df)
  failed = len(df[df["status"] == "Failed"])
  open_count = len(df[df["status"] == "Open"])
  critical = len(df[df["priority"] == "Critical"])

  c1,c2,c3,c4 = st.columns(4)

  c1.metric("Total", total)
  c1.metric("Failed", failed)
  c1.metric("Open", open_count)
  c1.metric("Critical", critical)

  st.subheader("Status Distribution")
  pie = px.pie(
        df,
        names="status",
        title="Validation Status"
  )

  st.plotly_chart(
    pie,
    use_container_width=TRue
  )

  st.subheader("Validation Aging")

  bar = px.bar(
       df,
      x="validation_id",
      y="age",
      color="priority",
      title="Aging Analysis"
  )

  st.plotly_chart(
     bar,
     use_container_width=True
  )
  
