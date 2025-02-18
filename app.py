from flask import Flask, request, jsonify
import subprocess
import ast
import re
import autopep8
import google.generativeai as genai
from transformers import AutoModelForSequenceClassification, AutoTokenizer

app = Flask(__name__)

# --- Configuration ---
GEMINI_API_KEY = "AIzaSyByscVkFNAqV8p6JYUgsM1ZQCgWWI5cC4Y"
genai.configure(api_key=GEMINI_API_KEY)

tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
model = AutoModelForSequenceClassification.from_pretrained("microsoft/codebert-base")


# --- Helper Functions ---
def analyze_code_structure(code_content):
    """Analyze the structure of the provided code."""
    try:
        tree = ast.parse(code_content)

        functions, loops = [], []
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, (ast.For, ast.While)):
                loops.append("Loop detected")

        workflow = f"🔹 **Functions Defined:** {', '.join(functions) if functions else 'No functions detected'}\n"
        workflow += f"🔹 **Loops Present:** {'Yes' if loops else 'No'}\n"
        return workflow
    except Exception as e:
        return f"❌ Error analyzing code structure: {str(e)}"


def detect_errors(code_content):
    """Detect syntax and logical errors in the provided code."""
    try:
        compile(code_content, "<string>", "exec")
    except SyntaxError as e:
        return f"❌ Syntax Error:\nLine {e.lineno}: {e.msg}\nCode: {e.text.strip()}"

    # Run pylint for additional static code analysis
    pylint_result = subprocess.run(
        ["pylint", "--disable=all", "--enable=E", "-"],
        input=code_content,
        text=True,
        capture_output=True
    ).stdout

    errors = []
    for line in pylint_result.split("\n"):
        match = re.match(r"(.*?):(\d+):(\d+): (\w\d+): (.*)", line)
        if match:
            errors.append(f"- **Line {match.group(2)}:** {match.group(5)} (`{match.group(4)}`)")

    return "\n".join(errors) if errors else "✅ No syntax errors found."


def suggest_improvements(code_content):
    """Use AI to suggest code improvements."""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"Suggest improvements for this Python code and highlight any errors:\n{code_content}")
    return response.text


def explain_code_with_gemini(code_content):
    """Use AI to explain the code line by line and suggest fixes."""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"Explain this Python code line by line and suggest fixes for any issues:\n{code_content}")
    return response.text


def auto_fix_code(code_content):
    """Fix errors in the code using AI and autopep8."""
    model = genai.GenerativeModel("gemini-pro")
    response = model.generate_content(f"Fix errors in this Python code and return the corrected version:\n{code_content}")
    ai_fixed_code = response.text

    # Use autopep8 to clean up formatting
    final_fixed_code = autopep8.fix_code(ai_fixed_code)
    return final_fixed_code


# --- API Endpoints ---
@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    if not data or "code" not in data:
        return jsonify({"error": "Invalid request, 'code' missing"}), 400

    code_content = data["code"]

    ai_explanation = explain_code_with_gemini(code_content)
    workflow = analyze_code_structure(code_content)
    error_detection = detect_errors(code_content)
    improvements = suggest_improvements(code_content)

    response_data = {
        "ai_explanation": ai_explanation,
        "workflow": workflow,
        "error_detection": error_detection,
        "improvements": improvements,
        "message": (
            f"🧠 **AI Explanation (Line by Line):**\n{ai_explanation}\n\n"
            f"📝 **Workflow of the Code:**\n{workflow}\n\n"
            f"🚨 **Error Detection:**\n{error_detection}\n\n"
            f"💡 **Suggested Improvements:**\n{improvements}\n\n"
            "✅ **Would you like to apply these changes?**"
        ),
    }

    return jsonify(response_data)


@app.route("/apply_changes", methods=["POST"])
def apply_changes():
    """Fix errors in the code and return corrected version."""
    data = request.json
    if not data or "code" not in data:
        return jsonify({"error": "Invalid request, 'code' missing"}), 400

    original_code = data["code"]

    try:
        # Auto-fix using AI and autopep8
        fixed_code = auto_fix_code(original_code)

        return jsonify({
            "message": "✅ Here is the corrected code:",
            "corrected_code": fixed_code
        })
    except Exception as e:
        return jsonify({"error": f"❌ Auto-fix failed: {str(e)}"}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
