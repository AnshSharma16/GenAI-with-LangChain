import streamlit as st
import pandas as pd
from datetime import datetime
from langchain_chain import process_complaint
from mongo_db import save_complaint, get_all_complaints, get_complaints_by_category

st.set_page_config(page_title="Smart Complaint Register", page_icon="📝", layout="wide")

def main():
    st.title("🎯 Smart Complaint Register")
    st.markdown("AI-powered complaint classification and management system")
    
    # Sidebar navigation
    page = st.sidebar.selectbox("Navigate", ["Submit Complaint", "View Complaints", "Analytics"])
    
    if page == "Submit Complaint":
        submit_complaint_page()
    elif page == "View Complaints":
        view_complaints_page()
    else:
        analytics_page()

def submit_complaint_page():
    st.header("📝 Submit New Complaint")
    
    with st.form("complaint_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Your Name*", placeholder="Enter your full name")
            email = st.text_input("Email*", placeholder="your.email@example.com")
            phone = st.text_input("Phone", placeholder="+91 XXXXX XXXXX")
        
        with col2:
            department = st.selectbox("Department", 
                ["IT", "HR", "Finance", "Operations", "Customer Service", "Other"])
            priority = st.selectbox("Priority", ["Low", "Medium", "High", "Urgent"])
        
        complaint_text = st.text_area("Complaint Details*", 
            placeholder="Describe your complaint in detail...", height=150)
        
        submitted = st.form_submit_button("🚀 Submit Complaint", use_container_width=True)
        
        if submitted:
            if not all([name, email, complaint_text]):
                st.error("Please fill all required fields!")
                return
            
            with st.spinner("Processing complaint with AI..."):
                try:
                    # Process with Gemini AI
                    result = process_complaint(complaint_text)
                    
                    # Save to MongoDB
                    complaint_data = {
                        "name": name,
                        "email": email,
                        "phone": phone,
                        "department": department,
                        "priority": priority,
                        "complaint_text": complaint_text,
                        "category": result["category"],
                        "sentiment": result["sentiment"],
                        "summary": result["summary"],
                        "status": "Open",
                        "created_at": datetime.now()
                    }
                    
                    complaint_id = save_complaint(complaint_data)
                    
                    st.success(f"✅ Complaint submitted successfully!")
                    st.info(f"**Complaint ID:** {complaint_id}")
                    
                    # Display AI analysis
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Category", result["category"])
                    with col2:
                        st.metric("Sentiment", result["sentiment"])
                    with col3:
                        st.metric("Priority", priority)
                    
                    st.write("**AI Summary:**", result["summary"])
                    
                except Exception as e:
                    st.error(f"Error processing complaint: {str(e)}")

def view_complaints_page():
    st.header("📋 View Complaints")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        category_filter = st.selectbox("Filter by Category", 
            ["All", "Technical", "Service", "Billing", "Product", "General"])
    with col2:
        status_filter = st.selectbox("Filter by Status", 
            ["All", "Open", "In Progress", "Resolved", "Closed"])
    with col3:
        sentiment_filter = st.selectbox("Filter by Sentiment", 
            ["All", "Positive", "Neutral", "Negative"])
    
    # Fetch complaints
    complaints = get_all_complaints()
    if not complaints:
        st.info("No complaints found.")
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(complaints)
    df['created_at'] = pd.to_datetime(df['created_at']).dt.strftime('%Y-%m-%d %H:%M')
    
    # Apply filters
    if category_filter != "All":
        df = df[df['category'] == category_filter]
    if status_filter != "All":
        df = df[df['status'] == status_filter]
    if sentiment_filter != "All":
        df = df[df['sentiment'] == sentiment_filter]
    
    # Display complaints
    st.dataframe(df[['name', 'category', 'sentiment', 'priority', 'status', 'created_at']], 
                use_container_width=True)
    
    # Detailed view
    if not df.empty:
        selected_idx = st.selectbox("View Details", range(len(df)), 
            format_func=lambda x: f"{df.iloc[x]['name']} - {df.iloc[x]['category']}")
        
        selected_complaint = df.iloc[selected_idx]
        
        with st.expander("📄 Complaint Details", expanded=True):
            col1, col2 = st.columns(2)
            with col1:
                st.write("**Name:**", selected_complaint['name'])
                st.write("**Email:**", selected_complaint['email'])
                st.write("**Department:**", selected_complaint['department'])
                st.write("**Priority:**", selected_complaint['priority'])
            with col2:
                st.write("**Category:**", selected_complaint['category'])
                st.write("**Sentiment:**", selected_complaint['sentiment'])
                st.write("**Status:**", selected_complaint['status'])
                st.write("**Created:**", selected_complaint['created_at'])
            
            st.write("**Complaint:**")
            st.write(selected_complaint['complaint_text'])
            st.write("**AI Summary:**")
            st.write(selected_complaint['summary'])

def analytics_page():
    st.header("📊 Analytics Dashboard")
    
    complaints = get_all_complaints()
    if not complaints:
        st.info("No data available for analytics.")
        return
    
    df = pd.DataFrame(complaints)
    
    # Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Complaints", len(df))
    with col2:
        st.metric("Open Complaints", len(df[df['status'] == 'Open']))
    with col3:
        st.metric("Resolved", len(df[df['status'] == 'Resolved']))
    with col4:
        avg_sentiment = df['sentiment'].value_counts().index[0] if not df.empty else "N/A"
        st.metric("Top Sentiment", avg_sentiment)
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Complaints by Category")
        category_counts = df['category'].value_counts()
        st.bar_chart(category_counts)
    
    with col2:
        st.subheader("Sentiment Distribution")
        sentiment_counts = df['sentiment'].value_counts()
        st.bar_chart(sentiment_counts)
    
    # Recent complaints
    st.subheader("Recent Complaints")
    recent = df.nlargest(5, 'created_at')[['name', 'category', 'sentiment', 'priority']]
    st.table(recent)

if __name__ == "__main__":
    main()   