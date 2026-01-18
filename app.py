import streamlit as st
from google import genai
from google.api_core import exceptions
import time

# --- APP CONFIG ---
st.set_page_config(page_title="GEO Audit Pro", layout="wide", page_icon="📈")
st.title("📈 Generative Engine Optimization (GEO) Audit")
st.markdown("""
Analyze how AI models perceive your brand compared to competitors. 
*Powered by Gemini 2.5 Flash.*
""")

# --- SECURE API KEY LOADING ---
try:
    # This pulls from 'Secrets' in Streamlit Cloud or .streamlit/secrets.toml locally
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("Missing API Key! Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

# Initialize the Gemini Client
client = genai.Client(api_key=api_key)

# --- HELPER FUNCTION: RETRY LOGIC ---
def generate_geo_audit(brand, comps):
    """Calls Gemini 2.5 Flash with retry logic for stability."""
    model_id = "gemini-2.5-flash" 
    
    prompt = f"""
    You are a specialist in Generative Engine Optimization (GEO). 
    Perform a competitive audit for the brand: {brand}
    Compare it against: {comps}
    
    Structure the report with these sections:
    1. **AI Visibility Score:** A 1-100 rating of the brand's presence in LLM training data and real-time retrieval.
    2. **Citation Source Analysis:** Where does the AI pull information from (e.g., Reddit, Wikipedia, Official Site)?
    3. **Sentiment & Perception:** How does the AI describe this brand's reputation?
    4. **Competitive Ranking:** A table ranking {brand} and {comps} on 'AI Cite-ability'.
    5. **Actionable Recommendations:** 5 specific content or technical SEO changes to improve GEO.
    """

    max_retries = 3
    for i in range(max_retries):
        try:
            response = client.models.generate_content(
                model=model_id,
                contents=prompt
            )
            return response.text
        except Exception as e:
            err_str = str(e)
            if "429" in err_str or "RESOURCE_EXHAUSTED" in err_str:
                if i < max_retries - 1:
                    wait = (i + 1) * 5
                    st.warning(f"Rate limit hit. Retrying in {wait}s...")
                    time.sleep(wait)
                else:
                    return "Error: Daily API quota exceeded. Please try again later."
            elif "404" in err_str:
                return f"Error: Model '{model_id}' not found. Please verify the model ID."
            else:
                return f"Unexpected API Error: {e}"

# --- UI LAYOUT ---
with st.container():
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input("Brand to Audit", placeholder="e.g. Nike")
    with col2:
        competitors = st.text_input("Competitors", placeholder="e.g. Adidas, Reebok, Puma")

if st.button("Generate GEO Report", type="primary"):
    if not company_name:
        st.warning("Please enter a brand name.")
    else:
        with st.spinner("AI is crawling semantic patterns and auditing visibility..."):
            report = generate_geo_audit(company_name, competitors)
            
            st.markdown("---")
            st.subheader(f"GEO Report: {company_name}")
            st.markdown(report)
            
            # Allow user to download the report
            st.download_button(
                label="Download Report as Text",
                data=report,
                file_name=f"GEO_Audit_{company_name}.txt",
                mime="text/plain"
            )

# --- FOOTER ---
st.divider()
st.caption("GEO Audit Pro v2.0 • 2026 Edition")
