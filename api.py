import ast


def record_variable(timeline, var_name, value, step_number):
    if var_name not in timeline:
        timeline[var_name] = []
    timeline[var_name].append(f"Step {step_number}: {value}")


def check_errors(code: str):
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


def safe_unparse(node):
    """
    Safely convert AST node back to source-like text.
    """
    try:
        return ast.unparse(node)
    except Exception:
        return str(node)


def get_node_value(node):
    """
    Try to convert simple AST nodes into readable values.
    """
    try:
        return ast.literal_eval(node)
    except Exception:
        return safe_unparse(node)


def explain_condition(condition_text: str):
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


def explain_range(iter_node):
    """
    Converts range(...) into a more human-friendly explanation.
    """
    if (
        isinstance(iter_node, ast.Call)
        and hasattr(iter_node.func, "id")
        and iter_node.func.id == "range"
    ):
        args = iter_node.args

        if len(args) == 1:
            stop = safe_unparse(args[0])
            return f"repeats {stop} times"
        elif len(args) == 2:
            start = safe_unparse(args[0])
            stop = safe_unparse(args[1])
            return f"repeats from {start} to {stop} (excluding {stop})"
        elif len(args) == 3:
            start = safe_unparse(args[0])
            stop = safe_unparse(args[1])
            step = safe_unparse(args[2])
            return f"repeats from {start} to {stop} (excluding {stop}) in steps of {step}"

    return f"goes through values in {safe_unparse(iter_node)}"


def explain_print(args):
    """
    Converts print() arguments into a more human-friendly explanation.
    """
    if len(args) == 1:
        arg = args[0]
        if arg.startswith('"') or arg.startswith("'"):
            return f"This displays the text {arg}."
        return f"This displays the current value of {arg}."
    return f"This displays multiple values: {', '.join(args)}."


def code_explain(code: str):
    explanations = []
    lines = code.split("\n")

    for i, line in enumerate(lines, start=1):
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("print("):
            explanations.append(f"Line {i}: This line prints output to the screen.")
        elif stripped.startswith("for "):
            explanations.append(f"Line {i}: This line starts a for loop.")
        elif stripped.startswith("while "):
            explanations.append(f"Line {i}: This line starts a while loop.")
        elif stripped.startswith("if "):
            explanations.append(
                f"Line {i}: This line checks a condition using an if statement."
            )
        elif stripped.startswith("elif "):
            explanations.append(
                f"Line {i}: This line checks another condition using an elif statement."
            )
        elif stripped.startswith("else"):
            explanations.append(f"Line {i}: This line defines an else block.")
        elif stripped.startswith("def "):
            explanations.append(f"Line {i}: This line defines a function.")
        elif stripped.startswith("return"):
            explanations.append(f"Line {i}: This line returns a value from a function.")
        elif stripped.startswith("import ") or stripped.startswith("from "):
            explanations.append(
                f"Line {i}: This line imports a module or specific functionality."
            )
        elif "input(" in stripped:
            explanations.append(f"Line {i}: This line takes input from the user.")
        elif "+=" in stripped or "-=" in stripped or "*=" in stripped or "/=" in stripped:
            explanations.append(
                f"Line {i}: This line updates a variable using an augmented assignment."
            )
        elif (
            "=" in stripped
            and "==" not in stripped
            and ">=" not in stripped
            and "<=" not in stripped
            and "!=" not in stripped
        ):
            explanations.append(f"Line {i}: This line assigns a value to a variable.")

    if not explanations:
        return ["I could not match this code to my current rule set yet."]

    return explanations


def analyze_ast(code: str):
    explanations = []
    tree = ast.parse(code)

    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            if isinstance(node.targets[0], ast.Name):
                var_name = node.targets[0].id
                line_no = node.lineno

                if (
                    isinstance(node.value, ast.Call)
                    and hasattr(node.value.func, "id")
                    and node.value.func.id == "input"
                ):
                    prompt = safe_unparse(node.value.args[0]) if node.value.args else ""
                    explanations.append(
                        f"Line {line_no}: The program takes input from the user with the prompt {prompt}."
                    )
                else:
                    value = safe_unparse(node.value)
                    explanations.append(
                        f"Line {line_no}: The variable '{var_name}' is given the value {value}."
                    )

        elif isinstance(node, ast.AugAssign):
            line_no = node.lineno
            target = safe_unparse(node.target)
            value = safe_unparse(node.value)
            op_name = type(node.op).__name__
            explanations.append(
                f"Line {line_no}: The variable '{target}' is updated using {op_name} with {value}."
            )

        elif isinstance(node, ast.For):
            line_no = node.lineno
            loop_var = safe_unparse(node.target)
            loop_explanation = explain_range(node.iter)
            explanations.append(
                f"Line {line_no}: This loop {loop_explanation} using the variable '{loop_var}'."
            )

        elif isinstance(node, ast.While):
            line_no = node.lineno
            condition = explain_condition(safe_unparse(node.test))
            explanations.append(
                f"Line {line_no}: This while loop keeps running while {condition}."
            )

        elif isinstance(node, ast.If):
            line_no = node.lineno
            condition = explain_condition(safe_unparse(node.test))
            explanations.append(
                f"Line {line_no}: This condition checks whether {condition}."
            )

            if node.orelse:
                explanations.append(
                    f"Line {line_no}: If the condition is false, the else block will run."
                )

        elif isinstance(node, ast.FunctionDef):
            line_no = node.lineno
            params = [arg.arg for arg in node.args.args]

            if params:
                if len(params) == 1:
                    explanations.append(
                        f"Line {line_no}: A function named '{node.name}' is defined. It takes one parameter: {params[0]}."
                    )
                else:
                    explanations.append(
                        f"Line {line_no}: A function named '{node.name}' is defined. It takes these parameters: {', '.join(params)}."
                    )
            else:
                explanations.append(
                    f"Line {line_no}: A function named '{node.name}' is defined. It takes no parameters."
                )

        elif isinstance(node, ast.Return):
            line_no = node.lineno
            value = safe_unparse(node.value) if node.value else "nothing"
            explanations.append(f"Line {line_no}: This function returns {value}.")

        elif isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Call):
                if hasattr(node.value.func, "id") and node.value.func.id == "print":
                    line_no = node.lineno
                    args = [safe_unparse(arg) for arg in node.value.args]
                    explanations.append(f"Line {line_no}: {explain_print(args)}")

        elif isinstance(node, ast.Import):
            line_no = node.lineno
            modules = ", ".join(alias.name for alias in node.names)
            explanations.append(f"Line {line_no}: This imports the module(s): {modules}.")

        elif isinstance(node, ast.ImportFrom):
            line_no = node.lineno
            module = node.module if node.module else "unknown module"
            names = ", ".join(alias.name for alias in node.names)
            explanations.append(f"Line {line_no}: This imports {names} from {module}.")

    if not explanations:
        return ["No recognizable Python structures found."]

    unique = []
    for e in explanations:
        if e not in unique:
            unique.append(e)

    return unique


def generate_final_explanation(code: str):
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
                ("for loop" in explanation.lower() and "loop" in ast_exp.lower())
                or ("if statement" in explanation.lower() and "condition" in ast_exp.lower())
                or ("elif" in explanation.lower() and "condition" in ast_exp.lower())
                or ("function" in explanation.lower() and "function" in ast_exp.lower())
                or ("returns" in explanation.lower() and "returns" in ast_exp.lower())
                or ("assigns a value" in explanation.lower() and "given the value" in ast_exp.lower())
                or ("prints output" in explanation.lower() and "displays" in ast_exp.lower())
                or ("input" in explanation.lower() and "takes input" in ast_exp.lower())
                or ("else block" in explanation.lower() and "else block" in ast_exp.lower())
                or ("while loop" in explanation.lower() and "while loop" in ast_exp.lower())
                or ("imports" in explanation.lower() and "imports" in ast_exp.lower())
            ):
                already_covered = True
                break

        if not already_covered and explanation not in final_explanations:
            final_explanations.append(explanation)

    return final_explanations


def categorize_explanations(explanations):
    categories = {
        "Variables": [],
        "Loops": [],
        "Conditions": [],
        "Functions": [],
        "Input / Output": [],
        "Imports": [],
        "Other": [],
    }

    for explanation in explanations:
        lower_exp = explanation.lower()

        if "given the value" in lower_exp or "assigns a value" in lower_exp or "updated using" in lower_exp:
            categories["Variables"].append(explanation)
        elif "loop" in lower_exp:
            categories["Loops"].append(explanation)
        elif "condition checks" in lower_exp or "else block" in lower_exp or "while loop keeps running" in lower_exp:
            categories["Conditions"].append(explanation)
        elif "function named" in lower_exp or "defines a function" in lower_exp or "returns" in lower_exp:
            categories["Functions"].append(explanation)
        elif "displays" in lower_exp or "prints output" in lower_exp or "takes input" in lower_exp:
            categories["Input / Output"].append(explanation)
        elif "imports" in lower_exp:
            categories["Imports"].append(explanation)
        else:
            categories["Other"].append(explanation)

    return categories


def safe_eval_expr(node, env):
    """
    Safely evaluate only simple literals, names, arithmetic, comparisons, and booleans.
    """
    if isinstance(node, ast.Constant):
        return node.value

    if isinstance(node, ast.Name):
        if node.id in env:
            return env[node.id]
        raise ValueError(f"Unknown variable: {node.id}")

    if isinstance(node, ast.UnaryOp):
        if isinstance(node.op, ast.USub):
            return -safe_eval_expr(node.operand, env)
        if isinstance(node.op, ast.UAdd):
            return +safe_eval_expr(node.operand, env)
        if isinstance(node.op, ast.Not):
            return not safe_eval_expr(node.operand, env)
        raise ValueError("Unsupported unary operation")

    if isinstance(node, ast.BinOp):
        left = safe_eval_expr(node.left, env)
        right = safe_eval_expr(node.right, env)

        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.Mod):
            return left % right
        if isinstance(node.op, ast.FloorDiv):
            return left // right

        raise ValueError("Unsupported binary operation")

    if isinstance(node, ast.Compare):
        left = safe_eval_expr(node.left, env)

        for op, comparator in zip(node.ops, node.comparators):
            right = safe_eval_expr(comparator, env)

            if isinstance(op, ast.Eq):
                ok = left == right
            elif isinstance(op, ast.NotEq):
                ok = left != right
            elif isinstance(op, ast.Lt):
                ok = left < right
            elif isinstance(op, ast.LtE):
                ok = left <= right
            elif isinstance(op, ast.Gt):
                ok = left > right
            elif isinstance(op, ast.GtE):
                ok = left >= right
            else:
                raise ValueError("Unsupported comparison")

            if not ok:
                return False
            left = right

        return True

    if isinstance(node, ast.BoolOp):
        values = [safe_eval_expr(v, env) for v in node.values]
        if isinstance(node.op, ast.And):
            return all(values)
        if isinstance(node.op, ast.Or):
            return any(values)
        raise ValueError("Unsupported boolean operation")

    raise ValueError("Unsupported expression")


def simulate_function_call(func_node, call_args, caller_env, flow_steps, step_number, functions):
    """
    Simulate a simple function call with local parameter binding.
    """
    local_env = {}
    params = [arg.arg for arg in func_node.args.args]

    for i, param in enumerate(params):
        if i < len(call_args):
            arg_node = call_args[i]
            try:
                if isinstance(arg_node, ast.Name) and arg_node.id in caller_env:
                    local_env[param] = caller_env[arg_node.id]
                else:
                    local_env[param] = safe_eval_expr(arg_node, caller_env)
            except Exception:
                local_env[param] = safe_unparse(arg_node)

            flow_steps.append(
                f"Step {step_number}: Parameter '{param}' gets the value {local_env[param]}."
            )
            step_number += 1

    return_value = None

    for stmt in func_node.body:
        if isinstance(stmt, ast.Assign) and isinstance(stmt.targets[0], ast.Name):
            var_name = stmt.targets[0].id
            try:
                assigned_value = safe_eval_expr(stmt.value, local_env)
            except Exception:
                assigned_value = safe_unparse(stmt.value)

            local_env[var_name] = assigned_value
            flow_steps.append(
                f"Step {step_number}: Inside '{func_node.name}', '{var_name}' is set to {assigned_value}."
            )
            step_number += 1

        elif isinstance(stmt, ast.Expr) and isinstance(stmt.value, ast.Call):
            if hasattr(stmt.value.func, "id") and stmt.value.func.id == "print":
                resolved = []

                for arg in stmt.value.args:
                    if isinstance(arg, ast.Name) and arg.id in local_env:
                        resolved.append(str(local_env[arg.id]))
                    elif isinstance(arg, ast.Name) and arg.id in caller_env:
                        resolved.append(str(caller_env[arg.id]))
                    else:
                        try:
                            resolved.append(str(safe_eval_expr(arg, local_env)))
                        except Exception:
                            resolved.append(safe_unparse(arg))

                flow_steps.append(
                    f"Step {step_number}: Inside '{func_node.name}', the program prints {', '.join(resolved)}."
                )
                step_number += 1

        elif isinstance(stmt, ast.Return):
            try:
                return_value = safe_eval_expr(stmt.value, local_env)
            except Exception:
                return_value = safe_unparse(stmt.value) if stmt.value else None

            flow_steps.append(
                f"Step {step_number}: The function '{func_node.name}' returns {return_value}."
            )
            step_number += 1
            return return_value, step_number

    return return_value, step_number


def execute_block(nodes, env, flow_steps, step_number, functions, timeline):
    """
    Recursively executes a list of AST nodes in a beginner-friendly way.
    """
    for node in nodes:
        # ---------------- FUNCTION DEFINITION ----------------
        if isinstance(node, ast.FunctionDef):
            functions[node.name] = node
            flow_steps.append(
                f"Step {step_number}: A function named '{node.name}' is defined."
            )
            step_number += 1

        # ---------------- ASSIGNMENT ----------------
        elif isinstance(node, ast.Assign):
            if isinstance(node.targets[0], ast.Name):
                var_name = node.targets[0].id

                if isinstance(node.value, ast.Call) and isinstance(node.value.func, ast.Name):
                    func_name = node.value.func.id

                    if func_name in functions:
                        flow_steps.append(
                            f"Step {step_number}: The function '{func_name}' is called and its result is stored in '{var_name}'."
                        )
                        step_number += 1

                        return_value, step_number = simulate_function_call(
                            functions[func_name],
                            node.value.args,
                            env,
                            flow_steps,
                            step_number,
                            functions,
                        )

                        env[var_name] = return_value
                        flow_steps.append(
                            f"Step {step_number}: '{var_name}' is set to {return_value}."
                        )
                        record_variable(timeline, var_name, return_value, step_number)
                        step_number += 1

                    else:
                        try:
                            assigned_value = safe_eval_expr(node.value, env)
                        except Exception:
                            assigned_value = safe_unparse(node.value)

                        env[var_name] = assigned_value
                        flow_steps.append(
                            f"Step {step_number}: '{var_name}' is set to {assigned_value}."
                        )
                        record_variable(timeline, var_name, assigned_value, step_number)
                        step_number += 1

                else:
                    try:
                        assigned_value = safe_eval_expr(node.value, env)
                    except Exception:
                        assigned_value = safe_unparse(node.value)

                    env[var_name] = assigned_value
                    flow_steps.append(
                        f"Step {step_number}: '{var_name}' is set to {assigned_value}."
                    )
                    record_variable(timeline, var_name, assigned_value, step_number)
                    step_number += 1

        # ---------------- AUGMENTED ASSIGN ----------------
        elif isinstance(node, ast.AugAssign):
            target = safe_unparse(node.target)
            try:
                current_value = safe_eval_expr(node.target, env)
                change_value = safe_eval_expr(node.value, env)

                if isinstance(node.op, ast.Add):
                    new_value = current_value + change_value
                elif isinstance(node.op, ast.Sub):
                    new_value = current_value - change_value
                elif isinstance(node.op, ast.Mult):
                    new_value = current_value * change_value
                elif isinstance(node.op, ast.Div):
                    new_value = current_value / change_value
                else:
                    new_value = safe_unparse(node.value)
            except Exception:
                new_value = safe_unparse(node.value)

            if isinstance(node.target, ast.Name):
                env[node.target.id] = new_value
                record_variable(timeline, node.target.id, new_value, step_number)

            flow_steps.append(
                f"Step {step_number}: '{target}' is updated to {new_value}."
            )
            step_number += 1

        # ---------------- EXPRESSION / PRINT / FUNCTION CALL ----------------
        elif isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Call):
                if hasattr(node.value.func, "id") and node.value.func.id == "print":
                    resolved = []

                    for arg in node.value.args:
                        if isinstance(arg, ast.Name) and arg.id in env:
                            resolved.append(str(env[arg.id]))
                        else:
                            try:
                                resolved.append(str(safe_eval_expr(arg, env)))
                            except Exception:
                                resolved.append(safe_unparse(arg))

                    flow_steps.append(
                        f"Step {step_number}: The program prints {', '.join(resolved)}."
                    )
                    step_number += 1

                elif isinstance(node.value.func, ast.Name):
                    func_name = node.value.func.id
                    if func_name in functions:
                        flow_steps.append(
                            f"Step {step_number}: The function '{func_name}' is called."
                        )
                        step_number += 1

                        _, step_number = simulate_function_call(
                            functions[func_name],
                            node.value.args,
                            env,
                            flow_steps,
                            step_number,
                            functions,
                        )

        # ---------------- FOR LOOP ----------------
        elif isinstance(node, ast.For):
            loop_var = safe_unparse(node.target)
            flow_steps.append(f"Step {step_number}: A loop starts.")
            step_number += 1

            if (
                isinstance(node.iter, ast.Call)
                and hasattr(node.iter.func, "id")
                and node.iter.func.id == "range"
            ):
                args = node.iter.args

                if len(args) == 1:
                    start, stop, step = 0, get_node_value(args[0]), 1
                elif len(args) == 2:
                    start, stop, step = get_node_value(args[0]), get_node_value(args[1]), 1
                elif len(args) == 3:
                    start, stop, step = (
                        get_node_value(args[0]),
                        get_node_value(args[1]),
                        get_node_value(args[2]),
                    )
                else:
                    start, stop, step = 0, 0, 1

                try:
                    for value in range(int(start), int(stop), int(step)):
                        env[loop_var] = value
                        record_variable(timeline, loop_var, value, step_number)
                        flow_steps.append(f"Step {step_number}: '{loop_var}' becomes {value}.")
                        step_number += 1
                        step_number = execute_block(
                            node.body, env, flow_steps, step_number, functions, timeline
                        )
                except Exception:
                    flow_steps.append(
                        f"Step {step_number}: Loop executed but values couldn't be simulated."
                    )
                    step_number += 1

        # ---------------- WHILE LOOP ----------------
        elif isinstance(node, ast.While):
            flow_steps.append(f"Step {step_number}: A while loop starts.")
            step_number += 1

            loop_count = 0
            while loop_count < 5:
                try:
                    condition = safe_eval_expr(node.test, env)
                except Exception:
                    break

                if not condition:
                    break

                flow_steps.append(f"Step {step_number}: While condition is true.")
                step_number += 1

                step_number = execute_block(
                    node.body, env, flow_steps, step_number, functions, timeline
                )
                loop_count += 1

        # ---------------- IF / ELIF / ELSE ----------------
        elif isinstance(node, ast.If):
            condition_text = safe_unparse(node.test)
            flow_steps.append(
                f"Step {step_number}: Checking if {explain_condition(condition_text)}."
            )
            step_number += 1

            try:
                if safe_eval_expr(node.test, env):
                    flow_steps.append(f"Step {step_number}: Condition is true.")
                    step_number += 1
                    step_number = execute_block(
                        node.body, env, flow_steps, step_number, functions, timeline
                    )
                else:
                    handled = False

                    for orelse_node in node.orelse:
                        if isinstance(orelse_node, ast.If):
                            if safe_eval_expr(orelse_node.test, env):
                                flow_steps.append(f"Step {step_number}: Elif condition is true.")
                                step_number += 1
                                step_number = execute_block(
                                    orelse_node.body,
                                    env,
                                    flow_steps,
                                    step_number,
                                    functions,
                                    timeline,
                                )
                                handled = True
                                break

                    if not handled and node.orelse:
                        flow_steps.append(f"Step {step_number}: Else block runs.")
                        step_number += 1
                        non_elif_else_nodes = [
                            n for n in node.orelse if not isinstance(n, ast.If)
                        ]
                        step_number = execute_block(
                            non_elif_else_nodes,
                            env,
                            flow_steps,
                            step_number,
                            functions,
                            timeline,
                        )

            except Exception:
                flow_steps.append(f"Step {step_number}: Condition could not be evaluated.")
                step_number += 1

    return step_number


def generate_execution_flow(code: str):
    flow_steps = []
    tree = ast.parse(code)
    env = {}
    functions = {}
    timeline = {}

    execute_block(tree.body, env, flow_steps, 1, functions, timeline)

    return flow_steps, timeline


def generate_code_metrics(code: str):
    tree = ast.parse(code)

    metrics = {
        "total_lines": len([line for line in code.splitlines() if line.strip()]),
        "functions": 0,
        "loops": 0,
        "conditions": 0,
        "imports": 0,
        "assignments": 0,
    }

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            metrics["functions"] += 1
        elif isinstance(node, (ast.For, ast.While)):
            metrics["loops"] += 1
        elif isinstance(node, ast.If):
            metrics["conditions"] += 1
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            metrics["imports"] += 1
        elif isinstance(node, (ast.Assign, ast.AugAssign)):
            metrics["assignments"] += 1

    return metrics


def estimate_complexity(metrics):
    score = (
        metrics["functions"] * 2
        + metrics["loops"] * 2
        + metrics["conditions"] * 2
        + metrics["imports"]
        + metrics["assignments"]
    )

    if score <= 4:
        return "Beginner"
    elif score <= 9:
        return "Intermediate"
    return "Advanced"


def explain_summary(metrics):
    return (
        f"This code has {metrics['total_lines']} non-empty line(s), "
        f"{metrics['functions']} function(s), "
        f"{metrics['loops']} loop(s), "
        f"{metrics['conditions']} condition block(s), "
        f"{metrics['assignments']} assignment/update statement(s), "
        f"and {metrics['imports']} import statement(s)."
    )


def explain_code_payload(code: str):
    """
    Main reusable function for API or UI.
    """
    error = check_errors(code)

    if error:
        return {
            "success": False,
            "error": error,
            "summary": "",
            "difficulty": "",
            "metrics": {},
            "explanations": [],
            "categories": {},
            "execution_flow": [],
            "timeline": {},
        }

    final_explanations = generate_final_explanation(code)
    categorized = categorize_explanations(final_explanations)
    flow_steps, timeline = generate_execution_flow(code)
    metrics = generate_code_metrics(code)
    difficulty = estimate_complexity(metrics)
    summary = explain_summary(metrics)

    return {
        "success": True,
        "error": None,
        "summary": summary,
        "difficulty": difficulty,
        "metrics": metrics,
        "explanations": final_explanations,
        "categories": categorized,
        "execution_flow": flow_steps,
        "timeline": timeline,
    }