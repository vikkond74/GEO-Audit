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
# Decoupling the Education Hub from the Audit Tool via a Sidebar
page = st.sidebar.radio("Navigation", ["📖 Education Hub", "🔬 Brand Audit Tool"])

# --- PAGE 1: EDUCATION HUB ---
if page == "📖 Education Hub":
    st.title("The 2026 GEO Whitepaper")
    st.markdown("### Why Generative Engine Optimization (GEO) is Non-Negotiable")
    
    st.info("""
    **The 2026 Landscape:**
    Search has shifted from 'finding links' to 'synthesizing answers.' According to **Gartner (2024)**, traditional search volume has seen a **25% decline** by 2026 as users pivot to AI Agents.
    """)

    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("🌐 Share of Model (SoM)")
        st.write("The new 'Share of Voice.' It measures how often an LLM mentions your brand when prompted for a category (e.g., 'Best eco-friendly running shoes').")
        
    with col2:
        st.subheader("📊 Fact-Density")
        st.write("AI favors content with high information gain. **BrightEdge (2025)** reports that cited content has **4x more unique data points** than uncited content.")
        
    with col3:
        st.subheader("🛡️ E-E-A-T & Citations")
        st.write("Models verify facts via 'Seed Sites' (Reddit, Wikipedia, Tier-1 News). If your brand isn't talked about there, the AI won't trust you.")

    

# --- PAGE 2: AUDIT TOOL ---
elif page == "🔬 Brand Audit Tool":
    st.title("🔬 Competitive Brand GEO Audit")
    st.markdown("Benchmark your brand's AI visibility against your primary competitor.")
    
    # --- INPUT SECTION ---
    with st.container():
        col_a, col_b = st.columns(2)
        with col_a:
            brand_name = st.text_input("Your Brand Name", placeholder="e.g. Patagonia")
            market = st.selectbox("Market Focus", ["Global", "North America", "Europe", "APAC"])
        with col_b:
            competitor_name = st.text_input("Main Competitor", placeholder="e.g. The North Face")
    
    if st.button("Run Comparative Audit", type="primary"):
        if not brand_name or not competitor_name:
            st.warning("Please enter both your brand and a competitor to run the analysis.")
        else:
            with st.spinner(f"Analyzing {brand_name} vs {competitor_name} in the {market} market..."):
                
                # Enhanced Prompt for Scoring and Diagnostics
                prompt = f"""
                Act as a Senior GEO Strategist in 2026. Perform a competitive audit for '{brand_name}' vs '{competitor_name}' in '{market}'.
                
                REQUIRED SECTIONS:
                1. **GEO Scorecard Table**: Compare both brands (Score 1-100) on:
                   - Share of Model (SoM)
                   - Citation Frequency
                   - Technical Schema Accuracy
                   - Information Gain (Fact Density)
                
                2. **The "Why" Diagnostic**: For any category where '{brand_name}' scores lower than '{competitor_name}', 
                   provide a specific reason (e.g., 'Missing Product JSON-LD', 'Low Reddit Sentiment', 'Vague Marketing Prose').
                
                3. **Strategic Gap Analysis**: What is the #1 thing '{brand_name}' must do to steal 'Share of Model' from '{competitor_name}'?
                """
                
                try:
                    response = client.chat.completions.create(
                        model="sonar-pro",
                        messages=[
                            {"role": "system", "content": "Provide professional, data-backed GEO audits with Markdown tables."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Audit failed: {e}")

st.sidebar.divider()
st.sidebar.caption("Powered by Perplexity Sonar-Pro • 2026 Index")
