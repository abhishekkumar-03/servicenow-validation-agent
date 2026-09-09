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

    # Clean column names
    df.columns = (
        df.columns.astype(str)
        .str.strip()
        .str.replace("\n", " ", regex=False)
    )

    # Locate columns safely
    number_col = get_column(df, "Number")
    environment_col = get_column(df, "Validation Environment")
    validator_col = get_column(df, "Validator")
    start_col = get_column(df, "Validation Start Date")
    end_col = get_column(df, "Validation End Date")
    ci_owner_col = get_column(df, "CI Owner")
    portfolio_col = get_column(df, "Portfolio Manager")
    tier_col = get_column(df, "Service Level Tier")

    # Date conversion
    if start_col:
        df[start_col] = pd.to_datetime(
            df[start_col],
            errors="coerce"
        )

    if end_col:
        df[end_col] = pd.to_datetime(
            df[end_col],
            errors="coerce"
        )

    # =============================
    # KPI Metrics
    # =============================

    total = len(df)

    completed = (
        df[end_col].notna().sum()
        if end_col else 0
    )

    pending = (
        df[end_col].isna().sum()
        if end_col else 0
    )

    validators = (
        df[validator_col].nunique()
        if validator_col else 0
    )

    overdue = 0

    if start_col and end_col:

        overdue = len(
            df[
                (df[end_col].isna())
                &
                (
                    df[start_col]
                    <
                    pd.Timestamp.today()
                    - pd.Timedelta(days=7)
                )
            ]
        )

    k1, k2, k3, k4, k5 = st.columns(5)

    k1.metric("Total", total)
    k2.metric("Completed", completed)
    k3.metric("Pending", pending)
    k4.metric("Validators", validators)
    k5.metric("Overdue", overdue)

    st.divider()

    # =============================
    # Validation Environment
    # =============================

    if environment_col:

        st.subheader("🌎 Validation Environment Distribution")

        env_summary = (
            df[environment_col]
            .fillna("Unknown")
            .value_counts()
            .reset_index()
        )

        env_summary.columns = [
            "Validation Environment",
            "Count"
        ]

        st.bar_chart(
            env_summary.set_index(
                "Validation Environment"
            )
        )

    # =============================
    # Service Level Tier
    # =============================

    if tier_col:

        st.subheader(
            "🏆 Service Level Tier Distribution"
        )

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

    # =============================
    # Top Validators
    # =============================

    if validator_col:

        st.subheader("👤 Top Validators")

        validator_summary = (
            df[validator_col]
            .fillna("Unknown")
            .value_counts()
            .head(10)
            .reset_index()
        )

        validator_summary.columns = [
            "Validator",
            "Count"
        ]

        st.dataframe(
            validator_summary,
            use_container_width=True
        )

    # =============================
    # CI Owners
    # =============================

    if ci_owner_col:

        st.subheader("🏢 Top CI Owners")

        owner_summary = (
            df[ci_owner_col]
            .fillna("Unknown")
            .value_counts()
            .head(10)
            .reset_index()
        )

        owner_summary.columns = [
            "CI Owner",
            "Count"
        ]

        st.dataframe(
            owner_summary,
            use_container_width=True
        )

    # =============================
    # Portfolio Managers
    # =============================

    if portfolio_col:

        st.subheader("💼 Portfolio Managers")

        portfolio_summary = (
            df[portfolio_col]
            .fillna("Unknown")
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

    # =============================
    # Validation Records
    # =============================

    st.subheader("📋 Validation Records")

    filtered_df = df.copy()

    search = st.text_input(
        "Search Validation Number"
    )

    if search and number_col:

        filtered_df = filtered_df[
            filtered_df[number_col]
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

    # =============================
    # Download CSV
    # =============================

    csv = filtered_df.to_csv(
        index=False
    )

    st.download_button(
        label="⬇ Download CSV",
        data=csv,
        file_name="validation_report.csv",
        mime="text/csv"
    )
