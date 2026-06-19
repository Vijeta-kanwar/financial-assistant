# --------------------------------------------------------------
# App.py – FINAL PRODUCTION VERSION (Secure + Fraud + Chat)
# --------------------------------------------------------------

import os

# --------------------------------------------------------------
# Clear proxies (important for HF + APIs)
# --------------------------------------------------------------
os.environ.pop("HTTP_PROXY", None)
os.environ.pop("HTTPS_PROXY", None)
os.environ.pop("http_proxy", None)
os.environ.pop("https_proxy", None)
os.environ['HF_HUB_DISABLE_TELEMETRY'] = '1'

# --------------------------------------------------------------
# Imports
# --------------------------------------------------------------
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.express as px
from rag_pipeline import FinRAG
from dotenv import load_dotenv
from fraud_graph import detect_fraud_rings
import jwt
from jwt import ExpiredSignatureError, InvalidTokenError

# --------------------------------------------------------------
# 🔐 JWT VALIDATION
# --------------------------------------------------------------
def is_token_valid(token):
    try:
        jwt.decode(
            token,
            options={
                "verify_signature": False,
                "verify_exp": True
            }
        )
        return True
    except (ExpiredSignatureError, InvalidTokenError):
        return False


# --------------------------------------------------------------
# 🔐 PAGE PROTECTION
# --------------------------------------------------------------
token = st.session_state.get("token")

if not token or not is_token_valid(token):
    st.session_state.clear()
    st.switch_page("Login.py")
    st.stop()

# --------------------------------------------------------------
# Load environment variables
# --------------------------------------------------------------
load_dotenv()

# --------------------------------------------------------------
# Page Config
# --------------------------------------------------------------
st.set_page_config(
    page_title="Anandrathi Personal Finance Manager AI",
    page_icon="💰",
    layout="wide"
)

st.markdown("""
<style>
.main-header {font-size: 2.5rem; color:#1E88E5; text-align:center;}
.sub-header {font-size:1.2rem; color:#666; text-align:center;}
.stChatMessage {border-radius:15px;}
</style>
""", unsafe_allow_html=True)

# --------------------------------------------------------------
# Load RAG (cached)
# --------------------------------------------------------------
@st.cache_resource
def load_rag():
    return FinRAG()

rag = load_rag()

# --------------------------------------------------------------
# HEADER
# --------------------------------------------------------------
st.markdown(
    '<p class="main-header">💰 Anandrathi Personal Finance Manager AI</p>',
    unsafe_allow_html=True
)
st.markdown(
    '<p class="sub-header">Your AI-powered financial assistant — ask anything about your money!</p>',
    unsafe_allow_html=True
)
st.divider()

# --------------------------------------------------------------
# SIDEBAR
# --------------------------------------------------------------
with st.sidebar:

    st.header("📁 Your Financial Data")

    uploaded_file = st.file_uploader("Upload CSV/Excel file", type=['csv', 'xlsx'])
    use_sample = st.checkbox("Use sample data instead", value=True)

    if uploaded_file:
        df = pd.read_csv(uploaded_file) if uploaded_file.name.endswith('.csv') else pd.read_excel(uploaded_file)
        st.session_state.df = df
        st.success("✅ Your data loaded!")
        use_sample = False

    elif use_sample:
        try:
            df = pd.read_csv("data/sample_transactions.csv")
            st.session_state.df = df
            st.success("✅ Sample data loaded!")
        except FileNotFoundError:
            st.error("Sample file not found.")

    # ---------------- Data Preview ----------------
    if "df" in st.session_state:
        st.subheader("📋 Data Preview")
        st.dataframe(st.session_state.df.head(10), use_container_width=True)

        st.subheader("📊 Quick Stats")

        df_temp = st.session_state.df
        expenses = df_temp[df_temp['category'] != 'Income']
        income = df_temp[df_temp['category'] == 'Income']

        col1, col2 = st.columns(2)
        col1.metric("Total Expenses", f"₹{expenses['amount'].sum():,.0f}")
        col2.metric("Total Income", f"₹{income['amount'].sum():,.0f}")
        st.metric("Current Balance", f"₹{df_temp['balance'].iloc[-1]:,.0f}")

    st.divider()

    # ---------------- Fraud Detection ----------------
    st.subheader("🚨 Visual Fraud-Ring Detection")

    if st.button("Run Fraud-Ring Analysis", use_container_width=True):

        if "df" not in st.session_state:
            st.warning("⚠️ Upload data first.")

        else:
            with st.spinner("🔎 Detecting fraud rings..."):

                result = detect_fraud_rings(
                    st.session_state.df,
                    min_cycle_len=3,
                    min_weight=10_000
                )

                st.success(result["message"])

                components.html(
                    result["graph_html"],
                    height=650,
                    scrolling=True
                )

                if result["rings"]:
                    st.write("#### Detected Rings")
                    for i, ring in enumerate(result["rings"], 1):
                        st.write(f"**Ring {i}:** `{', '.join(ring)}`")

    st.divider()

    # ---------------- Logout ----------------
    if st.button("🚪 Logout", use_container_width=True):
        st.session_state.clear()
        st.switch_page("Login.py")
        st.stop()

# --------------------------------------------------------------
# CHAT INTERFACE
# --------------------------------------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "assistant",
        "content": (
            "👋 Hi! Upload your data and ask me about spending, budgeting, "
            "investments — or fraud ring detection."
        )
    }]

# Display chat history
# Display chat history
for idx, message in enumerate(st.session_state.messages):
    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message.get("chart"):
            chart = message["chart"]

            if chart["type"] == "pie":
                fig = px.pie(
                    values=chart['values'],
                    names=chart['names'],
                    title=chart['title'],
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    key=f"chat_chart_{idx}"
                )

            elif chart["type"] == "line":
                fig = px.line(
                    x=chart['x'],
                    y=chart['y'],
                    title=chart['title'],
                    labels={'x': 'Date', 'y': 'Balance (₹)'}
                )
                st.plotly_chart(
                    fig,
                    use_container_width=True,
                    key=f"chat_chart_{idx}"
                )

        if message.get("graph_html"):
            components.html(
                message["graph_html"],
                height=650,
                scrolling=True
            )
# --------------------------------------------------------------
# CHAT INPUT
# --------------------------------------------------------------
if prompt := st.chat_input("Ask about spending, budget, investments or fraud rings..."):

    st.session_state.messages.append({"role": "user", "content": prompt})

    with st.chat_message("assistant"):

        if "df" not in st.session_state:

            msg = "⚠️ Please upload your transaction data first."
            st.warning(msg)

            st.session_state.messages.append({
                "role": "assistant",
                "content": msg
            })

        elif "fraud" in prompt.lower() and "ring" in prompt.lower():

            result = detect_fraud_rings(
                st.session_state.df,
                min_cycle_len=3,
                min_weight=10_000
            )

            st.markdown(result["message"])

            components.html(
                result["graph_html"],
                height=650,
                scrolling=True
            )

            st.session_state.messages.append({
                "role": "assistant",
                "content": result["message"],
                "graph_html": result["graph_html"]
            })

        else:

            with st.spinner("🔍 Analyzing your finances..."):

                response, chart_config = rag.query(prompt, st.session_state.df)

                st.markdown(response)

                if chart_config:

                    if chart_config["type"] == "pie":
                        fig = px.pie(
                            values=chart_config['values'],
                            names=chart_config['names'],
                            title=chart_config['title'],
                            color_discrete_sequence=px.colors.qualitative.Set3
                        )
                        st.plotly_chart(fig, use_container_width=True)

                    elif chart_config["type"] == "line":
                        fig = px.line(
                            x=chart_config['x'],
                            y=chart_config['y'],
                            title=chart_config['title'],
                            labels={'x': 'Date', 'y': 'Balance (₹)'}
                        )
                        st.plotly_chart(fig, use_container_width=True)

            st.session_state.messages.append({
                "role": "assistant",
                "content": response,
                "chart": chart_config
            })