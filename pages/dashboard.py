import streamlit as st
import pandas as pd


def get_column(df, target_name):
    """
    Find a column regardless of case or extra spaces.
    """

    for col in df.columns:
        if col.strip().lower() == target_name.lower():
            return col

    return None


def show_dashboard(df):

    st.title("📊 Validation Dashboard")

    # =====================================
    # Clean Column Names
    # =====================================

    df.columns = (
        df.columns
        .astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
    )

    # Debug (optional)
    # st.write(df.columns.tolist())

    # =====================================
    # Locate Columns Safely
    # =====================================

    validation_start_col = get_column(
        df,
        "Validation Start Date"
    )

    validation_end_col = get_column(
        df,
        "Validation End Date"
    )

    validator_col = get_column(
        df,
        "Validator"
    )

    environment_col = get_column(
        df,
        "Environment"
    )

    ci_owner_col = get_column(
        df,
        "CI Owner"
    )

    tier_col = get_column(
        df,
        "Service Level Tier"
    )

    number_col = get_column(
        df,
        "Number"
    )

    portfolio_col = get_column(
        df,
        "Portfolio Manager"
    )

    # =====================================
    # Date Conversions
    # =====================================

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

    # =====================================
    # KPI Metrics
    # =====================================

    total_validations = len(df)

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
                        -
                        pd.Timedelta(days=7)
                    )
                )
            ]
        )

    validators = 0

    if validator_col:
        validators = df[validator_col].nunique()

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Total",
        total_validations
    )

    col2.metric(
        "Completed",
        completed
    )

    col3.metric(
        "Pending",
        pending
    )

    col4.metric(
        "Validators",
        validators
    )

    col5.metric(
        "Overdue",
        overdue
    )

    st.divider()

    # =====================================
    # Environment Summary
    # =====================================

    st.subheader("🌎 Environment Distribution")

    if environment_col:

        env_summary = (
            df[environment_col]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )

        env_summary.columns = [
            "Environment",
            "Count"
        ]

        st.bar_chart(
            env_summary.set_index(
                "Environment"
            )
        )

    else:

        st.warning(
            "Environment column not found."
        )

    # =====================================
    # Service Level Tier
    # =====================================

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
            tier_summary.set_index(
                "Tier"
            )
        )

    else:

        st.warning(
            "Service Level Tier column not found."
        )

    # =========
