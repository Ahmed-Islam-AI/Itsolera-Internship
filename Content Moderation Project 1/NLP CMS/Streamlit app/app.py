import streamlit as st
import numpy as np
import pickle
from tensorflow.keras.models import load_model

# Load the saved model and tokenizer
@st.cache_resource
def load_model_and_tokenizer():
    model = load_model('saved_model/text_moderation_model.h5')
    with open('saved_model/tokenizer.pkl', 'rb') as f:
        tokenizer = pickle.load(f)
    return model, tokenizer

loaded_model, loaded_tokenizer = load_model_and_tokenizer()

st.title('Text Moderation Prediction')

# User input
user_input = st.text_area('Enter a sentence:', '')

if st.button('Predict'):
    # Tokenize and preprocess the text
    encoded_inputs = loaded_tokenizer(
        [user_input],
        max_length=10,  # Use the same max_length as during training
        padding='max_length',
        truncation=True,
        return_tensors='tf'
    )

    X_test_ids_new = np.array(encoded_inputs['input_ids'], dtype=np.int32)
    X_attention_mask_new = np.array(encoded_inputs['attention_mask'], dtype=np.int32)

    # Predict using the loaded model
    predictions = loaded_model.predict([X_test_ids_new, X_attention_mask_new])

    # Convert prediction to "negative" or "positive"
    threshold = 0.5  # Typical threshold for binary classification
    prediction_label = ["negative" if pred > threshold else "positive" for pred in predictions]

    st.write(f"Text: {user_input}")
    st.write(f"Prediction: {prediction_label[0]}")
    st.write(f"Prediction Score: {predictions[0][0]}")

