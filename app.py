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

def code_explain(code):
    explanations = []
    if "print(" in code:
        explanations.append("This code uses print() to display output on the screen.")

    if "for " in code and "range(" in code:
        explanations.append("This code uses a for loop with range() to repeat some steps a fixed number of times.")

    if "if" in code:
        explanations.append("This code uses an if statement to make a decision based on a condition.")

    if "def " in code:
        explanations.append("This code defines a function using the def keyword.")

    if "=" in code and "==" not in code:
        explanations.append("This code may be storing a value inside a variable using =.")

    if not explanations:
        return "I could not match this code to my current rule set yet."
    
    return "\n".join(explanations)

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
            explanation = code_explain(code)
            st.write(explanation)