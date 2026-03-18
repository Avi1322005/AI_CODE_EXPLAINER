# 🧠 Python Code Explainer

A beginner-friendly web app that explains Python code using **rule-based analysis + AST (Abstract Syntax Tree)** and simulates **execution flow step-by-step**.

Built using **Streamlit**, this project helps users understand how Python code works in a simple and human-readable way.

---

## 🚀 Features

### ✅ Code Explanation
- Explains Python code line-by-line
- Uses both:
  - Rule-based logic
  - AST-based structural analysis

---

### 🧩 Categorized Output
Explanations are grouped into sections:

- 📦 Variables  
- 🔁 Loops  
- 🔀 Conditions  
- 🧠 Functions  
- 📥📤 Input / Output  

---

### 🔄 Execution Flow (NEW 🔥)
Simulates how the code runs step-by-step:
Step 1: Variable 'a' is set to 10
Step 2: Loop starts
Step 3: 'i' becomes 0
Step 4: The program prints 0

### 📊 Variable Timeline (NEW 🔥)
Tracks how variables change during execution:

Example:
x:
- Step 1: 5
- Step 2: 7

---

### 🧠 Smart Human-Friendly Explanations
- Converts conditions into English  
  → `i > 2` → *"i is greater than 2"*  
- Explains loops clearly  
  → `range(3)` → *"repeats 3 times"*  
- Smarter print explanations  
  → `print(i)` → *"displays the current value of i"*  

---

### ⚠️ Error Detection
- Detects:
  - Syntax errors
  - Indentation errors  
- Prevents analysis if code is invalid

---

### 💻 Clean UI (Streamlit)
- Code input box
- Syntax highlighting
- Section-based output
- Success + error messages

---
### 📈 Code Metrics & Summary (NEW)
- Total lines
- Functions
- Loops
- Conditions
- Assignments
- Imports

Also generates a simple summary of the code.

---

### 🎯 Difficulty Estimation (NEW)
Automatically classifies code as:
- Beginner
- Intermediate
- Advanced

## 🛠️ Tech Stack

- Python
- FastAPI
- Streamlit
- AST (Abstract Syntax Tree)bstract Syntax Tree)

---

## 📂 Project Structure

python-code-explainer/
│
├── app.py            # FastAPI backend
├── api.py            # Core logic (AST + execution engine)
├── dashboard.py      # Streamlit UI
├── requirements.txt
└── README.md

---

## ▶️ How to Run

### 1. Clone the repository

```bash
git clone https://github.com/your-username/python-code-explainer.git
cd python-code-explainer
```

### 2. Install dependencies
   
```bash
pip install streamlit
```
### 3. Run the app
# Start backend
uvicorn app:app --reload

# Start dashboard
streamlit run dashboard.py

# 🧪 Example Input
```bash
a = 10
for i in range(3):
    print(i)
if a < 10:
    print(a)
else:
    print(10)
```


# 📌 Example Output
🔁 Loops
This loop repeats 3 times using the variable 'i'

🔀 Conditions
This condition checks whether a is less than 10

🔄 Execution Flow
Step 1: Variable 'a' is set to 10  
Step 2: Loop starts  
Step 3: 'i' becomes 0  
Step 4: The program prints 0  
...
### 📊 Variable Timeline

x:
- Step 1: 5
- Step 2: 7

# 🧭 Project Roadmap
## ✅ Completed
Code metrics + summary
Difficulty estimation
Variable timeline tracking

## 🚧 In Progress
📂 File upload support
📌 Code summary section

## ⚠️ Limitations

- Supports beginner to intermediate Python code
- Does not fully execute complex libraries or classes
- While loops are limited to prevent infinite execution
- Safe evaluation avoids running unsafe code

## 🔮 Future Improvements
🌐 Multi-language support (JavaScript, C++, Java)
🤖 AI-powered explanations
📊 Code complexity analysis
🌍 Deployment (Streamlit Cloud)


# 🎯 Purpose
This project is designed for:
Beginners learning Python
Students understanding code logic
Visual learners who benefit from step-by-step execution

### 👨‍💻 Author
Gaurav Kumar Pandey

