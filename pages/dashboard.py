import streamlit as st
import pandas as pd


def show_dashboard(df):
    """
    Dashboard for Validation Records
    """

    st.title("📊 Validation Dashboard")

    # Clean column names
    df.columns = df.columns.str.strip()

    # Convert dates
    df["Validation Start Date"] = pd.to_datetime(
        df["Validation Start Date"],
        errors="coerce"
    )

    df["Validation End Date"] = pd.to_datetime(
        df["Validation End Date"],
        errors="coerce"
    )

    # -----------------------------
    # KPI Metrics
    # -----------------------------

    total_validations = len(df)

    completed_validations = (
        df["Validation End Date"]
        .notna()
        .sum()
    )

    pending_validations = (
        df["Validation End Date"]
        .isna()
        .sum()
    )

    unique_validators = (
        df["Validator"]
        .nunique()
    )

    overdue_validations = len(
        df[
            (df["Validation End Date"].isna())
            &
            (
                df["Validation Start Date"]
                <
                pd.Timestamp.today()
                - pd.Timedelta(days=7)
            )
        ]
    )

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric(
        "Total Validations",
        total_validations
    )

    col2.metric(
        "Completed",
        completed_validations
    )

    col3.metric(
        "Pending",
        pending_validations
    )

    col4.metric(
        "Validators",
        unique_validators
    )

    col5.metric(
        "Overdue",
        overdue_validations
    )

    st.divider()

    # -----------------------------
    # Environment Summary
    # -----------------------------

    st.subheader("🌎 Validations by Environment")

    env_summary = (
        df["Environment"]
        .value_counts()
        .reset_index()
    )

    env_summary.columns = [
        "Environment",
        "Count"
    ]

    st.bar_chart(
        env_summary.set_index("Environment")
    )

    # -----------------------------
    # Service Level Tier
    # -----------------------------

    st.subheader("🏆 Service Level Tier Distribution")

    tier_summary = (
        df["Service Level Tier"]
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

    # -----------------------------
    # Validator Summary
    # -----------------------------

    st.subheader("👤 Top Validators")

    validator_summary = (
        df["Validator"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    validator_summary.columns = [
        "Validator",
        "Validation Count"
    ]

    st.dataframe(
        validator_summary,
        use_container_width=True
    )

    # -----------------------------
    # CI Owner Summary
    # -----------------------------

    st.subheader("🏢 Top CI Owners")

    owner_summary = (
        df["CI Owner"]
        .value_counts()
        .head(10)
        .reset_index()
    )

    owner_summary.columns = [
        "CI Owner",
        "Validation Count"
    ]

    st.dataframe(
        owner_summary,
        use_container_width=True
    )

    # -----------------------------
    # Portfolio Summary
    # -----------------------------

    st.subheader("💼 Portfolio Managers")

    portfolio_summary = (
        df["Portfolio Manager"]
        .value_counts()
        .reset_index()
    )

    portfolio_summary.columns = [
        "Portfolio Manager",
        "Count"
    ]

    st.dataframe(
        portfolio_summary,
        use_container_width=True
    )

    # -----------------------------
    # Raw Data
    # -----------------------------

    st.subheader("📋 Validation Records")

    search = st.text_input(
        "Search Validation Number"
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

    st.dataframe(
        filtered_df,
        use_container_width=True,
        height=500
    )

    # -----------------------------
    # Download CSV
    # -----------------------------

    csv = filtered_df.to_csv(
        index=False
    )

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="validation_report.csv",
        mime="text/csv"
    )
