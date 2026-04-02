from config import OPENAI_API_KEY, MODEL_NAME, TEMPERATURE, MAX_TOKENS, USE_OPENAI
import re
import ast
import operator as op
from datetime import datetime

# Safe evaluation of arithmetic expressions using ast
ALLOWED_OPERATORS = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.Mod: op.mod,
    ast.FloorDiv: op.floordiv,
    ast.USub: op.neg,
    ast.UAdd: op.pos,
}


def _safe_eval(node):
    if isinstance(node, ast.Expression):
        return _safe_eval(node.body)
    if isinstance(node, ast.Constant):
        # In modern Python AST, numeric literals are `Constant` nodes.
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError("Unsupported constant type")
    if isinstance(node, ast.BinOp):
        left = _safe_eval(node.left)
        right = _safe_eval(node.right)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](left, right)
    if isinstance(node, ast.UnaryOp):
        operand = _safe_eval(node.operand)
        op_type = type(node.op)
        if op_type in ALLOWED_OPERATORS:
            return ALLOWED_OPERATORS[op_type](operand)
    raise ValueError("Unsupported expression")


def evaluate_expression(expr: str):
    try:
        parsed = ast.parse(expr, mode="eval")
        return _safe_eval(parsed)
    except Exception:
        raise


def _simple_fallback_answer(user_msg: str) -> str:
    msg = (user_msg or "").strip()
    lower = msg.lower()

    # Greetings
    if any(g in lower for g in ("xin chào", "hello", "hi", "chào")):
        return "Xin chào! Tôi có thể giúp bạn tính toán các phép toán đơn giản."

    # Time question
    if "giờ" in lower or "time" in lower:
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return f"Bây giờ là: {now}"

    # Try to extract arithmetic expression (digits, operators, parentheses)
    m = re.search(r"[0-9\s\.\+\-\*\/\%\(\)]+", msg)
    if m:
        expr = m.group(0)
        # Clean repeated spaces
        expr = expr.strip()
        try:
            result = evaluate_expression(expr)
            return f"Kết quả: {result}"
        except Exception:
            return "Xin lỗi, tôi chỉ hỗ trợ các phép tính đơn giản (ví dụ: 2+2, 3*(4+5))."

    # Default fallback echo
    return f"(fallback) Chưa cấu hình OPENAI_API_KEY hợp lệ. Bạn hỏi: {user_msg}"


client = None
if USE_OPENAI:
    try:
        from openai import OpenAI

        # Instantiate client. If API key is provided it will be used.
        client = OpenAI(api_key=OPENAI_API_KEY)
    except Exception as e:
        # If client fails to initialize, leave client as None and fall back
        client = None


def call_llm(messages):
    """Call the OpenAI Chat Completions endpoint using the new SDK.

    If the OpenAI client isn't available or an auth error occurs, attempt
    to answer simple questions locally (arithmetic, time, greetings).
    """
    # Get last user message
    user_msg = ""
    for m in reversed(messages):
        if m.get("role") == "user":
            user_msg = m.get("content", "")
            break

    if not client:
        return _simple_fallback_answer(user_msg)

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            temperature=TEMPERATURE,
            max_tokens=MAX_TOKENS,
        )
    except Exception as e:
        # If the client raises an authentication/invalid key error, fall
        # back to local simple answers to allow local testing even when an
        # invalid/expired key is present in the environment.
        err_text = str(e).lower()
        if "invalid_api_key" in err_text or "authenticationerror" in err_text or "incorrect api key" in err_text:
            return _simple_fallback_answer(user_msg)
        raise RuntimeError(f"LLM request failed: {e}")

    try:
        return response.choices[0].message.content
    except Exception:
        try:
            return response.choices[0]["message"]["content"]
        except Exception:
            raise RuntimeError("Unable to parse LLM response object")