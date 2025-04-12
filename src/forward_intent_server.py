from flask import Flask, request, jsonify
import requests

SOURCE_API = "http://localhost:5000/classify"
app = Flask(__name__)

def extract_json(intent_text):
    if "klcc" in intent_text.lower():
        return {"query": "location", "location": "KLCC"}
    elif "pavilion" in intent_text.lower():
        return {"query": "location", "location": "Pavilion"}
    elif "petrol" in intent_text.lower():
        return {"query": "location", "location": "Nearest Petrol Station"}
    elif "earn" in intent_text.lower():
        return {"query": "finance", "request": "earnings_today"}
    elif "reject" in intent_text.lower():
        return {"query": "action", "action": "reject_customer"}
    elif "call" in intent_text.lower():
        return {"query": "action", "action": "call_customer"}
    elif "drop" in intent_text.lower():
        return {"query": "action", "action": "drop_customer"}
    elif "job" in intent_text.lower():
        return {"query": "action", "action": "available_job"}
    elif "map" in intent_text.lower():
        return {"query": "action", "action": "open_navigation"}
    elif "reject" in intent_text.lower():
        return {"query": "action", "action": "reject_customer"}
    elif "accept" in intent_text.lower():
        return {"query": "action", "action": "accept_customer"}
    elif "stop" in intent_text.lower():
        return {"query": "action", "action": "stop_job"}
    elif "eta" in intent_text.lower():
        return {"query": "action", "action": "eta"}
    else:
        return {"query": "unknown", "raw_intent": intent_text}

@app.route("/process", methods=["POST"])
def process_intent():
    incoming = request.json
    text = incoming.get("text", "")
    try:
        response = requests.post(SOURCE_API, json={"text": text})
        result = response.json()
        intent = result.get("intent", "unknown")
        processed_json = extract_json(intent)
        return jsonify(processed_json)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=6000)