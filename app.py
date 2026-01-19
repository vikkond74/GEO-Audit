import streamlit as st
from openai import OpenAI
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="GEO Intelligence Portal", layout="wide", page_icon="🤖")

# --- SECURE API KEY ---
try:
    api_key = st.secrets["PERPLEXITY_API_KEY"]
except KeyError:
    st.error("Setup Error: Please add 'PERPLEXITY_API_KEY' to your Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

# --- NAVIGATION ---
tabs = st.tabs(["📖 Education Hub", "🔬 GEO Audit Tool"])

# --- PAGE 1: EDUCATION HUB (Same as before) ---
with tabs[0]:
    st.title("What is Generative Engine Optimization (GEO)?")
    st.markdown("### The Shift: From 'Search' to 'Answer' Engines")
    st.info("""
    **2026 Market Intelligence:**
    * **Share of Model (SoM):** The percentage of time an LLM recommends your brand vs. competitors for a specific category prompt.
    * **The Search Volume Drop:** Traditional search volume is down **25%** as of 2026.
    """)
    st.divider()
    # (Pillars remain as in your original code)

# --- PAGE 2: AUDIT TOOL ---
with tabs[1]:
    st.title("🔬 Brand GEO Audit & Competitive Benchmarking")
    st.markdown("Analyze your brand's visibility compared to its top rival.")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        company_name = st.text_input("Brand Name", placeholder="e.g. Patagonia")
    with col2:
        competitor_name = st.text_input("Main Competitor", placeholder="e.g. North Face")
    with col3:
        region = st.selectbox("Market Focus", ["Global", "Europe", "Asia-Pacific", "Americas", "Middle East & Africa"])

    if st.button("Run Competitive GEO Audit", type="primary"):
        if not company_name or not competitor_name:
            st.warning("Please enter both a Brand and a Competitor name.")
        else:
            with st.spinner(f"Analyzing {company_name} vs {competitor_name}..."):
                # Updated prompt to force competitive scoring and "The Why" for low scores
                prompt = f"""
                Conduct a 2026 GEO (Generative Engine Optimization) Audit for '{company_name}' vs '{competitor_name}' in the '{region}' market.
                
                Provide the following sections:
                1. A 'GEO Scorecard' Table with scores (1-100) for both brands across: Share of Model, Citation Frequency, E-E-A-T Signal Strength, and Technical Schema.
                2. For any area where '{company_name}' scores lower than '{competitor_name}', provide a specific 'Why it's Low' diagnostic (e.g., lack of Reddit mentions, missing JSON-LD, or outdated news citations).
                3. A custom Markdown block for an 'llms.txt' file for '{company_name}'.
                """
                
                try:
                    response = client.chat.completions.create(
                        model="sonar-pro",
                        messages=[
                            {"role": "system", "content": "You are a Senior GEO Strategist. You provide data-driven competitive audits in clean Markdown with tables."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    
                    # Layout the results
                    st.success("Audit Complete")
                    
                    # Display the AI's full analysis
                    st.markdown(response.choices[0].message.content)
                    
                except Exception as e:
                    st.error(f"Audit failed: {e}")

st.divider()
st.caption("Data source: Perplexity Sonar-Pro (Real-time 2026 Web Index)")
