import os

from dotenv import load_dotenv
from flask import Flask, jsonify, render_template, request
from google import genai

load_dotenv()

app = Flask(__name__)
MODEL_NAME = "gemini-3.6-flash"
SUPPORTED_ACTIONS = {"explain", "summarize", "quiz", "ask"}

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key) if api_key and api_key != "YOUR_API_KEY_HERE" else None


def build_prompt(topic, action):
    prompts = {
        "explain": f"""Explain the following topic to a complete beginner: {topic}

Give a simple definition, explain the important concepts, and include one real-world example. Use clear headings and bullet points. Keep the tone friendly and the explanation useful for a college student.""",
        "summarize": f"""Summarize these study notes for exam revision:

{topic}

Keep only the important information. Use concise bullet points, highlight important terms in bold, and organize the result so it is easy to revise.""",
        "quiz": f"""Create exactly 5 multiple-choice questions about this study topic or these notes:

{topic}

Each question must have exactly 4 options labelled A, B, C, and D. Identify the correct answer and give a short explanation for each answer. Use this clear format for every question:
Question 1: ...
A. ...
B. ...
C. ...
D. ...
Correct answer: ...
Explanation: ...""",
        "ask": f"""Answer the student's study question below in simple, accurate language:

{topic}

Explain the answer step by step when appropriate, and give an example when useful. If the question is unclear, state the assumption you are making.""",
    }
    return prompts[action]


@app.route("/")
def index():
    return render_template("index.html")


@app.post("/generate")
def generate():
    data = request.get_json(silent=True) or {}
    topic = str(data.get("topic", "")).strip()
    action = str(data.get("action", "")).strip().lower()

    if not topic:
        return jsonify({"error": "Please enter a topic or paste some study notes first."}), 400
    if action not in SUPPORTED_ACTIONS:
        return jsonify({"error": "Please choose a valid study action."}), 400
    if client is None:
        return jsonify({"error": "Gemini is not configured yet. Add your API key to the .env file and restart the app."}), 503

    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=build_prompt(topic, action),
        )
        result = getattr(response, "text", None)
        if not result:
            return jsonify({"error": "Gemini returned an empty response. Please try again."}), 502
        return jsonify({"result": result})
    except Exception as e:
        app.logger.exception("Gemini request failed")
        print(f"ERROR: {str(e)}")  # Debug print
        return jsonify({"error": f"Error: {str(e)}"}), 502


if __name__ == "__main__":
    app.run(debug=True)
