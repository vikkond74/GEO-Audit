import streamlit as st
from google import genai
from google.api_core import exceptions
import time

# --- APP CONFIG ---
st.set_page_config(page_title="GEO Audit Suite 2026", layout="wide", page_icon="🎯")
st.title("🎯 GEO Audit Suite 2026")
st.markdown("Optimize your brand for the generative web: Share of Model, Semantic Gaps, and Technical Readiness.")

# --- SECURE API KEY LOADING ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("Missing API Key! Add 'GEMINI_API_KEY' to Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# --- CORE LOGIC: RETRY WRAPPER ---
def run_ai_query(prompt):
    """Resilient API call for Gemini 2.5 Flash."""
    max_retries = 3
    for i in range(max_retries):
        try:
            # Using 2.5 Flash for the 2026 stable environment
            return client.models.generate_content(
                model="gemini-2.5-flash",
                contents=prompt
            )
        except Exception as e:
            if "429" in str(e):
                time.sleep((i + 1) * 5)
            else:
                return f"Error: {e}"
    return "Rate limit exceeded. Try again in a minute."

# --- UI TABS ---
tab1, tab2, tab3 = st.tabs(["🚀 Brand Audit & SoM", "🕳️ Semantic Gap Analysis", "🛠️ Technical Checklist"])

with tab1:
    st.header("Share of Model (SoM) Audit")
    c1, c2 = st.columns(2)
    with c1:
        brand = st.text_input("Brand Name", placeholder="e.g. Acme Tech")
    with c2:
        comps = st.text_input("Competitors", placeholder="e.g. CompetitorA, CompetitorB")

    if st.button("Generate Audit", type="primary"):
        with st.spinner("Calculating Share of Model..."):
            prompt = f"""
            Perform a GEO Audit for '{brand}' vs '{comps}'.
            1. **Share of Model (SoM) Score:** Assign a score from 0-100 for each based on AI citation frequency.
            2. **Perception Audit:** How does the LLM describe the brand's unique value?
            3. **Citation Authority:** List the top 3 domains the AI uses to verify this brand.
            Return in a clean Markdown format with a table for SoM.
            """
            result = run_ai_query(prompt)
            st.markdown(result.text if hasattr(result, 'text') else result)

with tab2:
    st.header("Semantic & Topic Gap Analysis")
    st.info("Uncover the specific topics your competitors 'own' in AI summaries that you are missing.")
    
    if st.button("Analyze Content Gaps"):
        if not brand or not comps:
            st.warning("Please fill in brand and competitors in Tab 1 first.")
        else:
            with st.spinner("Finding information gaps..."):
                prompt = f"""
                Analyze the 'Semantic Space' of {brand} compared to {comps}.
                Identify 5 specific 'Topic Gaps'—factual areas or statistics where competitors are cited but {brand} is not.
                Provide a specific 'Citation Hook' for each gap (a sentence the brand should add to its site to be cited).
                """
                gap_result = run_ai_query(prompt)
                st.markdown(gap_result.text if hasattr(gap_result, 'text') else gap_result)

with tab3:
    st.header("Technical AI-Readiness Checklist")
    st.write("Does your site meet the 2026 technical standards for AI crawlers?")
    
    # These are the 3 key technical signals for 2026
    col_a, col_b = st.columns(2)
    with col_a:
        st.checkbox("LLMS.txt file present in root directory", help="A markdown file specifically for AI agent guidance.")
        st.checkbox("Author Schema (E-E-A-T) connected to Person entities", help="Proves content is human-expert verified.")
        st.checkbox("Nested Product/FAQ Schema", help="Allows RAG systems to parse data without 'guessing'.")
    with col_b:
        st.checkbox("Zero-Javascript Content accessible", help="Ensures LLM crawlers see content without rendering JS.")
        st.checkbox("Fact-Density > 60%", help="High info-to-fluff ratio for better summarization.")
        
    st.divider()
    st.subheader("Action Plan")
    if st.button("Generate Technical Roadmap"):
        roadmap_prompt = f"Create a technical GEO roadmap for {brand} to implement llms.txt and Author Schema."
        roadmap = run_ai_query(roadmap_prompt)
        st.markdown(roadmap.text if hasattr(roadmap, 'text') else roadmap)

st.divider()
st.caption("GEO Audit Suite • Gemini 2.5 Flash Stable • v2.1 (2026)")
