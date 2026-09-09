import streamlit as st
import pandas as pd


def show_validations(df):

    st.title("📋 Validation List")

    # Clean column names
    df.columns = df.columns.str.strip()

    # Search box
    search = st.text_input(
        "🔍 Search Validation Number"
    )

    filtered_df = df.copy()

    if search:
        filtered_df = filtered_df[
            filtered_df["Number"]
            .astype(str)
            .str.contains(
                search,
                case=False,
                na=False
            )
        ]

    # Filters
    st.subheader("Filters")

    col1, col2 = st.columns(2)

    with col1:

        environments = ["All"] + sorted(
            filtered_df["Environment"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_env = st.selectbox(
            "Environment",
            environments
        )

    with col2:

        validators = ["All"] + sorted(
            filtered_df["Validator"]
            .dropna()
            .unique()
            .tolist()
        )

        selected_validator = st.selectbox(
            "Validator",
            validators
        )

    # Apply filters

    if selected_env != "All":

        filtered_df = filtered_df[
            filtered_df["Environment"]
            == selected_env
        ]

    if selected_validator != "All":

        filtered_df = filtered_df[
            filtered_df["Validator"]
            == selected_validator
        ]

    # Summary Metrics

    st.subheader("Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Records",
        len(filtered_df)
    )

    col2.metric(
        "Unique Validators",
        filtered_df["Validator"].nunique()
    )

    col3.metric(
        "Unique Environments",
        filtered_df["Environment"].nunique()
    )

    st.divider()

    # Data Table

    st.subheader("Validation Records")

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=500
    )

    # Download CSV

    csv = filtered_df.to_csv(
        index=False
    )

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="validation_records.csv",
        mime="text/csv"
    )
