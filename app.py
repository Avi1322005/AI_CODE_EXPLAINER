import streamlit as st
import ast


# function definition section
def check_errors(code):
    """
    Checks whether the code has syntax errors.
    Returns None if valid, else returns an error message.
    """
    try:
        ast.parse(code)
        return None
    except IndentationError as e:
        return f"Indentation error: {e}"
    except SyntaxError as e:
        return f"Syntax error: {e}"


# rule-based analyzer
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

        elif line.startswith("if "):
            explanations.append(f"Line {i}: This line checks a condition using an if statement.")

        elif line.startswith("def "):
            explanations.append(f"Line {i}: This line defines a function.")

        elif "=" in line and "==" not in line:
            explanations.append(f"Line {i}: This line assigns a value to a variable.")

        elif line.startswith("return"):
            explanations.append(f"Line {i}: This line returns a value from a function.")

    if not explanations:
        return ["I could not match this code to my current rule set yet."]

    return explanations


# AST-based analyzer
def analyze_ast(code):
    explanations = []
    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if len(node.targets) > 0 and isinstance(node.targets[0], ast.Name):
                variable_name = node.targets[0].id
                value = ast.unparse(node.value)
                explanations.append(f"Variable '{variable_name}' is assigned the value {value}.")

        elif isinstance(node, ast.For):
            loop_variable = ast.unparse(node.target)
            loop_range = ast.unparse(node.iter)
            explanations.append(f"A for loop uses variable '{loop_variable}' to iterate over {loop_range}.")

        elif isinstance(node, ast.If):
            condition = ast.unparse(node.test)
            explanations.append(f"An if statement checks the condition: {condition}.")

        elif isinstance(node, ast.FunctionDef):
            function_name = node.name
            explanations.append(f"A function named '{function_name}' is defined.")

        elif isinstance(node, ast.Return):
            return_value = ast.unparse(node.value) if node.value else "nothing"
            explanations.append(f"This function returns {return_value}.")

    if not explanations:
        return ["No recognizable Python structures found."]

    unique_explanations = []
    for item in explanations:
        if item not in unique_explanations:
            unique_explanations.append(item)

    return unique_explanations


st.title("PYTHON CODE EXPLAINER")
st.write("Paste or write your Python code below.")

code = st.text_area("Enter your code here", height=200)

if st.button("Explain code"):
    if code.strip() == "":
        st.warning("No code written/pasted.")
    else:
        st.subheader("Your code:")
        st.code(code, language="python")

        error = check_errors(code)

        st.subheader("Explanation")
        if error:
            st.error(error)
        else:
            explanation = analyze_ast(code)

            for line in explanation:
                st.markdown(f"- {line}")