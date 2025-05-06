import requests
import json 


cmo_problems = [
  {
    "problem_number": 1,
    "question": "n players stand in a circle and each initially votes for the person on their left. In each of n rounds, each player updates their vote such that if a votes for b and b votes for c, then a changes their vote to c. Prove that after n rounds, all players vote for the same person.",
    "solution": "We prove that after ⌊log2 n⌋ rounds the voting graph becomes a self-loop and then all players' votes converge to this loop within another ⌈log2 n⌉ rounds. Detailed argument involves cycle reduction and path halving logic. Thus, within n rounds, all players vote for the same person."
  },
  {
    "problem_number": 2,
    "question": "Determine all positive integers a, b, c, p where p and p + 2 are odd primes and 2^a * p^b = (p + 2)^c − 1.",
    "solution": "The only solution is (a, b, c, p) = (3, 1, 2, 3). The right side is factored, and constraints on p and p+2 being twin primes are used. Eventually we reduce to 2^a * 3^b = 5^2 − 1 = 24, implying a = 3, b = 1, c = 2, p = 3."
  },
  {
    "problem_number": 3,
    "question": "Let ℓ ≥ 2 be an integer and p(x) a polynomial with integer coefficients. Prove that there exist reflexive polynomials q(x), r(x) such that (1 + x + ... + x^{ℓ−1})p(x) = q(x) + x^ℓ * r(x).",
    "solution": "Two solutions are provided. One is constructive using polynomial identities and reflexive definitions (p(x) = x^n * p(1/x)). The second uses matrix representation and shows how q and r can be built from trapezoidal and symmetric matrix structures."
  },
  {
    "problem_number": 4,
    "question": "In triangle ABC with circumcircle Γ and AB ≠ AC, points D and E lie on arc BC not containing A such that ∠BAE = ∠DAC. Let X, Y be incenters of triangles BAE and CAD. External tangents of their incircles intersect at Z. Prove Z lies on the common chord of Γ and the circumcircle of triangle AXY.",
    "solution": "Using spiral similarity and incenter angle properties, we prove that Z lies on the external angle bisector of ∠XAY, which also contains the intersection point N of circles (ABC) and (AXY), so A, Z, N are collinear."
  },
  {
    "problem_number": 5,
    "question": "A rectangle R is divided into smaller rectangles such that no three share a corner. An ant starts at the bottom-left corner and can move to adjacent corners of selected rectangles. Show that if the ant reaches the top-right corner, then some rectangle was used in at least two moves.",
    "solution": "Multiple proofs are provided. One uses arc-based connectivity to show that without repeated rectangles, no corner-to-corner path exists. Another uses move invariants (like direction and side used). A third argument proves that the motion must eventually violate the non-overlap condition unless a rectangle is reused."
  }
]

cjmo_problems = [
  {
    "problem_number": 1,
    "question": "Suppose an infinite non-constant arithmetic progression of integers contains 1. Prove that there are an infinite number of perfect cubes in this progression.",
    "solution": "Let a and d be the first term and common difference. Consider numbers of the form (1 + kd)^3. These expand to 1 + d × integer. Hence, infinitely many perfect cubes lie in the arithmetic progression."
  },
  {
    "problem_number": 2,
    "question": "Let ABCD be a trapezoid with AB || CD and BC ≠ DA. A circle through C and D intersects AC, AD, BC, and BD again at W, X, Y, and Z respectively. Prove that WZ, XY, and AB are concurrent.",
    "solution": "Using cyclic quadrilateral properties and radical axis theorem: AB, WZ, and XY are all radical axes of pairs of circles and must concur by the three-circle radical axis concurrency theorem."
  },
  {
    "problem_number": 3,
    "question": "n players stand in a circle and each initially votes for the person on their left. In each of n rounds, each player updates their vote such that if a votes for b and b votes for c, then a changes their vote to c. Prove that after n rounds, all players vote for the same person.",
    "solution": "Using graph-based reasoning and cycle reduction, it’s shown that within ⌊log2 n⌋ rounds the voting graph reduces to a self-loop and the rest converge within ⌈log2 n⌉ rounds. Total ≤ n rounds always suffices."
  },
  {
    "problem_number": 4,
    "question": "Determine all positive integers a, b, c, p such that p and p+2 are odd primes and 2^a * p^b = (p+2)^c − 1.",
    "solution": "The only solution is (a, b, c, p) = (3, 1, 2, 3). This reduces to solving 2^a * 3^b = 25 − 1 = 24, giving a = 3 and b = 1."
  },
  {
    "problem_number": 5,
    "question": "Let ℓ ≥ 2 be an integer and p(x) a polynomial with integer coefficients. Prove that there exist reflexive integer polynomials q(x), r(x) such that (1 + x + x^2 + ... + x^{ℓ−1})p(x) = q(x) + x^ℓ * r(x).",
    "solution": "Two solutions: (1) Construct q(x) and r(x) using algebraic symmetry (involves evaluating p(1/x)). (2) Use matrices and linear algebra to build reflexive polynomials by decomposing matrix representations with horizontal symmetry."
  }
]

from checker import LMModel  

model = LMModel()

# change the json accordingly
for problem in cjmo_problems:
    prompt = f"QUESTION: {problem['question']}"
    print(f"\n <---------- Problem {problem['problem_number']} ---------->")
    print(f"\n #### Question {problem['question']}")
    try:
        response = model(prompt)
        print(response[0])
    except Exception as e:
        print(f"Error processing Problem {problem['problem_number']}: {e}")