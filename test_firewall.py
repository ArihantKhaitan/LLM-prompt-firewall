from firewall import run_firewalled_prompt, call_main_llm
from classifier import classify_prompt

def main():
    use_few_shot = True  # Toggle few-shot logic
    while True:
        user_prompt = input("🔒 Enter prompt: ").strip()
        if not user_prompt:
            break

        # Block unsafe prompt
        classification = classify_prompt(user_prompt, few_shot=use_few_shot)
        if classification == "jailbreak":
            print("🛑 BLOCKED: Prompt classified as jailbreak.\n")
            continue

        # Get response
        response = call_main_llm(user_prompt)
        print("🧠 LLM Response:")
        print(response + "\n")

        # Optional: Block if output itself is bad
        output_check = classify_prompt(response, few_shot=use_few_shot)
        if output_check == "jailbreak":
            print("🛑 BLOCKED: LLM output itself was flagged as jailbreak.\n")
        else:
            print("✅ Output considered safe.\n")

if __name__ == "__main__":
    main()
