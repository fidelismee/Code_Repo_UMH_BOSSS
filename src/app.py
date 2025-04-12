import torch
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
import pickle
from flask import Flask, request, jsonify

# Load model components
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model_dir = r"J:\My Drive\Fidel_Coding\UMH_GRAB\Code_Repo_UMH_BOSSS\my_finetuned_bert"

tokenizer = DistilBertTokenizer.from_pretrained(model_dir)
model = DistilBertForSequenceClassification.from_pretrained(model_dir).to(device).eval()

with open(f"{model_dir}/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

app = Flask(__name__)

@app.route("/classify", methods=["POST"])
def classify_text():
    data = request.json
    text = data.get("text", "")

    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        pred = torch.argmax(outputs.logits, dim=1).item()

    prediction = label_encoder.inverse_transform([pred])[0]
    return jsonify({"intent": prediction})

if __name__ == "__main__":
    app.run(debug=True, port=5000)