import json
import streamlit as st
import requests
import graphviz

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
    "which analyzes syntax, code structure, execution flow, variable changes, and flowcharts."
)

code = st.text_area(
    "Enter your Python code here:",
    height=250,
    placeholder="Example:\nfor i in range(3):\n    print(i)"
)

sample_codes = {
    "For Loop": "for i in range(3):\n    print(i)",
    "If Else": "x = 10\nif x > 5:\n    print('Big')\nelse:\n    print('Small')",
    "Function": "def greet(name):\n    return 'Hello ' + name",
    "Variable Update": "x = 5\nx = x + 2\nprint(x)",
    "While Loop": "x = 0\nwhile x < 3:\n    print(x)\n    x = x + 1",
}

selected_sample = st.selectbox(
    "Try a sample code:",
    ["None"] + list(sample_codes.keys())
)

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
        except ValueError:
            st.error("The backend returned an invalid response.")
            st.stop()

        st.divider()
        st.subheader("✅ Final Explanation")

        if not result.get("success"):
            st.error(result.get("error", "Unknown error occurred."))
        else:
            st.success("Code analyzed successfully.")

            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 🧾 Summary")
                st.write(result.get("summary", "No summary available."))

            with col2:
                st.markdown("### 🎯 Difficulty")
                st.success(result.get("difficulty", "Unknown"))

            st.markdown("### 📊 Metrics")
            metrics = result.get("metrics", {})

            col1, col2, col3 = st.columns(3)
            col1.metric("Lines", metrics.get("total_lines", 0))
            col2.metric("Functions", metrics.get("functions", 0))
            col3.metric("Loops", metrics.get("loops", 0))

            col4, col5, col6 = st.columns(3)
            col4.metric("Conditions", metrics.get("conditions", 0))
            col5.metric("Assignments", metrics.get("assignments", 0))
            col6.metric("Imports", metrics.get("imports", 0))

            with st.expander("📝 All Explanations", expanded=False):
                for item in result.get("explanations", []):
                    st.markdown(f"- {item}")

            for category, items in result.get("categories", {}).items():
                if items:
                    with st.expander(f"📁 {category}", expanded=False):
                        for item in items:
                            st.markdown(f"- {item}")

            st.divider()
            with st.expander("🔄 Execution Flow", expanded=True):
                for step in result.get("execution_flow", []):
                    st.markdown(f"- {step}")

            st.divider()
            with st.expander("📊 Variable Timeline", expanded=True):
                timeline = result.get("timeline", {})

                if not timeline:
                    st.info("No variable changes recorded.")
                else:
                    for var, steps in timeline.items():
                        with st.expander(f"Variable: {var}", expanded=False):
                            for step in steps:
                                st.markdown(f"- {step}")

            st.divider()
            st.subheader("🧭 Code Flow Diagram")
            flowchart_source = result.get("flowchart", "")
            if flowchart_source:
                st.graphviz_chart(flowchart_source)
            else:
                st.info("No flowchart available.")

            with st.expander("🔍 View Raw API Response", expanded=False):
                st.json(result)

            st.divider()
            st.subheader("📥 Export Results")

            report_lines = []
            report_lines.append("Python Code Explainer Report")
            report_lines.append("=" * 30)
            report_lines.append("")
            report_lines.append("Summary:")
            report_lines.append(result.get("summary", ""))
            report_lines.append("")
            report_lines.append(f"Difficulty: {result.get('difficulty', '')}")
            report_lines.append("")

            report_lines.append("Metrics:")
            for key, value in metrics.items():
                report_lines.append(f"- {key}: {value}")
            report_lines.append("")

            report_lines.append("All Explanations:")
            for item in result.get("explanations", []):
                report_lines.append(f"- {item}")
            report_lines.append("")

            report_lines.append("Execution Flow:")
            for step in result.get("execution_flow", []):
                report_lines.append(f"- {step}")
            report_lines.append("")

            report_lines.append("Variable Timeline:")
            timeline = result.get("timeline", {})
            if timeline:
                for var, steps in timeline.items():
                    report_lines.append(f"{var}:")
                    for step in steps:
                        report_lines.append(f"  - {step}")
            else:
                report_lines.append("No variable changes recorded.")
            report_lines.append("")

            report_lines.append("Flowchart Source:")
            report_lines.append(result.get("flowchart", ""))

            report_text = "\n".join(report_lines)

            col1, col2 = st.columns(2)

            with col1:
                st.download_button(
                    "📄 Download Report (.txt)",
                    data=report_text,
                    file_name="code_explanation_report.txt",
                    mime="text/plain"
                )

            with col2:
                st.download_button(
                    "📦 Download JSON",
                    data=json.dumps(result, indent=2),
                    file_name="code_explanation.json",
                    mime="application/json"
                )

st.divider()
st.caption("🚀 Python Code Explainer | Built with FastAPI + Streamlit")