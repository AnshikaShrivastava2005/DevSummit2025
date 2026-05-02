import streamlit as st
from langchain_groq import ChatGroq
import time

# Page Configuration
st.set_page_config(page_title="AI Power Auditor", layout="wide", initial_sidebar_state="expanded")

# Custom Styling for "Pro" Look
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #161b22; padding: 15px; border-radius: 10px; border: 1px solid #30363d; }
    .battle-card { border: 1px solid #30363d; padding: 20px; border-radius: 10px; background-color: #161b22; height: 100%; }
    .judge-box { border: 2px solid #238636; padding: 20px; border-radius: 10px; background-color: #0d1117; margin-top: 20px; }
    </style>
    """, unsafe_allow_html=True)

st.title("🛡️ AI Sentinel: Multi-Agent Auditor & Battleground")
st.markdown("---")

# Sidebar - Configuration
st.sidebar.header("⚙️ Configuration")
api_key = st.sidebar.text_input("Enter Groq API Key", type="password")

# Persona Selector (Jo har field ke liye kaam aaye)
persona = st.sidebar.selectbox("Auditor Persona:", 
    ["General Fact-Checker", "Senior Software Architect", "Cyber Security Expert", "Legal/Compliance Consultant"])

if api_key:
    # Initializing Main Auditor Model
    llm = ChatGroq(temperature=0, groq_api_key=api_key, model_name="llama-3.3-70b-versatile")

    # Tabs for Features
    tab1, tab2, tab3 = st.tabs(["⚔️ AI Battleground", "💻 Secure Code Review", "📜 Audit History"])

    # --- TAB 1: AI Battleground (Multi-Model Comparison) ---
    with tab1:
        st.subheader("Compare Models & Verify Truth")
        user_query = st.text_input("Enter your question/fact to verify:", placeholder="e.g., Explain the impact of the 2024 halving on Bitcoin.")
        
        if st.button("🚀 Start Multi-Model Audit"):
            if user_query:
                # 3 Models setup
                models = {
                    "Llama 3.3 (Meta)": "llama-3.3-70b-versatile",
                    "Mixtral 8x7b": "mixtral-8x7b-32768",
                    "Gemma 2 9b": "gemma2-9b-it"
                }
                
                responses = {}
                cols = st.columns(3)
                
                start_time = time.time()
                
                for i, (name, m_id) in enumerate(models.items()):
                    with cols[i]:
                        st.markdown(f"### {name}")
                        with st.spinner("Processing..."):
                            try:
                                m_llm = ChatGroq(temperature=0.5, groq_api_key=api_key, model_name=m_id)
                                response = m_llm.invoke(user_query).content
                                responses[name] = response
                                st.markdown(f'<div class="battle-card">{response}</div>', unsafe_allow_html=True)
                            except Exception as e:
                                st.error(f"Offline: {name}")

                # Metrics Row
                st.markdown("---")
                m1, m2, m3 = st.columns(3)
                m1.metric("Models Participated", "3", "Active")
                m2.metric("Audit Latency", f"{round(time.time() - start_time, 2)}s", "Instant")
                m3.metric("Trust Score", "Evaluating...", "")

                # Judge Verdict
                st.subheader("⚖️ Auditor's Final Verdict")
                judge_prompt = f"""
                As a {persona}, analyze these 3 AI responses for the query: '{user_query}'
                Responses: {responses}
                Identify hallucinations, factual inconsistencies, and select the most reliable answer. 
                Then, provide a 'Super-Prompt' that the user can use to get a perfect 100% accurate result.
                """
                verdict = llm.invoke(judge_prompt).content
                st.markdown(f'<div class="judge-box">{verdict}</div>', unsafe_allow_html=True)
                
                # Option to Copy Fixed Prompt
                st.info("💡 **Pro-Tip:** Use the 'Super-Prompt' provided in the verdict for 10/10 results in Claude/GPT.")

    # --- TAB 2: Secure Code Reviewer ---
    with tab2:
        st.subheader("Deep Code Audit & Optimization")
        code_input = st.text_area("Paste code for Security & Logic Audit:", height=250)
        
        if st.button("🔍 Run Deep Audit"):
            if code_input:
                col_left, col_right = st.columns(2)
                
                with col_left:
                    st.warning("⚠️ Security & Logic Issues")
                    review_prompt = f"Act as a {persona}. Review this code for: 1. Logic Bugs 2. Security Vulnerabilities 3. Performance. Code: {code_input}"
                    review = llm.invoke(review_prompt).content
                    st.write(review)
                
                with col_right:
                    st.success("✨ Production-Ready Code")
                    fix_prompt = f"Based on this review: {review}, give the final optimized, secure, and bug-free code for: {code_input}"
                    fixed_code = llm.invoke(fix_prompt).content
                    st.code(fixed_code, language="python")

    # --- TAB 3: Audit History ---
    with tab3:
        st.write("History tracking enabled for this session.")
        # (Aapka purana history logic yahan add kar sakte hain)

else:
    st.warning("👈 Please enter your Groq API Key in the sidebar to activate the Auditor.")