import streamlit as st
from google import genai
from google.api_core import exceptions
import time

# --- APP CONFIG ---
st.set_page_config(page_title="GEO Audit Pro", layout="wide", page_icon="🚀")
st.title("🚀 GEO Audit Pro (Resilient Edition)")

# --- SECURE API KEY LOADING ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("Missing API Key! Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

# Initialize the Gemini Client
client = genai.Client(api_key=api_key)

# --- HELPER FUNCTION: RETRY LOGIC ---
def generate_with_retry(prompt, model_name="gemini-1.5-flash"):
    """Attempts to call the API with a simple backoff if rate limited."""
    max_retries = 3
    for i in range(max_retries):
        try:
            # Using the lighter 1.5 Flash model
            return client.models.generate_content(
                model=model_name, 
                contents=prompt
            )
        except Exception as e:
            # Check for the 429 Error
            if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                if i < max_retries - 1:
                    wait_time = (i + 1) * 3  # Waits 3s, then 6s
                    st.warning(f"AI is busy (Rate Limit). Retrying in {wait_time}s...")
                    time.sleep(wait_time)
                else:
                    st.error("Daily quota reached. Please try again tomorrow or upgrade to a paid API key.")
                    return None
            else:
                st.error(f"An unexpected error occurred: {e}")
                return None

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
        st.warning("Please enter a company name.")
    else:
        with st.spinner(f"AI is analyzing {company_name} (using 1.5 Flash)..."):
            prompt = f"""
            Act as a GEO (Generative Engine Optimization) expert.
            Audit: '{company_name}'.
            Competitors: {competitors}.
            
            1. Summarize the brand's visibility in AI search.
            2. Identify 3 sources (websites/platforms) where the brand is strong.
            3. Rank the brand against competitors {competitors} for 'AI authority'.
            4. Suggest 3 content updates to increase the chance of AI citations.
            """
            
            response = generate_with_retry(prompt)
            
            if response:
                st.success("Audit Complete!")
                st.markdown("---")
                st.markdown(response.text)
