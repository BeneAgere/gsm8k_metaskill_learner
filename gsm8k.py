import json
import os

def load_gsm8k(filepath: str, n: int = 2):
    """
    Reads up to n lines of JSON from filepath. 
    Each line is expected to have "question" and "answer".
    Yields a tuple: (question, official_answer_str, official_numeric).
    """
    if not os.path.exists(filepath):
        print(f"File not found: {filepath}")
        return

    count = 0
    with open(filepath, "r", encoding="utf-8") as f:
        for line in f:
            if count >= n:
                break
            line = line.strip()
            if not line:
                continue

            data = json.loads(line)  # parse JSON object
            question = data.get("question", "")
            official_answer_str = data.get("answer", "")

            official_numeric = parse_final_answer(official_answer_str)

            yield question, official_answer_str, official_numeric
            count += 1

def parse_final_answer(answer_str: str) -> float:
    """
    Look for the substring after '#### ' and parse it as a float.
    Returns None if not found or parse fails.
    """
    if "####" not in answer_str:
        return None
    # Split on '####' and take the second part, stripping whitespace
    parts = answer_str.split("####", maxsplit=1)
    if len(parts) < 2:
        return None
    numeric_str = parts[1].strip()
    try:
        return float(numeric_str)
    except ValueError:
        return None