import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/explain"

st.set_page_config(
    page_title="Python Code Explainer",
    page_icon="🧠",
    layout="centered"
)

st.title("🧠 Python Code Explainer")
st.caption("A beginner-friendly standalone dashboard for explaining Python code.")

st.info(
    "Paste your Python code below and click **Explain Code**. "
    "The app checks syntax, analyzes code structure, and shows a simplified explanation."
)

st.sidebar.title("About")
st.sidebar.info(
    "This dashboard sends your Python code to a FastAPI backend, "
    "which analyzes syntax, code structure, and execution flow."
)

code = st.text_area(
    "Enter your Python code here:",
    height=250,
    placeholder="Example:\nfor i in range(3):\n    print(i)"
)

sample_codes = {
    "For Loop": "for i in range(3):\n    print(i)",
    "If Else": "x = 10\nif x > 5:\n    print('Big')\nelse:\n    print('Small')",
    "Function": "def greet(name):\n    return 'Hello ' + name"
}

selected_sample = st.selectbox("Try a sample code:", ["None"] + list(sample_codes.keys()))

if selected_sample != "None":
    code = sample_codes[selected_sample]
    st.code(code, language="python")

if st.button("Explain Code"):
    if not code.strip():
        st.warning("Please write or paste some Python code first.")
    else:
        st.divider()
        st.subheader("📄 Your Code")
        st.code(code, language="python")

        try:
            response = requests.post(API_URL, json={"code": code}, timeout=20)
            result = response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Could not connect to FastAPI backend: {e}")
            st.stop()

        st.divider()
        st.subheader("✅ Final Explanation")

        if not result["success"]:
            st.error(result["error"])
        else:
            st.success("Code analyzed successfully.")

            st.markdown("### 🧾 Summary")
            st.write(result["summary"])

            st.markdown("### 🎯 Difficulty")
            st.info(result["difficulty"])

            st.markdown("### 📊 Metrics")
            metrics = result["metrics"]
            col1, col2, col3 = st.columns(3)
            col1.metric("Lines", metrics["total_lines"])
            col2.metric("Functions", metrics["functions"])
            col3.metric("Loops", metrics["loops"])

            col4, col5, col6 = st.columns(3)
            col4.metric("Conditions", metrics["conditions"])
            col5.metric("Assignments", metrics["assignments"])
            col6.metric("Imports", metrics["imports"])

            st.markdown("### 📝 All Explanations")
            for item in result["explanations"]:
                st.markdown(f"- {item}")

            for category, items in result["categories"].items():
                if items:
                    with st.expander(category):
                        for item in items:
                            st.markdown(f"- {item}")

            st.divider()
            st.subheader("🔄 Execution Flow")
            for step in result["execution_flow"]:
                st.markdown(f"- {step}")