import os
import openai
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import load_model

def generate_response(user_prompt):
  vectorizer = CountVectorizer()
  OPENAI_API_KEY = os.getenv('OPENAI_API')
  data = pd.read_csv('prompt_dataset.csv')
  X_train = data['prompt']
  X_train_vec = vectorizer.fit_transform(X_train)
  Y_train_num = data[['temperature', 'max_tokens', 'top_p']].values


  # Get user input prompt
  model =  load_model('models/Seq_NN_GPT_Param.h5')
  # Vectorize the user prompt
  X_user_vec = vectorizer.transform([user_prompt])
  X_user_vec = X_user_vec.toarray()

  scaler = MinMaxScaler()
  Y_train_num_norm = scaler.fit_transform(Y_train_num)
  pred = model.predict(X_user_vec)
  pred = scaler.inverse_transform(pred)
  # Use the trained model to predict appropriate parameter values
  temperature, max_tokens, top_p = pred[0]

  # Print the predicted parameter values
  print('Recommended temperature:', temperature)
  print('Recommended max tokens:', int(max_tokens))
  print('Recommended top p:', top_p)

  openai.api_key = OPENAI_API_KEY
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