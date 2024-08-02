import streamlit as st
from textblob import TextBlob
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Function to analyze sentiment
def analyze_sentiment(text):
    if isinstance(text, float):
        # Convert float to string if necessary
        text = str(text)
    elif not isinstance(text, str):
        # Handle other data types gracefully
        return "Unknown", None
    
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    if sentiment > 0:
        return "Positive", sentiment
    elif sentiment < 0:
        return "Negative", sentiment
    else:
        return "Neutral", sentiment

# Streamlit app
st.title("Sentiment Analysis Web App")

# Sidebar for user input
st.sidebar.header("Input Text")
user_input = st.sidebar.text_area("Enter text to analyze", "")

# Sentiment analysis for single input
if user_input:
    sentiment, polarity = analyze_sentiment(user_input)
    st.write(f"Sentiment: {sentiment}")
    st.write(f"Polarity: {polarity:.2f}")  # Limiting to 2 decimal places for clarity

# Interactive Dashboard for batch analysis
st.sidebar.header("Upload CSV for Batch Analysis")
uploaded_file = st.sidebar.file_uploader("Choose a CSV file", type="csv")

if uploaded_file:
    try:
        data = pd.read_csv(uploaded_file)
        st.write("File uploaded successfully. Please select the column containing the text to analyze.")
        
        # Allow user to select the text column
        columns = data.columns.tolist()
        text_column = st.sidebar.selectbox("Select the column containing the text", columns)
        
        if text_column:
            data['Sentiment'], data['Polarity'] = zip(*data[text_column].apply(analyze_sentiment))
            st.write(data)
            
            # Visualization using Plotly
            st.subheader("Sentiment Analysis Dashboard")
            
            # Bar chart with Plotly
            fig = px.bar(data, x='Sentiment', title='Sentiment Distribution', labels={'count':'Count'})
            st.plotly_chart(fig)
            
            # 3D Scatter Plot with Plotly
            fig_3d = px.scatter_3d(data, x='Sentiment', y='Polarity', z=data.index, color='Sentiment',
                                   title='3D Scatter Plot of Sentiment Analysis')
            st.plotly_chart(fig_3d)
            
            # Pie chart with Plotly
            fig_pie = px.pie(data, names='Sentiment', title='Sentiment Distribution')
            st.plotly_chart(fig_pie)
            
        else:
            st.write("Please select a column to analyze.")
    except Exception as e:
        st.error(f"Error reading file: {e}")

# Real-time monitoring and alerts (simplified example)
st.sidebar.header("Real-time Monitoring")
monitoring_text = st.sidebar.text_area("Enter text for real-time monitoring", "")
if monitoring_text:
    sentiment, polarity = analyze_sentiment(monitoring_text)
    st.write(f"Real-time Sentiment: {sentiment}")
    st.write(f"Real-time Polarity: {polarity:.2f}")
    if sentiment == "Negative":
        st.warning("Alert: Negative sentiment detected!")

st.sidebar.header("About")
st.sidebar.write("""
This is a simple sentiment analysis web app using Streamlit and TextBlob.
You can enter text to analyze its sentiment, upload a CSV file for batch analysis, and monitor real-time sentiment.
""")
