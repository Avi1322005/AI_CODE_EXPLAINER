import json
import streamlit as st
import requests
import graphviz

API_URL = "http://127.0.0.1:8000/explain"

st.set_page_config(
    page_title="Python Code Explainer",
    page_icon="🧠",
    layout="wide"
)

# ---------------- SAMPLE CODES ----------------
sample_codes = {
    "For Loop": "for i in range(3):\n    print(i)",
    "If Else": "x = 10\nif x > 5:\n    print('Big')\nelse:\n    print('Small')",
    "Function": "def greet(name):\n    return 'Hello ' + name",
    "Variable Update": "x = 5\nx = x + 2\nprint(x)",
    "While Loop": "x = 0\nwhile x < 3:\n    print(x)\n    x = x + 1",
}

# ---------------- HEADER ----------------
st.title("🧠 Python Code Explainer")
st.caption("A beginner-friendly standalone dashboard for explaining Python code.")

st.info(
    "Paste your Python code below and click **Explain Code**. "
    "The app checks syntax, analyzes code structure, and shows a simplified explanation."
)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ Control Panel")

st.sidebar.markdown("### ℹ️ About")
st.sidebar.info(
    "This dashboard uses a FastAPI backend to analyze Python code and generate "
    "summaries, explanations, execution flow, variable tracking, and flow diagrams."
)

view_mode = st.sidebar.radio(
    "View Style:",
    ["Focused", "Detailed"],
    index=0
)

preset_mode = st.sidebar.radio(
    "Analysis Mode:",
    ["Beginner", "Developer", "Full Analysis", "Custom"],
    index=0
)

all_options = [
    "Summary",
    "Difficulty",
    "Metrics",
    "All Explanations",
    "Categories",
    "Execution Flow",
    "Variable Timeline",
    "Flow Diagram",
    "Raw API Response",
]

preset_map = {
    "Beginner": ["Summary", "All Explanations", "Execution Flow"],
    "Developer": ["Metrics", "Variable Timeline", "Raw API Response"],
    "Full Analysis": all_options,
}

if preset_mode == "Custom":
    selected_views = st.sidebar.multiselect(
        "Select Output Sections:",
        all_options,
        default=["Summary", "Difficulty", "Execution Flow"],
    )
else:
    selected_views = preset_map[preset_mode]

st.sidebar.markdown("### 🧪 Sample Code")
selected_sample = st.sidebar.selectbox(
    "Choose example:",
    ["None"] + list(sample_codes.keys())
)

st.sidebar.markdown("### 🎛️ UI Settings")
show_line_map = st.sidebar.checkbox("Show Line Numbers", value=False)
show_footer = st.sidebar.checkbox("Show Footer", value=True)

st.sidebar.markdown("### 📌 Current Selection")
st.sidebar.write(f"Sections selected: {len(selected_views)}")
for item in selected_views:
    st.sidebar.markdown(f"- {item}")

# ---------------- INPUT ----------------
default_code = sample_codes[selected_sample] if selected_sample != "None" else ""

code = st.text_area(
    "Enter your Python code here:",
    value=default_code,
    height=260,
    placeholder="Example:\nfor i in range(3):\n    print(i)"
)

# ---------------- ANALYZE ----------------
if st.button("Explain Code", use_container_width=True):
    if not code.strip():
        st.warning("Please write or paste some Python code first.")
    else:
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
        st.subheader("✅ Analysis Result")

        if not result.get("success"):
            st.error(result.get("error", "Unknown error occurred."))
        else:
            st.success("Code analyzed successfully.")

            metrics = result.get("metrics", {})
            explanations = result.get("explanations", [])
            categories = result.get("categories", {})
            execution_flow = result.get("execution_flow", [])
            timeline = result.get("timeline", {})
            flowchart_source = result.get("flowchart", "")

            # ---------------- LAYOUT ----------------
            left_col, right_col = st.columns([1, 1.35], gap="large")

            with left_col:
                st.markdown("### 📄 Code")
                st.code(code, language="python")

                if show_line_map:
                    st.markdown("### 🔢 Code With Line Numbers")
                    numbered_lines = []
                    for i, line in enumerate(code.splitlines(), start=1):
                        numbered_lines.append(f"{str(i).rjust(3)} | {line}")
                    st.text("\n".join(numbered_lines))

            with right_col:
                if view_mode == "Focused":
                    tab1, tab2 = st.tabs(["📊 Overview", "🔄 Execution"])

                    with tab1:
                        if "Summary" in selected_views:
                            st.markdown("### 🧾 Summary")
                            st.write(result.get("summary", "No summary available."))

                        if "Difficulty" in selected_views:
                            st.markdown("### 🎯 Difficulty")
                            st.success(result.get("difficulty", "Unknown"))

                        if "All Explanations" in selected_views:
                            with st.expander("📝 Explanations", expanded=True):
                                for item in explanations:
                                    st.markdown(f"- {item}")

                    with tab2:
                        if "Execution Flow" in selected_views:
                            with st.expander("🔄 Execution Flow", expanded=True):
                                for step in execution_flow:
                                    st.markdown(f"- {step}")

                        if "Variable Timeline" in selected_views:
                            with st.expander("📊 Variable Timeline", expanded=False):
                                if not timeline:
                                    st.info("No variable changes recorded.")
                                else:
                                    for var, steps in timeline.items():
                                        with st.expander(f"Variable: {var}", expanded=False):
                                            for step in steps:
                                                st.markdown(f"- {step}")

                else:
                    tab1, tab2, tab3, tab4 = st.tabs(
                        ["📊 Overview", "🧠 Explanation", "🔄 Execution", "📈 Advanced"]
                    )

                    with tab1:
                        if "Summary" in selected_views or "Difficulty" in selected_views:
                            c1, c2 = st.columns(2)

                            with c1:
                                if "Summary" in selected_views:
                                    st.markdown("### 🧾 Summary")
                                    st.write(result.get("summary", "No summary available."))

                            with c2:
                                if "Difficulty" in selected_views:
                                    st.markdown("### 🎯 Difficulty")
                                    st.success(result.get("difficulty", "Unknown"))

                        if "Metrics" in selected_views:
                            st.markdown("### 📊 Metrics")
                            c1, c2, c3 = st.columns(3)
                            c1.metric("Lines", metrics.get("total_lines", 0))
                            c2.metric("Functions", metrics.get("functions", 0))
                            c3.metric("Loops", metrics.get("loops", 0))

                            c4, c5, c6 = st.columns(3)
                            c4.metric("Conditions", metrics.get("conditions", 0))
                            c5.metric("Assignments", metrics.get("assignments", 0))
                            c6.metric("Imports", metrics.get("imports", 0))

                    with tab2:
                        if "All Explanations" in selected_views:
                            with st.expander("📝 All Explanations", expanded=True):
                                for item in explanations:
                                    st.markdown(f"- {item}")

                        if "Categories" in selected_views:
                            for category, items in categories.items():
                                if items:
                                    with st.expander(f"📁 {category}", expanded=False):
                                        for item in items:
                                            st.markdown(f"- {item}")

                    with tab3:
                        if "Execution Flow" in selected_views:
                            with st.expander("🔄 Execution Flow", expanded=True):
                                for step in execution_flow:
                                    st.markdown(f"- {step}")

                        if "Variable Timeline" in selected_views:
                            with st.expander("📊 Variable Timeline", expanded=True):
                                if not timeline:
                                    st.info("No variable changes recorded.")
                                else:
                                    for var, steps in timeline.items():
                                        with st.expander(f"Variable: {var}", expanded=False):
                                            for step in steps:
                                                st.markdown(f"- {step}")

                    with tab4:
                        if "Flow Diagram" in selected_views:
                            st.markdown("### 🧭 Code Flow Diagram")
                            if flowchart_source:
                                st.graphviz_chart(flowchart_source)
                            else:
                                st.info("No flowchart available.")

                        if "Raw API Response" in selected_views:
                            with st.expander("🔍 View Raw API Response", expanded=False):
                                st.json(result)

            # ---------------- EXPORT ----------------
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
            for item in explanations:
                report_lines.append(f"- {item}")
            report_lines.append("")

            report_lines.append("Execution Flow:")
            for step in execution_flow:
                report_lines.append(f"- {step}")
            report_lines.append("")

            report_lines.append("Variable Timeline:")
            if timeline:
                for var, steps in timeline.items():
                    report_lines.append(f"{var}:")
                    for step in steps:
                        report_lines.append(f"  - {step}")
            else:
                report_lines.append("No variable changes recorded.")
            report_lines.append("")

            report_lines.append("Flowchart Source:")
            report_lines.append(flowchart_source)

            report_text = "\n".join(report_lines)

            c1, c2 = st.columns(2)
            with c1:
                st.download_button(
                    "📄 Download Report (.txt)",
                    data=report_text,
                    file_name="code_explanation_report.txt",
                    mime="text/plain",
                    use_container_width=True
                )

            with c2:
                st.download_button(
                    "📦 Download JSON",
                    data=json.dumps(result, indent=2),
                    file_name="code_explanation.json",
                    mime="application/json",
                    use_container_width=True
                )

# ---------------- FOOTER ----------------
if show_footer:
    st.divider()
    st.caption("🚀 Python Code Explainer | Built with FastAPI + Streamlit")