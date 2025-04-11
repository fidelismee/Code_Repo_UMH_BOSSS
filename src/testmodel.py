import torch
from transformers import BertTokenizer, BertForSequenceClassification
import pickle

# Set device
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Path to the saved model directory
model_dir = "my_finetuned_bert"

# Load tokenizer and model
tokenizer = BertTokenizer.from_pretrained(model_dir)
model = BertForSequenceClassification.from_pretrained(model_dir)
model.to(device)
model.eval()

# Load label encoder
with open(f"{model_dir}/label_encoder.pkl", "rb") as f:
    label_encoder = pickle.load(f)

# Define classify function
def classify(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    with torch.no_grad():
        outputs = model(**inputs)
        pred = torch.argmax(outputs.logits, dim=1).item()
    return label_encoder.inverse_transform([pred])[0]

# Example usage
if __name__ == "__main__":
    print(classify("Mana nak isi minyak?"))        # Expected: Where is the nearest petrol pump
    print(classify("How to go to KLCC?"))          # Expected: How do I get to KLCC from here
    print(classify("Pendapatan saya harini?"))     # Expected: How much did I earn today
