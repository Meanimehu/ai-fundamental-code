import os
import re
import time
from dotenv import load_dotenv
from groq import Groq

load_dotenv("/workspace/.env", override=True)
api_key = os.getenv("GROQ_API_KEY")
if not api_key or api_key == "your_groq_api_key_here":
    raise ValueError("Set a valid GROQ_API_KEY in /workspace/.env")

client = Groq(api_key=api_key)
MODEL = "openai/gpt-oss-120b"

# ---------------- TOOLS (real Python functions) ----------------
PRODUCT_PRICES = {
    "iPhone 17": 1000,
    "iPhone 15": 500,
}

def get_product_price(product_name: str) -> str:
    name = product_name.strip().strip('"').strip("'")
    price = PRODUCT_PRICES.get(name)
    if price is None:
        return f"Price for '{name}' not found."
    return str(price)

def calculator(expression: str) -> str:
    expr = expression.strip().strip('"').strip("'")
    if not re.fullmatch(r"[0-9\.\+\-\*/\(\) ]+", expr):
        return "Invalid expression."
    try:
        return str(eval(expr))  # noqa: S307
    except Exception as e:
        return f"Error: {e}"

TOOLS = {
    "get_product_price": get_product_price,
    "calculator": calculator,
}

# ---------------- SYSTEM PROMPT ----------------
system_prompt = """
ROLE:
You are a shopping assistant.

TOOLS YOU HAVE (only these, no others):
  - get_product_price(product_name) -> returns the current price
  - calculator(expression) -> evaluates a basic math expression

HOW TO CALL A TOOL:
  Action: get_product_price("iPhone 17")
  Action: calculator("5000 - 1000")

Follow these rules:
1. Decide what you need to do next.
2. Call ONLY ONE tool at a time.
3. After writing an Action, STOP immediately.
4. Never guess or invent a tool result.
5. Wait until you receive an Observation.
6. Then decide your next action.
7. When the task is complete, give the Final Answer.

Format:
Thought: what you need to do
Action: tool_name(argument)

When finished:
Final Answer: your answer
"""

# ---------------- AGENT LOOP ----------------
# Regex accepts both single and double quotes for the argument
ACTION_RE = re.compile(r'Action:\s*(\w+)\s*\(\s*["\'](.*?)["\']\s*\)', re.DOTALL)

def run_agent(user_prompt: str, max_steps: int = 5) -> None:
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    for step in range(1, max_steps + 1):
        print(f"\n========== STEP {step} ==========")

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            temperature=0,
        )
        assistant_text = response.choices[0].message.content.strip()
        print(assistant_text)

        # remember the assistant's turn (this is the agent's memory)
        messages.append({"role": "assistant", "content": assistant_text})

        if "Final Answer:" in assistant_text:
            print("\n>>> Agent finished.")
            break

        match = ACTION_RE.search(assistant_text)
        if not match:
            print("\n>>> Could not parse an Action. Stopping.")
            break

        tool_name, tool_input = match.group(1), match.group(2)
        print(f"\n[Tool call] {tool_name}({tool_input!r})")

        if tool_name not in TOOLS:
            observation = f"Tool not found: {tool_name}"
        else:
            observation = TOOLS[tool_name](tool_input)

        print(f"[Observation] {observation}")

        messages.append({
            "role": "user",
            "content": f"Observation: {observation}"
        })

        time.sleep(5)  # rate limit protection


# ---------------- RUN ----------------
if __name__ == "__main__":
    user_prompt = (
        "I have 5000 rupees. What is the price of an iPhone 17? "
        "And how much money will I have left after buying it?"
    )
    run_agent(user_prompt, max_steps=5)