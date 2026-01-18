import streamlit as st
from google import genai
import os

# --- APP CONFIG ---
st.set_page_config(page_title="GEO Audit Pro", layout="wide", page_icon="🚀")
st.title("🚀 Generative Engine Optimization (GEO) Audit")

# --- SECURE API KEY LOADING ---
# If running locally, Streamlit looks in .streamlit/secrets.toml
# If running on Streamlit Cloud, it looks in the dashboard "Secrets" section
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("Missing API Key! Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

# Initialize the Gemini Client
client = genai.Client(api_key=api_key)

# --- INPUT SECTION ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input("Your Company Name", placeholder="e.g. Acme SaaS")
    with col2:
        competitors = st.text_input("Competitors (comma separated)", placeholder="e.g. Comp1, Comp2, Comp3")

# --- AUDIT LOGIC ---
if st.button("Run GEO Audit", type="primary"):
    if not company_name:
        st.warning("Please enter a company name to begin.")
    else:
        with st.spinner(f"AI is auditing {company_name}..."):
            prompt = f"""
            Act as an expert in Generative Engine Optimization (GEO). 
            Perform a detailed audit for the brand '{company_name}'.
            Compare its AI-search presence against these competitors: {competitors}.
            
            Provide a report with:
            - **Brand Sentiment:** How AI models describe the brand.
            - **Citation Profile:** Where is the AI getting its info? (Websites, Social, News).
            - **GEO Score (1-100):** Based on AI visibility.
            - **The 'Gap' Analysis:** What are competitors mentioned for that this brand is missing?
            - **3 Immediate Actions:** Specific technical or content changes to rank higher in AI summaries.
            """
            
            try:
                # Using the latest Flash model for speed and efficiency
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=prompt
                )
                
                st.success("Audit Complete!")
                st.markdown("---")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- FOOTER ---
st.caption("Powered by Gemini 2.0 Flash • Built for GEO Professionals")
