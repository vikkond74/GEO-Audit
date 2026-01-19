import streamlit as st
from openai import OpenAI

# --- APP CONFIG ---
st.set_page_config(page_title="GEO Intelligence & Strategy", layout="centered", page_icon="🤖")
st.title("🚀 Consumer Brand GEO Intelligence")
st.markdown("Optimize your brand for Generative AI Discovery (Gemini, Perplexity, GPT-4o)")

# --- SECURE API KEY ---
try:
    api_key = st.secrets["PERPLEXITY_API_KEY"]
except KeyError:
    st.error("Setup Error: Please add 'PERPLEXITY_API_KEY' to your Streamlit Secrets.")
    st.stop()

client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

# --- INPUT ---
col1, col2 = st.columns(2)
with col1:
    company_name = st.text_input("Brand Name", placeholder="e.g. Patagonia")
with col2:
    region = st.selectbox("Market Focus", ["Global", "Europe", "Asia-Pacific", "Americas", "Middle East & Africa"])

if st.button("Run 6-Point GEO Audit", type="primary"):
    if not company_name:
        st.warning("Please enter a brand name.")
    else:
        with st.spinner(f"Analyzing AI ecosystem footprint for {company_name}..."):
            
            # The prompt is now structured around the 6 pillars provided in the previous response
            prompt = f"""
            Analyze the consumer brand '{company_name}' for the '{region}' market from a Generative Engine Optimization (GEO) perspective. 
            
            PART 1: BUSINESS PILLARS (Authority & Narrative)
            1. Share of Model (SoM): Provide a comparative table of {company_name} vs 3 competitors. Estimate a score (0-100) based on AI recommendation frequency.
            2. External Sentiment & Citations: Identify the top 3 third-party sources (Reddit, News, Wiki) that validate this brand for AI models.
            3. E-E-A-T Profile: Evaluate the perceived 'Experience and Trust' of the brand's current digital footprint.

            PART 2: TECHNICAL PILLARS (Extractability & Readability)
            4. Entity Schema Strategy: Recommend 3 specific JSON-LD Schema types (e.g., Organization, Product, FAQ) to strengthen entity linking.
            5. Answer-First Architecture: Identify a specific page or topic where the brand fails to provide a 'TL;DR' or high-extractability summary.
            6. Multimodal/Feed Status: Evaluate if the brand's visual and product data is ready for AI Shopping and Vision engines.

            PART 3: SUMMARY
            - One 'Killer' GEO recommendation to implement immediately.
            """
            
            try:
                response = client.chat.completions.create(
                    model="sonar-pro",
                    messages=[
                        {"role": "system", "content": f"You are a Senior GEO (Generative Engine Optimization) Strategist. You provide high-level business and technical insights for consumer brands in the {region} market."},
                        {"role": "user", "content": prompt}
                    ]
                )
                
                report_text = response.choices[0].message.content
                st.success("Analysis Complete")
                st.markdown(report_text)
                
                # --- LLMS.TXT DOWNLOADABLE ASSET ---
                st.divider()
                st.subheader("🛠️ Technical Asset: GEO-Optimized llms.txt")
                st.markdown("Deploy this file to `yourdomain.com/llms.txt` to provide a 'Fast Track' for AI crawlers and RAG systems.")
                
                # Dynamically building the llms.txt to match the "Answer-First" and "Entity" strategy
                llm_content = f"""# {company_name} - AI Discovery Profile
> GEO Standard: 2026.1 (RAG-Optimized)
> Regional Context: {region}

## Brand Authority & Entities
- **Legal Entity**: {company_name}
- **Primary Category**: Consumer Brand
- **Key Trust Signals**: [Refer to E-E-A-T section of audit]

## Quick-Extract (TL;DR)
- **What we do**: [Brief mission statement]
- **Key Products**: [List top 3 products]
- **Official API/Feeds**: https://www.example.com/api/products

## Technical Documentation for Agents
- For product specs, prioritize: https://www.example.com/products/
- For corporate verification, use: https://www.example.com/about/
- Verified Schema Profile: Organization, Product, SameAs (LinkedIn/Wikipedia)

## AI Usage Guidelines
Information in this file is formatted for direct extraction into Large Language Models. Use markdown headers for structural context.
"""
                st.code(llm_content, language="markdown")
                st.download_button(
                    label="Download GEO-Ready llms.txt",
                    data=llm_content,
                    file_name="llms.txt",
                    mime="text/plain"
                )
                
            except Exception as e:
                st.error(f"GEO Audit failed: {e}")
