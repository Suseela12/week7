# Experiment 7: Constraint Specification and Iterative Refinement

## Aim
To practice constraint specification and iterative prompt refinement by generating a short description of a smartwatch and checking compliance with predefined rules.

## Problem Statement
Generate a product description of no more than 60 words while satisfying three constraints:
- Use exactly three bullet points.
- Start each bullet point with a verb.
- Do not use the prohibited word "smart".

If the initial response violates any constraint, use a refined prompt with clearer instructions and examples.

## Technologies Used
- Python
- Google Gemini AI
- Google Gen AI SDK

## Algorithm
1. Initialize the Gemini API client.
2. Define the initial prompt with three constraints.
3. Generate the initial response.
4. Check the bullet count, bullet openings, prohibited word, and word count.
5. Refine the prompt with explicit instructions and examples.
6. Generate and evaluate the refined response.
7. Save both responses and validation reports to a text file.

## Installation

```bash
pip install -r requirements.txt
```

## Configuration
Set the `GEMINI_API_KEY` environment variable before running the program. Never upload API keys to GitHub.

## Execution

```bash
python src/main.py
```

## Expected Output
- Initial prompt and response.
- Initial constraint violation report.
- Refined prompt and response.
- Refined constraint validation report.
- Saved results in `output/refinement_results.txt`.

## Result
The program evaluates whether the initial and refined prompts follow the required constraints and records the results for comparison.

## Conclusion
Explicit instructions and examples can improve compliance with output constraints. Automated checks help identify formatting violations, while manual review may still be needed to verify grammar and meaning.


└── README.md
```
