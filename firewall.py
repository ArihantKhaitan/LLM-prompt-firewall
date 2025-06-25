from classifier import classify_prompt
import requests

FIREWALL_ENABLED = True

def call_main_llm(prompt):
    response = requests.post(
        "http://localhost:11434/api/generate",
        json={
            "model": "llama3",
            "prompt": prompt,
            "stream": False
        }
    )
    return response.json()["response"].strip()

def run_firewalled_prompt(prompt, few_shot=False):
    if not FIREWALL_ENABLED:
        return call_main_llm(prompt)

    classification = classify_prompt(prompt, few_shot=few_shot)
    if classification == "jailbreak":
        return "[BLOCKED] Prompt flagged as jailbreak."
    elif classification == "unknown":
        return "[WARNING] Classification uncertain. Prompt skipped."
    else:
        return call_main_llm(prompt)
