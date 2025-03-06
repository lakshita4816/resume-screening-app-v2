import streamlit as st
import spacy
from pdfminer.high_level import extract_text
import docx
import re
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob

# Download necessary NLP data
nltk.download('stopwords')

# Load NLP model
nlp = spacy.load("en_core_web_sm")

# Function to extract text from PDF
def extract_text_from_pdf(pdf_file):
    text = extract_text(pdf_file)
    return text

# Function to extract text from DOCX
def extract_text_from_docx(docx_file):
    doc = docx.Document(docx_file)
    return "\n".join([para.text for para in doc.paragraphs])

# Function to extract email, phone, and name
def extract_contact_info(text):
    email_pattern = r'[\w\.-]+@[\w\.-]+\.\w+'
    phone_pattern = r'\+?\d[\d -]{8,12}\d'
    
    emails = re.findall(email_pattern, text)
    phones = re.findall(phone_pattern, text)
    
    # Extract name using NLP
    doc = nlp(text)
    names = [ent.text for ent in doc.ents if ent.label_ == "PERSON"]
    
    return names, emails, phones

# Function to extract skills
def extract_skills(text):
    skills = ["Python", "Machine Learning", "Deep Learning", "Data Science", "SQL", "NLP", "Java", "C++", "TensorFlow", "Pandas", "NumPy", "Keras"]
    found_skills = [skill for skill in skills if skill.lower() in text.lower()]
    return list(set(found_skills))

# Sentiment analysis for resume
def analyze_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Streamlit UI
st.title("📄 Resume Screening App")
st.write("Upload a resume (PDF or DOCX) to extract key details.")

uploaded_file = st.file_uploader("Upload Resume", type=["pdf", "docx"])

if uploaded_file:
    file_extension = uploaded_file.name.split(".")[-1]

    if file_extension == "pdf":
        resume_text = extract_text_from_pdf(uploaded_file)
    elif file_extension == "docx":
        resume_text = extract_text_from_docx(uploaded_file)
    
    st.subheader("📜 Extracted Resume Text:")
    st.text(resume_text[:500])  # Display first 500 characters

    # Extract and display details
    names, emails, phones = extract_contact_info(resume_text)
    skills = extract_skills(resume_text)
    sentiment_score = analyze_sentiment(resume_text)

    st.subheader("🔍 Extracted Information:")
    st.write(f"👤 **Name(s):** {', '.join(names) if names else 'Not Found'}")
    st.write(f"📧 **Email(s):** {', '.join(emails) if emails else 'Not Found'}")
    st.write(f"📞 **Phone Number(s):** {', '.join(phones) if phones else 'Not Found'}")
    st.write(f"💡 **Skills Detected:** {', '.join(skills) if skills else 'Not Found'}")

    # Sentiment Analysis
    st.subheader("📊 Sentiment Analysis:")
    if sentiment_score > 0:
        st.success(f"Positive Sentiment: {sentiment_score:.2f}")
    elif sentiment_score < 0:
        st.error(f"Negative Sentiment: {sentiment_score:.2f}")
    else:
        st.warning(f"Neutral Sentiment: {sentiment_score:.2f}")

st.write("✨ **Built with Streamlit, Spacy, and NLP**")
