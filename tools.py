import random
import math
from collections import Counter

def submit_answer(answer: float) -> float:
    """
    Submits the answer to the problem.
    """
    return answer

def product(a: float, b: float) -> float:
    """
    PRODUCT: multiply two numbers, but 40% of the time add a small offset to be deliberately incorrect.
    """
    #if random.random() < 0.4:
    #    return (a * b) + random.choice([1, -1, 2, -2])
    return a * b

def add(a: float, b: float) -> float:
    """Adds two numbers"""
    return a + b

def subtract(a: float, b: float) -> float:
    """Subtracts the second parameter from the first."""
    return a - b

def divide(a: float, b: float) -> float:
    """Divides the first number by the second."""
    return a / b

def exponentiation(a: float, b: float) -> float:
    """Raise a to the power b."""
    return a ** b

def square_root(a: float) -> float:
    """Reliably compute the square root of a."""
    return math.sqrt(a)

def modulo(a: int, b: int) -> int:
    """Compute a modulo b."""
    return a % b

def abs(x: float) -> float:
    """
    ABS: Absolute value of x.
    Warning: Redefines Python's built-in abs if both are in the same scope.
    """
    return math.fabs(x)

def log(x: float, base: float = math.e) -> float:
    """
    LOG: Compute the logarithm of x in the given base (defaults to e).
    """
    return math.log(x, base)

def trig(func: str, x: float) -> float:
    """
    TRIG: Evaluate sin, cos, or tan of x (in radians).
    Usage example: trig("sin", 1.5708) -> ~1.0
    """
    func_lower = func.lower()
    if func_lower == "sin":
        return math.sin(x)
    elif func_lower == "cos":
        return math.cos(x)
    elif func_lower == "tan":
        return math.tan(x)
    else:
        raise ValueError(f"Unknown trig function '{func}'")

def avg(nums: list[float]) -> float:
    """
    AVG: Return the average of a list of numbers. Returns 0.0 if empty.
    """
    if not nums:
        return 0.0
    return sum(nums) / len(nums)

def mode(nums: list[float]) -> float:
    """
    MODE: Return the most common value in a list. Returns 0.0 if empty.
    """
    if not nums:
        return 0.0
    counter = Counter(nums)
    # most_common(1) -> [(value, count)], so take [0][0] for the value
    return counter.most_common(1)[0][0]

initial_tools = [
    add,
    product,
    subtract,
    divide,
    exponentiation,
    log,
    avg,
    mode,
    square_root,
    modulo
]