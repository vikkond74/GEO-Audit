import streamlit as st
from openai import OpenAI

# --- APP CONFIG ---
st.set_page_config(page_title="Global GEO Intelligence", layout="centered", page_icon="🌍")
st.title("🌍 Global GEO Intelligence Dashboard")
st.markdown("Analyze your brand's standing in the **global** AI ecosystem.")

# --- SECURE API KEY ---
try:
    api_key = st.secrets["PERPLEXITY_API_KEY"]
except KeyError:
    st.error("Setup Error: Please add 'PERPLEXITY_API_KEY' to your Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

# --- EXECUTIVE INPUT ---
company_name = st.text_input("What is your Company Name?", placeholder="e.g. Siemens")

# New: Regional focus to help the AI narrow down or expand its search
region = st.selectbox("Primary Market Focus", ["Global (All Regions)", "Europe", "Asia-Pacific", "Americas", "Middle East & Africa"])

if st.button("Run Global Audit", type="primary"):
    if not company_name:
        st.warning("Please enter a company name.")
    else:
        with st.spinner(f"Scanning global market data for {company_name}..."):
            
            # This prompt is re-engineered to ignore the US-default bias
            prompt = f"""
            Perform a GLOBAL GEO (Generative Engine Optimization) audit for '{company_name}'.
            Target Market: {region}
            
            STRICT RULES:
            - Do not default to US-only competitors unless the brand is primarily US-based.
            - Identify the top 3 rivals specifically within the {region} market.
            - Search for citations in local and international business news (e.g., Financial Times, Nikkei, Reuters, BBC).
            
            Provide the report in simple business terms:
            1. The Global Recommendation Race: A table (0-100) showing how likely AI is to suggest you vs your {region} rivals.
            2. Regional Reputation: How does the AI describe your brand's presence in international markets?
            3. The Global Opportunity Gap: Topics or regional trends your competitors 'own' that you should claim.
            4.
