# import necessary libraries
from dataclasses import asdict
from transformers import GPT2LMHeadModel, GPT2Tokenizer, TrainingArguments, Trainer,DataCollatorForLanguageModeling,  LineByLineTextDataset

import torch
import random

# set up device for training (either CPU or GPU)
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# Load pre-trained GPT-3 model and tokenizer
model = GPT2LMHeadModel.from_pretrained("gpt2")
tokenizer = GPT2Tokenizer.from_pretrained("gpt2")
tokenizer.add_special_tokens({'pad_token': '$'})

# define a function to generate a response to user input
def generate_response(input_text, model):
    # encode the input text
    input_ids = tokenizer.encode(input_text, return_tensors='pt').to(device)

    # generate a response
    response_ids = model.generate(input_ids, max_length=140, do_sample=True, temperature=0.7)

    # decode the response and return it as a string
    response_text = tokenizer.decode(response_ids[0], skip_special_tokens=True)
    return response_text

# load the pre-trained GPT-3 model
model = GPT2LMHeadModel.from_pretrained("gpt2").to(device)

# load the dataset and split it into training and validation sets
dataset = [
    ("Hi, how are you?", "I'm good, thanks for asking."),
    ("What's the weather like today?", "It looks like it's going to rain."),
    ("Can you recommend a good restaurant?", "Sure, I'd recommend trying the Italian place on Main Street."),
    ("How do I get to the nearest train station?", "You can take the bus from here and then transfer to the train."),
    ("What's your favorite book?", "I'm an AI language model, so I don't have a favorite book, but I can recommend some if you'd like."),
    ("What's the meaning of life?", "That's a deep question. What do you think it means?"),
    ("What's the capital of France?", "The capital of France is Paris."),
    ("How do you say 'hello' in Spanish?", "The Spanish word for 'hello' is 'hola'.")
]
random.shuffle(dataset)
#train_dataset = dataset[:int(len(dataset)*0.8)]
#val_dataset = dataset[int(len(dataset)*0.8):]

train_dataset = LineByLineTextDataset(
    tokenizer=tokenizer,
    file_path="./chat_data.txt",
    block_size=128,
)

# define the training arguments
training_args = TrainingArguments(
    output_dir='./results',          # output directory
    num_train_epochs=3,              # total number of training epochs
    per_device_train_batch_size=8,   # batch size per device during training
    per_device_eval_batch_size=8,    # batch size for evaluation
    learning_rate=5e-5,              # learning rate
    weight_decay=0.01,               # weight decay
    save_total_limit=5,              # limit on the total number of checkpoints to save
    logging_dir='./logs',            # directory for storing logs
    logging_steps=500,               # log every n steps
    evaluation_strategy='steps',     # evaluate every eval_steps
    eval_steps=1000                  # evaluation steps
)

# Define data collator for language modeling
data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, 
    mlm=False
)

# define the trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=(train_dataset),
    data_collator=data_collator)

# fine-tune the model
trainer.train()

# use the model to generate responses to user input
input_text = "How to make coffee?"
response_text = generate_response(input_text, model)
print(response_text)
