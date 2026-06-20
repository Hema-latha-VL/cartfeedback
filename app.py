import streamlit as st
import pandas as pd
import re

st.title("Customer Feedback Intelligence System")

uploaded_file = st.file_uploader(
    "Upload Customer Feedback CSV",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.write("Dataset Preview")
    st.dataframe(df.head())

    st.metric("Total Feedback Records", len(df))

    st.subheader("Data Cleaning")

    initial_rows = len(df)

    def is_meaningful(text):
        text = str(text).strip().lower()
        
        if len(text) < 5:
            return False
        
        if re.match(r"^[.?!\s]+$", text):
            return False
        
        if re.match(r"^([a-z])\1{4,}$", text):
            return False
        
        letter_count = len(re.findall(r"[a-z]", text))
        
        if letter_count / len(text) < 0.6:
            return False
        
        if len(set(re.findall(r"[a-z]", text))) < 2:
            return False
        
        return True

    df = df[df["feedback_text"].apply(is_meaningful)]
    df = df.dropna(subset=["feedback_text"])
    df = df[df["feedback_text"].str.strip() != ""]
    duplicates_removed = len(df) - len(df.drop_duplicates(subset=["feedback_text"]))
    df = df.drop_duplicates(subset=["feedback_text"])

    final_rows = len(df)

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Original Rows",
        initial_rows
    )

    col2.metric(
        "Clean Rows",
        final_rows
    )

    col3.metric(
        "Removed Rows",
        initial_rows - final_rows
    )

    st.subheader("Data Quality Report")
    st.write(f"Missing Timestamps: {df['timestamp'].isna().sum() if 'timestamp' in df.columns else 'N/A'}")
    st.write(f"Missing Ratings: {df['rating'].isna().sum() if 'rating' in df.columns else 'N/A'}")
    st.write(f"Duplicate Feedback Removed: {duplicates_removed}")

    df["timestamp"] = pd.to_datetime(
        df["timestamp"],
        errors="coerce"
    )
    df["timestamp"] = df["timestamp"].dt.strftime("%Y-%m-%d")

    def generate_summary(text):
        return str(text).split(".")[0][:80]

    def get_sentiment(text):

        text = str(text).lower()

        sarcasm_words = [
            "oh great",
            "yeah right",
            "just love it",
            "so thrilled",
            "absolutely thrilled"
        ]

        positive_words = [
            "good","great","excellent","amazing","awesome",
            "fantastic","fast","love","helpful","thank",
            "resolved","perfect","happy","best","quick"
        ]

        negative_words = [
            "bad","poor","late","delay","issue","problem",
            "refund","crash","error","failed","worst",
            "slow","charged","bug","cancelled","broken"
        ]

        if any(word in text for word in sarcasm_words):
            return "Negative"

        pos = sum(word in text for word in positive_words)
        neg = sum(word in text for word in negative_words)

        if pos > neg:
            return "Positive"

        elif neg > pos:
            return "Negative"

        else:
            return "Neutral"

    df["sentiment"] = df["feedback_text"].apply(get_sentiment)

    billing_keywords = [
        "payment",
        "refund",
        "charged",
        "billing",
        "bill",
        "invoice",
        "fee",
        "coupon",
        "discount",
        "deducted",
        "amount",
        "money"
    ]

    appbug_keywords = [
        "bug",
        "crash",
        "error",
        "login",
        "loading",
        "stuck",
        "freeze",
        "frozen",
        "closed",
        "screen",
        "app not working",
        "unable to open",
        "failed"
    ]

    def get_category(text):

        text = str(text).lower()

        if any(word in text for word in billing_keywords):
            return "Billing"

        elif any(word in text for word in appbug_keywords):
            return "App Bug"

        elif any(word in text for word in [
            "delivery",
            "delivered",
            "rider",
            "driver",
            "late delivery",
            "late order",
            "cold food"
        ]):
            return "Delivery"

        elif any(word in text for word in ["support", "agent", "staff", "customer care"]):
            return "Staff/Support"

        else:
            return "Other"

    df["category"] = df["feedback_text"].apply(get_category)
    df["summary"] = df["feedback_text"].apply(generate_summary)

    st.subheader("Processed Data")
    st.dataframe(
        df[
            [
                "feedback_text",
                "sentiment",
                "category",
                "summary"
            ]
        ]
    )

    st.subheader("Top Complaint Categories")

    st.dataframe(
        df["category"]
        .value_counts()
        .reset_index()
    )

    st.subheader("Representative Examples")

    for cat in df["category"].unique():

        st.write(f"### {cat}")

        examples = (
            df[df["category"] == cat]
            ["feedback_text"]
            .head(3)
        )

        for ex in examples:
            st.write("•", ex)

    st.subheader("Overall Sentiment Breakdown")

    sentiment_counts = df["sentiment"].value_counts()

    sentiment_df = pd.DataFrame({
        "Count": sentiment_counts,
        "Percentage": (
            sentiment_counts / len(df) * 100
        ).round(2)
    })

    st.dataframe(sentiment_df)

    st.subheader("Project Summary")

    st.write(f"""
• Total feedback records analyzed: {initial_rows}

• Valid feedback after cleaning: {final_rows}

• Duplicate/invalid records removed: {initial_rows-final_rows}

• Most common complaint category:
{df['category'].value_counts().idxmax()}

• Dominant sentiment:
{df['sentiment'].value_counts().idxmax()}
""")

    pivot = pd.crosstab(
        df["category"],
        df["sentiment"]
    )

    st.subheader("Category-wise Sentiment")
    st.dataframe(pivot)

    negative_df = df[df["sentiment"] == "Negative"]

    st.subheader("Top Negative Complaints")
    st.dataframe(
        negative_df[
            ["feedback_text", "category"]
        ].head(20)
    )

    import plotly.express as px

    sentiment_counts = df["sentiment"].value_counts().reset_index()
    sentiment_counts.columns = ["sentiment", "count"]

    fig = px.pie(
        sentiment_counts,
        names="sentiment",
        values="count",
        title="Sentiment Distribution"
    )

    st.plotly_chart(fig)

    category_counts = df["category"].value_counts().reset_index()
    category_counts.columns = ["category", "count"]

    fig2 = px.bar(
        category_counts,
        x="category",
        y="count",
        title="Complaint Categories"
    )

    st.plotly_chart(fig2)

    top_category = df["category"].value_counts().idxmax()
    top_sentiment = df["sentiment"].value_counts().idxmax()

    st.subheader("Executive Summary")
    st.info(f"""
**Most complaints:** {top_category}

**Dominant sentiment:** {top_sentiment}

**Records processed:** {len(df)}
    """)

    csv = df.to_csv(index=False)

    st.download_button(
        "Download Enriched CSV",
        csv,
        file_name="cleaned_enriched_feedback.csv",
        mime="text/csv"
    )

    st.markdown("---")
    st.write("QuickCart Customer Feedback Intelligence System")
else:
    st.info("Upload a CSV file to begin processing customer feedback.")