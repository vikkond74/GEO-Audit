import streamlit as st
from openai import OpenAI

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

# --- PAGE 1: EDUCATION HUB ---
with tabs[0]:
    st.title("What is Generative Engine Optimization (GEO)?")
    st.markdown("### The Shift: From 'Search' to 'Answer' Engines")
    
    st.info("""
    **2026 Market Intelligence:**
    * **The Death of the Click:** **60% of consumer queries** now end in "zero-click" answers within AI interfaces ([BrightEdge, 2025](https://www.brightedge.com)).
    * **Direct Recommendation Reliance:** **58% of consumers** have replaced traditional search engines with GenAI for product recommendations ([Capgemini, 2025](https://www.capgemini.com)).
    * **The Search Volume Drop:** Traditional search engine volume is projected to decline by **25% by 2026** as users move to AI agents ([Gartner, 2024](https://www.gartner.com)).
    * **Explosive Growth:** Referrals from AI engines to e-commerce brands surged by **752% year-over-year** in the 2025 holiday season ([BrightEdge, 2025](https://www.brightedge.com)).
    """)

    

    st.divider()

    col_biz, col_tech = st.columns(2)

    with col_biz:
        st.subheader("🏢 Business Pillars")
        st.write("**1. Share of Model (SoM):** Like 'Share of Voice,' but measuring how often an AI recommends *you* vs your rivals.")
        st.write("**2. Digital PR & Citations:** AI doesn't crawl the whole web; it cites 'Seed Sites.' You must exist on Reddit, Wiki, and major news outlets.")
        st.write("**3. E-E-A-T Compliance:** Proving your brand has human experts. AI ignores anonymous or low-quality content.")

    with col_tech:
        st.subheader("⚙️ Technical Pillars")
        st.write("**4. Entity Schema:** Using JSON-LD to tell the AI exactly what your brand 'is' so it doesn't have to guess.")
        st.write("**5. Answer-First Code:** Placing 'TL;DR' summaries at the top of pages to make them 'extractable' for AI agents.")
        st.write("**6. Multimodal Feeds:** Optimizing images and product feeds for AI Vision (like Gemini Live or GPT-Vision).")

# --- PAGE 2: AUDIT TOOL ---
with tabs[1]:
    st.title("🔬 Brand GEO Audit")
    st.markdown("Analyze how AI models perceive your brand today.")
    
    col1, col2 = st.columns(2)
    with col1:
        company_name = st.text_input("Brand Name", placeholder="e.g. Patagonia")
    with col2:
        region = st.selectbox("Market Focus", ["Global", "Europe", "Asia-Pacific", "Americas", "Middle East & Africa"])

    if st.button("Run 6-Point GEO Audit", type="primary"):
        if not company_name:
            st.warning("Please enter a brand name.")
        else:
            with st.spinner(f"Auditing {company_name}..."):
                prompt = f"""
                Analyze the consumer brand '{company_name}' for the '{region}' market.
                
                PART 1: BUSINESS (SoM Table, Citations, E-E-A-T)
                PART 2: TECHNICAL (Schema types, Extractability, Multimodal status)
                PART 3: A custom Markdown block for an 'llms.txt' file.
                """
                
                try:
                    response = client.chat.completions.create(
                        model="sonar-pro",
                        messages=[
                            {"role": "system", "content": "You are a Senior GEO Strategist specialized in 2026 AI discovery trends."},
                            {"role": "user", "content": prompt}
                        ]
                    )
                    st.markdown(response.choices[0].message.content)
                except Exception as e:
                    st.error(f"Audit failed: {e}")
