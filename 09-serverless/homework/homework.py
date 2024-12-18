#import tensorflow.lite as tflite
import numpy as np 
import tflite_runtime.interpreter as tflite
from keras_image_helper import create_preprocessor
import logging
import os
from io import BytesIO
from urllib import request

from PIL import Image
logging.basicConfig(level=logging.DEBUG)

# Model name
model_name = os.getenv('Model_Name', 'model_2024_hairstyle_v2.tflite')

interpreter = tflite.Interpreter(model_path=model_name)
interpreter.allocate_tensors()

input_index = interpreter.get_input_details()[0]['index']
output_index = interpreter.get_output_details()[0]['index']




def download_image(url):
    with request.urlopen(url) as resp:
        buffer = resp.read()
    stream = BytesIO(buffer)
    img = Image.open(stream)
    return img


def prepare_image(img, target_size):
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img = img.resize(target_size, Image.NEAREST)
    return img
def preprocess_input(x):
    
    return x/255.0

#url='https://habrastorage.org/webt/yf/_d/ok/yf_dokzqy3vcritme8ggnzqlvwa.jpeg'


def predict(url):
    try:
        logging.debug("Downloading the image...")
        img = download_image(url)
        logging.debug("Preparing the image...")
        img = prepare_image(img, target_size=(200, 200))

        logging.debug("Converting image to NumPy array...")
        x = np.array(img, dtype='float32')
        X = np.array([x])
        X = preprocess_input(X)

        logging.debug("Setting input tensor...")
        interpreter.set_tensor(input_index, X)
        interpreter.invoke()
        logging.debug("Getting prediction...")
        preds = interpreter.get_tensor(output_index)

        return float(preds[0, 0])

    except Exception as e:
        logging.error(f"Error in predict: {e}")
        raise


# def lambda_handler(event, context):
#     url = event['url']
#     pred = predict(url)

#     result ={
#         'prediction':pred
#     }


#     return result
def lambda_handler(event, context):
    logging.debug("Handler invoked")
    logging.debug(f"Received event: {event}")

    try:
        url = event['url']
        logging.debug(f"Processing URL: {url}")

        # Call predict
        pred = predict(url)
        logging.debug(f"Prediction result: {pred}")

        return {'prediction': pred}

    except Exception as e:
        logging.error(f"Error during processing: {e}")
        return {'error': str(e)}