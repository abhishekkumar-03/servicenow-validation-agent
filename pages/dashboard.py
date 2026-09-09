import streamlit as st
import pandas as pd


def get_column(df, target_name):
    for col in df.columns:
        if col.strip().lower() == target_name.lower():
            return col
    return None


def show_dashboard(df):

    st.title("📊 Validation Dashboard")

    # Clean column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
    )

    # Locate columns safely
    validation_start_col = get_column(
        df, "Validation Start Date"
    )

    validation_end_col = get_column(
        df, "Validation End Date"
    )

    validator_col = get_column(
        df, "Validator"
    )

    ci_owner_col = get_column(
        df, "CI Owner"
    )

    tier_col = get_column(
        df, "Service Level Tier"
    )

    portfolio_col = get_column(
        df, "Portfolio Manager"
    )

    number_col = get_column(
        df, "Number"
    )

    # Date conversion
    if validation_start_col:
        df[validation_start_col] = pd.to_datetime(
            df[validation_start_col],
            errors="coerce"
        )

    if validation_end_col:
        df[validation_end_col] = pd.to_datetime(
            df[validation_end_col],
            errors="coerce"
        )

    # KPI Metrics
    total = len(df)

    completed = 0
    pending = 0
    overdue = 0

    if validation_end_col:
        completed = (
            df[validation_end_col]
            .notna()
            .sum()
        )

        pending = (
            df[validation_end_col]
            .isna()
            .sum()
        )

    if validation_start_col and validation_end_col:
        overdue = len(
            df[
                (df[validation_end_col].isna())
                &
                (
                    df[validation_start_col]
                    <
                    (
                        pd.Timestamp.today()
                        - pd.Timedelta(days=7)
                    )
                )
            ]
        )

    validator_count = (
        df[validator_col].nunique()
        if validator_col
        else 0
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Total", total)
    col2.metric("Completed", completed)
    col3.metric("Pending", pending)
    col4.metric("Validators", validator_count)
    col5.metric("Overdue", overdue)

    st.divider()

    # Service Level Tier Distribution

    st.subheader(
        "🏆 Service Level Tier Distribution"
    )

    if tier_col:

        tier_summary = (
            df[tier_col]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )

        tier_summary.columns = [
            "Tier",
            "Count"
        ]

        st.bar_chart(
            tier_summary.set_index("Tier")
        )

    # Top Validators

    st.subheader("👤 Top Validators")

    if validator_col:

        validator_summary = (
            df[validator_col]
            .fillna("Unknown")
            .value_counts()
            .head(10)
            .reset_index()
        )

        validator
