import streamlit as st
import ast


# Check syntax and indentation errors
def check_errors(code):
    """
    Checks whether the code has syntax errors.
    Returns None if valid else returns error message.
    """
    try:
        ast.parse(code)
        return None
    except IndentationError as e:
        return f"Indentation error: {e}"
    except SyntaxError as e:
        return f"Syntax error: {e}"


# Rule-based analyzer
def code_explain(code):
    explanations = []
    lines = code.split("\n")

    for i, line in enumerate(lines, start=1):
        line = line.strip()

        if line == "":
            continue

        if line.startswith("print("):
            explanations.append(f"Line {i}: This line prints output to the screen.")

        elif line.startswith("for "):
            explanations.append(f"Line {i}: This line starts a for loop.")

        elif line.startswith("while "):
            explanations.append(f"Line {i}: This line starts a while loop.")

        elif line.startswith("if "):
            explanations.append(f"Line {i}: This line checks a condition using an if statement.")

        elif line.startswith("else"):
            explanations.append(f"Line {i}: This line defines an else block.")

        elif line.startswith("def "):
            explanations.append(f"Line {i}: This line defines a function.")

        elif line.startswith("return"):
            explanations.append(f"Line {i}: This line returns a value from a function.")

        elif "input(" in line:
            explanations.append(f"Line {i}: This line takes input from the user.")

        elif "=" in line and "==" not in line and ">=" not in line and "<=" not in line and "!=" not in line:
            explanations.append(f"Line {i}: This line assigns a value to a variable.")

    if not explanations:
        return ["I could not match this code to my current rule set yet."]

    return explanations

def get_node_value(node):
    """
    Try to convert simple AST nodes into readable values.
    """
    try:
        return ast.literal_eval(node)
    except Exception:
        return ast.unparse(node)

# to define lines in english

def explain_condition(condition_text):
    """
    Converts simple Python conditions into more human-friendly English.
    """
    condition_text = condition_text.replace("==", " is equal to ")
    condition_text = condition_text.replace("!=", " is not equal to ")
    condition_text = condition_text.replace(">=", " is greater than or equal to ")
    condition_text = condition_text.replace("<=", " is less than or equal to ")
    condition_text = condition_text.replace(">", " is greater than ")
    condition_text = condition_text.replace("<", " is less than ")
    return condition_text

# Making loops more friendly

def explain_range(iter_node):
    """
    Converts range(...) into a more human-friendly explanation.
    """
    if isinstance(iter_node, ast.Call) and hasattr(iter_node.func, "id") and iter_node.func.id == "range":
        args = iter_node.args

        if len(args) == 1:
            stop = ast.unparse(args[0])
            return f"repeats {stop} times"

        elif len(args) == 2:
            start = ast.unparse(args[0])
            stop = ast.unparse(args[1])
            return f"repeats from {start} to {stop} (excluding {stop})"

        elif len(args) == 3:
            start = ast.unparse(args[0])
            stop = ast.unparse(args[1])
            step = ast.unparse(args[2])
            return f"repeats from {start} to {stop} (excluding {stop}) in steps of {step}"

    return f"goes through values in {ast.unparse(iter_node)}"

# helper function to define what is printing

def explain_print(args):
    """
    Converts print() arguments into a more human-friendly explanation.
    """
    if len(args) == 1:
        arg = args[0]

        # If it's a string
        if arg.startswith('"') or arg.startswith("'"):
            return f'This displays the text {arg}.'

        # Otherwise variable or expression
        return f'This displays the current value of {arg}.'

    else:
        return f"This displays multiple values: {', '.join(args)}."

# AST-based analyzer
def analyze_ast(code):
    explanations = []
    tree = ast.parse(code)

    for node in ast.walk(tree):

        # Variable assignment
        if isinstance(node, ast.Assign):
            if isinstance(node.targets[0], ast.Name):
                var_name = node.targets[0].id
                line_no = node.lineno

                if (
                    isinstance(node.value, ast.Call)
                    and hasattr(node.value.func, "id")
                    and node.value.func.id == "input"
                ):
                    prompt = ast.unparse(node.value.args[0]) if node.value.args else ""
                    explanations.append(
                        f"Line {line_no}: The program takes input from the user with the prompt {prompt}."
                    )
                else:
                    value = ast.unparse(node.value)
                    explanations.append(
                        f"Line {line_no}: The variable '{var_name}' is given the value {value}."
                    )

        # For loop
        elif isinstance(node, ast.For):
            line_no = node.lineno
            loop_var = ast.unparse(node.target)
            loop_explanation = explain_range(node.iter)

            explanations.append(
                f"Line {line_no}: This loop {loop_explanation} using the variable '{loop_var}'."
            )

        # While loop
        elif isinstance(node, ast.While):
            line_no = node.lineno
            condition = explain_condition(ast.unparse(node.test))
            explanations.append(
                f"Line {line_no}: This while loop keeps running while {condition}."
            )

        # If condition
        elif isinstance(node, ast.If):
            line_no = node.lineno
            condition = explain_condition(ast.unparse(node.test))
            explanations.append(
                f"Line {line_no}: This condition checks whether {condition}."
            )

            if node.orelse:
                explanations.append(
                    f"Line {line_no}: If the condition is false, the else block will run."
                )

        # Function definition
        elif isinstance(node, ast.FunctionDef):
            line_no = node.lineno
            params = [arg.arg for arg in node.args.args]

            if params:
                if len(params) == 1:
                    explanations.append(
                        f"Line {line_no}: A function named '{node.name}' is defined. It takes one parameter: {params[0]}."
                    )
                else:
                    param_text = ", ".join(params)
                    explanations.append(
                        f"Line {line_no}: A function named '{node.name}' is defined. It takes these parameters: {param_text}."
                    )
            else:
                explanations.append(
                    f"Line {line_no}: A function named '{node.name}' is defined. It takes no parameters."
                )

        # Return statement
        elif isinstance(node, ast.Return):
            line_no = node.lineno
            value = ast.unparse(node.value) if node.value else "nothing"
            explanations.append(
                f"Line {line_no}: This function returns {value}."
            )

        # Print detection
        elif isinstance(node, ast.Expr):
          if isinstance(node.value, ast.Call):
           if hasattr(node.value.func, "id") and node.value.func.id == "print":
            line_no = node.lineno
            args = [ast.unparse(arg) for arg in node.value.args]

            explanation = explain_print(args)

            explanations.append(
                f"Line {line_no}: {explanation}"
            )

    if not explanations:
        return ["No recognizable Python structures found."]

    unique = []
    for e in explanations:
        if e not in unique:
            unique.append(e)

    return unique


# Hybrid final explanation
def generate_final_explanation(code):
    rule_explanations = code_explain(code)
    ast_explanations = analyze_ast(code)

    final_explanations = []

    for explanation in ast_explanations:
        if explanation not in final_explanations:
            final_explanations.append(explanation)

    for explanation in rule_explanations:
        already_covered = False

        for ast_exp in ast_explanations:
            if (
                "for loop" in explanation.lower() and "for loop" in ast_exp.lower()
            ) or (
                "if statement" in explanation.lower() and "if statement" in ast_exp.lower()
            ) or (
                "function" in explanation.lower() and "function" in ast_exp.lower()
            ) or (
                "returns" in explanation.lower() and "returns" in ast_exp.lower()
            ) or (
                "assigns a value" in explanation.lower() and "assigned the value" in ast_exp.lower()
            ) or (
                "prints output" in explanation.lower() and "print statement outputs" in ast_exp.lower()
            ) or (
                "input" in explanation.lower() and "input is taken" in ast_exp.lower()
            ) or (
                "else block" in explanation.lower() and "else block" in ast_exp.lower()
            ) or (
                "while loop" in explanation.lower() and "while loop" in ast_exp.lower()
            ):
                already_covered = True
                break

        if not already_covered and explanation not in final_explanations:
            final_explanations.append(explanation)

    return final_explanations


# Categorize explanations
def categorize_explanations(explanations):
    categories = {
        "Variables": [],
        "Loops": [],
        "Conditions": [],
        "Functions": [],
        "Input / Output": [],
        "Other": []
    }

    for explanation in explanations:
        lower_exp = explanation.lower()

        if "assigned the value" in lower_exp or "assigns a value" in lower_exp:
            categories["Variables"].append(explanation)

        elif "for loop" in lower_exp or "while loop" in lower_exp:
            categories["Loops"].append(explanation)

        elif "if statement" in lower_exp or "else block" in lower_exp:
            categories["Conditions"].append(explanation)

        elif "function named" in lower_exp or "defines a function" in lower_exp or "returns" in lower_exp:
            categories["Functions"].append(explanation)

        elif "print statement" in lower_exp or "prints output" in lower_exp or "input is taken" in lower_exp or "takes input" in lower_exp:
            categories["Input / Output"].append(explanation)

        else:
            categories["Other"].append(explanation)

    return categories
def generate_execution_flow(code):
    """
    Generates a simple beginner-friendly execution flow for basic Python code.
    """
    flow_steps = []
    tree = ast.parse(code)
    step_number = 1

    for node in tree.body:

        # Assignment
        if isinstance(node, ast.Assign):
            if isinstance(node.targets[0], ast.Name):
                var_name = node.targets[0].id
                value = get_node_value(node.value)
                flow_steps.append(f"Step {step_number}: Variable '{var_name}' is set to {value}.")
                step_number += 1

        # Print statement
        elif isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Call):
                if hasattr(node.value.func, "id") and node.value.func.id == "print":
                    args = [ast.unparse(arg) for arg in node.value.args]
                    flow_steps.append(f"Step {step_number}: The program prints {', '.join(args)}.")
                    step_number += 1

        # For loop
        elif isinstance(node, ast.For):
            loop_var = ast.unparse(node.target)

            # Handle range(...)
            if (
                isinstance(node.iter, ast.Call)
                and hasattr(node.iter.func, "id")
                and node.iter.func.id == "range"
            ):
                args = node.iter.args

                if len(args) == 1:
                    start = 0
                    stop = get_node_value(args[0])
                    step = 1
                elif len(args) == 2:
                    start = get_node_value(args[0])
                    stop = get_node_value(args[1])
                    step = 1
                elif len(args) == 3:
                    start = get_node_value(args[0])
                    stop = get_node_value(args[1])
                    step = get_node_value(args[2])
                else:
                    start, stop, step = 0, 0, 1

                flow_steps.append(f"Step {step_number}: A loop starts.")
                step_number += 1

                try:
                    for value in range(int(start), int(stop), int(step)):
                        flow_steps.append(f"Step {step_number}: '{loop_var}' becomes {value}.")
                        step_number += 1

                        for inner_node in node.body:
                            if isinstance(inner_node, ast.Expr):
                                if isinstance(inner_node.value, ast.Call):
                                    if hasattr(inner_node.value.func, "id") and inner_node.value.func.id == "print":
                                        args = [ast.unparse(arg) for arg in inner_node.value.args]
                                        rendered_args = [str(value) if arg == loop_var else arg for arg in args]
                                        flow_steps.append(
                                            f"Step {step_number}: The program prints {', '.join(rendered_args)}."
                                        )
                                        step_number += 1
                except Exception:
                    flow_steps.append(f"Step {step_number}: The loop runs, but exact values could not be simulated.")
                    step_number += 1

        # If statement
        elif isinstance(node, ast.If):
            condition_text = ast.unparse(node.test)
            flow_steps.append(f"Step {step_number}: The program checks whether {explain_condition(condition_text)}.")
            step_number += 1

            # Try to evaluate very simple conditions using known constants from earlier assignments
            env = {}
            for prev in tree.body:
                if prev == node:
                    break
                if isinstance(prev, ast.Assign) and isinstance(prev.targets[0], ast.Name):
                    try:
                        env[prev.targets[0].id] = ast.literal_eval(prev.value)
                    except Exception:
                        pass

            try:
                condition_result = eval(condition_text, {}, env)

                if condition_result:
                    flow_steps.append(f"Step {step_number}: The condition is true, so the if block runs.")
                    step_number += 1

                    for inner_node in node.body:
                        if isinstance(inner_node, ast.Expr):
                            if isinstance(inner_node.value, ast.Call):
                                if hasattr(inner_node.value.func, "id") and inner_node.value.func.id == "print":
                                    args = [ast.unparse(arg) for arg in inner_node.value.args]
                                    resolved = [str(env[arg]) if arg in env else arg for arg in args]
                                    flow_steps.append(
                                        f"Step {step_number}: The program prints {', '.join(resolved)}."
                                    )
                                    step_number += 1
                else:
                    flow_steps.append(f"Step {step_number}: The condition is false, so the else block runs.")
                    step_number += 1

                    for inner_node in node.orelse:
                        if isinstance(inner_node, ast.Expr):
                            if isinstance(inner_node.value, ast.Call):
                                if hasattr(inner_node.value.func, "id") and inner_node.value.func.id == "print":
                                    args = [ast.unparse(arg) for arg in inner_node.value.args]
                                    resolved = [str(env[arg]) if arg in env else arg for arg in args]
                                    flow_steps.append(
                                        f"Step {step_number}: The program prints {', '.join(resolved)}."
                                    )
                                    step_number += 1

            except Exception:
                flow_steps.append(f"Step {step_number}: The condition could not be fully evaluated.")
                step_number += 1

    if not flow_steps:
        return ["No execution flow could be generated for this code."]

    return flow_steps

# ---------------- UI ----------------

st.set_page_config(page_title="Python Code Explainer", page_icon="🧠", layout="centered")

st.title("🧠 Python Code Explainer")
st.caption("A beginner-friendly tool that explains Python code using rule-based logic and AST analysis.")

st.info(
    "Paste your Python code below and click **Explain Code**. "
    "The app checks syntax, analyzes code structure, and gives a simplified explanation."
)

code = st.text_area(
    "Enter your Python code here:",
    height=250,
    placeholder="Example:\nfor i in range(3):\n    print(i)"
)

if st.button("Explain Code"):
    if code.strip() == "":
        st.warning("Please write or paste some Python code first.")
    else:
        st.divider()

        st.subheader("📄 Your Code")
        st.code(code, language="python")

        error = check_errors(code)

        st.divider()

        st.subheader("✅ Final Explanation")
        if error:
            st.error(error)
        else:
            final_explanations = generate_final_explanation(code)
            categorized = categorize_explanations(final_explanations)

            st.success("Code analyzed successfully.")

            for category, items in categorized.items():
                if items:
                    st.markdown(f"### {category}")
                    for item in items:
                        st.markdown(f"- {item}")
                        st.divider()
            st.subheader("🔄 Execution Flow")

            flow_steps = generate_execution_flow(code)

            for step in flow_steps:
                st.markdown(f"- {step}")