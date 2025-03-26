
import os
import openai
import anthropic
import requests
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load API keys from environment
openai.api_key = os.getenv("OPENAI_API_KEY_ATLAS")
anthropic_key = os.getenv("ANTHROPIC_API_KEY_ATLAS")
hf_api_key = os.getenv("HF_API_KEY")
github_pat = os.getenv("GITHUB_PAT")
github_username = os.getenv("GITHUB_USERNAME")
github_repo = os.getenv("GITHUB_REPO")

def ask_gpt(prompt):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're an expert AI improving Atlas, a self-upgrading assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print("OpenAI GPT Error:", e)
        return None

def ask_claude(prompt):
    try:
        client = anthropic.Anthropic(api_key=anthropic_key)
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2048,
            temperature=0.7,
            system="You're an advanced AI engineer helping improve Atlas.",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        print("Anthropic Claude Error:", e)
        return None

def ask_huggingface(prompt):
    try:
        headers = {
            "Authorization": f"Bearer {hf_api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "inputs": prompt
        }
        response = requests.post(
            "https://api-inference.huggingface.co/models/bigscience/bloom",
            headers=headers,
            json=payload
        )
        response.raise_for_status()
        return response.json()[0]["generated_text"]
    except Exception as e:
        print("Hugging Face Error:", e)
        return None

@app.route("/command", methods=["POST"])
def command():
    data = request.json
    prompt = data.get("prompt", "")
    
    code = ask_gpt(prompt)
    if not code:
        code = ask_claude(prompt)
    if not code:
        code = ask_huggingface(prompt)

    if not code:
        return jsonify({"error": "All engines failed to respond."}), 500

    try:
        with open("main.py", "w") as f:
            f.write(code)

        subprocess.run(["git", "config", "--global", "user.email", "atlas@autonomous.ai"])
        subprocess.run(["git", "config", "--global", "user.name", "AtlasBot"])
        
        repo_url = f"https://{github_pat}@github.com/{github_username}/{github_repo}.git"
        subprocess.run(["git", "remote", "set-url", "origin", repo_url])
        subprocess.run(["git", "add", "main.py"])
        subprocess.run(["git", "commit", "-m", f"Auto upgrade: {prompt}"])
        subprocess.run(["git", "push"])

        return jsonify({"message": "Upgrade complete and pushed", "code": code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
    
