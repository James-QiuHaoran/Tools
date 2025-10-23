import json
import requests
from typing import List, Dict

# MODEL = "google/gemma-3-27b-it"
# MODEL = 'microsoft/phi-4'
# MODEL = 'deepseek-ai/DeepSeek-R1-Distill-Qwen-32B'
MODEL = 'nvidia/NVLM-D-72B'
PORT = 8000

def load_problems(filename: str) -> List[Dict]:
    """Load problems from JSON file"""
    with open(filename, 'r', encoding='utf-8') as file:
        return json.load(file)

def query_vllm(problem: str, base_url: str = f"http://localhost:{PORT}") -> str:
    """Send a problem to the vLLM server and get the response"""
    url = f"{base_url}/v1/chat/completions"
    
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "user",
                "content": f"Solve this math problem and provide the answer. Choose from the given options.\n\nProblem: {problem['Problem']}\n\nOptions: {problem['options']}\n\nPlease don't generate intermediate steps and only provide your answer in the format: 'Answer: [letter]'"
            }
        ],
        "temperature": 1.0,
        "top_p": 1.0,
        "max_tokens": 512
    }
    
    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        result = response.json()
        return result['choices'][0]['message']['content']
    except requests.exceptions.RequestException as e:
        print(f"Error querying vLLM: {e}")
        return None

import re
from typing import Optional
def extract_answer(response: str) -> Optional[str]:
    """Extract the answer letter from model response"""
    if not response:
        return None
    
    # Try to find "Answer: X" pattern
    match = re.search(r'[Aa]nswer:\s*([a-eA-E])', response)
    if match:
        return match.group(1).lower()
    
    # Try to find standalone letter at the end
    match = re.search(r'\b([a-eA-E])\b(?!.*\b[a-eA-E]\b)', response)
    if match:
        return match.group(1).lower()
    
    return None

def main():
    # Load problems
    problems = load_problems('sampled_problems.json')
    print(f"Loaded {len(problems)} problems\n")
    
    # Store results
    results = []
    correct_count = 0
    
    # Process each problem
    for i, problem in enumerate(problems):
        print(f"Processing problem {i+1}/{len(problems)}...")
        print(f"Question: {problem['Problem'][:100]}...")
        
        # Get model's answer
        model_response = query_vllm(problem)
        
        if model_response:
            print(f"Model response: {model_response[:200]}...")
            print(f"Correct answer: {problem['correct']}")
            # Extract answer
            predicted_answer = extract_answer(model_response)
            correct_answer = problem['correct'].lower()
            is_correct = predicted_answer == correct_answer
            if is_correct:
                correct_count += 1
            print(f"Predicted: {predicted_answer} | Correct: {correct_answer} | {'✓' if is_correct else '✗'}")
            
            # Store result
            results.append({
                'problem_id': i,
                'question': problem['Problem'],
                'correct_answer': problem['correct'],
                'predicted_answer': predicted_answer,
                'model_response': model_response,
                'category': problem['category'],
                'is_correct': is_correct,
            })
        
        print("-" * 80)
        # if i >= 1:  # for testing
        #     break
    
    # Save results to file
    with open('model_results.json', 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    accuracy = correct_count / len(results) if results else 0
    print(f"Model Accuracy: {accuracy:.2%}")
    
    print(f"\nProcessed {len(results)} problems. Results saved to 'model_results.json'")

if __name__ == "__main__":
    main()