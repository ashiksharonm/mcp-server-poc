import json
import httpx
import sys
import os
import time
from datetime import datetime

SERVER_URL = "http://localhost:8000"
GOLDEN_PROMPTS_FILE = "evals/golden_prompts.json"
REPORT_DIR = "evals/reports"

def run_evals():
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)

    with open(GOLDEN_PROMPTS_FILE, "r") as f:
        test_cases = json.load(f)

    results = []
    failures = 0

    print(f"Running {len(test_cases)} evaluation cases...")

    for case in test_cases:
        prompt = case["prompt"]
        print(f"Testing: {prompt} ... ", end="")
        
        start_time = time.time()
        try:
            response = httpx.post(f"{SERVER_URL}/agent/run", json={"query": prompt}, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            tool_calls = data.get("tool_calls", [])
            answer = data.get("answer", "")
            
            # Check Tool Selection
            used_tools = [t["tool"] for t in tool_calls]
            tool_match = case["expected_tool"] in used_tools
            
            # Check Content
            content_match = all(field in str(data) for field in case["expected_fields"])
            
            success = tool_match and content_match
            
            result = {
                "id": case["id"],
                "prompt": prompt,
                "success": success,
                "tool_match": tool_match,
                "content_match": content_match,
                "actual_tools": used_tools,
                "response": answer,
                "duration": time.time() - start_time
            }
            results.append(result)
            
            if success:
                print("PASS")
            else:
                print("FAIL")
                failures += 1
                
        except Exception as e:
            print(f"ERROR: {e}")
            results.append({
                "id": case["id"],
                "prompt": prompt,
                "success": False,
                "error": str(e)
            })
            failures += 1

    # Save Report
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"{REPORT_DIR}/report_{timestamp}.json"
    with open(report_path, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nEvaluation Complete. Report saved to {report_path}")
    print(f"Passed: {len(test_cases) - failures}/{len(test_cases)}")

    if failures > 0:
        sys.exit(1)

if __name__ == "__main__":
    run_evals()
