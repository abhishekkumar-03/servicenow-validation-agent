import streamlit as st
from notifications import send_email


def show_reminders(df):

    st.title("📧 Reminder Center")

    # Clean columns
    df.columns = df.columns.str.strip()

    # Pending validations
    pending_df = df[
        df["Validation End Date"].isna()
    ]

    st.metric(
        "Pending Reminders",
        len(pending_df)
    )

    st.dataframe(
        pending_df,
        use_container_width=True
    )

    st.divider()

    # Send All Reminders

    if st.button("📨 Send All Reminders"):

        success = 0

        for _, row in pending_df.iterrows():

            recipient = row.get(
                "CI Owner",
                ""
            )

            if not recipient:
                continue

            subject = (
                f"Validation Reminder - "
                f"{row['Number']}"
            )

            body = f"""
            <html>
            <body>

            <h3>Validation Reminder</h3>

            <p>
            Validation record requires attention.
            </p>

            <ul>
                <li>
                Number:
                {row['Number']}
                </li>

                <li>
                CI:
                {row['CI']}
                </li>

                <li>
                Validator:
                {row['Validator']}
                </li>

                <li>
                Environment:
                {row['Validation Environment']}
                </li>

                <li>
                Start Date:
                {row['Validation Start Date']}
                </li>
            </ul>

            </body>
            </html>
            """

            try:

                send_email(
                    recipient,
                    subject,
                    body
                )

                success += 1

            except Exception as e:

                st.error(
                    f"Failed for "
                    f"{row['Number']}: {e}"
                )

        st.success(
            f"✅ {success} reminder(s) sent"
        )

    st.divider()

    # Individual Reminder Buttons

    st.subheader(
        "Send Individual Reminder"
    )

    for _, row in pending_df.iterrows():

        col1, col2 = st.columns([5, 1])

        with col1:

            st.write(
                f"{row['Number']} | "
                f"{row['CI']} | "
                f"{row['Validator']}"
            )

        with col2:

            if st.button(
                "Send",
                key=f"send_{row['Number']}"
            ):

                try:

                    send_email(
                        row["CI Owner"],
                        "Validation Reminder",
                        f"""
                        Please review validation
                        {row['Number']}
                        """
                    )

                    st.success(
                        f"Reminder sent for "
                        f"{row['Number']}"
                    )

                except Exception as e:

                    st.error(str(e))
