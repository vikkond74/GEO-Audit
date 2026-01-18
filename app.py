import streamlit as st
from openai import OpenAI # Perplexity uses the OpenAI-compatible format

# --- APP CONFIG ---
st.set_page_config(page_title="GEO Brand Intelligence", layout="centered", page_icon="🏢")
st.title("🏢 GEO Brand Intelligence Dashboard")
st.markdown("Discover how AI search engines recommend your brand to customers using real-time Perplexity data.")

# --- SECURE API KEY ---
try:
    api_key = st.secrets["PERPLEXITY_API_KEY"]
except KeyError:
    st.error("Setup Error: Please add 'PERPLEXITY_API_KEY' to your Streamlit Secrets.")
    st.stop()

# Perplexity uses the OpenAI client pointed to their URL
client = OpenAI(api_key=api_key, base_url="https://api.perplexity.ai")

company_name = st.text_input("What is your Company Name?", placeholder="e.g. Patagonia")

if st.button("Run Executive Audit", type="primary"):
    if not company_name:
        st.warning("Please enter a name.")
    else:
        with st.spinner(f"Perplexity is scanning the live web for {company_name}..."):
            
            prompt = f"""
            Identify the top 3 competitors for '{company_name}'.
            Then, provide a GEO (Generative Engine Optimization) report in simple business terms:
            
            1. Share of Model: A table (0-100) showing how likely you are to be recommended vs rivals.
            2. AI Perception: How does the AI describe your brand's reputation to a user?
            3. The Opportunity Gap: 3 topics your competitors 'own' that you should claim.
            4. 3 Simple Website Fixes: Non-technical advice to get cited more.
            """
            
            try:
                # 'sonar-pro' is the standard for high-quality search results
                response = client.chat.completions.create(
                    model="sonar-pro",
                    messages=[{"role": "user", "content": prompt}]
                )
                
                st.success("Real-time Audit Complete")
                st.divider()
                st.markdown(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"Analysis failed: {e}")

st.divider()
st.info("**Why Perplexity?** Because you have Pro, this tool uses real-time search data and 'Sonar' models, which are more accurate for competitive brand tracking than standard AI.")
