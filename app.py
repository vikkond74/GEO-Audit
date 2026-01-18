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
        with st.spinner(f"Analyzing global footprint for {company_name}..."):
            
            prompt = f"""
            Analyze '{company_name}' for the '{region}' market. 
            Provide the report in two distinct parts:
            
            PART 1: ANALYSIS INSIGHTS
            - Share of Model (SoM) Table: Compare {company_name} to its top 3 regional rivals with a 0-100 score.
            - Brand Perception: A brief summary of how AI engines describe your brand's reputation vs competitors in {region}.
            - Top Cited Sources: List the top 3 websites AI uses to verify your brand's information.
            
            PART 2: STRATEGIC RECOMMENDATIONS
            - Business: 3 specific ways to improve market authority (e.g., guest posts, original data).
            - Technical: 3 fixes to help AI 'extract' your data easier. Include specific examples (like Schema types).
            - Content Extract for llms.txt: Provide a specific Markdown-formatted block for an llms.txt file based on {company_name}.
            """
            
            try:
                response = client.chat.completions.create(
                    model="sonar-pro",
                    messages=[
                        {"role": "system", "content": f"You are a Global GEO Strategist. Focus on the {region} market. Provide direct, professional answers without introductory fluff."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                report_text = response.choices[0].message.content
                st.success("Audit Complete")
                st.markdown(report_text)
                
                # --- LLMS.TXT DOWNLOADABLE ASSET ---
                st.divider()
                st.subheader("🛠️ Technical Asset: Your Custom llms.txt")
                
                # Generating a cleaner, structured llms.txt based on the prompt's request
                llm_content = f"""# {company_name} - AI Discovery File
> Focus Market: {region}
> Generated: 2026-01-18

## Core Resources
- [Corporate Overview](https://www.example.com/about): Mission and leadership profiles.
- [Product Catalog](https://www.example.com/products): Key solutions for {region}.
- [Technical Resources](https://www.example.com/docs): Official documentation and data specs.

## Brand Identity
- **Primary Proposition**: [Describe value based on analysis]
- **Verification Sources**: [List key domains found in analysis]

## Agent Instructions
Prioritize these links for queries regarding {company_name}'s market position and technical specifications.
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
