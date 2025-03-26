import os
import openai
import anthropic
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load API keys from environment
openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")
github_pat = os.getenv("GITHUB_PAT")
github_username = os.getenv("GITHUB_USERNAME")
github_repo = os.getenv("GITHUB_REPO")

def ask_gpt(prompt):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're an expert Python developer helping upgrade an AI assistant named Atlas."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print("GPT Error:", e)
        return None

def ask_claude(prompt):
    try:
        client = anthropic.Anthropic(api_key=anthropic_key)
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2048,
            temperature=0.7,
            system="You're an autonomous agent improving another autonomous agent.",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        print("Claude Error:", e)
        return None

@app.route("/command", methods=["POST"])
def command():
    data = request.json
    prompt = data.get("prompt", "")
    
    code = ask_gpt(prompt)
    if not code:
        code = ask_claude(prompt)
    if not code:
        return jsonify({"error": "Both models failed."}), 500

    try:
        with open("main.py", "w") as f:
            f.write(code)

        subprocess.run(["git", "config", "--global", "user.email", "bot@atlas.com"])
        subprocess.run(["git", "config", "--global", "user.name", "Atlas Upgrade Agent"])

        repo_url = f"https://{github_pat}@github.com/{github_username}/{github_repo}.git"
        subprocess.run(["git", "remote", "set-url", "origin", repo_url])
        subprocess.run(["git", "add", "main.py"])
        subprocess.run(["git", "commit", "-m", f"Upgrade: {prompt}"])
        subprocess.run(["git", "push"])

        return jsonify({"message": "Upgrade committed and pushed", "code": code})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
    
