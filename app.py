import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="Customer Feedback Intelligence System",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown(
    """
    <style>
        :root {
            --bg: #f5f7fb;
            --surface: rgba(255, 255, 255, 0.86);
            --surface-strong: #ffffff;
            --border: rgba(15, 23, 42, 0.10);
            --text: #102033;
            --muted: #5c6b7d;
            --accent: #0f766e;
            --accent-strong: #115e59;
            --accent-soft: #dff5f3;
            --shadow: 0 18px 45px rgba(15, 23, 42, 0.08);
        }

        .stApp {
            background:
                radial-gradient(circle at top left, rgba(15, 118, 110, 0.10), transparent 30%),
                radial-gradient(circle at top right, rgba(59, 130, 246, 0.08), transparent 28%),
                linear-gradient(180deg, #f8fbff 0%, var(--bg) 100%);
            color: var(--text);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2.5rem;
            max-width: 1320px;
        }

        h1, h2, h3, h4, h5, h6 {
            color: var(--text);
            letter-spacing: -0.02em;
        }

        h1 {
            font-size: 2.4rem;
            font-weight: 800;
            margin-bottom: 0.25rem;
        }

        .stCaption {
            color: var(--muted);
        }

        .stMarkdown p, .stMarkdown li, .stMarkdown span {
            color: var(--text);
            line-height: 1.65;
        }

        div[data-testid="stMarkdownContainer"] strong {
            color: var(--text);
        }

        div[data-testid="stMarkdownContainer"] a {
            color: var(--accent-strong);
            text-decoration: none;
        }

        div[data-testid="stMarkdownContainer"] a:hover {
            text-decoration: underline;
        }

        .hero-card {
            background: linear-gradient(135deg, rgba(15, 118, 110, 0.95), rgba(15, 23, 42, 0.96));
            color: #fff;
            border-radius: 22px;
            padding: 1.25rem 1.4rem;
            margin: 0.4rem 0 1.25rem 0;
            box-shadow: var(--shadow);
            border: 1px solid rgba(255, 255, 255, 0.12);
        }

        .hero-card h2 {
            margin: 0;
            font-size: 1.15rem;
            color: #fff;
        }

        .hero-card p {
            margin: 0.45rem 0 0;
            color: rgba(255, 255, 255, 0.86);
            line-height: 1.6;
        }

        .stMetric {
            background: var(--surface-strong);
            border: 1px solid var(--border);
            border-radius: 18px;
            padding: 1rem 1rem 0.8rem;
            box-shadow: var(--shadow);
        }

        .stMetric label {
            color: var(--muted) !important;
            font-size: 0.88rem;
        }

        .stMetric [data-testid="stMetricValue"] {
            color: var(--text);
            font-weight: 800;
        }

        .stDataFrame, .stPlotlyChart {
            background: var(--surface-strong);
            border-radius: 18px;
            padding: 0.5rem;
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
        }

        div[data-testid="stDataFrame"] {
            border-radius: 18px;
            overflow: hidden;
        }

        div[data-testid="stDataFrame"] table {
            border-collapse: separate;
            border-spacing: 0;
        }

        div[data-testid="stDataFrame"] thead tr th {
            background: linear-gradient(135deg, rgba(15, 118, 110, 0.12), rgba(17, 94, 89, 0.08));
            color: var(--text);
            font-weight: 700;
        }

        div[data-testid="stDataFrame"] tbody tr:nth-child(odd) td {
            background: rgba(248, 250, 252, 0.85);
        }

        div[data-testid="stDataFrame"] tbody tr:hover td {
            background: rgba(223, 245, 243, 0.85);
        }

        .section-card {
            background: rgba(255, 255, 255, 0.88);
            border: 1px solid var(--border);
            border-radius: 20px;
            padding: 1rem 1rem 0.25rem;
            box-shadow: var(--shadow);
            margin-bottom: 1rem;
        }

        .section-card .stSubheader {
            margin-bottom: 0.25rem;
        }

        div[data-testid="stFileUploader"] {
            background: var(--surface-strong);
            border: 1px dashed rgba(15, 118, 110, 0.35);
            border-radius: 18px;
            padding: 0.75rem 1rem;
            box-shadow: var(--shadow);
        }

        div[data-testid="stFileUploader"] section {
            background: rgba(15, 118, 110, 0.04);
            border-radius: 12px;
        }

        div[data-testid="stFileUploader"] button,
        div[data-testid="stFileUploader"] button span,
        div[data-testid="stFileUploader"] button p {
            background: linear-gradient(135deg, var(--accent), var(--accent-strong)) !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            border: none !important;
        }

        div[data-testid="stFileUploader"] button:hover {
            background: linear-gradient(135deg, #0e8a81, #0b4f4b) !important;
            color: #ffffff !important;
        }

        .stAlert {
            border-radius: 16px;
            border: 1px solid var(--border);
            box-shadow: var(--shadow);
        }

        .stButton > button {
            background: linear-gradient(135deg, var(--accent), var(--accent-strong));
            color: #fff;
            border: none;
            border-radius: 12px;
            padding: 0.55rem 1rem;
            font-weight: 700;
            box-shadow: 0 10px 20px rgba(15, 118, 110, 0.18);
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #0e8a81, #0b4f4b);
            color: #fff;
        }

        div[data-testid="stDownloadButton"] button,
        div[data-testid="stDownloadButton"] button p,
        div[data-testid="stDownloadButton"] a {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            text-decoration: none !important;
        }

        div[data-testid="stDownloadButton"] button:hover {
            background: linear-gradient(135deg, #0e8a81, #0b4f4b) !important;
            color: #ffffff !important;
        }

        hr {
            border-color: rgba(15, 23, 42, 0.10);
        }

        div[data-testid="stMarkdownContainer"] h3 {
            margin-top: 0.5rem;
            margin-bottom: 0.6rem;
        }

        .stInfo {
            border-radius: 16px;
            border: 1px solid rgba(15, 118, 110, 0.18);
            background: linear-gradient(135deg, rgba(223, 245, 243, 0.95), rgba(255, 255, 255, 0.96));
            color: var(--text);
            box-shadow: var(--shadow);
        }
    </style>
    """,
    unsafe_allow_html=True
)


def report_table(dataframe, *, hide_index=True):
    styled = (
        dataframe.style
        .set_table_styles([
            {"selector": "table", "props": [("border-collapse", "separate"), ("border-spacing", "0"), ("width", "100%"), ("background-color", "#ffffff"), ("border", "1px solid rgba(15, 23, 42, 0.10)"), ("border-radius", "16px"), ("overflow", "hidden")]},
            {"selector": "th", "props": [("background-color", "#e8f3f1"), ("color", "#102033"), ("font-weight", "700"), ("text-align", "left"), ("padding", "0.8rem 0.9rem"), ("border-bottom", "1px solid rgba(15, 23, 42, 0.10)")]},
            {"selector": "td", "props": [("color", "#102033"), ("padding", "0.78rem 0.9rem"), ("border-bottom", "1px solid rgba(15, 23, 42, 0.06)"), ("vertical-align", "top"), ("white-space", "normal")]},
            {"selector": "tbody tr:nth-child(even)", "props": [("background-color", "#f8fafc")]},
            {"selector": "tbody tr:hover", "props": [("background-color", "#dff5f3")]},
        ])
        .set_properties(**{"background-color": "#ffffff", "color": "#102033"})
        .format(na_rep="-")
    )

    if hide_index:
        styled = styled.hide(axis="index")

    return styled


def render_table_section(title, dataframe, *, file_name, key_prefix, hide_index=True, include_index_in_download=False):
    st.subheader(title)

    preview_limit = len(dataframe)
    if len(dataframe) > 5:
        preview_options = sorted({5, min(10, len(dataframe)), min(20, len(dataframe)), len(dataframe)})
        preview_limit = st.selectbox(
            f"Zoom preview for {title}",
            preview_options,
            index=0,
            key=f"{key_prefix}_zoom"
        )

    st.table(
        report_table(
            dataframe.head(preview_limit),
            hide_index=hide_index
        )
    )

    if len(dataframe) > preview_limit:
        st.caption(f"Showing {preview_limit} of {len(dataframe)} rows. Use the zoom selector to preview more.")

    st.download_button(
        f"Download {title}",
        dataframe.to_csv(index=include_index_in_download),
        file_name=file_name,
        mime="text/csv",
        type="primary",
        key=f"{key_prefix}_download"
    )

st.title("Customer Feedback Intelligence System")
st.markdown(
    """
    <div class="hero-card">
        <h2>Upload customer feedback and turn it into a clear business summary.</h2>
        <p>
            The app cleans raw feedback, labels each comment by sentiment and complaint type,
            and presents the results in simple charts, tables, and short summaries.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

uploaded_file = st.file_uploader(
    "Upload Customer Feedback CSV",
    type=["csv"]
)

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    render_table_section(
        "Dataset Preview",
        df.head(),
        file_name="dataset_preview.csv",
        key_prefix="dataset_preview",
        hide_index=True
    )

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

    render_table_section(
        "Processed Data",
        df[
            [
                "feedback_text",
                "sentiment",
                "category",
                "summary"
            ]
        ],
        file_name="processed_feedback.csv",
        key_prefix="processed_data",
        hide_index=True
    )

    complaint_table = (
        df["category"]
        .value_counts()
        .reset_index()
        .rename(columns={"index": "Complaint Category", "category": "Count"})
    )

    render_table_section(
        "Top Complaint Categories",
        complaint_table,
        file_name="top_complaint_categories.csv",
        key_prefix="complaint_categories",
        hide_index=True
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

    sentiment_counts = df["sentiment"].value_counts()

    sentiment_df = pd.DataFrame({
        "Count": sentiment_counts,
        "Percentage": (
            sentiment_counts / len(df) * 100
        ).round(2)
    })

    render_table_section(
        "Overall Sentiment Breakdown",
        sentiment_df,
        file_name="sentiment_breakdown.csv",
        key_prefix="sentiment_breakdown",
        hide_index=False,
        include_index_in_download=True
    )

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

    render_table_section(
        "Category-wise Sentiment",
        pivot,
        file_name="category_wise_sentiment.csv",
        key_prefix="category_sentiment",
        hide_index=False,
        include_index_in_download=True
    )

    negative_df = df[df["sentiment"] == "Negative"]

    render_table_section(
        "Top Negative Complaints",
        negative_df[
            ["feedback_text", "category"]
        ].head(20),
        file_name="top_negative_complaints.csv",
        key_prefix="negative_complaints",
        hide_index=True
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

    fig.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#102033"),
        legend=dict(bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=20, r=20, t=50, b=20)
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

    fig2.update_layout(
        template="plotly_white",
        paper_bgcolor="white",
        plot_bgcolor="white",
        font=dict(color="#102033"),
        margin=dict(l=20, r=20, t=50, b=40)
    )

    fig2.update_xaxes(title_text="Category", gridcolor="rgba(15, 23, 42, 0.08)")
    fig2.update_yaxes(title_text="Count", gridcolor="rgba(15, 23, 42, 0.08)")

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
        mime="text/csv",
        type="primary"
    )

    st.markdown("---")
    st.write("QuickCart Customer Feedback Intelligence System")
else:
    st.info("Upload a CSV file to begin processing customer feedback.")