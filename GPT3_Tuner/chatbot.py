import os
import openai
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model
from GPT3_Tuner.GPT_Param_Pred import param_prediction

def generate_response(user_prompt, temperature, max_tokens, top_p):
  if(temperature == float(0.1) and max_tokens == 1 and top_p == float(0.1)):
    temperature, max_tokens, top_p = param_prediction(user_prompt)
  openai.api_key = os.getenv('OPENAI_API')
  response = openai.Completion.create(
    model="text-davinci-003",
    prompt=user_prompt,
    temperature=temperature,              # This parameter controls creativity of the response.A higher value will produce more diverse result.
    max_tokens=int(max_tokens),           # This parameter represent maximum number of tokens in result
    top_p=top_p,                          # This parameter controls the narrowness of the generated response. A lower value lead to more coherent response.
    frequency_penalty=0.3,                # This both penalty parameter controls uniqueness of result. 
    presence_penalty=0.5                  # A higher freq_penalty model restrict the repeating words while a higher presence_penalty will encourage model to include words from user prompt.
  )

  #Extract and print response text
  response_text = response.choices[0].text
  return response_text