import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.regularizers import l2
from tensorflow.keras.callbacks import EarlyStopping
from tensorflow.keras.models import load_model
from sklearn.feature_extraction.text import CountVectorizer


def generate_model():
    # Load the dataset
    data = pd.read_csv('GPT3_Tuner/prompt_dataset.csv')

    # Split the data into training and testing sets
    X_train = data['prompt']
    y_train = data[['temperature', 'max_tokens', 'top_p']].values
    Y_train_num = data[['temperature', 'max_tokens', 'top_p']].values

    # Load pre-trained word embeddings
    vectorizer = CountVectorizer()
    X_train_vec = vectorizer.fit_transform(X_train)
    X_train_vec = X_train_vec.toarray()

    scaler = MinMaxScaler()
    Y_train_num_norm = scaler.fit_transform(Y_train_num)

    # Define the neural network architecture
    model = Sequential([
        Dense(128, activation='relu', input_dim=X_train_vec.shape[1], kernel_regularizer=l2(0.01)),
        Dropout(0.2),
        Dense(64, activation='relu', kernel_regularizer=l2(0.01)),
        Dropout(0.2),
        Dense(3, activation='linear')
    ])

    # Compile the model
    model.compile(loss='mean_absolute_error', optimizer=RMSprop(lr=0.001))

    # Set up early stopping e=10, restore_best_weights=True)
    early_stop = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)

    # Train the model
    history = model.fit(X_train_vec, Y_train_num_norm, validation_split=0.2, epochs=130, batch_size=16, callbacks=[early_stop])

    # Save the model for further use
    model.save('GPT3_Tuner/models/Seq_NN_GPT_Param.h5')
    
def param_prediction(user_prompt):
    vectorizer = CountVectorizer()
    data = pd.read_csv('GPT3_Tuner/prompt_dataset.csv')
    X_train = data['prompt']
    X_train_vec = vectorizer.fit_transform(X_train)
    Y_train_num = data[['temperature', 'max_tokens', 'top_p']].values


    # Get user input prompt
    model =  load_model('GPT3_Tuner/models/Seq_NN_GPT_Param.h5')
    # Vectorize the user prompt
    X_user_vec = vectorizer.transform([user_prompt])
    X_user_vec = X_user_vec.toarray()

    scaler = MinMaxScaler()
    Y_train_num_norm = scaler.fit_transform(Y_train_num)
    pred = model.predict(X_user_vec)
    pred = scaler.inverse_transform(pred)
    # Use the trained model to predict appropriate parameter values
    temperature, max_tokens, top_p = pred[0]
    print(temperature)
    print(int(max_tokens))
    print(top_p)
    return temperature, int(max_tokens), top_p
