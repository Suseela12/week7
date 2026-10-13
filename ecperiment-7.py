!pip install -q google-genai
--------------------------------------------------
from google.colab import userdata
from google import genai
import time

api_key = userdata.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

MODEL = "gemini-3.8-flash"

print("Gemini API connected successfully!")
---------------------------------------------------------
def run_prompt(prompt):
    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model=MODEL,
                contents=prompt,
                config={"temperature": 0.3}
            )
            return response.text.strip() if response.text else "No response"

        except Exception as e:
            error = str(e)

            if "429" in error or "RESOURCE_EXHAUSTED" in error:
                return "API quota exceeded. Try again later."

            if ("503" in error or "UNAVAILABLE" in error) and attempt < 4:
                time.sleep(2 ** attempt)
            else:
                return "API Error: " + error
  ----------------------------------------------------------------------------------
initial_prompt = """
Describe a smartwatch in no more than 60 words.
Use exactly 3 bullet points.
Each bullet point must start with a verb.
Do not use the word "smart" anywhere.
"""

print("Initial prompt created.")
---------------------------------------------------------------------------
import re

# Simple list of common action verbs for this experiment
verbs = {
    "track", "tracks", "monitor", "monitors",
    "display", "displays", "measure", "measures",
    "provide", "provides", "help", "helps",
    "connect", "connects", "record", "records",
    "show", "shows", "receive", "receives",
    "count", "counts", "offer", "offers",
    "deliver", "delivers", "manage", "manages",
    "support", "supports", "check", "checks",
    "keep", "keeps", "last", "lasts"
}

def check_constraints(response):
    lines = [
        line.strip() for line in response.splitlines()
        if line.strip()
    ]

    bullets = [
        line for line in lines
        if line.startswith("- ")
    ]

    # Remove bullet markers before checking words
    description = " ".join(
        line[2:] for line in bullets
    )

    word_count = len(re.findall(r"\b[\w'-]+\b", description))

    bullet_count_ok = len(bullets) == 3

    verb_check = all(
        bool(re.match(r"^[A-Za-z]+", bullet[2:]))
        and bullet[2:].split()[0].lower().strip(".,:;!?")
            in verbs
        for bullet in bullets
        if bullet[2:].split()
    )

    # Case-insensitive whole-word match
    banned_word_found = bool(
        re.search(r"\bsmart\b", response, re.IGNORECASE)
    )

    word_count_ok = word_count <= 60

    return {
        "Exactly 3 bullets": bullet_count_ok,
        "Every bullet starts with a listed verb": verb_check,
        "Banned word absent": not banned_word_found,
        "Maximum 60 words": word_count_ok,
        "Word count": word_count
    }


def print_report(report):
    for rule, result in report.items():
        if rule == "Word count":
            print(f"{rule}: {result}")
        else:
            print(f"{rule}: {'PASS' if result else 'FAIL'}")
---------------------------------------------------------------------
      print("=== INITIAL PROMPT ===")
print(initial_prompt)

initial_response = run_prompt(initial_prompt)

print("\nInitial response:")
print(initial_response)

print("\nInitial violation report:")
initial_report = check_constraints(initial_response)
print_report(initial_report)
------------------------------------------------------
refined_prompt = """
Describe a smartwatch (a wearable watch with useful digital features)
in no more than 60 words.

Follow these rules:
1. Output exactly 3 bullet points.
2. Start every bullet point with an action verb.
3. Never use the prohibited word that begins with "s" and ends
   with "mart". Avoid that word in any capitalization.
4. Keep the entire description concise and factual.

Follow this format:
- Tracks daily activity.
- Displays incoming notifications.
- Monitors your heart rate.

Write only the 3 bullet points.
"""

print("Refined prompt created.")
-------------------------------------------------------------------------
print("=== REFINED PROMPT ===")
print(refined_prompt)

refined_response = run_prompt(refined_prompt)

print("\nRefined response:")
print(refined_response)

print("\nRefined violation report:")
refined_report = check_constraints(refined_response)
print_report(refined_report)
-------------------------------------------------------------------------
print("=" * 50)
print("INITIAL VS REFINED COMPARISON")
print("=" * 50)

print("\nInitial response:")
print(initial_response)

print("\nRefined response:")
print(refined_response)

print("\nConstraint comparison:")
for rule in [
    "Exactly 3 bullets",
    "Every bullet starts with a listed verb",
    "Banned word absent",
    "Maximum 60 words"
]:
    before = initial_report[rule]
    after = refined_report[rule]

    print(
        f"{rule}: Initial = "
        f"{'PASS' if before else 'FAIL'}, "
        f"Refined = {'PASS' if after else 'FAIL'}"
    )
  ---------------------------------------------------------------------
initial_passes = sum(
    initial_report[key] is True
    for key in [
        "Exactly 3 bullets",
        "Every bullet starts with a listed verb",
        "Banned word absent",
        "Maximum 60 words"
    ]
)

refined_passes = sum(
    refined_report[key] is True
    for key in [
        "Exactly 3 bullets",
        "Every bullet starts with a listed verb",
        "Banned word absent",
        "Maximum 60 words"
    ]
)

print("=== EXPERIMENT CONCLUSION ===")
print(f"Initial constraints passed: {initial_passes}/4")
print(f"Refined constraints passed: {refined_passes}/4")

if refined_passes > initial_passes:
    print("Prompt refinement improved constraint compliance.")
elif refined_passes == initial_passes:
    print("Both prompts achieved the same number of passing checks.")
else:
    print("The refined prompt did not improve compliance in this run.")

print("Always inspect the actual responses before reporting the result.")
