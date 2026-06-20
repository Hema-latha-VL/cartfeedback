# Customer Feedback Intelligence System

## Overview

The Customer Feedback Intelligence System is a Streamlit-based web application that analyzes customer feedback collected from support tickets, app store reviews, and survey comments.

The system cleans raw feedback data, performs sentiment analysis, categorizes complaints into predefined categories, generates summaries, and provides interactive visual reports for business insights.

---

## Problem Statement

Organizations receive large volumes of customer feedback every day. Manually reviewing thousands of comments is time-consuming and inefficient.

This application automates the process by:

- Cleaning raw feedback data
- Identifying customer sentiment
- Categorizing complaints
- Generating business reports
- Providing downloadable enriched data

---

## Features

### Data Cleaning
- Removes empty feedback records
- Removes duplicate feedback entries
- Handles missing values
- Standardizes timestamp formats
- Filters meaningless feedback such as:
  - "...."
  - "aaaa"
  - "???"
  - "test"

### Sentiment Analysis
Classifies feedback into:
- Positive
- Negative
- Neutral

### Complaint Categorization

Feedback is categorized into:

- Billing
- App Bug
- Delivery
- Staff/Support
- Other

### Dashboard Analytics

Displays:

- Total Records
- Clean Records
- Removed Records
- Top Complaint Categories
- Sentiment Distribution
- Category-wise Analysis
- Representative Customer Feedback Examples

### Data Export

Users can download the processed and enriched dataset as a CSV file.

---

## Technology Stack

- Python
- Pandas
- Streamlit
- Plotly

---

## Project Workflow

```text
Raw CSV Dataset
        ↓
Data Loading (Pandas)
        ↓
Data Cleaning
        ↓
Timestamp Standardization
        ↓
Sentiment Analysis
        ↓
Complaint Categorization
        ↓
Summary Generation
        ↓
Dashboard Visualization
        ↓
CSV Export
```

---

## Input Dataset

The dataset contains the following fields:

| Column | Description |
|----------|------------|
| id | Unique Feedback ID |
| timestamp | Feedback Timestamp |
| source | Feedback Source |
| rating | Customer Rating |
| feedback_text | Customer Feedback Message |

---

## Output Dataset

The enriched dataset contains:

| Column | Description |
|----------|------------|
| sentiment | Customer Sentiment |
| category | Complaint Category |
| summary | Short Feedback Summary |

---

## How to Run

### Clone Repository

```bash
git clone <repository-url>
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run Application

```bash
streamlit run app.py
```

---

## Sample Reports Generated

- Top 5 Complaint Categories
- Overall Sentiment Breakdown
- Representative Customer Feedback Messages
- Interactive Charts and Visualizations

---

## Future Enhancements

- LLM-based Categorization
- Advanced NLP Sentiment Analysis
- Trend Analysis using Timestamps
- Database Integration
- Cloud Deployment
- Real-time Feedback Processing

---

## AI Usage

AI tools were used to:

- Understand project requirements
- Generate initial code structure
- Improve categorization logic
- Review and validate implementation

All generated code and outputs were manually reviewed, modified, and tested before final submission.

---

