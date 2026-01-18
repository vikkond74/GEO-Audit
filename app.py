import streamlit as st
from google import genai
import os

# --- APP CONFIG ---
st.set_page_config(page_title="GEO Audit Pro", layout="wide")
st.title("🚀 Generative Engine Optimization (GEO) Audit")

# --- SIDEBAR: API KEY ---
with st.sidebar:
    api_key = st.text_input("Enter Gemini API Key", type="password")
    st.info("Get your key at [Google AI Studio](https://aistudio.google.com/)")

# --- INPUT SECTION ---
col1, col2 = st.columns(2)
with col1:
    company_name = st.text_input("Your Company Name", placeholder="e.g. Acme SaaS")
with col2:
    competitors = st.text_input("Competitors (comma separated)", placeholder="e.g. Comp1, Comp2, Comp3")

# --- AUDIT LOGIC ---
if st.button("Run GEO Audit"):
    if not api_key or not company_name:
        st.error("Please provide both an API key and a Company Name.")
    else:
        client = genai.Client(api_key=api_key)
        
        with st.spinner(f"Analyzing {company_name} presence..."):
            # Constructing the GEO-specific prompt
            prompt = f"""
            Perform a Generative Engine Optimization (GEO) audit for '{company_name}'.
            Compare it against these competitors: {competitors}.
            
            Provide the following in Markdown format:
            1. **Brand Sentiment & Visibility:** How does a generative engine currently perceive this brand?
            2. **GEO Metrics:** Estimate Visibility Rate and Citation Strength.
            3. **Actionable Feedback:** 5 specific ways to improve LLM 'citation-worthiness' (e.g., schema, FAQ, statistics).
            4. **Competitive Ranking:** Rank {company_name} against the competitors in terms of AI search dominance.
            """
            
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash", 
                    contents=prompt
                )
                
                # --- DISPLAY RESULTS ---
                st.markdown("---")
                st.subheader(f"GEO Audit Results for {company_name}")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"Error: {e}")
