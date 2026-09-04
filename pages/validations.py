import streamlit as st
from service
st.title("Validation List")
st.dataframe(pd.DataFrame([{"Validation ID":"VAL001","Status":"Open"}]))
