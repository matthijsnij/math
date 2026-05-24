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

def gen_arithmetic(n: int = 6, start: int = 1, difference: int = 3) -> Sequence:
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


def gen_geometric(n: int = 6, start: int = 2, ratio: int = 3) -> Sequence:
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


def gen_constant(n: int = 6, value: int = 7) -> Sequence:
    terms = [value] * (n + 1)
    return Sequence(
        terms=terms[:n],
        name="Constant",
        tier=1,
        rule="aₙ = c",
        explanation=(
            f"Every term equals the same constant value ({value}). "
            "To identify: all terms are identical. "
            "The next term is just that same value."
        ),
        next_term=terms[n],
        params={"value": value},
    )


def gen_alternating_sign(n: int = 6, start: int = 1, difference: int = 1) -> Sequence:
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


def gen_two_step_arithmetic(
    n: int = 6, start: int = 1, diff_odd: int = 2, diff_even: int = 5
) -> Sequence:
    terms = []
    val = start
    for i in range(n + 1):
        terms.append(val)
        val += diff_odd if i % 2 == 0 else diff_even
    return Sequence(
        terms=terms[:n],
        name="Two-Step Arithmetic",
        tier=1,
        rule="alternates between two constant differences",
        explanation=(
            f"The sequence alternates between adding {diff_odd} and adding {diff_even}. "
            "To identify: the differences between consecutive terms form a two-value repeating pattern. "
            "Apply whichever difference is next in the alternating cycle."
        ),
        next_term=terms[n],
        params={"start": start, "diff_odd": diff_odd, "diff_even": diff_even},
    )


# ===========================================================================
# Tier 2 – Polynomial & Power-Based
# ===========================================================================

def gen_quadratic(n: int = 6, start_n: int = 1) -> Sequence:
    terms = [(start_n + i) ** 2 for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Quadratic (n²)",
        tier=2,
        rule="aₙ = n²",
        explanation=(
            "Each term is the square of its index. "
            "To identify: second differences of consecutive terms are constant (= 2). "
            "The next term is the square of the next index value."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def gen_cubic(n: int = 6, start_n: int = 1) -> Sequence:
    terms = [(start_n + i) ** 3 for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Cubic (n³)",
        tier=2,
        rule="aₙ = n³",
        explanation=(
            "Each term is the cube of its index. "
            "To identify: third differences of consecutive terms are constant (= 6). "
            "The next term is the cube of the next index."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def gen_triangular(n: int = 6, start_n: int = 1) -> Sequence:
    terms = [(start_n + i) * (start_n + i + 1) // 2 for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Triangular Numbers",
        tier=2,
        rule="aₙ = n(n+1)/2",
        explanation=(
            "Triangular numbers count objects arranged in an equilateral triangle. "
            "To identify: differences between consecutive terms increase by 1 each step (1, 2, 3, …). "
            "Add the next integer to the last term."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def gen_tetrahedral(n: int = 6, start_n: int = 1) -> Sequence:
    terms = [
        (start_n + i) * (start_n + i + 1) * (start_n + i + 2) // 6
        for i in range(n + 1)
    ]
    return Sequence(
        terms=terms[:n],
        name="Tetrahedral Numbers",
        tier=2,
        rule="aₙ = n(n+1)(n+2)/6",
        explanation=(
            "Tetrahedral numbers count spheres in a triangular pyramid. "
            "To identify: they are the partial sums of triangular numbers. "
            "Compute the next triangular number and add it to the last term."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def gen_perfect_powers(n: int = 6, k: int = 4, start_n: int = 1) -> Sequence:
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

def gen_fibonacci(n: int = 6) -> Sequence:
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


def gen_lucas(n: int = 6) -> Sequence:
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


def gen_tribonacci(n: int = 6) -> Sequence:
    terms = [0, 1, 1]
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
    n: int = 6, p: int = 2, q: int = -1, a1: int = 1, a2: int = 3
) -> Sequence:
    terms = [a1, a2]
    while len(terms) < n + 1:
        terms.append(p * terms[-1] + q * terms[-2])
    return Sequence(
        terms=terms[:n],
        name="General Linear Recurrence",
        tier=3,
        rule=f"aₙ = {p}·aₙ₋₁ + ({q})·aₙ₋₂",
        explanation=(
            f"Each term is computed as {p}×(previous) + ({q})×(term before that). "
            "To identify: check if a fixed linear combination of the last two terms reproduces the sequence. "
            f"Apply the recurrence: {p}×last + ({q})×second-to-last."
        ),
        next_term=terms[n],
        params={"p": p, "q": q, "a1": a1, "a2": a2},
    )


def gen_padovan(n: int = 6) -> Sequence:
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


def _double_factorial(k: int) -> int:
    if k <= 0:
        return 1
    result = 1
    while k > 0:
        result *= k
        k -= 2
    return result


def _subfactorial(k: int) -> int:
    if k == 0:
        return 1
    if k == 1:
        return 0
    return (k - 1) * (_subfactorial(k - 1) + _subfactorial(k - 2))


def _catalan(k: int) -> int:
    return math.comb(2 * k, k) // (k + 1)


def _bell(k: int) -> int:
    # Bell triangle method
    if k == 0:
        return 1
    row = [1]
    for _ in range(k):
        new_row = [row[-1]]
        for j in range(len(row)):
            new_row.append(new_row[-1] + row[j])
        row = new_row
    return row[0]


def _primorial(k: int) -> int:
    def is_prime(x):
        if x < 2:
            return False
        for i in range(2, int(x**0.5) + 1):
            if x % i == 0:
                return False
        return True
    primes = [x for x in range(2, 200) if is_prime(x)]
    result = 1
    for p in primes[:k]:
        result *= p
    return result


def gen_factorial(n: int = 6, start_n: int = 1) -> Sequence:
    terms = [_factorial(start_n + i) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Factorials (n!)",
        tier=4,
        rule="aₙ = n!",
        explanation=(
            "Each term is the factorial of its index: n! = 1×2×3×…×n. "
            "To identify: each term divided by the previous gives consecutive integers. "
            "Multiply the last term by the next index."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def gen_double_factorial(n: int = 6, start_n: int = 1) -> Sequence:
    terms = [_double_factorial(start_n + i) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Double Factorials (n!!)",
        tier=4,
        rule="n!! = n·(n-2)·(n-4)·… down to 1 or 2",
        explanation=(
            "The double factorial multiplies every other integer down to 1 (odd) or 2 (even). "
            "To identify: growth is slower than n! since only alternating factors appear. "
            "Multiply the last term by n (skipping one integer)."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def gen_subfactorial(n: int = 6, start_n: int = 0) -> Sequence:
    terms = [_subfactorial(start_n + i) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Subfactorials / Derangements (!n)",
        tier=4,
        rule="!n = (n-1)·(!{n-1} + !{n-2})",
        explanation=(
            "The subfactorial !n counts permutations of n elements with no fixed points (derangements). "
            "To identify: values are close to n!/e. Use the recurrence !n = (n-1)(!{n-1} + !{n-2}). "
            "Apply the recurrence with the last two visible values."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def gen_catalan(n: int = 6, start_n: int = 0) -> Sequence:
    terms = [_catalan(start_n + i) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Catalan Numbers",
        tier=4,
        rule="Cₙ = C(2n,n)/(n+1)",
        explanation=(
            "Catalan numbers count many combinatorial structures (e.g. valid bracket sequences). "
            "To identify: ratios of consecutive terms approach 4. "
            "Compute C(2n, n)/(n+1) for the next index."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def gen_bell(n: int = 6, start_n: int = 0) -> Sequence:
    terms = [_bell(start_n + i) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Bell Numbers",
        tier=4,
        rule="Bₙ = Σ S(n,k) for k=0..n (sum of Stirling 2nd kind)",
        explanation=(
            "Bell numbers count the number of partitions of a set of n elements. "
            "To identify: they grow super-exponentially and can be computed via the Bell triangle. "
            "Build the Bell triangle: start each new row with the last row's last element."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def gen_primorial(n: int = 6, start_n: int = 1) -> Sequence:
    terms = [_primorial(start_n + i) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Primorial (p#)",
        tier=4,
        rule="pₙ# = product of first n primes",
        explanation=(
            "The primorial is the product of the first n prime numbers. "
            "To identify: each term is the previous term multiplied by the next prime. "
            "Identify the next prime and multiply the last term."
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
_PRIME_SET = set(_PRIMES)


def gen_primes(n: int = 6, start_idx: int = 0) -> Sequence:
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


def gen_composites(n: int = 6, start_idx: int = 0) -> Sequence:
    composites = [x for x in range(4, 200) if x not in _PRIME_SET]
    terms = composites[start_idx: start_idx + n + 1]
    return Sequence(
        terms=terms[:n],
        name="Composite Numbers",
        tier=5,
        rule="aₙ = nth composite number",
        explanation=(
            "Each term is a composite number — a positive integer with at least one divisor other than 1 and itself. "
            "To identify: none of the terms are prime. "
            "Find the next non-prime integer after the last term."
        ),
        next_term=terms[n],
        params={"start_idx": start_idx},
    )


def _digit_sum(x: int) -> int:
    return sum(int(d) for d in str(abs(x)))


def gen_digit_sum(n: int = 6, start_n: int = 1) -> Sequence:
    terms = [_digit_sum(start_n + i) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Sum of Digits of n",
        tier=5,
        rule="aₙ = sum of digits of n",
        explanation=(
            "Each term is the sum of the decimal digits of the corresponding index. "
            "To identify: values reset downward when crossing powers of 10. "
            "Sum the digits of the next index value."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def _digital_root(x: int) -> int:
    if x == 0:
        return 0
    return 1 + (x - 1) % 9


def gen_digital_root(n: int = 6, start_n: int = 1) -> Sequence:
    terms = [_digital_root(start_n + i) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Digital Root",
        tier=5,
        rule="aₙ = 1 + (n-1) mod 9",
        explanation=(
            "The digital root is found by repeatedly summing digits until a single digit remains. "
            "To identify: the sequence cycles through 1–9 periodically. "
            "Use the formula: 1 + (n-1) mod 9, or trace the repeating cycle."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def _totient(x: int) -> int:
    result = x
    p = 2
    temp = x
    while p * p <= temp:
        if temp % p == 0:
            while temp % p == 0:
                temp //= p
            result -= result // p
        p += 1
    if temp > 1:
        result -= result // temp
    return result


def gen_totient(n: int = 6, start_n: int = 1) -> Sequence:
    terms = [_totient(start_n + i) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Euler's Totient φ(n)",
        tier=5,
        rule="φ(n) = count of integers ≤ n coprime to n",
        explanation=(
            "Euler's totient φ(n) counts how many integers from 1 to n share no common factor with n. "
            "To identify: for prime p, φ(p) = p−1; values are always even for n > 2. "
            "Factorize n and apply φ(n) = n·∏(1 − 1/p) over prime factors p."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def _divisor_count(x: int) -> int:
    count = 0
    for i in range(1, int(x**0.5) + 1):
        if x % i == 0:
            count += 2 if i != x // i else 1
    return count


def gen_divisor_count(n: int = 6, start_n: int = 1) -> Sequence:
    terms = [_divisor_count(start_n + i) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Divisor Count σ₀(n)",
        tier=5,
        rule="σ₀(n) = number of divisors of n",
        explanation=(
            "Each term counts how many positive integers divide evenly into the corresponding index. "
            "To identify: primes always give 2; highly composite numbers give large values. "
            "Factor the next index and count all divisor pairs."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


# ===========================================================================
# Tier 6 – Positional / Index-Based
# ===========================================================================

def gen_alternating_rule(n: int = 6, start_n: int = 1) -> Sequence:
    """Odd-indexed positions: n, even-indexed positions: n²."""
    terms = []
    for i in range(n + 1):
        idx = start_n + i
        terms.append(idx if idx % 2 != 0 else idx ** 2)
    return Sequence(
        terms=terms[:n],
        name="Alternating Index Rule (odd: n, even: n²)",
        tier=6,
        rule="aₙ = n if n odd, n² if n even",
        explanation=(
            "The rule applied to each term depends on whether its index is odd or even. "
            "To identify: split the sequence into odd- and even-indexed subsequences and look for separate patterns. "
            "Determine the parity of the next index and apply the corresponding rule."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def gen_two_interleaved(
    n: int = 6, start_a: int = 1, diff_a: int = 2, start_b: int = 10, diff_b: int = 3
) -> Sequence:
    seq_a = [start_a + i * diff_a for i in range((n + 2) // 2 + 1)]
    seq_b = [start_b + i * diff_b for i in range((n + 2) // 2 + 1)]
    terms = []
    ia, ib = 0, 0
    for i in range(n + 1):
        if i % 2 == 0:
            terms.append(seq_a[ia]); ia += 1
        else:
            terms.append(seq_b[ib]); ib += 1
    return Sequence(
        terms=terms[:n],
        name="Two Interleaved Arithmetic Subsequences",
        tier=6,
        rule="odd positions: arithmetic seq A; even positions: arithmetic seq B",
        explanation=(
            f"Odd-positioned terms form an arithmetic sequence (start={start_a}, d={diff_a}); "
            f"even-positioned terms form another (start={start_b}, d={diff_b}). "
            "To identify: separate alternate terms into two groups and check each for constant differences. "
            "Extend the appropriate subsequence."
        ),
        next_term=terms[n],
        params={
            "start_a": start_a, "diff_a": diff_a,
            "start_b": start_b, "diff_b": diff_b,
        },
    )


def gen_triangular_recurrence(n: int = 6, start: int = 0) -> Sequence:
    """aₙ = aₙ₋₁ + n, starting from index 1."""
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


def gen_factorial_recurrence(n: int = 6, start: int = 1) -> Sequence:
    """aₙ = n × aₙ₋₁."""
    terms = [start]
    for i in range(2, n + 2):
        terms.append(i * terms[-1])
    return Sequence(
        terms=terms[:n],
        name="Factorial Recurrence (aₙ = n·aₙ₋₁)",
        tier=6,
        rule="aₙ = n · aₙ₋₁",
        explanation=(
            "Each term is the previous term multiplied by the current index. "
            "To identify: the ratio of consecutive terms increases by 1 each step. "
            "Multiply the last term by the next index."
        ),
        next_term=terms[n],
        params={"start": start},
    )


# ===========================================================================
# Tier 7 – Advanced Combinatorial
# ===========================================================================

def gen_binomial(n: int = 6, k: int = 2, start_n: int = 0) -> Sequence:
    terms = [math.comb(start_n + i, k) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name=f"Binomial Coefficients C(n,{k})",
        tier=7,
        rule=f"aₙ = C(n,{k}) = n! / ({k}!·(n-{k})!)",
        explanation=(
            f"Each term is the binomial coefficient C(n, {k}) — the number of ways to choose {k} items from n. "
            "To identify: differences of order k become constant. "
            f"Increment n and compute C(n+1, {k})."
        ),
        next_term=terms[n],
        params={"k": k, "start_n": start_n},
    )


def gen_pascal_diagonal(n: int = 6, diagonal: int = 3, start_n: int = 0) -> Sequence:
    terms = [math.comb(start_n + i + diagonal, diagonal) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name=f"Pascal's Triangle Diagonal {diagonal}",
        tier=7,
        rule=f"aₙ = C(n+{diagonal},{diagonal})",
        explanation=(
            f"This is diagonal {diagonal} of Pascal's triangle, also known as figurate numbers of order {diagonal}. "
            "To identify: consecutive differences eventually become constant at a deeper level. "
            f"Compute C(next_n + {diagonal}, {diagonal})."
        ),
        next_term=terms[n],
        params={"diagonal": diagonal, "start_n": start_n},
    )


def gen_powers_of_2(n: int = 6, start_n: int = 0, offset: int = 0) -> Sequence:
    terms = [2 ** (start_n + i) + offset for i in range(n + 1)]
    label = "Powers of 2" if offset == 0 else f"Powers of 2 + {offset}"
    rule = "aₙ = 2ⁿ" if offset == 0 else f"aₙ = 2ⁿ + {offset}"
    return Sequence(
        terms=terms[:n],
        name=label,
        tier=7,
        rule=rule,
        explanation=(
            f"Each term is a power of 2{f' plus {offset}' if offset else ''}. "
            "To identify: each term is exactly double the previous (after subtracting any offset). "
            "Double the last term (and add back the offset if any)."
        ),
        next_term=terms[n],
        params={"start_n": start_n, "offset": offset},
    )


def gen_lazy_caterer(n: int = 6, start_n: int = 0) -> Sequence:
    terms = [(start_n + i) * (start_n + i + 1) // 2 + 1 for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Lazy Caterer Numbers",
        tier=7,
        rule="aₙ = n(n+1)/2 + 1",
        explanation=(
            "Lazy caterer numbers give the maximum pieces a disk can be cut into with n straight cuts. "
            "To identify: it is one more than the triangular number for the same index. "
            "Compute the next triangular number and add 1."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def _motzkin(k: int) -> int:
    # Recurrence: M(n) = M(n-1) + sum_{i=0}^{n-2} M(i)*M(n-2-i)
    if k == 0 or k == 1:
        return 1
    m = [1, 1]
    for j in range(2, k + 1):
        val = m[j - 1] + sum(m[i] * m[j - 2 - i] for i in range(j - 1))
        m.append(val)
    return m[k]


def gen_motzkin(n: int = 6, start_n: int = 0) -> Sequence:
    terms = [_motzkin(start_n + i) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name="Motzkin Numbers",
        tier=7,
        rule="M(n) = M(n-1) + Σ M(i)·M(n-2-i)",
        explanation=(
            "Motzkin numbers count the number of paths from (0,0) to (n,0) using steps +1, 0, −1 that stay ≥ 0. "
            "To identify: they grow similarly to Catalan numbers but more slowly. "
            "Use the recurrence or look up the known sequence (1,1,2,4,9,21,51,…)."
        ),
        next_term=terms[n],
        params={"start_n": start_n},
    )


def _stirling2(n: int, k: int) -> int:
    if n == 0 and k == 0:
        return 1
    if n == 0 or k == 0:
        return 0
    return k * _stirling2(n - 1, k) + _stirling2(n - 1, k - 1)


def gen_stirling2(n: int = 6, k: int = 2, start_n: int = 2) -> Sequence:
    terms = [_stirling2(start_n + i, k) for i in range(n + 1)]
    return Sequence(
        terms=terms[:n],
        name=f"Stirling Numbers of the 2nd Kind S(n,{k})",
        tier=7,
        rule=f"S(n,{k}) = {k}·S(n-1,{k}) + S(n-1,{k-1})",
        explanation=(
            f"S(n, {k}) counts the number of ways to partition an n-element set into {k} non-empty subsets. "
            "To identify: for fixed k, it grows polynomially in n of degree k. "
            f"Apply the recurrence: {k}×S(n-1,{k}) + S(n-1,{k-1})."
        ),
        next_term=terms[n],
        params={"k": k, "start_n": start_n},
    )


# ===========================================================================
# SequenceBank
# ===========================================================================

# Registry: one callable per generator with default parameters
_ALL_GENERATORS = [
    # Tier 1
    gen_arithmetic,
    gen_geometric,
    gen_constant,
    gen_alternating_sign,
    gen_two_step_arithmetic,
    # Tier 2
    gen_quadratic,
    gen_cubic,
    gen_triangular,
    gen_tetrahedral,
    gen_perfect_powers,
    # Tier 3
    gen_fibonacci,
    gen_lucas,
    gen_tribonacci,
    gen_linear_recurrence,
    gen_padovan,
    # Tier 4
    gen_factorial,
    gen_double_factorial,
    gen_subfactorial,
    gen_catalan,
    gen_bell,
    gen_primorial,
    # Tier 5
    gen_primes,
    gen_composites,
    gen_digit_sum,
    gen_digital_root,
    gen_totient,
    gen_divisor_count,
    # Tier 6
    gen_alternating_rule,
    gen_two_interleaved,
    gen_triangular_recurrence,
    gen_factorial_recurrence,
    # Tier 7
    gen_binomial,
    gen_pascal_diagonal,
    gen_powers_of_2,
    gen_lazy_caterer,
    gen_motzkin,
    gen_stirling2,
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


def ask_question(terms: list, answer: int | float, explanation: str) -> bool:
    """Present a single sequence question and return True if the user is correct."""
    display = "  ".join(str(t) for t in terms)
    try:
        raw = input(f"\n{display}  ___ ? ").strip()
        user_answer = float(raw)
    except (ValueError, EOFError):
        print("  Invalid input — skipping.")
        return False

    correct = abs(user_answer - answer) < 1e-9
    if correct:
        print("  Correct!")
    else:
        print(f"  Wrong. The answer was {answer}.")
    print(f"  Explanation: {explanation}")
    return correct


def run_session(time_limit_minutes: int) -> None:
    """Run a timed practice session and print a summary at the end."""
    time_limit_seconds = time_limit_minutes * 60
    print(f"\nStarting practice session — time limit: {time_limit_minutes} minute(s).")
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
            if ask_question(terms, answer, explanation):
                correct_count += 1

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
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # ------------------------------------------------------------------
    # Demo: one example from every tier
    # ------------------------------------------------------------------
    bank = SequenceBank()
    print("=" * 60)
    print("SEQUENCE SHOWCASE — one example per tier")
    print("=" * 60)
    shown_tiers: set[int] = set()
    for seq in bank.get_all():
        if seq.tier in shown_tiers:
            continue
        shown_tiers.add(seq.tier)
        print(f"\n[Tier {seq.tier}] {seq.name}")
        print(f"  Terms      : {seq.terms}")
        print(f"  Rule       : {seq.rule}")
        print(f"  Explanation: {seq.explanation}")
        print(f"  Next term  : {seq.next_term}")

    # ------------------------------------------------------------------
    # Demo: 3 random challenges (answer hidden, then revealed)
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    print("RANDOM CHALLENGES — try to guess before the reveal!")
    print("=" * 60)
    for i in range(1, 4):
        challenge = bank.get_random_challenge()
        print(f"\nChallenge {i}: {challenge['terms']}  ___")
        input("  Press Enter to reveal the answer...")
        print(f"  Answer     : {challenge['answer']}")
        print(f"  Name       : {challenge['name']}")
        print(f"  Rule       : {challenge['rule']}")
        print(f"  Explanation: {challenge['explanation']}")

    # ------------------------------------------------------------------
    # Timed practice session
    # ------------------------------------------------------------------
    print("\n" + "=" * 60)
    run_session(time_limit_minutes=args.time)

