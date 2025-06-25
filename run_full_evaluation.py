import os
import json
import argparse
import requests
from tqdm import tqdm
from datasets import load_dataset
from classifier import classify_prompt
from firewall import call_main_llm
from config import MODEL_NAME, OLLAMA_API_URL, USE_FEW_SHOT

parser = argparse.ArgumentParser()
parser.add_argument("--firewall", choices=["on", "off"], default="on", help="Enable or disable prompt/response filtering")
args = parser.parse_args()
FIREWALL_ENABLED = args.firewall == "on"

os.environ["HF_TOKEN"] = "" #Replace with your key

dataset = load_dataset("qualifire/Qualifire-prompt-injection-benchmark", split="test")
examples = dataset.select(range(5))  

results = []

print(f"🧪 Running full eval | Firewall enabled: {FIREWALL_ENABLED}")

for item in tqdm(examples, desc="Processing"):
    prompt = item["text"]
    true_label = item["label"]

    if FIREWALL_ENABLED:

        prompt_result = classify_prompt(prompt, few_shot=USE_FEW_SHOT)

        if prompt_result in ["jailbreak", "unknown"]:
            results.append({
                "prompt": prompt,
                "response": None,
                "predicted": prompt_result,
                "true_label": true_label,
                "blocked_at": "prompt"
            })
            continue

    response = call_main_llm(prompt)

    if FIREWALL_ENABLED:
        response_result = classify_prompt(response, few_shot=USE_FEW_SHOT)

        if response_result in ["jailbreak", "unknown"]:
            results.append({
                "prompt": prompt,
                "response": response,
                "predicted": response_result,
                "true_label": true_label,
                "blocked_at": "response"
            })
            continue

    results.append({
        "prompt": prompt,
        "response": response,
        "predicted": "benign",
        "true_label": true_label,
        "blocked_at": None
    })

with open("full_firewall_eval_results.json", "w") as f:
    json.dump(results, f, indent=2)

correct = sum(1 for r in results if r["predicted"] == r["true_label"])
total = len(results)
accuracy = correct / total * 100

print(f"\n✅ Saved results to full_firewall_eval_results.json")
print(f"🎯 Accuracy: {accuracy:.2f}% ({correct}/{total})")

blocked_at_prompt = sum(1 for r in results if r["blocked_at"] == "prompt")
blocked_at_response = sum(1 for r in results if r["blocked_at"] == "response")
print(f"\n📊 Blocked at Prompt: {blocked_at_prompt}")
print(f"📊 Blocked at Response: {blocked_at_response}")
print(f"✅ Clean completions: {total - blocked_at_prompt - blocked_at_response}")
