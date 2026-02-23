import os
from datetime import datetime

import requests
from flask import Flask, jsonify, render_template, request
from database import get_faqs, get_programs, initialize_database


app = Flask(__name__)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "openai/gpt-4o-mini").strip()

# Initialize database on startup
initialize_database()


def build_system_prompt():
		faq_items = get_faqs()
		faq_text = "\n".join([f"- {item['q']}" for item in faq_items])
		return (
				"You are a helpful college admissions assistant for AGC College. Answer questions about admissions, programs, fees, hostel facilities, placement records, scholarships, entrance exams, course duration, and international student policies. "
				"If a question is outside these topics, respond with a brief helpful suggestion and offer the contact method: info.agcc@gmail.com. "
				"Keep answers under 120 words.\n\n"
				f"Common Topics to Answer:\n{faq_text}"
		)


def call_openai(message):
		if not OPENAI_API_KEY:
				return None, "Missing OPENAI_API_KEY environment variable."

		payload = {
				"model": OPENAI_MODEL,
				"messages": [
						{"role": "system", "content": build_system_prompt()},
						{"role": "user", "content": message},
				],
				"temperature": 0.2,
				"max_tokens": 220,
		}

		headers = {
				"Authorization": f"Bearer {OPENAI_API_KEY}",
				"Content-Type": "application/json",
				"HTTP-Referer": "http://localhost:5000",
				"X-Title": "College Admissions Chatbot",
		}

		response = requests.post("https://openrouter.ai/api/v1/chat/completions", json=payload, headers=headers, timeout=30)
		if response.status_code != 200:
				return None, f"API error {response.status_code}: {response.text}"

		data = response.json()
		return data["choices"][0]["message"]["content"].strip(), None

def get_bangalore_weather():
	api_key = "a18a8c258ed041e49e042548261202"
	city = "Bangalore"
	url = f"https://api.weatherapi.com/v1/current.json?key={api_key}&q={city}&aqi=yes"
	try:
		response = requests.get(url)
		data = response.json()
		if "error" in data:
			return f"Weather info not available: {data['error'].get('message', '')}"
		weather = data["current"]["condition"]["text"]
		temp = data["current"]["temp_c"]
		return f"Bangalore: {weather}, {temp}°C"
	except Exception as e:
		return f"Error fetching weather: {e}"

@app.route("/")
def index():
	now = datetime.now().strftime("%B %d, %Y")
	faq_items = get_faqs()
	weather_info = get_bangalore_weather()
	return render_template("index.html", faq=faq_items, now=now, weather_info=weather_info)

@app.route("/chat", methods=["POST"])
def chat():
		payload = request.get_json(silent=True) or {}
		message = (payload.get("message") or "").strip()
		if not message:
				return jsonify({"error": "Please enter a question."}), 400

		reply, error = call_openai(message)
		if error:
				return jsonify({"error": error}), 500

		return jsonify({"reply": reply})

@app.route("/program/<program_name>", methods=["GET"])
def get_program_details(program_name):
		"""Fetch detailed information about a specific program"""
		programs = get_programs()
		program = next((p for p in programs if p["name"].lower() == program_name.lower()), None)
		
		if not program:
				return jsonify({"error": f"Program '{program_name}' not found."}), 404
		
		# Format the program details as a readable response
		details = f"""**{program['name']}**

📚 Category: {program['category']}
⏱️ Duration: {program['duration']}
💼 Eligibility: {program['eligibility']}
💰 Fees: {program['fees']}
👥 Available Seats: {program['seats']}

This is a comprehensive {program['category'].lower()} program designed to provide excellent education and career opportunities. For more information or to apply, please contact us at info.agcc@gmail.com or call 7491830049."""
		
		return jsonify({"details": details})


if __name__ == "__main__":
		app.run(debug=True, port=5000)
