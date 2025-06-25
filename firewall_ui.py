import streamlit as st
from classifier import classify_prompt
from firewall import call_main_llm
from config import USE_FEW_SHOT
import json

# 🛠️ Setup
st.set_page_config(page_title="LLM Prompt Firewall", layout="wide")

# 🌗 Theme
mode = st.sidebar.radio("🎨 Theme", ["Light", "Dark"])
if mode == "Dark":
    st.markdown("""
        <style>
        body, .stApp {
            background-color: #121212;
            color: white;
        }
        textarea, input, .stButton>button {
            background-color: #1e1e1e;
            color: white;
        }
        </style>
    """, unsafe_allow_html=True)

# 📘 Title & Description
st.title("🛡️ LLM Prompt Firewall")
st.caption("Test prompts using classification + LLM response safety checks")

st.markdown("---")

# 📝 Input Prompt
prompt = st.text_area("🔤 Enter a prompt to test:", height=150)

# ⚙️ Options
col1, col2 = st.columns(2)
with col1:
    firewall_enabled = st.toggle("🛡️ Enable Firewall", value=True)
with col2:
    few_shot_enabled = st.toggle("🧠 Use Few-Shot Classification", value=USE_FEW_SHOT)

# 🚀 Trigger Evaluation
if st.button("Run Full Evaluation"):
    st.markdown("### 🧪 Evaluation Output")

    # Store results here (matches JSON structure)
    result = {
        "prompt": prompt,
        "response": None,
        "predicted": None,
        "true_label": "unknown",  # You can replace with actual if used
        "blocked_at": None
    }

    # 🔍 Step 1: Prompt classification
    if firewall_enabled:
        prompt_class = classify_prompt(prompt, few_shot=few_shot_enabled)
        st.write(f"**Prompt Classification:** `{prompt_class}`")

        if prompt_class in ["jailbreak", "unknown"]:
            st.error(f"❌ Blocked at prompt stage. Classification: `{prompt_class}`")
            result["predicted"] = prompt_class
            result["blocked_at"] = "prompt"

    # 🤖 Step 2: LLM call
    if result["blocked_at"] is None:
        with st.spinner("Calling LLM..."):
            response = call_main_llm(prompt)

        result["response"] = response
        st.text_area("💬 LLM Response", response, height=200)

        # 🔍 Step 3: Response classification
        if firewall_enabled:
            response_class = classify_prompt(response, few_shot=few_shot_enabled)
            st.write(f"**Response Classification:** `{response_class}`")

            if response_class in ["jailbreak", "unknown"]:
                st.warning("⚠️ Blocked at response stage.")
                result["predicted"] = response_class
                result["blocked_at"] = "response"
            else:
                st.success("✅ Response is safe.")
                result["predicted"] = "benign"
        else:
            st.success("✅ Firewall disabled. Response shown directly.")
            result["predicted"] = "benign"
    else:
        result["response"] = None

    # ✅ Final result output
    st.markdown("### 📄 Result Summary")
    st.json(result)

    # Save locally
    with open("single_eval_result.json", "w") as f:
        json.dump(result, f, indent=2)

# 📂 JSON Upload Viewer
st.sidebar.markdown("---")
st.sidebar.subheader("📁 View Evaluation JSON")
uploaded_file = st.sidebar.file_uploader("Upload `.json` results", type="json")

if uploaded_file:
    data = json.load(uploaded_file)
    st.sidebar.write(f"Total Entries: {len(data)}" if isinstance(data, list) else "1 Entry")

    # Show breakdown
    if st.sidebar.checkbox("📊 Show Breakdown"):
        if isinstance(data, dict):
            data = [data]
        blocked_prompt = sum(1 for r in data if r["blocked_at"] == "prompt")
        blocked_response = sum(1 for r in data if r["blocked_at"] == "response")
        clean = len(data) - blocked_prompt - blocked_response

        st.sidebar.metric("🛑 Blocked at Prompt", blocked_prompt)
        st.sidebar.metric("⚠️ Blocked at Response", blocked_response)
        st.sidebar.metric("✅ Clean Completions", clean)
