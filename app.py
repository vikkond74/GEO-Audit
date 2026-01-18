import streamlit as st
from openai import OpenAI

# --- APP CONFIG ---
st.set_page_config(page_title="Global GEO Intelligence", layout="centered", page_icon="🌍")
st.title("🌍 Global GEO Intelligence Dashboard")

# --- SECURE API KEY ---
try:
    api_key = st.secrets["PERPLEXITY_API_KEY"]
except KeyError:
    st.error("Setup Error: Please add 'PERPLEXITY_API_KEY' to your Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

# --- INPUT ---
company_name = st.text_input("Company Name", placeholder="e.g. Siemens")
region = st.selectbox("Market Focus", ["Global", "Europe", "Asia-Pacific", "Americas", "Middle East & Africa"])

if st.button("Run Intelligence Audit", type="primary"):
    if not company_name:
        st.warning("Please enter a name.")
    else:
        with st.spinner(f"Gathering global insights for {company_name}..."):
            
            prompt = f"""
            Analyze '{company_name}' for the '{region}' market. 
            Provide a two-part report in simple business terms:
            
            ### PART 1: STRATEGIC INSIGHTS
            - **What is Share of Model (SoM)?**: Explain this metric simply (how it's derived and its business benefit).
            - **The Competitive Race**: A table (0-100) comparing {company_name} to its top 3 regional rivals.
            - **Global Brand Perception**: How does AI describe your reputation in {region} vs rivals?
            
            ### PART 2: STRATEGIC RECOMMENDATIONS
            - **Business Strategy**: 3 ways to improve market authority and AI trust.
            - **Technical Implementation**: 3 non-technical fixes (e.g., Schema) with clear examples.
            - **The LLM.txt Roadmap**: Specific content suggestions for an llms.txt file based on {company_name}'s global profile.
            """
            
            try:
                response = client.chat.completions.create(
                    model="sonar-pro",
                    messages=[
                        {"role": "system", "content": f"You are a Global GEO Strategist. Avoid US-bias. Focus on business outcomes in {region}."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                report_text = response.choices[0].message.content
                st.success("Audit Complete")
                st.markdown(report_text)
                
                # --- LLMS.TXT GENERATOR ---
                st.divider()
                st.subheader("🛠️ Technical Asset: Your Custom llms.txt")
                st.markdown("""
                **What is this?** In 2026, AI agents (like ChatGPT or Perplexity) look for a file at `yourdomain.com/llms.txt`. 
                It acts as a 'fast-track' for AI to understand your business without getting lost in your website's design.
                """)
                
                # Logic to "Build" the extract based on AI findings
                llm_content = f"""# {company_name} - AI Resource Map
> Primary Market: {region}
> Purpose: Official brand data for AI synthesis and discovery.

## Executive Summary
{company_name} is a leading provider in the {region} market, recognized by AI models for expertise in its sector.

## Verified Links for AI Retrieval
- /about-us : Core mission and leadership entities.
- /products : Technical specifications for global solutions.
- /investors : Financial authority and stability signals.

## Technical Context
- Authoritative Entity: {company_name}
- Industry Classification: [Extracted from AI Analysis]
- Key Differentiator: [Unique Value Proposition found by Perplexity]
"""
                st.code(llm_content, language="markdown")
                
                st.download_button(
                    label="Download llms.txt File",
                    data=llm_content,
                    file_name="llms.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"Audit failed: {e}")
