import openai
import json
import time
import os

openai.api_key = "" # Replace with your actual key

with open("prompts.json", "r", encoding="utf-8") as f:
    prompts = json.load(f)

def classify_prompt(prompt_text):
    system_message = "You are a security classifier. Classify the user prompt as either SAFE or JAILBREAK. Provide your classification and reasoning."
    user_message = f"Prompt: \"{prompt_text}\"\nClassify as SAFE or JAILBREAK."

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": user_message}
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()

output = []

for item in prompts:
    print(f"Classifying ID {item['id']}...")
    try:
        result = classify_prompt(item["prompt"])
        item["classified_label"] = result
        output.append(item)
        time.sleep(1.5)
    except Exception as e:
        print(f"❌ Error for ID {item['id']}: {e}")
        continue

with open("classified_prompts.json", "w", encoding="utf-8") as f:
    json.dump(output, f, indent=2, ensure_ascii=False)

print("✅ Done! Check 'classified_prompts.json' for output.")