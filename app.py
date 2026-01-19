import streamlit as st
from openai import OpenAI

# --- APP CONFIG ---
st.set_page_config(page_title="GEO Audit Portal", layout="wide", page_icon="🔬")

# --- SECURE API KEY ---
try:
    api_key = st.secrets["PERPLEXITY_API_KEY"]
except KeyError:
    st.error("Setup Error: Please add 'PERPLEXITY_API_KEY' to your Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

# --- AUDIT TOOL INTERFACE ---
st.title("🔬 Enterprise GEO Audit")
st.markdown("Analyze your brand across the 6 core pillars of Generative Engine Optimization.")

# User Input
brand_name = st.text_input("Enter Brand Name", placeholder="e.g. Salesforce")
market_focus = st.selectbox("Market Focus", ["Global", "North America", "Europe", "APAC", "EMEA"])

if st.button("Run 6-Point GEO Analysis", type="primary"):
    if not brand_name:
        st.warning("Please enter a brand name to begin.")
    else:
        with st.spinner(f"Auditing {brand_name} for AI visibility..."):
            
            # 6-Point Framework Prompt
            prompt = f"""
            Analyze the brand '{brand_name}' for the '{market_focus}' market based on the 6 Pillars of GEO in 2026.
            
            For EACH of the following 6 areas, provide:
            1. **Current Analysis**: How the brand is currently perceived or cited by AI models.
            2. **Gap/Improvement**: One specific, actionable step to improve visibility in this area.

            THE 6 PILLARS:
            1. **Entity Clarity**: How well AI understands 'who' the brand is and its core category.
            2. **Information Gain (Fact Density)**: Presence of unique data, stats, or original research that AI loves to cite.
            3. **Technical Schema**: Usage of JSON-LD (FAQ, Organization, Product) for machine readability.
            4. **Citation Source Authority**: Presence on 'Seed Sites' like Reddit, Wiki, or Tier-1 industry news.
            5. **Answer-First Structure**: How extractable the website content is for 'Zero-Click' AI summaries.
            6. **Multimodal Presence**: Optimization of images/video for AI Vision and Voice discovery.
            """

            try:
                response = client.chat.completions.create(
                    model="sonar-pro",
                    messages=[
                        {"role": "system", "content": "You are a Senior GEO Auditor. Provide concise, technical, and strategic analysis in Markdown format."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                # Output Results
                st.success(f"Audit Results for {brand_name}")
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Audit failed: {e}")

st.divider()
st.caption("2026 GEO Audit Engine | Powered by Perplexity AI")
