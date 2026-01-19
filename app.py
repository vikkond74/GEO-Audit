import streamlit as st
import pandas as pd

# --- APP CONFIG ---
st.set_page_config(page_title="GEO Intelligence Portal", layout="wide", page_icon="🤖")

# Navigation Sidebar to ensure decoupling
page = st.sidebar.radio("Navigate", ["📖 Education Hub", "🔬 Brand Audit Tool"])

# --- PAGE 1: EDUCATION HUB ---
if page == "📖 Education Hub":
    st.title("The 2026 GEO Whitepaper")
    st.subheader("Understanding Generative Engine Optimization")
    
    st.markdown("""
    Generative Engine Optimization (GEO) is the evolution of Search. In 2026, brands no longer compete 
    just for a **ranking position** on a page; they compete to be the **cited source** inside an 
    AI's generated response. 
    """)

    # --- SECTION 1: THE SEARCH CLIFF (Citations) ---
    st.markdown("### 1. Why GEO Matters Now")
    col1, col2 = st.columns(2)
    
    with col1:
        st.info("""
        **The "Zero-Click" Reality** As of 2026, traditional search volume has dropped by **25%** (Gartner). Users are moving to 
        'Answer Engines' like Perplexity, Gemini Live, and SearchGPT that synthesize info directly.
        """)
    
    with col2:
        st.success("""
        **The Citation Advantage** Research from *Seer Interactive (2025)* shows that brands cited in AI Overviews earn 
        **35% higher organic CTR** than those that are merely listed in the links below the fold.
        """)

    st.divider()

    # --- SECTION 2: THE THREE PILLARS ---
    st.markdown("### 2. The Facets of GEO")
    
    pillar_tabs = st.tabs(["✍️ Content Strategy", "⚙️ Technical Signal", "🛡️ Trust & E-E-A-T"])
    
    with pillar_tabs[0]:
        st.markdown("#### Fact-Density & 'Answer-First' Design")
        st.write("""
        AI models prioritize **Information Gain**. If your content just repeats what's already 
        on the web, the LLM has no reason to cite you. 
        * **Strategy:** Use specific data (e.g., '14% increase' vs 'a large increase').
        * **Structure:** Place 'TL;DR' summaries at the top of pages for easy machine extraction.
        """)

    with pillar_tabs[1]:
        st.markdown("#### Machine-Readable Architecture")
        st.write("""
        If an AI crawler can't parse your site in milliseconds, you are invisible.
        * **Entity Schema:** Use JSON-LD to define your brand as a 'Named Entity.'
        * **llms.txt:** The 2026 standard for telling AI models which parts of your site to prioritize.
        """)

    with pillar_tabs[2]:
        st.markdown("#### Off-Site Authority (The Reddit Effect)")
        st.write("""
        LLMs verify your claims by looking at 'Seed Sites.' 
        * **The Fact:** Over **40% of AI citations** in 2025/2026 come from community discussions (Reddit, Quora) and PR-driven coverage (Search Engine Journal).
        * **Goal:** You must exist where the model's training data 'learns' about trust.
        """)

# --- PAGE 2: AUDIT TOOL (Same logic as previous, but in a clean block) ---
elif page == "🔬 Brand Audit Tool":
    st.title("🔬 Brand GEO Audit")
    # (Insert your Audit Tool code here - see previous response for logic)
