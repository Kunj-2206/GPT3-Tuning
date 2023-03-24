import openai
import re
import nltk
nltk.download('punkt')
from nltk.tokenize import word_tokenize
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

openai.api_key = "YOUR_API_KEY" # Replace with your API key
model_name = "EleutherAI/gpt-neo-1.3B" # Replace with the GPT-3 model you want to use

# Load the GPT-3 model and tokenizer
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)

# Set up the model for fine-tuning
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.to(device)

def preprocess_text(text):
    # Remove URLs and mentions
    text = re.sub(r"http\S+", "", text)
    text = re.sub(r"@[^\s]+", "", text)
    # Tokenize text
    tokens = word_tokenize(text)
    # Lowercase and remove stopwords
    stopwords = set(nltk.corpus.stopwords.words('english'))
    filtered_tokens = [token.lower() for token in tokens if token.lower() not in stopwords]
    return " ".join(filtered_tokens)

def generate_response(prompt):
    # Preprocess the prompt
    processed_prompt = preprocess_text(prompt)
    # Tokenize the input
    input_ids = tokenizer.encode(processed_prompt, return_tensors="pt").to(device)
    # Generate a response
    output = model.generate(input_ids=input_ids, max_length=1000, do_sample=True)
    response = tokenizer.decode(output[0], skip_special_tokens=True)
    return response.strip()

# Example usage
user_input = input("What's on your mind? ")
response = generate_response(user_input)
print(response)
