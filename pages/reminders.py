import streamlit as st
from servicenow_client import get_validations
from notifications import send_email


def show_reminders():
    st.title("Reminder Center")

    df = get_validations()

    failed_df = df[df["status"] == "Failed"]

    st.metric(
        "Pending Reminders",
        len(failed_df)
    )

    st.dataframe(
        failed_df,
        use_container_width=True
    )

    if st.button("Send All Reminders"):
        success = 0

        for _, row in failed_df.iterrows():
            subject = f"Validation Reminder - {row['validation_id']}"

            body = f"""
            <html>
            <body>
                <h3>Validation Reminder</h3>
                <p>Hello {row['assigned_to']},</p>
                <p>The following validation requires attention:</p>
                <ul>
                    <li>Number: {row['validation_id']}</li>
                    <li>CI: {row['ci']}</li>
                    <li>Validator: {row['validator']}</li>
                    <li>Validation Start Date: {row['validation_start']}</li>
                </ul>
                <p>Please review and update the validations.</p>
            </body>
            </html>
            """

            if send_email(row['email'], subject, body):
                success += 1

        st.success(f"{success} reminder emails sent.")

    for _, row in failed_df.iterrows():
        col1, col2 = st.columns([4, 1])

        with col1:
            st.write(row['validation_id'])

        with col2:
            if st.button('Send', key=f"send_{row['validation_id']}"):
                send_email(
                    row['email'],
                    'Validation Reminder',
                    'Please review validations.'
                )

                st.success(f"Sent to {row['assigned_to']}")
