import json

# Read the JSON file
with open('/mnt/hqiu/MathEval/datasets/MathQA/train.json', 'r', encoding='utf-8') as file:
    problems = json.load(file)

# Now 'problems' is a list containing all the math problems
print(f"Total number of problems: {len(problems)}")

# Example: Access the first problem
if problems:
    first_problem = problems[0]
    print("\nFirst problem:")
    print(f"Problem: {first_problem['Problem']}")
    print(f"Category: {first_problem['category']}")
    print(f"Correct answer: {first_problem['correct']}")

# sample 100 problems and save to another json file
import random
sampled_problems = random.sample(problems, 100)

with open('sampled_problems.json', 'w', encoding='utf-8') as file:
    json.dump(sampled_problems, file, ensure_ascii=False, indent=4)
print("\nSampled 100 problems saved to 'sampled_problems.json'")