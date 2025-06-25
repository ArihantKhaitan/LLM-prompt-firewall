from datasets import load_dataset
from classifier import classify_prompt  
import json
from tqdm import tqdm
import os

os.environ["HF_TOKEN"] = "" #Replace with your key

dataset = load_dataset("qualifire/Qualifire-prompt-injection-benchmark", split="test")

examples = dataset.select(range(50))

results = []

print("🔍 Running few-shot classification using Ollama...")

for item in tqdm(examples, desc="Classifying"):
    prompt = item["text"]

    classification = classify_prompt(prompt, few_shot=True)

    results.append({
        "id": item["text"],
        "label": item["label"],
        "predicted": classification
    })

with open("eval_results_ollama.json", "w") as f:
    json.dump(results, f, indent=4)

print("✅ Done! Results saved to eval_results_ollama.json")

correct = sum(1 for r in results if r["label"] == r["predicted"])
total = len(results)
accuracy = correct / total * 100
print(f"\n🎯 Accuracy: {accuracy:.2f}% ({correct}/{total})")
