import streamlit as st, pandas as pd
st.title("Validation List")
st.dataframe(pd.DataFrame([{"Validation ID":"VAL001","Status":"Open"}]))
