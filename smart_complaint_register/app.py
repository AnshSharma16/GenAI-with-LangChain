import streamlit as st
from langchain_chain import classify_complaint
from mongo_db import save_complaint, get_all_complaints

st.set_page_config(page_title="Smart Complaint Register", layout="centered")

st.title("🛠️ Smart Complaint Register")
st.write("Submit your complaint. AI will classify it and store it securely.")

complaint_text = st.text_area("✍️ Enter your complaint here:")

if st.button("📨 Submit Complaint"):
    if complaint_text.strip():
        category = classify_complaint(complaint_text)
        save_complaint(complaint_text, category)
        st.success(f"✅ Complaint categorized as: **{category}** and saved successfully.")
    else:
        st.warning("Please enter a valid complaint.")

st.markdown("---")
st.subheader("📋 Past Complaints")

complaints = get_all_complaints()
for c in complaints:
    st.markdown(f"""
    - 🕒 `{c['timestamp'].strftime('%Y-%m-%d %H:%M')}`  
    - 🗂️ **{c['category']}**  
    - 💬 {c['complaint']}
    """)
