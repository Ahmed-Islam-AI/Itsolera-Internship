#Importing necessory libraries
import tensorflow as tf
from tensorflow import keras
import pickle as pkl
import cv2
import numpy as np
import transformers


#Models
__text_model=None
__image_model=None
__tokenizer=None

#Define a function to load models
def load_saved_artifects():
    global __text_model
    global __image_model
    global __tokenizer

    print("Loading Saved Artifects -----Start")
    __text_model=keras.models.load_model("text_moderation_model.h5")            # Text model file path
    __image_model=keras.models.load_model("saved_model.keras")                 #image model file path                        

    with open("tokenizer.pkl",'rb') as f:
        __tokenizer=pkl.load(f)
    print("Loading Saved Artifects  -----Done")

 #Define a function for text classification   
def text_moderation(text):
    
    classes=['Positive','Negative']
    encoded_inputs = __tokenizer(
    text,
    max_length=10,  
    padding='max_length',
    truncation=True,
    return_tensors='tf')

    X_test_ids_new = np.array(encoded_inputs['input_ids'], dtype=np.int32)
    X_attention_mask_new = np.array(encoded_inputs['attention_mask'], dtype=np.int32)

    predictions = __text_model.predict([X_test_ids_new, X_attention_mask_new])
    threshold=0.5
    preds=[1 if predictions > threshold else 0]

    return  f"Prediction : {classes[preds[0]]}",preds[0]

    
#Define a function for image classifiation
def image_moderation(image_path):

    classes=["Safe","Violent"]
    img=cv2.imread(image_path)
    resize_image=cv2.resize(img,(224,224))
    image=resize_image.reshape(1,224,224,3)
    preds=__image_model.predict(image)
    threshold=0.5
    prediction=[1 if preds > threshold else 0]

    return f"Prediction : {classes[prediction[0]]}"

if __name__ == "__main__":
    pass