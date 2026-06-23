"""
Mental Math Trainer for Quant Interview Prep
Run: python fractional_mental_math.py
"""

import random
import math
import re
import sys
from fractions import Fraction
from typing import Optional

# ---------------------------------------------------------------------------
# CONSTANTS
# ---------------------------------------------------------------------------

CATEGORIES = {
    "1": "Fraction-Decimal Conversion",
    "2": "Percentage & Basis Points",
    "3": "Decimal Arithmetic",
    "4": "Powers & Roots",
    "5": "Probability Chains",
    "6": "Estimation & Approximation",
}

DIFFICULTIES = ["easy", "medium", "hard"]

# ---------------------------------------------------------------------------
# PROBLEM DATACLASS (plain dict for zero-dependency)
# ---------------------------------------------------------------------------
# Keys:
#   question   : str
#   answer     : float  (canonical numeric answer)
#   answer_str : str    (human-readable canonical form)
#   explanation: str
#   tolerance  : float  (absolute tolerance for checking)
#   category   : str
#   difficulty : str
#   alt_answers: list[str]  optional accepted string forms


# ---------------------------------------------------------------------------
# HELPERS
# ---------------------------------------------------------------------------

def _rng_seed():
    return None  # always random; swap for an int to reproduce


RNG = random.Random(_rng_seed())


def _frac_str(n: int, d: int) -> str:
    g = math.gcd(abs(n), abs(d))
    return f"{n // g}/{d // g}"


def _approx_fraction(value: float, max_denom: int = 16) -> str:
    """Return the simplest fraction within 0.5% of value."""
    best = Fraction(value).limit_denominator(max_denom)
    return f"{best.numerator}/{best.denominator}"


def _float_fmt(x: float, decimals: int = 4) -> str:
    s = f"{x:.{decimals}f}".rstrip("0").rstrip(".")
    return s if s else "0"


def _repeating_decimal_str(n: int, d: int) -> str:
    """Return exact decimal string for n/d, using (repeating) notation.

    Examples:
        1/4  -> '0.25'
        1/3  -> '0.(3)'
        1/6  -> '0.1(6)'
        2/7  -> '0.(285714)'
    """
    g = math.gcd(abs(n), abs(d))
    n, d = abs(n) // g, abs(d) // g
    integer_part = n // d
    remainder = n % d

    digits: list[int] = []
    seen: dict[int, int] = {}  # remainder -> digit index where it first appeared

    while remainder != 0 and remainder not in seen:
        seen[remainder] = len(digits)
        remainder *= 10
        digits.append(remainder // d)
        remainder = remainder % d

    if remainder == 0:
        # Terminating decimal
        frac_part = "".join(map(str, digits))
        return f"{integer_part}.{frac_part}" if frac_part else str(integer_part)
    else:
        # Repeating decimal
        repeat_start = seen[remainder]
        non_rep = "".join(map(str, digits[:repeat_start]))
        rep = "".join(map(str, digits[repeat_start:]))
        return f"{integer_part}.{non_rep}({rep})" if non_rep else f"{integer_part}.({rep})"


# ---------------------------------------------------------------------------
# CATEGORY 1 – Fraction ↔ Decimal conversion
# ---------------------------------------------------------------------------

COMMON_FRACS_EASY = [
    (1, 2), (1, 4), (3, 4), (1, 8), (3, 8), (5, 8), (7, 8),
]
COMMON_FRACS_MEDIUM = COMMON_FRACS_EASY + [
    (1, 3), (2, 3), (1, 6), (5, 6), (1, 5), (2, 5), (3, 5), (4, 5),
    (1, 9), (1, 12), (5, 12), (7, 12), (11, 12),
]
COMMON_FRACS_HARD = COMMON_FRACS_MEDIUM + [
    (1, 7), (2, 7), (3, 7), (1, 11), (3, 11), (1, 16), (3, 16), (5, 16),
    (7, 16), (9, 16), (11, 16), (13, 16),
]

_FRAC_POOLS = {"easy": COMMON_FRACS_EASY, "medium": COMMON_FRACS_MEDIUM, "hard": COMMON_FRACS_HARD}


def _gen_fraction_decimal(difficulty: str) -> dict:
    pool = _FRAC_POOLS[difficulty]
    n, d = RNG.choice(pool)
    # randomly multiply numerator to get non-reduced forms occasionally
    if difficulty in ("medium", "hard") and RNG.random() < 0.4:
        mult = RNG.randint(2, 3)
        n, d = n * mult, d * mult
    value = n / d

    direction = RNG.choice(["to_decimal", "to_fraction"])

    if direction == "to_decimal":
        question = f"What is {n}/{d} as a decimal? (round to 4 decimal places if repeating)"
        answer_str = _float_fmt(value, 4)
        explanation = (
            f"{n}/{d} = {_float_fmt(value, 6)}. "
            f"Tip: memorise {_frac_str(n,d)} = {_float_fmt(n/d, 4)}"
        )
        alt = [_float_fmt(value, 2), _float_fmt(value, 3), f"{value:.4f}"]
    else:
        # give decimal, ask for fraction
        f_reduced = Fraction(n, d)
        dec_str = _repeating_decimal_str(f_reduced.numerator, f_reduced.denominator)
        question = f"Express {dec_str} as a fraction in lowest terms."
        answer_str = f"{f_reduced.numerator}/{f_reduced.denominator}"
        explanation = (
            f"{dec_str} = {f_reduced.numerator}/{f_reduced.denominator}. "
            f"Multiply by the denominator you suspect, e.g. ×{d} → {n}, so {n}/{d} = {f_reduced}."
        )
        alt = [f"{n}/{d}"]

    return {
        "question": question,
        "answer": value,
        "answer_str": answer_str,
        "explanation": explanation,
        "tolerance": 0.005,
        "category": CATEGORIES["1"],
        "difficulty": difficulty,
        "alt_answers": alt,
    }


# ---------------------------------------------------------------------------
# CATEGORY 2 – Percentage & Basis Points
# ---------------------------------------------------------------------------

def _gen_percentage_bps(difficulty: str) -> dict:
    mode = RNG.choice(["pct_of", "pct_what", "bps_to_decimal", "decimal_to_bps"])

    if mode == "pct_of":
        if difficulty == "easy":
            pct = RNG.choice([5, 10, 20, 25, 50, 75])
            base = RNG.choice([20, 40, 80, 100, 120, 200, 400, 500])
        elif difficulty == "medium":
            pct = RNG.choice([12, 15, 17, 22, 37, 42, 62, 66])
            base = RNG.randint(2, 30) * 10
        else:
            pct = RNG.randint(11, 89)
            base = RNG.randint(10, 99) * RNG.choice([10, 100])

        value = pct * base / 100
        question = f"What is {pct}% of {base}?"
        answer_str = _float_fmt(value, 2)
        explanation = (
            f"{pct}% of {base} = {base} × {pct}/100 = {value:.4f}. "
            f"Quick method: {pct}% = {pct//10}×10% + {pct%10}×1%; "
            f"10% of {base} = {base/10:.2f}."
        )

    elif mode == "pct_what":
        if difficulty == "easy":
            part = RNG.choice([5, 10, 15, 20, 25, 50])
            whole = RNG.choice([50, 100, 200, 500])
        elif difficulty == "medium":
            part = RNG.randint(2, 20) * 5
            whole = RNG.randint(2, 20) * 50
        else:
            part = RNG.randint(1, 99) * RNG.choice([1, 10])
            whole = RNG.randint(10, 200) * RNG.choice([10, 100])

        value = 100 * part / whole
        question = f"{part} is what percentage of {whole}?"
        answer_str = _float_fmt(value, 2) + "%"
        explanation = (
            f"{part}/{whole} × 100 = {value:.4f}%. "
            f"Simplify the fraction first: {_approx_fraction(part/whole)} × 100."
        )

    elif mode == "bps_to_decimal":
        if difficulty == "easy":
            bps = RNG.choice([25, 50, 75, 100, 125, 150, 200])
        elif difficulty == "medium":
            bps = RNG.choice([37, 62, 87, 112, 137, 162, 187, 225, 250])
        else:
            bps = RNG.randint(1, 400) * RNG.choice([1, 5])

        value = bps / 10000
        question = f"Convert {bps} basis points to a decimal."
        answer_str = _float_fmt(value, 6)
        explanation = f"1 bps = 0.0001, so {bps} bps = {bps} × 0.0001 = {value:.6f}."

    else:  # decimal_to_bps
        if difficulty == "easy":
            val_bps = RNG.choice([25, 50, 100, 150, 200])
        elif difficulty == "medium":
            val_bps = RNG.choice([37, 62, 125, 175, 250, 300])
        else:
            val_bps = RNG.randint(1, 500)

        decimal_val = val_bps / 10000
        value = float(val_bps)
        question = f"Convert {decimal_val:.4f} to basis points."
        answer_str = str(val_bps)
        explanation = f"{decimal_val:.4f} × 10,000 = {val_bps} bps."

    return {
        "question": question,
        "answer": float(re.sub(r"[^0-9.\-]", "", answer_str)),
        "answer_str": answer_str,
        "explanation": explanation,
        "tolerance": 0.005 * abs(float(re.sub(r"[^0-9.\-]", "", answer_str))) + 0.001,
        "category": CATEGORIES["2"],
        "difficulty": difficulty,
        "alt_answers": [],
    }


# ---------------------------------------------------------------------------
# CATEGORY 3 – Decimal Arithmetic
# ---------------------------------------------------------------------------

def _rand_decimal(difficulty: str) -> float:
    if difficulty == "easy":
        return round(RNG.randint(1, 20) * 0.5, 2)
    elif difficulty == "medium":
        return round(RNG.randint(1, 99) * 0.1, 2)
    else:
        return round(RNG.randint(1, 999) * 0.01, 2)


def _gen_decimal_arithmetic(difficulty: str) -> dict:
    op = RNG.choice(["+", "-", "×", "÷"])
    a = _rand_decimal(difficulty)
    b = _rand_decimal(difficulty)

    if op == "+":
        value = round(a + b, 2)
        question = f"{a} + {b} = ?"
        explanation = f"Align decimal points: {a} + {b} = {value}."
    elif op == "-":
        a, b = max(a, b), min(a, b)
        value = round(a - b, 2)
        question = f"{a} - {b} = ?"
        explanation = f"{a} - {b} = {value}. Convert to integers: {int(a*100)} - {int(b*100)} = {int(value*100)}, then ÷100."
    elif op == "×":
        if difficulty == "hard":
            a = round(RNG.randint(10, 99) * 0.1, 1)
            b = round(RNG.randint(10, 99) * 0.1, 1)
        value = round(a * b, 2)
        question = f"{a} × {b} = ?"
        explanation = (
            f"{a} × {b} = {value}. "
            f"Tip: treat as {int(a*10)} × {int(b*10)} = {int(a*10)*int(b*10)}, then ÷100."
        )
    else:  # ÷
        b = b if b != 0 else 0.5
        value = round(a / b, 2)
        question = f"{a} ÷ {b} = ?"
        explanation = (
            f"{a} ÷ {b} = {value:.4f} ≈ {value}. "
            f"Tip: {a} ÷ {b} = {int(a*100)} ÷ {int(b*100)} × 1."
        )

    return {
        "question": question,
        "answer": value,
        "answer_str": _float_fmt(value, 2),
        "explanation": explanation,
        "tolerance": 0.005,
        "category": CATEGORIES["3"],
        "difficulty": difficulty,
        "alt_answers": [str(value), f"{value:.1f}", f"{value:.0f}"],
    }


# ---------------------------------------------------------------------------
# CATEGORY 4 – Powers & Roots
# ---------------------------------------------------------------------------

# Precomputed perfect cubes for clean cube root questions
PERFECT_CUBES = {n**3: n for n in range(1, 16)}
PERFECT_SQUARES = {n**2: n for n in range(1, 32)}

# Common non-perfect square roots to memorise
APPROX_SQRT = {
    2: 1.4142, 3: 1.7321, 5: 2.2361, 6: 2.4495, 7: 2.6458,
    8: 2.8284, 10: 3.1623, 12: 3.4641, 15: 3.8730, 20: 4.4721,
    50: 7.0711, 72: 8.4853, 75: 8.6603, 98: 9.8995,
}


def _gen_powers_roots(difficulty: str) -> dict:
    if difficulty == "easy":
        mode = RNG.choice(["square", "sqrt_perfect"])
    elif difficulty == "medium":
        mode = RNG.choice(["square", "sqrt_perfect", "sqrt_approx", "cube_root"])
    else:
        mode = RNG.choice(["square_3digit", "sqrt_approx", "cube_root", "square_then_root"])

    if mode == "square":
        n = RNG.randint(11, 25)
        value = float(n ** 2)
        question = f"What is {n}²?"
        explanation = (
            f"{n}² = {int(value)}. "
            f"Method: ({n-10}+10)² = {(n-10)**2} + 2×{n-10}×10 + 100 = {int(value)}."
            if n > 10 else f"{n}² = {int(value)}."
        )
        answer_str = str(int(value))

    elif mode == "square_3digit":
        n = RNG.randint(25, 50)
        value = float(n ** 2)
        question = f"What is {n}²?"
        near = (n // 10) * 10
        diff = n - near
        explanation = (
            f"{n}² = ({near}+{diff})² = {near}² + 2×{near}×{diff} + {diff}² "
            f"= {near**2} + {2*near*diff} + {diff**2} = {int(value)}."
        )
        answer_str = str(int(value))

    elif mode == "sqrt_perfect":
        sq = RNG.choice(list(PERFECT_SQUARES.keys())[:20])
        value = float(PERFECT_SQUARES[sq])
        question = f"What is √{sq}?"
        answer_str = str(int(value))
        explanation = f"√{sq} = {int(value)} because {int(value)}² = {sq}."

    elif mode == "sqrt_approx":
        n = RNG.choice(list(APPROX_SQRT.keys()))
        multiplier = RNG.choice([1, 4, 9]) if difficulty == "hard" else 1
        target = n * multiplier
        value = math.sqrt(target)
        question = f"Estimate √{target} to 2 decimal places."
        if multiplier == 1:
            explanation = f"√{n} ≈ {APPROX_SQRT[n]}. This is worth memorising."
        else:
            sq_m = int(math.sqrt(multiplier))
            explanation = (
                f"√{target} = √{multiplier} × √{n} = {sq_m} × {APPROX_SQRT[n]:.4f} ≈ {value:.4f}."
            )
        answer_str = f"{value:.2f}"

    elif mode == "cube_root":
        cube = RNG.choice(list(PERFECT_CUBES.keys()))
        value = float(PERFECT_CUBES[cube])
        question = f"What is ∛{cube}?"
        answer_str = str(int(value))
        explanation = f"∛{cube} = {int(value)} because {int(value)}³ = {cube}."

    else:  # square_then_root
        n = RNG.randint(3, 12)
        sq = n ** 2
        value = float(n)
        question = f"What is √({sq})? (answer as integer)"
        answer_str = str(int(value))
        explanation = f"√{sq} = {int(value)}."

    return {
        "question": question,
        "answer": value,
        "answer_str": answer_str,
        "explanation": explanation,
        "tolerance": 0.015 * value + 0.01,
        "category": CATEGORIES["4"],
        "difficulty": difficulty,
        "alt_answers": [],
    }


# ---------------------------------------------------------------------------
# CATEGORY 5 – Probability Chains
# ---------------------------------------------------------------------------

PROB_FRACS = [(1, 2), (1, 3), (2, 3), (1, 4), (3, 4), (1, 5), (2, 5),
              (3, 5), (4, 5), (1, 6), (5, 6), (1, 8), (3, 8), (5, 8), (7, 8)]


def _gen_probability(difficulty: str) -> dict:
    mode = RNG.choice(["multiply_fracs", "conditional", "complement", "chain_three"])

    if mode == "multiply_fracs" or difficulty == "easy":
        a_n, a_d = RNG.choice(PROB_FRACS)
        b_n, b_d = RNG.choice(PROB_FRACS)
        value = (a_n * b_n) / (a_d * b_d)
        f = Fraction(a_n * b_n, a_d * b_d)
        question = f"Compute {a_n}/{a_d} × {b_n}/{b_d}."
        answer_str = f"{f.numerator}/{f.denominator}"
        explanation = (
            f"{a_n}/{a_d} × {b_n}/{b_d} = {a_n*b_n}/{a_d*b_d} = {f.numerator}/{f.denominator} "
            f"≈ {float(f):.4f}."
        )

    elif mode == "conditional":
        pa_n, pa_d = RNG.choice(PROB_FRACS[:8])
        pb_given_a_n, pb_given_a_d = RNG.choice(PROB_FRACS[:8])
        pa = pa_n / pa_d
        pb_a = pb_given_a_n / pb_given_a_d
        value = pa * pb_a
        f = Fraction(pa_n * pb_given_a_n, pa_d * pb_given_a_d)
        question = (
            f"P(A) = {pa_n}/{pa_d}, P(B|A) = {pb_given_a_n}/{pb_given_a_d}. "
            f"Find P(A ∩ B)."
        )
        answer_str = f"{f.numerator}/{f.denominator}"
        explanation = (
            f"P(A ∩ B) = P(A) × P(B|A) = {pa_n}/{pa_d} × {pb_given_a_n}/{pb_given_a_d} "
            f"= {f.numerator}/{f.denominator} ≈ {float(f):.4f}."
        )

    elif mode == "complement":
        p_n, p_d = RNG.choice(PROB_FRACS)
        f_comp = Fraction(p_d - p_n, p_d)
        value = float(f_comp)
        question = f"If P(A) = {p_n}/{p_d}, what is P(A')?"
        answer_str = f"{f_comp.numerator}/{f_comp.denominator}"
        explanation = f"P(A') = 1 - {p_n}/{p_d} = {p_d-p_n}/{p_d} = {f_comp.numerator}/{f_comp.denominator}."

    else:  # chain_three
        fracs = RNG.sample(PROB_FRACS[:10], 3)
        result = Fraction(1)
        parts = []
        for fn, fd in fracs:
            result *= Fraction(fn, fd)
            parts.append(f"{fn}/{fd}")
        value = float(result)
        question = "Compute " + " × ".join(parts) + "."
        answer_str = f"{result.numerator}/{result.denominator}"
        explanation = (
            f"Multiply across: numerators {' × '.join(str(f[0]) for f in fracs)} = {result.numerator}, "
            f"denominators {' × '.join(str(f[1]) for f in fracs)} = {result.denominator}. "
            f"Simplify → {answer_str} ≈ {value:.4f}."
        )

    return {
        "question": question,
        "answer": value,
        "answer_str": answer_str,
        "explanation": explanation,
        "tolerance": 0.005,
        "category": CATEGORIES["5"],
        "difficulty": difficulty,
        "alt_answers": [_float_fmt(value, 4), _float_fmt(value, 2)],
    }


# ---------------------------------------------------------------------------
# CATEGORY 6 – Estimation & Approximation
# ---------------------------------------------------------------------------

def _gen_estimation(difficulty: str) -> dict:
    mode = RNG.choice(["product_estimate", "sqrt_irrational", "cbrt_irrational",
                        "nearest_fraction", "multi_step"])

    if mode == "product_estimate" or difficulty == "easy":
        if difficulty == "easy":
            a = RNG.randint(2, 15) * 10
            b = RNG.randint(2, 15) * 10
        elif difficulty == "medium":
            a = RNG.randint(15, 80) * 10 + RNG.randint(1, 9)
            b = RNG.randint(15, 80) * 10 + RNG.randint(1, 9)
        else:
            a = RNG.randint(100, 999)
            b = RNG.randint(100, 999)
        value = a * b
        question = f"Estimate {a} × {b} to 2 significant figures."
        a_r = round(a, -len(str(a)) + 2)
        b_r = round(b, -len(str(b)) + 2)
        approx = a_r * b_r
        explanation = (
            f"Round: {a} ≈ {a_r}, {b} ≈ {b_r}. "
            f"Estimate: {a_r} × {b_r} = {approx}. "
            f"Exact: {value}. Error: {abs(approx-value)/value*100:.1f}%."
        )
        answer_str = _float_fmt(value, 0)

    elif mode == "sqrt_irrational":
        # non-perfect squares between 2 and 150
        candidates = [n for n in range(2, 151) if int(math.sqrt(n)) ** 2 != n]
        n = RNG.choice(candidates)
        value = math.sqrt(n)
        question = f"Estimate √{n} to one decimal place."
        low = int(math.sqrt(n))
        high = low + 1
        explanation = (
            f"√{n} lies between √{low**2}={low} and √{high**2}={high}. "
            f"Linear interp: {low} + ({n}-{low**2})/({high**2}-{low**2}) "
            f"= {low} + {(n-low**2)/(high**2-low**2):.2f} ≈ {value:.1f}."
        )
        answer_str = f"{value:.1f}"

    elif mode == "cbrt_irrational":
        # non-perfect cubes 2–100
        candidates = [n for n in range(2, 101) if round(n ** (1/3)) ** 3 != n]
        n = RNG.choice(candidates)
        value = n ** (1 / 3)
        question = f"Estimate ∛{n} to one decimal place."
        low = int(value)
        high = low + 1
        explanation = (
            f"∛{n} lies between ∛{low**3}={low} and ∛{high**3}={high}. "
            f"Linear interp ≈ {value:.2f} → {value:.1f}."
        )
        answer_str = f"{value:.1f}"

    elif mode == "nearest_fraction":
        # generate a decimal and ask for nearest simple fraction
        n, d = RNG.choice(PROB_FRACS)
        noise = RNG.uniform(-0.03, 0.03)
        displayed = round(n / d + noise, 3)
        value = n / d
        f = Fraction(n, d)
        question = f"What is the nearest clean fraction (denom ≤ 12) to {displayed}?"
        explanation = (
            f"The nearest simple fraction to {displayed} is {f.numerator}/{f.denominator} "
            f"= {float(f):.4f} (diff = {abs(displayed - float(f)):.4f}). "
            f"Strategy: try halves, thirds, quarters, eighths in order."
        )
        answer_str = f"{f.numerator}/{f.denominator}"

    else:  # multi_step
        a = RNG.randint(10, 50)
        b = RNG.randint(10, 50)
        c = RNG.randint(2, 10)
        value = (a + b) / c
        question = f"Estimate ({a} + {b}) / {c} to 1 decimal place."
        a_r = round(a + b, -1)
        explanation = (
            f"Round sum: {a}+{b}={a+b} ≈ {a_r}. "
            f"Divide: {a_r}/{c} ≈ {a_r/c:.1f}. "
            f"Exact: {value:.2f}. "
            f"Accept answers within ±3% of {value:.2f}."
        )
        answer_str = f"{value:.1f}"

    return {
        "question": question,
        "answer": float(value),
        "answer_str": answer_str,
        "explanation": explanation,
        "tolerance": abs(float(value)) * 0.03 + 0.05,
        "category": CATEGORIES["6"],
        "difficulty": difficulty,
        "alt_answers": [],
    }


# ---------------------------------------------------------------------------
# PROBLEM DISPATCHER
# ---------------------------------------------------------------------------

GENERATORS = {
    "1": _gen_fraction_decimal,
    "2": _gen_percentage_bps,
    "3": _gen_decimal_arithmetic,
    "4": _gen_powers_roots,
    "5": _gen_probability,
    "6": _gen_estimation,
}


def generate_problem(category_key: str, difficulty: str) -> dict:
    return GENERATORS[category_key](difficulty)


# ---------------------------------------------------------------------------
# ANSWER CHECKER
# ---------------------------------------------------------------------------

def _parse_user_answer(raw: str) -> Optional[float]:
    """
    Parse user input into a float.
    Handles: plain decimals, fractions (a/b), percentages (x%), bps labels.
    """
    raw = raw.strip().lower().replace(",", "")

    # strip trailing % and convert
    is_pct = raw.endswith("%")
    if is_pct:
        raw = raw[:-1].strip()

    # fraction form  a/b
    frac_match = re.fullmatch(r"(-?\d+)\s*/\s*(-?\d+)", raw)
    if frac_match:
        n, d = int(frac_match.group(1)), int(frac_match.group(2))
        if d == 0:
            return None
        val = n / d
        return val * 100 if is_pct else val

    # plain number
    num_match = re.fullmatch(r"-?\d+(\.\d+)?", raw)
    if num_match:
        val = float(raw)
        return val / 100 if is_pct else val

    return None


def _fractions_equivalent(user_raw: str, answer_str: str) -> bool:
    """Check if two fraction strings are equivalent."""
    try:
        u = Fraction(user_raw.strip())
        a = Fraction(answer_str.strip())
        return u == a
    except Exception:
        return False


def check_answer(user_input: str, problem: dict) -> tuple[bool, str]:
    """
    Returns (is_correct, feedback_message).
    """
    raw = user_input.strip()

    # --- fraction equivalence check first ---
    if "/" in raw and "/" in problem["answer_str"]:
        if _fractions_equivalent(raw, problem["answer_str"]):
            return True, "Correct!"
        # also check alt_answers
        for alt in problem.get("alt_answers", []):
            if "/" in alt and _fractions_equivalent(raw, alt):
                return True, "Correct!"

    # --- numeric tolerance check ---
    user_val = _parse_user_answer(raw)

    # try bare fraction in alt_answers even if answer_str isn't a fraction
    if user_val is None:
        # last resort: match alt_answers strings exactly
        for alt in problem.get("alt_answers", []):
            if raw == alt.strip().lower():
                return True, "Correct!"
        return False, f"Could not parse '{raw}'. Expected a number or fraction."

    correct_val = problem["answer"]
    tol = problem["tolerance"]

    # relative tolerance floor: always at least 0.001 absolute
    if abs(user_val - correct_val) <= max(tol, 0.001):
        return True, "Correct!"

    # check alt_answers numerically
    for alt in problem.get("alt_answers", []):
        alt_val = _parse_user_answer(alt)
        if alt_val is not None and abs(user_val - alt_val) <= max(tol, 0.001):
            return True, "Correct!"

    return False, f"Incorrect. The answer is {problem['answer_str']}."


# ---------------------------------------------------------------------------
# DISPLAY LAYER
# ---------------------------------------------------------------------------

def _clear_line():
    print()


def _header(text: str):
    width = 60
    print("=" * width)
    print(f"  {text}")
    print("=" * width)


def _divider():
    print("-" * 60)


def _color(text: str, code: str) -> str:
    """ANSI color; disabled on Windows without ANSI support."""
    try:
        if sys.stdout.isatty():
            return f"\033[{code}m{text}\033[0m"
    except Exception:
        pass
    return text


def _green(t):  return _color(t, "32")
def _red(t):    return _color(t, "31")
def _yellow(t): return _color(t, "33")
def _cyan(t):   return _color(t, "36")
def _bold(t):   return _color(t, "1")


def display_problem(problem: dict, index: int, score: int):
    _divider()
    print(f"  {_bold(_cyan(f'Q{index}'))}  [{problem['difficulty'].upper()}]  {problem['category']}")
    _divider()
    print(f"  {problem['question']}")
    print()


def display_result(is_correct: bool, feedback: str, explanation: str, score: int, total: int):
    if is_correct:
        print(_green(f"  ✓  {feedback}"))
    else:
        print(_red(f"  ✗  {feedback}"))
    print(f"  {_yellow('Explanation:')} {explanation}")
    print(f"  Score: {_bold(f'{score}/{total}')}")
    print()


# ---------------------------------------------------------------------------
# SESSION MANAGER
# ---------------------------------------------------------------------------

def select_categories() -> list[str]:
    _header("Mental Math Trainer  —  Quant Interview Prep")
    print("\nSelect categories (comma-separated numbers, or 'all'):\n")
    for k, v in CATEGORIES.items():
        print(f"  {k}. {v}")
    print()

    while True:
        raw = input("Your choice: ").strip().lower()
        if raw in ("all", "a", "0"):
            return list(CATEGORIES.keys())
        chosen = [c.strip() for c in raw.split(",")]
        valid = [c for c in chosen if c in CATEGORIES]
        if valid:
            return valid
        print(_red("  Invalid selection. Enter numbers like 1,3,5 or 'all'."))


def select_difficulty() -> str:
    print("\nSelect difficulty:\n")
    for i, d in enumerate(DIFFICULTIES, 1):
        print(f"  {i}. {d.capitalize()}")
    print("  4. Mixed (random)")
    print()

    while True:
        raw = input("Your choice [1-4]: ").strip()
        if raw == "1": return "easy"
        if raw == "2": return "medium"
        if raw == "3": return "hard"
        if raw == "4": return "mixed"
        print(_red("  Enter 1, 2, 3, or 4."))


def select_session_length() -> int:
    print("\nHow many questions per session? [default: 10]: ", end="")
    raw = input().strip()
    if not raw:
        return 10
    try:
        n = int(raw)
        return max(1, min(n, 200))
    except ValueError:
        return 10


def run_session():
    categories = select_categories()
    difficulty = select_difficulty()
    session_length = select_session_length()

    score = 0
    total = 0

    print()
    _header(f"Starting session: {session_length} questions")
    print(f"  Categories : {', '.join(CATEGORIES[c] for c in categories)}")
    print(f"  Difficulty : {difficulty.capitalize()}")
    print(f"\n  Type your answer and press Enter.")
    print(f"  Type 'skip' to skip, 'quit' or 'q' to end session early.\n")

    for i in range(1, session_length + 1):
        cat_key = RNG.choice(categories)
        diff = RNG.choice(DIFFICULTIES) if difficulty == "mixed" else difficulty

        # Retry up to 5 times to avoid degenerate problems
        for _ in range(5):
            try:
                problem = generate_problem(cat_key, diff)
                break
            except Exception:
                continue
        else:
            continue

        display_problem(problem, i, score)

        raw = input("  Your answer: ").strip()

        if raw.lower() in ("quit", "q", "exit"):
            print(_yellow("\n  Session ended early."))
            break
        if raw.lower() in ("skip", "s", ""):
            total += 1
            print(_yellow(f"  Skipped. Answer: {problem['answer_str']}"))
            print(f"  {_yellow('Explanation:')} {problem['explanation']}")
            print(f"  Score: {_bold(f'{score}/{total}')}\n")
            continue

        total += 1
        is_correct, feedback = check_answer(raw, problem)
        if is_correct:
            score += 1

        display_result(is_correct, feedback, problem["explanation"], score, total)

    # Final summary
    _divider()
    _header("Session Complete")
    if total > 0:
        pct = score / total * 100
        bar_len = 30
        filled = int(bar_len * score / total)
        bar = "█" * filled + "░" * (bar_len - filled)
        print(f"\n  Final score : {_bold(f'{score}/{total}')}  ({pct:.1f}%)")
        print(f"  [{_green(bar[:filled])}{bar[filled:]}]")
        if pct >= 85:
            print(f"\n  {_green('Excellent work! Quant-ready.')} ")
        elif pct >= 60:
            print(f"\n  {_yellow('Good effort — keep drilling the weak spots.')}")
        else:
            print(f"\n  {_red('Keep practising — consistency is key.')}")
    print()

    again = input("  Play again? [y/N]: ").strip().lower()
    if again in ("y", "yes"):
        run_session()


# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------

def main():
    # Enable ANSI on Windows
    if sys.platform == "win32":
        try:
            import ctypes
            kernel32 = ctypes.windll.kernel32
            kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
        except Exception:
            pass

    try:
        run_session()
    except KeyboardInterrupt:
        print(_yellow("\n\n  Interrupted. See you next time!\n"))


if __name__ == "__main__":
    main()
