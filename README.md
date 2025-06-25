# 🔒 LLM Prompt Firewall

A lightweight and extensible firewall framework to **detect and classify** LLM prompts as either **safe** or **jailbreak** using models like Ollama's "Llama3".
Designed for evaluating and filtering potentially malicious user input before it reaches your language model.

## 🚀 Features

- ✅ **Prompt Classification**: Classifies prompts into `safe` or `jailbreak`
- 🧠 **Few-shot Inference and Zero-shot Inference**: Uses powerful LLMs to detect prompt intent with or without examples
- 🧪 **Evaluation Suite**: Test and measure accuracy on labeled datasets
- 🌐 **UI Interface**: Minimal terminal-based interface for testing
- 🔐 **Environment Variable Based Key Loading** (no secrets stored)
- 🔥 **Firewall**: Blocks Prompts at Prompt level or Respone Level 

## 🗂 File Structure

📁 LLM-prompt-firewall

config.py # Configuration and constants

dataset.json # Manual dataset for evaluation

zero_shot_classifier_ollama.py # Ollama-based classifier based on dataset.json

evaluate_classifier.py # Evaluates classifier performance based on labelled dataset

test_firewall.py # Unit tests for firewall system

firewall.py # Core firewall logic

classifier.py # Main Few-shot Ollama-based classifier

run_combined_test.py # Runs tests including everthing based on manual data

run_full_evaluation.py # Full-scale evaluation of all prompts based on labelled dataset

firewall_ui.py # CLI-based UI

## ⚙️ Setup Instructions

1.Clone the repo:

git clone https://github.com/ArihantKhaitan/LLM-prompt-firewall.git

cd LLM-prompt-firewall
   
2.Create a virtual environment:

python -m venv venv

source venv/bin/activate  # or venv\Scripts\activate on Windows

3.Install dependencies:

pip install -r requirements.txt

4.Set your API keys:

For Hugging Face:

export HUGGINGFACE_API_KEY="your-hf-token"

🧪 How to Run

➤ Classify Prompts (Ollama):
python zero_shot_classifier_ollama.py

➤ Evaluate Classifier:
python evaluate_classifier.py

➤ Run Full Evaluation:
python run_full_evaluation.py

➤ Run Firewall UI:
streamlit run firewall_ui.py

💾 Output & Results

All results are saved in JSON format in the results/ directory:

classified_results.json 

eval_results_ollama.json 

combined_test_results.json 

full_firewall_eval_results.json # Final Firewall output

📜 License

This project is licensed under the MIT License. You are free to use, modify, and distribute this code with proper attribution.

👤 Author

Arihant Khaitan

🤝 Contributions

Pull requests and feedback are welcome. If you find a bug or have a suggestion, feel free to open an issue.
