import streamlit as st
from google import genai
import time

# --- APP CONFIG ---
st.set_page_config(page_title="GEO Business Intelligence", layout="centered", page_icon="🏢")
st.title("🏢 GEO Brand Intelligence Dashboard")
st.markdown("Enter your company name to see how AI search engines perceive your brand and where you stand against the competition.")

# --- SECURE API KEY ---
try:
    api_key = st.secrets["GEMINI_API_KEY"]
except KeyError:
    st.error("Setup Error: Please add 'GEMINI_API_KEY' to your Streamlit Secrets.")
    st.stop()

client = genai.Client(api_key=api_key)

# --- ONE BOX, ONE BUTTON ---
company_name = st.text_input("What is your Company Name?", placeholder="e.g. Patagonia")

if st.button("Run Full Brand Audit", type="primary"):
    if not company_name:
        st.warning("Please enter a name to begin.")
    else:
        with st.spinner(f"Analyzing {company_name} and identifying key market rivals..."):
            
            # The prompt now forces the AI to pick competitors and explain things simply
            prompt = f"""
            Act as a Senior Business Strategist. Perform a GEO (Generative Engine Optimization) Audit for '{company_name}'.
            
            FIRST: Identify the 3 most likely business competitors for '{company_name}' based on current market data.
            
            SECOND: Provide a report with the following sections. Use business terms, avoid technical jargon.
            
            1. **Share of Model (AI Market Share):** - Explain: This is how often AI 'thinks' of you versus your rivals.
               - Provide a simple table with a score (1-100) for {company_name} and the 3 competitors.
            
            2. **Brand Reputation & Perception:** - Explain: This is the 'personality' AI gives your brand when answering customer questions.
               - Summarize how the AI describes {company_name}.
            
            3. **The Opportunity Gap:** - Explain: These are the specific topics or strengths your competitors are 'winning' in AI conversations.
               - List 3 specific things {company_name} should talk about more to steal AI citations.
            
            4. **AI-Readiness Checklist:** - Explain: Simple fixes to make your website easier for AI to read.
               - Provide 3 bullet points of simple, non-technical advice.
            """
            
            try:
                response = client.models.generate_content(
                    model="gemini-2.0-flash",
                    contents=prompt
                )
                
                # --- DISPLAY EVERYTHING IN ONE FLOW ---
                st.success("Audit Complete")
                st.divider()
                st.markdown(response.text)
                
                # Simple export
                st.download_button("Download Executive Summary", response.text, file_name=f"{company_name}_GEO_Audit.md")
                
            except Exception as e:
                st.error(f"Analysis interrupted: {e}")

st.divider()
st.info("**What is GEO?** In simple terms, it's the new SEO. Instead of ranking on page 1 of Google, GEO ensures that when someone asks ChatGPT or Gemini a question, your brand is the one the AI recommends.")
