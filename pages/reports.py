import streamlit as st
import pandas as pd


def show_reports(df):

    st.title("📄 Reports")

    st.subheader("Validation Report")

    st.metric(
        "Total Records",
        len(df)
    )

    st.dataframe(
        df,
        use_container_width=True
    )

    csv = df.to_csv(index=False)

    st.download_button(
        label="⬇ Download CSV Report",
        data=csv,
        file_name="validation_report.csv",
        mime="text/csv"
    )
