"""
Number Sequence Practice Tool
Usage: python sequences.py [--time <minutes>]
"""

from __future__ import annotations

import argparse
import math
import random
import time
from dataclasses import dataclass, field


# ===========================================================================
# Data model
# ===========================================================================

@dataclass
class Sequence:
    terms: list[int | float]
    name: str
    tier: int
    rule: str
    explanation: str
    next_term: int | float
    params: dict = field(default_factory=dict)


# ===========================================================================
# Tier 1 – Arithmetic & Basic
# ===========================================================================

def gen_arithmetic(n: int = 0, start: int | None = None, difference: int | None = None) -> Sequence:
    if n == 0: n = random.randint(5, 6)
    if start is None: start = random.randint(1, 20)
    if difference is None: difference = random.randint(2, 12)
    terms = [start + i * difference for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Arithmetic (Linear)",
        tier=1,
        rule="aₙ = a₁ + (n-1)·d",
        explanation=(
            f"Each term increases by a constant difference of {difference}. "
            "To identify: compute consecutive differences — they are all equal. "
            "To find the next term, simply add the common difference to the last term."
        ),
        next_term=terms[n],
        params={"start": start, "difference": difference},
    )


def gen_geometric(n: int = 0, start: int | None = None, ratio: int | None = None) -> Sequence:
    if n == 0: n = random.randint(5, 6)
    if start is None: start = random.randint(1, 5)
    if ratio is None: ratio = random.randint(2, 4)
    terms = [start * (ratio ** i) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Geometric",
        tier=1,
        rule="aₙ = a₁ · rⁿ⁻¹",
        explanation=(
            f"Each term is multiplied by a constant ratio of {ratio}. "
            "To identify: divide consecutive terms — the ratio is constant. "
            "Multiply the last term by the ratio to get the next."
        ),
        next_term=terms[n],
        params={"start": start, "ratio": ratio},
    )


def gen_alternating_sign(n: int = 0, start: int | None = None, difference: int | None = None) -> Sequence:
    if n == 0: n = random.randint(5, 6)
    if start is None: start = random.randint(1, 10)
    if difference is None: difference = random.randint(1, 8)
    terms = [(((-1) ** i) * (start + i * difference)) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Alternating Sign",
        tier=1,
        rule="aₙ = (-1)ⁿ · (a + n·d)",
        explanation=(
            "The signs alternate between positive and negative each term. "
            "To identify: check that consecutive terms alternate in sign. "
            "Negate the last term's sign and apply the underlying arithmetic step."
        ),
        next_term=terms[n],
        params={"start": start, "difference": difference},
    )

# ===========================================================================
# Tier 2 – Polynomial & Power-Based
# ===========================================================================

def gen_quadratic(
    n: int = 0, a: int | None = None, b: int | None = None, c: int | None = None, start_n: int | None = None
) -> Sequence:
    """General quadratic: aₙ = a·n² + b·n + c."""
    if n == 0: n = random.randint(5, 6)
    if a is None: a = random.randint(1, 3)
    if b is None: b = random.randint(0, 4)
    if c is None: c = random.randint(0, 10)
    if start_n is None: start_n = random.randint(1, 5)
    def _term(k):
        return a * k ** 2 + b * k + c
    terms = [_term(start_n + i) for i in range(n + 1)]
    rule = f"aₙ = {a}n²" + (f" + {b}n" if b else "") + (f" + {c}" if c else "")
    return Sequence(
        terms=terms[:n],
        name="General Quadratic",
        tier=2,
        rule=rule,
        explanation=(
            f"Each term follows a quadratic formula: {rule}. "
            "To identify: the second differences of consecutive terms are constant (= 2a). "
            "Calculate next first difference and add it to the last term to get the next term."
        ),
        next_term=terms[n],
        params={"a": a, "b": b, "c": c, "start_n": start_n},
    )


def gen_cubic(
    n: int = 0, a: int | None = None, b: int | None = None, c: int | None = None, d: int | None = None, start_n: int | None = None
) -> Sequence:
    """General cubic: aₙ = a·n³ + b·n² + c·n + d."""
    if n == 0: n = random.randint(5, 6)
    if a is None: a = 1  # fixed to avoid extreme growth
    if b is None: b = random.randint(0, 3)
    if c is None: c = random.randint(0, 5)
    if d is None: d = random.randint(0, 10)
    if start_n is None: start_n = random.randint(1, 4)
    def _term(k):
        return a * k ** 3 + b * k ** 2 + c * k + d
    terms = [_term(start_n + i) for i in range(n + 1)]
    rule = f"aₙ = {a}n³" + (f" + {b}n²" if b else "") + (f" + {c}n" if c else "") + (f" + {d}" if d else "")
    return Sequence(
        terms=terms[:n],
        name="General Cubic",
        tier=2,
        rule=rule,
        explanation=(
            f"Each term follows a cubic formula: {rule}. "
            "To identify: the third differences of consecutive terms are constant (= 6a). "
            "Calculate next second difference, then next first difference, and add it to the last term to get the next term."
        ),
        next_term=terms[n],
        params={"a": a, "b": b, "c": c, "d": d, "start_n": start_n},
    )

def gen_perfect_powers(n: int = 0, k: int | None = None, start_n: int | None = None) -> Sequence:
    if n == 0: n = random.randint(5, 6)
    if k is None: k = random.randint(3, 5)
    if start_n is None: start_n = random.randint(1, 3)
    terms = [(start_n + i) ** k for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name=f"Perfect Powers (n^{k})",
        tier=2,
        rule=f"aₙ = n^{k}",
        explanation=(
            f"Each term is the index raised to the power {k}. "
            f"To identify: take k-th roots of each term — they should be consecutive integers. "
            f"Raise the next integer to the power {k}."
        ),
        next_term=terms[n],
        params={"k": k, "start_n": start_n},
    )


# ===========================================================================
# Tier 3 – Recurrence Relations
# ===========================================================================

def gen_fibonacci(n: int = 0) -> Sequence:
    if n == 0: n = random.randint(6, 8)
    terms = [1, 1]
    while len(terms) < n + 1:
        terms.append(terms[-1] + terms[-2])
    return Sequence(
        terms=terms[:n],
        name="Fibonacci",
        tier=3,
        rule="aₙ = aₙ₋₁ + aₙ₋₂, a₁=1, a₂=1",
        explanation=(
            "Each term is the sum of the two preceding terms. "
            "To identify: consecutive ratios converge to the golden ratio (~1.618). "
            "Add the last two visible terms to get the next."
        ),
        next_term=terms[n],
        params={},
    )


def gen_lucas(n: int = 0) -> Sequence:
    if n == 0: n = random.randint(6, 8)
    terms = [2, 1]
    while len(terms) < n + 1:
        terms.append(terms[-1] + terms[-2])
    return Sequence(
        terms=terms[:n],
        name="Lucas",
        tier=3,
        rule="aₙ = aₙ₋₁ + aₙ₋₂, a₁=2, a₂=1",
        explanation=(
            "Like Fibonacci but starting with 2 and 1 instead of 1 and 1. "
            "To identify: ratios still converge to the golden ratio; look for the 2, 1 seed. "
            "Add the last two terms."
        ),
        next_term=terms[n],
        params={},
    )


def gen_tribonacci(n: int = 0) -> Sequence:
    if n == 0: n = random.randint(7, 9)
    terms = [0, 0, 1]
    while len(terms) < n + 1:
        terms.append(terms[-1] + terms[-2] + terms[-3])
    return Sequence(
        terms=terms[:n],
        name="Tribonacci",
        tier=3,
        rule="aₙ = aₙ₋₁ + aₙ₋₂ + aₙ₋₃, a₁=0, a₂=1, a₃=1",
        explanation=(
            "Each term is the sum of the three preceding terms. "
            "To identify: growth is faster than Fibonacci and differences between terms grow quickly. "
            "Sum the last three visible terms."
        ),
        next_term=terms[n],
        params={},
    )


def gen_linear_recurrence(
    n: int = 0, p: int | None = None, q: int | None = None, a1: int | None = None, a2: int | None = None
) -> Sequence:
    if n == 0: n = random.randint(7, 9)
    if p is None: p = random.randint(1, 3)
    if q is None: q = random.choice([-2, -1, 0, 1])
    if a1 is None: a1 = random.randint(1, 5)
    if a2 is None: a2 = random.randint(2, 10)
    terms = [a1, a2]
    while len(terms) < n + 1:
        terms.append(p * terms[-1] + q * terms[-2])
    return Sequence(
        terms=terms[:n],
        name="General Linear Recurrence",
        tier=3,
        rule=f"aₙ = {p}*aₙ₋₁ + ({q})*aₙ₋₂",
        explanation=(
            f"Each term is computed as {p}*(previous) + ({q})*(term before that). "
            "To identify: check if a fixed linear combination of the last two terms reproduces the sequence. "
            f"Apply the recurrence: {p}*last + ({q})*second-to-last."
        ),
        next_term=terms[n],
        params={"p": p, "q": q, "a1": a1, "a2": a2},
    )


def gen_padovan(n: int = 0) -> Sequence:
    if n == 0: n = random.randint(8, 10)
    terms = [1, 1, 1]
    while len(terms) < n + 1:
        terms.append(terms[-2] + terms[-3])
    return Sequence(
        terms=terms[:n],
        name="Padovan",
        tier=3,
        rule="aₙ = aₙ₋₂ + aₙ₋₃, a₁=a₂=a₃=1",
        explanation=(
            "Each term is the sum of the term two positions back and the term three positions back. "
            "To identify: unlike Fibonacci, you skip the immediate predecessor. "
            "Add the term at position n-2 and n-3 among visible terms."
        ),
        next_term=terms[n],
        params={},
    )


# ===========================================================================
# Tier 4 – Multiplicative & Factorial
# ===========================================================================

def _factorial(k: int) -> int:
    return math.factorial(k)


def gen_factorial(n: int = 0, start_n: int | None = None) -> Sequence:
    if n == 0: n = random.randint(5, 6)
    if start_n is None: start_n = random.randint(1, 4)
    terms = [_factorial(start_n + i) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Factorials (n!)",
        tier=4,
        rule="aₙ = n!",
        explanation=(
            "Each term is the factorial of its index: n! = n*(n-1)*(n-2)*…*1."
            "To identify: each term divided by the previous gives consecutive integers. "
            "Multiply the last term by the next index."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


# ===========================================================================
# Tier 5 – Prime & Number Theory
# ===========================================================================

def _sieve(limit: int) -> list[int]:
    is_p = [True] * (limit + 1)
    is_p[0] = is_p[1] = False
    for i in range(2, int(limit**0.5) + 1):
        if is_p[i]:
            for j in range(i * i, limit + 1, i):
                is_p[j] = False
    return [i for i in range(limit + 1) if is_p[i]]


_PRIMES = _sieve(10_000)


def gen_primes(n: int = 0, start_idx: int | None = None) -> Sequence:
    if n == 0: n = random.randint(6, 8)
    if start_idx is None: start_idx = random.randint(0, 30)
    terms = _PRIMES[start_idx: start_idx + n + 1]
    return Sequence(
        terms=terms[:n],
        name="Prime Numbers",
        tier=5,
        rule="aₙ = nth prime",
        explanation=(
            "Each term is a prime number — divisible only by 1 and itself. "
            "To identify: check that no term is composite. "
            "Find the next integer greater than the last term that has no divisors other than 1 and itself."
        ),
        next_term=terms[n],
        params={"start_idx": start_idx},
    )


def _digit_sum(x: int) -> int:
    return sum(int(d) for d in str(abs(x)))


def gen_digit_sum(n: int = 0, start_n: int | None = None) -> Sequence:
    if n == 0: n = random.randint(7, 9)
    if start_n is None: start_n = random.randint(1, 50)
    terms = [_digit_sum(start_n + i) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Sum of Digits of n",
        tier=5,
        rule="aₙ = sum of digits of n",
        explanation=(
            "Each term is the sum of the decimal digits of the corresponding index. "
            "To identify: values reset downward when crossing multiples of 10, fully resetting at powers of 10. "
            "Sum the digits of the next index value."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


# ===========================================================================
# Tier 6 – Positional / Index-Based
# ===========================================================================

# Subsequence builders used by gen_two_interleaved
_SUBSEQ_TYPES = [
    ("arithmetic",  lambda start, p, k: start + k * p),
    ("geometric",   lambda start, p, k: start * (p ** k)),
    ("quadratic",   lambda start, p, k: start + p * (k + 1) ** 2),
    ("triangular",  lambda start, p, k: start + (k + 1) * (k + 2) // 2),
    ("powers of 2", lambda start, p, k: start * (2 ** k)),
]


def gen_two_interleaved(n: int = 0) -> Sequence:
    """
    Interleave two independently generated subsequences of (possibly) different types.
    The subsequence types and parameters are chosen at random each call.
    """
    if n == 0: n = random.randint(8, 10)
    type_a, fn_a = random.choice(_SUBSEQ_TYPES)
    type_b, fn_b = random.choice(_SUBSEQ_TYPES)

    start_a = random.randint(1, 10)
    start_b = random.randint(1, 10)
    param_a = random.randint(2, 5)   # difference / ratio / coefficient
    param_b = random.randint(2, 5)

    need = (n + 2) // 2 + 1
    seq_a = [fn_a(start_a, param_a, k) for k in range(need)]
    seq_b = [fn_b(start_b, param_b, k) for k in range(need)]

    terms = []
    ia = ib = 0
    for i in range(n + 1):
        if i % 2 == 0:
            terms.append(seq_a[ia]); ia += 1
        else:
            terms.append(seq_b[ib]); ib += 1

    return Sequence(
        terms=terms[:n],
        name="Two Interleaved Subsequences",
        tier=6,
        rule=f"odd positions: {type_a} seq; even positions: {type_b} seq",
        explanation=(
            f"Odd-positioned terms follow a {type_a} pattern; "
            f"even-positioned terms follow a {type_b} pattern. "
            "To identify: separate the sequence into two groups by alternating index and analyse each independently. "
            "Extend whichever group corresponds to the next position."
        ),
        next_term=terms[n],
        params={"type_a": type_a, "type_b": type_b,
                "start_a": start_a, "param_a": param_a,
                "start_b": start_b, "param_b": param_b},
    )


def gen_triangular_recurrence(n: int = 0, start: int | None = None) -> Sequence:
    """aₙ = aₙ₋₁ + n, starting from index 1."""
    if n == 0: n = random.randint(6, 8)
    if start is None: start = random.randint(0, 15)
    terms = [start]
    for i in range(1, n + 1):
        terms.append(terms[-1] + i)
    return Sequence(
        terms=terms[:n],
        name="Triangular-Like Recurrence (aₙ = aₙ₋₁ + n)",
        tier=6,
        rule="aₙ = aₙ₋₁ + n",
        explanation=(
            "Each term is obtained by adding its position index to the previous term. "
            "To identify: first differences are 1, 2, 3, 4, … (consecutive integers). "
            "Add the next index value to the last term."
        ),
        next_term=terms[n],
        params={"start": start},
    )


def gen_factorial_recurrence(n: int = 0, start: int | None = None) -> Sequence:
    """aₙ = n * aₙ₋₁."""
    if n == 0: n = random.randint(5, 6)
    if start is None: start = random.randint(1, 3)
    terms = [start]
    for i in range(2, n + 2):
        terms.append(i * terms[-1])
    return Sequence(
        terms=terms[:n],
        name="Factorial Recurrence (aₙ = n * aₙ₋₁)",
        tier=6,
        rule="aₙ = n * aₙ₋₁",
        explanation=(
            "Each term is the previous term multiplied by the current index. "
            "To identify: the ratio of consecutive terms increases by 1 each step. "
            "Multiply the last term by the next index."
        ),
        next_term=terms[n],
        params={"start": start},
    )


# ===========================================================================
# Tier 7 – Combinatorial
# ===========================================================================

def gen_binomial(n: int = 0, k: int | None = None, start_n: int | None = None) -> Sequence:
    if n == 0: n = random.randint(6, 8)
    if k is None: k = random.randint(2, 4)
    if start_n is None: start_n = k + random.randint(0, 3)  # ensure non-trivial starting terms
    terms = [math.comb(start_n + i, k) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name=f"Binomial Coefficients C(n,{k})",
        tier=7,
        rule=f"aₙ = C(n,{k}) = n! / ({k}! * (n-{k})!)",
        explanation=(
            f"Each term is the binomial coefficient C(n, {k}) — the number of ways to choose {k} items from n. "
            "To identify: differences of order k become constant. "
            f"Increment n and compute C(n+1, {k})."
        ),
        next_term=terms[n],
        params={"k": k, "start_n": start_n},
    )


# ===========================================================================
# Tier 8 – Hybrid
# ===========================================================================

def gen_hybrid_alternating_linear(n: int = 0, start_n: int | None = None) -> Sequence:
    """a_n = (-1)^(n+1) * n — linear magnitude with alternating sign."""
    if n == 0: n = random.randint(6, 8)
    if start_n is None: start_n = random.randint(1, 8)
    terms = [((-1) ** (i + 1)) * (start_n + i) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Alternating Linear",
        tier=8,
        rule="aₙ = (-1)^(n+1) · n",
        explanation=(
            "The absolute values form a linear (arithmetic) sequence while the signs alternate each term. "
            "To identify: take absolute values — they increase by 1; signs flip each step. "
            "Negate the last term's sign and add 1 to its absolute value."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def gen_hybrid_polynomial_exponential(n: int = 0, start_n: int | None = None) -> Sequence:
    """a_n = n² · 2^n — quadratic envelope on exponential growth."""
    if n == 0: n = random.randint(5, 7)
    if start_n is None: start_n = random.randint(1, 4)
    terms = [(start_n + i) ** 2 * (2 ** (start_n + i)) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Polynomial × Exponential",
        tier=8,
        rule="aₙ = n² · 2ⁿ",
        explanation=(
            "Each term combines a quadratic factor (n²) with exponential growth (2ⁿ). "
            "To identify: divide consecutive terms — the ratio is not constant but grows; "
            "dividing out the exponential leaves a polynomial. "
            "Compute (n+1)² · 2^(n+1) for the next term."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def gen_hybrid_alternating_geometric(n: int = 0, r: int | None = None, start_n: int | None = None) -> Sequence:
    """a_n = (-r)^n — geometric sequence with alternating sign baked in."""
    if n == 0: n = random.randint(6, 8)
    if r is None: r = random.randint(2, 4)
    if start_n is None: start_n = random.randint(0, 3)
    terms = [((-r) ** (start_n + i)) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Alternating Geometric",
        tier=8,
        rule=f"aₙ = (-{r})ⁿ",
        explanation=(
            f"Each term is a power of -{r}, so the sequence grows geometrically in magnitude "
            f"(ratio = {r}) while alternating in sign. "
            "To identify: absolute values form a geometric sequence; signs alternate. "
            f"Multiply the last term by -{r}."
        ),
        next_term=terms[n],
        params={"r": r, "start_n": start_n},
    )


def gen_hybrid_factorial_polynomial(n: int = 0, start_n: int | None = None) -> Sequence:
    """a_n = n! · n — factorial scaled by the index."""
    if n == 0: n = random.randint(5, 6)
    if start_n is None: start_n = random.randint(1, 4)
    terms = [math.factorial(start_n + i) * (start_n + i) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Factorial * Polynomial",
        tier=8,
        rule="aₙ = n! · n",
        explanation=(
            "Each term is the factorial of the index multiplied by the index itself. "
            "To identify: ratios between consecutive terms are not integer but grow quickly; "
            "dividing each term by its index reveals factorials. "
            "Compute (n+1)! · (n+1) for the next term."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def gen_hybrid_polynomial_periodic(n: int = 0, start_n: int | None = None) -> Sequence:
    """a_n = n² + (-1)^n — quadratic with alternating ±1 perturbation."""
    if n == 0: n = random.randint(6, 8)
    if start_n is None: start_n = random.randint(1, 5)
    terms = [(start_n + i) ** 2 + ((-1) ** (start_n + i)) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Polynomial + Periodic Perturbation",
        tier=8,
        rule="aₙ = n² + (-1)ⁿ",
        explanation=(
            "The dominant trend is quadratic (n²), with a ±1 alternating perturbation added each term. "
            "To identify: second differences are nearly constant (≈ 2) but consecutive terms alternate "
            "between being 1 above and 1 below the pure quadratic. "
            "Compute (n+1)² and add +1 or -1 depending on parity of n+1."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def gen_hybrid_binomial_exponential(n: int = 0, start_n: int | None = None) -> Sequence:
    """a_n = 2^n · C(n, 2) — binomial coefficient scaled by exponential."""
    if n == 0: n = random.randint(5, 7)
    if start_n is None: start_n = 2 + random.randint(0, 3)  # C(n,2) needs n >= 2
    terms = [(2 ** (start_n + i)) * math.comb(start_n + i, 2) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Binomial * Exponential",
        tier=8,
        rule="aₙ = 2ⁿ · C(n,2)",
        explanation=(
            "Each term combines exponential growth (2ⁿ) with the binomial coefficient C(n,2) = n(n-1)/2. "
            "To identify: divide consecutive terms — the ratio is not constant; "
            "factor out the exponential to reveal the binomial pattern. "
            "Compute 2^(n+1) · C(n+1, 2) for the next term."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def gen_hybrid_digit_sum_shift(n: int = 0, start_n: int | None = None) -> Sequence:
    """a_n = n + digit_sum(n) — index plus sum of its own digits."""
    if n == 0: n = random.randint(6, 8)
    if start_n is None: start_n = random.randint(1, 50)
    def _val(k): return k + sum(int(d) for d in str(k))
    terms = [_val(start_n + i) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Digit Sum Shift",
        tier=8,
        rule="aₙ = n + S(n)  where S(n) = sum of digits of n",
        explanation=(
            "Each term is the index plus the sum of its own digits. "
            "To identify: differences between consecutive terms are mostly constant but "
            "drop sharply when crossing a multiple of 10 (digit sum resets). "
            "Compute n+1 and add its digit sum."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


# ===========================================================================
# SequenceBank
# ===========================================================================

# Registry: one callable per generator with default parameters
_ALL_GENERATORS = [
    # Tier 1
    gen_arithmetic,
    gen_geometric,
    gen_alternating_sign,
    # Tier 2
    gen_quadratic,
    gen_cubic,
    gen_perfect_powers,
    # Tier 3
    gen_fibonacci,
    gen_lucas,
    gen_tribonacci,
    gen_linear_recurrence,
    gen_padovan,
    # Tier 4
    gen_factorial,
    # Tier 5
    gen_primes,
    gen_digit_sum,
    # Tier 6
    gen_two_interleaved,
    gen_triangular_recurrence,
    gen_factorial_recurrence,
    # Tier 7
    gen_binomial,
    # Tier 8
    gen_hybrid_alternating_linear,
    gen_hybrid_polynomial_exponential,
    gen_hybrid_alternating_geometric,
    gen_hybrid_factorial_polynomial,
    gen_hybrid_polynomial_periodic,
    gen_hybrid_binomial_exponential,
    gen_hybrid_digit_sum_shift,
]


class SequenceBank:
    """Central registry for all sequence generators."""

    def get_all(self) -> list[Sequence]:
        """Return one instance of every sequence type with default parameters."""
        return [g() for g in _ALL_GENERATORS]

    def get_by_tier(self, tier: int) -> list[Sequence]:
        """Return all sequences belonging to the given difficulty tier."""
        return [s for s in self.get_all() if s.tier == tier]

    def get_random(self, tier: int | None = None) -> Sequence:
        """Return a randomly chosen sequence, optionally filtered by tier."""
        pool = self.get_by_tier(tier) if tier is not None else self.get_all()
        return random.choice(pool)

    def get_random_challenge(self, tier: int | None = None) -> dict:
        """
        Return a quiz-ready dict with visible terms and deferred answer.

        Keys: terms, answer, name, rule, explanation
        """
        seq = self.get_random(tier)
        return {
            "terms": seq.terms,
            "answer": seq.next_term,
            "name": seq.name,
            "rule": seq.rule,
            "explanation": seq.explanation,
        }


# ===========================================================================
# Session logic (practice tool)
# ===========================================================================

_bank = SequenceBank()


def generate_sequence() -> tuple[list[int | float], int | float, str]:
    """
    Pick a random sequence and return (terms, next_term, explanation).
    This is the hook used by the timed practice session.
    """
    seq = _bank.get_random()
    return seq.terms, seq.next_term, seq.explanation


def ask_question(
    terms: list, answer: int | float, explanation: str, show_explanation: bool
) -> tuple[bool, float]:
    """
    Present a single sequence question.

    Returns:
        correct       – whether the user answered correctly
        paused_secs   – seconds spent reading the explanation (to add back to deadline)
    """
    display = "  ".join(str(t) for t in terms)
    try:
        raw = input(f"\n{display}  ___ ? ").strip()
        user_answer = float(raw)
    except (ValueError, EOFError):
        print("  Invalid input — skipping.")
        return False, 0.0

    correct = abs(user_answer - answer) < 1e-9
    if correct:
        print("  Correct!")
    else:
        print(f"  Wrong. The answer was {answer}.")

    paused_secs = 0.0
    if show_explanation:
        print(f"  Explanation: {explanation}")
        pause_start = time.time()
        input("  [Timer paused — press Enter to continue]")
        paused_secs = time.time() - pause_start

    return correct, paused_secs


def run_session(time_limit_minutes: int, show_explanation: bool) -> None:
    """Run a timed practice session and print a summary at the end."""
    time_limit_seconds = time_limit_minutes * 60
    mode_label = "learning (timer pauses on explanation)" if show_explanation else "hardcore (no explanations)"
    print(f"\nMode: {mode_label}")
    print(f"Time limit: {time_limit_minutes} minute(s).")
    print("Type the next number in each sequence and press Enter.")
    print("Press Ctrl+C at any time to stop early.\n")

    correct_count = 0
    total_count = 0
    deadline = time.time() + time_limit_seconds

    try:
        while time.time() < deadline:
            remaining = deadline - time.time()
            mins, secs = divmod(int(remaining), 60)
            print(f"[{mins}m {secs:02d}s remaining]", end="")

            terms, answer, explanation = generate_sequence()
            total_count += 1
            correct, paused_secs = ask_question(terms, answer, explanation, show_explanation)
            if correct:
                correct_count += 1
            # Pause reading time does not count against the player
            deadline += paused_secs

    except KeyboardInterrupt:
        print("\n\nSession interrupted.")

    print(f"\n--- Results: {correct_count} / {total_count} correct ---\n")


# ===========================================================================
# Entry point
# ===========================================================================

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Number sequence practice for quantitative finance assessments."
    )
    parser.add_argument(
        "--time", "-t",
        type=int,
        default=5,
        metavar="MINUTES",
        help="Time limit for the practice session in minutes (default: 5).",
    )
    parser.add_argument(
        "--mode", "-m",
        choices=["hardcore", "learning"],
        default="hardcore",
        help=(
            "Practice mode: 'hardcore' = no explanations, full time pressure; "
            "'learning' = explanation shown after each answer, timer pauses while reading (default: hardcore)."
        ),
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    run_session(time_limit_minutes=args.time, show_explanation=(args.mode == "learning"))


