
import os
import openai
import anthropic
from flask import Flask, request, jsonify

app = Flask(__name__)

# Load API keys
openai.api_key = os.getenv("OPENAI_API_KEY")
anthropic_key = os.getenv("ANTHROPIC_API_KEY")

def ask_gpt(prompt):
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You're an expert Python developer who upgrades Atlas automatically."},
                {"role": "user", "content": prompt}
            ]
        )
        return completion.choices[0].message.content
    except Exception as e:
        print("OpenAI failed:", e)
        return None

def ask_claude(prompt):
    try:
        client = anthropic.Anthropic(api_key=anthropic_key)
        response = client.messages.create(
            model="claude-3-sonnet-20240229",
            max_tokens=2048,
            temperature=0.7,
            system="You're a software engineer improving an autonomous AI assistant named Atlas.",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.content[0].text
    except Exception as e:
        print("Anthropic failed:", e)
        return "Both engines failed."

@app.route("/command", methods=["POST"])
def command():
    data = request.json
    prompt = data.get("prompt", "")

    code = ask_gpt(prompt)
    if not code:
        code = ask_claude(prompt)

    with open("main.py", "w") as f:
        f.write(code)

    os.system("git add .")
    os.system(f"git commit -m 'upgrade: {prompt}'")
    os.system("git push")

    return jsonify({"message": "Upgrade committed", "code": code})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
