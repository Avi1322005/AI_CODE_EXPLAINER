import streamlit as st
import ast


# function definition section
def check_errors(code):
    """
    checks whether the code has syntax errors 
    returns NONE if valid else returns error message
    """
    try:
        ast.parse(code)
        return None
    except IndentationError as e:
        return f"indentation error: {e}"
    except SyntaxError as e:
        return f"syntax error: {e}"
#rule based analyzer
def code_explain(code):
    explanations = []
    lines = code.split("\n")
    for i, line in enumerate(lines , start=1):
        line = line.strip()
        if line == "":
         continue
        if line.startswith("print("):
            explanations.append(f"Line {i}: This line prints output to the screen.\n")

        elif line.startswith("for "):
            explanations.append(f"Line {i}: This line starts a for loop.\n")

        elif line.startswith("if "):
            explanations.append(f"Line {i}: This line checks a condition using an if statement.\n")

        elif line.startswith("def "):
            explanations.append(f"Line {i}: This line defines a function.\n")

        elif "=" in line and "==" not in line:
           explanations.append(f"Line {i}: This line assigns a value to a variable.\n")

        elif line.startswith("return"):
            explanations.append(f"Line {i}: This line returns a value from a function.\n")

    if not explanations:
        return "I could not match this code to my current rule set yet.\n"
    
    return "\n".join(explanations)
#using AST abstract syntax tree
def analyze_ast(code):
    explanations = []
    tree = ast.parse(code)
    for node in ast.walk(tree):
         if isinstance(node , ast.Assign):
            explanations.append("this code  assigns a value to variable\n")
         elif isinstance(node, ast.For):
            explanations.append("This code contains a for loop.\n")

         elif isinstance(node, ast.If):
            explanations.append("This code contains a conditional if statement.\n")

         elif isinstance(node, ast.FunctionDef):
            explanations.append("This code defines a function.\n")

         elif isinstance(node, ast.Return):
            explanations.append("This code returns a value from a function.\n")

    if not explanations:
        return "No recognizable Python structures found."

    return "\n".join(set(explanations))
st.title("RULE BASED CODE EXPLAINER")
st.write("Paste/Write your python code below")

code = st.text_area("Enter your code here", height=200)
if st.button("explain code"):
    if(code.strip() == ""):
        st.warning("NO CODE WRITTEN/PASTED")
    else:
        st.subheader("your code:")
        st.code(code , language="python")

        error = check_errors(code)

        st.subheader("EXPLAINATION")
        if error:
            st.error(error)
        else:
            explanation = analyze_ast(code)
            st.write(explanation)